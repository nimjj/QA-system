# Instructions for AI assistants (Claude Code)

This repo is the S-Net call-grading service plus the work to replace Ollama with a fine-tuned Laya model. It has **two segments**: the QA application at the repo root (with the production weights in `models/final-softce-3`), and everything about the Laya model (training, tools, evaluation scripts in `laya-finetuning/eval/`, all test sets in `laya-finetuning/inputs/`, experiment weights) in `laya-finetuning/`. Run scripts from the repo root. Map: `Docs/CODEBASE_GUIDE.md` section 5.
**Read `Docs/AI_HANDOVER.md` first**: current status, how to run the fine-tuned model, rules, test sets, next steps.

Hard rules (details in the handover, section 4):
- Every result is measured against AI-written keys, not human-labelled. Say so. Never call a development-set number a test result.
- Never edit or print `.env`. Never touch the `bitbucket` remote. Commit and push only when asked. Weights never go to GitHub.
- Production has customer-side sentiment only; never use agent sentiment.
- Do not change `laya_inputs.py`, `rule_engine.py`, `laya_windows.py` or the question wording without re-freezing (`python laya-finetuning/tools/export_checks.py --check`).
- Do not train on `laya-finetuning/inputs/AG50`. Do not restart background jobs that the system stopped.
- Keep the repo out of Google Drive synced folders; commit right after editing.
- Owner: Nimithra (they/them), a beginner at ML. Keep replies short and simple; ask only at real decision points.

App v3 (new pipeline in `src/v3/`, `LAYA_FLOW=v3`, built beside the frozen v2 files and never editing them): see `Docs/V3.md`. Tests: `python -m unittest discover -s tests/unit -t .` (no model needed). Real-model checks: `laya-finetuning/eval/v3_compare.py` (v3 vs v2) and `laya-finetuning/eval/v3_service_test.py` (server, load, memory).

Run the fine-tuned model: put the weights in `models/final-softce-3`, add `LAYA_CHECKPOINT=models/final-softce-3` to `.env`, then `python main.py`.
New machine: `laya-finetuning/docs/NEW_PC_SETUP.md`.
