# Antigravity V2: rules shared by the training set (AG-T) and the sealed test set (AG-B)

You already wrote 50 calls for us (`inputs/AG50/`) from `Docs/ANTIGRAVITY_TEST_BRIEF.md`. We are now asking for two new sets. This file says **what is the same, what changes, and exactly how to label the calls**. Your task file says how many calls and what mix. (This file was written for the sets AG-T and AG-B; the task files of every set delivered so far, AG-T, AG-B, AG-B2 and AG-C, were removed from the repo on 2026-10-22 once the sets were sealed. They are in git history at commit `8a6842b` and make good templates for a new one.) Read in this order:

1. `Docs/ANTIGRAVITY_TEST_BRIEF.md`: the rulebook. Everything in it still applies **unless this file overrides it**.
2. This file.
3. `Docs/ANTIGRAVITY_V2_EXAMPLES.md`: worked examples of every label. Read it before writing.
4. Your task file.

---

## 1. What is the same as the rulebook

- Payload shape, field rules, timing and length: rulebook sections 6 and 6.1 (10 to 20 minute calls, 30 s per turn at most, the dead-air formula). **One change: sentiment, see section 2 below.**
- **Never pad a call to reach a length.** No stock clauses appended to lines, no repeated or copy-pasted turns, no generator that inflates the dialogue. If a call is too short, write more real support work. The validator rejects padding.
- The 11 criteria, deductions and final-score formula: rulebook section 7. **Changes: Empathy is stricter, and four judged criteria are sharpened, see section 3.**
- The key format: rulebook section 8 (scorecard, coaching, `grader.items` with evidence). **One addition: `grader.markers`, see section 4.**
- Scenario variety, speech-to-text roughness, style traps: rulebook sections 9.4 and 9.5. All S-Net calls, 30% with roughness, quality must not show in style.
- Working method: rulebook section 10. Write the dialogue first, then grade it by re-reading, **the text wins over your plan**.

## 2. Change 1: sentiment (customer only, noisy)

In production only the **customer's** speech is scored, by a text-emotion classifier that reads one line at a time. So:

- **Agent turns carry no `sentiment_score` at all.** Leave the field out. (A 0.0 is tolerated; any other number is an error.)
- **Customer turns carry a float `sentiment_score` on every turn**, between -100 and 100, one decimal. Score each customer line **from its own words and tone only**, as if a classifier saw that single line with no memory of the call.

| Customer line | Typical score |
|---|---|
| Neutral or factual ("It's a Hub 4.", "Ten minutes ago.") | -6 to +6 |
| Short backchannel ("okay", "right", "mm-hm", "yes") | about 0, never beyond +/-12 |
| Mild complaint or worry | -10 to -25 |
| Clearly angry, distressed or fed up | -25 to -60 |
| Relieved, thankful | +10 to +40 |

Make it **noisy and imperfect**, like the real classifier:
- Add independent jitter of 3 to 8 points to every turn. Two neutral turns in a row should not have the same score. Do not make the scores follow a smooth story arc.
- In about 1 turn in 10 let the classifier be wrong: sarcasm scored positive ("oh brilliant, thanks a lot" +14), a polite-but-upset line scored near zero ("I'd really appreciate someone looking at this, it's been three days" -4), a blunt calm line scored mildly negative.
- Calls where an upset customer scores calm, and calm customers who score negative, are wanted.

`Scripts/validate_calls.py` prints a WARN when the scores are too smooth or when a one-to-three word turn scores far from zero.

## 3. Change 2: grading definitions (these replace the matching paragraphs in rulebook 7.2)

Grade like a careful human QA expert. Use only the definitions below; do not invent extra rules.

