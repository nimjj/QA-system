# Brief for Antigravity: write 50 independent test calls and their answer keys

You already know the QA project (the `qa-analysis` call-grading service). This document explains **why** we need 50 new calls, **what we have found so far**, and **exactly what to produce**. Read all of it before writing anything.

---

## 1. What you are being asked to do (one paragraph)

Write **50 realistic S-Net customer-support phone calls, each 10 to 20 minutes long**, as JSON request payloads (with a sentiment score on every turn), and for each call write the **response payload an experienced call-centre QA expert would produce** (the ideal scorecard and final score). We will run three grading engines on your calls and compare each one against your answer keys. Your keys are the yardstick, so they must be right, clear-cut and written independently.

---

## 2. Background: what this project is

`qa-analysis` grades telephony support calls. Each call is graded on **11 criteria** and gets a score out of 100.

- **4 criteria are rule-based** (fixed code): Branding, Hold time and dead air, Verified customer, Personalized.
- **7 criteria need judgement.** Today an LLM (Ollama, `llama3.1`) judges them. We are replacing it with **Laya**, a small local model (ModernBERT-large, 421M parameters, 512-token window) that answers one yes/no question per criterion about a short snippet cut from the call. It is faster (about 8 s per call against about 2 minutes), runs on CPU, and we **fine-tuned** it on synthetic calls so it grades like our QA team.

The three engines we will compare on your calls:

| Engine | What it is |
|---|---|
| **Ollama** | the current production judge (llama3.1) |
| **Laya stock** | the original Laya checkpoint, no training |
| **Laya fine-tuned** | our trained checkpoint (the candidate replacement) |

---

## 3. What we have found so far (and why we need you)

Two test sets exist. **Both were written and graded by the same AI (Claude) that wrote the fine-tuned model's training data**, with no human review.

| Test set | Calls | Fine-tuned Laya | Laya stock | Ollama |
|---|---|---|---|---|
| Main (long calls, 16-22 min) | 4 (44 items) | 41/44 items match the key | n/a here | 40/44 |
| Eval50 (short calls, 1-5 min) | 50 (550 items) | **506/550 (92%)** | 458/550 (83%) | 448/550 (81%) |

Other Eval50 facts: mean error of the final score was 6.0 (fine-tuned), 12.2 (stock), 9.3 (Ollama) points. Time per call was 7.8 s, 7.7 s and 122.6 s. Weakest items for the fine-tuned model were **Took ownership** (balanced accuracy 0.68) and **Active listening** (0.70). On 22 items, all three engines agreed with each other and **disagreed with the key**, which means either a shared blind spot or an over-strict key.

**Why that is not enough:**
1. The author of the training data also wrote the answer keys, so a good score may only mean "the model learned Claude's style".
2. Eval50 calls are short (1-5 minutes). Real calls are 10-20 minutes, and the model only sees snippets of a long call, so long calls are the real test.
3. Some numbers (for example the Rapport cutoff) were tuned on the Main calls, so Main is no longer a clean test.

**You are the independent author.** A different model family writes the calls *and* the answer keys, with a different style and different instincts. If the fine-tuned model still does well on your calls, we can believe it. If it does badly, we learn exactly where.

---

## 4. Independence rules (important)

1. **Do NOT open** any of these: `laya-finetuning/` (anywhere), `qa-analysis/inputs/Eval50/`, `qa-analysis/inputs/Main tests/`, `qa-analysis/inputs/Bulk tests/`, `qa-analysis/inputs/Tough checks/`, `qa-analysis/inputs/Test (results)/`, `qa-analysis/Docs/EVAL50_RESULTS.md`, `qa-analysis/Docs/LAYA_*`. They contain the earlier calls, keys and results. Reading them would copy their style and spoil the test.
2. **Do NOT read** `src/services/dynamic_evaluator.py`, `laya_*`, or any model code to decide how to grade the 7 judged criteria. Grade those **as a human QA expert would**, from the criteria below.
3. You **may** read `src/services/rule_engine.py` (functions `evaluate_branding`, `evaluate_hold_and_dead_air`, `evaluate_verified_customer`, `evaluate_personalized_call`) and `resources/criteria_config.json`, **only** to double-check the 4 rule-based items. They are deterministic, so the key must match the code exactly.
4. Do not write calls to be easy or hard for any particular engine. You will never see their outputs.
5. Do not reuse dialogue, scenario or agent/customer name patterns across your own calls. Each call must read as its own call, not a template with swapped nouns.

