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

This batch has 25 card(s). Write one excerpt for each.

CARDS
[
 {
  "id": "G0450",
  "industry": "electric utility",
  "problem": "repeated short power cuts",
  "agent_style": "terse",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only reads back an account detail or plan name, never the problem itself."
 },
 {
  "id": "G0452",
  "industry": "travel agency",
  "problem": "package holiday changed without notice",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only reads back an account detail or plan name, never the problem itself."
 },
 {
  "id": "G0458",
  "industry": "auto insurance",
  "problem": "repair shop approval delayed",
  "agent_style": "chatty",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only asks questions that reuse the customer's own words (for example 'Which light is blinking orange?') and never restates the problem."
 },
 {
  "id": "G0472",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent summarises the problem incorrectly: they describe a different problem than the one the customer gave."
 },
 {
  "id": "G0501",
  "industry": "auto insurance",
  "problem": "claim status unclear after an accident",
  "agent_style": "warm",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent says things like 'I understand, let me look into that' but never states what the problem is."
 },
 {
  "id": "G0504",
  "industry": "pharmacy",
  "problem": "delivery missed twice",
  "agent_style": "warm",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent jumps straight to an action or instruction without restating the problem."
 },
 {
  "id": "G0511",
  "industry": "airline",
  "problem": "seat selection will not save",
  "agent_style": "warm",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent says things like 'I understand, let me look into that' but never states what the problem is."
 },
 {
  "id": "G0517",
  "industry": "health insurance",
  "problem": "claim shows the full amount owed",
  "agent_style": "warm",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent summarises the problem incorrectly: they describe a different problem than the one the customer gave."
 },
 {
  "id": "G0524",
  "industry": "water utility",
  "problem": "low pressure since a repair",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent says things like 'I understand, let me look into that' but never states what the problem is."
 },
 {
  "id": "G0534",
  "industry": "food delivery app",
  "problem": "driver marked it delivered but it never came",
  "agent_style": "warm",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0535",
  "industry": "gym membership",
  "problem": "still billed after cancelling",
  "agent_style": "hurried",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent says things like 'I understand, let me look into that' but never states what the problem is."
 },
 {
  "id": "G0537",
  "industry": "e-commerce",
  "problem": "refund for a return is late",
  "agent_style": "chatty",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0538",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "terse",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only reads back an account detail or plan name, never the problem itself."
 },
 {
  "id": "G0541",
  "industry": "pharmacy",
  "problem": "insurance claim rejected at the counter",
  "agent_style": "hurried",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent first asks one clarifying question, then restates the problem in their own words."
 },
 {
  "id": "G0542",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "formal",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent first asks one clarifying question, then restates the problem in their own words."
 },
 {
  "id": "G0544",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "warm",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only reads back an account detail or plan name, never the problem itself."
 },
 {
  "id": "G0547",
  "industry": "mobile carrier",
  "problem": "bill much higher than usual",
  "agent_style": "terse",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent jumps straight to an action or instruction without restating the problem."
 },
 {
  "id": "G0550",
  "industry": "hotel booking site",
  "problem": "room type differs from what was booked",
  "agent_style": "formal",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only reads back an account detail or plan name, never the problem itself."
 },
 {
  "id": "G0561",
  "industry": "travel agency",
  "problem": "refund promised but not paid",
  "agent_style": "formal",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent first asks one clarifying question, then restates the problem in their own words."
 },
 {
  "id": "G0562",
  "industry": "rental housing portal",
  "problem": "deposit return delayed",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0567",
  "industry": "pharmacy",
  "problem": "wrong dose label",
  "agent_style": "terse",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0574",
  "industry": "electric utility",
  "problem": "smart meter display is blank",
  "agent_style": "formal",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0578",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "warm",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0581",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "technical",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0582",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent first asks one clarifying question, then restates the problem in their own words."
 }
]
