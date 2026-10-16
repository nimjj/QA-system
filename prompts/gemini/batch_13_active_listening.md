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
  "id": "G0336",
  "industry": "university student services",
  "problem": "transcript request is stuck",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0337",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "technical",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 },
 {
  "id": "G0338",
  "industry": "hotel booking site",
  "problem": "cancellation refund not received",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0341",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0342",
  "industry": "travel agency",
  "problem": "transfer not booked",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0343",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "apologetic",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0345",
  "industry": "rental housing portal",
  "problem": "rent payment not recorded",
  "agent_style": "formal",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 },
 {
  "id": "G0361",
  "industry": "SaaS software",
  "problem": "export keeps failing",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0366",
  "industry": "mobile carrier",
  "problem": "texts not arriving",
  "agent_style": "terse",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0370",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "technical",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0390",
  "industry": "hotel booking site",
  "problem": "double charge for one stay",
  "agent_style": "chatty",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0398",
  "industry": "water utility",
  "problem": "low pressure since a repair",
  "agent_style": "chatty",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0407",
  "industry": "food delivery app",
  "problem": "promo credit disappeared",
  "agent_style": "warm",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0419",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "warm",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0421",
  "industry": "hotel booking site",
  "problem": "double charge for one stay",
  "agent_style": "scripted",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0425",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "scripted",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0426",
  "industry": "water utility",
  "problem": "bill doubled after a meter swap",
  "agent_style": "chatty",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0427",
  "industry": "electric utility",
  "problem": "estimated bill is far too high",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0446",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0449",
  "industry": "credit card company",
  "problem": "fraudulent charge on the card",
  "agent_style": "warm",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0454",
  "industry": "hotel booking site",
  "problem": "room type differs from what was booked",
  "agent_style": "scripted",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "As above, but the repeat comes after four or five turns of other conversation."
 },
 {
  "id": "G0461",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "formal",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0468",
  "industry": "mobile carrier",
  "problem": "texts not arriving",
  "agent_style": "apologetic",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0476",
  "industry": "hotel booking site",
  "problem": "cancellation refund not received",
  "agent_style": "scripted",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The customer's first answer is vague ('a while', 'it's weird'); the agent asks again using similar words, asking for the missing detail."
 },
 {
  "id": "G0477",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "formal",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0482",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "technical",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks for the same information again and the customer reacts with something like 'like I said' or 'I already told you'."
 },
 {
  "id": "G0491",
  "industry": "mobile carrier",
  "problem": "texts not arriving",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks about the current state of something (a light, a screen, a speed, a balance), has the customer do something that could change it, then asks the same question again with 'now' or 'this time' because the answer may have changed."
 },
 {
  "id": "G0492",
  "industry": "university student services",
  "problem": "student portal will not load",
  "agent_style": "formal",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 6 to 10 turns. The agent's second question must share most of its words with the agent's first question (this is required).",
  "BEHAVIOUR": "The agent asks a question, the customer answers it clearly, and a few turns later the agent asks for the same information again using almost the same words."
 }
]
