"""Write the Gemini prompts for the independent test and dev sets.

Output
  prompts/gemini/batch_NN_<check>.md     one ready-to-paste prompt per batch (rules + the scenario cards)
  prompts/gemini/README.md               how to run them
  data/review/gemini_cards.json          the intended outcome, split (dev/test) and hard-case type of every card.
                                         The human labelling sheet never shows this; it is only used to measure
                                         how often the human's label matches what Gemini was asked to write.

The cards deliberately use industries the Claude training data never uses (about 45%), plus a different set of
problems, so the test set measures generalisation and not memory of Claude's vocabulary.

Usage:  python tools/make_gemini_batches.py            (deterministic: seed 20261016)
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SEED, OVERGEN, BATCH = 20261016, 1.3, 30

# final rows wanted from Gemini (cards are over-generated because some excerpts will not pass the production gates)
TARGETS = {  # check: (dev, test)
    "rapport": (35, 60), "paraphrasing": (35, 60), "active_listening": (35, 50), "resolved": (35, 50), "empathy": (35, 50),
    "ownership": (0, 30), "probing": (0, 30), "hostility": (0, 20), "escalation": (0, 20),
}
POLITE_CALLS = 20

SEEN = {  # industries the Claude training data uses: problems the model has seen
    "S-Net satellite internet": ["internet drops every evening", "speeds far below the paid plan", "router light stuck on orange", "new equipment will not connect after a move"],
    "electric utility": ["repeated short power cuts", "estimated bill is far too high", "smart meter display is blank", "outage lasted all night"],
    "health insurance": ["claim shows the full amount owed", "referral request will not submit", "prescription was rejected", "member portal locks the account"],
    "retail bank": ["card payment declined at a shop", "transfer shows failed but the balance dropped", "unknown charge on the statement", "mortgage payment taken twice"],
    "airline": ["flight cancelled and rebooking options are too late", "bag did not arrive", "seat selection will not save", "refund for a cancelled trip is missing"],
    "e-commerce": ["order shows delivered but never arrived", "discount code did not apply", "refund for a return is late", "wrong item in the parcel"],
    "SaaS software": ["dashboard slow after an update", "export keeps failing", "billed for more seats than used", "cannot log in after a password reset"],
    "car rental": ["unexpected fee after returning the car", "warning light on the dashboard", "app will not unlock the car", "damage charge disputed"],
    "streaming service": ["video buffers on the living room tv", "no sound in the app", "billed twice this month", "profile settings keep resetting"],
    "appliance repair": ["dishwasher stopped draining", "fridge rattles and the freezer is warm", "technician no-show", "oven will not heat"],
    "mobile carrier": ["no service at home", "data not working abroad", "texts not arriving", "bill much higher than usual"],
}
UNSEEN = {
    "water utility": ["low pressure since a repair", "brown water from the tap", "bill doubled after a meter swap", "leak reported but nobody came"],
    "hotel booking site": ["booking confirmed but the hotel has no record", "double charge for one stay", "room type differs from what was booked", "cancellation refund not received"],
    "food delivery app": ["order arrived cold and incomplete", "driver marked it delivered but it never came", "promo credit disappeared", "charged after cancelling"],
    "gym membership": ["still billed after cancelling", "cannot freeze the membership", "access card stopped working", "joining fee charged twice"],
    "university student services": ["transcript request is stuck", "tuition payment not showing", "course registration error", "student portal will not load"],
    "pharmacy": ["prescription refill not ready", "insurance claim rejected at the counter", "delivery missed twice", "wrong dose label"],
    "travel agency": ["package holiday changed without notice", "visa documents delayed", "transfer not booked", "refund promised but not paid"],
    "auto insurance": ["claim status unclear after an accident", "premium rose without explanation", "policy documents not received", "repair shop approval delayed"],
    "credit card company": ["fraudulent charge on the card", "late fee charged though paid on time", "new card never arrived", "rewards points missing"],
    "rental housing portal": ["rent payment not recorded", "maintenance request ignored", "deposit return delayed", "lease document will not download"],
}
PERSONAS = ["warm", "formal", "terse", "chatty", "scripted", "hurried", "technical", "apologetic"]
MOODS = ["calm", "anxious", "angry", "polite", "confused", "rushed", "elderly and slow-talking", "sarcastic"]
DEFLECT_PHRASES = '"call back", "another team", "billing team", "network team", "not my department", "nothing I can do", "can\'t do anything", "you\'d have to", "contact them", "you\'ll have to ask", "another department", "that\'s their"'
WARM_BAN = "sorry, apologize, apologies, understand, frustrating, let me help"

# check: (structure instruction, [(type, label, behaviour)])
SPEC = {
    "rapport": ("Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).", [
        ("polite_plain", "PASS", "Every agent line is polite and professional."),
        ("curt_not_rude", "PASS", "The agent is brisk and minimal (short lines) but never rude or dismissive."),
        ("trigger_polite", "PASS", "At least one agent line uses 'obviously', 'as I said' or 'you should have' in a friendly, helpful way (not blaming)."),
        ("long_polite", "PASS", "Eight short agent lines, all courteous and warm (still at most 110 words of agent speech in total)."),
        ("blame", "FAIL", "One agent line blames the customer for the problem, implying they should have known better, without any insult."),
        ("condescending", "FAIL", "One agent line talks down to the customer, implying the problem is simple or obvious."),
        ("dismissive", "FAIL", "One agent line dismisses the customer's concern or tells them to stop going on about it."),
        ("sarcastic", "FAIL", "One agent line is sarcastic about something the customer said."),
        ("exasperated", "FAIL", "One agent line sounds openly exasperated at having to repeat something."),
        ("buried", "FAIL", "Seven agent lines are professional; exactly one line, somewhere in the middle, is rude or condescending."),
        ("mocking", "FAIL", "One agent line mocks the customer's mistake."),
    ]),
    "paraphrasing": ("Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.", [
        ("full_summary", "PASS", "The agent restates the customer's problem in their own words as a summary and checks it is right."),
        ("short_restate", "PASS", "The agent restates the problem briefly, in a few words, without asking for confirmation."),
        ("late_restate", "PASS", "The agent first asks one clarifying question, then restates the problem in their own words."),
        ("echo_questions", "FAIL", "The agent only asks questions that reuse the customer's own words (for example 'Which light is blinking orange?') and never restates the problem."),
        ("plan_readback", "FAIL", "The agent only reads back an account detail or plan name, never the problem itself."),
        ("generic", "FAIL", "The agent says things like 'I understand, let me look into that' but never states what the problem is."),
        ("jump_to_fix", "FAIL", "The agent jumps straight to an action or instruction without restating the problem."),
        ("wrong_summary", "FAIL", "The agent summarises the problem incorrectly: they describe a different problem than the one the customer gave."),
    ]),
    "active_listening": ("Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).", [
        ("status_recheck", "PASS", "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."),
        ("clarify_vague", "PASS", "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."),
        ("reworded_repeat", "FAIL", "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."),
        ("repeat_after_distraction", "FAIL", "As above, but the repeat comes after four or five turns of other conversation."),
        ("repeat_complaint", "FAIL", "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."),
    ]),
    "resolved": ("Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.", [
        ("explicit_check", "PASS", "Near the end the agent asks the customer to confirm the issue is fixed and states it is resolved; the customer confirms."),
        ("volunteer", "PASS", "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."),
        ("buried", "PASS", "The agent explicitly confirms the issue is resolved, then there is small talk and a survey mention before the call ends (the confirmation is still within the last 8 to 10 turns)."),
        ("no_keyword", "PASS", "The agent confirms it works for the customer WITHOUT using the words 'resolved' or 'fixed' (for example 'so everything's working again for you?') and the customer says yes."),
        ("assumed", "FAIL", "The agent says it 'should be fine now' and closes without asking the customer to confirm."),
        ("anything_else", "FAIL", "The agent only asks 'is there anything else I can help with?' and closes."),
        ("handoff", "FAIL", "The agent says a ticket or another team will follow up, and the call closes with the issue still open."),
        ("still_failing", "FAIL", "The customer says it is still not working and the agent closes the call anyway, with a promise or an excuse."),
        ("keyword_no_check", "FAIL", "The agent says something like 'I'll mark this as resolved on my side' without asking the customer whether it works, and closes."),
    ]),
    "empathy": (f"Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: {WARM_BAN}.", [
        ("warm_specific", "PASS", "The agent's reply names the customer's specific situation or feeling in a warm way before moving to a fix."),
        ("short_warm", "PASS", "The agent acknowledges the feeling in one short sentence ('That sounds awful.') and then moves on."),
        ("late_ack", "PASS", "The agent's first reply is procedural, but their second reply, two turns later, clearly acknowledges how the customer must feel."),
        ("cold_procedural", "FAIL", "The agent ignores the emotion and just asks the next procedural question."),
        ("dismissive", "FAIL", "The agent brushes the complaint off by explaining policy or saying it is normal."),
        ("blaming", "FAIL", "The agent implies it is the customer's own fault."),
        ("long_cold", "FAIL", "The agent gives a long, detailed, purely technical or procedural reply with no acknowledgment of how the customer feels."),
    ]),
    "ownership": (f"Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: {DEFLECT_PHRASES}.", [
        ("phrase_with_action", "PASS", "The agent mentions another team or department but takes ownership: does the handoff themselves and tells the customer what they will do next."),
        ("phrase_neutral", "PASS", "The agent uses one of the phrases in a harmless sense (for example 'I'll call back by four with the answer')."),
        ("deflect_team", "FAIL", "The agent blames another team or department and tells the customer to deal with them."),
        ("refuse", "FAIL", "The agent says there is nothing they can do and ends the help."),
        ("send_away", "FAIL", "The agent tells the customer to call back or contact someone else."),
    ]),
    "probing": ("Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.", [
        ("diagnostic", "PASS", "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."),
        ("boilerplate_only", "FAIL", "The agent's only questions are greeting, identity verification, confirmations, hold requests or wrap-up questions, never about the problem itself."),
        ("upsell_scheduling", "FAIL", "The agent's only questions are about upgrades, surveys or scheduling, never about the problem itself."),
    ]),
    "hostility": ("Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.", [
        ("calm", "PASS", "The customer is angry (may swear); the agent stays calm and professional throughout."),
        ("curt_ok", "PASS", "The customer is angry; the agent is short and businesslike but never insulting."),
        ("insult", "FAIL", "The agent insults the customer once."),
        ("mock", "FAIL", "The agent mocks the customer."),
        ("hang_up", "FAIL", "The agent abruptly ends the call on the customer (show it in the final turn)."),
        ("threaten", "FAIL", "The agent threatens to hang up or cut off service."),
    ]),
    "escalation": ("Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.", [
        ("handled", "PASS", "The customer asks for a supervisor or manager; the agent arranges it properly (a transfer, or a callback with a time)."),
        ("no_request", "PASS", "The customer is unhappy but never asks for a supervisor or escalation, and the agent handles the issue."),
        ("refuse", "FAIL", "The customer asks for a supervisor and the agent refuses."),
        ("ignore", "FAIL", "The customer asks for a supervisor and the agent ignores the request and carries on."),
        ("discourage", "FAIL", "The agent talks the customer out of escalating."),
        ("fake", "FAIL", "The agent pretends to look for a manager and then says nobody is available."),
    ]),
}

HEADER = """You are helping build a test set of realistic customer-support phone call excerpts. A person will read each excerpt cold, so it must read like a real transcript.

