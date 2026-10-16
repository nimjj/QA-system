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
  "id": "G0199",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "apologetic",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."
 },
 {
  "id": "G0200",
  "industry": "retail bank",
  "problem": "unknown charge on the statement",
  "agent_style": "apologetic",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "Near the end the agent asks the customer to confirm the issue is fixed and states it is resolved; the customer confirms."
 },
 {
  "id": "G0204",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "chatty",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says a ticket or another team will follow up, and the call closes with the issue still open."
 },
 {
  "id": "G0213",
  "industry": "rental housing portal",
  "problem": "rent payment not recorded",
  "agent_style": "terse",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent confirms it works for the customer WITHOUT using the words 'resolved' or 'fixed' (for example 'so everything's working again for you?') and the customer says yes."
 },
 {
  "id": "G0215",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it is still not working and the agent closes the call anyway, with a promise or an excuse."
 },
 {
  "id": "G0222",
  "industry": "auto insurance",
  "problem": "repair shop approval delayed",
  "agent_style": "apologetic",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it is still not working and the agent closes the call anyway, with a promise or an excuse."
 },
 {
  "id": "G0223",
  "industry": "mobile carrier",
  "problem": "data not working abroad",
  "agent_style": "warm",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says a ticket or another team will follow up, and the call closes with the issue still open."
 },
 {
  "id": "G0230",
  "industry": "hotel booking site",
  "problem": "cancellation refund not received",
  "agent_style": "scripted",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."
 },
 {
  "id": "G0232",
  "industry": "water utility",
  "problem": "low pressure since a repair",
  "agent_style": "chatty",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says something like 'I'll mark this as resolved on my side' without asking the customer whether it works, and closes."
 },
 {
  "id": "G0234",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "chatty",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent only asks 'is there anything else I can help with?' and closes."
 },
 {
  "id": "G0237",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "chatty",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says it 'should be fine now' and closes without asking the customer to confirm."
 },
 {
  "id": "G0246",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "scripted",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent explicitly confirms the issue is resolved, then there is small talk and a survey mention before the call ends (the confirmation is still within the last 8 to 10 turns)."
 },
 {
  "id": "G0253",
  "industry": "university student services",
  "problem": "transcript request is stuck",
  "agent_style": "terse",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent explicitly confirms the issue is resolved, then there is small talk and a survey mention before the call ends (the confirmation is still within the last 8 to 10 turns)."
 },
 {
  "id": "G0260",
  "industry": "airline",
  "problem": "seat selection will not save",
  "agent_style": "apologetic",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "Near the end the agent asks the customer to confirm the issue is fixed and states it is resolved; the customer confirms."
 },
 {
  "id": "G0273",
  "industry": "auto insurance",
  "problem": "premium rose without explanation",
  "agent_style": "chatty",
  "customer_mood": "polite",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says it 'should be fine now' and closes without asking the customer to confirm."
 },
 {
  "id": "G0286",
  "industry": "travel agency",
  "problem": "transfer not booked",
  "agent_style": "warm",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."
 },
 {
  "id": "G0290",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "technical",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "Near the end the agent asks the customer to confirm the issue is fixed and states it is resolved; the customer confirms."
 },
 {
  "id": "G0303",
  "industry": "travel agency",
  "problem": "visa documents delayed",
  "agent_style": "warm",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says something like 'I'll mark this as resolved on my side' without asking the customer whether it works, and closes."
 },
 {
  "id": "G0305",
  "industry": "credit card company",
  "problem": "new card never arrived",
  "agent_style": "hurried",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent confirms it works for the customer WITHOUT using the words 'resolved' or 'fixed' (for example 'so everything's working again for you?') and the customer says yes."
 },
 {
  "id": "G0312",
  "industry": "pharmacy",
  "problem": "insurance claim rejected at the counter",
  "agent_style": "formal",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says a ticket or another team will follow up, and the call closes with the issue still open."
 },
 {
  "id": "G0334",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "technical",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "Near the end the agent asks the customer to confirm the issue is fixed and states it is resolved; the customer confirms."
 },
 {
  "id": "G0348",
  "industry": "gym membership",
  "problem": "access card stopped working",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it is still not working and the agent closes the call anyway, with a promise or an excuse."
 },
 {
  "id": "G0349",
  "industry": "airline",
  "problem": "flight cancelled and rebooking options are too late",
  "agent_style": "scripted",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it is still not working and the agent closes the call anyway, with a promise or an excuse."
 },
 {
  "id": "G0357",
  "industry": "hotel booking site",
  "problem": "double charge for one stay",
  "agent_style": "technical",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."
 },
 {
  "id": "G0363",
  "industry": "credit card company",
  "problem": "fraudulent charge on the card",
  "agent_style": "apologetic",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent only asks 'is there anything else I can help with?' and closes."
 },
 {
  "id": "G0368",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "terse",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."
 },
 {
  "id": "G0372",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "apologetic",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent only asks 'is there anything else I can help with?' and closes."
 },
 {
  "id": "G0377",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "formal",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says something like 'I'll mark this as resolved on my side' without asking the customer whether it works, and closes."
 }
]
