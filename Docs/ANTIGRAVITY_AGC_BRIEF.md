# Task: AG-C, 50 sealed test calls

Read first, in this order: `Docs/ANTIGRAVITY_TEST_BRIEF.md` (rulebook), `Docs/ANTIGRAVITY_V2_COMMON.md` (what changes and how to label), `Docs/ANTIGRAVITY_V2_EXAMPLES.md` (worked examples). This file only adds the job and the mix.

**Use a fresh session.** This set is the final exam. It must be written without knowledge of any other call set in this repo.

---

## 1. The job

Write **50 realistic S-Net support calls, 10 to 20 minutes each**, with the answer key a careful QA expert would write, **including `grader.markers`** (COMMON section 4). We will run several grading systems on them once and compare each with your keys. Grade honestly; do not write to favour or trip up any system.

## 2. Files

```
inputs/AG-C/
  agc_01.json ... agc_50.json                        request payloads
  expected/expected_agc_01.json ... expected_agc_50.json   keys, with grader.markers
  SUMMARY.md                                          plan first, then one row per call
```

`call_id` inside a key is `agc_NN`. Create the folders.

## 3. The mix (the validator checks all of it)

| Group | Calls |
|---|---|
| Excellent (all PASS, score 100) | 8 |
| 1 to 2 faults | 15 |
| 3 to 4 faults | 12 |
| 5 or more faults | 11 |
| Auto-fail (agent loses their temper; vary the words) | 4 |

Minimum FAIL counts: Branding 8, Dead air 8, Verified 8, Personalized 8, Empathy 12, Paraphrasing 12, Active listening 12, Ownership 12, Rapport 10, Probing 10, Resolved 12. Every item also PASSes in at least 25 calls. At least 40% of FAILs and about 30% of PASSes are hard cases (rulebook 9.2), at most 5 borderline items, 50 different customer first names.

**Quality must not show in length.** Spread lengths over the whole range (about 10 calls of 10-12 min, 15 of 12-15, 15 of 15-18, 10 of 18-20) **independently of quality**: at least 3 excellent calls of 15+ minutes and at least 3 poor calls (5+ faults, not auto-fail) of 10-12 minutes. The validator rejects the set if call length and the number of failed items correlate beyond +/-0.3.

**Upset moments.** At least 8 calls with two or more distinct outbursts (COMMON section 3), at least 4 of them where the first is handled and a later one is not, and at least 5 outbursts in the last third of a call.

**Upset-looking but fine.** Real customers often sound negative without needing an apology: relief ("thank goodness, I was so worried"), a flat factual report ("it's still red"), mild impatience that the agent simply resolves. Put such lines in good and bad calls alike, and mark each with an `empathy` marker of kind `no_outburst` (COMMON section 4). At least 15 over the set.

Use every other hard case of rulebook 9.2 and COMMON section 3 as well: harmless re-checks next to real re-asks, echoes and account confirmations next to real restatements, blunt-but-acceptable lines next to rude ones, deflections worded in many different ways, resolution confirmed early followed by small talk, confirmation never given.

## 4. Never pad

Length must come from real support work: no stock clauses appended to lines, no repeated or copy-pasted turns, no generator that inflates dialogue. The validator rejects padding. About 1,200 to 2,800 words of real dialogue per call.

## 5. How to work

1. Write the plan in `SUMMARY.md` (call number, length, group, failed items, outbursts) and check it against section 3, including the length/quality spread.
2. Batches of 5 to 10 calls. Dialogue first, then grade it by re-reading as a QA expert, then the markers last. The text wins over the plan.
3. After each batch: `python Scripts/validate_calls.py --suite agc --subset agc_01,...` and fix every error.
4. Obey COMMON section 6. Never open `inputs/AG-T/`, `inputs/AG-B/`, `inputs/AG-B2/`, or any folder whose name starts with an underscore.

## 6. When you are done

- `python Scripts/validate_calls.py --suite agc` prints PASS on every line and exits with code 0.
- **Seal it**: no more edits to calls or keys, and show them to no one but us. If you find an error later, tell us instead of fixing it.
- Send us the validator output and a short list of anything you were unsure about.
