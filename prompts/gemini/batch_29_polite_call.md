You are helping build a test set of realistic customer-support phone call excerpts. A person will read each excerpt cold, so it must read like a real transcript.

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

This batch has 4 card(s). Write one excerpt for each.

CARDS
[
 {
  "id": "G0712",
  "industry": "travel agency",
  "problem": "transfer not booked",
  "agent_style": "apologetic",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE call of 40 to 60 turns (about 8 to 10 minutes): greeting, identity check, problem, troubleshooting, a fix, confirmation and closing.",
  "BEHAVIOUR": "Every agent line is polite and professional, though the agent may be brisk, formal or chatty. The agent may use words like 'obviously' or 'as I said' only in a friendly way."
 },
 {
  "id": "G0713",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "scripted",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE call of 40 to 60 turns (about 8 to 10 minutes): greeting, identity check, problem, troubleshooting, a fix, confirmation and closing.",
  "BEHAVIOUR": "Every agent line is polite and professional, though the agent may be brisk, formal or chatty. The agent may use words like 'obviously' or 'as I said' only in a friendly way."
 },
 {
  "id": "G0714",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE call of 40 to 60 turns (about 8 to 10 minutes): greeting, identity check, problem, troubleshooting, a fix, confirmation and closing.",
  "BEHAVIOUR": "Every agent line is polite and professional, though the agent may be brisk, formal or chatty. The agent may use words like 'obviously' or 'as I said' only in a friendly way."
 },
 {
  "id": "G0715",
  "industry": "travel agency",
  "problem": "transfer not booked",
  "agent_style": "formal",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE call of 40 to 60 turns (about 8 to 10 minutes): greeting, identity check, problem, troubleshooting, a fix, confirmation and closing.",
  "BEHAVIOUR": "Every agent line is polite and professional, though the agent may be brisk, formal or chatty. The agent may use words like 'obviously' or 'as I said' only in a friendly way."
 }
]
