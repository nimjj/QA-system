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
  "id": "G0187",
  "industry": "gym membership",
  "problem": "cannot freeze the membership",
  "agent_style": "scripted",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0193",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "chatty",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 },
 {
  "id": "G0197",
  "industry": "streaming service",
  "problem": "billed twice this month",
  "agent_style": "apologetic",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0202",
  "industry": "e-commerce",
  "problem": "discount code did not apply",
  "agent_style": "warm",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0209",
  "industry": "hotel booking site",
  "problem": "room type differs from what was booked",
  "agent_style": "chatty",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0210",
  "industry": "electric utility",
  "problem": "estimated bill is far too high",
  "agent_style": "formal",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0214",
  "industry": "retail bank",
  "problem": "unknown charge on the statement",
  "agent_style": "hurried",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0225",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "apologetic",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0228",
  "industry": "water utility",
  "problem": "leak reported but nobody came",
  "agent_style": "chatty",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0235",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "apologetic",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0240",
  "industry": "gym membership",
  "problem": "joining fee charged twice",
  "agent_style": "warm",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0241",
  "industry": "rental housing portal",
  "problem": "rent payment not recorded",
  "agent_style": "technical",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0243",
  "industry": "car rental",
  "problem": "app will not unlock the car",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0249",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "technical",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 },
 {
  "id": "G0256",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0259",
  "industry": "university student services",
  "problem": "course registration error",
  "agent_style": "chatty",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 },
 {
  "id": "G0264",
  "industry": "water utility",
  "problem": "bill doubled after a meter swap",
  "agent_style": "chatty",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 },
 {
  "id": "G0271",
  "industry": "streaming service",
  "problem": "video buffers on the living room tv",
  "agent_style": "hurried",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0276",
  "industry": "car rental",
  "problem": "unexpected fee after returning the car",
  "agent_style": "apologetic",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0278",
  "industry": "rental housing portal",
  "problem": "rent payment not recorded",
  "agent_style": "terse",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0284",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "chatty",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0289",
  "industry": "rental housing portal",
  "problem": "lease document will not download",
  "agent_style": "apologetic",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 },
 {
  "id": "G0294",
  "industry": "food delivery app",
  "problem": "charged after cancelling",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0295",
  "industry": "car rental",
  "problem": "damage charge disputed",
  "agent_style": "apologetic",
  "customer_mood": "polite",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0313",
  "industry": "streaming service",
  "problem": "no sound in the app",
  "agent_style": "chatty",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0319",
  "industry": "streaming service",
  "problem": "profile settings keep resetting",
  "agent_style": "scripted",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0324",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "terse",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0335",
  "industry": "university student services",
  "problem": "transcript request is stuck",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 }
]
