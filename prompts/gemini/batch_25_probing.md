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

This batch has 20 card(s). Write one excerpt for each.

CARDS
[
 {
  "id": "G0004",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "technical",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0075",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "hurried",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are greeting, identity verification, confirmations, hold requests or wrap-up questions, never about the problem itself."
 },
 {
  "id": "G0077",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "chatty",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are greeting, identity verification, confirmations, hold requests or wrap-up questions, never about the problem itself."
 },
 {
  "id": "G0083",
  "industry": "credit card company",
  "problem": "rewards points missing",
  "agent_style": "terse",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are about upgrades, surveys or scheduling, never about the problem itself."
 },
 {
  "id": "G0098",
  "industry": "pharmacy",
  "problem": "wrong dose label",
  "agent_style": "warm",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are about upgrades, surveys or scheduling, never about the problem itself."
 },
 {
  "id": "G0101",
  "industry": "water utility",
  "problem": "brown water from the tap",
  "agent_style": "terse",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0144",
  "industry": "health insurance",
  "problem": "member portal locks the account",
  "agent_style": "technical",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0158",
  "industry": "rental housing portal",
  "problem": "maintenance request ignored",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0178",
  "industry": "water utility",
  "problem": "bill doubled after a meter swap",
  "agent_style": "formal",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0181",
  "industry": "pharmacy",
  "problem": "insurance claim rejected at the counter",
  "agent_style": "hurried",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are about upgrades, surveys or scheduling, never about the problem itself."
 },
 {
  "id": "G0203",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "terse",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0206",
  "industry": "e-commerce",
  "problem": "discount code did not apply",
  "agent_style": "terse",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0247",
  "industry": "car rental",
  "problem": "unexpected fee after returning the car",
  "agent_style": "chatty",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0248",
  "industry": "gym membership",
  "problem": "still billed after cancelling",
  "agent_style": "terse",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0251",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "warm",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are greeting, identity verification, confirmations, hold requests or wrap-up questions, never about the problem itself."
 },
 {
  "id": "G0272",
  "industry": "mobile carrier",
  "problem": "bill much higher than usual",
  "agent_style": "technical",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0316",
  "industry": "water utility",
  "problem": "low pressure since a repair",
  "agent_style": "formal",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are greeting, identity verification, confirmations, hold requests or wrap-up questions, never about the problem itself."
 },
 {
  "id": "G0317",
  "industry": "pharmacy",
  "problem": "wrong dose label",
  "agent_style": "chatty",
  "customer_mood": "polite",
  "style": "stt",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are about upgrades, surveys or scheduling, never about the problem itself."
 },
 {
  "id": "G0326",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "chatty",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0330",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "terse",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are about upgrades, surveys or scheduling, never about the problem itself."
 }
]
