import sys
import os
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from gen_batch_3 import build_call

# ==========================================
# agt_021: Damian, 5G outdoor antenna misaligned, 11:25 (685s)
# 1-2 faults (good), score 88.3, Empathy FAIL
# ==========================================
cid_021 = "agt_021"
cname_021 = "Damian"
dur_021 = 685
raw_021 = [
    ("Agent", "Thank you for calling S-Net mobile broadband support, my name is Chloe. How can I help you today?", None),
    ("Customer", "Hi Chloe, my name is Damian Cross. We had severe gale force winds overnight in Cumbria, and since then our 5G outdoor home broadband antenna has shifted and our internet speed dropped to almost zero.", -26.4),
    ("Agent", "Good morning Damian. I can look into your 5G mast signal readings. Before we inspect your outdoor unit telemetry, could you confirm your full postal address and your account security PIN?", None),
    ("Customer", "Yes, it is High Farm Cottage, Keswick, CA12 4PQ, and my security PIN is 5018. My account telephone number is 01768 790411.", 2.1),
    ("Agent", "Thank you Damian, that verifies your account. How is the signal LED indicator behaving on your indoor power injector PoE box right now?", None),
    ("Customer", "The power LED is green, but the RF signal bar light is flashing solid red. Usually all four blue signal bars are illuminated.", -19.5),
    ("Agent", "So what I understand is that severe gale force winds physically knocked your outdoor 5G directional antenna out of alignment on your chimney stack, causing the signal indicator to flash red and severely throttling your bandwidth, is that right?", None),
    ("Customer", "Yes, that is exactly it. It is physically pointing about forty-five degrees away from the local cell mast now.", -8.3),
    ("Agent", "Bear with me for a couple of minutes while I poll your outdoor CPE antenna diagnostic interface from our cellular operations gateway.", None),
    ("Agent", "Thank you for waiting, Damian. The diagnostic telemetry confirms the antenna RSRP reading has fallen from minus seventy-five dBm down to minus one hundred and eighteen dBm, which indicates severe line-of-sight misalignment.", None),
    ("Customer", "I am supposed to be hosting a video conference with international clients in three hours! I run an architectural consultancy from this farmhouse, and without broadband my entire presentation is ruined! This is absolute chaos for my business!", -54.2),
    ("Agent", "The outdoor antenna uses a calibrated bracket clamped to your chimney stack. Have you inspected whether the bracket bolts are loose?", None),
    ("Customer", "I am not climbing up onto a three-storey pitched roof in sixty-mile-an-hour gusts to tighten bolts! That would be suicidal!", -46.8),
    ("Agent", "The S-Net safety policy strictly forbids customers from climbing onto roofs. We dispatch certified height-safety rigging engineers for outdoor antenna adjustments.", None),
    ("Customer", "Okay, when can an engineer come out here to Keswick to re-align the antenna?", -12.4),
    ("Agent", "Before I check the emergency dispatch calendar, that contact telephone number ending in 411 was 01768 790411, correct?", None),
    ("Customer", "Yes, 01768 790411, that is our landline.", 1.2),
    ("Agent", "Obviously high-gain directional 5G antennas require precise line-of-sight targeting to the sector panel, so manual realignment with an optical signal meter is essential.", None),
    ("Customer", "Understood. Is there an engineer available today or tomorrow?", -14.6),
    ("Agent", "The earliest specialized rigging engineer appointment for rural Cumbria is tomorrow between 9 AM and 1 PM.", None),
    ("Customer", "Tomorrow morning works. But what about my critical client meeting this afternoon?", -18.2),
    ("Agent", "I can provision a temporary high-speed 50GB mobile hotspot bundle directly to your S-Net smartphone SIM right now at no extra charge.", None),
    ("Customer", "That would allow me to tether my laptop for the video conference! Please do that.", 18.5),
    ("Agent", "I have applied the 50GB emergency data tethering pass to your mobile account right now. You should receive confirmation within two minutes.", None),
    ("Customer", "I just saw the SMS confirmation appear on my mobile! That solves my afternoon crisis.", 28.4),
    ("Agent", "And your outdoor antenna realignment appointment is officially confirmed for tomorrow between 9 AM and 1 PM under reference R-77291.", None),
    ("Customer", "R-77291 noted down carefully. Thank you.", 11.2),
    ("Agent", "And just to confirm before we conclude, your indoor Wi-Fi router is broadcasting normally on 2.4 and 5 GHz bands?", None),
    ("Customer", "Yes, local Wi-Fi around the house connects without any issue.", 4.5),
    ("Agent", "The emergency data is active, the engineer visit is booked, and your client meeting can proceed smoothly via hotspot.", None),
    ("Customer", "Thank you Chloe, that is everything I needed today.", 16.2),
    ("Agent", "Thank you for choosing S-Net today, Damian. Goodbye.", None)
]

