# Task: AG-T, 100 training calls with answer keys and markers

Read first, in this order: `Docs/ANTIGRAVITY_TEST_BRIEF.md` (rulebook), `Docs/ANTIGRAVITY_V2_COMMON.md` (what changes and how to label), `Docs/ANTIGRAVITY_V2_EXAMPLES.md` (worked examples). This file only adds the job, the counts and the craft advice.

---

## 1. The job

Write **100 realistic S-Net support calls, 10 to 20 minutes each**, with the answer key a careful QA expert would write, **including `grader.markers`** (turn-level labels for four criteria). We will **train a small grading model on your calls**, so every label has to be right and every hard case has to be a real hard case. This is not a test set; a separate one (AG-B) is being written elsewhere. Do not write to be easy or hard for any model.

Why your calls and not ours: the model we have was trained on calls written by one other author, and it learned that author's habits instead of the skill. Your own natural style, scenarios and instincts are what we need. Do not imitate any other document's dialogue style.

## 2. Files

```
inputs/AG-T/
  agt_001.json ... agt_100.json                          request payloads (rulebook 6, with the sentiment change in COMMON section 2)
  expected/expected_agt_001.json ... expected_agt_100.json   keys (rulebook 8, plus grader.markers)
  SUMMARY.md                                              plan first, then one row per call (section 7)
```

`call_id` inside a key is `agt_NNN` (three digits). Create the folders if they do not exist.

## 3. The mix (the validator enforces all of this on the full set)

**Call groups** (number of failed items; auto-fail counts only as auto-fail), tolerance +/-3 per group:

| Group | Calls |
|---|---|
| Excellent: every item PASS, score 100 | 20 |
| 1 to 2 faults | 30 |
| 3 to 4 faults | 25 |
| 5 or more faults | 20 |
| Auto-fail (the agent loses their temper; use different trigger words: "shut up", "idiot", "stupid", "get lost"; rate the 11 items honestly) | 5 |

**Minimum FAIL counts over the 100 calls** (each item must also PASS in at least 40 calls):

| Criterion | Min FAIL | | Criterion | Min FAIL |
|---|---|---|---|---|
| Empathy | 30 | | Branding | 10 |
| Paraphrasing | 35 | | Hold time and Dead Air | 10 |
| Active listening | 30 | | Verified customer | 10 |
| Build rapport | 30 | | Personalized | 10 |
| Took ownership | 15 | | Probing | 15 |
| Confirmed resolved | 15 | | Borderline items allowed | 10 in total |

Empathy, Paraphrasing, Active listening and Rapport are the four criteria we are training for, so they get the most labelled events.

**Markers to write over the whole set** (counts of marker entries; the validator checks them):

| Marker | Min | Why |
|---|---|---|
| Active listening `repeat` | 30 | real faults. Of them at least 12 `"reworded": true`, and at least 10 with the repeat 5 or more minutes after the first mention |
| Active listening `harmless_recheck` | 70 | **the most important number in this brief.** Good agents re-check changing things, confirm before acting and ask for the rest of partial information all the time. Put them in good calls and in faulty calls |
| Paraphrasing `restatement` | 60 | real restatements: early, mid-call or late, in different phrasings |
| Paraphrasing `not_a_restatement` | 50 | echoes, account-detail confirmations ("just to confirm your address"), next-step summaries. Spread over PASS and FAIL calls |
| Rapport `rude` | 30 | at least 20 of them inside calls of 12+ minutes, buried in an otherwise warm, helpful call. Vary the style: condescension without insults, sarcasm, impatience, blame, belittling |
| Rapport `blunt_but_ok` | 60 | brisk, firm or short-tempered but acceptable lines, over at least 40 calls. Use the **same** trigger words as in rude lines ("obviously", "as I said", "actually", "it's not complicated") |
| Empathy `handled` | 40 | at least 15 acknowledged **late** (3 or 4 turns after the outburst, after a first procedural answer) and at least 15 with `"with_refusal": true` ("I do understand why that's upsetting, but I can't waive it") |
| Empathy `unhandled` | 35 | the agent goes straight to procedure, explains policy, argues or dismisses, or acknowledges too late (5 or more turns). Include calls with 2 or 3 outbursts where one is missed |

**Spread of the events (the validator warns during batches and enforces it on the full set).** Events must not all sit at the start of the call, and the look-alikes must not all be easy:

