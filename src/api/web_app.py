import os
import sys
import json
import time
import uuid
import traceback
from datetime import datetime, timezone
from typing import Optional, List, Union, Dict, Any

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
for _path in [_ROOT, _SRC]:
    if _path not in sys.path:
        sys.path.insert(0, _path)

import hmac
import threading

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.api.logger import logger
from src.services.dynamic_evaluator import evaluate_interaction

app = FastAPI(title="Stateless QA Service API")

# CORS_ORIGINS="https://a.example,https://b.example" restricts browsers to those sites; unset keeps the old "any origin" behaviour (no cookies)
_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()] or ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_ORIGINS,
    allow_credentials=_ORIGINS != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_REQUEST_BYTES = int(os.getenv("MAX_REQUEST_BYTES", str(2_000_000)))
LOG_REQUEST_BODIES = os.getenv("LOG_REQUEST_BODIES", "").strip().lower() in ("1", "true", "yes", "on")


def _api_key_ok(request: Request) -> bool:
    """With QA_API_KEY set, every /api/ call must send it in the x-api-key header. Unset keeps the service open, as before."""
    key = os.getenv("QA_API_KEY", "")
    if not key or not request.url.path.startswith("/api/"):
        return True
    return hmac.compare_digest(request.headers.get("x-api-key", "").encode(), key.encode())


def _safe_body(body: Any) -> Any:
    """What the request log may keep. Transcripts and customer names are personal data: log their size, not their words
    (LOG_REQUEST_BODIES=1 restores full bodies for debugging on a machine that holds no real calls)."""
    if LOG_REQUEST_BODIES:
        return body
    if not isinstance(body, dict):
        return {"omitted_chars": len(str(body))} if body else body
    out = dict(body)
    tx = out.get("transcript")
    if isinstance(tx, list):
        out["transcript"] = {"turns": len(tx), "chars": sum(len(str((t or {}).get("text", ""))) if isinstance(t, dict) else len(str(t)) for t in tx)}
    elif isinstance(tx, str):
        out["transcript"] = {"chars": len(tx)}
    for k in ("customer_name", "customerName", "agent_name"):
        if out.get(k):
            out[k] = "[redacted]"
    return out


@app.get("/health")
def health_check():
    """Liveness only: the process is up. Use /ready to know whether it can grade."""
    return {
        "status": "healthy",
        "service": "qa-service"
    }


_model_ready = False
_model_load_error: Optional[str] = None


@app.get("/ready")
def readiness_check():
    """Readiness. Flow v3: the model has loaded. Other flows: the criteria database answers."""
    out = {"status": "ready", "flow": os.getenv("LAYA_FLOW", "").strip().lower() or "default"}
    if not _v3_enabled():
        try:
            get_all_tenants()
        except Exception as e:
            logger.error({"log_type": "APP", "message": f"readiness: database not reachable: {type(e).__name__}"})
            return JSONResponse(status_code=503, content={"status": "not ready", "database": "unreachable"})
        out["database"] = "ok"
    else:
        if not _model_ready:
            out["status"] = "model failed to load" if _model_load_error else "model loading"
            if _model_load_error:
                out["load_error"] = _model_load_error
            return JSONResponse(status_code=503, content=out)
        out["model_ready"] = True
    return out


@app.on_event("startup")
def on_startup():
    global _model_ready, _model_load_error
    if _v3_enabled():
        logger.info({
            "log_type": "APP",
            "message": "Initializing model weights and warming up..."
        })
        try:
            _warm_model()
            _model_ready = True
            logger.info({
                "log_type": "APP",
                "message": "Model loaded successfully. Service ready."
            })
        except Exception as e:
            _model_load_error = f"{type(e).__name__}: {e}"
            logger.error({
                "log_type": "APP",
                "message": f"Model failed to load during startup: {_model_load_error}"
            })
    else:
        try:
            init_db()
        except Exception as e:
            logger.error({"log_type": "APP", "message": f"Failed to initialize database: {e}"})
        try:
            _warm_model()
            _model_ready = True
        except Exception as e:
            logger.warning({"log_type": "APP", "message": f"Model warmup skipped: {e}"})

    logger.info({
        "log_type": "APP",
        "message": "Stateless QA Service started. Logging live to logs/app.log."
    })


