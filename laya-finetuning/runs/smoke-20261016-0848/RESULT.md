# Plan A smoke test: PASSED (2026-10-16)

Plumbing only. None of these numbers say anything about grading quality.

| Check | Result |
|---|---|
| Colab GPU | NVIDIA L4, `device cuda:0` |
| Base checkpoint | `convaiinnovations/laya` @ `7b928d82…`, sha256 identical to the local copy |
| Dry run | 20 rows read, 21 valid items, nothing skipped |
| Training | 1 epoch, exit code 0, through `tools/laya_train_cuda.py` (laya 0.4.0 crashes on GPUs without it) |
| Drive watcher | 2 copies (epoch 1, final), each verified 7 files / 846 MB, then renamed |
| Output config | `fine_tuned: true`, `max_len 512`, `head_max_len 192`, base `temperature_by_options` dropped |
| Reload | `laya.load` and `Router(models={"english": ...})` agree exactly; Drive copies agree with `/content` copy |
| Local CPU through `laya_adapter` (`LAYA_CHECKPOINT`) | 21 predictions in 35.6 s, largest difference from Colab 0.0057 (tolerance 0.03) |
| Original base weights | unchanged (sha256 verified) |

## Measured training speed (cell 9b, L4)
13.7 items/s at 367 mean state tokens: **~15 min of training for 3,400 items x 4 epochs, plus ~2 min load/save.**

## Found along the way
- laya 0.4.0 `finetune()` runs its "before" evaluation while the model is still on the CPU, so it crashes on CUDA. Worked around by `tools/laya_train_cuda.py`.
- Use one question id per check in real data (the smoke rows reused `q`, which only triggers a harmless warning).

## Files
`00_smoke_test.executed.ipynb` is the notebook as run (cells 1-8 outputs were not saved). `manifest.json`, the prediction files, `smoke.jsonl` and the logs are the run's small artefacts. The 846 MB checkpoint lives on Drive (`MyDrive/laya-finetuning/checkpoints/smoke-20261016-0848/`) and is not in git.
