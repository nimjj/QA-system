import os
from celery import Celery
from src.services.rule_engine import evaluate_branding, evaluate_hold_and_dead_air

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
app = Celery('logic_worker', broker=REDIS_URL, backend=REDIS_URL)

@app.task(name='logic_evaluate_branding')
def task_evaluate_branding(turns):
    return evaluate_branding(turns)

@app.task(name='logic_evaluate_hold')
def task_evaluate_hold_and_dead_air(turns, parsed_times):
    return evaluate_hold_and_dead_air(turns, parsed_times)

