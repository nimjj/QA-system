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

This batch has 19 card(s). Write one excerpt for each.

CARDS
[
 {
  "id": "G0299",
  "industry": "rental housing portal",
  "problem": "deposit return delayed",
  "agent_style": "chatty",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent uses one of the phrases in a harmless sense (for example 'I'll call back by four with the answer')."
 },
 {
  "id": "G0301",
  "industry": "travel agency",
  "problem": "visa documents delayed",
  "agent_style": "hurried",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent says there is nothing they can do and ends the help."
 },
 {
  "id": "G0323",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "technical",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent uses one of the phrases in a harmless sense (for example 'I'll call back by four with the answer')."
 },
 {
  "id": "G0327",
  "industry": "hotel booking site",
  "problem": "double charge for one stay",
  "agent_style": "chatty",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent tells the customer to call back or contact someone else."
 },
 {
  "id": "G0332",
  "industry": "travel agency",
  "problem": "refund promised but not paid",
  "agent_style": "scripted",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent says there is nothing they can do and ends the help."
 },
 {
  "id": "G0359",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "hurried",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent uses one of the phrases in a harmless sense (for example 'I'll call back by four with the answer')."
 },
 {
  "id": "G0364",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "apologetic",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent blames another team or department and tells the customer to deal with them."
 },
 {
  "id": "G0395",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent uses one of the phrases in a harmless sense (for example 'I'll call back by four with the answer')."
 },
 {
  "id": "G0411",
  "industry": "hotel booking site",
  "problem": "booking confirmed but the hotel has no record",
  "agent_style": "apologetic",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent tells the customer to call back or contact someone else."
 },
 {
  "id": "G0436",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "stt",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent blames another team or department and tells the customer to deal with them."
 },
 {
  "id": "G0576",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "chatty",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent mentions another team or department but takes ownership: does the handoff themselves and tells the customer what they will do next."
 },
 {
  "id": "G0590",
  "industry": "appliance repair",
  "problem": "oven will not heat",
  "agent_style": "terse",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent mentions another team or department but takes ownership: does the handoff themselves and tells the customer what they will do next."
 },
 {
  "id": "G0592",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "terse",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent mentions another team or department but takes ownership: does the handoff themselves and tells the customer what they will do next."
 },
 {
  "id": "G0599",
  "industry": "streaming service",
  "problem": "billed twice this month",
  "agent_style": "scripted",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent mentions another team or department but takes ownership: does the handoff themselves and tells the customer what they will do next."
 },
 {
  "id": "G0603",
  "industry": "university student services",
  "problem": "course registration error",
  "agent_style": "scripted",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent uses one of the phrases in a harmless sense (for example 'I'll call back by four with the answer')."
 },
 {
  "id": "G0605",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "chatty",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent tells the customer to call back or contact someone else."
 },
 {
  "id": "G0674",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "apologetic",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent tells the customer to call back or contact someone else."
 },
 {
  "id": "G0677",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "chatty",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent blames another team or department and tells the customer to deal with them."
 },
 {
  "id": "G0703",
  "industry": "travel agency",
  "problem": "transfer not booked",
  "agent_style": "technical",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write 4 to 8 turns. One agent line MUST contain one of these exact phrases: \"call back\", \"another team\", \"billing team\", \"network team\", \"not my department\", \"nothing I can do\", \"can't do anything\", \"you'd have to\", \"contact them\", \"you'll have to ask\", \"another department\", \"that's their\".",
  "BEHAVIOUR": "The agent blames another team or department and tells the customer to deal with them."
 }
]
