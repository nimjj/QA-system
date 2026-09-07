import os
from celery import Celery
from src.services.llm_adapter import get_llm

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
app = Celery('llm_worker', broker=REDIS_URL, backend=REDIS_URL)

@app.task(name='llm_generate')
def generate_text(prompt: str, **kwargs):
    llm = get_llm()
    return llm.generate(prompt, **kwargs)

