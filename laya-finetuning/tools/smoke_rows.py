"""The 20 smoke-test rows, shared by the Colab notebook and tools/check_local_load.py.

Each row is built from the FROZEN production question (data/frozen/checks_frozen.json), so the smoke test
trains and predicts with the real LAYA_CHECKS wording. The states are hand-written in the shape the
rule_engine extractors produce; they are plumbing fixtures, not training data, and are never reused later.

A row's `verdict` is the QA outcome (PASS or FAIL). `expected` is the answer to the yes/no question:
true when the question's "yes" means that verdict, so Rapport FAIL -> true but Resolved FAIL -> false.
"""
import json

CUST_DROP = ("Customer: This is the third time this week my connection died during a client call, "
             "I'm honestly about to cancel.\n")
PARA_CUST = ("CUSTOMER: My internet keeps dropping every evening around eight and the router light turns orange. "
             "I have a client presentation tomorrow.\nAGENT: ")
PROBE_HEAD = "CUSTOMER PROBLEM: My internet keeps dropping every evening around eight.\n\nThe agent asked these questions during the call:\n"

# (id, check, verdict, state)
SMOKE = [
    ("rapport_fail", "rapport", "FAIL",
     "Agent: You should have restarted the router before you called, that's the first thing anyone should do.\n"
     "Agent: That's basic stuff."),
    ("rapport_pass", "rapport", "PASS",
     "Agent: Obviously I want to get this sorted for you today, so let me check the line.\n"
     "Agent: As I said earlier, I'll stay on the line with you until it's back up."),
    ("para_pass", "paraphrasing", "PASS",
     PARA_CUST + "Let me make sure I have this right: the connection drops each evening around eight, the router "
     "goes orange, and you need it stable before tomorrow's presentation. Is that correct?"),
    ("para_fail", "paraphrasing", "FAIL",
     PARA_CUST + "Which light is blinking orange? What time did the evening drop start? Is the router in the living room?"),
    ("al_fail", "active_listening", "FAIL",
     "Turn 6: What colour is the light on the front of the modem?\n"
     "... Turn 14: Can you tell me the colour of the light on the modem?\nCustomer: I just said, it's red."),
    ("al_pass", "active_listening", "PASS",
     "Turn 6: What colour is the light on the front of the modem?\n"
     "... Turn 22: What is the light doing now after the restart?"),
    ("resolved_pass", "resolved", "PASS",
     "Agent: Let's test it together. Can you open a page for me?\n"
     "Customer: It loaded right away, and the video call is stable too.\n"
     "Agent: Wonderful. So to confirm, the internet issue is fully resolved on your end?\n"
     "Customer: Yes, completely resolved, thank you.\n"
     "Agent: Is there anything else I can help with?\nCustomer: No, that's all."),
    ("resolved_fail", "resolved", "FAIL",
     "Agent: I've reset the line from here, it should be fine now.\n"
     "Customer: Okay, I'll see how it goes.\n"
     "Agent: Thank you for calling S-Net. Have a good day.\nCustomer: Bye."),
    ("empathy_pass", "empathy", "PASS",
     CUST_DROP + "Agent: Three drops in a week during client calls is really stressful, and I'm sorry you've been "
     "through that. Let's get to the bottom of it right now.\nCustomer: Thank you.\n"),
    ("empathy_fail", "empathy", "FAIL",
     CUST_DROP + "Agent: They can help with that. What's your account number?\nCustomer: It's 55 21 08.\n"),
    ("ownership_fail", "ownership", "FAIL",
     "Agent: That's not my department, you'd have to call the billing team back tomorrow."),
    ("ownership_pass", "ownership", "PASS",
     "Agent: That sits with another team's system, but I'll open the ticket with them myself so you don't have to "
     "call back."),
    ("probing_pass", "probing", "PASS",
     PROBE_HEAD + "- Which lights on the router change colour when it drops?\n"
     "- Does it happen on every device or only your laptop?\n- Have you tried restarting the router?"),
    ("probing_fail", "probing", "FAIL",
     PROBE_HEAD + "- Is there anything else I can help you with today?\n- Would you like a short survey after the call?"),
    ("hostility_fail", "hostility", "FAIL",
     "Customer: My router has been dead since this morning.\n"
     "Agent: Maybe if you read the instructions you wouldn't be this clueless. I don't have time for this.\n"
     "Customer: Excuse me?\nAgent: Whatever. Call someone else."),
    ("hostility_pass", "hostility", "PASS",
     "Customer: You people are useless, my router has been dead since this morning!\n"
     "Agent: I hear how upsetting this is, and I'm going to fix it with you. Let me look at the line.\n"
     "Customer: Fine."),
    ("escalation_fail", "escalation", "FAIL",
     "Customer: I want to speak to a supervisor right now.\n"
     "Agent: There's no need for that, I can handle it. Supervisors can't do more than I can.\n"
     "Customer: I asked for a supervisor.\nAgent: Let's just continue with the troubleshooting."),
    ("escalation_pass", "escalation", "PASS",
     "Customer: Can I speak to a supervisor?\n"
     "Agent: Of course. I'll transfer you now and pass on the full details so you don't repeat yourself.\n"
     "Customer: Thanks."),
]


def _generic(instructions, true_text, false_text):
    """A generic custom-criterion question, shaped like dynamic_evaluator._batch_check builds them."""
    return {"type": "noul", "instructions": instructions, "criteria": {"true": true_text, "false": false_text}}


# Replay rows keep the model's behaviour on tenant-defined criteria; `gold` is a soft target (P(false), P(true)).
REPLAY = [
    {"id": "replay_callback", "state": "Agent: If we get cut off, I'll call you back on the number ending 4417 within "
                                       "ten minutes.\nCustomer: Great.",
     "questions": {"item_0": _generic("Did the agent do this: Offered a callback number?",
                                      "the agent clearly did it: offered a callback number",
                                      "the agent did not do it")},
     "gold": {"item_0": {"probabilities": {"false": 0.2, "true": 0.8}}}},
    {"id": "replay_batch", "state": "Agent: I can't compare us with other providers, but here is what our plan includes. "
                                    "Before you go, would you be willing to rate this call?\nCustomer: Sure.",
     "questions": {
         "item_0": _generic("Does the agent violate this rule: Never discuss competitors?",
                            "an agent line clearly violates it: never discuss competitors",
                            "no agent line violates it"),
         "item_1": _generic("Did the agent do this: Offer a survey?",
                            "the agent clearly did it: offer a survey",
                            "the agent did not do it")},
     "gold": {"item_0": {"probabilities": {"false": 0.85, "true": 0.15}},
              "item_1": {"probabilities": {"false": 0.1, "true": 0.9}}}},
]


def build_rows(frozen):
    """The 20 JSONL rows. `frozen` is the parsed checks_frozen.json (or its ["frozen"] part)."""
    checks = (frozen.get("frozen") or frozen)["checks"]
    rows = []
    for rid, key, verdict, state in SMOKE:
        check = checks[key]
        rows.append({
            "state": state,
            "questions": {"q": check["question"]},
            "expected": {"q": verdict == check["yes_means"]},
            "meta": {"id": rid, "check": key, "verdict": verdict},   # laya-train ignores unknown keys
        })
    for r in REPLAY:
        rows.append({"state": r["state"], "questions": r["questions"], "gold": r["gold"], "meta": {"id": r["id"]}})
    return rows


def to_jsonl(rows):
    return "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n"
