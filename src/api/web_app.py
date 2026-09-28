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

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.api.logger import logger
from src.services.dynamic_evaluator import preview_evaluation_prompt, evaluate_interaction

app = FastAPI(title="Stateless QA Service API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    try:
        init_db()
    except Exception as e:
        logger.error({"log_type": "APP", "message": f"Failed to initialize database: {e}"})
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

    req_body_bytes = await request.body()
    try:
        req_body = json.loads(req_body_bytes)
    except Exception:
        req_body = req_body_bytes.decode("utf-8", errors="replace") if req_body_bytes else {}

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
    speaker: str
    text: str
    start_time_sec: Optional[int] = 0
    sentiment_score: Optional[float] = 0.0


class EvaluateRequest(BaseModel):
    transcript: Union[List[Turn], str]
    criteria_data: Optional[Dict[str, Any]] = None
    tenant_id: Optional[str] = None
    tenantId: Optional[str] = None
    call_id: Optional[str] = None
    callId: Optional[str] = None
    channel: Optional[str] = "Call"
    agent_name: Optional[str] = "Agent"
    custom_prompt: Optional[str] = None
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


@app.get("/api/samples")
def list_sample_inputs():
    inputs_dir = os.path.join(_ROOT, "inputs")
    samples = []
    if os.path.exists(inputs_dir):
        for fname in sorted(os.listdir(inputs_dir)):
            if fname.endswith(".json"):
                fpath = os.path.join(inputs_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        data["filename"] = fname
                        samples.append(data)
                except Exception as e:
                    logger.error({"message": f"Error loading sample {fname}: {e}"})
    return samples


@app.post("/api/evaluate")
def evaluate_tenant_transcript(req: EvaluateRequest):
    """Synchronous evaluation endpoint using PostgreSQL tenant criteria."""
    tenant_id = req.get_tenant_id()
    call_id = req.get_call_id()
    criteria_data = req.criteria_data or get_active_criteria_for_evaluation(tenant_id)
    transcript_payload = [t.dict() for t in req.transcript] if isinstance(req.transcript, list) else req.transcript

    result = evaluate_interaction(
        transcript_data=transcript_payload,
        criteria_data=criteria_data,
        tenant_id=tenant_id,
        channel=req.channel or "Call",
        custom_prompt=req.custom_prompt,
        caller=req.get_customer_name()
    )

    return {
        "call_id": call_id,
        "tenant_id": tenant_id,
        "status": "completed",
        "result": result
    }


@app.post("/api/preview-prompt")
def preview_tenant_prompt(req: EvaluateRequest):
    tenant_id = req.get_tenant_id()
    criteria_data = req.criteria_data or get_active_criteria_for_evaluation(tenant_id)
    preview = preview_evaluation_prompt(
        transcript_text=req.transcript,
        criteria_data=criteria_data,
        tenant_id=tenant_id,
        channel=req.channel or "Call"
    )
    return preview


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
