import os
import sys
import httpx
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
for _p in [_ROOT, _SRC]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from src.db.database import get_tenant_criteria, toggle_tenant_criterion

load_dotenv()

APP_URL = os.getenv("APP_URL", "http://localhost:8006").rstrip("/")
GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", "8005"))
GATEWAY_HOST = os.getenv("GATEWAY_HOST", "0.0.0.0")

gateway = FastAPI(title="QA System API Gateway", version="1.0.0")

gateway.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ToggleCriterionRequest(BaseModel):
    is_active: bool


@gateway.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "api-gateway",
        "target_app": APP_URL
    }


@gateway.get("/api/tenants/{tenant_id}/criteria")
def get_criteria_for_tenant(tenant_id: str):
    try:
        return get_tenant_criteria(tenant_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@gateway.patch("/api/tenants/{tenant_id}/criteria/{line_item_id}/toggle")
@gateway.post("/api/tenants/{tenant_id}/criteria/{line_item_id}/toggle")
def toggle_criterion(tenant_id: str, line_item_id: str, req: ToggleCriterionRequest):
    try:
        return toggle_tenant_criterion(tenant_id, line_item_id, req.is_active)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@gateway.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
async def route_api_request(request: Request, path: str):
    target_url = f"{APP_URL}/api/{path}"
    
    body = await request.body()
    query_params = request.url.query
    if query_params:
        target_url = f"{target_url}?{query_params}"

    excluded_headers = {"host", "content-length", "connection"}
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in excluded_headers
    }

    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            backend_resp = await client.request(
                method=request.method,
                url=target_url,
                content=body,
                headers=headers
            )
            
            resp_headers = dict(backend_resp.headers)
            resp_headers.pop("content-length", None)
            resp_headers.pop("transfer-encoding", None)

            return Response(
                content=backend_resp.content,
                status_code=backend_resp.status_code,
                headers=resp_headers,
                media_type=backend_resp.headers.get("content-type")
            )
        except httpx.ConnectError:
            return Response(
                content=b'{"error": "Backend QA Service unavailable on port 8006. Is main.py running?"}',
                status_code=503,
                media_type="application/json"
            )
        except Exception as e:
            return Response(
                content=f'{{"error": "Gateway proxy error: {str(e)}"}}'.encode("utf-8"),
                status_code=502,
                media_type="application/json"
            )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(gateway, host=GATEWAY_HOST, port=GATEWAY_PORT)
