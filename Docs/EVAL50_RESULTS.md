# Eval50: engines vs Claude's expected scorecards

50 calls. Expected scorecards were written by Claude before any engine ran (not human-reviewed).


## Summary

| | laya-ft | laya-stock | ollama |
|---|---|---|---|
| Calls scored | 50 | 50 | 50 |
| All items matching expected | 506/550 (92%) | 458/550 (83%) | 448/550 (81%) |
| Model-judged items matching (7 items: empathy ... resolved) | 306/350 (87%) | 258/350 (74%) | 251/350 (72%) |
| Mean absolute final-score error | 6.0 | 12.2 | 9.3 |
| Auto-fail decision matching | 50/50 | 50/50 | 50/50 |
| Mean time per call | 7.8 s | 7.7 s | 122.6 s |

## Per item: matching expected / balanced accuracy (FAIL = positive)

| Item | expected FAILs | laya-ft | laya-stock | ollama |
|---|---|---|---|---|
| Branding | 9 | 50/50 / 1.00 | 50/50 / 1.00 | 50/50 / 1.00 |
| Dead air | 8 | 50/50 / 1.00 | 50/50 / 1.00 | 47/50 / 0.96 |
| Verified | 10 | 50/50 / 1.00 | 50/50 / 1.00 | 50/50 / 1.00 |
| Personalized | 9 | 50/50 / 1.00 | 50/50 / 1.00 | 50/50 / 1.00 |
| Empathy | 16 | 45/50 / 0.93 | 42/50 / 0.88 | 34/50 / 0.65 |
| Paraphrasing | 16 | 45/50 / 0.86 | 40/50 / 0.77 | 34/50 / 0.50 |
| Active listening | 9 | 43/50 / 0.70 | 42/50 / 0.56 | 42/50 / 0.64 |
| Ownership | 14 | 41/50 / 0.68 | 38/50 / 0.57 | 40/50 / 0.64 |
| Rapport | 15 | 42/50 / 0.83 | 35/50 / 0.50 | 37/50 / 0.57 |
| Probing | 11 | 47/50 / 0.86 | 33/50 / 0.75 | 29/50 / 0.73 |
| Resolved | 20 | 43/50 / 0.82 | 28/50 / 0.60 | 35/50 / 0.73 |

## Final scores per call

| Call | expected | laya-ft | laya-stock | ollama |
|---|---|---|---|---|
| eval_01 | 100.0 | 100.0 | 100.0 | 100.0 |
| eval_02 | 100.0 | 100.0 | 71.7 | 100.0 |
| eval_03 | 100.0 | 100.0 | 100.0 | 100.0 |
| eval_04 | 100.0 | 100.0 | 83.3 | 85.0 |
| eval_05 | 100.0 | 100.0 | 83.3 | 90.0 |
| eval_06 | 100.0 | 93.3 | 78.3 | 93.3 |
| eval_07 | 100.0 | 100.0 | 90.0 | 73.3 |
| eval_08 | 100.0 | 88.3 | 71.7 | 83.3 |
| eval_09 | 95.0 | 95.0 | 85.0 | 95.0 |
| eval_10 | 95.0 | 85.0 | 58.3 | 95.0 |
| eval_11 | 90.0 | 90.0 | 80.0 | 100.0 |
| eval_12 | 90.0 | 93.3 | 73.3 | 83.3 |
| eval_13 | 78.3 | 88.3 | 88.3 | 73.3 |
| eval_14 | 78.3 | 78.3 | 51.7 | 78.3 |
| eval_15 | 93.3 | 100.0 | 73.3 | 73.3 |
| eval_16 | 73.3 | 100.0 | 83.3 | 73.3 |
| eval_17 | 83.3 | 83.3 | 73.3 | 90.0 |
| eval_18 | 93.3 | 93.3 | 73.3 | 55.0 |
| eval_19 | 85.0 | 85.0 | 85.0 | 78.3 |
| eval_20 | 73.3 | 73.3 | 63.3 | 83.3 |
| eval_21 | 81.7 | 88.3 | 61.7 | 83.3 |
| eval_22 | 68.3 | 76.7 | 73.3 | 78.3 |
| eval_23 | 88.3 | 95.0 | 78.3 | 95.0 |
| eval_24 | 73.3 | 73.3 | 63.3 | 73.3 |
| eval_25 | 73.3 | 73.3 | 73.3 | 68.3 |
| eval_26 | 66.7 | 73.3 | 63.3 | 83.3 |
| eval_27 | 51.7 | 68.3 | 68.3 | 56.7 |
| eval_28 | 78.3 | 76.7 | 73.3 | 56.7 |
| eval_29 | 61.7 | 71.7 | 88.3 | 90.0 |
| eval_30 | 51.7 | 51.7 | 51.7 | 51.7 |
| eval_31 | 76.7 | 90.0 | 68.3 | 71.7 |
| eval_32 | 68.3 | 68.3 | 51.7 | 51.7 |
| eval_33 | 65.0 | 81.7 | 78.3 | 100.0 |
| eval_34 | 46.6 | 56.6 | 56.6 | 56.6 |
| eval_35 | 83.3 | 83.3 | 80.0 | 80.0 |
| eval_36 | 51.7 | 55.0 | 68.3 | 45.0 |
| eval_37 | 71.7 | 71.7 | 68.3 | 56.7 |
| eval_38 | 48.3 | 65.0 | 45.0 | 56.6 |
| eval_39 | 58.3 | 58.3 | 58.3 | 51.7 |
| eval_40 | 38.3 | 55.0 | 51.7 | 40.0 |
| eval_41 | 38.3 | 38.3 | 61.7 | 33.3 |
| eval_42 | 36.7 | 36.7 | 36.7 | 35.0 |
| eval_43 | 50.0 | 50.0 | 56.7 | 40.0 |
| eval_44 | 45.0 | 61.7 | 51.7 | 66.7 |
| eval_45 | 35.0 | 60.0 | 50.0 | 40.0 |
| eval_46 | 11.7 | 28.3 | 51.7 | 23.3 |
| eval_47 | 15.0 | 48.3 | 45.0 | 45.0 |
| eval_48 | 0.0 AF | 0.0 AF | 0.0 AF | 0.0 AF |
| eval_49 | 0.0 AF | 0.0 AF | 0.0 AF | 0.0 AF |
| eval_50 | 0.0 AF | 0.0 AF | 0.0 AF | 0.0 AF |

