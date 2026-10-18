# AG50: engines vs Antigravity's expected scorecards

50 calls. Expected scorecards were written by Antigravity (not human-reviewed).


## Summary

| | laya-stock | laya-ft | ollama |
|---|---|---|---|
| Calls scored | 50 | 50 | 50 |
| All items matching expected | 426/550 (77%) | 452/550 (82%) | 471/550 (86%) |
| Model-judged items matching (7 items: empathy ... resolved) | 226/350 (65%) | 252/350 (72%) | 275/350 (79%) |
| Mean absolute final-score error | 16.0 | 12.7 | 12.8 |
| Auto-fail decision matching | 50/50 | 50/50 | 50/50 |
| Mean time per call | 17.1 s | 16.2 s | 386.2 s |

## Per item: matching expected / balanced accuracy (FAIL = positive)

| Item | expected FAILs | laya-stock | laya-ft | ollama |
|---|---|---|---|---|
| Branding | 11 | 50/50 / 1.00 | 50/50 / 1.00 | 50/50 / 1.00 |
| Dead air | 11 | 50/50 / 1.00 | 50/50 / 1.00 | 46/50 / 0.95 |
| Verified | 10 | 50/50 / 1.00 | 50/50 / 1.00 | 50/50 / 1.00 |
| Personalized | 12 | 50/50 / 1.00 | 50/50 / 1.00 | 50/50 / 1.00 |
| Empathy | 17 | 17/50 / 0.50 | 25/50 / 0.62 | 39/50 / 0.70 |
| Paraphrasing | 16 | 32/50 / 0.54 | 34/50 / 0.58 | 34/50 / 0.50 |
| Active listening | 15 | 35/50 / 0.50 | 35/50 / 0.50 | 35/50 / 0.50 |
| Ownership | 17 | 37/50 / 0.62 | 43/50 / 0.79 | 41/50 / 0.74 |
| Rapport | 15 | 35/50 / 0.50 | 35/50 / 0.71 | 39/50 / 0.63 |
| Probing | 13 | 29/50 / 0.64 | 40/50 / 0.67 | 43/50 / 0.81 |
| Resolved | 19 | 41/50 / 0.82 | 40/50 / 0.77 | 44/50 / 0.84 |

## Final scores per call

| Call | expected | laya-stock | laya-ft | ollama |
|---|---|---|---|---|
| ag_01 | 93.3 | 78.3 | 88.3 | 100.0 |
| ag_02 | 100.0 | 78.3 | 88.3 | 100.0 |
| ag_03 | 68.3 | 61.7 | 68.3 | 100.0 |
| ag_04 | 40.0 | 35.0 | 38.3 | 46.7 |
| ag_05 | 0.0 AF | 0.0 AF | 0.0 AF | 0.0 AF |
| ag_06 | 93.3 | 78.3 | 93.3 | 93.3 |
| ag_07 | 100.0 | 88.3 | 88.3 | 95.0 |
| ag_08 | 51.7 | 50.0 | 43.3 | 61.7 |
| ag_09 | 73.3 | 78.3 | 55.0 | 90.0 |
| ag_10 | 21.7 | 51.7 | 61.7 | 61.7 |
| ag_11 | 95.0 | 66.7 | 83.4 | 95.0 |
| ag_12 | 78.3 | 83.4 | 88.3 | 95.0 |
| ag_13 | 100.0 | 71.7 | 81.7 | 100.0 |
| ag_14 | 28.3 | 55.0 | 55.0 | 56.7 |
| ag_15 | 73.3 | 51.7 | 100.0 | 83.3 |
| ag_16 | 0.0 AF | 0.0 AF | 0.0 AF | 0.0 AF |
| ag_17 | 88.3 | 61.7 | 71.7 | 100.0 |
| ag_18 | 63.3 | 51.7 | 61.7 | 73.3 |
| ag_19 | 100.0 | 78.3 | 78.3 | 100.0 |
| ag_20 | 40.0 | 35.0 | 66.7 | 73.3 |
| ag_21 | 90.0 | 78.3 | 88.3 | 100.0 |
| ag_22 | 75.0 | 88.3 | 88.3 | 76.7 |
| ag_23 | 28.3 | 68.3 | 51.7 | 68.3 |
| ag_24 | 73.3 | 45.0 | 83.3 | 83.3 |
| ag_25 | 100.0 | 71.7 | 71.7 | 83.3 |
| ag_26 | 51.7 | 56.7 | 73.3 | 51.7 |
| ag_27 | 95.0 | 66.7 | 73.3 | 95.0 |
| ag_28 | 0.0 AF | 0.0 AF | 0.0 AF | 0.0 AF |
| ag_29 | 78.3 | 56.7 | 63.3 | 95.0 |
| ag_30 | 16.7 | 56.7 | 33.3 | 18.3 |
| ag_31 | 100.0 | 78.3 | 88.3 | 95.0 |
| ag_32 | 78.3 | 66.7 | 66.7 | 78.3 |
| ag_33 | 68.3 | 66.7 | 76.7 | 95.0 |
| ag_34 | 53.3 | 66.7 | 60.0 | 95.0 |
| ag_35 | 83.3 | 55.0 | 65.0 | 83.3 |
| ag_36 | 55.0 | 71.7 | 61.7 | 83.3 |
| ag_37 | 100.0 | 71.7 | 71.7 | 100.0 |
| ag_38 | 46.7 | 58.3 | 71.7 | 80.0 |
| ag_39 | 83.3 | 88.3 | 100.0 | 100.0 |
| ag_40 | 0.0 AF | 0.0 AF | 0.0 AF | 0.0 AF |
| ag_41 | 76.7 | 71.7 | 100.0 | 83.3 |
| ag_42 | 73.3 | 63.3 | 63.3 | 95.0 |
| ag_43 | 100.0 | 71.7 | 88.3 | 100.0 |
| ag_44 | 23.3 | 50.0 | 23.3 | 45.0 |
| ag_45 | 88.3 | 66.7 | 95.0 | 95.0 |
| ag_46 | 66.7 | 61.7 | 71.7 | 78.4 |
| ag_47 | 23.3 | 46.7 | 46.7 | 68.3 |
| ag_48 | 78.3 | 61.7 | 78.3 | 90.0 |
| ag_49 | 56.6 | 55.0 | 55.0 | 83.3 |
| ag_50 | 55.0 | 73.4 | 66.7 | 66.7 |

