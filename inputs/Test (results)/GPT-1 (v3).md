# GPT-1 (v3) vs planted faults

Measured against AI-written synthetic calls and keys (planted faults); no human review.

| Item | Faults caught | Clean calls passed | Overall |
|---|---|---|---|
| Branding and Survey Check | 4/4 (100%) | 16/16 (100%) | 20/20 (100%) |
| Hold time and Dead Air | 1/1 (100%) | 19/19 (100%) | 20/20 (100%) |
| Verified customer | 1/1 (100%) | 19/19 (100%) | 20/20 (100%) |
| Personalized the call/ticket appropriately | 4/4 (100%) | 16/16 (100%) | 20/20 (100%) |
| Empathy & Acknowledgment Statement | 9/9 (100%) | 4/11 (36%) | 13/20 (65%) |
| Paraphrasing | 2/2 (100%) | 4/18 (22%) | 6/20 (30%) |
| Active listening | 2/2 (100%) | 18/18 (100%) | 20/20 (100%) |
| Took ownership of the problem | 3/5 (60%) | 14/15 (93%) | 17/20 (85%) |
| Build rapport and observed professionalism | 3/3 (100%) | 15/17 (88%) | 18/20 (90%) |
| Probing | 2/3 (67%) | 16/17 (94%) | 18/20 (90%) |
| Confirmed the issue is resolved | 7/10 (70%) | 8/10 (80%) | 15/20 (75%) |
| **All items** | 38/44 (86%) | 149/176 (85%) | **187/220 (85%)** |

## Missed faults (6)

- gpt_09_noname_nogreet_noclose_noconfirm: Confirmed the issue is resolved graded PASS (planted fault)
- gpt_11_empathy_noconfirm: Confirmed the issue is resolved graded PASS (planted fault)
- gpt_13_noprobe_empathy_ownership_noconfirm: Took ownership of the problem graded PASS (planted fault)
- gpt_13_noprobe_empathy_ownership_noconfirm: Confirmed the issue is resolved graded PASS (planted fault)
- gpt_18_empathy_noconfirm_ownership: Took ownership of the problem graded PASS (planted fault)
- gpt_19_noprobe_ownership_noname_empathy_rapport_noconfirm: Probing graded PASS (planted fault)

## False alarms (27)

- gpt_02_clean: Empathy & Acknowledgment Statement graded FAIL (not planted)
- gpt_03_clean: Paraphrasing graded FAIL (not planted)
- gpt_03_clean: Build rapport and observed professionalism graded FAIL (not planted)
- gpt_04_clean: Empathy & Acknowledgment Statement graded FAIL (not planted)
- gpt_05_clean: Empathy & Acknowledgment Statement graded FAIL (not planted)
- gpt_06_nogreet: Paraphrasing graded FAIL (not planted)
- gpt_07_noclose: Paraphrasing graded FAIL (not planted)
- gpt_07_noclose: Probing graded FAIL (not planted)
- gpt_07_noclose: Confirmed the issue is resolved graded FAIL (not planted)
- gpt_08_noverify_noclose: Empathy & Acknowledgment Statement graded FAIL (not planted)
- gpt_08_noverify_noclose: Paraphrasing graded FAIL (not planted)
- gpt_08_noverify_noclose: Build rapport and observed professionalism graded FAIL (not planted)
- gpt_09_noname_nogreet_noclose_noconfirm: Empathy & Acknowledgment Statement graded FAIL (not planted)
- gpt_09_noname_nogreet_noclose_noconfirm: Paraphrasing graded FAIL (not planted)
- gpt_10_gaps_noconfirm_noname: Empathy & Acknowledgment Statement graded FAIL (not planted)
- gpt_10_gaps_noconfirm_noname: Paraphrasing graded FAIL (not planted)
- gpt_11_empathy_noconfirm: Paraphrasing graded FAIL (not planted)
- gpt_13_noprobe_empathy_ownership_noconfirm: Paraphrasing graded FAIL (not planted)
- gpt_14_ownership_empathy_noprobe_noconfirm: Paraphrasing graded FAIL (not planted)
- gpt_15_al_empathy: Paraphrasing graded FAIL (not planted)
- gpt_15_al_empathy: Confirmed the issue is resolved graded FAIL (not planted)
- gpt_16_noconfirm: Empathy & Acknowledgment Statement graded FAIL (not planted)
- gpt_16_noconfirm: Paraphrasing graded FAIL (not planted)
- gpt_17_rapport_empathy_noconfirm: Paraphrasing graded FAIL (not planted)
- gpt_17_rapport_empathy_noconfirm: Took ownership of the problem graded FAIL (not planted)
- gpt_18_empathy_noconfirm_ownership: Paraphrasing graded FAIL (not planted)
- gpt_19_noprobe_ownership_noname_empathy_rapport_noconfirm: Paraphrasing graded FAIL (not planted)

## Per call

| Call | Score | Mismatches |
|---|---|---|
| gpt_01_clean | 100.0 | all match |
| gpt_02_clean | 88.3 | false alarm Empathy & Acknowledgment Statement |
| gpt_03_clean | 83.3 | false alarm Paraphrasing; false alarm Build rapport and observed professionalism |
| gpt_04_clean | 88.3 | false alarm Empathy & Acknowledgment Statement |
| gpt_05_clean | 88.3 | false alarm Empathy & Acknowledgment Statement |
| gpt_06_nogreet | 85.0 | false alarm Paraphrasing |
| gpt_07_noclose | 58.3 | false alarm Paraphrasing; false alarm Probing; false alarm Confirmed the issue is resolved |
| gpt_08_noverify_noclose | 50.0 | false alarm Empathy & Acknowledgment Statement; false alarm Paraphrasing; false alarm Build rapport and observed professionalism |
| gpt_09_noname_nogreet_noclose_noconfirm | 68.3 | false alarm Empathy & Acknowledgment Statement; false alarm Paraphrasing; missed Confirmed the issue is resolved |
| gpt_10_gaps_noconfirm_noname | 58.3 | false alarm Empathy & Acknowledgment Statement; false alarm Paraphrasing |
| gpt_11_empathy_noconfirm | 78.3 | false alarm Paraphrasing; missed Confirmed the issue is resolved |
| gpt_12_nopara_empathy | 78.3 | all match |
| gpt_13_noprobe_empathy_ownership_noconfirm | 61.7 | false alarm Paraphrasing; missed Took ownership of the problem; missed Confirmed the issue is resolved |
| gpt_14_ownership_empathy_noprobe_noconfirm | 35.0 | false alarm Paraphrasing |
| gpt_15_al_empathy | 61.7 | false alarm Paraphrasing; false alarm Confirmed the issue is resolved |
| gpt_16_noconfirm | 68.3 | false alarm Empathy & Acknowledgment Statement; false alarm Paraphrasing |
| gpt_17_rapport_empathy_noconfirm | 45.0 | false alarm Paraphrasing; false alarm Took ownership of the problem |
| gpt_18_empathy_noconfirm_ownership | 68.3 | false alarm Paraphrasing; missed Took ownership of the problem |
| gpt_19_noprobe_ownership_noname_empathy_rapport_noconfirm | 40.0 | false alarm Paraphrasing; missed Probing |
| gpt_20_nopara_al_rapport_noname_empathy_ownership_noconfirm | 33.3 | all match |
