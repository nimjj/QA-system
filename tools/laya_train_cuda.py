"""laya-train with one fix for GPUs. Same arguments as `laya-train` / `python -m laya.train_cli`.

Why it exists: in laya 0.4.0, finetune() evaluates the calibration slice (or the --eval file) BEFORE training,
but load_checkpoint() returns the model on the CPU and only train_model() moves it to the GPU. On CUDA that
evaluation crashes with "Expected all tensors to be on the same device ... index_select". Laya's own tests run
on CPU, so they never hit it. This wrapper moves the model to the target device before every
calibration_records() call. Nothing in the installed laya package is edited.

Use it exactly like laya-train:
    python laya_train_cuda.py --data train.jsonl --base <dir> --out <dir> --loss soft-ce --epochs 4 ...
Drop this wrapper if a later laya release fixes it upstream (run once without it to find out).
"""
import sys

import laya.train as _train

_original = _train.calibration_records


def _calibration_records_on_device(model, tok, items, device, *args, **kwargs):
    model.to(device)      # a no-op when it is already there (after training)
    return _original(model, tok, items, device, *args, **kwargs)


# finetune() looks calibration_records up in laya.train's globals at call time, so this takes effect
_train.calibration_records = _calibration_records_on_device

from laya.train_cli import main  # noqa: E402  (imported after the patch on purpose)

if __name__ == "__main__":
    sys.exit(main())
