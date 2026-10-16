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

This batch has 24 card(s). Write one excerpt for each.

CARDS
[
 {
  "id": "G0601",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "chatty",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line mocks the customer's mistake."
 },
 {
  "id": "G0604",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "hurried",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line blames the customer for the problem, implying they should have known better, without any insult."
 },
 {
  "id": "G0609",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "chatty",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line dismisses the customer's concern or tells them to stop going on about it."
 },
 {
  "id": "G0614",
  "industry": "pharmacy",
  "problem": "wrong dose label",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line mocks the customer's mistake."
 },
 {
  "id": "G0616",
  "industry": "gym membership",
  "problem": "cannot freeze the membership",
  "agent_style": "technical",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "At least one agent line uses 'obviously', 'as I said' or 'you should have' in a friendly, helpful way (not blaming)."
 },
 {
  "id": "G0617",
  "industry": "credit card company",
  "problem": "fraudulent charge on the card",
  "agent_style": "hurried",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line blames the customer for the problem, implying they should have known better, without any insult."
 },
 {
  "id": "G0621",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Every agent line is polite and professional."
 },
 {
  "id": "G0623",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "formal",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Eight short agent lines, all courteous and warm (still at most 110 words of agent speech in total)."
 },
 {
  "id": "G0627",
  "industry": "gym membership",
  "problem": "cannot freeze the membership",
  "agent_style": "technical",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "At least one agent line uses 'obviously', 'as I said' or 'you should have' in a friendly, helpful way (not blaming)."
 },
 {
  "id": "G0629",
  "industry": "appliance repair",
  "problem": "technician no-show",
  "agent_style": "chatty",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Every agent line is polite and professional."
 },
 {
  "id": "G0637",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "warm",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line blames the customer for the problem, implying they should have known better, without any insult."
 },
 {
  "id": "G0641",
  "industry": "university student services",
  "problem": "course registration error",
  "agent_style": "warm",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line blames the customer for the problem, implying they should have known better, without any insult."
 },
 {
  "id": "G0643",
  "industry": "gym membership",
  "problem": "access card stopped working",
  "agent_style": "hurried",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Every agent line is polite and professional."
 },
 {
  "id": "G0658",
  "industry": "credit card company",
  "problem": "late fee charged though paid on time",
  "agent_style": "scripted",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "The agent is brisk and minimal (short lines) but never rude or dismissive."
 },
 {
  "id": "G0662",
  "industry": "food delivery app",
  "problem": "driver marked it delivered but it never came",
  "agent_style": "scripted",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line blames the customer for the problem, implying they should have known better, without any insult."
 },
 {
  "id": "G0664",
  "industry": "pharmacy",
  "problem": "prescription refill not ready",
  "agent_style": "warm",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Seven agent lines are professional; exactly one line, somewhere in the middle, is rude or condescending."
 },
 {
  "id": "G0668",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "formal",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Eight short agent lines, all courteous and warm (still at most 110 words of agent speech in total)."
 },
 {
  "id": "G0669",
  "industry": "food delivery app",
  "problem": "driver marked it delivered but it never came",
  "agent_style": "warm",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Every agent line is polite and professional."
 },
 {
  "id": "G0672",
  "industry": "university student services",
  "problem": "course registration error",
  "agent_style": "warm",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line sounds openly exasperated at having to repeat something."
 },
 {
  "id": "G0675",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "technical",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "At least one agent line uses 'obviously', 'as I said' or 'you should have' in a friendly, helpful way (not blaming)."
 },
 {
  "id": "G0680",
  "industry": "e-commerce",
  "problem": "wrong item in the parcel",
  "agent_style": "technical",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line blames the customer for the problem, implying they should have known better, without any insult."
 },
 {
  "id": "G0682",
  "industry": "appliance repair",
  "problem": "technician no-show",
  "agent_style": "warm",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line is sarcastic about something the customer said."
 },
 {
  "id": "G0687",
  "industry": "food delivery app",
  "problem": "order arrived cold and incomplete",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Eight short agent lines, all courteous and warm (still at most 110 words of agent speech in total)."
 },
 {
  "id": "G0694",
  "industry": "credit card company",
  "problem": "new card never arrived",
  "agent_style": "terse",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line mocks the customer's mistake."
 }
]
