# Labelling guide

Version 1, 2026-10-16. Applies to every labelled item in this project: the training data Claude writes, the pilot you skim, and the independent Gemini test set you label. It matches the frozen questions (`qa-analysis` tag `laya-inputs-frozen-v1`). If a definition here changes after data is generated, the affected data is regenerated.

## The rules that apply to every check
1. **Label what the app should grade, on the text shown.** The model only ever sees a short snippet, not the whole call. Judge the snippet in front of you, not what might have happened elsewhere in the call.
2. **The label is the criterion's outcome: PASS or FAIL.** Not yes/no. (Internally, for some checks "yes" means FAIL; ignore that.)
3. **Quote the line.** For FAIL on Rapport, Ownership and Hostility, you should be able to point at the exact line.
4. **Tone beats words.** A listed trigger word ("obviously", "as I said", "call back") is neither proof of FAIL nor of PASS. Read the line in context.
5. **UNSURE is allowed.** Use it when a reasonable person could go either way, and write one line saying why. UNSURE items are left out of training and scoring. If more than 10% of a check's items are UNSURE, this guide is wrong for that check and we fix it.
6. **Don't reward length or politeness alone.** A long, friendly agent can still fail (Probing, Resolved, Paraphrasing). A curt agent can still pass (Rapport) if nothing is rude.

Open requirement question (not decided): should *Active listening* also fail an agent who **ignores something the customer already said** (e.g. "you should have restarted it" after the customer said they did)? **Default used here: no, only re-asked questions fail**, because that is what the app's check and its question say. If you decide otherwise, only the Active-listening section changes.

---

## 1. Empathy and acknowledgment (Empathy)
**Laya sees:** an upset customer turn plus the next 4 turns. **Question:** does the agent acknowledge the customer's frustration with empathy?

- **PASS:** in the snippet the agent names or reflects the feeling or the situation ("that sounds stressful", "three drops in a week is awful"), or gives a real apology for the problem ("I'm sorry to hear that"), even briefly, before or while moving to a fix.
- **FAIL:** the agent ignores the upset statement and goes straight to procedure, brushes it off, answers coldly, or is dismissive.
- **Not enough for PASS:** a pure procedural next step ("Okay. Can you do it one more time?").

| Snippet (shortened) | Label | Why |
|---|---|---|
| Customer: This is the third time this week my connection died during a client call. / Agent: Three drops in a week during client calls is really stressful, and I'm sorry. Let's fix it now. | PASS | names the situation and apologises |
| Customer: Honestly this has been a nightmare, I've lost four days of work. / Agent: Okay. I'm looking at the move order now. | FAIL | ignores the feeling entirely |
| Customer: I'm furious, nobody has called me back. / Agent: Oh no, I'm sorry about that, that's not the service we want to give you. | PASS | short but genuine |
| Customer: I've been on hold forever, this is ridiculous. / Agent: Can I have your account number? | FAIL | procedural, no acknowledgment |
| Customer: It keeps dropping and I'm about to cancel. / Agent: I hear you. I can see three drops in the logs this week. Let me look at the cause. | PASS | acknowledges, uses evidence |
| Customer: Why does this keep happening? I'm fed up. / Agent: You should have called earlier. | FAIL | dismissive and blaming |

**Hard-case pairs to cover:** same upset line with a warm vs a cold reply; a generic "sorry for the inconvenience" with no reference to the problem (label **PASS** only if it follows an upset statement and is real; a script read after an empty reply is UNSURE); acknowledgment that comes in the 3rd or 4th turn instead of the 1st (PASS).

## 2. Build rapport and professionalism (Rapport)
**Laya sees:** a chunk of up to 8 consecutive agent lines. **Question:** is any agent line rude, condescending, dismissive, sarcastic or unprofessional toward the customer?

- **FAIL:** at least one line talks down to the customer, blames them ("you should have...", "that's basic stuff", "it's not difficult"), dismisses them ("whatever", "not my problem"), mocks them, or is unprofessional. **No insult is needed.**
- **PASS:** every line is polite, neutral or professional. Curt, flat or hurried is still PASS if nothing is rude.

