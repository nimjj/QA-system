# Main tests

Four realistic S-Net tech-support calls (16–22 minutes), graded by hand against the tenant-abc matrix in `resources/criteria_config.json`. The app was **not** run to produce these grades. Each `expected/expected_*.json` uses the same layout as the `/api/evaluate` response, so it can be diffed against a real run.

| File | Tier | Length | Turns | Soft Skills | Technical | **Score** | Failed items |
|---|---|---|---|---|---|---|---|
| `gold_01_excellent_22min` | Excellent | 22:08 | 109 | 100 | 100 | **100.0** | none |
| `gold_02_good_17min` | Good | 17:28 | 85 | 85 | 90 | **88.3** | Branding (closing), Active listening |
| `gold_03_okay_22min` | Okay | 21:39 | 117 | 50 | 60 | **56.7** | Dead air, Verified, Empathy, Paraphrasing |
| `gold_04_bad_16min` | Bad | 16:25 | 111 | 0 | 20 | **13.3** | everything except Verified and Active listening |

Score = Soft Skills × 0.333 + Technical Knowledge × 0.667. Each category starts at 100 and loses the item's deduction on a FAIL: Branding 15, Dead air 15, Personalized 15, Empathy 35, Rapport 20; Paraphrasing 15, Verified 25, Probing 25, Ownership 25, Active listening 10, Resolved 15.

The tiers are my labels. The app has no good/okay/bad bands, only the number.

## Running them
```bash
python Scripts/batch_test.py main --label laya     # or --label ollama
```
Results go to `inputs/Test (results)/Main tests (<label>)/`. The script sends the criteria from `resources/criteria_config.json` with each call, so no database is needed. It skips the `expected/` folder.

## What's in each expected file
- `result`: the scorecard exactly as the app would return it. It uses the app's own PASS and FAIL coaching strings so a diff lines up.
- `grader.items[]`: for each criterion, the timestamped evidence behind my rating, plus what the app is expected to do on that item (deterministic rule result, or what the pre-filter will hand to Laya).
- `grader.app_traps`: places where I expect the app to disagree with a human for reasons in the app, not the call.

## Expected disagreements to look for
- **Call 3, profanity.** The customer says "this stupid modem". Since the auto-fail check now reads agent lines only, this should **not** auto-fail. If it does, the fix isn't active on that engine.
- **Call 2, dead air → app FAIL.** A properly announced hold with check-ins is counted as two >30 s gaps (each turn is assumed to last 10 s).
- **Call 2, active listening → app PASS.** Two real re-asked questions are reworded, so they stay under the 0.70 similarity pre-filter.
- **Call 1, probing.** The 100-word question budget is used up by the greeting and address-check lines, so Laya never sees the diagnostic questions.
- **Empathy, Resolved and Rapport** are Laya calls with cutoffs that the main README already flags as off on real calls.

## Payload notes
- Turns carry `start_time_sec` and `sentiment_score`, which the API reads, plus `[mm:ss]` `start_time`/`end_time` strings for reading, which the API ignores. `customer_name` is set so the Personalized rule is exercised.
