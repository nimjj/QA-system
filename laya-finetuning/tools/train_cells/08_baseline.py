# CELL 8: baseline. The untouched base model answers every dev and test question (about 1 minute).
# EXPECT: a table of the BASE model's test scores per check: balanced accuracy at the production cutoff and AUC.
# AUC 0.50 = no signal; the base model is expected to be weak on rapport. Saved to /content/work/preds_base.json.
t0 = time.time()
base_agent = laya.load(BASE)
PRED = {"base": {"dev": predict_rows(base_agent, DEV), "test": predict_rows(base_agent, TEST), "test_long": predict_rows(base_agent, TEST_LONG),
                 "test_calls": predict_rows(base_agent, TEST_CALLS)}}
del base_agent
torch.cuda.empty_cache()
json.dump(PRED["base"], open(f"{WORK}/preds_base.json", "w"))
RES = {"base": evaluate(DEV, PRED["base"]["dev"], TEST, PRED["base"]["test"])}
RES["base"]["long"] = evaluate_long(TEST_LONG, PRED["base"]["test_long"], None)
RES["base"]["nat"] = evaluate_long(TEST_CALLS, PRED["base"]["test_calls"], None)
print(f"base scored in {time.time() - t0:.0f}s")
print(f"{'check':<18}{'n':>5}{'BA@prod cut':>13}{'AUC':>7}")
for c in TRAINED + REGRESSION:
    r = RES["base"]["checks"][c]
    print(f"{c:<18}{r['n_test']:>5}{r['ba_test_frozen_cut']:>13.3f}{r['auc_test']:>7.3f}")
print("ECE (test):", round(RES["base"]["ece_test"], 3))
print("natural-call snippets (cut by the extractors from complete calls, 8 unseen-industry calls):", {c: f"BA {v['ba']:.2f} AUC {v['auc']:.2f}" for c, v in RES["base"]["nat"].items()})
print("long snippets (padded, closer to real call length):", {c: f"BA {v['ba']:.2f} AUC {v['auc']:.2f}" for c, v in RES["base"]["long"].items()})
