# Laya vs Ollama test log: Main tests, 2026-10-12

## What was run
- **Calls:** the 4 hand-graded calls in `inputs/Main tests/`. The expected scorecards are in `expected/` (graded by Claude, not yet human-reviewed).
- **Ollama:** `origin/version-10` (llama3.1 + nomic-embed-text), run from a local worktree.
- **Laya:** `version-10-laya` (English checkpoint, CPU).
- **Same setup for both:**
  - The 11 criteria from `resources/criteria_config.json`, sent inline, with no database.
  - The profanity auto-fail checks agent lines only.
  - The service ran on the PC (no Docker), one engine at a time.
- **Results:** `inputs/Test (results)/Main tests (ollama|laya)/`.

## Scores

| Call | Expected | Ollama | Laya |
|---|---|---|---|
| 1 Excellent (22 min) | 100.0 | 100.0 | 61.7 |
| 2 Good (17 min) | 88.3 | 83.3 | 68.3 |
| 3 Okay (22 min) | 56.7 | 78.3 | 56.7* |
| 4 Bad (16 min) | 13.3 | 23.3 | 20.0 |
| Items matching expected | | 40/44 (91%) | 34/44 (77%) |
| Mean score error | | 9.2 | 16.3 |
| Time per call | | ~6.4 min | ~8.5 s |

\* Call 3 is correct by coincidence: a wrong Paraphrasing PASS and a wrong Resolved FAIL cancel out.

Ollama keeps the calls in the right order. Laya ranks the Excellent call below the Good one.

## Item results (✗ = disagrees with expected)

| Item | Ollama | Laya |
|---|---|---|
| Branding, Verified customer, Personalized | 12/12 | 12/12 |
| Took ownership | 4/4 | 4/4 |
| Hold time and Dead Air | 3/4 (✗ call 2) | 3/4 (✗ call 2) |
| Empathy | 3/4 (✗ call 3) | 2/4 (✗ calls 1, 2) |
| Paraphrasing | 2/4 (✗ calls 3, 4) | 3/4 (✗ call 3) |
| Active listening | 4/4 | 3/4 (✗ call 2) |
| Build rapport | 4/4 | 3/4 (✗ call 4) |
| Probing | 4/4 | 3/4 (✗ call 1) |
| Confirmed resolved | 4/4 | 1/4 (✗ calls 1, 2, 3) |

## Laya's raw scores
These come from a re-run that recorded Laya's output. The scores matched the service run exactly.

"Pass score" is P(yes) for checks where yes means PASS (Empathy, Paraphrasing, Probing, Resolved). For Rapport and Ownership, where yes means FAIL, it is 1 − P(yes).

| Check | Cutoff | Should PASS | Should FAIL | Can a cutoff separate them? |
|---|---|---|---|---|
| Confirmed resolved | 0.80 | 0.725, 0.737, 0.741 | 0.677 | Yes at ~0.70, but the margin is only 0.05 |
| Empathy | 0.78 | 0.780, 0.725, 0.656 | 0.567, 0.639 | Barely (0.656 vs 0.639) |
| Paraphrasing | 0.50 | 0.527, 0.646 | **0.658**, 0.499 | **No.** The call with no paraphrase scores highest. |
| Build rapport | 0.81 | (no lines flagged) | **0.851** (P(rude) = 0.149) | **No.** Clearly condescending lines are rated polite. |
| Probing | 0.60 | **0.582**, 0.696, 0.826 | 0.506 | Yes, once the input is fixed (see below) |
| Took ownership | 0.52 | 0.814 | 0.286 | Yes, with a wide margin |
| Active listening | 0.19 | no Laya call | no Laya call | Not tested: the pre-filter sent nothing |

## Where to focus Laya training

### 1. Build rapport and observed professionalism: high priority
- **The miss:** in call 4, Laya rated these agent lines as polite, with P(rude) = 0.15:
  - "You should have restarted the router before you called, that's the first thing anyone should do."
  - "That's basic stuff."
  - "It's not difficult."
  - "Obviously if you want the full 500…"
- **Why training, not a cutoff:** Laya treats condescension as polite when there is no insult or swear word.
- **Training data:**
  - Rude: condescending, blaming, belittling and dismissive lines, labelled rude even without insults.
  - Not rude: ordinary professional lines that contain the same trigger words ("obviously", "as I said"), so the model learns the tone rather than the words.

### 2. Paraphrasing: high priority
- **The miss:** call 1 has a textbook paraphrase ("Let me make sure I've got the full picture… Is that right?") but scored only 0.53. Call 3 never restates the problem, only asks follow-ups that reuse the customer's words ("Which light is blinking orange?"), yet scored 0.66.
- **Why training:** no cutoff works. Laya can't tell restating the problem from asking about it. Ollama's embedding method also failed here (it passed every call).
- **Training data:**
  - Paraphrase: the customer's opening plus an agent summary that restates it.
  - Not a paraphrase: the same opening plus agent questions that echo the customer's words without restating.