---

## 5. Deliverables and file layout

All files go in `qa-analysis/inputs/AG50/`:

```
inputs/AG50/
  ag_01.json ... ag_50.json                 request payloads (section 6)
  expected/expected_ag_01.json ... expected_ag_50.json   answer keys (section 8)
  SUMMARY.md                                one table row per call (section 11)
  selfcheck.py                              your own validator (section 11)
```

The file names matter. Our scripts pair `ag_NN.json` with `expected/expected_ag_NN.json`, and `call_id` inside the key must be `ag_NN`.

---

## 6. Request payload format (`ag_NN.json`)

Same shape as our existing payloads:

```json
{
  "tenant_id": "tenant-abc",
  "customer_name": "Priyanka",
  "transcript": [
    {
      "speaker": "Agent",
      "start_time": "[00:00]",
      "end_time": "[00:06]",
      "start_time_sec": 0,
      "text": "Thank you for calling S-Net, my name is Daniel. How can I help you today?",
      "sentiment_score": 8.0
    },
    {
      "speaker": "Customer",
      "start_time": "[00:07]",
      "end_time": "[00:17]",
      "start_time_sec": 7,
      "text": "Hi Daniel. My broadband has been dropping out every half an hour since yesterday.",
      "sentiment_score": -24.0
    }
  ]
}
```

Field rules:
- `tenant_id`: always `"tenant-abc"`.
- `customer_name`: the customer's **first name only** (what an agent would say aloud). One string.
- `speaker`: exactly `"Agent"` or `"Customer"`.
- `start_time` / `end_time`: `"[MM:SS]"` strings. `start_time_sec`: integer seconds equal to `start_time`.
- `text`: what was said, as speech-to-text would write it.
- `sentiment_score`: a float on every turn, one decimal, e.g. `-24.0`.
- Turns must be in time order, and a turn cannot start before the previous one ends.

### 6.1 Timing and length (each call must be 10 to 20 minutes)

- **The last turn's `end_time` must fall between `[10:00]` and `[20:00]`.** No call outside that range.
- Spread: about 10 calls of 10-12 min, 15 of 12-15 min, 15 of 15-18 min, 10 of 18-20 min.
- A 10-20 minute call has roughly **60 to 160 turns** and **1,200 to 2,800 words**. Length must come from real support work: troubleshooting steps, account checks, holds, repeated explanations, side topics. **Do not pad with filler.**
- Speech takes time: a turn lasts about **words ÷ 2.5 seconds**. Between turns there is a normal pause of **1 to 4 seconds** unless you are deliberately creating a hold or silence.
- Holds and silences take clock time and must show as gaps between the previous turn's `end_time` and the next turn's `start_time`.
- **Keep every turn to 30 seconds of speech or less (about 75 words).** Split longer explanations into two Agent turns with a short customer acknowledgment in between ("mm-hm", "okay", "right"). Reason: the app assumes each turn lasts 10 s when it measures dead air (see 7.1). A very long turn would make the app see a "gap" that a human listening would not hear, and the key would then disagree with the code for a reason that is not the call's fault.
- For deliberate silences and holds, compute the gap with the **app formula in 7.1** (not by eye from `end_time`), and make sure normal turn-to-turn gaps by that formula stay at **30 s or below**.

### 6.2 Sentiment scores (required on every turn)

Scale: roughly −100 (furious) to +100 (delighted). In practice use these ranges, as a speech-emotion tool would produce:

