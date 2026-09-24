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

    # 1. Safely read and parse request body
    req_body_bytes = await request.body()
    try:
        req_body = json.loads(req_body_bytes)
    except Exception:
        req_body = req_body_bytes.decode("utf-8", errors="replace") if req_body_bytes else {}

    # 2. Log incoming request as single-line JSON
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

        # 3. Safely capture response body
        res_body_bytes = b""
        async for chunk in response.body_iterator:
            res_body_bytes += chunk

        try:
            res_body = json.loads(res_body_bytes)
        except Exception:
            res_body = res_body_bytes.decode("utf-8", errors="replace") if res_body_bytes else {}

        latency_ms = round((time.time() - start_time) * 1000, 2)
        outcome = "SUCCESS" if 200 <= response.status_code < 400 else "FAILURE"

        # 4. Log outgoing response as single-line JSON
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


CRITERIA_FILE = os.path.join(_ROOT, "resources", "criteria_config.json")


def load_criteria(tenant_id: str) -> Dict[str, Any]:
    """Load rubric criteria from local JSON configuration file."""
    if os.path.exists(CRITERIA_FILE):
        try:
            with open(CRITERIA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get(tenant_id, data.get("tenant-abc", {}))
        except Exception as e:
            logger.warning({"message": f"Could not read criteria from {CRITERIA_FILE}: {e}"})
    return {}


class Turn(BaseModel):
    speaker: str
    text: str
    start_time_sec: Optional[int] = 0
    sentiment_score: Optional[float] = 0.0


class EvaluateRequest(BaseModel):
    transcript: Union[List[Turn], str]
    criteria_data: Optional[Dict[str, Any]] = None
    tenant_id: Optional[str] = "default"
    channel: Optional[str] = "Call"
    agent_name: Optional[str] = "Agent"
    custom_prompt: Optional[str] = None
    customer_name: Optional[str] = None


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
    """Synchronous evaluation endpoint using local criteria config and in-process execution."""
    criteria_data = req.criteria_data or load_criteria(req.tenant_id or "tenant-abc")
    transcript_payload = [t.dict() for t in req.transcript] if isinstance(req.transcript, list) else req.transcript

    result = evaluate_interaction(
        transcript_data=transcript_payload,
        criteria_data=criteria_data,
        tenant_id=req.tenant_id or "default",
        channel=req.channel or "Call",
        custom_prompt=req.custom_prompt,
        caller=req.customer_name
    )

    return {
        "status": "completed",
        "result": result
    }


@app.post("/api/preview-prompt")
def preview_tenant_prompt(req: EvaluateRequest):
    criteria_data = req.criteria_data or load_criteria(req.tenant_id or "tenant-abc")
    preview = preview_evaluation_prompt(
        transcript_text=req.transcript,
        criteria_data=criteria_data,
        tenant_id=req.tenant_id or "default",
        channel=req.channel or "Call"
    )
    return preview


if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    load_dotenv()

    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8000"))
    logger.info({
        "log_type": "APP",
        "message": f"Starting server directly on http://{host}:{port}..."
    })
    uvicorn.run(app, host=host, port=port)