- **Input fix first:** drop the verification and greeting lines from the agent text. In calls 1 and 2 they take up most of the 150-word agent budget.

### 3. Confirmed the issue is resolved: high priority (largest score impact)
- **The miss:** this fails every good call, which costs about 10 final-score points per call. Calls 1 and 2 end with an explicit "Would you say the issue is resolved?" / "Yes, completely", yet score only 0.72–0.74.
- **Short-term fix:** lower the cutoff from 0.80 to ~0.70. That fixes this set.
- **Why training too:** the margin to the bad call (0.68) is only 0.05, which is too thin to trust.
- **Training data:**
  - Resolved: endings where the agent explicitly checks and the customer confirms.
  - Not resolved: endings that stop without a check, where the customer says it still fails, or where the call is handed off. Include long endings with small talk and surveys mixed in.

### 4. Empathy and acknowledgment: medium priority
- **What Laya does:**
  - Good replies score 0.73–0.78. Example: "Freezing in the middle of a pitch to a new client is about the worst timing there is."
  - Cold replies score 0.57–0.64. Example: "They can help with that." in reply to a customer threatening to cancel.
- **Why it's medium:** the order is right, but the gap is too small for one cutoff.
- **Input fix first:** call 2's only snippet was a calm problem description, picked because of a sentiment drop, with no emotion to acknowledge. The real frustrated moment was skipped because the agent said "understand"/"frustrating".
- **Training data:** pairs of a frustrated customer turn with a warm reply, and the same turn with a cold, purely procedural or dismissive reply.

### Working: no training needed now
- **Took ownership:** good separation (0.81 vs 0.29). Keep it as a regression check.
- **Probing:** Laya's verdicts are right (0.70 and 0.83 for real diagnostic questions, 0.51 for "What's the issue?" only). Call 1 failed because of the input, not the model: see the next section.

## Pipeline fixes (not Laya training)
These caused wrong grades without Laya being involved, or before it was. Fix them first; otherwise training data will contain the same errors.

| Item | Problem | Fix |
|---|---|---|
| Probing | The 100-word budget is used up by boilerplate before the real questions are reached. In call 1 Laya saw only "Who do I have the pleasure of speaking with…", "confirm the service address…", "what's going on with the service today?" and "Do you mind if I ask a few questions first?". Whole turns are sent, including the statements before the question. | Extend the boilerplate filter to cover these phrasings, and send only the question sentence of each turn. |
| Active listening | Laya was never asked. In call 2 the agent re-asked two answered questions, with difflib similarity 0.23 and 0.64, both under the 0.70 cutoff. The Ollama version caught them with embeddings. | Detect "question already answered" instead of near-identical wording (embeddings, or lower the cutoff to ~0.55 and let Laya decide), then train if Laya then misjudges. |
| Hold time and Dead Air | The rule counts an announced hold with check-ins as 2 dead-air gaps. Both engines fail call 2. | Skip gaps that follow a hold announcement ("place you on a brief hold", "bear with me") or end in a check-in or a thank-you for waiting. |
| Empathy | The sentiment pre-filter picks problem descriptions, and the keyword skip hides real frustrated moments. | Trigger on customer emotion words as well as sentiment drops. Check the agent's reply rather than skipping on keywords. |

## Caveats
- **Sample size:** 4 calls is a small sample, and most checks got one Laya call per call. Treat this as a direction, not a measurement.
- **Labels:** the calls and expected grades were written by Claude. A human should spot-check them before any training data is built from them.
- **Training data needed:** a few hundred balanced, human-labelled examples per category above, taken from real calls. This should run on a GPU.
- **Order of work:** apply the pipeline fixes and the Resolved cutoff change first, re-run `python Scripts/batch_test.py main --label laya` and `bulk`, and only then start training.

---

# Round 2: pipeline fixes (2026-10-12)

## What changed
All changes are in `src/services/rule_engine.py` and `dynamic_evaluator.py`, uncommitted.

| Item | Change |
|---|---|
| Hold time and Dead Air | A gap after an announced hold, or one the agent ends with "thanks for holding/waiting", isn't dead air (up to 120 s). |
| Empathy | Bug fix: the sentiment drop is measured against the customer's own earlier turns. It used to include agent turns, so call 1 had 33 candidates and now has 7. Frustration words ("nightmare", "third time" …) also trigger. The apology-keyword skip is kept. |
| Active listening | Question sentences are compared instead of whole turns. A customer "like I said / I mentioned" reply pairs the question with the earlier one and is sent along. |
| Probing | Only question sentences are sent; the opener and check-in phrasings were added to the boilerplate list. The customer-problem text skips account-detail answers. |
| Paraphrasing | Greeting and verification lines and account-detail answers are removed from the input. |
| Confirmed resolved | Cutoff 0.80 → 0.73. |

### How the Resolved cutoff was chosen
It was picked on the 35 `b_*` bulk calls, whose filenames name the missing confirmation, so it isn't tuned to the Main calls. Laya barely separates them: no-confirmation endings score 0.66–0.75 and confirmed ones 0.47–0.79. No cutoff is good:

