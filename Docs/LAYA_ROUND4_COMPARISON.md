## Main tests vs expected

### gold_01_excellent_22min: expected 100.0, ollama 100.0, laya-v2 78.3, laya-v3.1 78.3, laya-ft 100.0

| Item | Expected | ollama | laya-v2 | laya-v3.1 | laya-ft |
|---|---|---|---|---|---|
| Branding and Survey Check | PASS | PASS | PASS | PASS | PASS |
| Hold time and Dead Air | PASS | PASS | PASS | PASS | PASS |
| Verified customer | PASS | PASS | PASS | PASS | PASS |
| Personalized the call/ticket appropriately | PASS | PASS | PASS | PASS | PASS |
| Empathy & Acknowledgment Statement | PASS | PASS | **FAIL** ✗ | **FAIL** ✗ | PASS |
| Paraphrasing | PASS | PASS | PASS | PASS | PASS |
| Active listening | PASS | PASS | PASS | PASS | PASS |
| Took ownership of the problem | PASS | PASS | PASS | PASS | PASS |
| Build rapport and observed professionalism | PASS | PASS | PASS | PASS | PASS |
| Probing | PASS | PASS | PASS | PASS | PASS |
| Confirmed the issue is resolved | PASS | PASS | **FAIL** ✗ | **FAIL** ✗ | PASS |

### gold_02_good_17min: expected 88.3, ollama 83.3, laya-v2 83.4, laya-v3.1 83.4, laya-ft 76.7

| Item | Expected | ollama | laya-v2 | laya-v3.1 | laya-ft |
|---|---|---|---|---|---|
| Branding and Survey Check | FAIL | FAIL | FAIL | FAIL | FAIL |
| Hold time and Dead Air | PASS | **FAIL** ✗ | PASS | PASS | PASS |
| Verified customer | PASS | PASS | PASS | PASS | PASS |
| Personalized the call/ticket appropriately | PASS | PASS | PASS | PASS | PASS |
| Empathy & Acknowledgment Statement | PASS | PASS | **FAIL** ✗ | **FAIL** ✗ | **FAIL** ✗ |
| Paraphrasing | PASS | PASS | PASS | PASS | PASS |
| Active listening | FAIL | FAIL | **PASS** ✗ | **PASS** ✗ | FAIL |
| Took ownership of the problem | PASS | PASS | PASS | PASS | PASS |
| Build rapport and observed professionalism | PASS | PASS | PASS | PASS | PASS |
| Probing | PASS | PASS | PASS | PASS | PASS |
| Confirmed the issue is resolved | PASS | PASS | PASS | PASS | PASS |

### gold_03_okay_22min: expected 56.7, ollama 78.3, laya-v2 60.0, laya-v3.1 66.7, laya-ft 50.0

| Item | Expected | ollama | laya-v2 | laya-v3.1 | laya-ft |
|---|---|---|---|---|---|
| Branding and Survey Check | PASS | PASS | PASS | PASS | PASS |
| Hold time and Dead Air | FAIL | FAIL | FAIL | FAIL | FAIL |
| Verified customer | FAIL | FAIL | FAIL | FAIL | FAIL |
| Personalized the call/ticket appropriately | PASS | PASS | PASS | PASS | PASS |
| Empathy & Acknowledgment Statement | FAIL | **PASS** ✗ | FAIL | FAIL | FAIL |
| Paraphrasing | FAIL | **PASS** ✗ | **PASS** ✗ | **PASS** ✗ | FAIL |
| Active listening | PASS | PASS | **FAIL** ✗ | PASS | **FAIL** ✗ |
| Took ownership of the problem | PASS | PASS | PASS | PASS | PASS |
| Build rapport and observed professionalism | PASS | PASS | PASS | PASS | PASS |
| Probing | PASS | PASS | PASS | PASS | PASS |
| Confirmed the issue is resolved | PASS | PASS | PASS | PASS | PASS |

### gold_04_bad_16min: expected 13.3, ollama 23.3, laya-v2 30.0, laya-v3.1 30.0, laya-ft 30.0

| Item | Expected | ollama | laya-v2 | laya-v3.1 | laya-ft |
|---|---|---|---|---|---|
| Branding and Survey Check | FAIL | FAIL | FAIL | FAIL | FAIL |
| Hold time and Dead Air | FAIL | FAIL | FAIL | FAIL | FAIL |
| Verified customer | PASS | PASS | PASS | PASS | PASS |
| Personalized the call/ticket appropriately | FAIL | FAIL | FAIL | FAIL | FAIL |
| Empathy & Acknowledgment Statement | FAIL | FAIL | FAIL | FAIL | FAIL |
| Paraphrasing | FAIL | **PASS** ✗ | **PASS** ✗ | **PASS** ✗ | FAIL |
| Active listening | PASS | PASS | PASS | PASS | PASS |
| Took ownership of the problem | FAIL | FAIL | FAIL | FAIL | FAIL |
| Build rapport and observed professionalism | FAIL | FAIL | **PASS** ✗ | **PASS** ✗ | FAIL |
| Probing | FAIL | FAIL | FAIL | FAIL | **PASS** ✗ |
| Confirmed the issue is resolved | FAIL | FAIL | FAIL | FAIL | FAIL |

