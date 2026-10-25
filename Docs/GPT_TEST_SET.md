# GPT-1: a test set written by ChatGPT

The fine-tuned model was trained on calls written by Claude and Antigravity, so calls from those authors flatter it. This set is written by **OpenAI ChatGPT**, a style the model has never seen. Each call has a few **planted faults** (or none). The planted faults are the answer key: every planted item should FAIL and every other item should PASS.

These are still AI-written calls with AI-written keys, not human-labelled real calls. Say so when you report the numbers.

## Steps

1. Open a **new ChatGPT chat**. Note the model name (for example GPT-5). Paste the **setup message** below once.
2. For each row of the **call plan**, send the one-line **call message**. ChatGPT answers with one JSON block.
3. Save each answer as `inputs/GPT-1/<file name from the plan>.json`. Start a fresh chat (and paste the setup again) every 8 to 10 calls, before the answers get shorter or sloppier.
4. Check the files (no server needed):
   ```bash
   .venv/bin/python Scripts/score_planted.py check "inputs/GPT-1"
   ```
   Regenerate any call it flags. Skim a few calls yourself: a planted fault ChatGPT forgot to write, or an extra fault it slipped in, makes the key wrong.
5. Start the server (`LAYA_FLOW=v3`, `LAYA_CHECKPOINT=models/final-softce-3`), then grade and score:
   ```bash
   .venv/bin/python Scripts/batch_test.py "inputs/GPT-1" --label v3
   .venv/bin/python Scripts/score_planted.py score "inputs/GPT-1" --label v3 --out "inputs/Test (results)/GPT-1 (v3).md"
   ```

## Setup message (paste once per chat)

````text
You write realistic, synthetic phone-call transcripts for testing an automated call-quality grader. The company is S-Net, a UK broadband, TV and mobile provider. A support agent talks to a customer. Write natural spoken English: fillers, interruptions, people correcting themselves, small talk, uneven turn lengths. Do not make the agent sound like a training script except where told to.

For every call I send you a call number, a file name, the customer's first name, a topic and a list of PLANTED FAULTS. Write the whole call and reply with ONE JSON code block and nothing else.

JSON layout:
{
  "tenant_id": "tenant-abc",
  "customer_name": "<first name and surname, first name as given>",
  "planted_faults": [<the fault codes exactly as given; [] when the list is "none">],
  "fault_notes": "<one or two sentences: where in the call each planted fault happens>",
  "transcript": [
    {"speaker": "Agent", "start_time": "[00:00]", "end_time": "[00:06]", "start_time_sec": 0, "end_time_sec": 6, "text": "..."},
    {"speaker": "Customer", "start_time": "[00:07]", "end_time": "[00:15]", "start_time_sec": 7, "end_time_sec": 15, "text": "...", "sentiment_score": -12.5}
  ]
}

Transcript rules:
- 8 to 15 minutes long, 50 to 100 turns, speakers "Agent" and "Customer" only. The agent speaks first.
- Times are real: each turn starts 1 to 4 seconds after the previous one ends, and a turn lasts about 0.4 seconds per word. The only longer silences are holds and planted dead air (below).
- Only Customer turns carry "sentiment_score", a number from -100 (furious) to +100 (delighted); calm small talk is around -5 to +10, annoyed -15 to -40, angry -40 to -70. Agent turns never carry one.
- Every call has at least one moment where the customer is clearly frustrated or upset.
- Never put swear words or insults in the agent's lines.

A GOOD agent does ALL of the following unless one of them is a planted fault:
- Opening: one of the agent's first lines contains the exact words "Thank you for calling S-Net".
- Closing: one of the agent's last lines contains the exact words "Thank you for choosing S-Net".
- Identity check: within the first two minutes the agent asks for the account PIN, an answer to the security question, or the first line of the address.
- Uses the customer's name at least twice.
- Holds: before any pause longer than 30 seconds the agent announces a hold, and comes back thanking the customer for waiting. No hold lasts more than 2 minutes.
- Empathy: when the customer is upset, the agent acknowledges the feeling in their own words before moving on.
- Paraphrasing: early in the call (first 5 minutes), the agent restates the customer's problem back to them in their own words and checks they have it right.
- Probing: the agent asks several diagnostic questions about the problem before fixing it (when it started, what lights are on, which devices, what has been tried...).
- Ownership: the agent takes responsibility for sorting the issue and never pushes the customer elsewhere.
- Active listening: the agent remembers what the customer already said and never asks for the same information twice.
- Rapport: polite, warm and professional throughout.
- Resolution: near the end the agent explicitly checks with the customer that the problem is now fixed, and the customer confirms it.