## Items where the engines and the expected key do not all agree

| Call | Item | expected | laya-stock | laya-ft | ollama | Claude's note |
|---|---|---|---|---|---|---|
| ag_01 | Empathy | PASS | FAIL | FAIL | PASS | Strong technical troubleshooting call where Daniel diagnoses DFS channel-switching firmware crashes on a Hub 4X, locks clean Wi-Fi channels, and pushes firmware |
| ag_01 | Paraphrasing | PASS | FAIL | PASS | PASS | Strong technical troubleshooting call where Daniel diagnoses DFS channel-switching firmware crashes on a Hub 4X, locks clean Wi-Fi channels, and pushes firmware |
| ag_01 | Active listening | FAIL | PASS | PASS | PASS | Strong technical troubleshooting call where Daniel diagnoses DFS channel-switching firmware crashes on a Hub 4X, locks clean Wi-Fi channels, and pushes firmware |
| ag_02 | Empathy | PASS | FAIL | FAIL | PASS | All-PASS excellent mobile roaming support call with natural STT disfluencies. Includes three hard-case PASS items: late-but-valid security verification at [03:3 |
| ag_02 | Paraphrasing | PASS | FAIL | PASS | PASS | All-PASS excellent mobile roaming support call with natural STT disfluencies. Includes three hard-case PASS items: late-but-valid security verification at [03:3 |
| ag_03 | Empathy | FAIL | FAIL | FAIL | PASS | Okay-tier billing dispute call (score 68.3) with three hard-case FAILs: Callum is polite and thorough with pro-rata math and takes strong personal ownership ([1 |
| ag_03 | Paraphrasing | FAIL | PASS | FAIL | PASS | Okay-tier billing dispute call (score 68.3) with three hard-case FAILs: Callum is polite and thorough with pro-rata math and takes strong personal ownership ([1 |
| ag_03 | Probing | PASS | FAIL | PASS | PASS | Okay-tier billing dispute call (score 68.3) with three hard-case FAILs: Callum is polite and thorough with pro-rata math and takes strong personal ownership ([1 |
| ag_03 | Resolved | FAIL | FAIL | FAIL | PASS | Okay-tier billing dispute call (score 68.3) with three hard-case FAILs: Callum is polite and thorough with pro-rata math and takes strong personal ownership ([1 |
| ag_04 | Empathy | PASS | FAIL | FAIL | PASS | Poor-tier TV support call (score 40.0) with 6 FAILs and 5 PASSes. Megan shows genuine early empathy ([00:24]), paraphrases well ([00:51]), and probes physical c |
| ag_04 | Active listening | FAIL | PASS | PASS | PASS | Poor-tier TV support call (score 40.0) with 6 FAILs and 5 PASSes. Megan shows genuine early empathy ([00:24]), paraphrases well ([00:51]), and probes physical c |
| ag_04 | Rapport | PASS | PASS | FAIL | PASS | Poor-tier TV support call (score 40.0) with 6 FAILs and 5 PASSes. Megan shows genuine early empathy ([00:24]), paraphrases well ([00:51]), and probes physical c |
| ag_04 | Resolved | FAIL | FAIL | PASS | FAIL | Poor-tier TV support call (score 40.0) with 6 FAILs and 5 PASSes. Megan shows genuine early empathy ([00:24]), paraphrases well ([00:51]), and probes physical c |
| ag_05 | Ownership | FAIL | PASS | FAIL | FAIL | Auto-fail call (final_score=0.0) where Gareth mechanically satisfies opening/closing branding (B PASS), security verification (V PASS), paraphrasing at [00:22]  |
| ag_05 | Rapport | FAIL | PASS | FAIL | PASS | Auto-fail call (final_score=0.0) where Gareth mechanically satisfies opening/closing branding (B PASS), security verification (V PASS), paraphrasing at [00:22]  |
| ag_06 | Empathy | PASS | FAIL | PASS | PASS | Strong technical troubleshooting call where Chloe verifies security early, shows warm empathy ([01:20]), paraphrases accurately ([01:33]), probes thoroughly int |
| ag_06 | Rapport | FAIL | PASS | FAIL | FAIL | Strong technical troubleshooting call where Chloe verifies security early, shows warm empathy ([01:20]), paraphrases accurately ([01:33]), probes thoroughly int |
| ag_06 | Resolved | PASS | FAIL | PASS | PASS | Strong technical troubleshooting call where Chloe verifies security early, shows warm empathy ([01:20]), paraphrases accurately ([01:33]), probes thoroughly int |
| ag_07 | Dead air | PASS | PASS | PASS | FAIL | Exemplary 100.0% call handling a vulnerable elderly customer's Digital Voice telecare and caller-ID failure. Includes three hard-PASS tests: (1) H is a near-mis |
| ag_07 | Empathy | PASS | FAIL | FAIL | PASS | Exemplary 100.0% call handling a vulnerable elderly customer's Digital Voice telecare and caller-ID failure. Includes three hard-PASS tests: (1) H is a near-mis |
| ag_08 | Empathy | PASS | FAIL | FAIL | PASS | Mixed 'okay' tier call with natural STT roughness. Sonia is warm, empathetic ([00:37], [02:02]), takes ownership ([02:41]), and resolves the stuck MNP split por |
| ag_08 | Paraphrasing | FAIL | PASS | PASS | PASS | Mixed 'okay' tier call with natural STT roughness. Sonia is warm, empathetic ([00:37], [02:02]), takes ownership ([02:41]), and resolves the stuck MNP split por |
| ag_08 | Rapport | PASS | PASS | FAIL | PASS | Mixed 'okay' tier call with natural STT roughness. Sonia is warm, empathetic ([00:37], [02:02]), takes ownership ([02:41]), and resolves the stuck MNP split por |
| ag_09 | Empathy | PASS | FAIL | FAIL | PASS | Strong technical diagnostic call where Marcus verifies PIN/address early ([00:24]–[00:32]), shows warm empathy ([00:13], [01:04]), paraphrases accurately ([01:1 |
| ag_09 | Ownership | FAIL | PASS | FAIL | PASS | Strong technical diagnostic call where Marcus verifies PIN/address early ([00:24]–[00:32]), shows warm empathy ([00:13], [01:04]), paraphrases accurately ([01:1 |
| ag_09 | Rapport | PASS | PASS | FAIL | PASS | Strong technical diagnostic call where Marcus verifies PIN/address early ([00:24]–[00:32]), shows warm empathy ([00:13], [01:04]), paraphrases accurately ([01:1 |
| ag_10 | Paraphrasing | FAIL | FAIL | PASS | PASS | Very poor soft-skills call (8 FAILs, 21.7 score) paired with live transactional resolution (RE hard PASS). Leah verifies PIN/address early ([00:31]–[00:54]) and |
| ag_10 | Active listening | FAIL | PASS | PASS | PASS | Very poor soft-skills call (8 FAILs, 21.7 score) paired with live transactional resolution (RE hard PASS). Leah verifies PIN/address early ([00:31]–[00:54]) and |
| ag_10 | Ownership | FAIL | PASS | PASS | PASS | Very poor soft-skills call (8 FAILs, 21.7 score) paired with live transactional resolution (RE hard PASS). Leah verifies PIN/address early ([00:31]–[00:54]) and |
| ag_10 | Rapport | FAIL | PASS | FAIL | PASS | Very poor soft-skills call (8 FAILs, 21.7 score) paired with live transactional resolution (RE hard PASS). Leah verifies PIN/address early ([00:31]–[00:54]) and |
| ag_10 | Probing | FAIL | FAIL | PASS | FAIL | Very poor soft-skills call (8 FAILs, 21.7 score) paired with live transactional resolution (RE hard PASS). Leah verifies PIN/address early ([00:31]–[00:54]) and |
| ag_10 | Resolved | PASS | PASS | FAIL | PASS | Very poor soft-skills call (8 FAILs, 21.7 score) paired with live transactional resolution (RE hard PASS). Leah verifies PIN/address early ([00:31]–[00:54]) and |
| ag_11 | Empathy | PASS | FAIL | FAIL | PASS | Strong emergency mobile support call where Toby handles an IMEI blacklist and replacement eSIM activation live during the call. Toby delivers the closing brandi |
| ag_11 | Probing | PASS | FAIL | PASS | PASS | Strong emergency mobile support call where Toby handles an IMEI blacklist and replacement eSIM activation live during the call. Toby delivers the closing brandi |
| ag_12 | Empathy | PASS | FAIL | PASS | PASS | STT-rough broadband upload fault call where Nadia passes 8 criteria including proactive ownership (booking Openreach and adding a free unlimited 5G tethering pa |
| ag_12 | Active listening | FAIL | PASS | PASS | PASS | STT-rough broadband upload fault call where Nadia passes 8 criteria including proactive ownership (booking Openreach and adding a free unlimited 5G tethering pa |
| ag_12 | Rapport | PASS | PASS | FAIL | PASS | STT-rough broadband upload fault call where Nadia passes 8 criteria including proactive ownership (booking Openreach and adding a free unlimited 5G tethering pa |
| ag_12 | Resolved | FAIL | PASS | PASS | PASS | STT-rough broadband upload fault call where Nadia passes 8 criteria including proactive ownership (booking Openreach and adding a free unlimited 5G tethering pa |
| ag_13 | Empathy | PASS | FAIL | FAIL | PASS | Exemplary 100% score call where Declan diagnoses a stuck RADIUS Content Shield policy attribute on the Belfast BNG. Tests three hard PASS cases: Empathy ([06:14 |
| ag_13 | Rapport | PASS | PASS | FAIL | PASS | Exemplary 100% score call where Declan diagnoses a stuck RADIUS Content Shield policy attribute on the Belfast BNG. Tests three hard PASS cases: Empathy ([06:14 |
| ag_13 | Probing | PASS | FAIL | PASS | PASS | Exemplary 100% score call where Declan diagnoses a stuck RADIUS Content Shield policy attribute on the Belfast BNG. Tests three hard PASS cases: Empathy ([06:14 |
| ag_14 | Dead air | PASS | PASS | PASS | FAIL | Poor home-move delay call failing 6 items (V, E, PA, O, R, RE) while passing B, H, P, AL, and PR. Tests five hard cases: late Verification ([08:27] past the 240 |
| ag_14 | Paraphrasing | FAIL | PASS | PASS | PASS | Poor home-move delay call failing 6 items (V, E, PA, O, R, RE) while passing B, H, P, AL, and PR. Tests five hard cases: late Verification ([08:27] past the 240 |
| ag_14 | Ownership | FAIL | PASS | FAIL | PASS | Poor home-move delay call failing 6 items (V, E, PA, O, R, RE) while passing B, H, P, AL, and PR. Tests five hard cases: late Verification ([08:27] past the 240 |
| ag_14 | Rapport | FAIL | PASS | PASS | PASS | Poor home-move delay call failing 6 items (V, E, PA, O, R, RE) while passing B, H, P, AL, and PR. Tests five hard cases: late Verification ([08:27] past the 240 |
| ag_14 | Probing | PASS | FAIL | PASS | PASS | Poor home-move delay call failing 6 items (V, E, PA, O, R, RE) while passing B, H, P, AL, and PR. Tests five hard cases: late Verification ([08:27] past the 240 |
| ag_14 | Resolved | FAIL | PASS | PASS | FAIL | Poor home-move delay call failing 6 items (V, E, PA, O, R, RE) while passing B, H, P, AL, and PR. Tests five hard cases: late Verification ([08:27] past the 240 |
| ag_15 | Empathy | PASS | FAIL | PASS | PASS | Warm, effective streaming support call where Amira resolves Jolanta's S-Net TV Go Error 409 device limit live on the call, but fails Paraphrasing ([00:50] jumpi |
| ag_15 | Paraphrasing | FAIL | FAIL | PASS | PASS | Warm, effective streaming support call where Amira resolves Jolanta's S-Net TV Go Error 409 device limit live on the call, but fails Paraphrasing ([00:50] jumpi |
| ag_15 | Probing | FAIL | FAIL | PASS | FAIL | Warm, effective streaming support call where Amira resolves Jolanta's S-Net TV Go Error 409 device limit live on the call, but fails Paraphrasing ([00:50] jumpi |
| ag_15 | Resolved | PASS | FAIL | PASS | PASS | Warm, effective streaming support call where Amira resolves Jolanta's S-Net TV Go Error 409 device limit live on the call, but fails Paraphrasing ([00:50] jumpi |
| ag_16 | Paraphrasing | FAIL | PASS | PASS | PASS | Auto-fail call where Agent Liam insults the customer ('idiot') at [15:03], blames the IT web team for portal outages ([08:16], O FAIL), omits branding ([00:00]) |
| ag_16 | Rapport | FAIL | PASS | FAIL | FAIL | Auto-fail call where Agent Liam insults the customer ('idiot') at [15:03], blames the IT web team for portal outages ([08:16], O FAIL), omits branding ([00:00]) |
| ag_17 | Empathy | FAIL | FAIL | FAIL | PASS | Near-miss Empathy FAIL ([00:19], [02:18], [03:29]): Svetlana is visibly shaken and frightened after a tech-support scammer phoned her landline, and while Agent  |
| ag_17 | Paraphrasing | PASS | PASS | FAIL | PASS | Near-miss Empathy FAIL ([00:19], [02:18], [03:29]): Svetlana is visibly shaken and frightened after a tech-support scammer phoned her landline, and while Agent  |
| ag_17 | Rapport | PASS | PASS | FAIL | PASS | Near-miss Empathy FAIL ([00:19], [02:18], [03:29]): Svetlana is visibly shaken and frightened after a tech-support scammer phoned her landline, and while Agent  |
| ag_17 | Probing | PASS | FAIL | PASS | PASS | Near-miss Empathy FAIL ([00:19], [02:18], [03:29]): Svetlana is visibly shaken and frightened after a tech-support scammer phoned her landline, and while Agent  |
| ag_17 | Resolved | PASS | FAIL | PASS | PASS | Near-miss Empathy FAIL ([00:19], [02:18], [03:29]): Svetlana is visibly shaken and frightened after a tech-support scammer phoned her landline, and while Agent  |
| ag_18 | Empathy | PASS | FAIL | FAIL | PASS | STT-rough call where Agent Owen performs strong optical diagnostics (PR PASS, AL PASS) and shows genuine empathy ([00:30], E PASS) and friendly rapport (R PASS) |
| ag_18 | Ownership | FAIL | PASS | PASS | PASS | STT-rough call where Agent Owen performs strong optical diagnostics (PR PASS, AL PASS) and shows genuine empathy ([00:30], E PASS) and friendly rapport (R PASS) |
| ag_18 | Probing | PASS | FAIL | FAIL | FAIL | STT-rough call where Agent Owen performs strong optical diagnostics (PR PASS, AL PASS) and shows genuine empathy ([00:30], E PASS) and friendly rapport (R PASS) |
| ag_18 | Resolved | FAIL | FAIL | PASS | PASS | STT-rough call where Agent Owen performs strong optical diagnostics (PR PASS, AL PASS) and shows genuine empathy ([00:30], E PASS) and friendly rapport (R PASS) |
| ag_19 | Empathy | PASS | FAIL | FAIL | PASS | Clean 100.0 PASS call demonstrating a brisk, concise, deeply technical agent style (R PASS hard case), a 90s managed hold ([03:34]-[05:28]) plus a 28s router-re |
| ag_19 | Paraphrasing | PASS | FAIL | FAIL | PASS | Clean 100.0 PASS call demonstrating a brisk, concise, deeply technical agent style (R PASS hard case), a 90s managed hold ([03:34]-[05:28]) plus a 28s router-re |
| ag_20 | Empathy | PASS | FAIL | PASS | PASS | Style-trap breaker (Section 9.4): Agent Benjamin is overflowing with warmth, politeness (R PASS), heartfelt empathy ([00:28], E PASS), personal ownership ([01:0 |
| ag_20 | Paraphrasing | FAIL | PASS | PASS | PASS | Style-trap breaker (Section 9.4): Agent Benjamin is overflowing with warmth, politeness (R PASS), heartfelt empathy ([00:28], E PASS), personal ownership ([01:0 |
| ag_20 | Active listening | FAIL | PASS | PASS | PASS | Style-trap breaker (Section 9.4): Agent Benjamin is overflowing with warmth, politeness (R PASS), heartfelt empathy ([00:28], E PASS), personal ownership ([01:0 |
| ag_20 | Rapport | PASS | PASS | FAIL | PASS | Style-trap breaker (Section 9.4): Agent Benjamin is overflowing with warmth, politeness (R PASS), heartfelt empathy ([00:28], E PASS), personal ownership ([01:0 |
| ag_20 | Probing | FAIL | FAIL | PASS | PASS | Style-trap breaker (Section 9.4): Agent Benjamin is overflowing with warmth, politeness (R PASS), heartfelt empathy ([00:28], E PASS), personal ownership ([01:0 |
| ag_20 | Resolved | PASS | FAIL | PASS | PASS | Style-trap breaker (Section 9.4): Agent Benjamin is overflowing with warmth, politeness (R PASS), heartfelt empathy ([00:28], E PASS), personal ownership ([01:0 |
| ag_21 | Empathy | PASS | FAIL | FAIL | PASS | Near-miss RE FAIL: Agent Daniel performs exemplary diagnostics (identifying a seized fan bearing at 0 RPM and 89C via telemetry), sets a temporary 4G low-therma |
| ag_21 | Resolved | FAIL | FAIL | PASS | PASS | Near-miss RE FAIL: Agent Daniel performs exemplary diagnostics (identifying a seized fan bearing at 0 RPM and 89C via telemetry), sets a temporary 4G low-therma |
| ag_22 | Empathy | FAIL | FAIL | FAIL | PASS | Hard-case E, AL, R FAILs paired with strong technical O, PR, H, RE PASSes under STT roughness. Agent Hannah never acknowledges Oluwaseun's anxiety about his new |
| ag_22 | Active listening | FAIL | PASS | PASS | PASS | Hard-case E, AL, R FAILs paired with strong technical O, PR, H, RE PASSes under STT roughness. Agent Hannah never acknowledges Oluwaseun's anxiety about his new |
| ag_22 | Rapport | FAIL | PASS | PASS | FAIL | Hard-case E, AL, R FAILs paired with strong technical O, PR, H, RE PASSes under STT roughness. Agent Hannah never acknowledges Oluwaseun's anxiety about his new |
| ag_22 | Probing | PASS | PASS | PASS | FAIL | Hard-case E, AL, R FAILs paired with strong technical O, PR, H, RE PASSes under STT roughness. Agent Hannah never acknowledges Oluwaseun's anxiety about his new |
| ag_23 | Paraphrasing | FAIL | PASS | FAIL | PASS | 8-FAIL very_poor call with hard-case PASSes on Branding ([00:00], [16:23]) and Probing ([01:53]-[03:40]) and hard-case FAILs on Hold/Dead Air ([04:06]-[05:02] 4 |
| ag_23 | Active listening | FAIL | PASS | PASS | PASS | 8-FAIL very_poor call with hard-case PASSes on Branding ([00:00], [16:23]) and Probing ([01:53]-[03:40]) and hard-case FAILs on Hold/Dead Air ([04:06]-[05:02] 4 |
| ag_23 | Ownership | FAIL | PASS | PASS | PASS | 8-FAIL very_poor call with hard-case PASSes on Branding ([00:00], [16:23]) and Probing ([01:53]-[03:40]) and hard-case FAILs on Hold/Dead Air ([04:06]-[05:02] 4 |
| ag_23 | Rapport | FAIL | PASS | FAIL | PASS | 8-FAIL very_poor call with hard-case PASSes on Branding ([00:00], [16:23]) and Probing ([01:53]-[03:40]) and hard-case FAILs on Hold/Dead Air ([04:06]-[05:02] 4 |
| ag_24 | Empathy | PASS | FAIL | PASS | PASS | Near-miss V FAIL and echo-trap PA FAIL on an otherwise warm, thorough call. In the first 4 minutes ([00:00]-[04:13]), Agent Megan refers only to the 'voicemail  |
| ag_24 | Paraphrasing | FAIL | PASS | PASS | PASS | Near-miss V FAIL and echo-trap PA FAIL on an otherwise warm, thorough call. In the first 4 minutes ([00:00]-[04:13]), Agent Megan refers only to the 'voicemail  |
| ag_24 | Probing | PASS | FAIL | PASS | PASS | Near-miss V FAIL and echo-trap PA FAIL on an otherwise warm, thorough call. In the first 4 minutes ([00:00]-[04:13]), Agent Megan refers only to the 'voicemail  |
| ag_24 | Resolved | PASS | FAIL | PASS | PASS | Near-miss V FAIL and echo-trap PA FAIL on an otherwise warm, thorough call. In the first 4 minutes ([00:00]-[04:13]), Agent Megan refers only to the 'voicemail  |
| ag_25 | Empathy | PASS | FAIL | FAIL | PASS | 100.0 excellent call with STT roughness and hard-case PASSes on Hold ([03:29]-[05:01] 82s managed hold for 1000-packet WAN ping test), Probing ([01:56]-[03:14]  |
| ag_25 | Probing | PASS | FAIL | FAIL | FAIL | 100.0 excellent call with STT roughness and hard-case PASSes on Hold ([03:29]-[05:01] 82s managed hold for 1000-packet WAN ping test), Probing ([01:56]-[03:14]  |
| ag_26 | Empathy | PASS | FAIL | FAIL | PASS | Hard-case B FAIL (near-miss 'thank you for contacting S-Net' at [00:00]), hard-case E PASS ([00:18], [02:06]) and PA PASS ([01:12]-[01:28]), paired with hard-ca |
| ag_26 | Ownership | FAIL | PASS | PASS | FAIL | Hard-case B FAIL (near-miss 'thank you for contacting S-Net' at [00:00]), hard-case E PASS ([00:18], [02:06]) and PA PASS ([01:12]-[01:28]), paired with hard-ca |
| ag_26 | Probing | FAIL | FAIL | PASS | FAIL | Hard-case B FAIL (near-miss 'thank you for contacting S-Net' at [00:00]), hard-case E PASS ([00:18], [02:06]) and PA PASS ([01:12]-[01:28]), paired with hard-ca |
| ag_27 | Empathy | PASS | FAIL | FAIL | PASS | Hard-case H FAIL: Marcus is polite and resolves the issue completely, but both holds ([04:53]-[05:47] 44s and [07:33]-[08:34] 51s) use casual phrases ('Just a s |
| ag_27 | Paraphrasing | PASS | PASS | FAIL | PASS | Hard-case H FAIL: Marcus is polite and resolves the issue completely, but both holds ([04:53]-[05:47] 44s and [07:33]-[08:34] 51s) use casual phrases ('Just a s |
| ag_27 | Probing | PASS | FAIL | PASS | PASS | Hard-case H FAIL: Marcus is polite and resolves the issue completely, but both holds ([04:53]-[05:47] 44s and [07:33]-[08:34] 51s) use casual phrases ('Just a s |
| ag_28 | Paraphrasing | PASS | FAIL | PASS | PASS | Auto-fail call (STT roughness=True): Agent snaps at [14:42] using banned word 'stupid'. Also features hard-case H FAIL ([04:44]-[05:33] 39s and [07:55]-[08:57]  |
| ag_28 | Active listening | FAIL | PASS | PASS | PASS | Auto-fail call (STT roughness=True): Agent snaps at [14:42] using banned word 'stupid'. Also features hard-case H FAIL ([04:44]-[05:33] 39s and [07:55]-[08:57]  |
| ag_28 | Rapport | FAIL | PASS | FAIL | PASS | Auto-fail call (STT roughness=True): Agent snaps at [14:42] using banned word 'stupid'. Also features hard-case H FAIL ([04:44]-[05:33] 39s and [07:55]-[08:57]  |
| ag_29 | Empathy | PASS | FAIL | FAIL | PASS | Hard-case P FAIL (Thaddeus gives his name at [00:08] but Toby never says 'Thaddeus'), hard-case PA FAIL (near-miss at [01:28] restating only account number/tari |
| ag_29 | Paraphrasing | FAIL | PASS | FAIL | PASS | Hard-case P FAIL (Thaddeus gives his name at [00:08] but Toby never says 'Thaddeus'), hard-case PA FAIL (near-miss at [01:28] restating only account number/tari |
| ag_29 | Active listening | FAIL | PASS | PASS | PASS | Hard-case P FAIL (Thaddeus gives his name at [00:08] but Toby never says 'Thaddeus'), hard-case PA FAIL (near-miss at [01:28] restating only account number/tari |
| ag_29 | Probing | PASS | FAIL | PASS | PASS | Hard-case P FAIL (Thaddeus gives his name at [00:08] but Toby never says 'Thaddeus'), hard-case PA FAIL (near-miss at [01:28] restating only account number/tari |
| ag_29 | Resolved | PASS | FAIL | FAIL | PASS | Hard-case P FAIL (Thaddeus gives his name at [00:08] but Toby never says 'Thaddeus'), hard-case PA FAIL (near-miss at [01:28] restating only account number/tari |
| ag_30 | Dead air | PASS | PASS | PASS | FAIL | 7-FAIL poor call: B FAIL (no closing branding), V FAIL (only postcode/account number), hard-case E FAIL (zero empathy when customer is in tears at -44.0), hard- |
| ag_30 | Ownership | FAIL | PASS | FAIL | FAIL | 7-FAIL poor call: B FAIL (no closing branding), V FAIL (only postcode/account number), hard-case E FAIL (zero empathy when customer is in tears at -44.0), hard- |
| ag_30 | Rapport | FAIL | PASS | FAIL | PASS | 7-FAIL poor call: B FAIL (no closing branding), V FAIL (only postcode/account number), hard-case E FAIL (zero empathy when customer is in tears at -44.0), hard- |
| ag_30 | Probing | FAIL | PASS | PASS | FAIL | 7-FAIL poor call: B FAIL (no closing branding), V FAIL (only postcode/account number), hard-case E FAIL (zero empathy when customer is in tears at -44.0), hard- |
| ag_31 | Dead air | PASS | PASS | PASS | FAIL | Clean 100% call with boundary closing branding on the 4th-from-last Agent turn ([18:41]), two long managed holds ([08:15], [13:45]), before/after ping verificat |
| ag_31 | Empathy | PASS | FAIL | FAIL | PASS | Clean 100% call with boundary closing branding on the 4th-from-last Agent turn ([18:41]), two long managed holds ([08:15], [13:45]), before/after ping verificat |
| ag_31 | Paraphrasing | PASS | FAIL | PASS | PASS | Clean 100% call with boundary closing branding on the 4th-from-last Agent turn ([18:41]), two long managed holds ([08:15], [13:45]), before/after ping verificat |
| ag_32 | Empathy | PASS | FAIL | FAIL | PASS | Hard-case FAIL on Personalization (Gavin addresses the customer politely as 'Mrs Whitaker' throughout but never says 'Genevieve', failing the deterministic cust |
| ag_33 | Empathy | PASS | FAIL | FAIL | PASS | 3 FAILs: Hold/Dead Air ([04:08]–[04:56] 38s and [06:53]–[07:49] 46s unannounced gaps), Paraphrasing ([01:31] 'Okay, I've got that noted down' without restating  |
| ag_33 | Paraphrasing | FAIL | PASS | PASS | PASS | 3 FAILs: Hold/Dead Air ([04:08]–[04:56] 38s and [06:53]–[07:49] 46s unannounced gaps), Paraphrasing ([01:31] 'Okay, I've got that noted down' without restating  |
| ag_33 | Ownership | FAIL | PASS | PASS | PASS | 3 FAILs: Hold/Dead Air ([04:08]–[04:56] 38s and [06:53]–[07:49] 46s unannounced gaps), Paraphrasing ([01:31] 'Okay, I've got that noted down' without restating  |
| ag_33 | Rapport | PASS | PASS | FAIL | PASS | 3 FAILs: Hold/Dead Air ([04:08]–[04:56] 38s and [06:53]–[07:49] 46s unannounced gaps), Paraphrasing ([01:31] 'Okay, I've got that noted down' without restating  |
| ag_33 | Probing | PASS | FAIL | PASS | PASS | 3 FAILs: Hold/Dead Air ([04:08]–[04:56] 38s and [06:53]–[07:49] 46s unannounced gaps), Paraphrasing ([01:31] 'Okay, I've got that noted down' without restating  |
| ag_34 | Empathy | FAIL | FAIL | FAIL | PASS | 5 FAILs (B, E, AL, O, R) with strong technical resolution (PA, PR, RE PASS): Liam omits closing branding ([15:23]), shows zero empathy for customer frustration  |
| ag_34 | Active listening | FAIL | PASS | PASS | PASS | 5 FAILs (B, E, AL, O, R) with strong technical resolution (PA, PR, RE PASS): Liam omits closing branding ([15:23]), shows zero empathy for customer frustration  |
| ag_34 | Ownership | FAIL | FAIL | FAIL | PASS | 5 FAILs (B, E, AL, O, R) with strong technical resolution (PA, PR, RE PASS): Liam omits closing branding ([15:23]), shows zero empathy for customer frustration  |
| ag_34 | Rapport | FAIL | PASS | FAIL | PASS | 5 FAILs (B, E, AL, O, R) with strong technical resolution (PA, PR, RE PASS): Liam omits closing branding ([15:23]), shows zero empathy for customer frustration  |
| ag_35 | Empathy | PASS | FAIL | FAIL | PASS | Single borderline FAIL on Ownership ([06:44]): Freya takes ownership of the £180 credit override, locks the return flag as Fulfilled, and confirms live that Cor |
| ag_35 | Rapport | PASS | PASS | FAIL | PASS | Single borderline FAIL on Ownership ([06:44]): Freya takes ownership of the £180 credit override, locks the return flag as Fulfilled, and confirms live that Cor |
| ag_35 | Probing | PASS | FAIL | PASS | PASS | Single borderline FAIL on Ownership ([06:44]): Freya takes ownership of the £180 credit override, locks the return flag as Fulfilled, and confirms live that Cor |
| ag_36 | Empathy | FAIL | FAIL | FAIL | PASS | Owen follows branding, manages his hold properly ([06:03]-[07:32]), probes thoroughly into physical hazard and ONT status, and takes ownership by ordering a 4G  |
| ag_36 | Paraphrasing | PASS | PASS | FAIL | PASS | Owen follows branding, manages his hold properly ([06:03]-[07:32]), probes thoroughly into physical hazard and ONT status, and takes ownership by ordering a 4G  |
| ag_36 | Rapport | FAIL | PASS | PASS | PASS | Owen follows branding, manages his hold properly ([06:03]-[07:32]), probes thoroughly into physical hazard and ONT status, and takes ownership by ordering a 4G  |
| ag_36 | Resolved | FAIL | PASS | PASS | PASS | Owen follows branding, manages his hold properly ([06:03]-[07:32]), probes thoroughly into physical hazard and ONT status, and takes ownership by ordering a 4G  |
| ag_37 | Empathy | PASS | FAIL | FAIL | PASS | Excellent 100.0 call with natural STT disfluencies. Zara verifies address and security question within 2 minutes ([00:52]-[01:21]), empathizes warmly ([00:23]-[ |
| ag_37 | Rapport | PASS | PASS | FAIL | PASS | Excellent 100.0 call with natural STT disfluencies. Zara verifies address and security question within 2 minutes ([00:52]-[01:21]), empathizes warmly ([00:23]-[ |
| ag_37 | Probing | PASS | FAIL | PASS | PASS | Excellent 100.0 call with natural STT disfluencies. Zara verifies address and security question within 2 minutes ([00:52]-[01:21]), empathizes warmly ([00:23]-[ |
| ag_37 | Resolved | PASS | PASS | FAIL | PASS | Excellent 100.0 call with natural STT disfluencies. Zara verifies address and security question within 2 minutes ([00:52]-[01:21]), empathizes warmly ([00:23]-[ |
| ag_38 | Empathy | PASS | FAIL | FAIL | PASS | Style-trap call: Benjamin is polite ([00:24], [06:25]), empathetic ([03:14], [15:13]), follows branding ([00:00], [18:20]), verifies PIN/address early ([00:54]- |
| ag_38 | Paraphrasing | FAIL | FAIL | PASS | PASS | Style-trap call: Benjamin is polite ([00:24], [06:25]), empathetic ([03:14], [15:13]), follows branding ([00:00], [18:20]), verifies PIN/address early ([00:54]- |
| ag_38 | Active listening | FAIL | PASS | PASS | PASS | Style-trap call: Benjamin is polite ([00:24], [06:25]), empathetic ([03:14], [15:13]), follows branding ([00:00], [18:20]), verifies PIN/address early ([00:54]- |
| ag_38 | Rapport | PASS | PASS | FAIL | PASS | Style-trap call: Benjamin is polite ([00:24], [06:25]), empathetic ([03:14], [15:13]), follows branding ([00:00], [18:20]), verifies PIN/address early ([00:54]- |
| ag_38 | Probing | FAIL | PASS | PASS | PASS | Style-trap call: Benjamin is polite ([00:24], [06:25]), empathetic ([03:14], [15:13]), follows branding ([00:00], [18:20]), verifies PIN/address early ([00:54]- |
| ag_38 | Resolved | FAIL | FAIL | PASS | FAIL | Style-trap call: Benjamin is polite ([00:24], [06:25]), empathetic ([03:14], [15:13]), follows branding ([00:00], [18:20]), verifies PIN/address early ([00:54]- |
| ag_39 | Empathy | PASS | FAIL | PASS | PASS | Good call (83.3) with two clear technical deduction failures: at [00:40] Chloe echoes Violetta's exact words from [00:10] verbatim (PA FAIL), and at [07:30] she |
| ag_39 | Paraphrasing | FAIL | PASS | PASS | PASS | Good call (83.3) with two clear technical deduction failures: at [00:40] Chloe echoes Violetta's exact words from [00:10] verbatim (PA FAIL), and at [07:30] she |
| ag_39 | Active listening | FAIL | PASS | PASS | PASS | Good call (83.3) with two clear technical deduction failures: at [00:40] Chloe echoes Violetta's exact words from [00:10] verbatim (PA FAIL), and at [07:30] she |
| ag_40 | Ownership | FAIL | PASS | FAIL | FAIL | Auto-fail call (final_score=0.0): Gareth follows opening/closing branding ([00:00], [16:34]), manages his single hold properly ([06:48]-[08:12]), verifies addre |
| ag_40 | Rapport | FAIL | PASS | FAIL | PASS | Auto-fail call (final_score=0.0): Gareth follows opening/closing branding ([00:00], [16:34]), manages his single hold properly ([06:48]-[08:12]), verifies addre |
| ag_40 | Probing | PASS | FAIL | PASS | PASS | Auto-fail call (final_score=0.0): Gareth follows opening/closing branding ([00:00], [16:34]), manages his single hold properly ([06:48]-[08:12]), verifies addre |
| ag_41 | Empathy | PASS | FAIL | PASS | PASS | Noah handles verification, empathy ([00:19], [00:43]), paraphrasing ([01:08]-[01:23]), a managed hold ([03:20]-[04:28]), and live resolution confirmation ([05:2 |
| ag_41 | Rapport | FAIL | PASS | PASS | PASS | Noah handles verification, empathy ([00:19], [00:43]), paraphrasing ([01:08]-[01:23]), a managed hold ([03:20]-[04:28]), and live resolution confirmation ([05:2 |
| ag_41 | Probing | FAIL | FAIL | PASS | FAIL | Noah handles verification, empathy ([00:19], [00:43]), paraphrasing ([01:08]-[01:23]), a managed hold ([03:20]-[04:28]), and live resolution confirmation ([05:2 |
| ag_42 | Empathy | FAIL | FAIL | FAIL | PASS | Yasmin performs strong technical probing ([01:56]-[06:53]), paraphrasing ([00:58]), active listening ([03:28], [16:42]), and a managed hold ([07:43]-[09:11]), b |
| ag_42 | Paraphrasing | PASS | FAIL | FAIL | PASS | Yasmin performs strong technical probing ([01:56]-[06:53]), paraphrasing ([00:58]), active listening ([03:28], [16:42]), and a managed hold ([07:43]-[09:11]), b |
| ag_42 | Resolved | FAIL | FAIL | FAIL | PASS | Yasmin performs strong technical probing ([01:56]-[06:53]), paraphrasing ([00:58]), active listening ([03:28], [16:42]), and a managed hold ([07:43]-[09:11]), b |
| ag_43 | Empathy | PASS | FAIL | FAIL | PASS | Exemplary 11/11 PASS call. Patrick verifies Wojciech's address, PIN, and security question at [03:38] (around 03:40, just inside the 240s threshold), manages a  |
| ag_43 | Probing | PASS | FAIL | PASS | PASS | Exemplary 11/11 PASS call. Patrick verifies Wojciech's address, PIN, and security question at [03:38] (around 03:40, just inside the 240s threshold), manages a  |
| ag_44 | Empathy | FAIL | FAIL | FAIL | PASS | 6-FAIL call (`V`, `P`, `E`, `PA`, `O`, `PR`) where `RE` and `R` still PASS. Imogen fails verification at [00:28] (only asks mobile number, DOB, and last bill am |
| ag_44 | Paraphrasing | FAIL | PASS | FAIL | PASS | 6-FAIL call (`V`, `P`, `E`, `PA`, `O`, `PR`) where `RE` and `R` still PASS. Imogen fails verification at [00:28] (only asks mobile number, DOB, and last bill am |
| ag_44 | Ownership | FAIL | PASS | FAIL | FAIL | 6-FAIL call (`V`, `P`, `E`, `PA`, `O`, `PR`) where `RE` and `R` still PASS. Imogen fails verification at [00:28] (only asks mobile number, DOB, and last bill am |
| ag_45 | Empathy | PASS | FAIL | PASS | PASS | Ross handles verification ([01:26]-[01:43]), empathy ([00:21]), paraphrasing ([00:58]), diagnostic probing ([02:03]-[02:40]), and live resolution verification ( |
| ag_45 | Active listening | FAIL | PASS | PASS | PASS | Ross handles verification ([01:26]-[01:43]), empathy ([00:21]), paraphrasing ([00:58]), diagnostic probing ([02:03]-[02:40]), and live resolution verification ( |
| ag_45 | Probing | PASS | FAIL | PASS | PASS | Ross handles verification ([01:26]-[01:43]), empathy ([00:21]), paraphrasing ([00:58]), diagnostic probing ([02:03]-[02:40]), and live resolution verification ( |
| ag_46 | Empathy | PASS | FAIL | FAIL | FAIL | Okay call with 4 FAILs (B, P, O, R). Agent Harriet opens with proper S-Net branding at [00:00], empathizes at [00:21], paraphrases at [00:44], verifies address  |
| ag_46 | Ownership | FAIL | PASS | PASS | PASS | Okay call with 4 FAILs (B, P, O, R). Agent Harriet opens with proper S-Net branding at [00:00], empathizes at [00:21], paraphrases at [00:44], verifies address  |
| ag_46 | Rapport | FAIL | PASS | FAIL | PASS | Okay call with 4 FAILs (B, P, O, R). Agent Harriet opens with proper S-Net branding at [00:00], empathizes at [00:21], paraphrases at [00:44], verifies address  |
| ag_46 | Probing | PASS | FAIL | PASS | PASS | Okay call with 4 FAILs (B, P, O, R). Agent Harriet opens with proper S-Net branding at [00:00], empathizes at [00:21], paraphrases at [00:44], verifies address  |
| ag_47 | Empathy | FAIL | FAIL | FAIL | PASS | Poor call with 7 FAILs (H, V, E, PA, AL, PR, RE) and 4 PASSes (B, P, O, R). Agent Craig uses proper branding ([00:00], [17:37]), addresses Zlatan by name, remai |
| ag_47 | Paraphrasing | FAIL | FAIL | FAIL | PASS | Poor call with 7 FAILs (H, V, E, PA, AL, PR, RE) and 4 PASSes (B, P, O, R). Agent Craig uses proper branding ([00:00], [17:37]), addresses Zlatan by name, remai |
| ag_47 | Active listening | FAIL | PASS | PASS | PASS | Poor call with 7 FAILs (H, V, E, PA, AL, PR, RE) and 4 PASSes (B, P, O, R). Agent Craig uses proper branding ([00:00], [17:37]), addresses Zlatan by name, remai |
| ag_47 | Probing | FAIL | PASS | PASS | PASS | Poor call with 7 FAILs (H, V, E, PA, AL, PR, RE) and 4 PASSes (B, P, O, R). Agent Craig uses proper branding ([00:00], [17:37]), addresses Zlatan by name, remai |
| ag_48 | Empathy | FAIL | FAIL | FAIL | PASS | Good technical security call with 2 FAILs (E, RE) and 9 PASSes. Customer Devika is terrified ([00:11], -48.0 sentiment) after clicking a phishing parcel SMS tha |
| ag_48 | Probing | PASS | FAIL | PASS | PASS | Good technical security call with 2 FAILs (E, RE) and 9 PASSes. Customer Devika is terrified ([00:11], -48.0 sentiment) after clicking a phishing parcel SMS tha |
| ag_49 | Empathy | PASS | FAIL | FAIL | PASS | Okay call with 3 FAILs (V, PA, PR) and 8 PASSes, featuring STT roughness on Customer turns. Agent Lewis opens and closes with proper S-Net branding ([00:00], [1 |
| ag_49 | Paraphrasing | FAIL | PASS | PASS | PASS | Okay call with 3 FAILs (V, PA, PR) and 8 PASSes, featuring STT roughness on Customer turns. Agent Lewis opens and closes with proper S-Net branding ([00:00], [1 |
| ag_49 | Probing | FAIL | FAIL | FAIL | PASS | Okay call with 3 FAILs (V, PA, PR) and 8 PASSes, featuring STT roughness on Customer turns. Agent Lewis opens and closes with proper S-Net branding ([00:00], [1 |
| ag_50 | Empathy | PASS | FAIL | FAIL | FAIL | Poor call with 6 FAILs (B, H, P, AL, O, R) and 5 PASSes (V, E, PA, PR, RE). Agent Eleanor opens with strong empathy ([00:22], E PASS), paraphrases the Dover cli |
| ag_50 | Active listening | FAIL | PASS | PASS | PASS | Poor call with 6 FAILs (B, H, P, AL, O, R) and 5 PASSes (V, E, PA, PR, RE). Agent Eleanor opens with strong empathy ([00:22], E PASS), paraphrases the Dover cli |
| ag_50 | Ownership | FAIL | PASS | PASS | PASS | Poor call with 6 FAILs (B, H, P, AL, O, R) and 5 PASSes (V, E, PA, PR, RE). Agent Eleanor opens with strong empathy ([00:22], E PASS), paraphrases the Dover cli |
| ag_50 | Rapport | FAIL | PASS | FAIL | FAIL | Poor call with 6 FAILs (B, H, P, AL, O, R) and 5 PASSes (V, E, PA, PR, RE). Agent Eleanor opens with strong empathy ([00:22], E PASS), paraphrases the Dover cli |
