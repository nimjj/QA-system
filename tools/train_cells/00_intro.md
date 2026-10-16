# Laya fine-tune: train, compare, report (one notebook, press **Run all**)

What it does, in order: checks the GPU, mounts Drive, installs the pinned libraries, downloads the untouched English checkpoint, scores the **base model** on the dev and test rows, trains two variants (soft-ce and rlcd), scores both, picks the better one on **dev**, saves everything to Drive, and prints a short summary to paste back.

Expect roughly 30 to 40 minutes on an L4. The data is embedded in this notebook (nothing to upload).

**Read this before trusting any number:** every train, dev and test row was written *and labelled by Claude*. No row is human-labelled and the test set is not independent. The test rows use industries, personas and wording that the training rows never contain, so the test gap is a fair sign of generalisation, but the scores say "good on Claude-written synthetic calls", not "good on real calls".

If a cell fails, the error is printed under it. Paste that to Claude. After a kernel restart: run cell 1, then continue from the cell that failed.

Nothing here modifies the original checkpoint: training reads a downloaded copy and writes new folders.