PLANTED FAULTS (each code turns ONE behaviour above into a clear failure; everything not listed stays good):
- nogreet: the opening greeting does not say "Thank you for calling S-Net" (e.g. "Hi, S-Net support, Jo speaking").
- noclose: the agent ends without "Thank you for choosing S-Net" (e.g. "Right, cheers, bye").
- noverify: the agent never asks for a PIN, security answer or address at any point (asking only for an account number or email does not count, and is allowed).
- noname: the agent never says the customer's name, not even once.
- gaps: two or more silences of 35 to 90 seconds with no hold announcement and no "thanks for waiting" afterwards (the agent just goes quiet; the customer may say "Hello? Still there?"). Show them only through the timestamps.
- empathy: when the customer is upset, the agent ignores the feeling and goes straight to process, every time.
- nopara: the agent never restates or summarises the customer's problem back to them.
- noprobe: the agent asks no diagnostic questions at all and jumps straight to a generic fix.
- ownership: the agent deflects at least once: blames another team or company, says it is not their job, or tells the customer to call someone else.
- al: the agent asks for information the customer already gave (at least twice in the call, e.g. asks again which room the router is in), and the customer has to repeat themselves.
- noconfirm: the agent never checks whether the problem is fixed; the call just ends after the fix is applied or scheduled.
- rapport: the agent is rude, sarcastic, impatient or condescending in at least one line (no swearing, no insults like "stupid" or "idiot").

Make each planted fault clear and unmistakable, as a human QA reviewer would mark it, but written naturally. Do not mention the fault codes or the grading anywhere in the transcript text.
````

## Call message (one per call)

```text
Call <NN>. File: <file name>. Customer first name: <name>. Topic: <topic>. PLANTED FAULTS: <faults>.
```

Example: `Call 08. File: gpt_08_noverify. Customer first name: Tomasz. Topic: router keeps rebooting at night. PLANTED FAULTS: noverify.`

## Call plan (20 calls)

| # | File name | Name | Topic | Planted faults |
|---|---|---|---|---|
| 01 | gpt_01_clean | Hannah | broadband drops every evening | none |
| 02 | gpt_02_clean | Kwame | TV box frozen on boot screen | none |
| 03 | gpt_03_clean | Priya | overcharged on last bill | none |
| 04 | gpt_04_clean | Callum | new mobile SIM not activating | none |
| 05 | gpt_05_clean | Fatima | Wi-Fi slow upstairs | none |
| 06 | gpt_06_nogreet | Oliver | email account locked | nogreet |
| 07 | gpt_07_noclose | Mei | moving house, transfer service | noclose |
| 08 | gpt_08_noverify | Tomasz | router keeps rebooting at night | noverify |
| 09 | gpt_09_noname | Grace | engineer missed appointment | noname |
| 10 | gpt_10_gaps | Ibrahim | landline crackling | gaps |
| 11 | gpt_11_empathy | Chloe | broadband down for three days, working from home | empathy |
| 12 | gpt_12_nopara | Daniel | TV channels missing after update | nopara |
| 13 | gpt_13_noprobe | Aisha | intermittent Wi-Fi on laptop only | noprobe |
| 14 | gpt_14_ownership | George | streaming app buffering | ownership |
| 15 | gpt_15_al | Sofia | mobile data not working abroad | al |
| 16 | gpt_16_noconfirm | Ravi | parental controls not applying | noconfirm |
| 17 | gpt_17_rapport | Emily | repeated calls about same fault | rapport |
| 18 | gpt_18_empathy_noconfirm | Molly | outage during child's online exam | empathy, noconfirm |
| 19 | gpt_19_noprobe_ownership | Kofi | speeds far below what was promised | noprobe, ownership |
| 20 | gpt_20_nopara_al_rapport | Eleanor | can't log into the S-Net app | nopara, al, rapport |

Five calls are fully good. Each rule check (greeting, closing, verification, name, dead air) is planted once and each model check twice, and every call keeps most items good, so false alarms (a PASS item graded FAIL) are measured as well as misses.