## Items where the engines and the expected key do not all agree

| Call | Item | expected | laya-ft | laya-stock | ollama | Claude's note |
|---|---|---|---|---|---|---|
| eval_02 | Empathy | PASS | PASS | FAIL | PASS | All PASS. Billing query handled cleanly; a managed hold (announced, thanked) is not dead air; empathy for the worried customer; resolution explicitly confirmed. |
| eval_02 | Probing | PASS | PASS | FAIL | PASS | All PASS. Billing query handled cleanly; a managed hold (announced, thanked) is not dead air; empathy for the worried customer; resolution explicitly confirmed. |
| eval_04 | Dead air | PASS | PASS | PASS | FAIL | All PASS. Agent mentions another team ("the field team") but OWNS it: books it himself and promises a call back; that is not deflection. Two managed holds. |
| eval_04 | Probing | PASS | PASS | FAIL | PASS | All PASS. Agent mentions another team ("the field team") but OWNS it: books it himself and promises a call back; that is not deflection. Two managed holds. |
| eval_04 | Resolved | PASS | PASS | PASS | FAIL | All PASS. Agent mentions another team ("the field team") but OWNS it: books it himself and promises a call back; that is not deflection. Two managed holds. |
| eval_05 | Probing | PASS | PASS | FAIL | PASS | All PASS. Calm customer (no frustration to acknowledge), so Empathy is PASS by default; short, efficient, warm call. |
| eval_05 | Resolved | PASS | PASS | PASS | FAIL | All PASS. Calm customer (no frustration to acknowledge), so Empathy is PASS by default; short, efficient, warm call. |
| eval_06 | Empathy | PASS | PASS | FAIL | PASS | All PASS. Speed fault fixed on the call with a firmware push during a managed hold (announced, thanked); speed re-tested after the fix (legitimate re-check, not |
| eval_06 | Paraphrasing | PASS | PASS | FAIL | PASS | All PASS. Speed fault fixed on the call with a firmware push during a managed hold (announced, thanked); speed re-tested after the fix (legitimate re-check, not |
| eval_06 | Active listening | PASS | FAIL | PASS | FAIL | All PASS. Speed fault fixed on the call with a firmware push during a managed hold (announced, thanked); speed re-tested after the fix (legitimate re-check, not |
| eval_07 | Paraphrasing | PASS | PASS | FAIL | PASS | All PASS. Moving-house request; customer neutral; agent paraphrases, probes, confirms. |
| eval_07 | Probing | PASS | PASS | PASS | FAIL | All PASS. Moving-house request; customer neutral; agent paraphrases, probes, confirms. |
| eval_07 | Resolved | PASS | PASS | PASS | FAIL | All PASS. Moving-house request; customer neutral; agent paraphrases, probes, confirms. |
| eval_08 | Empathy | PASS | FAIL | FAIL | PASS | All PASS. Very upset customer (overcharged for months); agent shows strong empathy, owns the fix, confirms resolution. |
| eval_08 | Probing | PASS | PASS | FAIL | FAIL | All PASS. Very upset customer (overcharged for months); agent shows strong empathy, owns the fix, confirms resolution. |
| eval_09 | Resolved | PASS | PASS | FAIL | PASS | B: the agent never uses the closing script ("thank you for choosing S-Net"); ends with "Thanks, bye now". Everything else is good. |
| eval_10 | Paraphrasing | PASS | FAIL | FAIL | PASS | PE: the agent never addresses Rowan by name at any point. Everything else is good. |
| eval_10 | Probing | PASS | PASS | FAIL | PASS | PE: the agent never addresses Rowan by name at any point. Everything else is good. |
| eval_10 | Resolved | PASS | PASS | FAIL | PASS | PE: the agent never addresses Rowan by name at any point. Everything else is good. |
| eval_11 | Paraphrasing | PASS | PASS | FAIL | PASS | CR: agent says "that should fix it" and closes without asking whether it worked; the customer never confirms. |
| eval_11 | Resolved | FAIL | FAIL | FAIL | PASS | CR: agent says "that should fix it" and closes without asking whether it worked; the customer never confirms. |
| eval_12 | Paraphrasing | FAIL | PASS | FAIL | PASS | PA: the agent never restates or checks the customer's problem; goes straight to questions. Otherwise good. |
| eval_12 | Rapport | PASS | FAIL | PASS | PASS | PA: the agent never restates or checks the customer's problem; goes straight to questions. Otherwise good. |
| eval_12 | Probing | PASS | PASS | FAIL | FAIL | PA: the agent never restates or checks the customer's problem; goes straight to questions. Otherwise good. |
| eval_13 | Empathy | FAIL | FAIL | FAIL | PASS | E: the customer is clearly upset (repeat outage, working from home, losing money); the agent never acknowledges it and moves straight to process. Not rude, just |
| eval_13 | Probing | PASS | PASS | PASS | FAIL | E: the customer is clearly upset (repeat outage, working from home, losing money); the agent never acknowledges it and moves straight to process. Not rude, just |
| eval_13 | Resolved | FAIL | PASS | PASS | FAIL | E: the customer is clearly upset (repeat outage, working from home, losing money); the agent never acknowledges it and moves straight to process. Not rude, just |
| eval_14 | Probing | PASS | PASS | FAIL | PASS | H: two unannounced silences of about 45 s and 50 s while the agent works (customer asks "hello?"). V: no PIN/address/security question in the first 4 minutes; t |
| eval_14 | Resolved | PASS | PASS | FAIL | PASS | H: two unannounced silences of about 45 s and 50 s while the agent works (customer asks "hello?"). V: no PIN/address/security question in the first 4 minutes; t |
| eval_15 | Active listening | FAIL | PASS | PASS | PASS | AL: the agent asks for the order number twice after the customer already gave it, and re-asks which phone was ordered after it was stated. Otherwise good. |
| eval_15 | Probing | PASS | PASS | FAIL | FAIL | AL: the agent asks for the order number twice after the customer already gave it, and re-asks which phone was ordered after it was stated. Otherwise good. |
| eval_15 | Resolved | PASS | PASS | FAIL | FAIL | AL: the agent asks for the order number twice after the customer already gave it, and re-asks which phone was ordered after it was stated. Otherwise good. |
| eval_16 | Probing | FAIL | PASS | FAIL | FAIL | PR: the agent asks no diagnostic questions about the problem at all (only verification and admin questions), and just sends a replacement remote. Probing FAIL.  |
| eval_16 | Resolved | FAIL | PASS | PASS | FAIL | PR: the agent asks no diagnostic questions about the problem at all (only verification and admin questions), and just sends a replacement remote. Probing FAIL.  |
| eval_17 | Ownership | FAIL | FAIL | FAIL | PASS | O: "Router faults are the hardware team's area, you'd have to call them on their own number" - tells the customer to call elsewhere. The agent stays polite and  |
| eval_17 | Resolved | PASS | PASS | FAIL | FAIL | O: "Router faults are the hardware team's area, you'd have to call them on their own number" - tells the customer to call elsewhere. The agent stays polite and  |
| eval_18 | Empathy | PASS | PASS | PASS | FAIL | R: "Honestly, it's not rocket science, most people manage to plug a cable in the right hole" - condescending. Everything else is done properly. |
| eval_18 | Rapport | FAIL | FAIL | PASS | FAIL | R: "Honestly, it's not rocket science, most people manage to plug a cable in the right hole" - condescending. Everything else is done properly. |
| eval_18 | Probing | PASS | PASS | FAIL | FAIL | R: "Honestly, it's not rocket science, most people manage to plug a cable in the right hole" - condescending. Everything else is done properly. |
| eval_18 | Resolved | PASS | PASS | FAIL | FAIL | R: "Honestly, it's not rocket science, most people manage to plug a cable in the right hole" - condescending. Everything else is done properly. |
| eval_19 | Probing | PASS | PASS | PASS | FAIL | B: greeting is "Hi, S-Net, Lily speaking" (not the scripted "Thank you for calling S-Net"). CR: the call ends with the agent assuming the fix worked ("you shoul |
| eval_19 | Resolved | FAIL | FAIL | FAIL | PASS | B: greeting is "Hi, S-Net, Lily speaking" (not the scripted "Thank you for calling S-Net"). CR: the call ends with the agent assuming the fix worked ("you shoul |
| eval_20 | Paraphrasing | FAIL | FAIL | FAIL | PASS | V: no PIN, address or security question (only name and date of birth). PA: the agent never restates the problem. |
| eval_20 | Resolved | PASS | PASS | FAIL | PASS | V: no PIN, address or security question (only name and date of birth). PA: the agent never restates the problem. |
| eval_21 | Empathy | FAIL | FAIL | FAIL | PASS | E: the customer is upset about a missed contract renewal (paying double); the agent never acknowledges her feelings. AL: asks again for the renewal date and the |
| eval_21 | Active listening | FAIL | PASS | PASS | PASS | E: the customer is upset about a missed contract renewal (paying double); the agent never acknowledges her feelings. AL: asks again for the renewal date and the |
| eval_21 | Probing | PASS | PASS | FAIL | FAIL | E: the customer is upset about a missed contract renewal (paying double); the agent never acknowledges her feelings. AL: asks again for the renewal date and the |
| eval_21 | Resolved | PASS | PASS | FAIL | PASS | E: the customer is upset about a missed contract renewal (paying double); the agent never acknowledges her feelings. AL: asks again for the renewal date and the |
| eval_22 | Empathy | PASS | FAIL | FAIL | PASS | PE: the agent never uses the customer's name. O: "Wiring inside your flat isn't really our problem, you'll need to get your landlord to sort that out" - deflect |
| eval_22 | Active listening | PASS | PASS | PASS | FAIL | PE: the agent never uses the customer's name. O: "Wiring inside your flat isn't really our problem, you'll need to get your landlord to sort that out" - deflect |
| eval_22 | Ownership | FAIL | PASS | PASS | PASS | PE: the agent never uses the customer's name. O: "Wiring inside your flat isn't really our problem, you'll need to get your landlord to sort that out" - deflect |
| eval_22 | Rapport | PASS | FAIL | PASS | PASS | PE: the agent never uses the customer's name. O: "Wiring inside your flat isn't really our problem, you'll need to get your landlord to sort that out" - deflect |
| eval_22 | Resolved | FAIL | PASS | FAIL | FAIL | PE: the agent never uses the customer's name. O: "Wiring inside your flat isn't really our problem, you'll need to get your landlord to sort that out" - deflect |
| eval_23 | Rapport | FAIL | PASS | PASS | PASS | H: two unannounced silences of about 50 s and 55 s (customer has to ask if the agent is there). R: "Like I said, it's on the screen in front of you, it's not ha |
| eval_23 | Probing | PASS | PASS | FAIL | PASS | H: two unannounced silences of about 50 s and 55 s (customer has to ask if the agent is there). R: "Like I said, it's on the screen in front of you, it's not ha |
| eval_24 | Paraphrasing | FAIL | FAIL | FAIL | PASS | PA: no restatement of the problem. PR: no diagnostic questions; the agent simply resets the voicemail PIN without asking anything about the problem. The reset d |
| eval_24 | Resolved | PASS | PASS | FAIL | FAIL | PA: no restatement of the problem. PR: no diagnostic questions; the agent simply resets the voicemail PIN without asking anything about the problem. The reset d |
| eval_25 | Empathy | FAIL | FAIL | FAIL | PASS | B: no closing script. E: customer very upset (third missed delivery, took time off); the agent never acknowledges it. CR: the router is not delivered or tested  |
| eval_25 | Probing | PASS | PASS | PASS | FAIL | B: no closing script. E: customer very upset (third missed delivery, took time off); the agent never acknowledges it. CR: the router is not delivered or tested  |
| eval_26 | Paraphrasing | FAIL | FAIL | FAIL | PASS | V: verification only by date of birth. PA: never restates the problem. AL: asks again for the error code and the device after the customer has given both. |
| eval_26 | Active listening | FAIL | PASS | PASS | PASS | V: verification only by date of birth. PA: never restates the problem. AL: asks again for the error code and the device after the customer has given both. |
| eval_26 | Resolved | PASS | PASS | FAIL | PASS | V: verification only by date of birth. PA: never restates the problem. AL: asks again for the error code and the device after the customer has given both. |
| eval_27 | Empathy | PASS | PASS | PASS | FAIL | H: two long unannounced silences (~60 s and ~45 s). O: "That's the porting team, not me. You'll have to wait for them to call you." PR: no questions about the p |
| eval_27 | Ownership | FAIL | PASS | PASS | PASS | H: two long unannounced silences (~60 s and ~45 s). O: "That's the porting team, not me. You'll have to wait for them to call you." PR: no questions about the p |
| eval_28 | Empathy | PASS | FAIL | FAIL | FAIL | PE: never uses the customer's name. R: "We've been over this, I'm not going to keep repeating myself" - dismissive and rude. CR: the call ends without confirmin |
| eval_28 | Rapport | FAIL | FAIL | PASS | PASS | PE: never uses the customer's name. R: "We've been over this, I'm not going to keep repeating myself" - dismissive and rude. CR: the call ends without confirmin |
| eval_28 | Probing | PASS | PASS | PASS | FAIL | PE: never uses the customer's name. R: "We've been over this, I'm not going to keep repeating myself" - dismissive and rude. CR: the call ends without confirmin |
| eval_28 | Resolved | FAIL | PASS | FAIL | FAIL | PE: never uses the customer's name. R: "We've been over this, I'm not going to keep repeating myself" - dismissive and rude. CR: the call ends without confirmin |
| eval_29 | Empathy | FAIL | FAIL | FAIL | PASS | E: customer is angry about being cut off mid-call twice; ignored. PA: no restatement. O: "Calls dropping is down to the mast operator, not S-Net, you'd need to  |
| eval_29 | Paraphrasing | FAIL | FAIL | PASS | PASS | E: customer is angry about being cut off mid-call twice; ignored. PA: no restatement. O: "Calls dropping is down to the mast operator, not S-Net, you'd need to  |
| eval_29 | Ownership | FAIL | PASS | PASS | PASS | E: customer is angry about being cut off mid-call twice; ignored. PA: no restatement. O: "Calls dropping is down to the mast operator, not S-Net, you'd need to  |
| eval_29 | Rapport | PASS | FAIL | PASS | PASS | E: customer is angry about being cut off mid-call twice; ignored. PA: no restatement. O: "Calls dropping is down to the mast operator, not S-Net, you'd need to  |
| eval_29 | Resolved | PASS | PASS | PASS | FAIL | E: customer is angry about being cut off mid-call twice; ignored. PA: no restatement. O: "Calls dropping is down to the mast operator, not S-Net, you'd need to  |
| eval_31 | Empathy | PASS | PASS | FAIL | FAIL | R: "I'd have thought someone your age would know how to use a phone app" - condescending. PA: no restatement. AL: asks again for the app name and when it starte |
| eval_31 | Paraphrasing | FAIL | FAIL | FAIL | PASS | R: "I'd have thought someone your age would know how to use a phone app" - condescending. PA: no restatement. AL: asks again for the app name and when it starte |
| eval_31 | Active listening | FAIL | PASS | PASS | PASS | R: "I'd have thought someone your age would know how to use a phone app" - condescending. PA: no restatement. AL: asks again for the app name and when it starte |
| eval_31 | Rapport | FAIL | PASS | PASS | PASS | R: "I'd have thought someone your age would know how to use a phone app" - condescending. PA: no restatement. AL: asks again for the app name and when it starte |
| eval_31 | Probing | PASS | PASS | PASS | FAIL | R: "I'd have thought someone your age would know how to use a phone app" - condescending. PA: no restatement. AL: asks again for the app name and when it starte |
| eval_31 | Resolved | PASS | PASS | FAIL | PASS | R: "I'd have thought someone your age would know how to use a phone app" - condescending. PA: no restatement. AL: asks again for the app name and when it starte |
| eval_32 | Probing | PASS | PASS | FAIL | FAIL | H: two unannounced silences (~50 s, ~40 s). PE: no name used. E: customer upset about a price rise she wasn't told about; not acknowledged. CR: the price change |
| eval_33 | Empathy | FAIL | FAIL | FAIL | PASS | E: customer angry after three failed attempts, not acknowledged. R: "Calm down, shouting won't make the internet faster." O: "The installer was from a contracto |
| eval_33 | Ownership | FAIL | PASS | PASS | PASS | E: customer angry after three failed attempts, not acknowledged. R: "Calm down, shouting won't make the internet faster." O: "The installer was from a contracto |
| eval_33 | Rapport | FAIL | FAIL | PASS | PASS | E: customer angry after three failed attempts, not acknowledged. R: "Calm down, shouting won't make the internet faster." O: "The installer was from a contracto |
| eval_33 | Resolved | PASS | PASS | FAIL | PASS | E: customer angry after three failed attempts, not acknowledged. R: "Calm down, shouting won't make the internet faster." O: "The installer was from a contracto |
| eval_34 | Paraphrasing | FAIL | PASS | FAIL | PASS | V: verification only by full name; no PIN/address/security question at all. PA: no restatement. PR: no diagnostic questions. CR: a refund "request" is raised; n |
| eval_34 | Resolved | FAIL | FAIL | PASS | FAIL | V: verification only by full name; no PIN/address/security question at all. PA: no restatement. PR: no diagnostic questions. CR: a refund "request" is raised; n |
| eval_35 | Active listening | FAIL | FAIL | PASS | PASS | B: closing is "Cheers, bye" (no scripted close). H: two unannounced silences (~45 s, ~55 s). AL: re-asks which room the box is in and whether it is on wifi, bot |
| eval_35 | Resolved | PASS | PASS | FAIL | FAIL | B: closing is "Cheers, bye" (no scripted close). H: two unannounced silences (~45 s, ~55 s). AL: re-asks which room the box is in and whether it is on wifi, bot |
| eval_36 | Paraphrasing | FAIL | FAIL | FAIL | PASS | E: customer distressed (elderly mother's phone line dead, care alarm offline); not acknowledged. PA: no restatement. O: "Care alarms are nothing to do with us,  |
| eval_36 | Ownership | FAIL | FAIL | PASS | FAIL | E: customer distressed (elderly mother's phone line dead, care alarm offline); not acknowledged. PA: no restatement. O: "Care alarms are nothing to do with us,  |
| eval_36 | Rapport | PASS | FAIL | PASS | PASS | E: customer distressed (elderly mother's phone line dead, care alarm offline); not acknowledged. PA: no restatement. O: "Care alarms are nothing to do with us,  |
| eval_36 | Probing | PASS | PASS | PASS | FAIL | E: customer distressed (elderly mother's phone line dead, care alarm offline); not acknowledged. PA: no restatement. O: "Care alarms are nothing to do with us,  |
| eval_36 | Resolved | FAIL | PASS | FAIL | FAIL | E: customer distressed (elderly mother's phone line dead, care alarm offline); not acknowledged. PA: no restatement. O: "Care alarms are nothing to do with us,  |
| eval_37 | Empathy | PASS | PASS | PASS | FAIL | PE: no name used. R: "Seriously, you could have just read the email we sent" - condescending. PR: no diagnostic questions (the agent knows the answer straight a |
| eval_37 | Rapport | FAIL | FAIL | PASS | PASS | PE: no name used. R: "Seriously, you could have just read the email we sent" - condescending. PR: no diagnostic questions (the agent knows the answer straight a |
| eval_37 | Resolved | PASS | PASS | FAIL | FAIL | PE: no name used. R: "Seriously, you could have just read the email we sent" - condescending. PR: no diagnostic questions (the agent knows the answer straight a |
| eval_38 | Empathy | FAIL | FAIL | FAIL | PASS | V: no PIN/address/security question in the first 4 minutes (the agent asks only for the email). E: customer upset about being double-charged; not acknowledged.  |
| eval_38 | Active listening | FAIL | PASS | PASS | PASS | V: no PIN/address/security question in the first 4 minutes (the agent asks only for the email). E: customer upset about being double-charged; not acknowledged.  |
| eval_38 | Ownership | FAIL | PASS | PASS | PASS | V: no PIN/address/security question in the first 4 minutes (the agent asks only for the email). E: customer upset about being double-charged; not acknowledged.  |
| eval_38 | Rapport | PASS | FAIL | PASS | PASS | V: no PIN/address/security question in the first 4 minutes (the agent asks only for the email). E: customer upset about being double-charged; not acknowledged.  |
| eval_38 | Probing | PASS | PASS | FAIL | FAIL | V: no PIN/address/security question in the first 4 minutes (the agent asks only for the email). E: customer upset about being double-charged; not acknowledged.  |
| eval_38 | Resolved | PASS | PASS | FAIL | FAIL | V: no PIN/address/security question in the first 4 minutes (the agent asks only for the email). E: customer upset about being double-charged; not acknowledged.  |
| eval_39 | Paraphrasing | FAIL | FAIL | FAIL | PASS | B: greeting "S-Net, hello" (no script) and no closing script. H: two unannounced silences (~45 s, ~60 s). E: customer upset; ignored. PA: no restatement. CR: en |
| eval_39 | Probing | PASS | PASS | PASS | FAIL | B: greeting "S-Net, hello" (no script) and no closing script. H: two unannounced silences (~45 s, ~60 s). E: customer upset; ignored. PA: no restatement. CR: en |
| eval_40 | Empathy | PASS | PASS | PASS | FAIL | V: no PIN/address/security question (asks for date of birth only). PE: no name used. R: "Look, I don't have all day." O: "Contract cancellations aren't my job,  |
| eval_40 | Ownership | FAIL | PASS | PASS | PASS | V: no PIN/address/security question (asks for date of birth only). PE: no name used. R: "Look, I don't have all day." O: "Contract cancellations aren't my job,  |
| eval_40 | Rapport | FAIL | FAIL | PASS | PASS | V: no PIN/address/security question (asks for date of birth only). PE: no name used. R: "Look, I don't have all day." O: "Contract cancellations aren't my job,  |
| eval_40 | Resolved | PASS | PASS | FAIL | FAIL | V: no PIN/address/security question (asks for date of birth only). PE: no name used. R: "Look, I don't have all day." O: "Contract cancellations aren't my job,  |
| eval_41 | Dead air | PASS | PASS | PASS | FAIL | Longer call with managed holds. E: customer distressed (no internet for a week, child doing exams); ignored. R: "If you'd listened the first time we wouldn't be |
| eval_41 | Paraphrasing | FAIL | FAIL | FAIL | PASS | Longer call with managed holds. E: customer distressed (no internet for a week, child doing exams); ignored. R: "If you'd listened the first time we wouldn't be |
| eval_41 | Ownership | FAIL | FAIL | PASS | FAIL | Longer call with managed holds. E: customer distressed (no internet for a week, child doing exams); ignored. R: "If you'd listened the first time we wouldn't be |
| eval_41 | Rapport | FAIL | FAIL | PASS | PASS | Longer call with managed holds. E: customer distressed (no internet for a week, child doing exams); ignored. R: "If you'd listened the first time we wouldn't be |
| eval_41 | Probing | PASS | PASS | PASS | FAIL | Longer call with managed holds. E: customer distressed (no internet for a week, child doing exams); ignored. R: "If you'd listened the first time we wouldn't be |
| eval_42 | Empathy | PASS | PASS | PASS | FAIL | B: no scripted greeting or closing. V: no PIN/address/security question. PE: no name used. PA: no restatement. PR: no diagnostic questions. CR: nothing confirme |
| eval_42 | Paraphrasing | FAIL | FAIL | FAIL | PASS | B: no scripted greeting or closing. V: no PIN/address/security question. PE: no name used. PA: no restatement. PR: no diagnostic questions. CR: nothing confirme |
| eval_43 | Ownership | FAIL | FAIL | PASS | FAIL | H: two unannounced silences (~50 s, ~45 s). E: customer upset about a missed refund promise; ignored. R: "I can't help you if you keep interrupting me." O: "Who |
| eval_43 | Rapport | FAIL | FAIL | PASS | PASS | H: two unannounced silences (~50 s, ~45 s). E: customer upset about a missed refund promise; ignored. R: "I can't help you if you keep interrupting me." O: "Who |
| eval_43 | Probing | PASS | PASS | FAIL | FAIL | H: two unannounced silences (~50 s, ~45 s). E: customer upset about a missed refund promise; ignored. R: "I can't help you if you keep interrupting me." O: "Who |
| eval_44 | Empathy | FAIL | FAIL | FAIL | PASS | B: no closing script. PE: no name used. E: upset customer ignored. PA: no restatement. AL: asks again for the account holder and the card ending, both already g |
| eval_44 | Paraphrasing | FAIL | FAIL | FAIL | PASS | B: no closing script. PE: no name used. E: upset customer ignored. PA: no restatement. AL: asks again for the account holder and the card ending, both already g |
| eval_44 | Active listening | FAIL | FAIL | PASS | FAIL | B: no closing script. PE: no name used. E: upset customer ignored. PA: no restatement. AL: asks again for the account holder and the card ending, both already g |
| eval_44 | Probing | FAIL | PASS | FAIL | FAIL | B: no closing script. PE: no name used. E: upset customer ignored. PA: no restatement. AL: asks again for the account holder and the card ending, both already g |
| eval_45 | Empathy | PASS | FAIL | FAIL | FAIL | H: two unannounced silences (~55 s, ~50 s). V: no PIN/address/security question in the first 4 minutes (asked for the PIN only at about 5 minutes). R: "Not ever |
| eval_45 | Paraphrasing | FAIL | PASS | PASS | PASS | H: two unannounced silences (~55 s, ~50 s). V: no PIN/address/security question in the first 4 minutes (asked for the PIN only at about 5 minutes). R: "Not ever |
| eval_45 | Active listening | PASS | FAIL | PASS | PASS | H: two unannounced silences (~55 s, ~50 s). V: no PIN/address/security question in the first 4 minutes (asked for the PIN only at about 5 minutes). R: "Not ever |
| eval_45 | Ownership | FAIL | PASS | PASS | PASS | H: two unannounced silences (~55 s, ~50 s). V: no PIN/address/security question in the first 4 minutes (asked for the PIN only at about 5 minutes). R: "Not ever |
| eval_45 | Rapport | FAIL | PASS | PASS | PASS | H: two unannounced silences (~55 s, ~50 s). V: no PIN/address/security question in the first 4 minutes (asked for the PIN only at about 5 minutes). R: "Not ever |
| eval_45 | Probing | PASS | PASS | FAIL | FAIL | H: two unannounced silences (~55 s, ~50 s). V: no PIN/address/security question in the first 4 minutes (asked for the PIN only at about 5 minutes). R: "Not ever |
| eval_45 | Resolved | FAIL | PASS | PASS | FAIL | H: two unannounced silences (~55 s, ~50 s). V: no PIN/address/security question in the first 4 minutes (asked for the PIN only at about 5 minutes). R: "Not ever |
| eval_46 | Dead air | PASS | PASS | PASS | FAIL | Very poor call with long managed holds (so H and V still pass). B: no scripts. PE: no name. E: distressed customer ignored. R: "I'm not a miracle worker." PA: n |
| eval_46 | Paraphrasing | FAIL | FAIL | PASS | PASS | Very poor call with long managed holds (so H and V still pass). B: no scripts. PE: no name. E: distressed customer ignored. R: "I'm not a miracle worker." PA: n |
| eval_46 | Active listening | FAIL | FAIL | PASS | FAIL | Very poor call with long managed holds (so H and V still pass). B: no scripts. PE: no name. E: distressed customer ignored. R: "I'm not a miracle worker." PA: n |
| eval_46 | Rapport | FAIL | FAIL | PASS | PASS | Very poor call with long managed holds (so H and V still pass). B: no scripts. PE: no name. E: distressed customer ignored. R: "I'm not a miracle worker." PA: n |
| eval_46 | Probing | FAIL | PASS | PASS | FAIL | Very poor call with long managed holds (so H and V still pass). B: no scripts. PE: no name. E: distressed customer ignored. R: "I'm not a miracle worker." PA: n |
| eval_47 | Paraphrasing | FAIL | PASS | PASS | PASS | V: no PIN/address/security question at all. E: angry customer ignored. R: "If you can't work a SIM tray, that's not really my problem." O: "Go back to the shop  |
| eval_47 | Ownership | FAIL | PASS | PASS | PASS | V: no PIN/address/security question at all. E: angry customer ignored. R: "If you can't work a SIM tray, that's not really my problem." O: "Go back to the shop  |
| eval_47 | Rapport | FAIL | FAIL | PASS | PASS | V: no PIN/address/security question at all. E: angry customer ignored. R: "If you can't work a SIM tray, that's not really my problem." O: "Go back to the shop  |
| eval_47 | Resolved | FAIL | PASS | FAIL | FAIL | V: no PIN/address/security question at all. E: angry customer ignored. R: "If you can't work a SIM tray, that's not really my problem." O: "Go back to the shop  |
| eval_48 | Paraphrasing | PASS | PASS | FAIL | PASS | AUTO-FAIL: "Can you just shut up for a second and let me check." R FAIL for the same line. E: customer upset about a broken promise; ignored before the outburst |
| eval_48 | Rapport | FAIL | FAIL | PASS | PASS | AUTO-FAIL: "Can you just shut up for a second and let me check." R FAIL for the same line. E: customer upset about a broken promise; ignored before the outburst |
| eval_48 | Probing | PASS | PASS | PASS | FAIL | AUTO-FAIL: "Can you just shut up for a second and let me check." R FAIL for the same line. E: customer upset about a broken promise; ignored before the outburst |
| eval_48 | Resolved | PASS | PASS | FAIL | PASS | AUTO-FAIL: "Can you just shut up for a second and let me check." R FAIL for the same line. E: customer upset about a broken promise; ignored before the outburst |
| eval_49 | Empathy | PASS | FAIL | FAIL | FAIL | AUTO-FAIL: "Only an idiot would pay a bill twice." R FAIL for the same line. O: "Refunds aren't my department, ring accounts." CR: nothing resolved. |
| eval_49 | Ownership | FAIL | PASS | PASS | PASS | AUTO-FAIL: "Only an idiot would pay a bill twice." R FAIL for the same line. O: "Refunds aren't my department, ring accounts." CR: nothing resolved. |
| eval_49 | Rapport | FAIL | FAIL | PASS | PASS | AUTO-FAIL: "Only an idiot would pay a bill twice." R FAIL for the same line. O: "Refunds aren't my department, ring accounts." CR: nothing resolved. |
| eval_49 | Probing | PASS | PASS | PASS | FAIL | AUTO-FAIL: "Only an idiot would pay a bill twice." R FAIL for the same line. O: "Refunds aren't my department, ring accounts." CR: nothing resolved. |
| eval_50 | Paraphrasing | FAIL | FAIL | PASS | PASS | AUTO-FAIL: "That's a stupid question, obviously it's included." R FAIL for the same line. E: upset customer ignored. PA: no restatement. CR: the roaming bolt-on |
| eval_50 | Rapport | FAIL | FAIL | PASS | FAIL | AUTO-FAIL: "That's a stupid question, obviously it's included." R FAIL for the same line. E: upset customer ignored. PA: no restatement. CR: the roaming bolt-on |
| eval_50 | Probing | PASS | PASS | FAIL | FAIL | AUTO-FAIL: "That's a stupid question, obviously it's included." R FAIL for the same line. E: upset customer ignored. PA: no restatement. CR: the roaming bolt-on |
| eval_50 | Resolved | PASS | PASS | FAIL | FAIL | AUTO-FAIL: "That's a stupid question, obviously it's included." R FAIL for the same line. E: upset customer ignored. PA: no restatement. CR: the roaming bolt-on |
