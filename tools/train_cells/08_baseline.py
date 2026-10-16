# CELL 8: baseline. The untouched base model answers every dev and test question (about 1 minute).
# EXPECT: a table of the BASE model's test scores per check: balanced accuracy at the production cutoff and AUC.
# AUC 0.50 = no signal; the base model is expected to be weak on rapport. Saved to /content/work/preds_base.json.
t0 = time.time()
base_agent = laya.load(BASE)
PRED = {"base": {"dev": predict_rows(base_agent, DEV), "test": predict_rows(base_agent, TEST)}}
del base_agent
torch.cuda.empty_cache()
json.dump(PRED["base"], open(f"{WORK}/preds_base.json", "w"))
RES = {"base": evaluate(DEV, PRED["base"]["dev"], TEST, PRED["base"]["test"])}
print(f"base scored in {time.time() - t0:.0f}s")
print(f"{'check':<18}{'n':>5}{'BA@prod cut':>13}{'AUC':>7}")
for c in TRAINED + REGRESSION:
    r = RES["base"]["checks"][c]
    print(f"{c:<18}{r['n_test']:>5}{r['ba_test_frozen_cut']:>13.3f}{r['auc_test']:>7.3f}")
print("ECE (test):", round(RES["base"]["ece_test"], 3))