| Requirement over the 100 calls | Min |
|---|---|
| Outbursts that start **after the first third** of the call (not only the customer's opening complaint), handled or not | 30 |
| Calls with **two or more outbursts** (for example the first handled warmly, a later one brushed off; or the reverse) | 15 |
| `harmless_recheck` entries whose `agent_turn` is **10 or more turns after** the `premise_turn` | 25 |
| `rude` lines in the **middle third** of the call | 8 |
| Events (outburst, `rude`, `repeat`, `harmless_recheck`) in the **last third** of the call | 25 |

**Vary the position of the events call by call.** Do not give every call the same skeleton (first outburst at turn 5, second at turn 20). The first outburst may come at turn 3 in one call and minute 12 in another. In some calls the only upset moment is near the end.

**Mark every hard-case line you wrote.** Real calls are full of lines that look bad but are fine: an agent confirming an address ("just to confirm your address"), echoing the customer, or saying "obviously" or "as I said" politely. Every such Agent line must carry a marker: `not_a_restatement` for the first two, `blunt_but_ok` for the last. Aim for about **one of each per call**. A call with no such markers is almost always missing them, not free of them. Likewise, mark every outburst you wrote (`handled` or `unhandled`) and every re-check.

**Acknowledgement timing and style are part of the lesson.** Over the set: at least 15 `handled` outbursts where the recognition comes **3 or 4 turns** after the customer's line (after a procedural answer first), at least 15 `handled` with `"with_refusal": true` (recognition, then still no), and a good number of `unhandled` where the recognition arrives **5 or more turns too late**. If every handled outburst is answered in the very next turn, the model learns a shortcut.

A `harmless_recheck` should resemble a real repeat: same topic, similar wording, minutes after the information was given. "Is it still orange after the restart?" asked **right after** the customer says it is fixed is the easiest kind; use it rarely. Prefer: the customer gave the plan at minute 2, and at minute 9 the agent asks "so that's the 150 plan, correct, before I change it?"; the customer gave half an address and the agent asks for the rest; the agent re-checks a reading that was taken before a change.

## 4. How to build the hard cases

- **Twins inside one call.** In many calls put a real fault *and* its harmless look-alike: one genuine re-ask of the router model and, later, one legitimate "is the light still red after the restart?". One rude line and, elsewhere, one blunt-but-fine "obviously I can't see your screen, so read me the number". A model can only learn the difference if both appear, in the same style.
- **Position.** Put events in the first third, the middle and the last third. A fault must not usually be near the start or end.
- **Outbursts.** About half of the calls contain at least one upset customer. Vary the cause and how it is said: loud, polite-but-fed-up, anxious, sarcastic, resigned. Some customers are upset only in one line. Some are upset in the middle of a call that started calm.
- **Calm calls.** Some calls have no outburst at all (`"empathy": []`, PASS).
- **Near-miss PASSes and FAILs.** Rulebook 9.2 still applies: a PASS that looks like a fail and a fail that looks like a pass, at least 40% of FAILs and about 30% of PASSes flagged in `hard_cases`.
- **Customer pushback.** Customers who give wrong details, change their story, interrupt, or answer a question that was not asked, with the agent doing well or badly.

## 5. Style traps (these would ruin the training)

1. **Quality must not show in style.** PASS calls must not be longer, more formal or politer than FAIL calls. Many FAIL calls are long, warm and professional apart from one fault. Many PASS calls are curt and plain.
2. **No trigger-word tells.** Words that appear in faults ("again", "obviously", "as I said", "sorry", "billing team", "I understand") must also appear in clean lines.
3. **No templates.** Every call reads as its own call. Do not rotate nouns in the same skeleton. Different agent personalities (warm, brisk, scripted, new, chatty, impatient), customer types (angry, anxious, elderly, hurried, chatty, confused, technical, polite-but-upset) and outcomes (fixed, escalated, unresolved). 100 different customer first names (agents may repeat, at most twice).
4. **Speech-to-text roughness** in about 30% of calls: fillers, false starts, numbers said as words, occasional homophone slips.
5. **Length comes from real support work** (troubleshooting, account checks, holds, side topics), never filler. **Never pad**: no stock clauses appended to lines, no repeated or copy-pasted turns, no generator that inflates dialogue. The validator rejects all three. For AG-T the minimum is 700 words, so there is no reason to pad.

## 6. How to work

1. Write the **plan first** in `SUMMARY.md`: one row per call with number, length, scenario, group, which items fail, and which markers it will contain. Check the plan against the counts in section 3 before writing any dialogue.
2. Write in **batches of 10**. For each call write the dialogue, then re-read it as a QA expert and grade it, then add the markers last. The text wins over the plan.
3. After each batch run `python Scripts/validate_calls.py --suite agt --subset agt_001,...,agt_010` and fix every error before the next batch.
4. Compute the four rule items and the final score with code, not by eye (the validator will tell you if you are wrong).
5. You may work across several sessions. Keep ids sequential and `SUMMARY.md` up to date so you can resume.
6. Do not ask us questions unless truly blocked. The decisions are yours.

## 7. When you are done

- `python Scripts/validate_calls.py --suite agt` on the full set prints PASS on every line and exits with code 0.
- `SUMMARY.md` has the table (id, duration, scenario, group, failed items, final score, hard-case flags) and under it the coverage tables the validator prints.
- Send us the validator output and a short list of anything you were unsure about.
