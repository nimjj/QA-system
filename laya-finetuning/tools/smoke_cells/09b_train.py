# CELL 9: the 1-epoch training run (the pipeline is tested here, not the quality).
# laya-train writes to /content (local disk). A watcher copies checkpoint_latest/ to Drive only once it is fully written.
# EXPECT (about 3-8 min including model load):
#   "train items 19, calibration items 2, eval items 2 (calibration_slice) ... device cuda"
#   "epoch 1/1 mean loss ..."
#   a RuntimeWarning "... calibration: not fitted: 2 calibration items, fewer than 10 ..." (normal here: only 2 items)
#   "Training complete! Model saved to /content/work/smoke-ckpt"
#   watcher lines: "epoch1: quiet for 30s -> copied to tmp -> verified N files / X MB -> renamed ..." then "final: ..."
#   last line: "exit code 0 | ... | watcher errors: []"
OUT = f"{WORK}/smoke-ckpt"
shutil.rmtree(OUT, ignore_errors=True)
DRIVE_RUN = f"{DRIVE}/checkpoints/{RUN_ID}"
os.makedirs(DRIVE_RUN, exist_ok=True)

TRAIN_CMD = [sys.executable, "-u", LAUNCHER, "--data", SMOKE, "--base", BASE, "--out", OUT,
             "--loss", "soft-ce", "--epochs", "1", "--micro-batch", "4", "--grad-accum", "1", "--seed", "0",
             "--max-len", "512", "--head-max-len", "192"]
watcher = CkptWatcher(f"{OUT}/checkpoint_latest", f"{DRIVE_RUN}/checkpoint_latest", quiet_s=30)
t0 = time.time()
rc, events = run_logged(TRAIN_CMD, f"{WORK}/smoke_train.log",
                        on_item=lambda it: ((watcher.feed(it) if it else None), watcher.flush()))
(watcher.finish if rc == 0 else watcher.stop)()
watcher.thread.join(timeout=300)
watcher.flush()
print(f"exit code {rc} | wall {time.time() - t0:.0f}s | watcher copies: {len(watcher.copies)} | watcher errors: {watcher.errors}")
assert rc == 0, "laya-train itself failed: the error is in the output above, paste it"
assert not watcher.errors and watcher.copies, "training worked but the copy to Drive failed: paste the watcher lines"