ratings_021 = {
    "Branding and Survey Check": "PASS",
    "Hold time and Dead Air": "PASS",
    "Verified customer": "PASS",
    "Personalized the call/ticket appropriately": "PASS",
    "Empathy & Acknowledgment Statement": "FAIL",
    "Paraphrasing": "PASS",
    "Active listening": "PASS",
    "Took ownership of the problem": "PASS",
    "Build rapport and observed professionalism": "PASS",
    "Probing": "PASS",
    "Confirmed the issue is resolved": "PASS"
}

coaching_021 = {
    "Empathy & Acknowledgment Statement": "Ignored customer anxiety at [03:45] regarding an imminent business presentation when broadband failed due to antenna misalignment."
}

evidence_021 = {
    "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net mobile broadband support' at [00:00] and closed with 'Thank you for choosing S-Net today' at [11:19].",
    "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
    "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
    "Personalized the call/ticket appropriately": "Agent addressed customer as Damian throughout the call.",
    "Empathy & Acknowledgment Statement": "[03:45] Customer: 'I am supposed to be hosting a video conference with international clients in three hours!... This is absolute chaos for my business!' ... [04:05] Agent: 'The outdoor antenna uses a calibrated bracket clamped to your chimney stack.'",
    "Paraphrasing": "Agent restated the antenna storm misalignment issue accurately at [02:15].",
    "Active listening": "Agent maintained accurate context and performed valid checks without improper repeats.",
    "Took ownership of the problem": "Agent arranged specialized rigging engineer and provided emergency 50GB tethering pass.",
    "Build rapport and observed professionalism": "Agent maintained professional and constructive tone throughout.",
    "Probing": "Agent asked effective diagnostic questions regarding PoE LED behavior and antenna orientation.",
    "Confirmed the issue is resolved": "Customer confirmed receipt of emergency hotspot data allowance and accepted appointment booking."
}

markers_021 = {
    "active_listening": [
        {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 15},
        {"kind": "harmless_recheck", "premise_turn": 5, "agent_turn": 27}
    ],
    "paraphrasing": [
        {"kind": "restatement", "agent_turn": 6},
        {"kind": "not_a_restatement", "agent_turn": 4}
    ],
    "rapport": [
        {"kind": "blunt_but_ok", "agent_turn": 17}
    ],
    "empathy": [
        {"kind": "unhandled", "customer_turn": 10}
    ]
}

notes_021 = "Agent efficiently diagnosed physical 5G antenna misalignment and provided an emergency mobile hotspot pass, but failed to show empathy when the customer expressed severe distress over an impending international client meeting."
hard_cases_021 = ["Active listening", "Empathy & Acknowledgment Statement", "Hold time and Dead Air"]

build_call(cid_021, cname_021, dur_021, "5G home broadband outdoor antenna misaligned after severe gale force winds", "good", raw_021, ratings_021, coaching_021, evidence_021, markers_021, hard_cases_021, notes_021)
