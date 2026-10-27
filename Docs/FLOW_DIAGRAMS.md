# Flow diagrams: how a call becomes a score (as of 2026-10-22)

> **Status on `main` (27 Oct 2026):** this page describes the earlier `app-v3` branch. On `main` the job queue (`/api/jobs`, `src/v3/jobs.py`) and `docker-compose.v3.yml` were removed: `/api/evaluate` is synchronous, tenant scorecards come from PostgreSQL with the built-in 11 items as fallback, and the Docker setup is `docker-compose.yml` with the fine-tuned weights mounted from `models/`. The current deployment guide is [`DEPLOYMENT_PLAN.md`](../DEPLOYMENT_PLAN.md).

Nine diagrams, from the big picture down to one model call, plus how the model and the new checks were built. They draw what the code does today on branch `app-v3`. Under each diagram a table names the file and function behind every box, so a statement on a slide can be checked in the code in a minute. Read [`CODEBASE_GUIDE.md`](CODEBASE_GUIDE.md) first if the words "v2", "v3", "flow", "gate" or "cutoff" are new.

> **Every accuracy figure in this repo is measured against AI-written answer keys, not human-labelled ones.** Diagrams 8 and 9 mention results; read them with that in mind.

Colour legend used in diagrams 6 to 9: grey = plain Python rule, no model; blue = model check, unchanged from v2; green = model check with a new v3 gate that is switched on; orange = tried, did not win, switched off.

