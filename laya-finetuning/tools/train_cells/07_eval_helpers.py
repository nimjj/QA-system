# CELL 7: scoring and metric helpers (balanced accuracy, AUC, bootstrap intervals by pair, ECE, replay drift).
# EXPECT: only "eval helpers ready".
import random

import laya
import numpy as np


def predict_rows(agent, rows):
    """{"<row id>/<question id>": P(yes)} for every question of every row."""
    out = {}
    for r in rows:
        res = agent.predict(r["state"], r["questions"])
        for qid in r["questions"]:
            out[f"{r['meta']['id']}/{qid}"] = float(res["answers"][qid]["noul"])
    return out


def p_pass(check, p_yes):
    return p_yes if CHECKS[check]["yes_means"] == "PASS" else 1.0 - p_yes


def supervised(rows):
    return [r for r in rows if r["meta"]["check"] != "replay"]


def by_check(rows, preds):
    """{check: [(P(pass), is_pass, pair_id), ...]}"""
    d = {}
    for r in supervised(rows):
        c = r["meta"]["check"]
        d.setdefault(c, []).append((p_pass(c, preds[f"{r['meta']['id']}/{c}"]), r["meta"]["label"] == "PASS", r["meta"]["pair_id"]))
    return d


def bal_acc(items, thr):
    pos = [p for p, y, _ in items if y]
    neg = [p for p, y, _ in items if not y]
    if not pos or not neg:
        return float("nan")
    return 0.5 * (sum(p >= thr for p in pos) / len(pos) + sum(p < thr for p in neg) / len(neg))


def auc(items):
    pos = [p for p, y, _ in items if y]
    neg = [p for p, y, _ in items if not y]
    if not pos or not neg:
        return float("nan")
    wins = sum((a > b) + 0.5 * (a == b) for a in pos for b in neg)
    return wins / (len(pos) * len(neg))


def best_cut(items):
    """Cutoff with the best balanced accuracy on these items; ties go to the one nearest 0.5."""
    ps = sorted({p for p, _, _ in items})
    cands = [0.0] + [(a + b) / 2 for a, b in zip(ps, ps[1:])] + [1.0]
    scored = [(bal_acc(items, t), -abs(t - 0.5), t) for t in cands]
    best = max(scored)
    return best[2], best[0]


def boot_ci(items, thr, n=1000, seed=0):
    """95% interval of balanced accuracy, resampling PAIRS (a pair's two rows always travel together)."""
    groups = {}
    for it in items:
        groups.setdefault(it[2], []).append(it)
    keys = list(groups)
    rng = random.Random(seed)
    vals = []
    for _ in range(n):
        sample = [it for k in (rng.choice(keys) for _ in keys) for it in groups[k]]
        v = bal_acc(sample, thr)
        if v == v:
            vals.append(v)
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]


def ece(rows, preds, bins=10):
    """Expected calibration error of P(yes) against the yes/no truth, pooled over all supervised rows."""
    pts = [(preds[f"{r['meta']['id']}/{r['meta']['check']}"], bool(r["expected"][r["meta"]["check"]])) for r in supervised(rows)]
    total, err = len(pts), 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        sel = [(p, y) for p, y in pts if lo <= p < hi or (b == bins - 1 and p == 1.0)]
        if sel:
            err += len(sel) / total * abs(sum(p for p, _ in sel) / len(sel) - sum(y for _, y in sel) / len(sel))
    return err


def replay_drift(rows, preds):
    """How far the tuned model's answers to generic custom-criteria questions moved from the base model's own."""
    diffs, agree, n = [], 0, 0
    for r in rows:
        if r["meta"]["check"] != "replay":
            continue
        for qid, g in r["gold"].items():
            base_p = g["probabilities"]["true"]
            p = preds[f"{r['meta']['id']}/{qid}"]
            diffs.append(abs(p - base_p))
            agree += (p > 0.5) == (base_p > 0.5)
            n += 1
    return {"items": n, "mean_abs_diff": float(np.mean(diffs)), "verdict_agreement": agree / n}


def evaluate(dev_rows, dev_preds, test_rows, test_preds, cuts=None):
    """Per-check metrics on test. Cutoffs for the TRAINED checks are tuned on dev (or passed in); regression checks keep the frozen cutoff."""
    dv, ts = by_check(dev_rows, dev_preds), by_check(test_rows, test_preds)
    out = {"checks": {}, "ece_test": ece(test_rows, test_preds), "replay_dev": replay_drift(dev_rows, dev_preds)}
    for c in TRAINED + REGRESSION:
        frozen_cut = CHECKS[c]["pass_threshold"]
        row = {"n_test": len(ts[c]), "frozen_cut": frozen_cut, "auc_test": auc(ts[c]), "auc_dev": auc(dv[c]),
               "ba_test_frozen_cut": bal_acc(ts[c], frozen_cut), "ba_dev_frozen_cut": bal_acc(dv[c], frozen_cut)}
        if c in TRAINED:
            cut = cuts[c] if cuts else best_cut(dv[c])[0]
            row.update({"tuned_cut": cut, "ba_dev_tuned": bal_acc(dv[c], cut), "ba_test_tuned": bal_acc(ts[c], cut)})
            row["ba_test_tuned_ci"] = boot_ci(ts[c], cut)
        else:
            row["ba_test_frozen_ci"] = boot_ci(ts[c], frozen_cut)
        out["checks"][c] = row
    out["mean_auc_dev_trained"] = float(np.mean([out["checks"][c]["auc_dev"] for c in TRAINED]))
    out["mean_ba_test_trained"] = float(np.mean([out["checks"][c]["ba_test_tuned"] for c in TRAINED]))
    return out


def evaluate_long(rows, preds, res):
    """Long-snippet test (Rapport, Paraphrasing, Resolved padded with neutral agent lines). Uses the dev-tuned cutoff of `res` when given."""
    ts, out = by_check(rows, preds), {}
    for c in ts:
        if not any(y for _, y, _ in ts[c]) or all(y for _, y, _ in ts[c]):      # needs both PASS and FAIL rows to score
            continue
        cut = res["checks"][c].get("tuned_cut", CHECKS[c]["pass_threshold"]) if res else CHECKS[c]["pass_threshold"]
        out[c] = {"n": len(ts[c]), "cut": cut, "ba": bal_acc(ts[c], cut), "ba_frozen_cut": bal_acc(ts[c], CHECKS[c]["pass_threshold"]),
                  "auc": auc(ts[c]), "ci": boot_ci(ts[c], cut)}
    return out


DEV, TEST, TEST_LONG, TEST_CALLS = SPLIT["dev_all"], SPLIT["test"], SPLIT["test_long"], SPLIT["test_calls"]
print("eval helpers ready")
