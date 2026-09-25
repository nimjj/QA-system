"""API Gateway for QA System.
Runs on port 8005 by default and routes incoming traffic to core FastAPI App (port 8000).
Also has direct DB access for fast querying as shown in the system architecture.
"""

import os
import sys
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Ensure root and src are on sys.path
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
for _p in [_ROOT, _SRC]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

load_dotenv()

APP_URL = os.getenv("APP_URL", "http://localhost:8000").rstrip("/")
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


@gateway.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "api-gateway",
        "target_app": APP_URL
    }


@gateway.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
async def route_api_request(request: Request, path: str):
    """Transparently proxies incoming /api/ requests to the backend App on port 8000."""
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
                content=b'{"error": "Backend QA Service unavailable on port 8000. Is main.py running?"}',
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
    print(f"Starting API Gateway on http://{GATEWAY_HOST}:{GATEWAY_PORT} -> forwarding to {APP_URL}...")
    uvicorn.run(gateway, host=GATEWAY_HOST, port=GATEWAY_PORT)