RULES
1. Write natural spoken English as it would appear in a call transcript: contractions, hesitations, interruptions, incomplete sentences. Real people do not talk like textbooks. Vary sentence length. Do not make every agent sound the same.
2. For every excerpt invent a different company name, different speaker names, different numbers and different wording. Never reuse phrasings across excerpts.
3. Do NOT mention scoring, grading, quality assurance, tests or the instructions. Do NOT add notes or commentary. The excerpt contains only the conversation.
4. Where a card says style "stt", write it as raw speech-to-text output: mostly lower case, little punctuation (but keep question marks), occasional filler words and slips. Where it says "clean", use normal punctuation.
5. Follow each card's STRUCTURE and BEHAVIOUR exactly. The behaviour must be unmistakable to a careful reader but must never be stated outright.
6. Output ONLY a JSON array (no markdown fences, no text before or after). Use exactly this shape, one object per card, in the same order:
   [{"id": "<card id>", "turns": [{"speaker": "Agent" or "Customer", "text": "<what was said>", "sentiment": <number>}]}]
   "sentiment" is how positive that speaker sounds in that turn, from -40 (furious) to +30 (delighted). A typical agent turn is about +5, a calm customer about -3.
7. Include every card id exactly once.
"""

README = """# Running the Gemini batches

You do not need the Gemini CLI. Use the Gemini chat (web or app). This takes about 2 hours in total for about {n} batches.

