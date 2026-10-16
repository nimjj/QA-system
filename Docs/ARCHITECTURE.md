# System Architecture & Technical Specifications

This document specifies the **Automated QA Analysis System**: the evaluation lifecycle, dynamic multi-tenant criteria selection, the deterministic rules, the Laya decision engine, and score normalization.

---

## 1. Master Pipeline Architecture

The system grades customer support interactions with a **hybrid of deterministic Python rules and the Laya decision engine**. Exact checks (scripts, timing, identity verification, profanity) run in plain Python. Judgement calls (empathy, rudeness, deflection, probing and so on) are yes/no questions answered by Laya.

Laya (`../laya-test/laya`) is a local, non-generative classifier. It returns a yes-probability per question in one forward pass and cannot write text. That is why every model input is kept short and pre-filtered, and why coaching tips are static text.

```mermaid
flowchart TD
    IN["POST /api/evaluate<br/>transcript + sentiment_score per turn + criteria"] --> PARSE["Parse turns<br/>agent / customer lines"]
    PARSE --> RULES["Python rules (no model)<br/>Branding · Dead air · Verified customer · Personalized call"]
    PARSE --> GATES["Python pre-filters pick a short snippet<br/>sentiment drop · phrase lists · similar questions"]
    GATES --> LAYA1["Laya yes/no per check<br/>Empathy (top 2 snippets) · Active listening · Ownership · Rapport · Probing"]
    PARSE --> PARA["Laya yes/no: Paraphrasing<br/>customer opening ≤50 words + first agent lines ≤150 words"]
    PARSE --> BATCH["Laya batches: one call, one question per item<br/>last 10 lines (Resolved) · agent-only text · full call"]
    RULES --> MERGE["Merge ratings · deductions · profanity auto-fail"]
    LAYA1 --> MERGE
    PARA --> MERGE
    BATCH --> MERGE
    MERGE --> SCORE["Category scores · weight normalization<br/>static PASS descriptions / FAIL coaching"]
```

---

## 2. Dynamic Multi-Tenant Criteria Engine

### 2.1 Dynamic Criteria Selection (`selected_criteria`)
All line items inside the tenant's categories are extracted into a normalized lowercase Python `set`:
```python
selected_criteria = {
    item.get("name", "").strip().lower()
    for cat in categories
    for item in cat.get("line_items", [])
}
```
Each check runs **if and only if** its name exists in `selected_criteria`:
```python
if "branding and survey check" in selected_criteria:
    rule_ratings.append(evaluate_branding(turns))
```
Unselected criteria are skipped entirely: no model calls and no deductions.

Built-in checks are matched by **exact name**, so renaming a built-in item in the database moves it to the generic batch path. Any other active item is rated by Laya in a batch using a question built from its name and description. A description starting with `VIOLATION-BASED` is asked as "did the agent violate this?"; anything else is asked as "did the agent do this?".

### 2.2 Dynamic Category Weight Normalization (`calculate_category_scores`)
When a tenant disables or omits categories, the remaining weights are re-balanced so a perfect call still scores 100.

For the evaluated categories $C_1, \dots, C_k$ with base weights $w_i$:

$$W_{\text{active}} = \sum_{i=1}^{k} w_i \qquad w_i' = \frac{w_i}{W_{\text{active}}} \qquad \text{Final Score} = \sum_{i=1}^{k} \left( \text{Score}_{C_i} \times w_i' \right)$$

Each category starts at 100 and loses each failed item's `deduction_value` (floor 0).

### 2.3 Static PASS descriptions and FAIL coaching
Laya cannot generate text, so the scorecard text is static:
* **PASS:** `RULE_BASED_PASS_DESCRIPTIONS` in `dynamic_evaluator.py`.
* **FAIL:** each check's own message (for example "Agent used rude or condescending language."), then `RULE_BASED_FAIL_COACHING` for batch-rated items, then a generic "Criteria standard for '…' was not met."

---

## 3. The 11 QA Evaluation Criteria

### Category 1: Soft Skills (Default Weight: 33.3%)
1. **Branding and Survey Check** (`evaluate_branding`, rule): `"thank you for calling s-net"` in the first 4 agent turns and `"thank you for choosing s-net"` in the last 4.
2. **Hold time and Dead Air** (`evaluate_hold_and_dead_air`, rule): gaps over 30 s between turns; **2 or more** such gaps fail.
   * A managed hold is not dead air: the agent announced it on the line before the gap ("place you on a brief hold", "bear with me"), or came back with "thanks for holding/waiting".
   * The exemption is capped at 120 s. It never applies when the customer breaks the silence with "Hello? Are you still there?".
