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

This batch has 26 card(s). Write one excerpt for each.

CARDS
[
 {
  "id": "G0010",
  "industry": "hotel booking site",
  "problem": "booking confirmed but the hotel has no record",
  "agent_style": "scripted",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor or manager; the agent arranges it properly (a transfer, or a callback with a time)."
 },
 {
  "id": "G0018",
  "industry": "university student services",
  "problem": "student portal will not load",
  "agent_style": "chatty",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The agent pretends to look for a manager and then says nobody is available."
 },
 {
  "id": "G0067",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "chatty",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor and the agent ignores the request and carries on."
 },
 {
  "id": "G0072",
  "industry": "SaaS software",
  "problem": "cannot log in after a password reset",
  "agent_style": "chatty",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor or manager; the agent arranges it properly (a transfer, or a callback with a time)."
 },
 {
  "id": "G0076",
  "industry": "retail bank",
  "problem": "unknown charge on the statement",
  "agent_style": "formal",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor and the agent refuses."
 },
 {
  "id": "G0094",
  "industry": "water utility",
  "problem": "brown water from the tap",
  "agent_style": "technical",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The agent talks the customer out of escalating."
 },
 {
  "id": "G0131",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "hurried",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor and the agent refuses."
 },
 {
  "id": "G0157",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "technical",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer is unhappy but never asks for a supervisor or escalation, and the agent handles the issue."
 },
 {
  "id": "G0191",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The agent pretends to look for a manager and then says nobody is available."
 },
 {
  "id": "G0201",
  "industry": "food delivery app",
  "problem": "order arrived cold and incomplete",
  "agent_style": "scripted",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor or manager; the agent arranges it properly (a transfer, or a callback with a time)."
 },
 {
  "id": "G0270",
  "industry": "travel agency",
  "problem": "transfer not booked",
  "agent_style": "chatty",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The agent talks the customer out of escalating."
 },
 {
  "id": "G0281",
  "industry": "credit card company",
  "problem": "new card never arrived",
  "agent_style": "technical",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer is unhappy but never asks for a supervisor or escalation, and the agent handles the issue."
 },
 {
  "id": "G0282",
  "industry": "streaming service",
  "problem": "video buffers on the living room tv",
  "agent_style": "technical",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor and the agent ignores the request and carries on."
 },
 {
  "id": "G0384",
  "industry": "electric utility",
  "problem": "repeated short power cuts",
  "agent_style": "apologetic",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The agent talks the customer out of escalating."
 },
 {
  "id": "G0434",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "apologetic",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer is unhappy but never asks for a supervisor or escalation, and the agent handles the issue."
 },
 {
  "id": "G0448",
  "industry": "food delivery app",
  "problem": "driver marked it delivered but it never came",
  "agent_style": "scripted",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The agent pretends to look for a manager and then says nobody is available."
 },
 {
  "id": "G0457",
  "industry": "food delivery app",
  "problem": "driver marked it delivered but it never came",
  "agent_style": "warm",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor and the agent ignores the request and carries on."
 },
 {
  "id": "G0498",
  "industry": "mobile carrier",
  "problem": "no service at home",
  "agent_style": "apologetic",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer is unhappy but never asks for a supervisor or escalation, and the agent handles the issue."
 },
 {
  "id": "G0552",
  "industry": "gym membership",
  "problem": "cannot freeze the membership",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor or manager; the agent arranges it properly (a transfer, or a callback with a time)."
 },
 {
  "id": "G0589",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "scripted",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor or manager; the agent arranges it properly (a transfer, or a callback with a time)."
 },
 {
  "id": "G0608",
  "industry": "water utility",
  "problem": "bill doubled after a meter swap",
  "agent_style": "apologetic",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor and the agent refuses."
 },
 {
  "id": "G0624",
  "industry": "water utility",
  "problem": "brown water from the tap",
  "agent_style": "chatty",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor or manager; the agent arranges it properly (a transfer, or a callback with a time)."
 },
 {
  "id": "G0651",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "scripted",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor or manager; the agent arranges it properly (a transfer, or a callback with a time)."
 },
 {
  "id": "G0693",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "technical",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer asks for a supervisor and the agent refuses."
 },
 {
  "id": "G0695",
  "industry": "auto insurance",
  "problem": "premium rose without explanation",
  "agent_style": "chatty",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer is unhappy but never asks for a supervisor or escalation, and the agent handles the issue."
 },
 {
  "id": "G0709",
  "industry": "credit card company",
  "problem": "new card never arrived",
  "agent_style": "hurried",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total.",
  "BEHAVIOUR": "The customer is unhappy but never asks for a supervisor or escalation, and the agent handles the issue."
 }
]
