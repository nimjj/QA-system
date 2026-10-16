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

This batch has 19 card(s). Write one excerpt for each.

CARDS
[
 {
  "id": "G0354",
  "industry": "food delivery app",
  "problem": "promo credit disappeared",
  "agent_style": "terse",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0365",
  "industry": "university student services",
  "problem": "tuition payment not showing",
  "agent_style": "warm",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are greeting, identity verification, confirmations, hold requests or wrap-up questions, never about the problem itself."
 },
 {
  "id": "G0389",
  "industry": "SaaS software",
  "problem": "billed for more seats than used",
  "agent_style": "scripted",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0393",
  "industry": "auto insurance",
  "problem": "repair shop approval delayed",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0394",
  "industry": "streaming service",
  "problem": "profile settings keep resetting",
  "agent_style": "hurried",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0399",
  "industry": "gym membership",
  "problem": "still billed after cancelling",
  "agent_style": "apologetic",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0420",
  "industry": "health insurance",
  "problem": "member portal locks the account",
  "agent_style": "technical",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are greeting, identity verification, confirmations, hold requests or wrap-up questions, never about the problem itself."
 },
 {
  "id": "G0424",
  "industry": "food delivery app",
  "problem": "driver marked it delivered but it never came",
  "agent_style": "scripted",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are about upgrades, surveys or scheduling, never about the problem itself."
 },
 {
  "id": "G0444",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "chatty",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are about upgrades, surveys or scheduling, never about the problem itself."
 },
 {
  "id": "G0455",
  "industry": "travel agency",
  "problem": "transfer not booked",
  "agent_style": "hurried",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are about upgrades, surveys or scheduling, never about the problem itself."
 },
 {
  "id": "G0474",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "apologetic",
  "customer_mood": "polite",
  "style": "stt",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0499",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "technical",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are about upgrades, surveys or scheduling, never about the problem itself."
 },
 {
  "id": "G0520",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "terse",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0558",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "scripted",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are greeting, identity verification, confirmations, hold requests or wrap-up questions, never about the problem itself."
 },
 {
  "id": "G0573",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "chatty",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0591",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "apologetic",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "Among the normal greeting and verification questions the agent asks at least one real diagnostic question about the problem (when it started, which device, what error or lights, what has been tried)."
 },
 {
  "id": "G0598",
  "industry": "rental housing portal",
  "problem": "rent payment not recorded",
  "agent_style": "technical",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are greeting, identity verification, confirmations, hold requests or wrap-up questions, never about the problem itself."
 },
 {
  "id": "G0606",
  "industry": "health insurance",
  "problem": "prescription was rejected",
  "agent_style": "hurried",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are greeting, identity verification, confirmations, hold requests or wrap-up questions, never about the problem itself."
 },
 {
  "id": "G0639",
  "industry": "car rental",
  "problem": "warning light on the dashboard",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 8 to 12 turns of the start of a call. The agent must ask at least one question. Include normal greeting and identity-check questions.",
  "BEHAVIOUR": "The agent's only questions are greeting, identity verification, confirmations, hold requests or wrap-up questions, never about the problem itself."
 }
]