| Chunk (shortened) | Label | Why |
|---|---|---|
| Agent: Let me check that for you. / Agent: Thanks for your patience, Sarah. | PASS | |
| Agent: You should have restarted the router before you called, that's the first thing anyone should do. | FAIL | blames and talks down |
| Agent: Obviously I want to get this fixed for you today, so let me check the line. | PASS | "obviously" used warmly, not as a put-down |
| Agent: Okay. / Agent: Next. / Agent: Do that and call back. | PASS | curt, but not rude (a Rapport pass can still be a poor call) |
| Agent: That's basic stuff. It's not difficult. | FAIL | condescending |
| Agent: As I said earlier, the technician comes between 8 and 12. | PASS | repeating information is not rude |
| Agent: As I said, twice already, the technician comes between 8 and 12. | FAIL | exasperated, scolding |

**Hard-case pairs to cover:** the same trigger words ("obviously", "as I said", "you should have") used politely vs used to belittle; a rude line hidden among 6 polite ones; sarcasm with a smiley tone ("Wow, great idea, restarting it").

## 3. Paraphrasing
**Laya sees:** the customer's problem (first about 50 words, account-detail turns skipped) and the agent's first non-greeting lines. **Question:** does the agent restate the customer's problem back to them?

- **PASS:** the agent says the problem in their own words, as a summary or a check ("So the connection drops every evening around eight and the router goes orange, is that right?"). A shorter restatement that still conveys the problem counts.
- **FAIL:** the agent only asks questions, **even ones that reuse the customer's words** ("Which light is blinking orange?"); reads back only a plan name or number; or never restates the problem.

| Snippet (shortened) | Label | Why |
|---|---|---|
| CUSTOMER: My internet drops every evening at eight, router light turns orange. / AGENT: So it drops each evening around eight and the router goes orange, is that right? | PASS | restates |
| (same customer) / AGENT: Which light is blinking orange? What time does it start? | FAIL | echoes words as questions, no restatement |
| (same customer) / AGENT: Got it, the evening drops. Let me pull up the line. | PASS | short but restates the core problem |
| (same customer) / AGENT: Okay, I see you're on the 500 plan. Can you restart it? | FAIL | no restatement of the problem |
| CUSTOMER: I moved Saturday and the modem blinks orange, four days now. / AGENT: So since the move four days ago the modem won't connect and blinks orange. | PASS | |

