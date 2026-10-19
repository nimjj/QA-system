## Done on Colab

Paste back to Claude: the cell 9b `TIMING = {...}` line, and any cell whose output differs from its "EXPECT" comment.

Then, **on your PC** (not in Colab): download the `final` folder into `laya-training/checkpoints/<run id>/final` and `smoke_preds_ft.json` into `laya-training/checkpoints/<run id>/files/`, then run `tools/check_local_load.py` (see the README).
