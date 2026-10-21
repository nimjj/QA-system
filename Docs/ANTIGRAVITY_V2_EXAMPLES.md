# Worked examples for the V2 labels

These show **the label format and the line between PASS and FAIL**. They are deliberately tiny. Your calls must be 10 to 20 minutes long, with the events spread out over the whole call and written in your own words. **Do not copy the wording, names or scenarios below.** Rules and definitions: `Docs/ANTIGRAVITY_V2_COMMON.md`.

---

## 1. One toy call, with turn numbers, scores and markers

Turn index = 0-based position in the `transcript` array. Agent turns have no sentiment. Customer scores are noisy and come from that line alone.

| # | Speaker | Text | Customer score |
|---|---|---|---|
| 0 | Agent | Thank you for calling S-Net, this is Dev. How can I help you today? | none |
| 1 | Customer | My wifi drops out every evening. It's the black Hub 4X. | -11.8 |
| 2 | Agent | Sorry to hear that. Just to confirm, you're on the Fibre 150 plan, Priya? | none |
| 3 | Customer | Yes, that's right. | 1.9 |
| 4 | Agent | So what I'm hearing is the wifi on your Hub 4X cuts out most evenings. Have I got that right? | none |
| 5 | Customer | Yes, since Monday, and honestly I've had enough. I work from home and I lost a whole client call today! | -38.6 |
| 6 | Agent | Okay, what colour is the middle light on the router right now? | none |
| 7 | Customer | Orange. | -2.7 |
| 8 | Agent | Losing a client call is awful, I'm sorry about that. Let's get it sorted. | none |
| 9 | Customer | Thanks. I'll restart it now. | 14.2 |
| 10 | Agent | Great. Which router have you got there again? | none |
| 11 | Customer | It's the Hub 4X, like I said. | -19.4 |
| 12 | Agent | Obviously I can't see your router from here, so I do need you to confirm it. Thanks, Priya. | none |
| 13 | Customer | Okay. It's restarted. | -3.1 |
| 14 | Agent | Is the middle light still orange now that it's restarted? | none |
| 15 | Customer | No, it's green now. | 22.5 |
| 16 | Agent | That's basic stuff, you should have restarted it before you called. It's not difficult. | none |

Its markers and what they say about the ratings:

```json
"markers": {
  "active_listening": [
    {"kind": "repeat",           "premise_turn": 1, "agent_turn": 10, "reworded": true},
    {"kind": "harmless_recheck", "premise_turn": 7, "agent_turn": 14}
  ],
  "paraphrasing": [
    {"kind": "restatement",       "agent_turn": 4},
    {"kind": "not_a_restatement", "agent_turn": 2}
  ],
  "rapport": [
    {"kind": "rude",         "agent_turn": 16},
    {"kind": "blunt_but_ok", "agent_turn": 12}
  ],
  "empathy": [
    {"kind": "handled", "customer_turn": 5, "agent_turn": 8, "with_refusal": false}
  ]
}
```

- **Active listening = FAIL.** Turn 1 gave the router model; turn 10 asks for it again in other words. Turn 14 asks about the light *after a restart*, which may have changed, so it is a `harmless_recheck`, not a fault.
- **Paraphrasing = PASS.** Turn 4 restates the problem in the agent's words and checks it. Turn 2 only confirms the plan, so it is `not_a_restatement`.
- **Rapport = FAIL.** Turn 16 is condescending without a single insult. Turn 12 uses "Obviously" but is polite and explains why the agent is asking, so it is `blunt_but_ok`.
- **Empathy = PASS.** The outburst at turn 5 is recognised at turn 8, which is 3 turns later (inside the limit of 4), so it is `handled`, a late one. Had the sorry come at turn 10, it would be `unhandled`.

In a real call these events sit minutes apart. Do not stack them like this.

---

## 2. Pairs that must be told apart

Left: what the label is. Right: a line that looks similar but gets the opposite label. Invent your own versions.

