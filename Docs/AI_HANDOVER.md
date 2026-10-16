# AI Handover Guide: QA Analysis System

If you are an AI assistant taking over this project, this is your map. `README.md` is the source of truth for setup and running. This file holds the context and constraints behind the design.

## Project Overview
A synchronous QA grading service for customer-support transcripts. It takes a call over a REST API, parses it, and grades it against tenant-configurable criteria. It uses deterministic Python rules plus **Laya**, a local yes/no decision engine. Ollama/Llama 3.1 was removed in version 10.

## Core Architecture
- **QA service (`src/api/web_app.py`, port 8006):** FastAPI. `POST /api/evaluate` grades a call synchronously and returns the scorecard. There is no queue, no Celery and no Redis.
- **Gateway (`src/gateway/gateway_app.py`, port 8005):** reverse proxy to the QA service, plus direct PostgreSQL routes for criteria fetch and toggle.
- **PostgreSQL (`src/db/database.py`):** tenants, categories, line items and per-tenant toggles. If a request carries `criteria_data`, the DB is not needed for that request.
- **Evaluator (`src/services/dynamic_evaluator.py`):** selects criteria, runs the rules, asks Laya, and scores.
- **Rule engine (`src/services/rule_engine.py`):** deterministic checks and the pre-filters that cut each Laya input down to a short snippet.
- **Laya adapter (`src/services/laya_adapter.py`):** loads the Laya `Router` once (English checkpoint) and exposes `predict_yes(text, questions)`, which returns P(yes) per question.

## Key constraints (read before changing the evaluator)
1. **Laya cannot generate text.** It only returns probabilities, so coaching tips are static strings (`RULE_BASED_PASS_DESCRIPTIONS`, `RULE_BASED_FAIL_COACHING`).
2. **Laya reads about 340 words per question.** Every input is capped:
   - Empathy: top 2 snippets, one call each.
   - Probing: problem ≤ 50 words plus questions ≤ 100 words.
   - Rapport: every agent line, in chunks of ≤ 8 lines / ≤ 120 words, one call per chunk.
   - Active listening: up to 3 question pairs, each with the customer's answer (≤ 40 words).
   - Paraphrasing: 50 + 150 words.
   - Resolved: the last 10 lines.
   
   Longer batch inputs fall back to windowed `predict_long`. Check sizes with `Scripts/check_prompt_sizes.py`.
3. **Every Laya question has explicit true/false criteria.** Without them the English checkpoint answers "no" regardless of the text.
4. **Thresholds are per check** (`LAYA_CHECKS`). They came from a synthetic test and need re-tuning on human-labelled calls: Confirmed-resolved, Rapport and Paraphrasing are known to be off on full-length calls.
5. **Built-in checks are matched by exact criterion name.** Renaming one in the DB sends it to the generic Laya batch instead.

## Directory Structure
- `inputs/Main tests/`: four hand-graded 16–22 minute calls, with expected scorecards in `expected/`. `inputs/Bulk tests/`: the older sample payloads. Batch-test outputs go to `inputs/Test (results)/`; older result files there come from the Ollama era.
- `tests/scoring_test/`: small raw-string transcripts with an intended quality tier.
- `resources/criteria_config.json`: reference criteria for tenant-abc.
- `Scripts/`: `batch_test.py` (posts inputs to the API) and `check_prompt_sizes.py` (verification, no server needed).

## How to Test
1. Start the service: `python main.py` (see README).
2. `python Scripts/batch_test.py [main|bulk] --label <engine>` posts that folder to `/api/evaluate` (criteria sent inline from `resources/criteria_config.json`, so no database is needed) and saves the scorecards to `inputs/Test (results)/<suite> (<label>)/`.
3. Without a server: `python Scripts/check_prompt_sizes.py` (stubbed model) or `python Scripts/check_prompt_sizes.py --live` (real Laya).

## Testing Structure (Guide for Transcript Generation)

To write mock transcripts that exercise each check, follow this structure.

### 1. JSON Payload Structure
```json
{
  "tenant_id": "tenant-abc",
  "customer_name": "Sarah",
  "transcript": [
    {"speaker": "Agent", "text": "Thank you for calling S-Net, my name is Alex. How can I help?", "start_time_sec": 0, "sentiment_score": 10.0},
    {"speaker": "Customer", "text": "Hi, I'm Sarah. My internet is completely down.", "start_time_sec": 10, "sentiment_score": -18.0},
    {"speaker": "Agent", "text": "To pull up your account, can you give me your PIN?", "start_time_sec": 20, "sentiment_score": 8.0}
  ]
}
```
**Important:**
- Put `sentiment_score` **on each turn**. A top-level `sentiment_scores` array is ignored by the API.
- Speakers must be exactly `Agent` / `Customer` in list payloads.
- Raw-string transcripts (`"[00:00] Agent: …"`) also work, but they carry no sentiment, so Empathy can never trigger.
- Keep baseline scores in the mid-positives (10 to 20) and only go negative to simulate frustration.

### 2. How Criteria are Measured (Triggers & Traps)

#### Rules (no model)
* **Branding and Survey Check:** "thank you for calling s-net" in the first 4 agent turns and "thank you for choosing s-net" in the last 4.
* **Hold time and Dead Air:** to **FAIL**, create 2 or more gaps of more than 30 s between consecutive `start_time_sec` values. A gap right after an announced hold ("place you on a brief hold") or ended by "thanks for holding" doesn't count (up to 120 s).
* **Personalized the call:** to **FAIL**, the agent never says the exact `customer_name`.
* **Verified customer:** the agent must say "PIN", "address" or "security question" within the first 4 minutes to **PASS**.

#### Pre-filter, then Laya
* **Empathy:**
  - It triggers on a customer turn with `sentiment_score` ≤ -15, a drop of ≥ 8 versus the customer's own previous 3 turns, or a negative score plus a frustration word ("nightmare", "third time" …).
  - It is skipped if the agent says sorry, apologize, understand, frustrating or "let me help" within 3 turns.
  - To **FAIL**, have the agent answer coldly. To **PASS** while still being checked, acknowledge the feeling without those keywords ("That sounds really stressful, let's fix it").
* **Active listening:** to **FAIL**, have the agent ask nearly the same question sentence twice (difflib similarity above 0.55), or re-ask something the customer answers with "like I said" / "I mentioned". Laya sees the first question, the customer's answer and the second question.
* **Took ownership:** only agent lines containing listed phrases are checked ("not my department", "call back" …). Lines without those phrases always pass.
* **Rapport:** every agent line is checked by Laya in chunks, so a rude line needs no particular phrase; one rude chunk fails the item. The cutoff is not tuned for this yet (Round 3 in `LAYA_TEST_LOG.md`).
* **Probing:** to **FAIL**, the agent asks only greetings, verification, confirmations or wrap-up questions.
* **Paraphrasing:** to **FAIL**, the agent never restates the customer's problem early in the call.
* **Confirmed the issue is resolved:** only the last 10 lines are read. To **FAIL**, end the call without confirming the fix worked.

### 3. Sentiment Score Simulation
Real scores move gradually, for example `0.0 -> -2.0 -> -5.0 -> -10.0 -> -20.0`, rather than jumping from +50 to -50. Ramp frustration down, let the agent respond well or badly, then recover (for example `-20.0 -> -5.0 -> +10.0`).
