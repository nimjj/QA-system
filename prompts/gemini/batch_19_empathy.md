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

This batch has 28 card(s). Write one excerpt for each.

CARDS
[
 {
  "id": "G0002",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "technical",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's first reply is procedural, but their second reply, two turns later, clearly acknowledges how the customer must feel."
 },
 {
  "id": "G0021",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "chatty",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent implies it is the customer's own fault."
 },
 {
  "id": "G0026",
  "industry": "hotel booking site",
  "problem": "cancellation refund not received",
  "agent_style": "technical",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's first reply is procedural, but their second reply, two turns later, clearly acknowledges how the customer must feel."
 },
 {
  "id": "G0029",
  "industry": "hotel booking site",
  "problem": "double charge for one stay",
  "agent_style": "technical",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent gives a long, detailed, purely technical or procedural reply with no acknowledgment of how the customer feels."
 },
 {
  "id": "G0030",
  "industry": "auto insurance",
  "problem": "premium rose without explanation",
  "agent_style": "apologetic",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent ignores the emotion and just asks the next procedural question."
 },
 {
  "id": "G0037",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "apologetic",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's reply names the customer's specific situation or feeling in a warm way before moving to a fix."
 },
 {
  "id": "G0054",
  "industry": "airline",
  "problem": "refund for a cancelled trip is missing",
  "agent_style": "chatty",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's first reply is procedural, but their second reply, two turns later, clearly acknowledges how the customer must feel."
 },
 {
  "id": "G0063",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "hurried",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent acknowledges the feeling in one short sentence ('That sounds awful.') and then moves on."
 },
 {
  "id": "G0065",
  "industry": "food delivery app",
  "problem": "charged after cancelling",
  "agent_style": "apologetic",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent acknowledges the feeling in one short sentence ('That sounds awful.') and then moves on."
 },
 {
  "id": "G0068",
  "industry": "water utility",
  "problem": "leak reported but nobody came",
  "agent_style": "terse",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent ignores the emotion and just asks the next procedural question."
 },
 {
  "id": "G0088",
  "industry": "gym membership",
  "problem": "cannot freeze the membership",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent acknowledges the feeling in one short sentence ('That sounds awful.') and then moves on."
 },
 {
  "id": "G0092",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "apologetic",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's reply names the customer's specific situation or feeling in a warm way before moving to a fix."
 },
 {
  "id": "G0109",
  "industry": "airline",
  "problem": "seat selection will not save",
  "agent_style": "warm",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent gives a long, detailed, purely technical or procedural reply with no acknowledgment of how the customer feels."
 },
 {
  "id": "G0110",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "apologetic",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent implies it is the customer's own fault."
 },
 {
  "id": "G0113",
  "industry": "travel agency",
  "problem": "refund promised but not paid",
  "agent_style": "hurried",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent acknowledges the feeling in one short sentence ('That sounds awful.') and then moves on."
 },
 {
  "id": "G0127",
  "industry": "university student services",
  "problem": "transcript request is stuck",
  "agent_style": "scripted",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent acknowledges the feeling in one short sentence ('That sounds awful.') and then moves on."
 },
 {
  "id": "G0129",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "hurried",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent acknowledges the feeling in one short sentence ('That sounds awful.') and then moves on."
 },
 {
  "id": "G0139",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "hurried",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent ignores the emotion and just asks the next procedural question."
 },
 {
  "id": "G0141",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "terse",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's first reply is procedural, but their second reply, two turns later, clearly acknowledges how the customer must feel."
 },
 {
  "id": "G0147",
  "industry": "car rental",
  "problem": "app will not unlock the car",
  "agent_style": "chatty",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent ignores the emotion and just asks the next procedural question."
 },
 {
  "id": "G0162",
  "industry": "water utility",
  "problem": "leak reported but nobody came",
  "agent_style": "scripted",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent implies it is the customer's own fault."
 },
 {
  "id": "G0165",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "hurried",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent acknowledges the feeling in one short sentence ('That sounds awful.') and then moves on."
 },
 {
  "id": "G0173",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "scripted",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent brushes the complaint off by explaining policy or saying it is normal."
 },
 {
  "id": "G0174",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "scripted",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent brushes the complaint off by explaining policy or saying it is normal."
 },
 {
  "id": "G0176",
  "industry": "hotel booking site",
  "problem": "double charge for one stay",
  "agent_style": "terse",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent brushes the complaint off by explaining policy or saying it is normal."
 },
 {
  "id": "G0190",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "terse",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent ignores the emotion and just asks the next procedural question."
 },
 {
  "id": "G0207",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "formal",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent brushes the complaint off by explaining policy or saying it is normal."
 },
 {
  "id": "G0216",
  "industry": "retail bank",
  "problem": "transfer shows failed but the balance dropped",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent acknowledges the feeling in one short sentence ('That sounds awful.') and then moves on."
 }
]