3. **Personalized the call/ticket appropriately** (`evaluate_personalized_call`, rule): the request's `customer_name` appears in an agent line.
4. **Empathy & Acknowledgment Statement** (Laya):
   * A snippet is taken when a customer turn's `sentiment_score` is ≤ -15, drops ≥ 8 versus the **customer's own** previous 3 turns, or is negative and contains a frustration word ("frustrated", "nightmare", "third time" …).
   * It is skipped if the agent apologises within 3 turns. Each snippet is the customer turn plus the next 4 turns.
   * Only the **2 most severe, non-overlapping** snippets are checked, one Laya call each. One FAIL fails the item.
5. **Build rapport and observed professionalism** (Laya, violation-based): **every agent line** is checked, in consecutive chunks of at most 8 lines / 120 words, one Laya call per chunk (about 8 per call; the longest Main call needs 21). One rude chunk fails the item. Before version 10.2 only lines containing a listed rude phrase were sent, so a rude line without a listed phrase never reached Laya.

### Category 2: Technical Knowledge (Default Weight: 66.7%)
6. **Paraphrasing** (Laya): the customer's opening (≤ 50 words) and the first 10 agent lines (≤ 150 words) are sent with the question "does the agent restate the customer's problem?".
   * Greeting and verification lines from the agent, and account-detail answers from the customer (account number, PIN, a short address), are skipped first.
   * This criterion is new on Laya and not yet calibrated.
7. **Verified customer** (`evaluate_verified_customer`, rule): `\b(pin|address|security question)\b` in an agent line within the first 240 s.
8. **Probing** (Laya):
   * No agent questions at all means FAIL without a model call.
   * Otherwise only the question sentences of each agent turn are used, and greeting, identity-check, confirmation and wrap-up questions are dropped.
   * The remaining questions (≤ 100 words) plus the customer problem (≤ 50 words, account-detail answers skipped) go to Laya.
9. **Took ownership of the problem** (Laya, violation-based): agent lines containing a deflection phrase (`"not my department"`, `"call back"` …) are sent to Laya. No hit means PASS.
10. **Active listening** (Laya): possible repeats are sent to Laya as *first question / the customer's answer / second question* (at most 3 pairs, answer cut to 40 words). There are two sources:
    * pairs of agent question *sentences* with a `difflib` similarity above 0.55 (check-ins like "Is that right?" are ignored);
    * agent questions the customer answers with "like I said" / "I mentioned", paired with the most similar earlier question. These pairs go first. The customer's "like I said" reply itself is not sent: it made Laya read the pair as a status re-check.
11. **Confirmed the issue is resolved** (Laya batch): the **last 10 lines** of the call. Its cutoff is 0.73, chosen on the `b_*` bulk calls (see `Docs/LAYA_TEST_LOG.md`).

Escalation, Hostility and custom criteria (if a tenant adds them) are rated in Laya batches. Escalation and Hostility use the full call, which goes through Laya's windowed `predict_long` when it is longer than one window.

### Thresholds
Each Laya check has a `pass_threshold` in `LAYA_CHECKS` (`dynamic_evaluator.py`). The starting values come from a synthetic out-of-the-box test (`laya_eval/RESULTS.md`). Tests on full-length calls (`Docs/LAYA_TEST_LOG.md`) show several do **not** transfer yet: Resolved barely separates (its cutoff was re-picked on the `b_*` calls), Rapport is inverted, and Paraphrasing doesn't separate. Version 10.2 moved Probing's cutoff from 0.60 to 0.70 (it then separates all `b_*` and Main calls), and with the Rapport chunk scan the old 0.81 cutoff fails most polite calls (`Docs/LAYA_TEST_LOG.md`, Round 3), so it is set to an interim 0.50 (never fails) until the model is fine-tuned and the cutoff can be tuned at call level. Treat them as starting values to re-tune on human-reviewed calls; `Scripts/probe_laya.py` and `Scripts/laya_cutoffs.py` show the raw probabilities and the best cutoff per check.