### Main tests: items matching expected

| Item | ollama | laya-v2 | laya-v3.1 | laya-ft |
|---|---|---|---|---|
| Branding and Survey Check | 4/4 | 4/4 | 4/4 | 4/4 |
| Hold time and Dead Air | 3/4 | 4/4 | 4/4 | 4/4 |
| Verified customer | 4/4 | 4/4 | 4/4 | 4/4 |
| Personalized the call/ticket appropriately | 4/4 | 4/4 | 4/4 | 4/4 |
| Empathy & Acknowledgment Statement | 3/4 | 2/4 | 2/4 | 3/4 |
| Paraphrasing | 2/4 | 2/4 | 2/4 | 4/4 |
| Active listening | 4/4 | 2/4 | 3/4 | 3/4 |
| Took ownership of the problem | 4/4 | 4/4 | 4/4 | 4/4 |
| Build rapport and observed professionalism | 4/4 | 3/4 | 3/4 | 4/4 |
| Probing | 4/4 | 4/4 | 4/4 | 3/4 |
| Confirmed the issue is resolved | 4/4 | 3/4 | 3/4 | 4/4 |
| **All items** | **40/44** | **36/44** | **37/44** | **41/44** |

## Bulk b_* calls vs the defects in their filenames

| Item | ollama | laya-v2 | laya-v3.1 | laya-ft |
|---|---|---|---|---|
| Branding and Survey Check | 0/0 | 35/35 | 35/35 | 35/35 |
| Hold time and Dead Air | 0/0 | 34/34 | 34/34 | 34/34 |
| Verified customer | 0/0 | 34/34 | 34/34 | 34/34 |
| Personalized the call/ticket appropriately | 0/0 | 35/35 | 35/35 | 35/35 |
| Empathy & Acknowledgment Statement | 0/0 | 34/34 | 34/34 | 34/34 |
| Paraphrasing | 0/0 | 28/34 | 28/34 | 29/34 |
| Active listening | 0/0 | 30/33 | 33/33 | 33/33 |
| Took ownership of the problem | 0/0 | 33/33 | 33/33 | 33/33 |
| Build rapport and observed professionalism | 0/0 | 33/33 | 29/33 | 24/33 |
| Probing | 0/0 | 30/34 | 34/34 | 34/34 |
| Confirmed the issue is resolved | 0/0 | 22/33 | 22/33 | 33/33 |
| **All items** | **0/0** | **348/372** | **351/372** | **358/372** |

<details><summary>ollama: 0 mismatches</summary>


</details>

<details><summary>laya-v2: 24 mismatches</summary>

- b_05_nogreet: Paraphrasing FAIL (want PASS)
- b_10_empathy: Confirmed the issue is resolved FAIL (want PASS)
- b_11_nopara: Paraphrasing PASS (want FAIL)
- b_13_ownership: Confirmed the issue is resolved FAIL (want PASS)
- b_14_al: Active listening PASS (want FAIL)
- b_17_noprobe_noverify: Probing PASS (want FAIL)
- b_18_empathy_ownership: Confirmed the issue is resolved FAIL (want PASS)
- b_21_noname_nopara: Paraphrasing PASS (want FAIL)
- b_22_al_noverify: Active listening PASS (want FAIL)
- b_23_noprobe_ownership: Probing PASS (want FAIL)
- b_23_noprobe_ownership: Confirmed the issue is resolved FAIL (want PASS)
- b_24_empathy_noname: Confirmed the issue is resolved FAIL (want PASS)
- b_25_noprobe_noverify_ownership: Probing PASS (want FAIL)
- b_25_noprobe_noverify_ownership: Confirmed the issue is resolved FAIL (want PASS)
- b_26_empathy_noname_rapport: Confirmed the issue is resolved FAIL (want PASS)
- b_27_gaps_noconfirm_noverify: Confirmed the issue is resolved PASS (want FAIL)
- b_28_noclose_nogreet_nopara: Paraphrasing PASS (want FAIL)
- b_29_al_noprobe_ownership: Active listening PASS (want FAIL)
- b_29_al_noprobe_ownership: Confirmed the issue is resolved FAIL (want PASS)
- b_30_empathy_gaps_noname_noverify: Confirmed the issue is resolved FAIL (want PASS)
- b_33_noclose_noname_nopara_noprobe_ownership: Paraphrasing PASS (want FAIL)
- b_33_noclose_noname_nopara_noprobe_ownership: Probing PASS (want FAIL)
- b_33_noclose_noname_nopara_noprobe_ownership: Confirmed the issue is resolved FAIL (want PASS)
- b_34_empathy_gaps_noclose_nogreet_noname_nopa: Paraphrasing PASS (want FAIL)

