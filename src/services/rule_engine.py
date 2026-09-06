from typing import List, Tuple, Optional, Dict, Any
import difflib

def similar(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def evaluate_branding(turns: List[Tuple[str, str]]) -> Dict[str, Any]:
    agent_lines = [txt for spk, txt in turns if spk.lower() == "agent"]
    
    if not agent_lines:
        return {
            "category": "Soft Skills",
            "name": "Branding and Survey Check",
            "rating": "FAIL",
            "score": 0,
            "reason": "No agent lines found in the transcript."
        }
        
    first_4 = " ".join(agent_lines[:4]).lower()
    last_4 = " ".join(agent_lines[-4:]).lower()
    
    greeting_match = False
    closing_match = False
    
    if "thank you for calling s-net" in first_4:
        greeting_match = True
        
    if "thank you for choosing s-net" in last_4:
        closing_match = True

    if greeting_match and closing_match:
        return {
            "category": "Soft Skills",
            "name": "Branding and Survey Check",
            "rating": "PASS",
            "score": 100,
            "reason": "Standard compliant response"
        }
    else:
        missed = []
        if not greeting_match: missed.append("Greeting")
        if not closing_match: missed.append("Closing")
        return {
            "category": "Soft Skills",
            "name": "Branding and Survey Check",
            "rating": "FAIL",
            "score": 0,
            "reason": f"Agent missed verbatim scripts for: {', '.join(missed)}"
        }

def evaluate_hold_and_dead_air(turns: List[Tuple[str, str]], parsed_times: List[Optional[int]]) -> Dict[str, Any]:
    if not parsed_times or len(parsed_times) != len(turns) or all(t is None for t in parsed_times):
        return {
            "category": "Soft Skills",
            "name": "Hold time and Dead Air",
            "rating": "PASS",
            "score": 100,
            "reason": "Standard compliant response (No timestamps to check)"
        }
        
    max_gap = 0
    for i in range(1, len(parsed_times)):
        t1 = parsed_times[i-1]
        t2 = parsed_times[i]
        if t1 is not None and t2 is not None:
            gap = t2 - t1
            if gap > max_gap:
                max_gap = gap
                
    if max_gap > 180:
        return {
            "category": "Soft Skills",
            "name": "Hold time and Dead Air",
            "rating": "FAIL",
            "score": 0,
            "reason": f"SLA Breach: Maximum delay between turns was {max_gap} seconds, exceeding 3 minutes."
        }
    elif max_gap > 20:
        return {
            "category": "Soft Skills",
            "name": "Hold time and Dead Air",
            "rating": "FAIL",
            "score": 0,
            "reason": f"Dead Air Breach: Maximum delay between turns was {max_gap} seconds, exceeding 20 seconds."
        }
        
    return {
        "category": "Soft Skills",
        "name": "Hold time and Dead Air",
        "rating": "PASS",
        "score": 100,
        "reason": "Standard compliant response"
    }
