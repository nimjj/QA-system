import json
import sys
import os
sys.path.insert(0, os.path.abspath("."))
from src.services.rule_engine import evaluate_branding, evaluate_hold_and_dead_air, evaluate_verified_customer, evaluate_personalized_call
from Scripts.validate_calls import SPEC, final_score

def mmss(sec):
    return f"[{sec//60:02d}:{sec%60:02d}]"

cid = "agt_020"
cname = "Clara"
target_dur = 1127

raw = [
    # 00
    ("Agent", "Thank you for calling S-Net customer services, my name is Darren. How can I help you today?", None),
    # 01
    ("Customer", "Hello Darren. My name is Clara Oswald. I have an urgent issue with my home phone. I am trying to call my family in Sydney, Australia, but every single call is instantly blocked by an automated message.", -24.8),
    # 02
    ("Agent", "Good morning Clara. I can check your telephone line features. Before we inspect your line provisioning, could you please confirm your full postal address and your account security PIN?", None),
    # 03
    ("Customer", "Yes, my address is 42 Westbourne Gardens, Glasgow, G12 9PF, and my security PIN is 7731. The Sydney number I am trying to call is 0061 2 9385 1199.", -8.4),
    # 04
    ("Agent", "Thank you Clara, that verifies your account. What does the automated announcement say when you attempt to dial Australia?", None),
    # 05
    ("Customer", "It says: Calls to this international destination are barred from this telephone line. Our landline number here in Glasgow is 0141 496 0822.", -18.2),
    # 06
    ("Agent", "So if I understand the situation correctly, Clara, you have been trying to reach your family in Sydney on the international prefix 0061, but every call is rejected with an automated barring announcement, and you need that international call restriction removed immediately, is that right?", None),
    # 07
    ("Customer", "Yes, exactly that. It was working fine last month when I called my sister, but today it refuses to connect.", -12.1),
    # 08 [Managed hold announcement]
    ("Agent", "Bear with me for a couple of minutes while I open your voice telephony routing profile on our central network switch.", None),
    # 09 [Hold 1 return]
    ("Agent", "Thank you for waiting, Clara. I am inspecting your switch line features. The account currently has the standard international call barring option enabled at the local exchange layer.", None),
    # 10
    ("Customer", "Why on earth would that be turned on? I never asked anyone to bar my calls to Australia!", -28.6),
    # 11 [Outburst 1]
    ("Customer", "My mother is eighty-four and had a sudden hospital scare this morning, and every time I dial it just beeps and cuts off! I am terrified something has happened to her and I cannot even reach her hospital bedside!", -52.4),
    # 12 [Agent procedural]
    ("Agent", "I need to check the call feature barring profile on our central exchange switch.", None),
    # 13 [Customer reply]
    ("Customer", "Please check it as quickly as possible, I am trembling with worry.", -33.1),
    # 14 [Agent late handled with refusal, distance 3!]
    ("Agent", "I can hear how terrifying that situation is with your mother in hospital, Clara, but unfortunately under company security policy I cannot lift an international high-rate bar on a standard call without sending a one-time passcode to the account mobile phone first.", None),
    # 15
    ("Customer", "That is fine, send the code to my mobile right now! Anything to get this sorted quickly.", -14.2),
    # 16
    ("Agent", "I have dispatched the six-digit verification code via SMS to the mobile number registered on file ending in 502.", None),
    # 17
    ("Customer", "I have my mobile here. The code just arrived: it is 839 201.", 4.1),
    # 18
    ("Agent", "Thank you. That security token authenticates the request to modify call barring on your telephone line.", None),
    # 19
    ("Customer", "Can you tell me how this bar got put on my phone in the first place?", -16.5),
    # 20 [Rude line in middle third]
    ("Agent", "Well if you had actually checked your monthly bill insert last month, you would know all residential accounts had international premium calling barred by default for fraud prevention.", None),
    # 21
    ("Customer", "You do not have to speak to me with such condescension! I am an anxious customer trying to contact my sick mother, not an idiot who needs scolding about bill inserts.", -41.3),
    # 22
    ("Agent", "I am stating the company billing procedure. I am now unchecking the international outgoing call bar on the switch console.", None),
    # 23
    ("Customer", "How long does the switch take to update once you uncheck it?", -11.9),
    # 24 [Harmless recheck: premise turn 05, 19 turns later]
    ("Agent", "And before I update the network barring profile on our switch, that UK landline number was 0141 496 0822, correct?", None),
    # 25
    ("Customer", "Yes, 0141 496 0822. That is our home number.", 2.3),
    # 26
    ("Agent", "Give me a moment while the exchange provisioning system commits the change across the digital local loop.", None),
    # 27
    ("Customer", "Once it is unbarred, will my calls definitely go through to Sydney without any connection drops?", -9.2),
    # 28 [Ownership fault: deflecting to Telstra]
    ("Agent", "Once the call leaves the UK gateway, Telstra Australia handles the routing. Any connection problems down there are Telstra's responsibility, not ours.", None),
    # 29
    ("Customer", "I understand that other networks are involved, but surely S-Net manages the handoff reliably.", -15.4),
    # 30 [blunt_but_ok]
    ("Agent", "Obviously international calling features carry significant toll fraud risk, so the network switch applies strict automated limits.", None),
    # 31
    ("Customer", "I understand the need for fraud prevention, but people have families overseas they need to speak with.", -8.7),
    # 32
    ("Agent", "The system has submitted the unbarring instruction. It takes between five and ten minutes to propagate through the regional tandem exchange.", None),
    # 33
    ("Customer", "Five to ten minutes? Is there any way to expedite it?", -20.1),
    # 34
    ("Agent", "No, exchange batches run on automated five-minute cycles. We have to wait for the next cycle acknowledgment.", None),
    # 35
    ("Customer", "Okay, I will wait on the line.", -1.2),
    # 36 [Active listening repeat: Australian number asked again, 6+ min later]
    ("Agent", "What was the exact Australian telephone number you were trying to dial again?", None),
    # 37
    ("Customer", "I gave you that right at the start! It is 0061 2 9385 1199, Sydney, Australia.", -27.5),
    # 38
    ("Agent", "I have entered that destination number into the call routing diagnostic monitor to watch for the next outbound attempt.", None),
    # 39
    ("Customer", "Thank you. Do I need to dial any special area codes or just the standard international format?", -3.6),
    # 40 [Harmless recheck in last third: premise turn 03, agent turn 40, 40/57 = 0.70 >= 0.66]
    ("Agent", "You dial 00, then 61 for Australia, then drop the leading zero. And just to confirm the local Sydney number before you dial, that was 9385 1199, correct?", None),
    # 41
    ("Customer", "Right, 9385 1199. That is exactly what I dialled from my handset.", 3.4),
    # 42 [Managed hold announcement]
    ("Agent", "Bear with me for two minutes while I query the exchange database for the completion receipt of the unbarring batch.", None),
    # 43 [Hold 2 return]
    ("Agent", "Thank you for waiting, Clara. The regional tandem switch has officially acknowledged the modification. The international bar has been cleared.", None),
    # 44
    ("Customer", "Is it completely active right now or do we still need to wait?", -6.8),
    # 45
    ("Agent", "The switch queue indicates processing is ninety percent complete. It should be fully active in two moments.", None),
    # 46
    ("Customer", "Can I try dialling it now while we are talking?", -5.1),
    # 47 [Outburst 2 in last third: 47/57 = 0.82]
    ("Customer", "I have been on this phone for over fifteen minutes while my sick mother is waiting for me to call Sydney! Why is this taking so long when it is just a switch setting?! I am getting so stressed out!", -51.8),
    # 48 [Agent unhandled: purely procedural]
    ("Agent", "The switch update takes thirty seconds. I am waiting for the confirmation flag on my terminal.", None),
    # 49
    ("Customer", "Fine. Tell me when to dial.", -19.4),
    # 50
    ("Agent", "The green status indicator has appeared. Please pick up your cordless handset and dial the full Australian number now.", None),
    # 51
    ("Customer", "Okay, dialling 00 61 2 9385 1199 now... Hearing tones... It is ringing! The Australian double ring tone is ringing!", 29.5),
    # 52
    ("Agent", "That confirms the international bar is completely lifted and outgoing international calls are routing successfully.", None),
    # 53
    ("Customer", "Someone picked up in Sydney! Hello, yes, it connected! I can hear my sister clearly! Thank you, I need to speak to them right away.", 38.2),
    # 54
    ("Agent", "I will let you proceed with your family call immediately, Clara.", None),
    # 55
    ("Customer", "Thank you, goodbye.", 7.2),
    # 56
    ("Agent", "Thank you for choosing S-Net today, Clara. Goodbye.", None)
]

