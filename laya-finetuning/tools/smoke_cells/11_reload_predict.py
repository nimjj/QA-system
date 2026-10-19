# CELL 11: reload the fine-tuned folder two ways and predict the 21 questions.
#   (a) laya.load(OUT)   (b) Router(models={"english": OUT}), which is how qa-analysis's laya_adapter will serve it.
# EXPECT: "max difference between the two load paths: 0.0000" (or ~1e-6), a table of base vs fine-tuned P(yes),
# and "moved toward their label: N/21". After only 5 training steps most rows should move toward the label,
# but small moves and a few wrong-way rows are normal. What must hold: no NaN and the two load paths agree.
import math

from laya import Router

ft_agent = laya.load(OUT)
P_FT = predict_all(lambda s, q: ft_agent.predict(s, q), ROWS)
del ft_agent
torch.cuda.empty_cache()

router = Router(models={"english": OUT}, default="english", max_loaded=1)
P_RT = predict_all(lambda s, q: router.predict(s, q, model="english"), ROWS)
del router
torch.cuda.empty_cache()

assert not any(math.isnan(v) for v in P_FT.values()), "NaN in fine-tuned predictions"
print(f"max difference between the two load paths: {max(abs(P_FT[k] - P_RT[k]) for k in P_FT):.6f}")
json.dump(P_FT, open(f"{WORK}/smoke_preds_ft.json", "w"), indent=1)

targets = {}
for r in ROWS:
    for qid in r["questions"]:
        key = f"{r['meta']['id']}/{qid}"
        targets[key] = float(r["expected"][qid]) if "expected" in r else r["gold"][qid]["probabilities"]["true"]
moved = 0
print(f"{'row/question':<28} {'target':>6} {'base':>7} {'tuned':>7}")
for k in P_FT:
    toward = abs(P_FT[k] - targets[k]) < abs(P_BASE[k] - targets[k])
    moved += toward
    print(f"{k:<28} {targets[k]:6.2f} {P_BASE[k]:7.3f} {P_FT[k]:7.3f} {'+' if toward else '-'}")
print(f"moved toward their label: {moved}/{len(P_FT)}")
