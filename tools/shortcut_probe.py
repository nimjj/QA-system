"""Shortcut probe: can cheap surface features predict the label?

If a bag-of-words classifier (or just the text length) predicts a check's label well on rows it has not seen,
the data may be giving the answer away through style, and a fine-tuned model could learn the shortcut instead of the
skill. Cross-validation is grouped by pair_id, so a matched pair is never split between train and test folds.

Per check it reports balanced accuracy for: bag-of-words (TF-IDF 1-2 grams, logistic regression), text length alone,
and the strongest words. Thresholds (see README): above 0.85 is a warning for every check and a hard fail for Rapport
and Paraphrasing. Some real signal is expected (a restatement does contain restating words), so a high score is a
prompt to look at the top words and add hard cases that break them, not proof of a defect by itself.

Usage (qa-analysis venv):
    python tools/shortcut_probe.py data/rows/pilot.jsonl
"""
import collections
import json
import sys

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import GroupKFold

WARN, HARD_FAIL_CHECKS = 0.85, {"rapport", "paraphrasing"}


def probe(rows, folds=5):
    by = collections.defaultdict(list)
    for r in rows:
        by[r["meta"]["check"]].append(r)
    results = {}
    for check, rs in sorted(by.items()):
        y = np.array([r["meta"]["label"] == "PASS" for r in rs], dtype=int)
        groups = np.array([r["meta"]["pair_id"] for r in rs])
        texts = [r["state"] for r in rs]
        n_groups = len(set(groups))
        k = min(folds, n_groups)
        if k < 2 or y.min() == y.max():
            results[check] = None
            continue
        pred_bow, pred_len, idx_all = np.zeros(len(rs), int), np.zeros(len(rs), int), np.arange(len(rs))
        for tr, te in GroupKFold(n_splits=k).split(idx_all, y, groups):
            vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, lowercase=True)
            xtr = vec.fit_transform([texts[i] for i in tr])
            if xtr.shape[1] == 0 or len(set(y[tr])) < 2:
                pred_bow[te] = int(round(y[tr].mean()))
            else:
                clf = LogisticRegression(max_iter=1000, C=3.0).fit(xtr, y[tr])
                pred_bow[te] = clf.predict(vec.transform([texts[i] for i in te]))
            lens = np.array([len(texts[i].split()) for i in range(len(rs))]).reshape(-1, 1)
            if len(set(y[tr])) == 2:
                pred_len[te] = LogisticRegression().fit(lens[tr], y[tr]).predict(lens[te])
        vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, lowercase=True)
        x = vec.fit_transform(texts)
        top = []
        if x.shape[1]:
            clf = LogisticRegression(max_iter=1000, C=3.0).fit(x, y)
            names = np.array(vec.get_feature_names_out())
            order = np.argsort(clf.coef_[0])
            top = [("FAIL", n) for n in names[order[:4]]] + [("PASS", n) for n in names[order[-4:]][::-1]]
        results[check] = {"n": len(rs), "pairs": n_groups,
                          "bow": balanced_accuracy_score(y, pred_bow), "length": balanced_accuracy_score(y, pred_len), "top": top}
    return results


def main():
    rows = [json.loads(line) for line in open(sys.argv[1], encoding="utf-8") if line.strip()]
    res = probe(rows)
    print(f"{'check':18s} {'rows':>5s} {'pairs':>5s} {'bag-of-words':>13s} {'length only':>12s}  verdict")
    worst = 0
    for check, r in res.items():
        if r is None:
            print(f"{check:18s}  (too few groups or one label)"); continue
        verdict = ("HARD FAIL" if check in HARD_FAIL_CHECKS else "warning") if r["bow"] > WARN or r["length"] > WARN else "ok"
        worst += verdict == "HARD FAIL"
        print(f"{check:18s} {r['n']:5d} {r['pairs']:5d} {r['bow']:13.2f} {r['length']:12.2f}  {verdict}")
    print("\nstrongest words per check (label the word points to):")
    for check, r in res.items():
        if r and r["top"]:
            print(f"  {check:18s} " + ", ".join(f"{w} ({lab})" for lab, w in r["top"]))
    print("\nnote: small samples are noisy; this is a smoke check at pilot size, the real gate runs at full size.")
    sys.exit(1 if worst else 0)


if __name__ == "__main__":
    main()
