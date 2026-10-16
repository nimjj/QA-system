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
  "id": "G0006",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "terse",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."
 },
 {
  "id": "G0013",
  "industry": "retail bank",
  "problem": "mortgage payment taken twice",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent explicitly confirms the issue is resolved, then there is small talk and a survey mention before the call ends (the confirmation is still within the last 8 to 10 turns)."
 },
 {
  "id": "G0028",
  "industry": "travel agency",
  "problem": "package holiday changed without notice",
  "agent_style": "chatty",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says it 'should be fine now' and closes without asking the customer to confirm."
 },
 {
  "id": "G0033",
  "industry": "water utility",
  "problem": "low pressure since a repair",
  "agent_style": "hurried",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it is still not working and the agent closes the call anyway, with a promise or an excuse."
 },
 {
  "id": "G0035",
  "industry": "rental housing portal",
  "problem": "lease document will not download",
  "agent_style": "scripted",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it is still not working and the agent closes the call anyway, with a promise or an excuse."
 },
 {
  "id": "G0042",
  "industry": "food delivery app",
  "problem": "driver marked it delivered but it never came",
  "agent_style": "hurried",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says it 'should be fine now' and closes without asking the customer to confirm."
 },
 {
  "id": "G0043",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "hurried",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent explicitly confirms the issue is resolved, then there is small talk and a survey mention before the call ends (the confirmation is still within the last 8 to 10 turns)."
 },
 {
  "id": "G0044",
  "industry": "pharmacy",
  "problem": "wrong dose label",
  "agent_style": "chatty",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says it 'should be fine now' and closes without asking the customer to confirm."
 },
 {
  "id": "G0045",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "scripted",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "Near the end the agent asks the customer to confirm the issue is fixed and states it is resolved; the customer confirms."
 },
 {
  "id": "G0049",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "formal",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says a ticket or another team will follow up, and the call closes with the issue still open."
 },
 {
  "id": "G0055",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "technical",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent explicitly confirms the issue is resolved, then there is small talk and a survey mention before the call ends (the confirmation is still within the last 8 to 10 turns)."
 },
 {
  "id": "G0085",
  "industry": "water utility",
  "problem": "low pressure since a repair",
  "agent_style": "chatty",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says something like 'I'll mark this as resolved on my side' without asking the customer whether it works, and closes."
 },
 {
  "id": "G0106",
  "industry": "streaming service",
  "problem": "no sound in the app",
  "agent_style": "hurried",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says something like 'I'll mark this as resolved on my side' without asking the customer whether it works, and closes."
 },
 {
  "id": "G0116",
  "industry": "SaaS software",
  "problem": "cannot log in after a password reset",
  "agent_style": "formal",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent confirms it works for the customer WITHOUT using the words 'resolved' or 'fixed' (for example 'so everything's working again for you?') and the customer says yes."
 },
 {
  "id": "G0124",
  "industry": "SaaS software",
  "problem": "export keeps failing",
  "agent_style": "warm",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."
 },
 {
  "id": "G0133",
  "industry": "S-Net satellite internet",
  "problem": "new equipment will not connect after a move",
  "agent_style": "technical",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it is still not working and the agent closes the call anyway, with a promise or an excuse."
 },
 {
  "id": "G0135",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "formal",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent confirms it works for the customer WITHOUT using the words 'resolved' or 'fixed' (for example 'so everything's working again for you?') and the customer says yes."
 },
 {
  "id": "G0138",
  "industry": "pharmacy",
  "problem": "delivery missed twice",
  "agent_style": "scripted",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent only asks 'is there anything else I can help with?' and closes."
 },
 {
  "id": "G0146",
  "industry": "auto insurance",
  "problem": "repair shop approval delayed",
  "agent_style": "terse",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent only asks 'is there anything else I can help with?' and closes."
 },
 {
  "id": "G0152",
  "industry": "SaaS software",
  "problem": "export keeps failing",
  "agent_style": "hurried",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent only asks 'is there anything else I can help with?' and closes."
 },
 {
  "id": "G0167",
  "industry": "SaaS software",
  "problem": "export keeps failing",
  "agent_style": "scripted",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent confirms it works for the customer WITHOUT using the words 'resolved' or 'fixed' (for example 'so everything's working again for you?') and the customer says yes."
 },
 {
  "id": "G0168",
  "industry": "water utility",
  "problem": "bill doubled after a meter swap",
  "agent_style": "formal",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says a ticket or another team will follow up, and the call closes with the issue still open."
 },
 {
  "id": "G0169",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "chatty",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent explicitly confirms the issue is resolved, then there is small talk and a survey mention before the call ends (the confirmation is still within the last 8 to 10 turns)."
 },
 {
  "id": "G0179",
  "industry": "gym membership",
  "problem": "joining fee charged twice",
  "agent_style": "warm",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."
 },
 {
  "id": "G0182",
  "industry": "car rental",
  "problem": "app will not unlock the car",
  "agent_style": "formal",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."
 },
 {
  "id": "G0184",
  "industry": "streaming service",
  "problem": "no sound in the app",
  "agent_style": "scripted",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent explicitly confirms the issue is resolved, then there is small talk and a survey mention before the call ends (the confirmation is still within the last 8 to 10 turns)."
 },
 {
  "id": "G0188",
  "industry": "electric utility",
  "problem": "smart meter display is blank",
  "agent_style": "warm",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent confirms it works for the customer WITHOUT using the words 'resolved' or 'fixed' (for example 'so everything's working again for you?') and the customer says yes."
 },
 {
  "id": "G0195",
  "industry": "rental housing portal",
  "problem": "deposit return delayed",
  "agent_style": "apologetic",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent only asks 'is there anything else I can help with?' and closes."
 }
]