word_counts = [len(t[1].split()) for t in raw]
durs = [max(4, min(24, int(w / 2.3))) for w in word_counts]
durs[-1] = 6

# Forward simulation to ensure strictly no overlap and valid dead air
# Target duration 1127.
# Total turns = 57.
# Holds at i=8->9 and i=42->43.
transcript = []
curr = 0
for i, (spk, txt, score) in enumerate(raw):
    dur = durs[i]
    st = curr
    et = st + dur
    turn_dict = {
        "speaker": spk,
        "start_time": mmss(st),
        "end_time": mmss(et),
        "start_time_sec": st,
        "text": txt
    }
    if spk == "Customer":
        turn_dict["sentiment_score"] = round(float(score), 1)
    transcript.append(turn_dict)
    
    # Calculate next start
    if i < len(raw) - 1:
        if i == 8 or i == 42:
            # Managed hold: gap in app formula is start_next - (st + 10). Let gap = 85s -> start_next = st + 10 + 85 = st + 95
            curr = max(et + 1, st + 95)
        else:
            # Normal transition: pause of ~3-5s
            curr = et + 3

# Now scale the normal pauses so the last turn finishes exactly at target_dur
current_end = transcript[-1]["start_time_sec"] + durs[-1]
diff = target_dur - current_end
print("Current natural end:", current_end, "Diff:", diff)