@app.on_event("shutdown")
def on_shutdown():
    logger.info({
        "log_type": "APP",
        "message": "Stateless QA Service shutting down."
    })


@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()
    correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    method = request.method
    path = request.url.path
    query_params = dict(request.query_params)

    if not _api_key_ok(request):
        return JSONResponse(status_code=401, content={"detail": "missing or wrong x-api-key"})
    declared = request.headers.get("content-length", "")
    if declared.isdigit() and int(declared) > MAX_REQUEST_BYTES:
        return JSONResponse(status_code=413, content={"detail": f"request larger than {MAX_REQUEST_BYTES} bytes"})
    req_body_bytes = await request.body()
    if len(req_body_bytes) > MAX_REQUEST_BYTES:
        return JSONResponse(status_code=413, content={"detail": f"request larger than {MAX_REQUEST_BYTES} bytes"})
    try:
        req_body = _safe_body(json.loads(req_body_bytes))
    except Exception:
        req_body = _safe_body(req_body_bytes.decode("utf-8", errors="replace") if req_body_bytes else {})

    logger.info({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "log_type": "INCOMING",
        "correlation_id": correlation_id,
        "actor": {
            "ip": client_ip,
            "user_agent": user_agent
        },
        "request": {
            "method": method,
            "path": path,
            "query_params": query_params,
            "body": req_body
        }
    })

    try:
        response = await call_next(request)

        res_body_bytes = b""
        async for chunk in response.body_iterator:
            res_body_bytes += chunk

        try:
            res_body = json.loads(res_body_bytes)
        except Exception:
            res_body = res_body_bytes.decode("utf-8", errors="replace") if res_body_bytes else {}
        if not LOG_REQUEST_BODIES and len(res_body_bytes) > 20_000:       # e.g. /api/samples returns whole transcripts
            res_body = {"omitted_bytes": len(res_body_bytes)}

        latency_ms = round((time.time() - start_time) * 1000, 2)
        outcome = "SUCCESS" if 200 <= response.status_code < 400 else "FAILURE"

        logger.info({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "log_type": "OUTGOING",
            "correlation_id": correlation_id,
            "actor": {
                "ip": client_ip,
                "user_agent": user_agent
            },
            "request": {
                "method": method,
                "path": path,
                "query_params": query_params
            },
            "response": {
                "status_code": response.status_code,
                "outcome": outcome,
                "latency_ms": latency_ms,
                "body": res_body
            }
        })

        headers = dict(response.headers)
        headers.pop("content-length", None)
        headers["x-correlation-id"] = correlation_id
        return Response(
            content=res_body_bytes,
            status_code=response.status_code,
            headers=headers,
            media_type=response.media_type
        )
    except Exception as exc:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        logger.error({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "log_type": "ERROR",
            "correlation_id": correlation_id,
            "actor": {
                "ip": client_ip,
                "user_agent": user_agent
            },
            "request": {
                "method": method,
                "path": path,
                "query_params": query_params,
                "body": req_body
            },
            "response": {
                "status_code": 500,
                "outcome": "FAILURE",
                "latency_ms": latency_ms
            },
            "error": str(exc),
            "traceback": traceback.format_exc()
        })
        raise exc


from src.db.database import (
    init_db,
    get_all_tenants,
    create_tenant as db_create_tenant,
    create_category as db_create_category,
    get_categories as db_get_categories,
    get_tenant_criteria,
    get_active_criteria_for_evaluation,
    toggle_tenant_criterion,
    get_all_criteria,
    create_criterion as db_create_criterion,
    update_criterion as db_update_criterion,
    delete_criterion as db_delete_criterion
)


