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
  "id": "G0007",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "technical",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent insults the customer once."
 },
 {
  "id": "G0011",
  "industry": "auto insurance",
  "problem": "premium rose without explanation",
  "agent_style": "hurried",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry (may swear); the agent stays calm and professional throughout."
 },
 {
  "id": "G0020",
  "industry": "food delivery app",
  "problem": "driver marked it delivered but it never came",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry (may swear); the agent stays calm and professional throughout."
 },
 {
  "id": "G0059",
  "industry": "water utility",
  "problem": "leak reported but nobody came",
  "agent_style": "apologetic",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry; the agent is short and businesslike but never insulting."
 },
 {
  "id": "G0060",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "chatty",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent mocks the customer."
 },
 {
  "id": "G0093",
  "industry": "car rental",
  "problem": "unexpected fee after returning the car",
  "agent_style": "formal",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry; the agent is short and businesslike but never insulting."
 },
 {
  "id": "G0099",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "technical",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent threatens to hang up or cut off service."
 },
 {
  "id": "G0103",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent abruptly ends the call on the customer (show it in the final turn)."
 },
 {
  "id": "G0140",
  "industry": "streaming service",
  "problem": "no sound in the app",
  "agent_style": "formal",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent insults the customer once."
 },
 {
  "id": "G0156",
  "industry": "gym membership",
  "problem": "joining fee charged twice",
  "agent_style": "technical",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent insults the customer once."
 },
 {
  "id": "G0180",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "formal",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent abruptly ends the call on the customer (show it in the final turn)."
 },
 {
  "id": "G0185",
  "industry": "health insurance",
  "problem": "member portal locks the account",
  "agent_style": "hurried",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent mocks the customer."
 },
 {
  "id": "G0224",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "formal",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry; the agent is short and businesslike but never insulting."
 },
 {
  "id": "G0229",
  "industry": "auto insurance",
  "problem": "policy documents not received",
  "agent_style": "terse",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry (may swear); the agent stays calm and professional throughout."
 },
 {
  "id": "G0250",
  "industry": "streaming service",
  "problem": "billed twice this month",
  "agent_style": "warm",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry (may swear); the agent stays calm and professional throughout."
 },
 {
  "id": "G0252",
  "industry": "hotel booking site",
  "problem": "booking confirmed but the hotel has no record",
  "agent_style": "terse",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent abruptly ends the call on the customer (show it in the final turn)."
 },
 {
  "id": "G0318",
  "industry": "water utility",
  "problem": "brown water from the tap",
  "agent_style": "chatty",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry (may swear); the agent stays calm and professional throughout."
 },
 {
  "id": "G0347",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "hurried",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry; the agent is short and businesslike but never insulting."
 },
 {
  "id": "G0406",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "warm",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry (may swear); the agent stays calm and professional throughout."
 },
 {
  "id": "G0456",
  "industry": "car rental",
  "problem": "warning light on the dashboard",
  "agent_style": "formal",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry (may swear); the agent stays calm and professional throughout."
 },
 {
  "id": "G0516",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "warm",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent insults the customer once."
 },
 {
  "id": "G0528",
  "industry": "mobile carrier",
  "problem": "no service at home",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry; the agent is short and businesslike but never insulting."
 },
 {
  "id": "G0630",
  "industry": "retail bank",
  "problem": "mortgage payment taken twice",
  "agent_style": "warm",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent threatens to hang up or cut off service."
 },
 {
  "id": "G0631",
  "industry": "car rental",
  "problem": "unexpected fee after returning the car",
  "agent_style": "technical",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent threatens to hang up or cut off service."
 },
 {
  "id": "G0656",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "apologetic",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The agent mocks the customer."
 },
 {
  "id": "G0689",
  "industry": "streaming service",
  "problem": "no sound in the app",
  "agent_style": "technical",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write a COMPLETE short call of 8 to 12 turns, under 200 words in total. The customer is angry or swears.",
  "BEHAVIOUR": "The customer is angry; the agent is short and businesslike but never insulting."
 }
]