| Speaker | Typical range | Behaviour |
|---|---|---|
| Customer, calm or neutral | −10 to +10 | small moves |
| Customer, annoyed or worried | −15 to −35 | goes down when the problem is described, or when the agent ignores, dismisses or repeats questions |
| Customer, very upset | −35 to −60 | dips further when the agent is rude |
| Customer, relieved or happy | +5 to +25 | rises as the issue is fixed |
| Agent, warm and professional | +5 to +22 | fairly steady |
| Agent, flat or cold | −5 to +5 | |
| Agent, rude | −20 to 0 | |

Rules:
- The score must **follow the story**. An upset customer should open negative and rise if the agent helps, or stay low or drop if the agent is cold. It should not be random noise or constant.
- Scores reflect **tone as well as words**. Some customers are polite on the surface but score negative (suppressed worry). Some are blunt but score near zero. Include a few of each.
- Do not make sentiment a giveaway for the QA outcome. Some good-agent calls have upset customers throughout, and some bad-agent calls have calm customers.

---

## 7. The 11 criteria and how to grade them

Each criterion is PASS or FAIL. A failed item loses its deduction from its category (starting at 100, minimum 0). Weights and deductions:

| Category (weight) | Criterion | Deduction if FAIL | Decided by |
|---|---|---|---|
| Soft Skills (0.333) | Branding and Survey Check | 15 | rule |
| Soft Skills | Hold time and Dead Air | 15 | rule |
| Soft Skills | Personalized the call/ticket appropriately | 15 | rule |
| Soft Skills | Empathy & Acknowledgment Statement | 35 | judgement |
| Soft Skills | Build rapport and observed professionalism | 20 | judgement |
| Technical Knowledge (0.667) | Verified customer | 25 | rule |
| Technical Knowledge | Paraphrasing | 15 | judgement |
| Technical Knowledge | Active listening | 10 | judgement |
| Technical Knowledge | Took ownership of the problem | 25 | judgement |
| Technical Knowledge | Probing | 25 | judgement |
| Technical Knowledge | Confirmed the issue is resolved | 15 | judgement |

### 7.1 Rule-based items (must match the code exactly)

- **Branding.** Look only at the Agent's lines. PASS needs the exact words **"thank you for calling S-Net"** (any capitalisation) inside the Agent's **first 4 lines** AND **"thank you for choosing S-Net"** inside the Agent's **last 4 lines**. Paraphrases such as "thanks for calling S-Net" or "thank you for contacting S-Net" FAIL. A closing said early, with 5 or more Agent lines after it, FAILS.
- **Hold time and Dead Air.** The app reads **only `start_time_sec`** and assumes every turn lasts 10 seconds, so for turn *i* the **gap = `start_time_sec[i]` − (`start_time_sec[i-1]` + 10)**. `end_time` is for human readers and is ignored. Count every gap **over 30 seconds**. FAIL if **2 or more** such gaps are not managed holds. A gap is a **managed hold** (not counted) only if it is 120 s or less AND either (a) the Agent's previous line announced it with one of: "place you on a brief/short/quick hold", "put you on hold", "bear with me", "one moment while ...", "give me a moment/minute/second while ...", or (b) the Agent's next line says "thank you for holding / waiting / your patience" or "sorry for the wait". A bare "hold on" or "just a sec" is **not** an announcement. If the customer breaks the silence with "hello?" or "are you still there?", that gap is **not** a managed hold. One unmanaged gap alone is still a PASS.
- **Verified customer.** PASS if any Agent line with `start_time_sec` **240 or less** contains the word **PIN**, **address**, or **security question** (whole word, any case). Asking for date of birth, email, or account number alone does **not** count.
- **Personalized.** PASS if the Agent says the `customer_name` (any case) in at least one Agent line. The customer saying their own name does not count.

### 7.2 Judged items (grade like a human QA expert)