# Add diff across the 54 normal transitions
normal_indices = [i for i in range(len(raw) - 1) if i not in (8, 42)]
extra_per = diff // len(normal_indices)
extra_rem = diff % len(normal_indices)

curr = 0
transcript = []
for i, (spk, txt, score) in enumerate(raw):
    dur = durs[i]
    st = curr
    et = st + dur
    turn_dict = {
        "speaker": spk,
        "start_time": mmss(st),
        "end_time": mmss(et),
        "start_time_sec": st,
        "text": txt
    }
    if spk == "Customer":
        turn_dict["sentiment_score"] = round(float(score), 1)
    transcript.append(turn_dict)
    
    if i < len(raw) - 1:
        if i == 8 or i == 42:
            curr = max(et + 1, st + 95)
        else:
            add = extra_per + (1 if normal_indices.index(i) < extra_rem else 0)
            curr = et + 3 + add

transcript[-1]["end_time"] = mmss(target_dur)
print("Adjusted last end:", transcript[-1]["end_time"], "sec:", transcript[-1]["start_time_sec"] + durs[-1])

# Validate rule items
tl = [(t["speaker"], t["text"]) for t in transcript]
tm = [(t["start_time_sec"], t["start_time_sec"] + 10) for t in transcript]

b_res = evaluate_branding(tl)
d_res = evaluate_hold_and_dead_air(tl, tm)
v_res = evaluate_verified_customer(tl, tm)
p_res = evaluate_personalized_call(tl, cname)

print("Branding:", b_res["rating"])
print("Dead Air:", d_res["rating"])
print("Verified:", v_res["rating"])
print("Personalized:", p_res["rating"])

# Write agt_020.json
payload = {
    "tenant_id": "tenant-abc",
    "customer_name": cname,
    "transcript": transcript
}