### Active listening
| FAIL: `repeat` | PASS: `harmless_recheck` (or no marker) |
|---|---|
| Minute 2 customer: "The error code is CS-104." Minute 11 agent: "What was that error code again?" | Minute 2: "The error code is CS-104." Minute 11 agent: "Is it still showing CS-104 after the reboot?" (may have changed) |
| Customer gave the email in full and spelled it. Agent later: "And what email address should I send the token to?" | Customer gave only "it's kowalski something at gmail". Agent: "Can you spell the part before the 'at' for me?" (information was partial) |
| Customer: "I'm on the 150 package." Later agent: "Which speed tier are you on, the 150 or the 300?" (reworded, far apart) | Customer: "I'm on the 150 package." Agent: "What speed are you actually getting on the speed test?" (different detail of the same topic) |
| Customer: "My landline is dead too." Agent, 8 minutes on: "Is the landline working?" | Customer: "I'm going to unplug it." Agent: "Just to confirm before I reset it, you want to keep your saved channels, yes?" (confirming before an irreversible step) |

### Paraphrasing
| FAIL: no `restatement` (maybe `not_a_restatement`) | PASS: has a `restatement` |
|---|---|
| Customer: "My box keeps rebooting." Agent: "Your box keeps rebooting. Okay." (echo) | Agent: "So the box restarts by itself every time you pick a channel, and that began after the update on Tuesday. Is that right?" |
| Agent: "Just to confirm, you're on Fibre 150 at 12 Marlow Road?" (account details) | Agent, at minute 9: "Let me check I've got the whole picture: the drops started Monday, they only happen on wifi, and the cable connection is fine, correct?" (late, but a real restatement) |
| Agent: "Right, so I'll send an engineer on Friday." (next steps) | Agent: "So you can't get your emails on the new phone, but the old one is fine, have I understood?" |
| Agent: "Okay, got it, thanks." | Agent: "What you're telling me is the bill doubled in March without any change to your plan. Have I got that?" |

### Rapport
| FAIL: `rude` | PASS: `blunt_but_ok` |
|---|---|
| "If you'd read the email we sent you'd know that." (condescending) | "As I said, the earliest slot is Friday. I know that's not what you hoped, I'm sorry." (same trigger words, respectful) |
| "Oh brilliant, another person who hasn't tried switching it off and on." (sarcasm) | "I need you to switch it off and on first. It fixes most of these." (brisk) |
| "That's basic stuff, it's not difficult." (belittling, no insult) | "No, I can't change that. It's a system rule." (short, firm, not rude) |
| "That's not my department, take it up with billing." (also an Ownership fault) | "Obviously I can't see your screen, so please read me what it says." (polite request) |

A rude line can sit in the middle of a long, warm, helpful call. Do not put every one near the start or the end.

### Empathy (strict, per outburst)
| FAIL: an `unhandled` outburst | PASS: every outburst `handled` |
|---|---|
| Customer: "Three days without internet, this is ridiculous!" Agent (next turn): "The policy says 30 days. Can I take your account number?" | Same customer line. Agent: "Three days is awful, I'm sorry. Let me look at this now." (distance 1) |
| Same customer line. Agent: asks two technical questions, customer answers twice, and "sorry about that" only comes 6 turns later (too late) | Same customer line. Agent: asks one technical question, customer answers, then "I can hear how frustrating this has been" (distance 3, late but inside 4) |
| Minute 3 outburst handled warmly. Minute 14 a second outburst ("You're joking, another fee?") gets "That's the charge." (one unhandled outburst fails the call) | Customer: "You're telling me I pay the fee again? That's outrageous." Agent: "I completely understand why that's upsetting. Unfortunately I can't waive it." (`handled`, `"with_refusal": true`) |
| Customer is clearly distressed. Agent only says "Okay. Account number?" | Customer is calm and factual the whole call. Nothing to mark, `"empathy": []`, PASS. |

---

## 3. A good call is not a boring call

Excellent calls (everything PASS) should still contain `harmless_recheck`, `not_a_restatement`, `blunt_but_ok` and `handled` events. FAIL calls should often be long and polite apart from one fault. Quality must never show in style, length or politeness; see rulebook 9.4.
