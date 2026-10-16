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
  "id": "G0149",
  "industry": "car rental",
  "problem": "unexpected fee after returning the car",
  "agent_style": "warm",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Eight short agent lines, all courteous and warm (still at most 110 words of agent speech in total)."
 },
 {
  "id": "G0153",
  "industry": "travel agency",
  "problem": "package holiday changed without notice",
  "agent_style": "technical",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "At least one agent line uses 'obviously', 'as I said' or 'you should have' in a friendly, helpful way (not blaming)."
 },
 {
  "id": "G0154",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "hurried",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "The agent is brisk and minimal (short lines) but never rude or dismissive."
 },
 {
  "id": "G0164",
  "industry": "university student services",
  "problem": "student portal will not load",
  "agent_style": "technical",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Every agent line is polite and professional."
 },
 {
  "id": "G0171",
  "industry": "university student services",
  "problem": "student portal will not load",
  "agent_style": "warm",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Seven agent lines are professional; exactly one line, somewhere in the middle, is rude or condescending."
 },
 {
  "id": "G0175",
  "industry": "credit card company",
  "problem": "rewards points missing",
  "agent_style": "scripted",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "The agent is brisk and minimal (short lines) but never rude or dismissive."
 },
 {
  "id": "G0183",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "technical",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line sounds openly exasperated at having to repeat something."
 },
 {
  "id": "G0196",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "apologetic",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line talks down to the customer, implying the problem is simple or obvious."
 },
 {
  "id": "G0212",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "chatty",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Seven agent lines are professional; exactly one line, somewhere in the middle, is rude or condescending."
 },
 {
  "id": "G0219",
  "industry": "health insurance",
  "problem": "prescription was rejected",
  "agent_style": "terse",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line mocks the customer's mistake."
 },
 {
  "id": "G0221",
  "industry": "food delivery app",
  "problem": "charged after cancelling",
  "agent_style": "formal",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line blames the customer for the problem, implying they should have known better, without any insult."
 },
 {
  "id": "G0226",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "hurried",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line dismisses the customer's concern or tells them to stop going on about it."
 },
 {
  "id": "G0227",
  "industry": "e-commerce",
  "problem": "order shows delivered but never arrived",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line mocks the customer's mistake."
 },
 {
  "id": "G0242",
  "industry": "university student services",
  "problem": "transcript request is stuck",
  "agent_style": "warm",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "The agent is brisk and minimal (short lines) but never rude or dismissive."
 },
 {
  "id": "G0244",
  "industry": "electric utility",
  "problem": "smart meter display is blank",
  "agent_style": "technical",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line blames the customer for the problem, implying they should have known better, without any insult."
 },
 {
  "id": "G0254",
  "industry": "health insurance",
  "problem": "referral request will not submit",
  "agent_style": "apologetic",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line talks down to the customer, implying the problem is simple or obvious."
 },
 {
  "id": "G0255",
  "industry": "university student services",
  "problem": "course registration error",
  "agent_style": "terse",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "At least one agent line uses 'obviously', 'as I said' or 'you should have' in a friendly, helpful way (not blaming)."
 },
 {
  "id": "G0261",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "technical",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line blames the customer for the problem, implying they should have known better, without any insult."
 },
 {
  "id": "G0265",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "chatty",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line is sarcastic about something the customer said."
 },
 {
  "id": "G0267",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "scripted",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "At least one agent line uses 'obviously', 'as I said' or 'you should have' in a friendly, helpful way (not blaming)."
 },
 {
  "id": "G0269",
  "industry": "streaming service",
  "problem": "profile settings keep resetting",
  "agent_style": "scripted",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Eight short agent lines, all courteous and warm (still at most 110 words of agent speech in total)."
 },
 {
  "id": "G0277",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "apologetic",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "Eight short agent lines, all courteous and warm (still at most 110 words of agent speech in total)."
 },
 {
  "id": "G0291",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "warm",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "The agent is brisk and minimal (short lines) but never rude or dismissive."
 },
 {
  "id": "G0292",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "scripted",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line sounds openly exasperated at having to repeat something."
 },
 {
  "id": "G0296",
  "industry": "electric utility",
  "problem": "smart meter display is blank",
  "agent_style": "technical",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 5 to 8 AGENT lines with AT MOST 110 words of agent speech in total (short customer lines in between are fine and do not count).",
  "BEHAVIOUR": "One agent line talks down to the customer, implying the problem is simple or obvious."
 }
]
