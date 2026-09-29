"""Root launcher for the API Gateway (port 8005)."""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    load_dotenv()

    host = os.getenv("GATEWAY_HOST", "0.0.0.0")
    port = int(os.getenv("GATEWAY_PORT", 8005))
    target = os.getenv("APP_URL", "http://localhost:8006")

    print(f"============================================================")
    print(f" Starting API Gateway on http://{host}:{port}")
    print(f" Routing /api/* requests to Backend App at: {target}")
    print(f"============================================================")

    from src.gateway.gateway_app import gateway
    uvicorn.run(gateway, host=host, port=port)
