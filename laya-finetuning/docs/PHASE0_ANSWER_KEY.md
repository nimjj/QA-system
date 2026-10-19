# Phase 0: the answer key for the 4 Main calls

**Status: NOT human-reviewed.** Every grade was written by Claude. Three contested items were re-read in full by Claude on 2026-10-16, at Nimithra's request ("you decide"), and all three were confirmed. Any result measured against this key must be reported as *"against Claude-written grades, no human review"*.

Machine-readable copy with a provenance per item: `data/review/answer_key_main.json`. Scores stay **100 / 88.3 / 56.7 / 13.3**, the numbers in `qa-analysis/inputs/Main tests/expected/`.

## What happened
| Step | Outcome |
|---|---|
| `Completed review.xlsx` (full 44-item sheet) | Not independent: every note began "Claude:", 43 of 44 verdicts matched Claude's, saved 32 minutes after the sheet was built. Not used. |
| `Completed_2.xlsx` (blind 20-item subset, no answers inside) | Not independent: 9 notes began "Claude (not human):" and quoted Claude's original grading text that was not in the blind file, so the filler had Claude's grades. 17 of 20 matched. Not used as a human verdict. |
| Contested items | The 3 items where Completed_2 differed from Claude were re-read in full by Claude (below). All three originals stand. |

Still unreviewed by any human: all 44 items. The 24 items outside the 20-item subset were never re-checked; the 5 random spot-checks in the subset were answered only by the non-independent file.

## The three contested items
**2-BRAND (Branding and Survey Check) → FAIL.** The call closes "Thanks for calling S-Net, have a great night. Bye." (#85). There is no "Thank you for choosing S-Net" and no survey mention anywhere in the call. The required closing script is not met.

**3-EMP (Empathy & Acknowledgment Statement) → FAIL.** #10 (sentiment -34): "this is the third time I've called this week… It's been four days." Agent: "Can you do it one more time for me?" #31 (-38): "this whole thing has been a nightmare… I've had to go and sit in a coffee shop to do my job." Agent: "Okay. I'm looking at the move order now." Two clear upset moments with no acknowledgement. The agent's only "sorry" (#76) is about being slow to reply.

**4-AL (Active listening) → PASS, with an open definition question.** No question is asked twice and no agent questions look alike. The agent does ignore what the customer said: at #56 it says "You should have restarted the router before you called" after the customer said at #19 he had, and he answers "I did restart it. I told you that." But this app defines the check as repeated or redundant questions (the Laya question is "does the second agent question ask for the same information as the first?"), so the key follows that definition.

## Decision for the business owner
Should Active listening also fail an agent who *ignores or contradicts what the customer already said*, not only one who re-asks a question? If yes, 4-AL becomes FAIL (Call 4 score 13.3 → 6.7) and the check's training data needs a second kind of FAIL example. It is a requirements question, not a model question.

## What this means for later phases
- Measured against this key, Ollama's mean score error stays **9.2** and Laya-v2's **11.7**.
- The first training run and its evaluation use the 4 Main calls only as a sanity check, not as the success gate. The success gate is the Gemini test set that Nimithra labels by hand (see `DATA_PLAN.md`).
- If a human ever grades these 44 items, drop the verdicts into `answer_key_main.json` (change the provenance) and re-run the comparisons.