- **Empathy & Acknowledgment.** FAIL only when the customer clearly shows frustration, worry or distress (in words and/or in negative sentiment) and the Agent **never acknowledges the feeling** (an apology, "that sounds stressful", "I understand how worrying that is"). A calm customer means PASS. Acknowledging once is enough.
- **Build rapport and professionalism.** Default PASS. FAIL if you can quote **at least one Agent line** that is rude, condescending, dismissive, sarcastic or unprofessional, even if the rest of the call is excellent. Being merely brisk or neutral is PASS.
- **Paraphrasing.** PASS if the Agent restates the customer's problem or request in their own words and checks it ("So what I'm hearing is ... is that right?") at least once during the call. Repeating the customer's exact words back like an echo, or only saying "okay, got it", is FAIL. Restating a **different** thing (an account number) does not count.
- **Active listening.** FAIL when the Agent asks again for information the customer **already gave clearly** (a question repeated, reworded, or asked minutes later). Re-checking something that may legitimately have changed ("is the light still red after the restart?") is **PASS**. One real re-ask is enough for FAIL.
- **Took ownership.** Default PASS. FAIL if you can quote an Agent line that blames another department or a third party, deflects responsibility, tells the customer to call back or go elsewhere, or refuses to help. Doing other useful things in the call does **not** cancel such a line. Handing a request to another team **while remaining the owner** ("I'll raise this with billing and ring you back") is PASS.
- **Probing.** PASS if the Agent asks diagnostic questions about the customer's actual problem (what happens, when it started, what lights or error messages show, what has been tried). Identity-check questions, greetings, "anything else?" and "is that right?" do not count.
- **Confirmed the issue is resolved.** PASS if the problem is actually fixed during the call **and the customer confirms** it works (or confirms the requested change is done). FAIL if the fix depends on something later (a delivery, an engineer visit, a callback, a request to another team) even if next steps are explained, or if the Agent never gets the customer's confirmation. Admin or billing changes count as resolved once the change is made and the customer confirms.

### 7.3 Auto-fail

Check the **Agent's lines only** (not the customer's) for any of these strings anywhere inside a line: **fuck, shut up, idiot, get lost, stupid, hang up**. If any appears in an Agent line, the call is an **auto-fail**: `is_auto_fail = true`, `final_score = 0.0`, and `auto_fail_reason` names the line. You still rate the 11 items honestly.

**Trap for the other 46 calls:** none of those six strings may appear in any Agent line, not even innocently ("that's not a stupid question", "I'll hang up the old line"). Customers may say them freely.

### 7.4 Final score

```
Soft      = max(0, 100 - sum of deductions of FAILED Soft Skills items)
Technical = max(0, 100 - sum of deductions of FAILED Technical Knowledge items)
final     = round(0.333 * Soft + 0.667 * Technical, 1)      # auto-fail: 0.0
```

Worked checks: Branding + Active listening fail → Soft 85, Tech 90 → 88.3. Dead air + Empathy + Verified + Paraphrasing fail → Soft 50, Tech 60 → 56.7. All five Soft items and four Technical items fail (Paraphrasing, Probing, Ownership, Resolved) → Soft 0, Tech 20 → 13.3.

---

## 8. Response payload / answer key format (`expected/expected_ag_NN.json`)

```json
{
  "call_id": "ag_01",
  "tenant_id": "tenant-abc",
  "status": "completed",
  "result": {
    "final_score": 88.3,
    "is_auto_fail": false,
    "auto_fail_reason": null,
    "scorecard": [
      {"category": "Soft Skills", "name": "Branding and Survey Check", "rating": "PASS", "coaching": ""},
      {"category": "Soft Skills", "name": "Hold time and Dead Air", "rating": "PASS", "coaching": ""},
      {"category": "Technical Knowledge", "name": "Verified customer", "rating": "PASS", "coaching": ""},
      {"category": "Soft Skills", "name": "Personalized the call/ticket appropriately", "rating": "PASS", "coaching": ""},
      {"category": "Soft Skills", "name": "Empathy & Acknowledgment Statement", "rating": "PASS", "coaching": ""},
      {"category": "Technical Knowledge", "name": "Paraphrasing", "rating": "PASS", "coaching": ""},
      {"category": "Technical Knowledge", "name": "Active listening", "rating": "FAIL", "coaching": "Asked for the router model again at 09:41 after the customer gave it at 02:15."},
      {"category": "Technical Knowledge", "name": "Took ownership of the problem", "rating": "PASS", "coaching": ""},
      {"category": "Soft Skills", "name": "Build rapport and observed professionalism", "rating": "PASS", "coaching": ""},
      {"category": "Technical Knowledge", "name": "Probing", "rating": "PASS", "coaching": ""},
      {"category": "Technical Knowledge", "name": "Confirmed the issue is resolved", "rating": "PASS", "coaching": ""}
    ]
  },
  "grader": {
    "graded_by": "Antigravity (<model name and version>)",
    "graded_on": "YYYY-MM-DD",
    "scenario": "one line: what the call is about",
    "tier": "excellent | good | okay | poor | very_poor | auto_fail",
    "duration_sec": 734,
    "notes": "2-4 sentences: why this score, in a QA reviewer's voice.",
    "hard_cases": ["Active listening"],
    "items": [
      {"name": "Active listening", "rating": "FAIL", "confidence": "clear",
       "evidence": "[02:15] Customer: 'It's a Hub 4.' ... [09:41] Agent: 'Which router do you have?'"}
    ]
  }
}
```