| Cutoff | b_* confirmed passed | b_* missing confirmation failed | b_* balanced | Main good passed | Main bad failed |
|---|---|---|---|---|---|
| 0.68 | 30/31 | 1/4 | 0.61 | 3/3 | 1/1 |
| 0.70 | 21/31 | 1/4 | 0.46 | 3/3 | 1/1 |
| **0.73** | 19/31 | 3/4 | **0.68** | 2/3 | 1/1 |
| 0.75 | 19/31 | 3/4 | 0.68 | 0/3 | 1/1 |
| 0.80 (old) | 0/31 | 4/4 | 0.50 | 0/3 | 1/1 |

## Results
Result folders: `Main tests (laya-v2)` and `Bulk tests (laya-v2)`. The bulk "before" run is `Bulk tests (laya)`. Run `python Scripts/compare_results.py ollama laya laya-v2` for the full tables. The raw Laya probabilities are in `inputs/Test (results)/Laya probes/` (`probe_laya.json` before, `probe_laya-v2.json` after); rebuild them with `python Scripts/probe_laya.py <out.json>` and the cutoff tables with `python Scripts/laya_cutoffs.py <probe.json>`.

| | Ollama | Laya before | Laya v2 |
|---|---|---|---|
| Main scores (expected 100 / 88.3 / 56.7 / 13.3) | 100 / 83.3 / 78.3 / 23.3 | 61.7 / 68.3 / 56.7 / 20.0 | 78.3 / 83.4 / 60.0 / 30.0 |
| Main items matching | 40/44 | 34/44 | 36/44 |
| Main mean score error | 9.2 | 16.3 | 11.7 |
| Bulk b_* items matching | – | 332/372 (89%) | 348/372 (94%) |

Laya v2 still ranks the Excellent call (78.3) below the Good one (83.4).

### Per item (Main tests | b_* calls)

| Item | Before | v2 | Verdict |
|---|---|---|---|
| Hold time and Dead Air | 3/4 · 34/34 | **4/4** · 34/34 | Keep. Fixed call 2 with no bulk regressions. |
| Probing | 3/4 · 30/34 | **4/4** · 30/34 | Keep. Fixed call 1. The 4 bulk misses are "no probing" calls scoring 0.57–0.68 against a 0.60 cutoff; real probing scores 0.745 or more. **A cutoff of 0.70 separates all 34 b_* calls and all 4 Main calls** (recommended next change). |
| Confirmed resolved | 1/4 · 4/33 | **3/4** · **22/33** | Keep for now. This is the largest gain, but Laya can't really tell the endings apart (see table above). Still a training priority. |
| Empathy | 2/4 · 34/34 | 2/4 · 34/34 | No change in outcome. The bug fix cut noise, but the 0.78 cutoff still fails calls 1 and 2. Training. |
| Paraphrasing | 3/4 · 27/34 | 2/4 · 28/34 | Inconclusive. On b_* the cleaner input separates better (best balanced accuracy 0.67 → 0.80), but at the 0.50 cutoff it flips real calls both ways and now passes call 4. Training. |
| Active listening | 3/4 · 33/33 | **2/4 · 30/33** | **Regression.** See below. |
| Build rapport | 3/4 · 33/33 | 3/4 · 33/33 | Not changed (training). |

### Why Active listening regressed
- **The attached reply confuses Laya.** Sending the customer's "…I just said, it's red." with the pair drops Laya's repeat score for the planted bulk repeats from 0.89 to 0.51, under the 0.81 needed to fail. Without that line they score 0.895 again.
- **Call 2's real repeats still pass.** Without the reply line they score 0.71 and 0.74, still under 0.81.
- **New false fail on call 3.** Sentence-level comparison now catches call 3's status re-check ("What is the globe light doing now?" / "What's the light doing?"). Laya rates it 0.82, a repeat, so call 3 now fails wrongly.
- **Conclusion:** Laya rates asking for a changing status again as more of a repeat than re-asking for information the customer already gave. A filter can't fix that; it needs training examples of both.

### Real and v8 calls (no item labels)
- **Resolved:** now passes on the high, above-average and perfect calls.
- **Paraphrasing:** flipped both ways, failing two strong calls and passing three weak ones (real_long midlow, low and poor).
- **Probing:** flipped on 3 calls.
- **Effect on real_long scores:** they are less spread out. Before they ran from 90 down to 41.6 in tier order. Now mid, midlow, low and poor all score 51.7. Paraphrasing and Probing account for most of this.

## Updated training focus (most important first)
1. **Active listening:** repeats of information already given vs. re-checking a changing status.
2. **Confirmed resolved:** explicit confirmation vs. an ending without a check.
3. **Paraphrasing:** restating the problem vs. asking about it in the customer's words.
4. **Build rapport:** condescension without insults.
5. **Empathy:** warm vs. cold replies to a frustrated customer.
