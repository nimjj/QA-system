# Task: AG-B, 50 sealed test calls with answer keys and markers

Read first, in this order: `Docs/ANTIGRAVITY_TEST_BRIEF.md` (rulebook), `Docs/ANTIGRAVITY_V2_COMMON.md` (what changes and how to label), `Docs/ANTIGRAVITY_V2_EXAMPLES.md` (worked examples). This file only adds the job and the counts.

**Use a fresh session, separate from the one that wrote AG-T.** This set is the final exam. It must be written without knowledge of the training set.

---

## 1. The job

Do again what you did for AG50, with three differences: no agent sentiment and noisy customer sentiment (COMMON section 2), the stricter Empathy definition and sharpened definitions (COMMON section 3), and `grader.markers` in every key (COMMON section 4). **50 realistic S-Net calls, 10 to 20 minutes each**, with the key a careful QA expert would write.

We will run three grading systems on these calls and compare each with your keys, then have a person check the disagreements. Your keys are the yardstick, so they must be right, clear-cut and honest. Write natural calls: do not write to favour or trip up any system.

## 2. Files

```
inputs/AG-B/
  agb_01.json ... agb_50.json                        request payloads
  expected/expected_agb_01.json ... expected_agb_50.json   keys, with grader.markers
  SUMMARY.md                                          plan first, then one row per call
```

`call_id` inside a key is `agb_NN`. Create the folders if they do not exist.

## 3. The mix: the same as AG50

Use rulebook section 9 as it stands:

| Group | Calls |
|---|---|
| Excellent (all PASS, score 100) | 8 |
| 1 to 2 faults | 15 |
| 3 to 4 faults | 12 |
| 5 or more faults | 11 |
| Auto-fail (agent loses their temper) | 4 |

Minimum FAIL counts: Branding 8, Dead air 8, Verified 8, Personalized 8, Empathy 12, Paraphrasing 12, Active listening 12, Ownership 12, Rapport 10, Probing 10, Resolved 12. Every item also PASSes in at least 25 calls. At least 40% of FAILs and about 30% of PASSes are hard cases (rulebook 9.2), at most 5 borderline items in the whole set. 50 different customer first names. Lengths: about 10 calls of 10-12 min, 15 of 12-15, 15 of 15-18, 10 of 18-20.

Hard cases to include on purpose, over the whole set, in good and bad calls alike:
- Legitimate re-checks, confirmations before an action, and requests to complete partial information, next to real re-asks (some reworded, some many minutes later).
- Echoes and account-detail confirmations next to real restatements.
- Brisk, blunt lines using words like "obviously" or "as I said", next to rude ones, and a rude line buried in a long warm call.
- Calls with more than one upset moment where one is handled and one is not, late acknowledgements (3 or 4 turns after), and acknowledgements that come too late (5 or more turns).
- Calm calls with no upset moment at all.

## 4. How to work

1. Write the plan first in `SUMMARY.md` (call number, length, scenario, group, failed items) and check it against section 3.
2. Batches of 5 to 10 calls. Dialogue first, then grade it by re-reading, then the markers last. The text wins over the plan.
3. After each batch: `python Scripts/validate_calls.py --suite agb --subset agb_01,...` and fix every error.
4. Do not look at `inputs/AG-T/`, and do not read anything listed under "Must NOT open" in COMMON section 6.

## 5. When you are done

- `python Scripts/validate_calls.py --suite agb` on the full set prints PASS on every line and exits with code 0.
- **Seal it.** After the validator passes, do not edit the calls or keys again, and do not show them to anyone but us. If you find an error afterwards, tell us instead of fixing it.
- Send us the validator output and a short list of anything you were unsure about.