Rules:
- Exactly **11 scorecard entries**, in the order and with the exact `name` and `category` shown above.
- `coaching` is `""` for PASS. For FAIL it is **one specific sentence that cites the evidence** (timestamp and what was said), as a QA coach would write it.
- `grader.items` has all 11 items. Each has `rating`, `confidence` (`"clear"` or `"borderline"`), and `evidence` (timestamped quote(s) for every FAIL, and for every PASS listed in `hard_cases`).
- `hard_cases` lists the criteria in that call that are close calls (see 9.2).
- `confidence: "borderline"` is allowed but should be **rare** (see 9.3).
- `final_score` must follow 7.4 exactly. `duration_sec` is the last turn's end time.

---

## 9. What mix of calls to write

### 9.1 Overall spread (50 calls)

| Group | Calls | Description |
|---|---|---|
| Excellent | 8 | every item PASS, score 100 |
| 1-2 faults | 15 | mostly good calls with one or two real misses |
| 3-4 faults | 12 | mixed |
| 5+ faults | 11 | poor calls |
| Auto-fail | 4 | Agent loses their temper (use different trigger words: for example "shut up", "idiot", "stupid", "get lost"). The 11 ratings in these calls vary. |

Minimum **FAIL** counts across all 50 calls (so every item is well tested): Branding 8, Dead air 8, Verified 8, Personalized 8, Empathy 12, Paraphrasing 12, Active listening 12, Ownership 12, Rapport 10, Probing 10, Resolved 12. Each item must also PASS in at least 25 calls.

### 9.2 Hard cases (at least 40% of all FAILs and about 30% of PASSes)

We need to learn where the engines break. Write subtle-but-fair cases, for example:
- **A good, long, warm call with one buried fault**: one rude or dismissive line around minute 14, a single re-asked question 8 minutes after the first answer, one "that's the billing team's problem" in an otherwise helpful call.
- **Near-miss PASSes that look like failures**: a question re-asked because the situation changed; an Agent who mentions another team but keeps ownership; a brisk, short-tempered but not rude agent; a customer who is upset about a minor thing and the agent acknowledges it in one short clause; a hold announced properly and 100 s long; a gap of 28 s by the 7.1 formula; PIN asked at 3:58.
- **Near-miss FAILs that look like passes**: great technical work and zero acknowledgment of a visibly distressed customer; paraphrasing that is only an echo; the Agent says "fixed" but the customer never confirms; resolution depends on an engineer visit; closing script said but followed by 6 more Agent lines; PIN asked at 4:02.
- **Long-call effects**: a fault in the first third, in the middle, and in the last third. A rude line must not always be near the start or end.
- **Customer pushback**: customers who get things wrong, change their story, interrupt, or are hard to understand, while the Agent does well or badly.

Mark these in `hard_cases`.

### 9.3 Keep every key clear-cut

If you can't decide whether something is a PASS or FAIL, **rewrite the dialogue** until a QA expert would agree quickly. Use `"borderline"` for at most 5 items across the whole set. We will drop borderline items from the scoring.

### 9.4 Style traps to avoid (they would fake our results)

