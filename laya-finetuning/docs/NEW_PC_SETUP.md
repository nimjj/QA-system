# Moving this project to a new PC

Written 2026-10-19. Covers: what lives where, how to rebuild the working setup, how to check it works, how to carry the Claude Code conversation and notes, and what breaks if you reorganise folders.

## 1. What travels how

| Item | Where it is now | How it moves |
|---|---|---|
| App code, docs, tests, results | GitHub `nimjj/QA-system`, branch **`version-10.2-laya-finetune`** (the repo's default branch is `version-8`, so check this one out), tag `laya-inputs-frozen-v2` | `git clone` |
| Training repo (data, tools, notebook, run notes) | GitHub `nimjj/laya-finetuning`, branch **`phase-5-data`** (default is `main`) | `git clone` |
| **Fine-tuned weights** (808 MB) | `laya-training\checkpoints\final-softce-3` (git-ignored). It was assembled from several downloads, so **Drive does not hold it as one piece** | Copy the whole folder (USB, Drive zip, network share), then verify (section 4) |
| Base Laya weights (1.5 GB cache) | `laya-test\hf_home` | Re-download (section 3) or copy; verify |
| Laya library | `laya-test\laya` (clone of `NandhaKishorM/laya`, tag **v0.4.0**, commit **3cf26cb**) | `git clone` and check out the tag |
| `qa-analysis\.env` | git-ignored | Recreate (section 3) |
| Python environment | `qa-analysis\.venv` (Python 3.14.3, transformers 5.16.1, torch 2.14 CPU) | Rebuild |
| Old Ollama copy of the app | `qa-analysis-ollama` (not a repo) | Only needed to re-run Ollama; all Ollama results are already in the repo. Skip unless you need it |
| Claude Code chat and notes | `C:\Users\adept\.claude\projects\D--Projects--Tests--QA-2-laya-training\` | Section 5 |
| Colab / Drive run outputs | Your Google account, Drive folder `laya-finetuning` | Nothing to move; sign in |

## 2. Folder layout (keep it, unless you change the settings in section 6)
```
<any parent folder>\
    qa-analysis\        clone of nimjj/QA-system, branch version-10.2-laya-finetune
    laya-training\      clone of nimjj/laya-finetuning, branch phase-5-data
    laya-test\
        laya\           clone of NandhaKishorM/laya at v0.4.0
        hf_home\        Hugging Face cache for the base weights
    qa-analysis-ollama\ (optional)
```
Two things assume `qa-analysis`, `laya-training` and `laya-test` are siblings: `qa-analysis\requirements.txt` has `-e ../laya-test/laya`, and the `laya-training\tools\*.py` scripts look for `../qa-analysis`.

## 3. Step by step (PowerShell)

Needs: Git, Python 3.14 (the version used here; another 3.x may work but is untested), about 6 GB free disk.

```powershell
# 3.1 clone
mkdir "D:\Projects\QA 2"; cd "D:\Projects\QA 2"
git clone https://github.com/nimjj/QA-system.git qa-analysis
git -C qa-analysis checkout version-10.2-laya-finetune
git clone https://github.com/nimjj/laya-finetuning.git laya-training
git -C laya-training checkout phase-5-data
mkdir laya-test; git clone https://github.com/NandhaKishorM/laya.git laya-test\laya
git -C laya-test\laya checkout v0.4.0          # expect commit 3cf26cb

# 3.2 environment (CPU is enough for serving and testing)
cd qa-analysis
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\pip install -r requirements.txt     # also installs ../laya-test/laya in editable mode
.\.venv\Scripts\pip install "transformers==5.16.1"  # the version everything was tested with
.\.venv\Scripts\python -c "import laya, transformers, torch; print(laya.__file__, transformers.__version__, torch.__version__)"
```
If `torch` came in as a GPU build, it still works on CPU.

**3.3 Base weights.** Either copy `laya-test\hf_home` from the old PC, or download the pinned revision (about 1.5 GB):
```powershell
$env:HF_HOME = "D:\Projects\QA 2\laya-test\hf_home"
.\.venv\Scripts\python -c "from huggingface_hub import snapshot_download; snapshot_download('convaiinnovations/laya', revision='7b928d828b7b0e022f929d9bd2e44165aa270148')"
```

**3.4 Fine-tuned weights.** Copy the whole folder to `laya-training\checkpoints\final-softce-3` (it contains `model.safetensors`, `questions.json`, `rl_agent_config.json`, `encoder\`, `tokenizer\`). Do not copy only `model.safetensors`.

**3.5 `.env`** in `qa-analysis`. These are the keys the old file has; the values below are examples, so copy the real values from the old file and only change the path:
```
LAYA_MODEL=english
LAYA_HF_HOME=D:\Projects\QA 2\laya-test\hf_home
LAYA_DEVICE=cpu
SERVER_HOST=0.0.0.0
SERVER_PORT=8006
```
Check the old `.env` for any other keys before copying this (database settings, for example). Never commit `.env`.

## 4. Check that the move worked

1. **Weights are bit-identical** (run from `laya-training`):
   ```powershell
   ..\qa-analysis\.venv\Scripts\python tools\checkpoint_manifest.py verify checkpoints\final-softce-3 --manifest runs\ft3-stage3\final-softce-3.manifest.json
   ..\qa-analysis\.venv\Scripts\python tools\checkpoint_manifest.py verify "..\laya-test\hf_home\hub\models--convaiinnovations--laya\snapshots\7b928d828b7b0e022f929d9bd2e44165aa270148" --manifest data\frozen\base_laya_7b928d82.manifest.json
   ```
   Both must print `ALL FILES MATCH`. Fine-tuned `model.safetensors` starts `fc6a3f1b793a`; base `model.safetensors` starts `891102d37268`.
2. **Extractors unchanged:** `..\qa-analysis\.venv\Scripts\python tools\export_checks.py --check` prints two `MATCH` lines (inputs hash `c1fd93541124`).
3. **End-to-end on the 4 golden calls** (2 minutes). In `qa-analysis`:
   ```powershell
   $env:LAYA_CHECKPOINT = "D:\Projects\QA 2\laya-training\checkpoints\final-softce-3"
   Start-Process .\.venv\Scripts\python -ArgumentList main.py -WindowStyle Hidden
   Start-Sleep 60
   .\.venv\Scripts\python Scripts\batch_test.py main --label newpc
   .\.venv\Scripts\python Scripts\compare_results.py laya-ft-v2b newpc
   ```
   Expected: **42 of 44** items, final scores about **100 / 88.3 / 50.0 / 30.0** (key 100 / 88.3 / 56.7 / 13.3). Scores can differ by a point or two on a different CPU. Stop the service afterwards. (A "database" warning at start is expected; the service runs statelessly.)
4. Optional, 15 minutes: `batch_test.py inputs\AG50 --label newpc` and `python Scripts\compare_eval.py AG50 laya-ft-v2b newpc` should agree closely.

## 5. The Claude Code conversation and notes

The chat is not in git. It lives in `C:\Users\adept\.claude\projects\D--Projects--Tests--QA-2-laya-training\` (this session `f99a48a2-...jsonl`, the earlier one `1e06a8c6-...jsonl`, and a `memory\` folder of notes that load automatically). The folder name is the working directory's path with separators turned into dashes.

- **Option A, recommended: start a fresh session.** Install Claude Code and sign in on the new PC. Copy the `memory\` folder to `C:\Users\<you>\.claude\projects\<new-path-slug>\memory\` (the slug is the path of the folder you open Claude in, for example `D:\Projects\QA 2\laya-training` becomes `D--Projects-QA-2-laya-training`; run Claude once in that folder, then look in `.claude\projects` to see the exact name). Then paste the first message below.
- **Option B: resume this exact session.** Copy the two `.jsonl` files and `memory\` into that same slug folder, open Claude in the folder, and use `/resume`. If the slug does not match the new path, the session will not be listed. The session is very long, so a fresh start is cleaner.
- The plan files in `C:\Users\adept\.claude\plans\` are not needed; their content is in `qa-analysis\Docs\FLOW_V2.md`.

**First message for the new session:**
> This project fine-tunes Laya to replace Ollama in the S-Net QA call-grading service. Read these first: `laya-training/README.md`, `laya-training/runs/ag50/RESULT.md`, `qa-analysis/Docs/FLOW_V2.md`, `qa-analysis/Docs/AG50_REPORT.md`, `qa-analysis/Docs/LAYA_TEST_LOG.md` and `laya-training/docs/NEW_PC_SETUP.md`. Then check the setup using section 4 of the setup doc, and continue with the next steps in `FLOW_V2.md`. Rules: describe all results as measured against AI-written keys (not human-labelled); never modify the original checkpoint; never touch `.env` or the `bitbucket` remote; commit or push only when I ask; production sentiment is customer-side only; keep replies short.

## 6. If you reorganise folders: what depends on paths

| Setting | Where | If the layout changes |
|---|---|---|
| `-e ../laya-test/laya` | `qa-analysis/requirements.txt` | Edit the relative path, or `pip install -e <path to laya>` |
| Base-weights cache default `../laya-test/hf_home` | `qa-analysis/src/services/laya_adapter.py` | Set `LAYA_HF_HOME` in `.env` (it wins over the default) |
| Fine-tuned weights | env `LAYA_CHECKPOINT` (absolute path) | Set it each time or in the shell profile. Never in a committed file |
| `../qa-analysis` | `laya-training/tools/export_checks.py`, `build_rows.py`, `build_calls.py`, `build_replay.py`, `build_eval50.py` | Pass `--qa-root` where offered, or keep the two repos side by side |
| `LAYA_FLOW` | env | Unset means flow v2 with a fine-tuned checkpoint, v1 for stock; override with `v1` or `v2` |
| Scripts in `qa-analysis/Scripts` | use their own location (`ROOT`) | No change needed |

Renaming `Projects (Tests)` or `QA 2` is fine. Spaces and brackets in paths work, but quote them in PowerShell.

## 7. Facts to keep
- Base checkpoint: `convaiinnovations/laya`, revision `7b928d828b7b0e022f929d9bd2e44165aa270148`; laya v0.4.0, commit `3cf26cbcb18725dbc2d127bb8bb2c4c43243ae63`; transformers 5.16.1.
- Train only through `tools/laya_train_cuda.py` (`laya-train` crashes on GPU), on Colab (L4), with the notebook `01_train_eval.ipynb`.
- Frozen inputs: tag `laya-inputs-frozen-v2`, `inputs_sha256` `c1fd935411242e06...` (it covers `laya_inputs.py`, `rule_engine.py` and `laya_windows.py`). If it stops matching, training data built earlier must be regenerated.
- Latest results: `qa-analysis/Docs/FLOW_V2.md`. Next steps: sealed test set and new training data from Antigravity, retrain, human review, shadow mode.
- Never push to the `bitbucket` remote of `qa-analysis`; the weights never go to GitHub.
