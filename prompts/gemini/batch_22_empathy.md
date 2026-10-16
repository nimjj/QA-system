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

This batch has 27 card(s). Write one excerpt for each.

CARDS
[
 {
  "id": "G0585",
  "industry": "appliance repair",
  "problem": "fridge rattles and the freezer is warm",
  "agent_style": "formal",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent ignores the emotion and just asks the next procedural question."
 },
 {
  "id": "G0586",
  "industry": "university student services",
  "problem": "student portal will not load",
  "agent_style": "formal",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent brushes the complaint off by explaining policy or saying it is normal."
 },
 {
  "id": "G0596",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "formal",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's first reply is procedural, but their second reply, two turns later, clearly acknowledges how the customer must feel."
 },
 {
  "id": "G0618",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "formal",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's first reply is procedural, but their second reply, two turns later, clearly acknowledges how the customer must feel."
 },
 {
  "id": "G0620",
  "industry": "airline",
  "problem": "bag did not arrive",
  "agent_style": "apologetic",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent gives a long, detailed, purely technical or procedural reply with no acknowledgment of how the customer feels."
 },
 {
  "id": "G0622",
  "industry": "mobile carrier",
  "problem": "no service at home",
  "agent_style": "terse",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent gives a long, detailed, purely technical or procedural reply with no acknowledgment of how the customer feels."
 },
 {
  "id": "G0625",
  "industry": "travel agency",
  "problem": "package holiday changed without notice",
  "agent_style": "chatty",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's reply names the customer's specific situation or feeling in a warm way before moving to a fix."
 },
 {
  "id": "G0626",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "formal",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent gives a long, detailed, purely technical or procedural reply with no acknowledgment of how the customer feels."
 },
 {
  "id": "G0635",
  "industry": "gym membership",
  "problem": "joining fee charged twice",
  "agent_style": "chatty",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's first reply is procedural, but their second reply, two turns later, clearly acknowledges how the customer must feel."
 },
 {
  "id": "G0644",
  "industry": "e-commerce",
  "problem": "order shows delivered but never arrived",
  "agent_style": "scripted",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's reply names the customer's specific situation or feeling in a warm way before moving to a fix."
 },
 {
  "id": "G0645",
  "industry": "airline",
  "problem": "bag did not arrive",
  "agent_style": "hurried",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's first reply is procedural, but their second reply, two turns later, clearly acknowledges how the customer must feel."
 },
 {
  "id": "G0646",
  "industry": "gym membership",
  "problem": "still billed after cancelling",
  "agent_style": "apologetic",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent brushes the complaint off by explaining policy or saying it is normal."
 },
 {
  "id": "G0648",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "chatty",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's first reply is procedural, but their second reply, two turns later, clearly acknowledges how the customer must feel."
 },
 {
  "id": "G0649",
  "industry": "e-commerce",
  "problem": "discount code did not apply",
  "agent_style": "scripted",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's first reply is procedural, but their second reply, two turns later, clearly acknowledges how the customer must feel."
 },
 {
  "id": "G0652",
  "industry": "pharmacy",
  "problem": "wrong dose label",
  "agent_style": "apologetic",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's reply names the customer's specific situation or feeling in a warm way before moving to a fix."
 },
 {
  "id": "G0654",
  "industry": "water utility",
  "problem": "low pressure since a repair",
  "agent_style": "scripted",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent acknowledges the feeling in one short sentence ('That sounds awful.') and then moves on."
 },
 {
  "id": "G0655",
  "industry": "hotel booking site",
  "problem": "room type differs from what was booked",
  "agent_style": "apologetic",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent brushes the complaint off by explaining policy or saying it is normal."
 },
 {
  "id": "G0663",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "apologetic",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent brushes the complaint off by explaining policy or saying it is normal."
 },
 {
  "id": "G0671",
  "industry": "hotel booking site",
  "problem": "booking confirmed but the hotel has no record",
  "agent_style": "chatty",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent gives a long, detailed, purely technical or procedural reply with no acknowledgment of how the customer feels."
 },
 {
  "id": "G0676",
  "industry": "airline",
  "problem": "bag did not arrive",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent gives a long, detailed, purely technical or procedural reply with no acknowledgment of how the customer feels."
 },
 {
  "id": "G0681",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "hurried",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent ignores the emotion and just asks the next procedural question."
 },
 {
  "id": "G0684",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "hurried",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's reply names the customer's specific situation or feeling in a warm way before moving to a fix."
 },
 {
  "id": "G0685",
  "industry": "food delivery app",
  "problem": "promo credit disappeared",
  "agent_style": "hurried",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent ignores the emotion and just asks the next procedural question."
 },
 {
  "id": "G0688",
  "industry": "credit card company",
  "problem": "late fee charged though paid on time",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's reply names the customer's specific situation or feeling in a warm way before moving to a fix."
 },
 {
  "id": "G0691",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "chatty",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent brushes the complaint off by explaining policy or saying it is normal."
 },
 {
  "id": "G0706",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "terse",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent implies it is the customer's own fault."
 },
 {
  "id": "G0707",
  "industry": "electric utility",
  "problem": "repeated short power cuts",
  "agent_style": "scripted",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 9 turns. The customer has ONE clearly upset turn (give it a sentiment of -20 or lower; every other customer turn must be between -2 and -12). IMPORTANT: no agent line in the three turns after the upset turn may contain any of these words: sorry, apologize, apologies, understand, frustrating, let me help.",
  "BEHAVIOUR": "The agent's first reply is procedural, but their second reply, two turns later, clearly acknowledges how the customer must feel."
 }
]