**Empathy & Acknowledgment (STRICT, per outburst; replaces the old "acknowledging once is enough").**
- An **outburst** is a customer line that clearly shows frustration, anger, worry or distress. If the customer stays upset over several consecutive lines, that is **one** outburst; count it at the first upset line. A new outburst starts only after the customer has been calm for at least four customer turns.
- An outburst is **handled** when an Agent line **within the next 4 turns** (counting every turn, both speakers) recognises the feeling or the situation: an apology, "that sounds stressful", "I'd be annoyed too", "three days without service is awful". It is still handled when the agent then says no ("I understand why that's upsetting, but I can't waive the fee"). A bare procedural answer is not recognition.
- An outburst is **unhandled** when the next 4 turns contain no recognition: the agent goes straight to procedure, explains policy, argues, or dismisses. An acknowledgement that only arrives **5 or more turns later is too late** and counts as unhandled for that outburst.
- **Empathy is PASS only if every outburst in the call is handled.** One unhandled outburst makes it FAIL, even if the agent was kind elsewhere. A call with no outburst is PASS.

**Active listening.** FAIL only when the agent **asks again for something the customer already told them clearly** (reworded, or minutes later). PASS cases that look like repeats and must stay PASS: checking something that may have changed ("is the light still red after the restart?"); asking for a different detail of the same topic; asking the customer to complete something they gave only partly or unclearly; confirming what the customer said before an irreversible action ("just to confirm, you want to keep your recordings?"). Asking to confirm is not asking again.

**Paraphrasing.** PASS if, at any point in the call, the agent restates **the customer's problem or request** in their own words (not word for word) and checks it. FAIL if the agent only echoes the customer's exact words, only says "okay, got it", only confirms account details (address, plan, name), or only summarises next steps.

**Build rapport and professionalism.** FAIL if you can quote at least one Agent line that is rude, condescending, dismissive, sarcastic or blaming, **even without insults** ("That's basic stuff, it's not difficult."). Brisk, blunt, short-tempered but respectful lines are PASS. The same words ("obviously", "as I said", "actually") appear in both rude and acceptable lines; judge the tone, not the word.

(Ownership, Probing, Resolved and the four rule-based items: unchanged from the rulebook.)

## 4. Change 3: markers (`grader.markers` in every key)

Next to `grader.items`, add `grader.markers`. It points at the exact turns behind your ratings, so a tool can find them. **Turn index = the 0-based position of the turn in the `transcript` array** (the first turn is 0). All four keys must be present; use `[]` when there is nothing to mark.

```json
"markers": {
  "active_listening": [
    {"kind": "repeat",           "premise_turn": 12, "agent_turn": 88, "reworded": true},
    {"kind": "harmless_recheck", "premise_turn": 30, "agent_turn": 52}
  ],
  "paraphrasing": [
    {"kind": "restatement",       "agent_turn": 9},
    {"kind": "not_a_restatement", "agent_turn": 5}
  ],
  "rapport": [
    {"kind": "rude",         "agent_turn": 71},
    {"kind": "blunt_but_ok", "agent_turn": 40}
  ],
  "empathy": [
    {"kind": "handled",   "customer_turn": 22, "agent_turn": 24, "with_refusal": false},
    {"kind": "unhandled", "customer_turn": 60}
  ]
}
```

| Check | Marker kinds | Meaning | Must agree with the rating |
|---|---|---|---|
| Active listening | `repeat` | `premise_turn` (a **Customer** turn that gave the information) and `agent_turn` (the **Agent** turn that asks for it again, later). Optional `"reworded": true` if the question uses different words | FAIL if there is at least one `repeat`, PASS if none |
| | `harmless_recheck` | same two fields; an agent question that **looks** like a repeat but is legitimate (see section 3) | no effect |
| Paraphrasing | `restatement` | the Agent turn that restates the problem | PASS if at least one, FAIL if none |
| | `not_a_restatement` | an Agent turn that echoes the customer's words, confirms account details or summarises next steps | no effect |
| Rapport | `rude` | the Agent turn you would quote as the fault | FAIL if at least one, PASS if none |
| | `blunt_but_ok` | an Agent turn that is brisk, blunt or uses a trigger word ("obviously", "as I said") but is acceptable | no effect |
| Empathy | `handled` | `customer_turn` (the outburst) and `agent_turn` 1 to 4 turns later that recognises it. Optional `"with_refusal": true` if the agent then says no | no effect |
| | `unhandled` | `customer_turn` of an outburst with no recognition in the next 4 turns | FAIL if at least one, PASS if none |
| | `no_outburst` (optional) | `customer_turn` of a line that **looks upset to a text classifier** (negative score, a complaint or worry word) but is **not** an outburst: relief ("I was so worried, thank goodness"), a factual status report, mild annoyance that needs no acknowledgement. Use it for such lines in any call | no effect |

