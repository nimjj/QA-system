# Docs index

Start with [`AI_HANDOVER.md`](AI_HANDOVER.md) (status, rules, how to run), then the file that matches your question.

| Question | Read |
|---|---|
| I am new. What is all this, and where is everything? | [`CODEBASE_GUIDE.md`](CODEBASE_GUIDE.md) |
| Show me the flow as diagrams (Mermaid) | [`FLOW_DIAGRAMS.md`](FLOW_DIAGRAMS.md) |
| What is the app and how does a call flow through it? What does the database look like? | [`ARCHITECTURE.md`](ARCHITECTURE.md) (original version-10 specification; the schema is only here) |
| What is the new v3 pipeline, how do I run and test it? | [`V3.md`](V3.md) |
| How are calls cut into snippets for the model (flow v2)? | [`FLOW_V2.md`](FLOW_V2.md), [`FLOW_V2_LAB.md`](FLOW_V2_LAB.md), [`FLOW_V2_REGRESSION.md`](FLOW_V2_REGRESSION.md) (cited by comments in the frozen `src/services/laya_inputs.py`, so they stay) |
| What did each test round find, and which model is in production? | [`LAYA_TEST_LOG.md`](LAYA_TEST_LOG.md), `../laya-finetuning/runs/CHECKPOINTS.md` |
| The independent AG50 test: why the model errs | [`AG50_REPORT.md`](AG50_REPORT.md) |
| API calls for Postman | [`postman_collection.json`](postman_collection.json) |

All results in these documents are measured against AI-written answer keys, not human-labelled ones.

## Removed on 2026-10-22

These were removed because the task they described is finished, or because a script regenerates them from data that stays in the repo. Nothing is lost: each file is in git history (the first ten at commit `8a6842b`, the last three at commit `a7ace67`).

Read one without restoring it: `git show 8a6842b:Docs/<file name>` (or `a7ace67` for the last three). Restore one: `git checkout 8a6842b -- Docs/<file name>`.

| File | Why it was removed | To regenerate it |
|---|---|---|
| `ANTIGRAVITY_AGT_BRIEF.md` | Task brief for AG-T (100 training calls), finished | not needed; the calls and keys are in `inputs/AG-T/` |
| `ANTIGRAVITY_AGB_BRIEF.md` | Task brief for AG-B (50 sealed test calls), finished | `inputs/AG-B/` |
| `ANTIGRAVITY_AGB2_BRIEF.md` | Task brief for AG-B2 (12 gap-filling calls), finished | `inputs/AG-B2/` |
| `ANTIGRAVITY_AGC_BRIEF.md` | Task brief for AG-C (50 sealed test calls), finished | `inputs/AG-C/` |
| `AG50_DASHBOARD.html` | Generated charts page for AG50 | `python Scripts/ag50_analysis.py && python Scripts/build_ag50_dashboard.py` (needs `pip install scipy scikit-learn`). **Caveat:** the committed page had been edited by hand after it was generated (flow-v2 engine colours and wording), so the script rebuilds an earlier three-engine layout; the final page is only in git history |
| `ag50_stats.json` | Generated statistics for AG50 | `python Scripts/ag50_analysis.py` (needs `pip install scipy scikit-learn`); verified to reproduce the removed file exactly |
| `AG50_RESULTS.md` | Generated per-call comparison for AG50 | `python Scripts/compare_eval.py AG50 laya-stock laya-ft ollama --out Docs/AG50_RESULTS.md`; reproduces the removed file exactly, except the last column header now reads "Antigravity's note" (the script used to print "Claude's") |
| `EVAL50_RESULTS.md` | Generated per-call comparison for Eval50 | `python Scripts/compare_eval.py Eval50 laya-ft laya-stock ollama --out Docs/EVAL50_RESULTS.md`; verified identical |
| `LAYA_ROUND4_COMPARISON.md` | Generated per-call tables for test round 4 (the round's story stays in `LAYA_TEST_LOG.md`) | `python Scripts/compare_results.py ollama laya-v2 laya-v3.1 laya-ft --out Docs/LAYA_ROUND4_COMPARISON.md` (on Windows set `PYTHONIOENCODING=utf-8` first); verified identical |
| `PIPELINE_FLOWCHART_LAYA.md` | Ollama-era analysis of what Laya could replace; superseded by `FLOW_DIAGRAMS.md` | not needed |
| `ANTIGRAVITY_TEST_BRIEF.md` | Rulebook for the AI author of the first test set and the base of every later brief; not needed to run or maintain the app. Read it before commissioning a new AI-written set | not needed; read it from commit `a7ace67` |
| `ANTIGRAVITY_V2_COMMON.md` | Label rules and the key and marker format for AG-T and AG-B. The structure of a key is now described in `CODEBASE_GUIDE.md` section 5; `validate_calls.py` enforces the rules in code | read it from commit `a7ace67` |
| `ANTIGRAVITY_V2_EXAMPLES.md` | Worked examples of the labels | read it from commit `a7ace67` |