</details>

<details><summary>laya-v3.1: 21 mismatches</summary>

- b_05_nogreet: Paraphrasing FAIL (want PASS)
- b_10_empathy: Confirmed the issue is resolved FAIL (want PASS)
- b_11_nopara: Paraphrasing PASS (want FAIL)
- b_13_ownership: Confirmed the issue is resolved FAIL (want PASS)
- b_16_rapport: Build rapport and observed professionalism PASS (want FAIL)
- b_18_empathy_ownership: Confirmed the issue is resolved FAIL (want PASS)
- b_20_gaps_rapport: Build rapport and observed professionalism PASS (want FAIL)
- b_21_noname_nopara: Paraphrasing PASS (want FAIL)
- b_23_noprobe_ownership: Confirmed the issue is resolved FAIL (want PASS)
- b_24_empathy_noname: Confirmed the issue is resolved FAIL (want PASS)
- b_25_noprobe_noverify_ownership: Confirmed the issue is resolved FAIL (want PASS)
- b_26_empathy_noname_rapport: Build rapport and observed professionalism PASS (want FAIL)
- b_26_empathy_noname_rapport: Confirmed the issue is resolved FAIL (want PASS)
- b_27_gaps_noconfirm_noverify: Confirmed the issue is resolved PASS (want FAIL)
- b_28_noclose_nogreet_nopara: Paraphrasing PASS (want FAIL)
- b_29_al_noprobe_ownership: Confirmed the issue is resolved FAIL (want PASS)
- b_30_empathy_gaps_noname_noverify: Confirmed the issue is resolved FAIL (want PASS)
- b_32_empathy_gaps_noconfirm_noverify_rapport: Build rapport and observed professionalism PASS (want FAIL)
- b_33_noclose_noname_nopara_noprobe_ownership: Paraphrasing PASS (want FAIL)
- b_33_noclose_noname_nopara_noprobe_ownership: Confirmed the issue is resolved FAIL (want PASS)
- b_34_empathy_gaps_noclose_nogreet_noname_nopa: Paraphrasing PASS (want FAIL)

</details>

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

## Other bulk calls: final scores

| Call | ollama | laya-v2 | laya-v3.1 | laya-ft |
|---|---|---|---|---|
| b_35_autofail | - | 0.0 AF | 0.0 AF | 0.0 AF |
| b_36_autofail | - | 0.0 AF | 0.0 AF | 0.0 AF |
| b_37_autofail | - | 0.0 AF | 0.0 AF | 0.0 AF |
| b_38_autofail | - | 0.0 AF | 0.0 AF | 0.0 AF |
| b_39_autofail | - | 0.0 AF | 0.0 AF | 0.0 AF |
| real_20min_above_average | - | 90.0 | 90.0 | 80.0 |
| real_20min_auto_fail | - | 0.0 AF | 0.0 AF | 0.0 AF |
| real_20min_low | - | 28.3 | 21.6 | 38.3 |
| real_20min_mid | - | 78.3 | 78.3 | 61.7 |
| real_20min_perfect_100 | - | 90.0 | 90.0 | 90.0 |
| real_long_aboveavg | - | 100.0 | 100.0 | 100.0 |
| real_long_autofail_escalation | - | 83.3 | 90.0 | 83.3 |
| real_long_autofail_profanity | - | 0.0 AF | 0.0 AF | 0.0 AF |
| real_long_good | - | 90.0 | 90.0 | 100.0 |
| real_long_high | - | 100.0 | 100.0 | 100.0 |
| real_long_low | - | 51.7 | 51.7 | 55.0 |
| real_long_mid | - | 51.7 | 51.7 | 61.7 |
| real_long_midlow | - | 51.7 | 51.7 | 55.0 |
| real_long_poor | - | 51.7 | 51.7 | 55.0 |
| v8_aboveavg | - | 83.3 | 83.3 | 76.7 |
| v8_autofail_shutup | - | 0.0 AF | 0.0 AF | 0.0 AF |
| v8_autofail_stupid | - | 0.0 AF | 0.0 AF | 0.0 AF |
| v8_good | - | 90.0 | 90.0 | 83.3 |
| v8_high | - | 95.0 | 95.0 | 88.3 |
| v8_low | - | 56.7 | 56.7 | 50.0 |
| v8_mid | - | 90.0 | 90.0 | 93.3 |
| v8_midlow | - | 73.3 | 73.3 | 83.3 |
| v8_perfect | - | 100.0 | 100.0 | 93.3 |
| v8_poor | - | 30.0 | 30.0 | 16.7 |
