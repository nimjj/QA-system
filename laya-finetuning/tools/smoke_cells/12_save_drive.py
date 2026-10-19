# CELL 12: save everything to Drive (temp folder -> verify -> rename), then LOAD the Drive copies to prove they work.
# EXPECT:
#   "final copy: N files / X MB verified", "weights sha256 on Drive matches /content: True"
#   "Drive final loads; max diff vs cell 11: 0.0000..." (must be below 1e-4)
#   "Drive checkpoint_latest loads; max diff vs final: ..." (informational, should be tiny)
#   a manifest summary and the folder to download for the local CPU check.
DRIVE_FINAL = f"{DRIVE_RUN}/final"
wait_stable(OUT, quiet_s=5, ignore=("checkpoint_latest",))
files, size = copy_verified(OUT, DRIVE_FINAL, "final", ignore=("checkpoint_latest",))
print(f"final copy: {files} files / {size / 1e6:.0f} MB verified")
ok_hash = sha256_file(f"{OUT}/model.safetensors") == sha256_file(f"{DRIVE_FINAL}/model.safetensors")
print("weights sha256 on Drive matches /content:", ok_hash)
assert ok_hash

os.makedirs(f"{DRIVE_RUN}/files", exist_ok=True)
for name in ("smoke.jsonl", "smoke_preds_base.json", "smoke_preds_ft.json", "smoke_train.log", "timing_train.log"):
    if os.path.exists(f"{WORK}/{name}"):
        shutil.copy(f"{WORK}/{name}", f"{DRIVE_RUN}/files/{name}")

from importlib.metadata import version

manifest = {
    "run_id": RUN_ID,
    "created": datetime.datetime.now().isoformat(timespec="seconds"),
    "purpose": "Plan A smoke test (plumbing only, not a quality result)",
    "gpu": subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], capture_output=True, text=True).stdout.strip(),
    "versions": {"python": sys.version.split()[0], "torch": version("torch"), "transformers": version("transformers"),
                 "laya": version("laya"), "laya_commit": LAYA_COMMIT},
    "base": {"repo": BASE_REPO, "revision": BASE_REV, "sha256": BASE_SHA256},
    "frozen_checks_sha256": FROZEN["sha256"],
    "qa_analysis_commit": FROZEN["qa_analysis_commit"],
    "smoke_jsonl_sha256": SMOKE_SHA256,
    "train_command": " ".join(TRAIN_CMD),
    "final_weights_sha256": sha256_file(f"{DRIVE_FINAL}/model.safetensors"),
    "watcher_copies": watcher.copies,
    "timing": globals().get("TIMING"),
}
json.dump(manifest, open(f"{DRIVE_RUN}/manifest.json", "w"), indent=2)
os.makedirs(f"{DRIVE}/runs/{RUN_ID}", exist_ok=True)
shutil.copy(f"{DRIVE_RUN}/manifest.json", f"{DRIVE}/runs/{RUN_ID}/manifest.json")

# load both Drive copies and compare with cell 11
drive_final = laya.load(DRIVE_FINAL)
P_DF = predict_all(lambda s, q: drive_final.predict(s, q), ROWS)
del drive_final
torch.cuda.empty_cache()
d1 = max(abs(P_DF[k] - P_FT[k]) for k in P_FT)
print(f"Drive final loads; max diff vs cell 11: {d1:.6f}")
assert d1 < 1e-4, "Drive copy predicts differently from /content: stop and tell Claude"

drive_latest = laya.load(f"{DRIVE_RUN}/checkpoint_latest")
P_DL = predict_all(lambda s, q: drive_latest.predict(s, q), ROWS)
del drive_latest
torch.cuda.empty_cache()
print(f"Drive checkpoint_latest loads; max diff vs final: {max(abs(P_DL[k] - P_DF[k]) for k in P_DF):.6f}")

print("\nleft in", DRIVE_RUN, ":", sorted(os.listdir(DRIVE_RUN)))
print("NEXT (on your PC): download", DRIVE_FINAL, "to laya-training/checkpoints/" + RUN_ID + "/final",
      "and", f"{DRIVE_RUN}/files/smoke_preds_ft.json", "to laya-training/checkpoints/" + RUN_ID + "/files/")
if globals().get("TIMING"):
    print("TIMING:", TIMING)