Mark **every** event of these kinds you wrote on purpose, in good calls too. A call with no `harmless_recheck`, `not_a_restatement`, `blunt_but_ok` or `handled` markers teaches nothing about the hard cases.

Add the markers **last**, after the dialogue is final, ideally with a small script that finds each turn by its text. If you insert or delete a turn later, every index after it shifts: re-run the validator.

## 5. The validator (use it; it is your safety net)

```
python Scripts/validate_calls.py --suite agt                       # all 100 AG-T calls
python Scripts/validate_calls.py --suite agt --subset agt_001,agt_002   # a batch while you are writing
python Scripts/validate_calls.py --suite agb                       # all 50 AG-B calls
```

Run it from the repo root after every batch. It checks, with the **application's own rule code** for the four rule items: file names and ids, turn fields and timing, 10 to 20 minute length, no agent sentiment, customer sentiment, the four rule items, auto-fail words (Agent lines only), the final score, 11 ordered scorecard entries, and that the markers agree with your ratings. On a full run it also checks the coverage targets in your task file. It prints counts and error messages, **never dialogue**. Fix every error; WARN lines are advice.

## 6. What you may and may not read

You can see the whole repo. Please **do not use all of it**. We want natural calls, graded by human instinct, and an independent test.

| May read | Reason |
|---|---|
| The four docs listed at the top of this file | the task |
| `src/services/rule_engine.py`: `evaluate_branding`, `evaluate_hold_and_dead_air`, `evaluate_verified_customer`, `evaluate_personalized_call` | the four rule items must match the code |
| `resources/criteria_config.json` | the criteria wording |
| `Scripts/validate_calls.py` (to run it, and to read an error you do not understand) | the safety net |
| At most 3 calls and their keys from `inputs/AG50/` | file format only. Do not reuse their scenarios, names, wording or structure |

| Must NOT open | Reason |
|---|---|
| `laya-finetuning/`, `src/services/laya_*.py`, `src/services/dynamic_evaluator.py`, everything in `Scripts/` except `validate_calls.py`, `CLAUDE.md`, `README.md`, `Docs/AI_HANDOVER.md`, `Docs/ARCHITECTURE.md` | model code, training data and notes about where the model is weak. Writing calls to fit how snippets are cut would fake the result |
| `inputs/Eval50/`, `inputs/Main tests/`, `inputs/Bulk tests/`, `inputs/Tough checks/`, `inputs/Test (results)/`, `Docs/LAYA_*`, `Docs/FLOW_*`, `Docs/AG50_*`, `Docs/EVAL50_*` | earlier calls, keys and results |
| Every call set other than the one you are writing: `inputs/AG-T/`, `inputs/AG-B/`, `inputs/AG-B2/`, and any folder whose name starts with an underscore | the sets must not know about each other |

Do not write a call to be easy or hard for any engine; you will never see their results.

## 7. Done means

`python Scripts/validate_calls.py --suite <agt|agb>` on the full set prints **PASS on every line** and exits with code 0.

**Never choose a label to meet a count.** The counts in the briefs guide what you write; they never decide how you grade. If an honest label makes a count fail, keep the label and tell us. A label bent to fit a quota teaches the model the wrong lesson. Then send us the validator output and a short list of anything you were unsure about (borderline gradings, scenarios you were not happy with). An honest, clear key is worth more than a flattering one.
