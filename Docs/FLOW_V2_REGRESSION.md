## Main tests vs expected

### gold_01_excellent_22min: expected 100.0, laya-ft 100.0, laya-ft-v2b 100.0

| Item | Expected | laya-ft | laya-ft-v2b |
|---|---|---|---|
| Branding and Survey Check | PASS | PASS | PASS |
| Hold time and Dead Air | PASS | PASS | PASS |
| Verified customer | PASS | PASS | PASS |
| Personalized the call/ticket appropriately | PASS | PASS | PASS |
| Empathy & Acknowledgment Statement | PASS | PASS | PASS |
| Paraphrasing | PASS | PASS | PASS |
| Active listening | PASS | PASS | PASS |
| Took ownership of the problem | PASS | PASS | PASS |
| Build rapport and observed professionalism | PASS | PASS | PASS |
| Probing | PASS | PASS | PASS |
| Confirmed the issue is resolved | PASS | PASS | PASS |

### gold_02_good_17min: expected 88.3, laya-ft 76.7, laya-ft-v2b 88.3

| Item | Expected | laya-ft | laya-ft-v2b |
|---|---|---|---|
| Branding and Survey Check | FAIL | FAIL | FAIL |
| Hold time and Dead Air | PASS | PASS | PASS |
| Verified customer | PASS | PASS | PASS |
| Personalized the call/ticket appropriately | PASS | PASS | PASS |
| Empathy & Acknowledgment Statement | PASS | **FAIL** ✗ | PASS |
| Paraphrasing | PASS | PASS | PASS |
| Active listening | FAIL | FAIL | FAIL |
| Took ownership of the problem | PASS | PASS | PASS |
| Build rapport and observed professionalism | PASS | PASS | PASS |
| Probing | PASS | PASS | PASS |
| Confirmed the issue is resolved | PASS | PASS | PASS |

### gold_03_okay_22min: expected 56.7, laya-ft 50.0, laya-ft-v2b 50.0

| Item | Expected | laya-ft | laya-ft-v2b |
|---|---|---|---|
| Branding and Survey Check | PASS | PASS | PASS |
| Hold time and Dead Air | FAIL | FAIL | FAIL |
| Verified customer | FAIL | FAIL | FAIL |
| Personalized the call/ticket appropriately | PASS | PASS | PASS |
| Empathy & Acknowledgment Statement | FAIL | FAIL | FAIL |
| Paraphrasing | FAIL | FAIL | FAIL |
| Active listening | PASS | **FAIL** ✗ | **FAIL** ✗ |
| Took ownership of the problem | PASS | PASS | PASS |
| Build rapport and observed professionalism | PASS | PASS | PASS |
| Probing | PASS | PASS | PASS |
| Confirmed the issue is resolved | PASS | PASS | PASS |

### gold_04_bad_16min: expected 13.3, laya-ft 30.0, laya-ft-v2b 30.0

| Item | Expected | laya-ft | laya-ft-v2b |
|---|---|---|---|
| Branding and Survey Check | FAIL | FAIL | FAIL |
| Hold time and Dead Air | FAIL | FAIL | FAIL |
| Verified customer | PASS | PASS | PASS |
| Personalized the call/ticket appropriately | FAIL | FAIL | FAIL |
| Empathy & Acknowledgment Statement | FAIL | FAIL | FAIL |
| Paraphrasing | FAIL | FAIL | FAIL |
| Active listening | PASS | PASS | PASS |
| Took ownership of the problem | FAIL | FAIL | FAIL |
| Build rapport and observed professionalism | FAIL | FAIL | FAIL |
| Probing | FAIL | **PASS** ✗ | **PASS** ✗ |
| Confirmed the issue is resolved | FAIL | FAIL | FAIL |

### Main tests: items matching expected

| Item | laya-ft | laya-ft-v2b |
|---|---|---|
| Branding and Survey Check | 4/4 | 4/4 |
| Hold time and Dead Air | 4/4 | 4/4 |
| Verified customer | 4/4 | 4/4 |
| Personalized the call/ticket appropriately | 4/4 | 4/4 |
| Empathy & Acknowledgment Statement | 3/4 | 4/4 |
| Paraphrasing | 4/4 | 4/4 |
| Active listening | 3/4 | 3/4 |
| Took ownership of the problem | 4/4 | 4/4 |
| Build rapport and observed professionalism | 4/4 | 4/4 |
| Probing | 3/4 | 3/4 |
| Confirmed the issue is resolved | 4/4 | 4/4 |
| **All items** | **41/44** | **42/44** |

## Bulk b_* calls vs the defects in their filenames

