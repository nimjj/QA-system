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
  "id": "G0008",
  "industry": "mobile carrier",
  "problem": "texts not arriving",
  "agent_style": "apologetic",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line talks down to the customer, implying the problem is simple or obvious."
 },
 {
  "id": "G0009",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "warm",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "At least one agent line uses 'obviously', 'as I said' or 'you should have' in a friendly, helpful way (not blaming)."
 },
 {
  "id": "G0019",
  "industry": "streaming service",
  "problem": "video buffers on the living room tv",
  "agent_style": "technical",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "The agent is brisk and minimal (short lines) but never rude or dismissive."
 },
 {
  "id": "G0031",
  "industry": "credit card company",
  "problem": "rewards points missing",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line talks down to the customer, implying the problem is simple or obvious."
 },
 {
  "id": "G0032",
  "industry": "mobile carrier",
  "problem": "bill much higher than usual",
  "agent_style": "technical",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line dismisses the customer's concern or tells them to stop going on about it."
 },
 {
  "id": "G0039",
  "industry": "water utility",
  "problem": "low pressure since a repair",
  "agent_style": "chatty",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "At least one agent line uses 'obviously', 'as I said' or 'you should have' in a friendly, helpful way (not blaming)."
 },
 {
  "id": "G0053",
  "industry": "credit card company",
  "problem": "late fee charged though paid on time",
  "agent_style": "chatty",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Eight short agent lines, all courteous and warm (still at most 110 words of agent speech in total)."
 },
 {
  "id": "G0057",
  "industry": "university student services",
  "problem": "course registration error",
  "agent_style": "chatty",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "The agent is brisk and minimal (short lines) but never rude or dismissive."
 },
 {
  "id": "G0058",
  "industry": "airline",
  "problem": "seat selection will not save",
  "agent_style": "apologetic",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Eight short agent lines, all courteous and warm (still at most 110 words of agent speech in total)."
 },
 {
  "id": "G0064",
  "industry": "streaming service",
  "problem": "billed twice this month",
  "agent_style": "formal",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Every agent line is polite and professional."
 },
 {
  "id": "G0066",
  "industry": "credit card company",
  "problem": "rewards points missing",
  "agent_style": "formal",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Every agent line is polite and professional."
 },
 {
  "id": "G0069",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "terse",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line is sarcastic about something the customer said."
 },
 {
  "id": "G0086",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "terse",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "At least one agent line uses 'obviously', 'as I said' or 'you should have' in a friendly, helpful way (not blaming)."
 },
 {
  "id": "G0089",
  "industry": "gym membership",
  "problem": "access card stopped working",
  "agent_style": "formal",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line talks down to the customer, implying the problem is simple or obvious."
 },
 {
  "id": "G0095",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "apologetic",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Seven agent lines are professional; exactly one line, somewhere in the middle, is rude or condescending."
 },
 {
  "id": "G0097",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line sounds openly exasperated at having to repeat something."
 },
 {
  "id": "G0100",
  "industry": "university student services",
  "problem": "course registration error",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line dismisses the customer's concern or tells them to stop going on about it."
 },
 {
  "id": "G0108",
  "industry": "auto insurance",
  "problem": "repair shop approval delayed",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "At least one agent line uses 'obviously', 'as I said' or 'you should have' in a friendly, helpful way (not blaming)."
 },
 {
  "id": "G0111",
  "industry": "hotel booking site",
  "problem": "cancellation refund not received",
  "agent_style": "apologetic",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "At least one agent line uses 'obviously', 'as I said' or 'you should have' in a friendly, helpful way (not blaming)."
 },
 {
  "id": "G0114",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Seven agent lines are professional; exactly one line, somewhere in the middle, is rude or condescending."
 },
 {
  "id": "G0115",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "hurried",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Eight short agent lines, all courteous and warm (still at most 110 words of agent speech in total)."
 },
 {
  "id": "G0121",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "hurried",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line sounds openly exasperated at having to repeat something."
 },
 {
  "id": "G0132",
  "industry": "appliance repair",
  "problem": "dishwasher stopped draining",
  "agent_style": "formal",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "The agent is brisk and minimal (short lines) but never rude or dismissive."
 },
 {
  "id": "G0134",
  "industry": "credit card company",
  "problem": "late fee charged though paid on time",
  "agent_style": "scripted",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Eight short agent lines, all courteous and warm (still at most 110 words of agent speech in total)."
 },
 {
  "id": "G0136",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "formal",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Every agent line is polite and professional."
 }
]
