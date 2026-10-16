# CELL 10: what laya-train wrote.
# EXPECT: files incl. model.safetensors (about 842 MB, fp16), encoder/, tokenizer/, questions.json, train_report.json, checkpoint_latest/;
# "fine_tuned: True", "max_len: 512", "head_max_len: 192", "base temperature_by_options values still present: []"
# (the base model's old calibration buckets must NOT survive). With only 2 calibration items the new config
# normally has no temperature_by_options at all.
for dp, _, fns in sorted(os.walk(OUT)):
    if "checkpoint_latest" in dp:
        continue
    for fn in sorted(fns):
        p = os.path.join(dp, fn)
        print(f"{os.path.getsize(p) / 1e6:9.2f} MB  {os.path.relpath(p, OUT)}")
print("checkpoint_latest/ exists:", os.path.isdir(f"{OUT}/checkpoint_latest"))

cfg = json.load(open(f"{OUT}/rl_agent_config.json"))
print("fine_tuned:", cfg.get("fine_tuned"))
print("max_len:", cfg.get("max_len"), "| head_max_len:", cfg.get("head_max_len"))
print("temperature:", cfg.get("temperature"))
old = BASE_CFG.get("temperature_by_options", {})
new = cfg.get("temperature_by_options", {})
print("temperature_by_options in new config:", new)
print("base temperature_by_options values still present:", [k for k, v in new.items() if old.get(k) == v])
print("training keys:", sorted(cfg.get("training", {})))
print("calibration report:", json.dumps(cfg["training"].get("laya_train_calibration"), indent=1)[:700])
