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
  "id": "G0298",
  "industry": "pharmacy",
  "problem": "prescription refill not ready",
  "agent_style": "chatty",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent first asks one clarifying question, then restates the problem in their own words."
 },
 {
  "id": "G0306",
  "industry": "credit card company",
  "problem": "late fee charged though paid on time",
  "agent_style": "technical",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only reads back an account detail or plan name, never the problem itself."
 },
 {
  "id": "G0308",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "terse",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent first asks one clarifying question, then restates the problem in their own words."
 },
 {
  "id": "G0309",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "technical",
  "customer_mood": "polite",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent jumps straight to an action or instruction without restating the problem."
 },
 {
  "id": "G0310",
  "industry": "gym membership",
  "problem": "joining fee charged twice",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent first asks one clarifying question, then restates the problem in their own words."
 },
 {
  "id": "G0314",
  "industry": "airline",
  "problem": "bag did not arrive",
  "agent_style": "technical",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0322",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "formal",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only asks questions that reuse the customer's own words (for example 'Which light is blinking orange?') and never restates the problem."
 },
 {
  "id": "G0328",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "scripted",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent says things like 'I understand, let me look into that' but never states what the problem is."
 },
 {
  "id": "G0329",
  "industry": "auto insurance",
  "problem": "premium rose without explanation",
  "agent_style": "terse",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0339",
  "industry": "electric utility",
  "problem": "estimated bill is far too high",
  "agent_style": "apologetic",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0358",
  "industry": "food delivery app",
  "problem": "promo credit disappeared",
  "agent_style": "formal",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0360",
  "industry": "retail bank",
  "problem": "transfer shows failed but the balance dropped",
  "agent_style": "scripted",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only asks questions that reuse the customer's own words (for example 'Which light is blinking orange?') and never restates the problem."
 },
 {
  "id": "G0367",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "chatty",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent says things like 'I understand, let me look into that' but never states what the problem is."
 },
 {
  "id": "G0371",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "formal",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent summarises the problem incorrectly: they describe a different problem than the one the customer gave."
 },
 {
  "id": "G0375",
  "industry": "credit card company",
  "problem": "rewards points missing",
  "agent_style": "scripted",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0376",
  "industry": "appliance repair",
  "problem": "technician no-show",
  "agent_style": "formal",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0391",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "apologetic",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0400",
  "industry": "hotel booking site",
  "problem": "double charge for one stay",
  "agent_style": "apologetic",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent first asks one clarifying question, then restates the problem in their own words."
 },
 {
  "id": "G0401",
  "industry": "travel agency",
  "problem": "refund promised but not paid",
  "agent_style": "chatty",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0410",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent says things like 'I understand, let me look into that' but never states what the problem is."
 },
 {
  "id": "G0413",
  "industry": "gym membership",
  "problem": "still billed after cancelling",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0417",
  "industry": "travel agency",
  "problem": "refund promised but not paid",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent first asks one clarifying question, then restates the problem in their own words."
 },
 {
  "id": "G0428",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "chatty",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent summarises the problem incorrectly: they describe a different problem than the one the customer gave."
 },
 {
  "id": "G0429",
  "industry": "streaming service",
  "problem": "video buffers on the living room tv",
  "agent_style": "warm",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent jumps straight to an action or instruction without restating the problem."
 },
 {
  "id": "G0431",
  "industry": "mobile carrier",
  "problem": "data not working abroad",
  "agent_style": "formal",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 }
]