class Turn(BaseModel):
    # seconds may arrive as 12.5, "1:12" or null; sentiment may be null. v3 reads them as sent, v2 gets the old int / float defaults below.
    speaker: str
    text: Optional[str] = ""
    start_time_sec: Optional[Union[float, str]] = 0
    end_time: Optional[Union[float, str]] = None
    end_time_sec: Optional[Union[float, str]] = None
    sentiment_score: Optional[float] = 0.0


def _v2_turn(t: "Turn") -> Dict[str, Any]:
    """The turn as v2 has always received it (int start second, 0.0 for a missing score)."""
    d = t.model_dump()
    try:
        d["start_time_sec"] = int(float(d["start_time_sec"] or 0))
    except (TypeError, ValueError):
        d["start_time_sec"] = 0
    d["text"] = d["text"] or ""
    d["sentiment_score"] = d["sentiment_score"] if d["sentiment_score"] is not None else 0.0
    return d


class EvaluateRequest(BaseModel):
    transcript: Union[List[Turn], str]
    criteria_data: Optional[Dict[str, Any]] = None
    tenant_id: Optional[str] = None
    tenantId: Optional[str] = None
    call_id: Optional[str] = None
    callId: Optional[str] = None
    channel: Optional[str] = "Call"
    agent_name: Optional[str] = "Agent"
    customer_name: Optional[str] = None
    customerName: Optional[str] = None

    def get_tenant_id(self) -> str:
        return self.tenant_id or self.tenantId or "tenant-abc"

    def get_call_id(self) -> str:
        return self.call_id or self.callId or f"call_{uuid.uuid4().hex[:10]}"

    def get_customer_name(self) -> Optional[str]:
        return self.customer_name or self.customerName


class CreateTenantRequest(BaseModel):
    tenant_id: str
    name: str


class ToggleCriterionRequest(BaseModel):
    is_active: bool


class CreateCategoryRequest(BaseModel):
    category_id: Optional[str] = None
    tenant_id: str
    name: str
    category_weight: Optional[float] = 1.0


class CreateCriterionRequest(BaseModel):
    category_id: str
    name: str
    description: Optional[str] = ""
    deduction_value: Optional[int] = 10
    line_item_id: Optional[str] = None


class UpdateCriterionRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    deduction_value: Optional[int] = 10


@app.get("/api/tenants")
def list_tenants():
    return get_all_tenants()


@app.post("/api/tenants")
def add_tenant(req: CreateTenantRequest):
    return db_create_tenant(req.tenant_id, req.name)


@app.get("/api/categories")
def list_categories(tenant_id: Optional[str] = None):
    return db_get_categories(tenant_id)


@app.post("/api/categories")
def add_category(req: CreateCategoryRequest):
    return db_create_category(req.category_id, req.tenant_id, req.name, req.category_weight or 1.0)


@app.get("/api/tenants/{tenant_id}/criteria")
def get_criteria_for_tenant(tenant_id: str):
    return get_tenant_criteria(tenant_id)


@app.patch("/api/tenants/{tenant_id}/criteria/{line_item_id}/toggle")
@app.post("/api/tenants/{tenant_id}/criteria/{line_item_id}/toggle")
def toggle_criterion(tenant_id: str, line_item_id: str, req: ToggleCriterionRequest):
    return toggle_tenant_criterion(tenant_id, line_item_id, req.is_active)


@app.get("/api/criteria")
def list_all_criteria():
    return get_all_criteria()


@app.post("/api/criteria")
def create_new_criterion(req: CreateCriterionRequest):
    return db_create_criterion(req.category_id, req.name, req.description, req.deduction_value, req.line_item_id)


@app.put("/api/criteria/{line_item_id}")
def update_existing_criterion(line_item_id: str, req: UpdateCriterionRequest):
    updated = db_update_criterion(line_item_id, req.name, req.description, req.deduction_value)
    if not updated:
        raise HTTPException(status_code=404, detail="Criterion not found")
    return updated