| Item | laya-ft | laya-ft-v2b |
|---|---|---|
| Branding and Survey Check | 35/35 | 35/35 |
| Hold time and Dead Air | 34/34 | 34/34 |
| Verified customer | 34/34 | 34/34 |
| Personalized the call/ticket appropriately | 35/35 | 35/35 |
| Empathy & Acknowledgment Statement | 34/34 | 34/34 |
| Paraphrasing | 29/34 | 30/34 |
| Active listening | 33/33 | 33/33 |
| Took ownership of the problem | 33/33 | 33/33 |
| Build rapport and observed professionalism | 24/33 | 24/33 |
| Probing | 34/34 | 34/34 |
| Confirmed the issue is resolved | 33/33 | 33/33 |
| **All items** | **358/372** | **359/372** |

<details><summary>laya-ft: 14 mismatches</summary>

- b_05_nogreet: Paraphrasing FAIL (want PASS)
- b_08_noname: Paraphrasing FAIL (want PASS)
- b_10_empathy: Paraphrasing FAIL (want PASS)
- b_10_empathy: Build rapport and observed professionalism FAIL (want PASS)
- b_13_ownership: Paraphrasing FAIL (want PASS)
- b_13_ownership: Build rapport and observed professionalism FAIL (want PASS)
- b_18_empathy_ownership: Build rapport and observed professionalism FAIL (want PASS)
- b_20_gaps_rapport: Paraphrasing FAIL (want PASS)
- b_23_noprobe_ownership: Build rapport and observed professionalism FAIL (want PASS)
- b_24_empathy_noname: Build rapport and observed professionalism FAIL (want PASS)
- b_25_noprobe_noverify_ownership: Build rapport and observed professionalism FAIL (want PASS)
- b_29_al_noprobe_ownership: Build rapport and observed professionalism FAIL (want PASS)
- b_30_empathy_gaps_noname_noverify: Build rapport and observed professionalism FAIL (want PASS)
- b_33_noclose_noname_nopara_noprobe_ownership: Build rapport and observed professionalism FAIL (want PASS)

</details>

<details><summary>laya-ft-v2b: 13 mismatches</summary>

- b_08_noname: Paraphrasing FAIL (want PASS)
- b_10_empathy: Paraphrasing FAIL (want PASS)
- b_10_empathy: Build rapport and observed professionalism FAIL (want PASS)
- b_13_ownership: Build rapport and observed professionalism FAIL (want PASS)
- b_18_empathy_ownership: Paraphrasing FAIL (want PASS)
- b_18_empathy_ownership: Build rapport and observed professionalism FAIL (want PASS)
- b_23_noprobe_ownership: Build rapport and observed professionalism FAIL (want PASS)
- b_24_empathy_noname: Paraphrasing FAIL (want PASS)
- b_24_empathy_noname: Build rapport and observed professionalism FAIL (want PASS)
- b_25_noprobe_noverify_ownership: Build rapport and observed professionalism FAIL (want PASS)
- b_29_al_noprobe_ownership: Build rapport and observed professionalism FAIL (want PASS)
- b_30_empathy_gaps_noname_noverify: Build rapport and observed professionalism FAIL (want PASS)
- b_33_noclose_noname_nopara_noprobe_ownership: Build rapport and observed professionalism FAIL (want PASS)

</details>

## Other bulk calls: final scores

| Call | laya-ft | laya-ft-v2b |
|---|---|---|
| b_35_autofail | 0.0 AF | 0.0 AF |
| b_36_autofail | 0.0 AF | 0.0 AF |
| b_37_autofail | 0.0 AF | 0.0 AF |
| b_38_autofail | 0.0 AF | 0.0 AF |
| b_39_autofail | 0.0 AF | 0.0 AF |
| real_20min_above_average | 80.0 | 90.0 |
| real_20min_auto_fail | 0.0 AF | 0.0 AF |
| real_20min_low | 38.3 | 28.3 |
| real_20min_mid | 61.7 | 71.7 |
| real_20min_perfect_100 | 90.0 | 100.0 |
| real_long_aboveavg | 100.0 | 90.0 |
| real_long_autofail_escalation | 83.3 | 83.3 |
| real_long_autofail_profanity | 0.0 AF | 0.0 AF |
| real_long_good | 100.0 | 90.0 |
| real_long_high | 100.0 | 90.0 |
| real_long_low | 55.0 | 16.7 |
| real_long_mid | 61.7 | 40.0 |
| real_long_midlow | 55.0 | 16.7 |
| real_long_poor | 55.0 | 26.7 |
| v8_aboveavg | 76.7 | 76.7 |
| v8_autofail_shutup | 0.0 AF | 0.0 AF |
| v8_autofail_stupid | 0.0 AF | 0.0 AF |
| v8_good | 83.3 | 83.3 |
| v8_high | 88.3 | 88.3 |
| v8_low | 50.0 | 61.7 |
| v8_mid | 93.3 | 93.3 |
| v8_midlow | 83.3 | 83.3 |
| v8_perfect | 93.3 | 93.3 |
| v8_poor | 16.7 | 16.7 |
