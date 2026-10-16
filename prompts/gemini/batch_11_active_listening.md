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
  "id": "G0003",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "hurried",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0005",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "chatty",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 },
 {
  "id": "G0017",
  "industry": "auto insurance",
  "problem": "claim status unclear after an accident",
  "agent_style": "chatty",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 },
 {
  "id": "G0025",
  "industry": "e-commerce",
  "problem": "refund for a return is late",
  "agent_style": "warm",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0034",
  "industry": "credit card company",
  "problem": "late fee charged though paid on time",
  "agent_style": "formal",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0036",
  "industry": "travel agency",
  "problem": "refund promised but not paid",
  "agent_style": "terse",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0040",
  "industry": "travel agency",
  "problem": "transfer not booked",
  "agent_style": "technical",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0048",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "formal",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0051",
  "industry": "university student services",
  "problem": "tuition payment not showing",
  "agent_style": "scripted",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0073",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "terse",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0081",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "terse",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0082",
  "industry": "credit card company",
  "problem": "new card never arrived",
  "agent_style": "hurried",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0084",
  "industry": "health insurance",
  "problem": "prescription was rejected",
  "agent_style": "technical",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0087",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "formal",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 },
 {
  "id": "G0091",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "apologetic",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0107",
  "industry": "university student services",
  "problem": "student portal will not load",
  "agent_style": "hurried",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0119",
  "industry": "food delivery app",
  "problem": "driver marked it delivered but it never came",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 },
 {
  "id": "G0122",
  "industry": "retail bank",
  "problem": "card payment declined at a shop",
  "agent_style": "scripted",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0126",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0128",
  "industry": "credit card company",
  "problem": "rewards points missing",
  "agent_style": "formal",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 },
 {
  "id": "G0130",
  "industry": "travel agency",
  "problem": "refund promised but not paid",
  "agent_style": "apologetic",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0145",
  "industry": "retail bank",
  "problem": "unknown charge on the statement",
  "agent_style": "terse",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0155",
  "industry": "pharmacy",
  "problem": "delivery missed twice",
  "agent_style": "terse",
  "customer_mood": "polite",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0159",
  "industry": "water utility",
  "problem": "brown water from the tap",
  "agent_style": "warm",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0160",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "technical",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0163",
  "industry": "credit card company",
  "problem": "new card never arrived",
  "agent_style": "apologetic",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0177",
  "industry": "auto insurance",
  "problem": "claim status unclear after an accident",
  "agent_style": "warm",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0186",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "formal",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 }
]