with open(f"inputs/AG-T/{cid}.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)
    f.write("\n")

ratings = {
    "Branding and Survey Check": "PASS",
    "Hold time and Dead Air": "PASS",
    "Verified customer": "PASS",
    "Personalized the call/ticket appropriately": "PASS",
    "Empathy & Acknowledgment Statement": "FAIL",
    "Paraphrasing": "PASS",
    "Active listening": "FAIL",
    "Took ownership of the problem": "FAIL",
    "Build rapport and observed professionalism": "FAIL",
    "Probing": "FAIL",
    "Confirmed the issue is resolved": "PASS"
}

coaching_map = {
    "Empathy & Acknowledgment Statement": f"Ignored customer distress and anxiety at {transcript[47]['start_time']} during delay in unbarring international calls.",
    "Active listening": f"Asked customer for the Australian destination phone number again at {transcript[36]['start_time']} after customer gave it clearly at {transcript[3]['start_time']}.",
    "Took ownership of the problem": f"Deflected responsibility at {transcript[28]['start_time']} by stating routing problems in Australia were Telstra's responsibility rather than owning customer inquiry.",
    "Build rapport and observed professionalism": f"Spoke condescendingly to customer at {transcript[20]['start_time']} by telling her she should have checked her monthly bill insert.",
    "Probing": "Failed to ask diagnostic probing questions regarding previous international calling patterns or handset call settings."
}

scorecard = []
for cat, nm, ded in SPEC:
    r = ratings[nm]
    c = coaching_map.get(nm, "") if r == "FAIL" else ""
    scorecard.append({
        "category": cat,
        "name": nm,
        "rating": r,
        "coaching": c
    })

sc = final_score(scorecard, False)

grader_items = [
    {
        "name": "Branding and Survey Check",
        "rating": "PASS",
        "confidence": "clear",
        "evidence": f"Agent opened with 'Thank you for calling S-Net customer services' at {transcript[0]['start_time']} and closed with 'Thank you for choosing S-Net today' at {transcript[56]['start_time']}."
    },
    {
        "name": "Hold time and Dead Air",
        "rating": "PASS",
        "confidence": "clear",
        "evidence": "Holds were properly announced with bear with me and thanked upon return without unmanaged dead air."
    },
    {
        "name": "Verified customer",
        "rating": "PASS",
        "confidence": "clear",
        "evidence": f"Verified full address and security PIN at {transcript[2]['start_time']} within first 240 seconds."
    },
    {
        "name": "Personalized the call/ticket appropriately",
        "rating": "PASS",
        "confidence": "clear",
        "evidence": "Agent addressed customer by first name Clara naturally throughout the call."
    },
    {
        "name": "Empathy & Acknowledgment Statement",
        "rating": "FAIL",
        "confidence": "clear",
        "evidence": f"{transcript[47]['start_time']} Customer: 'I have been on this phone for over fifteen minutes while my sick mother is waiting for me to call Sydney...' ... {transcript[48]['start_time']} Agent: 'The switch update takes thirty seconds.'"
    },
    {
        "name": "Paraphrasing",
        "rating": "PASS",
        "confidence": "clear",
        "evidence": f"Agent restated international call barring issue in own words at {transcript[6]['start_time']}: 'So if I understand the situation correctly, Clara...'"
    },
    {
        "name": "Active listening",
        "rating": "FAIL",
        "confidence": "clear",
        "evidence": f"{transcript[3]['start_time']} Customer: 'The Sydney number I am trying to call is 0061 2 9385 1199.' ... {transcript[36]['start_time']} Agent: 'What was the exact Australian telephone number you were trying to dial again?'"
    },
    {
        "name": "Took ownership of the problem",
        "rating": "FAIL",
        "confidence": "clear",
        "evidence": f"{transcript[28]['start_time']} Agent: 'Once the call leaves the UK gateway, Telstra Australia handles the routing. Any connection problems down there are Telstra's responsibility, not ours.'"
    },
    {
        "name": "Build rapport and observed professionalism",
        "rating": "FAIL",
        "confidence": "clear",
        "evidence": f"{transcript[20]['start_time']} Agent: 'Well if you had actually checked your monthly bill insert last month, you would know all residential accounts had international premium calling barred by default for fraud prevention.'"
    },
    {
        "name": "Probing",
        "rating": "FAIL",
        "confidence": "clear",
        "evidence": "Agent did not probe into line history or international calling features."
    },
    {
        "name": "Confirmed the issue is resolved",
        "rating": "PASS",
        "confidence": "clear",
        "evidence": f"Customer successfully dialled Sydney and confirmed ringing tone and connection to family at {transcript[51]['start_time']}."
    }
]

markers = {
    "active_listening": [
        {"kind": "repeat", "premise_turn": 3, "agent_turn": 36, "reworded": True},
        {"kind": "harmless_recheck", "premise_turn": 5, "agent_turn": 24},
        {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 40}
    ],
    "paraphrasing": [
        {"kind": "restatement", "agent_turn": 6},
        {"kind": "not_a_restatement", "agent_turn": 4}
    ],
    "rapport": [
        {"kind": "rude", "agent_turn": 20},
        {"kind": "blunt_but_ok", "agent_turn": 30}
    ],
    "empathy": [
        {"kind": "handled", "customer_turn": 11, "agent_turn": 14, "with_refusal": True},
        {"kind": "unhandled", "customer_turn": 47}
    ]
}

expected = {
    "call_id": cid,
    "tenant_id": "tenant-abc",
    "status": "completed",
    "result": {
        "final_score": sc,
        "is_auto_fail": False,
        "auto_fail_reason": None,
        "scorecard": scorecard
    },
    "grader": {
        "graded_by": "Antigravity (gemini-3.8-flash)",
        "graded_on": "2026-10-21",
        "scenario": "International call barring accidentally enabled, blocking calls to family in Australia",
        "tier": "poor",
        "duration_sec": target_dur,
        "notes": "Agent successfully unbarred international calling after verifying identity, but exhibited multiple customer service faults including a condescending remark regarding bill inserts, deflecting routing responsibility to Telstra, re-asking the destination number, and failing to acknowledge customer distress during an anxious delay.",
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Build rapport and observed professionalism", "Took ownership of the problem"],
        "items": grader_items,
        "markers": markers
    }
}

with open(f"inputs/AG-T/expected/expected_{cid}.json", "w", encoding="utf-8") as f:
    json.dump(expected, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Generated {cid} successfully! Final score: {sc}")
