import os
from celery import Celery

from src.services.qa_summary import generate_scalable_summary
from src.services.qa_suggestions import SUGGESTIONS_PROMPT, clean_suggestions
from src.services.dynamic_evaluator import check_auto_fail, calculate_category_scores, parse_dynamic_ratings

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
app = Celery('amalgamation_worker', broker=REDIS_URL, backend=REDIS_URL)

@app.task(name='amalgamation_finalize_report')
def finalize_report(llm_results, logic_results, transcript_text, criteria_data):
    # Merge Logic results into llm ratings
    ratings = logic_results + llm_results
    
    categories = criteria_data.get('categories', [])
    category_weights = criteria_data.get('category_weights', {})
    auto_fail_rules = criteria_data.get('auto_fail_rules', [])
    
    is_auto_fail, auto_fail_reason = check_auto_fail(transcript_text, [], auto_fail_rules, ratings)
    category_scores, blended_score = calculate_category_scores(ratings, category_weights, is_auto_fail)
    
    # Generate Summary
    audit_context_lines = []
    if is_auto_fail:
        audit_context_lines.append(f"CRITICAL AUTO-FAIL TRIGGERED: {auto_fail_reason}")
    for r in ratings:
        if r['rating'] in ['NO', 'FAIL']:
            audit_context_lines.append(f"FAILED CHECK - {r['name']}: {r['reason']}")
    
    evaluation_context_str = "\n".join(audit_context_lines) if audit_context_lines else "No critical failures identified. The agent passed all checks."
    summary = generate_scalable_summary(transcript_text, evaluation_context=evaluation_context_str)
    
    # Returning the final payload
    return {
        "final_score": blended_score,
        "is_auto_fail": is_auto_fail,
        "auto_fail_reason": auto_fail_reason,
        "category_scores": category_scores,
        "scorecard": ratings,
        "summary": summary,
        "suggestions": "Suggestions generation deferred to async or llm worker for speed."
    }