Contents: [1 System map](#1-system-map) · [2 Which pipeline runs](#2-which-pipeline-runs) · [3 Pipeline v2](#3-pipeline-v2-the-original-flow-one-request) · [4 Pipeline v3](#4-pipeline-v3-the-new-flow-one-request) · [5 One model call](#5-inside-one-model-call) · [6 The 11 checks](#6-the-11-checks-side-by-side) · [7 Scoring](#7-how-the-score-is-built) · [8 How a gate is chosen](#8-how-a-new-gate-is-chosen-and-switched-on) · [9 How the model is built](#9-how-the-model-and-the-test-sets-were-built)

---

## 1. System map

Who talks to whom when the whole stack is running. In v3 mode the database box is not used at all.

```mermaid
flowchart LR
    subgraph clients["Callers"]
        FE["Dashboard frontend<br/>React + Vite, port 5173"]
        PM["Postman, REST client,<br/>or another system"]
    end
    GW["API gateway<br/>run_gateway.py, port 8005"]
    APP["QA service, FastAPI<br/>main.py, port 8006"]
    DB[("PostgreSQL, port 5432<br/>tenants, categories, criteria<br/>used by pipeline v2 and the criteria screens")]
    MODEL["Laya model, one copy in memory<br/>checkpoint final-softce-3, about 1.95 GB"]

    FE -->|"UI lets you pick port 8005 or 8006"| GW
    FE -->|"or straight to the app"| APP
    PM --> APP
    PM --> GW
    GW -->|"proxies every other /api/ call"| APP
    GW -->|"criteria list and toggle read the DB directly"| DB
    APP -->|"v2: tenant criteria, tenants, categories"| DB
    APP -->|"yes or no questions about short pieces of the call"| MODEL
```

| Box | Where it is in the code | Note |
|---|---|---|
| Frontend | `frontend/src/App.jsx` (`apiBase` is `http://<host>:<port>/api`, port chosen in a drop-down) | Manages tenants and criteria, sends sample calls to `/api/evaluate` |
| Gateway | `run_gateway.py` starts `src/gateway/gateway_app.py` | Two routes talk to the DB itself; everything else is forwarded to `APP_URL` (default `http://localhost:8006`) |
| QA service | `main.py` starts `src/api/web_app.py` | All endpoints, the evaluators, the v3 queue |
| Database | `src/db/database.py` (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) | Needed by v2 and by the tenant and criteria screens. v3 grades against `src/v3/config/criteria.json` and never opens a connection |
| Model | `src/services/laya_adapter.py` | One copy, guarded by a lock: it answers one question at a time |

---

## 2. Which pipeline runs

Two settings decide what happens to a request: `LAYA_FLOW` and whether `LAYA_CHECKPOINT` is set. Today `.env` sets the checkpoint and does not set `LAYA_FLOW`, so **pipeline v2 with flow v2 windows is what runs by default**. Setting `LAYA_FLOW=v3` switches to the new pipeline.

```mermaid
flowchart TD
    REQ["POST /api/evaluate arrives"] --> Q1{"LAYA_FLOW = v3 ?"}
    Q1 -->|"yes"| P3["Pipeline v3<br/>src/v3, built-in criteria, job queue"]
    Q1 -->|"no"| P2["Pipeline v2<br/>evaluate_interaction, criteria from the request or PostgreSQL"]
    P2 --> Q2{"Which snippet-cutting rule?<br/>flow_version in laya_inputs.py"}
    P3 --> Q2
    Q2 -->|"LAYA_FLOW = v1"| W1["Flow v1: the original extractors"]
    Q2 -->|"LAYA_FLOW = v2"| W2["Flow v2: windows chosen by call structure<br/>laya_windows.py"]
    Q2 -->|"LAYA_FLOW not v1 or v2"| Q3{"LAYA_CHECKPOINT set?"}
    Q3 -->|"yes: fine-tuned model"| W2
    Q3 -->|"no: stock model"| W1
```

| Setting | Effect | Where |
|---|---|---|
| `LAYA_FLOW=v3` | Selects pipeline v3 (also `/api/jobs` exists, the DB is not used) | `src/api/web_app.py` `_v3_enabled()` |
| `LAYA_FLOW=v1` or `v2` | Forces the snippet-cutting rule | `src/services/laya_inputs.py` `flow_version()` |
| `LAYA_CHECKPOINT` set | Loads the fine-tuned weights, applies the fine-tuned cutoffs, and (if `LAYA_FLOW` is unset or `v3`) uses flow v2 windows | `laya_adapter.py`, `dynamic_evaluator.py` `FINETUNED_CUTOFFS`, `flow_version()` |
| `LAYA_AL_SOURCE2=1` | Adds a second source of candidate pairs for Active listening; only for ft5 and ft6, off for production | `laya_inputs.py` `al_source2_enabled()` |

Pipeline v3 reuses the flow v2 window builders for the checks it has not changed, so "v3" and "flow v2" are not alternatives: v3 is the pipeline around them.

---

## 3. Pipeline v2 (the original flow), one request

```mermaid
flowchart TD
    IN["POST /api/evaluate<br/>transcript, customer_name, optional criteria_data"] --> CRIT["Criteria: the request's criteria_data,<br/>else read from PostgreSQL for the tenant"]
    CRIT --> PARSE["parse_transcript<br/>turns, start times (end assumed start + 10 s),<br/>sentiment per turn, customer name"]
    PARSE --> RULES["4 rule checks, no model<br/>Branding, Hold and dead air,<br/>Verified customer, Personalized"]
    PARSE --> CUT["Cut each model check its own short snippet<br/>build_laya_inputs, flow v2 windows"]
    CUT --> E["Empathy: up to 4 windows,<br/>an upset customer line plus the next 4 turns"]
    CUT --> PA["Paraphrasing: customer problem plus the agent line<br/>with a restatement phrase in the first 300 s.<br/>No such line: FAIL without asking the model"]
    CUT --> AL["Active listening: pairs of similar agent questions,<br/>at most 3 pairs. No pair: PASS"]
    CUT --> OW["Ownership: agent lines containing a listed phrase,<br/>at most 6 lines. None: PASS"]
    CUT --> RA["Rapport: EVERY agent line,<br/>in chunks of 8 lines or 120 words"]
    CUT --> PR["Probing: customer problem plus the agent's questions<br/>without greeting and wrap-up questions.<br/>No question mark anywhere: FAIL without the model"]
    CUT --> RS["Resolved: the last 10 lines of the call"]
    E --> ASK["Ask the Laya model one yes or no question per snippet<br/>one FAIL in any snippet fails the check<br/>see diagram 5"]
    PA --> ASK
    AL --> ASK
    OW --> ASK
    RA --> ASK
    PR --> ASK
    RS --> ASK
    RULES --> MERGE["Collect the 11 ratings"]
    ASK --> MERGE
    MERGE --> AF{"Auto-fail?<br/>an agent line contains fuck, shut up, idiot,<br/>stupid, get lost or hang up"}
    AF -->|"yes"| ZERO["Final score 0"]
    AF -->|"no"| SCORE["Category scores and weighted final score<br/>see diagram 7"]
    ZERO --> OUT["Response: final_score, scorecard with coaching text,<br/>is_auto_fail, auto_fail_reason"]
    SCORE --> OUT
```

| Box | Code |
|---|---|
| Endpoint | `src/api/web_app.py` `evaluate_tenant_transcript` -> `src/services/dynamic_evaluator.py` `evaluate_interaction` |
| Criteria from DB | `src/db/database.py` `get_active_criteria_for_evaluation` |
| Parse | `src/services/laya_inputs.py` `parse_transcript`, `build_laya_inputs` |
| Rule checks | `src/services/rule_engine.py` `evaluate_branding`, `evaluate_hold_and_dead_air`, `evaluate_verified_customer`, `evaluate_personalized_call` |
| Empathy windows | `src/services/laya_windows.py` `empathy_episode_windows` (trigger: sentiment at or below -15, or a frustration word) |
| Paraphrasing window | `laya_windows.py` `paraphrase_window` (cue regex `_PARAPHRASE_CUE`) |
| Active listening pairs | `rule_engine.py` `extract_active_listening_snippets` (difflib similarity above 0.55) |
| Ownership phrases | `laya_windows.py` `ownership_candidates` (`_OWNERSHIP_PHRASES`, `_OWNERSHIP_RE`) |
| Rapport chunks | `rule_engine.py` `extract_rapport_chunks` |
| Probing input | `rule_engine.py` `extract_probing_inputs` (50 words of problem, 100 words of questions) |
| Resolved window | `laya_inputs.py`: `clean_lines[-RESOLVED_TAIL_LINES:]`, 10 lines; asked as a "batch" item by name in `evaluate_interaction` |
| Auto-fail | `dynamic_evaluator.py` `check_auto_fail` (plain substring match on agent text) |
| Score | `dynamic_evaluator.py` `calculate_category_scores` |

Things v2 does that v3 deliberately does not: it assumes every turn lasts 10 seconds, so dead air is guessed; its criteria query is not limited to the tenant's own categories; it matches the auto-fail words as substrings ("that's not a stupid question" zeroes a call); a tenant whose category names differ from "Soft Skills" and "Technical Knowledge" silently gets 100.

---

## 4. Pipeline v3 (the new flow), one request

Three layers: the web layer protects the service, the queue makes sure the single model is used by one call at a time, and the worker does the grading.

```mermaid
flowchart TD
    subgraph web["Web layer, src/api/web_app.py"]
        REQ["POST /api/evaluate or POST /api/jobs"] --> KEY{"QA_API_KEY set<br/>and wrong or missing?"}
        KEY -->|"yes"| E401["401"]
        KEY -->|"no"| SIZE{"Body larger than<br/>MAX_REQUEST_BYTES, 2 MB?"}
        SIZE -->|"yes"| E413["413"]
        SIZE -->|"no"| PRE["Pre-check: normalise the transcript<br/>and load the built-in criteria"]
        PRE -->|"empty or unreadable"| E422["422"]
        PRE -->|"over 1500 turns, 4000 characters<br/>per turn or 250000 in all"| E413b["413"]
        PRE -->|"gradable"| SUB["Submit a job"]
    end
    subgraph q["Queue, src/v3/jobs.py"]
        SUB --> FULL{"Waiting line full (50)<br/>or model failed to load?"}
        FULL -->|"yes"| E503["503 with Retry-After 30"]
        FULL -->|"no"| LINE["Job waits in line"]
        LINE --> WORKER["ONE worker thread takes jobs in order,<br/>and forgets the transcript as soon as it starts"]
    end
    subgraph work["Worker, src/v3/pipeline.py evaluate_v3"]
        WORKER --> N["1 normalise: roles, real times,<br/>null-safe sentiment, empty turns dropped"]
        N --> R["2 four v3 rule checks, no model"]
        N --> T["3 agent and customer turns only,<br/>question marks restored on bare questions"]
        T --> WIN["4 cut the windows<br/>the frozen v2 builders, build_laya_inputs"]
        WIN --> GATE["5 per-check gates from config v3.json<br/>Resolved v3 and Ownership v3 on,<br/>Empathy, Paraphrasing and the rest as v2"]
        GATE --> M["6 ask the model, see diagram 5"]
        R --> AFC
        M --> AFC{"7 auto-fail?<br/>word patterns on agent lines only"}
        AFC --> SC["8 score by item name, see diagram 7"]
        SC --> OUTP["9 scorecard, evidence turns, and meta:<br/>flow, gates, model rows and words, seconds, warnings"]
    end
    OUTP --> RES["Result stored on the job"]
    RES --> DONE["/api/evaluate: answer 200 with the result<br/>/api/jobs: poll GET /api/jobs/id until status is done"]
```

How the two entry points behave when the line is busy:

```mermaid
sequenceDiagram
    participant C as Caller
    participant A as web_app.py
    participant Q as JobQueue
    participant W as Worker and model

    Note over C,W: POST /api/evaluate (waits for the result)
    C->>A: transcript
    A->>A: key, size and transcript pre-checks
    A->>Q: submit
    Q-->>W: job runs when it reaches the front
    alt finished within EVALUATE_TIMEOUT_SEC, 120 s
        W-->>A: result
        A-->>C: 200 with call_id, tenant_id, status completed, result
    else still running after 120 s
        A-->>C: 503, Retry-After 30, body holds job_id
        Note over W: the call keeps being graded
        C->>A: GET /api/jobs/job_id later
        A-->>C: 200 with status done and the result
    end

    Note over C,W: POST /api/jobs (does not wait)
    C->>A: transcript
    A->>Q: submit
    A-->>C: 202 with job_id, status queued, queue_position while waiting
    C->>A: GET /api/jobs/job_id
    A-->>C: queued, running, done with the result, or failed with an error
```

| Box | Code |
|---|---|
| API key, size limit, redacted log | `web_app.py` `log_requests_middleware`, `_api_key_ok`, `_safe_body`, `MAX_REQUEST_BYTES` |
| Pre-check and submit | `web_app.py` `_submit_v3`; errors mapped by `_error_status` (`InvalidTranscript` and `NoCriteria` -> 422, `TranscriptTooLarge` -> 413) |
| Queue and worker | `src/v3/jobs.py` `JobQueue` (bounded by `QUEUE_MAX`, default 50; finished jobs are forgotten after 3600 s) |
| Model loads at startup | `web_app.py` `_warm_model`; `/ready` answers 503 until it has loaded |
| Normalise | `src/v3/normalise.py` `normalise` (limits in `src/v3/config/v3.json`) |
| Rules | `src/v3/rules.py` `evaluate_branding`, `evaluate_dead_air`, `evaluate_verified`, `evaluate_personalized`, `check_auto_fail` |
| Question marks | `src/v3/text.py` `add_question_marks`, used by `pipeline._v2_transcript` |
| Windows | `src/services/laya_inputs.py` `build_laya_inputs` (frozen, unchanged) |
| Gates | `pipeline._model_ratings`; the switches are the `gates` block of `src/v3/config/v3.json`; the windows are in `src/v3/candidates/` |
| Scoring | `src/v3/scoring.py` `score` |
| Built-in criteria | `src/v3/config/criteria.json` (a copy of the default set; `criteria_data` in a request is ignored) |

---

## 5. Inside one model call

Every model check, in both pipelines, ends here. The model never writes text: it returns the probability that the answer to one typed question is "yes".

```mermaid
flowchart TD
    A["A short window of the call plus one typed yes or no question<br/>question wording: LAYA_CHECKS in dynamic_evaluator.py"] --> B["predict_yes in laya_adapter.py<br/>takes a global lock, so one call at a time"]
    B --> C["Laya Router, ModernBERT-large, 421 million parameters<br/>weights: LAYA_CHECKPOINT if set, else stock 'english'"]
    C --> D{"Text longer than the 512-token window?"}
    D -->|"yes"| E["predict_long: overlapping windows,<br/>the strongest window decides"]
    D -->|"no"| F["P(yes)"]
    E --> F
    F --> G{"Which answer means PASS for this check?"}
    G -->|"yes means PASS<br/>Empathy, Paraphrasing, Probing, Resolved"| H["P(pass) = P(yes)"]
    G -->|"yes means FAIL<br/>Active listening, Ownership, Rapport"| I["P(pass) = 1 - P(yes)"]
    H --> J{"P(pass) at or above the check's cutoff?"}
    I --> J
    J -->|"yes"| K["PASS"]
    J -->|"no"| L["FAIL"]
```

Cutoffs in force with the fine-tuned checkpoint (`FINETUNED_CUTOFFS` and `LAYA_CHECKS` in `src/services/dynamic_evaluator.py`):

| Check | Question the model is asked (shortened) | Yes means | Cutoff on P(pass) |
|---|---|---|---|
| Empathy | Does the agent acknowledge the customer's frustration with empathy? | PASS | 0.49 |
| Paraphrasing | Does the agent restate the customer's problem back to them? | PASS | 0.47 |
| Active listening | Does the second agent question ask again for information the customer already gave? | FAIL | 0.50 |
| Ownership | Does the agent deflect responsibility, blame another team, or refuse to help? | FAIL | 0.52 |
| Rapport | Is any agent line rude, condescending, dismissive, sarcastic or unprofessional? | FAIL | 0.20 |
| Probing | Did the agent ask at least one genuine diagnostic question? | PASS | 0.70 |
| Resolved (v2) | Did the agent explicitly confirm that the issue was resolved? | PASS | 0.42 |
| Resolved (v3) | same question, but see diagram 6: the model score is blended with the customer's end-of-call mood | PASS | 0.65 on the blended score |

With the stock (not fine-tuned) model the cutoffs in `LAYA_CHECKS` apply instead; they are different and the stock model is much less accurate.

---

## 6. The 11 checks side by side

What each check looks at in v2 and in v3, and whether a new gate is on. Dotted arrows mean "same as v2".

```mermaid
flowchart LR
    subgraph rules["Plain Python rules, no model"]
        R1["Branding and Survey Check<br/>v3: accepts speech-to-text spellings of S-Net,<br/>greeting and closing on two different lines"]
        R2["Hold time and Dead Air<br/>v3: real gaps from end times, holds and customer<br/>look-ups excused, one 2-minute silence fails"]
        R3["Verified customer<br/>v3: agent must ask for PIN, address or security answer,<br/>email or IP address does not count"]
        R4["Personalized the call<br/>v3: whole-word name match,<br/>Sam no longer matches Samsung"]
    end
    subgraph green["Model check with a new v3 gate, ON"]
        G1["Resolved<br/>v2: last 10 lines, cutoff 0.42<br/>v3: last 16 informative lines, goodbyes skipped,<br/>blended 50 50 with the customer's end-of-call mood,<br/>cutoff 0.65"]
        G2["Ownership<br/>v2: window only if a listed phrase appears<br/>v3: much wider list of deflection wordings opens the window,<br/>the model still decides"]
    end
    subgraph blue["Model check, same as v2"]
        B1["Rapport<br/>every agent line in chunks, cutoff 0.20"]
        B2["Active listening<br/>similar agent question pairs<br/>v3 adds the missing question marks"]
        B3["Probing<br/>problem plus the agent's questions<br/>v3 adds the missing question marks"]
    end
    subgraph orange["Alternative tried, NOT adopted, switched off"]
        O1["Empathy<br/>v2 windows kept. Call-relative trigger tried:<br/>found more outbursts but failed many more good calls"]
        O2["Paraphrasing<br/>v2 window kept. Wider search tried: better on AG-T,<br/>worse on AG50, slightly worse on the hold-out sets"]
    end
    classDef rule fill:#e8e8e8,stroke:#555,color:#111;
    classDef same fill:#dbeafe,stroke:#1d4ed8,color:#111;
    classDef newg fill:#dcfce7,stroke:#15803d,color:#111;
    classDef tried fill:#ffedd5,stroke:#c2410c,color:#111;
    class R1,R2,R3,R4 rule;
    class B1,B2,B3 same;
    class G1,G2 newg;
    class O1,O2 tried;
```

Switches: `gates` in `src/v3/config/v3.json`. `"mode": "v3"` uses the new window, `"mode": "v2"` the original one. Changing a switch needs no code change.

How the v3 Resolved score is formed (`src/v3/candidates/resolved.py`):

```mermaid
flowchart TD
    A["Window: the last 16 informative lines, at most 320 words<br/>thanks and goodbye lines skipped, the call's final two lines kept"] --> B["Model: P(pass) that the agent confirmed the issue is resolved"]
    C["Customer sentiment per turn, customer side only"] --> D{"At least 4 scored customer turns?"}
    D -->|"no"| E["Score = model P(pass) alone"]
    D -->|"yes"| F["End mood = mean of the customer's last 3 sentiments<br/>minus the median of the customer's sentiments in this call<br/>so no absolute scale is assumed"]
    F --> G["Mood score = 1 / (1 + e to the power of minus end mood / 10)"]
    B --> H["Score = 0.5 x model + 0.5 x mood score"]
    G --> H
    B --> E
    H --> I{"Score at or above 0.65?"}
    E --> I
    I -->|"yes"| J["PASS"]
    I -->|"no"| K["FAIL"]
```

---

## 7. How the score is built

```mermaid
flowchart TD
    A["11 ratings, each PASS or FAIL"] --> B["Each category starts at 100.<br/>Every FAIL subtracts that item's deduction, never below 0"]
    B --> C["Soft Skills, weight 0.333<br/>Branding 15, Dead air 15, Personalized 15,<br/>Empathy 35, Rapport 20"]
    B --> D["Technical Knowledge, weight 0.667<br/>Paraphrasing 15, Verified 25, Probing 25,<br/>Ownership 25, Active listening 10, Resolved 15"]
    C --> E["Weighted average, weights rescaled to add up to 1"]
    D --> E
    F{"Auto-fail triggered?"} -->|"yes"| G["Every category 0, final score 0"]
    F -->|"no"| E
    E --> H["Final score, one decimal"]
    A --> I["Scorecard: category, name, PASS or FAIL, coaching text<br/>fixed sentences for PASS and FAIL, the rules add specifics<br/>such as the longest silence. The model cannot write text"]
```

| Part | v2 | v3 |
|---|---|---|
| Deductions and weights | Read from the criteria (request or DB) | Read from `src/v3/config/criteria.json` |
| Matching a rating to its item | By the category name written on the rating; a tenant with other category names silently scores 100 | By item name against the criteria's own categories |
| No active criteria | Scores 100 | Not possible: the built-in set is always used |
| Auto-fail | `check_auto_fail` in `dynamic_evaluator.py`: substring match of fuck, shut up, idiot, get lost, stupid, hang up on agent text | `check_auto_fail` in `src/v3/rules.py`: word patterns with an allow-list ("that's not a stupid question", "please hang up and call back" do not trigger) |
| Extra output | none | `evidence_turns` per item, `meta` (flow, config version, model, gates, rows and words sent to the model, seconds, warnings) |

Deductions come from `resources/criteria_config.json` (v2 reference set) and `src/v3/config/criteria.json` (v3), which hold the same values.

---

## 8. How a new gate is chosen and switched on

This is how Resolved and Ownership were adopted and how Empathy and Paraphrasing were rejected. The same steps apply to any future change.

```mermaid
flowchart TD
    A["Spot a gap: the window may be hiding the evidence<br/>e.g. Ownership gate opens on 1 of 14 failing calls"] --> B["Write candidate windows<br/>src/v3/candidates/"]
    B --> C["../laya-finetuning/eval/v3_gate_lab.py scores every candidate with the real model<br/>against the answer keys, answers cached"]
    C --> D["Choose the variant and its cutoff on the DEVELOPMENT sets<br/>AG-T and AG50, 150 calls"]
    D --> E["Confirm on the HOLD-OUT sets<br/>AG-B, AG-B2, AG-C, 112 calls"]
    E --> F{"Better on both,<br/>and not just by luck?"}
    F -->|"no, or mixed"| G["Keep v2 for that check.<br/>Code stays, switch stays off<br/>Empathy, Paraphrasing"]
    F -->|"yes"| H["Add it to gates in src/v3/config/v3.json"]
    H --> I["../laya-finetuning/eval/v3_compare.py runs v2 and v3 end to end<br/>through the real pipeline against the keys"]
    I --> J["Count calls only v3 got right against calls only v2 got right<br/>paired test, and mean error of the final score"]
    J --> K["A person reviews the calls where v2 and v3 disagree<br/>still to do: the keys are AI-written"]
```

Result of the end-to-end comparison (all figures against AI-written keys; files `../laya-finetuning/runs/v3/e2e_*.jsonl`):

| Set group | Calls | The 11 items matching the key, v2 -> v3 | Better / worse | p | Mean final-score error |
|---|---|---|---|---|---|
| Development (AG-T, AG50) | 150 | 1389 -> 1407 of 1650 | 45 / 27 | 0.044 | 10.5 -> 9.9 points |
| Hold-out (AG-B, AG-B2, AG-C) | 112 | 1031 -> 1056 of 1232 | 46 / 21 | 0.003 | 11.0 -> 9.0 points |

Almost all of the gain is the Resolved check. The Resolved hold-out numbers were read before the variant was finally picked, so they are a confirmation with some selection in them, not a clean test.

---

## 9. How the model and the test sets were built

Where the weights and every set of test calls came from. Every answer key in this chain was written by an AI and none has been checked by a human.

```mermaid
flowchart TD
    A0["Claude-written call fragments<br/>../laya-finetuning/data/fragments/claude<br/>stages 1 to 3, used for final-softce-3"] --> E
    A["Briefs for an AI author<br/>rulebook, key format and one task brief per set<br/>(removed from the repo, in git history)"] --> B["The AI author writes calls and answer keys<br/>each key rates the 11 items and marks the key moments"]
    B --> C["../laya-finetuning/eval/validate_calls.py<br/>checks format, recomputes the rule items with the app's own code"]
    C --> D["../laya-finetuning/inputs/AG-T training calls, AG50 development calls,<br/>AG-B, AG-B2, AG-C test calls, each with expected/ keys"]
    D --> E["../laya-finetuning/tools/build_ag_rows.py, build_rows.py<br/>cut the calls with the production windows into training rows"]
    E --> F["make_mix2.py mixes the rows<br/>build_train_notebook.py writes the Colab notebook"]
    F --> G["Colab GPU: notebooks 01 to 04 in ../laya-finetuning/<br/>laya_train_cuda.py fine-tunes Laya, saves to Google Drive"]
    G --> H["Download and install into<br/>../laya-finetuning/checkpoints/run-name/"]
    H --> I["checkpoint_manifest.py records and verifies the file hashes<br/>record kept in ../laya-finetuning/runs/"]
    I --> J["../laya-finetuning/eval/probe_laya.py records every probability on the development sets<br/>choose_cutoffs.py picks cutoffs, written down BEFORE the exam"]
    J --> K["One exam on a set the model never saw<br/>AG-B plus AG-B2, then AG-C"]
    K --> L["Paired test, score error, RESULT.md, ../laya-finetuning/runs/CHECKPOINTS.md<br/>decision recorded"]
    L --> M["Decision of 2026-10-22: production stays on final-softce-3,<br/>which was trained on Claude-written rows only"]
    Z["export_checks.py --check<br/>every training row records a hash of the question wording and the<br/>window code; if the app's window code changes the data must be rebuilt"] -.-> E
    Z -.-> M
```

| Step | Where |
|---|---|
| Briefs | The rulebook, the key and marker format, worked examples and one task brief per set (AG-T, AG-B, AG-B2, AG-C) were removed on 2026-10-22 once the sets were sealed. They are in git history at commit `a7ace67`; the structure of an answer key is described in `CODEBASE_GUIDE.md` section 5 |
| Calls and keys | `../laya-finetuning/inputs/AG-T`, `../laya-finetuning/inputs/AG50`, `../laya-finetuning/inputs/AG-B`, `../laya-finetuning/inputs/AG-B2`, `../laya-finetuning/inputs/AG-C` (`expected/` folders hold the keys) |
| Row building | `../laya-finetuning/tools/build_ag_rows.py`, `build_rows.py`, `make_mix2.py`; rows in `../laya-finetuning/data/rows/` |
| Training | `../laya-finetuning/0x_train_eval*.ipynb` on Google Colab; `../laya-finetuning/tools/laya_train_cuda.py` |
| Weights | `../laya-finetuning/checkpoints/` (git-ignored, never pushed); catalogue `../laya-finetuning/runs/CHECKPOINTS.md` |
| Freeze check | `../laya-finetuning/tools/export_checks.py`; frozen file `../laya-finetuning/data/frozen/checks_frozen.json` |
| Probes and exams | `../laya-finetuning/eval/probe_laya.py`, `choose_cutoffs.py`, `cutoff_eval.py`; results under `../laya-finetuning/runs/` and `inputs/Test (results)/` |
| Why the frozen files must not change | `laya_inputs.py`, `rule_engine.py`, `laya_windows.py` and the question wording are hashed into the training data; v3 imports them and never edits them |