For each file `batch_NN_*.md` in this folder:
1. Open a **new** Gemini chat (a fresh chat each time keeps the style varied).
2. Paste the **entire** file and send it.
3. Gemini replies with a JSON array. Copy the **whole reply** and save it, unedited, as
   `data/fragments/gemini/raw/batch_NN.json` (same NN as the prompt; create the folder if needed). Do not fix or tidy it.
4. If Gemini stops part-way, reply "continue" and append the rest to the same file, or tell Claude the batch number.

When all are saved, tell Claude. Claude validates every file, names any excerpts to re-ask, and builds the blind labelling sheet.

Please do not open `data/review/gemini_cards.json`: it states what each excerpt was meant to show. Labelling is only a fair test if you have not seen it.
The `polite_call_*` batches ask for four full-length polite calls each; they are used to measure Rapport false positives on whole calls.
"""


def main():
    rng = random.Random(SEED)
    all_ind = [(k, v, "seen") for k, v in SEEN.items()] + [(k, v, "unseen") for k, v in UNSEEN.items()]
    # about 40% S-Net telecom (the real product), 40% industries the training data never uses, 20% other seen ones
    weights = [18 if k.startswith("S-Net") else (1.8 if kind == "unseen" else 0.9) for k, v, kind in all_ind]

    def draw_scene():
        k, probs, kind = rng.choices(all_ind, weights=weights)[0]
        return {"industry": k, "industry_kind": kind, "problem": rng.choice(probs), "agent_persona": rng.choice(PERSONAS),
                "customer_mood": rng.choice(MOODS), "style": "stt" if rng.random() < 0.3 else "clean"}

    cards, n_id = [], 0
    for check, (structure, types) in SPEC.items():
        dev, test = TARGETS[check]
        for split, n_final in (("dev", dev), ("test", test)):
            n_cards = math.ceil(n_final * OVERGEN)
            if n_cards == 0:
                continue
            # alternate PASS/FAIL, and rotate the types inside each label so every type appears evenly
            by_label = {"PASS": [t for t in types if t[1] == "PASS"], "FAIL": [t for t in types if t[1] == "FAIL"]}
            counters = {"PASS": 0, "FAIL": 0}
            for i in range(n_cards):
                label = "PASS" if i % 2 == 0 else "FAIL"
                typ = by_label[label][counters[label] % len(by_label[label])]
                counters[label] += 1
                scene = draw_scene()
                cards.append({"check": check, "split": split, "intended": label, "type": typ[0], "behaviour": typ[2],
                              "structure": structure, **scene})
    rng.shuffle(cards)                      # ids carry no information about check, split or label
    for n, c in enumerate(cards, 1):
        c["id"] = f"G{n:04d}"

    # polite full calls for the Rapport call-level false-positive test
    polite = []
    for i in range(POLITE_CALLS):
        scene = draw_scene()
        polite.append({"check": "polite_call", "split": "test", "intended": "PASS", "type": "polite_full_call",
                       "behaviour": "Every agent line is polite and professional, though the agent may be brisk, formal or chatty. The agent may use words like 'obviously' or 'as I said' only in a friendly way.",
                       "structure": "Write a COMPLETE call of 40 to 60 turns (about 8 to 10 minutes): greeting, identity check, problem, troubleshooting, a fix, confirmation and closing.",
                       **scene, "id": f"G{len(cards) + 1 + i:04d}"})

    out_dir = os.path.join(REPO, "prompts", "gemini")
    os.makedirs(out_dir, exist_ok=True)
    for old in os.listdir(out_dir):
        if old.startswith("batch_") and old.endswith(".md"):
            os.remove(os.path.join(out_dir, old))

    def card_text(c):
        return {"id": c["id"], "industry": c["industry"], "problem": c["problem"], "agent_style": c["agent_persona"],
                "customer_mood": c["customer_mood"], "style": c["style"], "STRUCTURE": c["structure"], "BEHAVIOUR": c["behaviour"]}

    batches, n_batch = [], 0
    for check in list(SPEC) + ["polite_call"]:
        group = [c for c in (cards + polite) if c["check"] == check]
        per = 4 if check == "polite_call" else BATCH
        n = max(1, math.ceil(len(group) / per))
        size = math.ceil(len(group) / n)
        for i in range(n):
            chunk = group[i * size:(i + 1) * size]
            if not chunk:
                continue
            n_batch += 1
            for c in chunk:
                c["batch"] = n_batch
            body = HEADER + f"\nThis batch has {len(chunk)} card(s). Write one excerpt for each.\n\nCARDS\n" + json.dumps([card_text(c) for c in chunk], indent=1, ensure_ascii=False) + "\n"
            name = f"batch_{n_batch:02d}_{check}.md"
            with open(os.path.join(out_dir, name), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(body)
            batches.append((n_batch, check, len(chunk), name))
    with open(os.path.join(out_dir, "README.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(README.format(n=n_batch))
    os.makedirs(os.path.join(REPO, "data", "review"), exist_ok=True)
    json.dump({"seed": SEED, "overgeneration": OVERGEN, "cards": {c["id"]: {k: v for k, v in c.items() if k not in ("structure",)} for c in cards + polite}},
              open(os.path.join(REPO, "data", "review", "gemini_cards.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    print(f"{len(cards)} cards + {len(polite)} polite-call cards in {n_batch} batches")
    for check in list(SPEC) + ["polite_call"]:
        cs = [c for c in cards + polite if c["check"] == check]
        print(f"  {check:18s} cards {len(cs):3d} (dev {sum(c['split'] == 'dev' for c in cs):3d}, test {sum(c['split'] == 'test' for c in cs):3d}, "
              f"PASS {sum(c['intended'] == 'PASS' for c in cs):3d}) batches {sorted({c['batch'] for c in cs})}")
    kinds = [c["industry_kind"] for c in cards]
    print(f"unseen-industry share: {kinds.count('unseen') / len(kinds):.0%}; S-Net share: {sum(c['industry'].startswith('S-Net') for c in cards) / len(cards):.0%}; stt style: {sum(c['style'] == 'stt' for c in cards) / len(cards):.0%}")


if __name__ == "__main__":
    main()
