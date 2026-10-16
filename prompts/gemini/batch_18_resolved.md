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
  "id": "G0527",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "formal",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it is still not working and the agent closes the call anyway, with a promise or an excuse."
 },
 {
  "id": "G0529",
  "industry": "electric utility",
  "problem": "outage lasted all night",
  "agent_style": "warm",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says it 'should be fine now' and closes without asking the customer to confirm."
 },
 {
  "id": "G0536",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "technical",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "Near the end the agent asks the customer to confirm the issue is fixed and states it is resolved; the customer confirms."
 },
 {
  "id": "G0548",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "apologetic",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says a ticket or another team will follow up, and the call closes with the issue still open."
 },
 {
  "id": "G0554",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "warm",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent only asks 'is there anything else I can help with?' and closes."
 },
 {
  "id": "G0564",
  "industry": "food delivery app",
  "problem": "order arrived cold and incomplete",
  "agent_style": "terse",
  "customer_mood": "calm",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent explicitly confirms the issue is resolved, then there is small talk and a survey mention before the call ends (the confirmation is still within the last 8 to 10 turns)."
 },
 {
  "id": "G0568",
  "industry": "rental housing portal",
  "problem": "maintenance request ignored",
  "agent_style": "scripted",
  "customer_mood": "sarcastic",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it is still not working and the agent closes the call anyway, with a promise or an excuse."
 },
 {
  "id": "G0569",
  "industry": "electric utility",
  "problem": "smart meter display is blank",
  "agent_style": "chatty",
  "customer_mood": "rushed",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."
 },
 {
  "id": "G0570",
  "industry": "credit card company",
  "problem": "rewards points missing",
  "agent_style": "hurried",
  "customer_mood": "angry",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says something like 'I'll mark this as resolved on my side' without asking the customer whether it works, and closes."
 },
 {
  "id": "G0571",
  "industry": "S-Net satellite internet",
  "problem": "router light stuck on orange",
  "agent_style": "technical",
  "customer_mood": "elderly and slow-talking",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says a ticket or another team will follow up, and the call closes with the issue still open."
 },
 {
  "id": "G0575",
  "industry": "appliance repair",
  "problem": "fridge rattles and the freezer is warm",
  "agent_style": "hurried",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "Near the end the agent asks the customer to confirm the issue is fixed and states it is resolved; the customer confirms."
 },
 {
  "id": "G0577",
  "industry": "hotel booking site",
  "problem": "cancellation refund not received",
  "agent_style": "terse",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "Near the end the agent asks the customer to confirm the issue is fixed and states it is resolved; the customer confirms."
 },
 {
  "id": "G0584",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "formal",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent confirms it works for the customer WITHOUT using the words 'resolved' or 'fixed' (for example 'so everything's working again for you?') and the customer says yes."
 },
 {
  "id": "G0602",
  "industry": "SaaS software",
  "problem": "cannot log in after a password reset",
  "agent_style": "warm",
  "customer_mood": "anxious",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent confirms it works for the customer WITHOUT using the words 'resolved' or 'fixed' (for example 'so everything's working again for you?') and the customer says yes."
 },
 {
  "id": "G0607",
  "industry": "pharmacy",
  "problem": "prescription refill not ready",
  "agent_style": "apologetic",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says something like 'I'll mark this as resolved on my side' without asking the customer whether it works, and closes."
 },
 {
  "id": "G0613",
  "industry": "credit card company",
  "problem": "late fee charged though paid on time",
  "agent_style": "hurried",
  "customer_mood": "confused",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent only asks 'is there anything else I can help with?' and closes."
 },
 {
  "id": "G0615",
  "industry": "auto insurance",
  "problem": "premium rose without explanation",
  "agent_style": "hurried",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "Near the end the agent asks the customer to confirm the issue is fixed and states it is resolved; the customer confirms."
 },
 {
  "id": "G0636",
  "industry": "water utility",
  "problem": "low pressure since a repair",
  "agent_style": "apologetic",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says it 'should be fine now' and closes without asking the customer to confirm."
 },
 {
  "id": "G0650",
  "industry": "car rental",
  "problem": "damage charge disputed",
  "agent_style": "apologetic",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent explicitly confirms the issue is resolved, then there is small talk and a survey mention before the call ends (the confirmation is still within the last 8 to 10 turns)."
 },
 {
  "id": "G0661",
  "industry": "S-Net satellite internet",
  "problem": "internet drops every evening",
  "agent_style": "technical",
  "customer_mood": "calm",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent confirms it works for the customer WITHOUT using the words 'resolved' or 'fixed' (for example 'so everything's working again for you?') and the customer says yes."
 },
 {
  "id": "G0679",
  "industry": "hotel booking site",
  "problem": "room type differs from what was booked",
  "agent_style": "warm",
  "customer_mood": "angry",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says it 'should be fine now' and closes without asking the customer to confirm."
 },
 {
  "id": "G0686",
  "industry": "car rental",
  "problem": "unexpected fee after returning the car",
  "agent_style": "formal",
  "customer_mood": "rushed",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."
 },
 {
  "id": "G0692",
  "industry": "rental housing portal",
  "problem": "deposit return delayed",
  "agent_style": "scripted",
  "customer_mood": "confused",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent confirms it works for the customer WITHOUT using the words 'resolved' or 'fixed' (for example 'so everything's working again for you?') and the customer says yes."
 },
 {
  "id": "G0700",
  "industry": "credit card company",
  "problem": "late fee charged though paid on time",
  "agent_style": "warm",
  "customer_mood": "elderly and slow-talking",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "Near the end the agent asks the customer to confirm the issue is fixed and states it is resolved; the customer confirms."
 },
 {
  "id": "G0701",
  "industry": "S-Net satellite internet",
  "problem": "speeds far below the paid plan",
  "agent_style": "apologetic",
  "customer_mood": "polite",
  "style": "clean",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent says a ticket or another team will follow up, and the call closes with the issue still open."
 },
 {
  "id": "G0704",
  "industry": "credit card company",
  "problem": "rewards points missing",
  "agent_style": "terse",
  "customer_mood": "sarcastic",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The customer says it works now; the agent says that's great and explicitly confirms it is sorted before closing."
 },
 {
  "id": "G0705",
  "industry": "streaming service",
  "problem": "video buffers on the living room tv",
  "agent_style": "terse",
  "customer_mood": "anxious",
  "style": "stt",
  "STRUCTURE": "Write ONLY the final 8 to 10 turns of a call (the ending), as if the earlier part had already happened.",
  "BEHAVIOUR": "The agent explicitly confirms the issue is resolved, then there is small talk and a survey mention before the call ends (the confirmation is still within the last 8 to 10 turns)."
 }
]
