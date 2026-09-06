"""Stateless WEB VERSION of the QA analysis API.

Run with: uvicorn src.api.web_app:app --host 0.0.0.0 --port 8000
"""

import os
import sys
import json

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
for _path in [_ROOT, _SRC]:
    if _path not in sys.path:
        sys.path.insert(0, _path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from src.services.dynamic_evaluator import evaluate_interaction, preview_evaluation_prompt

app = FastAPI(title="Stateless QA Service API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EvaluateRequest(BaseModel):
    transcript: str
    channel: Optional[str] = "Call"
    agent_name: Optional[str] = "Agent"
    custom_prompt: Optional[str] = None

@app.get("/api/samples")
def list_sample_inputs():
    """List and return all sample conversation JSON files from the inputs/ folder."""
    inputs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputs")
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
                    print(f"Error loading sample {fname}: {e}")
    return samples

@app.post("/api/evaluate")
def evaluate_tenant_transcript(req: EvaluateRequest):
    """Run dynamic QA analysis on a transcript using stateless criteria."""
    # Criteria is now fully encapsulated within dynamic_evaluator.py ruleset
    criteria_data = {}

    result = evaluate_interaction(
        transcript_text=req.transcript,
        criteria_data=criteria_data,
        tenant_id="default",
        channel=req.channel or "Call",
        custom_prompt=req.custom_prompt
    )

    import uuid
    import datetime
    result["evaluation_id"] = str(uuid.uuid4())
    result["created_at"] = datetime.datetime.utcnow().isoformat()
    return result

@app.post("/api/preview-prompt")
def preview_tenant_prompt(req: EvaluateRequest):
    """Build and preview the exact LLM prompt without executing evaluation."""
    criteria_data = {}
    preview = preview_evaluation_prompt(
        transcript_text=req.transcript,
        criteria_data=criteria_data,
        tenant_id="default",
        channel=req.channel or "Call"
    )
    return preview

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    load_dotenv()

    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)

