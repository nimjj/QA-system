# Task: AG-B2, 12 extra sealed test calls that fill the gaps of the first test set

Read first, in this order: `Docs/ANTIGRAVITY_TEST_BRIEF.md` (rulebook), `Docs/ANTIGRAVITY_V2_COMMON.md` (what changes and how to label), `Docs/ANTIGRAVITY_V2_EXAMPLES.md` (worked examples). This file only adds the job and the mix.

**Use a fresh session.** This set is part of the final exam. It must be written without knowledge of any other call set in this repo.

---

## 1. The job

Write **12 realistic S-Net support calls, 10 to 20 minutes each**, with the answer key a careful QA expert would write, **including `grader.markers`** (COMMON section 4). They join an existing 50-call test set that has three gaps:
- no **long excellent** calls (every excellent call there is short),
- no **short poor** calls (every poor call there is long),
- almost no calls where the customer gets upset **more than once**, so the strict Empathy rule (every outburst must be handled) is barely tested.

Your 12 calls fill exactly those gaps. Grade them honestly; do not write to favour or trip up any grading system.

## 2. Files

```
inputs/AG-B2/
  agb2_01.json ... agb2_12.json                         request payloads
  expected/expected_agb2_01.json ... expected_agb2_12.json   keys, with grader.markers
  SUMMARY.md                                             plan first, then one row per call
```

`call_id` inside a key is `agb2_NN`. Create the folders.

## 3. The mix (the validator checks it)

| Calls | What | Rules |
|---|---|---|
| 4 | **Long excellent** | 15 to 20 minutes, **every item PASS**, score 100. Make them genuinely hard to grade: at least one upset moment each that the agent handles (in two of them, handled late: 3 or 4 turns after), harmless re-checks, blunt-but-acceptable lines, account-detail confirmations. |
| 3 | **Short poor** | 10 to 12 minutes, **5 or more failed items**, not auto-fail. Short does not mean sloppy writing: the faults are the agent's, the dialogue is realistic. |
| 5 | **Several upset moments** | 12 to 20 minutes, **2 or 3 distinct outbursts** each (COMMON section 3: distinct = after the customer was calm for 4+ customer turns). In at least 3 of them the first outburst is handled and a **later** one is not; in 1 the first is missed and a later one handled. Over the five, at least 3 outbursts sit in the **last third** of the call. Other faults vary. |

Spread the other faults naturally over all 11 criteria. Vary scenarios, agent personalities and customer types as in rulebook 9.5. 12 different customer first names. About 4 of the 12 calls with speech-to-text roughness.

## 4. Never pad

Length must come from real support work. **No** stock clauses appended to lines, **no** repeated or copy-pasted turns, **no** generator that inflates dialogue to reach a word count. The validator rejects all three. Each call needs about 1,200 to 2,800 words of real dialogue.

## 5. How to work

1. Write the plan in `SUMMARY.md` (call number, length, group, failed items, where each outburst sits) and check it against section 3.
2. One call at a time: dialogue first, then grade it by re-reading as a QA expert, then the markers last. The text wins over the plan.
3. After every 3 or 4 calls run `python Scripts/validate_calls.py --suite agb2 --subset agb2_01,agb2_02,...` and fix every error.
4. Obey COMMON section 6. In particular never open `inputs/AG-B/`, `inputs/AG-T/`, or any folder whose name starts with an underscore.

## 6. When you are done

- `python Scripts/validate_calls.py --suite agb2` prints PASS on every line and exits with code 0.
- **Seal it**: do not edit the calls or keys again, and show them to no one but us. If you find an error later, tell us instead of fixing it.
- Send us the validator output and a short list of anything you were unsure about.