- **Quality must not show in style.** Do not make PASS calls longer, more formal, or more polite-sounding than FAIL calls. Many FAIL calls should be long and polite apart from the single fault. Many PASS calls should be curt and plain.
- **Do not use the same trigger words only in failures.** If a rude line uses "obviously", some good calls should also use "obviously" politely ("obviously I'll check that for you"). The same for "ring them", "billing team", "engineer", "I understand".
- **Vary the fault wording.** A rude line may be sarcasm, impatience, condescension, talking over the customer, or a sigh-and-sneer, not always a blunt insult.
- Don't make every upset customer apologised to in the same words. Real agents say "that must be exhausting", "I'd be annoyed too", "sorry about the runaround".

### 9.5 Scenario variety

All calls are for **S-Net** (a telecom and internet provider), so the brand rule works. Spread across:
- Broadband drop-outs, slow speed, no connection, router and wifi problems, mesh and extenders
- TV box, channels, remote, streaming apps
- Mobile: no signal, roaming, SIM swap, lost/stolen phone, port-in/out, data usage
- Landline and voicemail, care alarms
- Billing: double charges, failed direct debit, late fees, refunds, price rises, plan changes
- Moving home, new installs, engineer appointments, contract and cancellation, business accounts, account takeover and security concerns, complaints

Vary: agent personality (warm, brisk, scripted, new, chatty, impatient), customer type (angry, anxious, elderly, hurried, chatty, confused, technical, polite-but-upset), outcome (fixed, escalated, unresolved), and agent/customer names (50 different customers; agents may repeat but not more than twice). About **30% of calls** should contain speech-to-text roughness: fillers ("um", "you know"), false starts, missing punctuation, numbers said as words ("four four one eight"), and occasional homophone slips. Do not make all text clean.

---

## 10. How to work

1. Plan all 50 first: a short table of call number, length, scenario, group (excellent / 1-2 / 3-4 / 5+ / auto-fail), and which items fail. Check it against 9.1 counts. Keep that plan in `SUMMARY.md`.
2. Write in batches of 5 to 10 calls. After each batch, run `selfcheck.py` and fix errors before continuing.
3. Write each call's dialogue **first**, then grade it by re-reading it as a QA expert would. Do not assign the ratings from your plan without checking the text. If the text and plan disagree, the **text wins**; fix the key or the call.
4. Compute the four rule items and the final score with code, not by eye. Judged items are your human-style reading.
5. Don't ask me questions unless you are truly blocked. The decisions are yours.

---

## 11. Self-check and summary (finish with these)

**`selfcheck.py`** (put it in `inputs/AG50/`, standard library only) must verify and print a pass/fail line per check:
- 50 payloads and 50 keys exist, names match, `call_id` correct.
- Every turn has all fields; `speaker` valid; `start_time_sec` equals `start_time`; times in order; no overlaps; `sentiment_score` is a float on every turn; no turn longer than 30 s (`end_time` − `start_time`); no unintended gap over 30 s by the 7.1 formula.
- Last `end_time` is between 10:00 and 20:00 for every call; length distribution is printed.
- The four rule items recomputed from the transcript (7.1) match the key.
- Auto-fail words appear in Agent lines only in the intended auto-fail calls (and are named in `auto_fail_reason`).
- Final score recomputed from the ratings (7.4) matches the key.
- 11 scorecard entries in the right order with the exact names; `coaching` empty for PASS, non-empty for FAIL.
- Coverage: FAIL and PASS counts per item against 9.1; number of hard cases; number of borderline items (≤ 5).

**`SUMMARY.md`**: one row per call: id, duration, scenario, group, failed items, final score, hard-case flags. Under it, the coverage table.

Then tell me: the output of `selfcheck.py`, and anything you were unsure about.

---

## 12. What happens next (for context)

We run Ollama, stock Laya and fine-tuned Laya on your 50 calls, compare each engine's 550 item ratings and 50 final scores with your keys, and take every item where the engines and your key disagree to a human reviewer. A "disagreement" will tell us whether the engine is wrong or the key is. This decides whether the fine-tuned model can replace Ollama in production, so **an honest, clear key is worth more than a flattering one**.