**Hard-case pairs to cover:** restate vs echo with the *same* words; restatement that is wrong or adds invented details (label FAIL, it is not a faithful restatement); a restatement after several questions (still PASS if it is within the agent's first lines).

## 4. Probing
**Laya sees:** the customer problem and the agent's question sentences (greetings, identity checks, confirmations and wrap-ups already removed). **Question:** did the agent ask at least one genuine diagnostic question about the problem?

- **PASS:** at least one question that investigates the cause or the specifics: when it started, which device, what error or lights, what was already tried, wired vs wifi.
- **FAIL:** only greetings, identity checks, confirmations ("is that right?"), upsell, scheduling, closing questions, or the opening "what's the issue?" alone.

| Questions asked | Label |
|---|---|
| - Which lights on the router change colour when it drops? - Does it happen on every device? | PASS |
| - Is there anything else I can help with today? - Would you like a short survey? | FAIL |
| - What's going on with the service today? | FAIL |
| - How long has this been happening? | PASS |
| - Can I put you on hold? - Is the account in your name? | FAIL |

**Hard-case pairs to cover:** one real diagnostic question buried among five boilerplate ones (PASS); "have you tried restarting?" alone (PASS, it is diagnostic); sales questions that sound technical ("would you like to upgrade to a faster plan?" is FAIL).

## 5. Took ownership
**Laya sees:** agent lines containing a deflection phrase ("call back", "another team", "not my department"...). **Question:** does the agent deflect, blame another team, or refuse to help?

- **FAIL:** a line that blames another department, deflects responsibility, tells the customer to contact or call back someone else, or refuses to help.
- **PASS:** the phrase appears but the agent keeps ownership: hands off *with* action ("I'll open the ticket with them myself so you don't have to call back"), or a legitimate sales/transfer route offered while still helping.

| Lines | Label |
|---|---|
| Agent: That's not my department, you'd have to call the billing team back tomorrow. | FAIL |
| Agent: That sits with another team's system, but I'll open the ticket with them myself so you don't have to call back. | PASS |
| Agent: I can't do anything about that. | FAIL |
| Agent: Normally the provisioning team picks these up, but I can push it through from here, so I'm doing that now. | PASS |
| Agent: That's a billing team thing. You'd have to call back and ask them. | FAIL |

**Hard-case pairs to cover:** "call back" meaning "I will call you back" (PASS) vs "you call back" (FAIL); naming another team while acting (PASS) vs naming it to end the conversation (FAIL).

## 6. Active listening
**Laya sees:** a pair of agent questions with the customer's answer to the first. **Question:** does the second question ask again for information the customer already gave in their answer?

- **FAIL:** the second question asks for information the customer already gave, in the same or different words.
- **PASS:** the second question asks for something new, **or re-checks something that can have changed** ("what is the light doing now?" after a restart), or clarifies a vague or incomplete answer.

| Pair | Label | Why |
|---|---|---|
| Q1: What colour is the light on the modem? / A: It's red. / Q2: Can you tell me the colour of the light on the modem? | FAIL | same information, reworded |
| Q1: What colour is the light on the modem? / A: It's red. / Q2: What is the light doing now after the restart? | PASS | status re-check |
| Q1: How long has this been happening? / A: About three weeks. / Q2: And how long has this been happening for, roughly? | FAIL | already answered |
| Q1: Does it happen on wired devices? / A: Only on wifi. / Q2: Does it happen on your phone as well? | PASS | new information |
| Q1: Which room is the router in? / A: The living room. / Q2: Which one, did you say? | UNSURE | could be a genuine mishear |

**Hard-case pairs to cover:** reworded repeat vs status re-check with similar words; repeat after a long gap (the customer's answer is far back); re-asking something the customer answered only partially (PASS if it asks for the missing part).

## 7. Confirmed the issue is resolved
**Laya sees:** the last 10 lines of the call. **Question:** did the agent explicitly confirm the issue was resolved?

- **PASS:** before closing, the agent checks with the customer and states that it is fixed or resolved, and the customer confirms ("So the internet issue is fully resolved on your end?" / "Yes, completely.").
- **FAIL:** the call just ends; the agent assumes it is fixed ("it should be fine now"); only "is there anything else?"; the customer says it still fails; or the case is handed off or ticketed instead.

| Last lines (shortened) | Label |
|---|---|
| Agent: So the issue is fully resolved on your end? / Customer: Yes, completely. / Agent: Great, anything else? / Customer: No. | PASS |
| Agent: I've reset the line, it should be fine now. / Customer: I'll see how it goes. / Agent: Thanks for calling. | FAIL |
| Customer: It's working now! / Agent: Wonderful, so that's resolved. Anything else? / Customer: No, thanks. | PASS |
| Agent: I've raised a ticket, someone will call you. / Customer: Fine. | FAIL |
| Customer: It's still blinking orange. / Agent: Okay, I'll escalate. | FAIL |

**Hard-case pairs to cover:** explicit check vs "anything else?" only; confirmation 8 lines before the end buried under small talk and a survey (still PASS if within the last 10 lines); the customer volunteers it works but the agent never says it.

## 8. Hostility (regression check)
**Laya sees:** the whole call. **Question:** is the agent hostile, abusive, insulting, threatening, mocking, or does the agent hang up on the customer?
- **FAIL:** any such line from the **agent**. **PASS:** the agent stays professional, **even if the customer is angry or swears**. A customer's abuse never fails the agent.

## 9. Escalation (regression check)
**Laya sees:** the whole call. **Question:** did the customer ask for a supervisor, manager or escalation that the agent refused, ignored, discouraged or faked?
- **FAIL:** the customer asked and the agent refused, ignored, talked them out of it, or pretended to transfer. **PASS:** the customer never asked, or the request was handled properly (transfer made, callback scheduled with a time).

---

## How labels are stored
One row per item: `item_id`, `check`, the snippet exactly as Laya sees it, `label` (PASS / FAIL / UNSURE), a one-line `note` when UNSURE. Gemini items are labelled blind: the file contains no intended label. Claude's intended label is stored separately and used only to measure agreement.
