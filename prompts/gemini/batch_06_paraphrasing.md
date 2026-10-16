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
  "id": "G0001",
  "industry": "food delivery app",
  "problem": "promo credit disappeared",
  "agent_style": "apologetic",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0016",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0022",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "scripted",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only reads back an account detail or plan name, never the problem itself."
 },
 {
  "id": "G0023",
  "industry": "e-commerce",
  "problem": "wrong item in the parcel",
  "agent_style": "apologetic",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent summarises the problem incorrectly: they describe a different problem than the one the customer gave."
 },
 {
  "id": "G0024",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "apologetic",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent first asks one clarifying question, then restates the problem in their own words."
 },
 {
  "id": "G0027",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "terse",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0038",
  "industry": "appliance repair",
  "problem": "fridge rattles and the freezer is warm",
  "agent_style": "apologetic",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0046",
  "industry": "SaaS software",
  "problem": "cannot log in after a password reset",
  "agent_style": "warm",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only reads back an account detail or plan name, never the problem itself."
 },
 {
  "id": "G0047",
  "industry": "water utility",
  "problem": "low pressure since a repair",
  "agent_style": "apologetic",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only asks questions that reuse the customer's own words (for example 'Which light is blinking orange?') and never restates the problem."
 },
 {
  "id": "G0050",
  "industry": "gym membership",
  "problem": "joining fee charged twice",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0052",
  "industry": "auto insurance",
  "problem": "policy documents not received",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0056",
  "industry": "appliance repair",
  "problem": "dishwasher stopped draining",
  "agent_style": "apologetic",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0061",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "apologetic",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent first asks one clarifying question, then restates the problem in their own words."
 },
 {
  "id": "G0062",
  "industry": "auto insurance",
  "problem": "repair shop approval delayed",
  "agent_style": "scripted",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only reads back an account detail or plan name, never the problem itself."
 },
 {
  "id": "G0071",
  "industry": "university student services",
  "problem": "course registration error",
  "agent_style": "scripted",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0078",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "chatty",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0080",
  "industry": "hotel booking site",
  "problem": "double charge for one stay",
  "agent_style": "warm",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only reads back an account detail or plan name, never the problem itself."
 },
 {
  "id": "G0090",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "scripted",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent says things like 'I understand, let me look into that' but never states what the problem is."
 },
 {
  "id": "G0096",
  "industry": "university student services",
  "problem": "tuition payment not showing",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only asks questions that reuse the customer's own words (for example 'Which light is blinking orange?') and never restates the problem."
 },
 {
  "id": "G0102",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "apologetic",
  "customer_mood": "polite",
  "style": "stt",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent says things like 'I understand, let me look into that' but never states what the problem is."
 },
 {
  "id": "G0104",
  "industry": "credit card company",
  "problem": "fraudulent charge on the card",
  "agent_style": "terse",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0105",
  "industry": "streaming service",
  "problem": "video buffers on the living room tv",
  "agent_style": "scripted",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the customer's problem in their own words as a summary and checks it is right."
 },
 {
  "id": "G0112",
  "industry": "food delivery app",
  "problem": "order arrived cold and incomplete",
  "agent_style": "apologetic",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent only asks questions that reuse the customer's own words (for example 'Which light is blinking orange?') and never restates the problem."
 },
 {
  "id": "G0120",
  "industry": "credit card company",
  "problem": "new card never arrived",
  "agent_style": "warm",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent restates the problem briefly, in a few words, without asking for confirmation."
 },
 {
  "id": "G0123",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "technical",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write the first 6 to 10 turns of the call: a brief greeting, the customer explaining the problem in one to three sentences, and the agent's next 3 to 6 turns.",
  "BEHAVIOUR": "The agent jumps straight to an action or instruction without restating the problem."
 }
]
