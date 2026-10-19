# CELL 8: baseline. The untouched base model answers all 21 questions; probabilities saved for later comparison.
# EXPECT: "device cuda" style load, then 21 numbers between 0 and 1 and "saved smoke_preds_base.json".
import laya


def predict_all(predict, rows):
    """{"<row id>/<question id>": P(yes)} using predict(state, questions) -> laya result."""
    out = {}
    for r in rows:
        res = predict(r["state"], r["questions"])
        for qid in r["questions"]:
            out[f"{r['meta']['id']}/{qid}"] = float(res["answers"][qid]["noul"])
    return out


base_agent = laya.load(BASE)
P_BASE = predict_all(lambda s, q: base_agent.predict(s, q), ROWS)
json.dump(P_BASE, open(f"{WORK}/smoke_preds_base.json", "w"), indent=1)
for k, v in P_BASE.items():
    print(f"  {k:<28} P(yes)={v:.3f}")
print("saved smoke_preds_base.json")
del base_agent
torch.cuda.empty_cache()