@app.delete("/api/criteria/{line_item_id}")
def delete_existing_criterion(line_item_id: str):
    deleted = db_delete_criterion(line_item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Criterion not found")
    return {"status": "deleted", "line_item_id": line_item_id}


SAMPLE_DIRS = ["Main tests", "Bulk tests"]


@app.get("/api/samples")
def list_sample_inputs():
    """Sample call payloads from inputs/Main tests and inputs/Bulk tests (expected/ grades are skipped)."""
    inputs_dir = os.path.join(_ROOT, "inputs")
    samples = []
    for sub in SAMPLE_DIRS:
        sample_dir = os.path.join(inputs_dir, sub)
        for dirpath, dirnames, filenames in os.walk(sample_dir):
            dirnames[:] = sorted(d for d in dirnames if d.lower() != "expected")
            for fname in sorted(filenames):
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(dirpath, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception as e:
                    logger.error({"message": f"Error loading sample {fname}: {e}"})
                    continue
                if isinstance(data, dict) and data.get("transcript"):
                    data["filename"] = os.path.relpath(fpath, inputs_dir).replace(os.sep, "/")
                    samples.append(data)
    return samples


def _v3_enabled() -> bool:
    return os.getenv("LAYA_FLOW", "").strip().lower() == "v3"


def _error_status(exc: BaseException) -> Optional[int]:
    """HTTP status for the input problems v3 knows about; None for anything else (reported as a generic 500)."""
    from src.v3.normalise import InvalidTranscript, TranscriptTooLarge
    from src.v3.scoring import NoCriteria
    if isinstance(exc, (InvalidTranscript, NoCriteria)):
        return 422
    if isinstance(exc, TranscriptTooLarge):
        return 413
    return None


def _warm_model() -> None:
    """Load the weights and answer one real question, so a bad checkpoint path or a broken install fails at startup, not on the first call."""
    from src.services import dynamic_evaluator as de
    de._laya_verdict("probing", "Agent: Can you tell me when the problem first started?\nCustomer: Yesterday evening.", "warmup")


@app.post("/api/evaluate")
def evaluate_tenant_transcript(req: EvaluateRequest):
    """Synchronous evaluation endpoint for call interactions."""
    tenant_id = req.get_tenant_id()
    call_id = req.get_call_id()

    if _v3_enabled():
        if not _model_ready:
            if _model_load_error:
                detail = (f"model failed to load: {_model_load_error}. Check that the weights are in "
                          "models/final-softce-3 (python Scripts/verify_weights.py) and restart the service.")
            else:
                detail = "model is still loading; try again in a few seconds (GET /ready says when it is done)."
            raise HTTPException(status_code=503, headers={"Retry-After": "30"}, detail=detail)
        from src.v3.pipeline import evaluate_v3
        from src.v3.normalise import normalise
        from src.v3 import load_criteria

        criteria_data = None
        if tenant_id:
            try:
                criteria_data = get_active_criteria_for_evaluation(tenant_id)
            except Exception:
                criteria_data = None
        if not criteria_data:
            criteria_data = load_criteria()

        payload = [t.model_dump() for t in req.transcript] if isinstance(req.transcript, list) else req.transcript
        try:
            normalise(payload, req.get_customer_name())
        except Exception as e:
            code = _error_status(e)
            if code is None:
                raise
            raise HTTPException(status_code=code, detail=str(e))

        result = evaluate_v3(payload, criteria_data, tenant_id, req.channel or "Call", req.get_customer_name())
        return {
            "call_id": call_id,
            "tenant_id": tenant_id,
            "status": "completed",
            "result": result
        }

    criteria_data = req.criteria_data or get_active_criteria_for_evaluation(tenant_id)
    transcript_payload = [_v2_turn(t) for t in req.transcript] if isinstance(req.transcript, list) else req.transcript

    result = evaluate_interaction(
        transcript_data=transcript_payload,
        criteria_data=criteria_data,
        tenant_id=tenant_id,
        channel=req.channel or "Call",
        caller=req.get_customer_name()
    )

    return {
        "call_id": call_id,
        "tenant_id": tenant_id,
        "status": "completed",
        "result": result
    }


if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    load_dotenv()

    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8006"))
    logger.info({
        "log_type": "APP",
        "message": f"Starting server directly on http://{host}:{port}..."
    })
    uvicorn.run(app, host=host, port=port)