### Category 3: Auto-Fail Circuit Breakers
* **Profanity & abuse:** a fixed word list (`"fuck"`, `"shut up"`, `"idiot"`, …) in any agent line forces a score of 0. Customer lines are not checked, so a customer swearing never fails the agent.
* **Scorecard circuit breaker:** any item in a category whose name contains "AUTO FAIL" that is rated FAIL forces a score of 0.

---

## 4. Database Schema Roadmap (Multi-Tenant Architecture)

The live tables are `tenants`, `categories`, `line_items` and `tenant_lines` (per-tenant `is_active` toggle) in `src/db/database.py`. The roadmap below adds evaluation history and a `rule_code` so built-in rules no longer depend on display names.

```mermaid
erDiagram
    TENANTS ||--o{ CATEGORIES : "configures"
    TENANTS ||--o{ USERS : "has"
    TENANTS ||--o{ EVALUATIONS : "owns"
    CATEGORIES ||--o{ LINE_ITEMS : "contains"
    EVALUATIONS ||--o{ EVALUATION_DETAILS : "records"
    LINE_ITEMS ||--o{ EVALUATION_DETAILS : "rated_in"

    TENANTS {
        string tenant_id PK
        string name
        boolean is_active
        timestamp created_at
    }

    CATEGORIES {
        int category_id PK
        string tenant_id FK
        string name
        float category_weight
        boolean is_active "Category Toggle"
    }

    LINE_ITEMS {
        int line_item_id PK
        int category_id FK
        string rule_code "BRANDING, DEAD_AIR, PROBING"
        string name "Display Name"
        string description
        int deduction_value
        boolean is_active "ON / OFF Toggle"
    }

    EVALUATIONS {
        int evaluation_id PK
        string tenant_id FK
        string call_id
        string channel
        float final_score
        boolean is_auto_fail
        string auto_fail_reason
        timestamp created_at
    }

    EVALUATION_DETAILS {
        int detail_id PK
        int evaluation_id FK
        int line_item_id FK
        string rating "PASS / FAIL"
        string coaching
    }
```

---

## 5. Codebase Map & Module Reference

| File Path | Description |
|---|---|
| `main.py` | QA service launcher (port 8006). Loads `.env`. |
| `run_gateway.py` | API Gateway launcher (port 8005). |
| `src/api/web_app.py` | FastAPI app: `/api/evaluate`, criteria/tenant CRUD, samples. |
| `src/api/logger.py` | Structured JSON request logger. |
| `src/gateway/gateway_app.py` | Gateway reverse proxy plus direct PostgreSQL routes for criteria fetch and toggle. |
| `src/db/database.py` | PostgreSQL data layer (tenants, categories, line items, toggles). |
| `src/services/dynamic_evaluator.py` | Orchestrator: criteria selection, input caps, Laya questions and thresholds, batches, scoring, static coaching. |
| `src/services/rule_engine.py` | Deterministic rules and snippet pre-filters (empathy, ownership, rapport chunks, active listening, probing inputs). |
| `src/services/laya_inputs.py` | `build_laya_inputs()`: parses a transcript and builds the text every Laya check receives. Shared with the training-data tools, so training rows match production exactly. |
| `src/services/laya_adapter.py` | Loads the Laya `Router` once and exposes `predict_yes()`. |
| `resources/criteria_config.json` | Reference criteria for tenant-abc (also used by the check script). |
| `Scripts/check_prompt_sizes.py` | Verifies input sizes and scorecards over all sample calls (`--live` runs real Laya). |
| `Scripts/batch_test.py` | Posts `inputs/Main tests` (default) or `inputs/Bulk tests` to `/api/evaluate` with inline criteria and saves results. |
| `Scripts/compare_results.py` | Compares result folders (by label) with the Main tests expected grades and the defects named in the `b_*` filenames. |
| `Scripts/probe_laya.py` | Runs the Main and Bulk calls in-process and records every Laya input and probability. |
| `Scripts/laya_cutoffs.py` | Best balanced-accuracy cutoff per Laya check from a probe file and the `b_*` filename defects. |
| `laya_eval/` | Synthetic 320-item gold set and the Laya vs Ollama benchmark behind the starting cutoffs (`RESULTS.md`). |
| `Docs/LAYA_TEST_LOG.md` | Ollama vs Laya test rounds on full-length calls, and the Laya training focus. |
| `Docs/PIPELINE_FLOWCHART_LAYA.md` | Pre-migration analysis of what Laya could replace. |
| `Docs/postman_collection.json` | Postman collection for the API. |
