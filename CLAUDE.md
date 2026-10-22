# Instructions for AI assistants (Claude Code)

This repo is the **QA application**: the S-Net call-grading service (Python rules plus the Laya model), its dashboard, its tests, and the production weights in `models/final-softce-3`. Everything about *training, fine-tuning, testing and evaluating* the Laya model lives in a **separate repo and folder next to this one**: `../laya-finetuning` (GitHub `nimjj/laya-finetuning`). The two are independent since 2026-10-22: this app does not need that folder to run; that folder needs this app's code (it imports `src/...` and hashes the frozen files) and finds it at `../QA-system`.
**Read `Docs/AI_HANDOVER.md` first**: current status, how to run the fine-tuned model, rules, test sets, next steps.

Hard rules (details in the handover, section 4):
- Every result is measured against AI-written keys, not human-labelled. Say so. Never call a development-set number a test result.
- Never edit or print `.env`. Never touch the `bitbucket` remote. Commit and push only when asked. Weights never go to GitHub.
- Production has customer-side sentiment only; never use agent sentiment.
- Do not change `laya_inputs.py`, `rule_engine.py`, `laya_windows.py` or the question wording without re-freezing (`python ../laya-finetuning/tools/export_checks.py --check`).
- Do not train on `../laya-finetuning/inputs/AG50`. Do not restart background jobs that the system stopped.
- Keep the repo out of Google Drive synced folders; commit right after editing.
- Owner: Nimithra (they/them), a beginner at ML. Keep replies short and simple; ask only at real decision points.

App v3 (new pipeline in `src/v3/`, `LAYA_FLOW=v3`, built beside the frozen v2 files and never editing them): see `Docs/V3.md`. Tests: `python -m unittest discover -s tests/unit -t .` (no model needed). Real-model checks live in the Laya repo: `../laya-finetuning/eval/v3_compare.py` (v3 vs v2) and `../laya-finetuning/eval/v3_service_test.py` (server, load, memory); run them with this app's Python (`.venv`).

Run the fine-tuned model: put the weights in `models/final-softce-3`, add `LAYA_CHECKPOINT=models/final-softce-3` to `.env`, then `python main.py`.
New machine: `../laya-finetuning/docs/NEW_PC_SETUP.md`. Map of both folders: `Docs/CODEBASE_GUIDE.md` section 5.
