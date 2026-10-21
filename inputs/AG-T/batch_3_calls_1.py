import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from make_batch_3 import build_call

# =========================================================================
# agt_021: Damian, 5G outdoor antenna misaligned, 11:25 (685s)
# 1-2 faults (good), score 88.3, Empathy FAIL
# =========================================================================
cid_021 = "agt_021"
cname_021 = "Damian"
dur_021 = 685

raw_021 = [
    ("Agent", "Thank you for calling S-Net mobile broadband customer support, my name is Chloe. How can I help you today?", None),
    ("Customer", "Hi Chloe, my name is Damian Cross. We had severe gale force winds overnight in Cumbria, and since then our 5G outdoor home broadband antenna has shifted on its chimney mount and our internet speed dropped to almost zero.", -26.4),
    ("Agent", "Good morning Damian. I can certainly look into your 5G mast signal readings and antenna telemetry. Before we inspect your outdoor unit, could you please confirm your full postal address and your account security PIN?", None),
    ("Customer", "Yes, it is High Farm Cottage, Keswick, CA12 4PQ, and my security PIN is 5018. My account telephone number is 01768 790411.", 2.1),
    ("Agent", "Thank you Damian, that verifies your account details. How is the signal LED indicator behaving on your indoor power injector PoE box on the wall right now?", None),
    ("Customer", "The power LED is green, but the RF signal bar light is flashing solid red. Usually all four blue signal bars are illuminated when it connects to the mast.", -19.5),
    ("Agent", "So what I understand is that severe gale force winds physically knocked your outdoor 5G directional antenna out of alignment on your chimney stack, causing the signal indicator to flash red and severely throttling your bandwidth, is that right?", None),
    ("Customer", "Yes, that is exactly it. It is physically pointing about forty-five degrees away from the local cell mast now.", -8.3),
    ("Agent", "Which model outdoor antenna unit is mounted on your chimney bracket, Damian?", None),
    ("Customer", "It is the rectangular white Nokia FastMile 5G receiver unit that your contractor installed on the chimney stack last August.", 1.4),
    ("Agent", "Has the Ethernet cable running from the antenna down along the exterior masonry suffered any visible physical damage or tension from the storm?", None),
    ("Customer", "No, the black exterior Cat 6 shielded cable looks completely intact and firmly clipped along the stone wall.", 3.2),
    ("Agent", "Bear with me for a couple of minutes while I poll your outdoor CPE antenna diagnostic interface and signal registers from our cellular operations gateway.", None),
    ("Agent", "Thank you for waiting, Damian. The diagnostic telemetry confirms the antenna RSRP reading has fallen from minus seventy-five dBm down to minus one hundred and eighteen dBm, which indicates severe line-of-sight misalignment.", None),
    # Outburst 1
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
    ("Customer", "Tomorrow morning works. But what about my critical client meeting this afternoon? I cannot miss it.", -18.2),
    ("Agent", "I can provision a temporary high-speed 50GB mobile hotspot bundle directly to your S-Net smartphone SIM right now at no extra charge.", None),
    ("Customer", "That would allow me to tether my laptop for the video conference! Please do that right away.", 18.5),
    ("Agent", "I have applied the 50GB emergency data tethering pass to your mobile account right now. You should receive confirmation within two minutes.", None),
    ("Customer", "I just saw the SMS confirmation appear on my mobile! That solves my afternoon crisis.", 28.4),
    ("Agent", "And your outdoor antenna realignment appointment is officially confirmed for tomorrow between 9 AM and 1 PM under reference R-77291.", None),
    ("Customer", "R-77291 noted down carefully. Thank you.", 11.2),
    ("Agent", "Let us quickly check your mobile signal strength on your phone inside the farmhouse.", None),
    ("Customer", "I am showing four bars of 5G on my phone near the window in my study.", 8.5),
    ("Agent", "Please turn on your personal hotspot on your phone and test connecting your architectural workstation.", None),
    ("Customer", "Hotspot enabled... laptop connected... and Ookla speed test is pulling 120 megabits down and 25 up!", 32.1),
    ("Agent", "That speed will support multi-party HD video calling and large CAD blueprint uploads effortlessly throughout your meeting.", None),
    ("Customer", "That is an enormous weight off my shoulders. I can conduct my client meeting without fear of disconnecting.", 24.3),
    ("Agent", "The engineer will carry replacement heavy-duty mounting brackets in case the storm stripped the chimney masonry anchor threads.", None),
    ("Customer", "Good idea, the stone on these old Cumbrian farmhouses can crumble under heavy wind loads during severe winter storms.", 6.2),
    ("Agent", "They will also re-test the weatherproofing seals around the outdoor junction box and the grounding wire.", None),
    ("Customer", "That is reassuring, moisture penetration in the connector would cause even worse signal degradation later.", 8.4),
    ("Agent", "Will an adult over eighteen be present on site tomorrow morning to allow the engineer access to the indoor power injector?", None),
    ("Customer", "Yes, either myself or my partner will be here in the house all morning.", 4.1),
    ("Agent", "And just to confirm before we conclude, your indoor Wi-Fi router is broadcasting normally on 2.4 and 5 GHz bands?", None),
    ("Customer", "Yes, local Wi-Fi around the house connects without any issue to our smart home equipment.", 5.5),
    ("Agent", "Bear with me for one moment while I add the roof ladder hazard advisory note to the engineer dispatch ticket.", None),
    ("Agent", "Thank you for waiting, Damian. The health and safety risk assessment note has been appended to job ticket R-77291.", None),
    ("Customer", "Perfect. Will the engineer phone before arriving at the farmhouse?", -2.4),
    ("Agent", "Yes, the technician will call you approximately thirty minutes prior to arrival in Keswick.", None),
    # Outburst 2 in last third (turn 47 / 57 = 0.82)
    ("Customer", "Wait, looking out the attic window right now, the antenna is swaying dangerously on one bracket! What if it rips off and smashes through our slate roof?! That could cause thousands of pounds of structural damage!", -52.1),
    ("Agent", "The emergency engineer ticket notes that high-priority stabilization is required upon arrival tomorrow morning.", None),
    ("Customer", "Fine, as long as they secure it first thing tomorrow.", -15.4),
    ("Agent", "The emergency data is active, the engineer visit is booked, and your client meeting can proceed smoothly via hotspot.", None),
    ("Customer", "Thank you Chloe, that is everything I needed today.", 16.2),
    ("Agent", "Is there any other matter on your S-Net broadband or mobile account I can assist with today, Damian?", None),
    ("Customer", "No, you have handled the situation very well.", 14.1),
    ("Agent", "We also recommend leaving the outdoor PoE injector powered on so our operations center can monitor signal telemetry.", None),
    ("Customer", "Understood, I will leave the wall power switch turned on.", 6.2),
    ("Agent", "Thank you for choosing S-Net today, Damian. Goodbye.", None),
    ("Customer", "Goodbye Chloe.", 8.2),
    ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
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
    "Empathy & Acknowledgment Statement": "Ignored customer anxiety at [02:50] regarding an imminent business presentation and at [09:40] regarding roof damage when antenna shifted."
}

evidence_021 = {
    "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net mobile broadband customer support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
    "Hold time and Dead Air": "Holds were properly announced with bear with me and thanked upon return without unmanaged dead air.",
    "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
    "Personalized the call/ticket appropriately": "Agent addressed customer as Damian throughout the call.",
    "Empathy & Acknowledgment Statement": "Customer had two outbursts ([02:50] business presentation threat, [09:40] roof damage fear) and agent offered only procedural responses without acknowledging feelings.",
    "Paraphrasing": "Agent restated the antenna storm misalignment issue accurately at [01:25].",
    "Active listening": "Agent maintained accurate context and performed valid checks without improper repeats.",
    "Took ownership of the problem": "Agent arranged specialized rigging engineer and provided emergency 50GB tethering pass.",
    "Build rapport and observed professionalism": "Agent maintained professional and constructive tone throughout.",
    "Probing": "Agent asked effective diagnostic questions regarding PoE LED behavior, cable integrity, and antenna orientation.",
    "Confirmed the issue is resolved": "Customer tested mobile hotspot tethering, achieved 120 Mbps, and confirmed meeting was saved."
}

markers_021 = {
    "active_listening": [
        {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 19},
        {"kind": "harmless_recheck", "premise_turn": 5, "agent_turn": 43}
    ],
    "paraphrasing": [
        {"kind": "restatement", "agent_turn": 6},
        {"kind": "not_a_restatement", "agent_turn": 4}
    ],
    "rapport": [
        {"kind": "blunt_but_ok", "agent_turn": 21}
    ],
    "empathy": [
        {"kind": "unhandled", "customer_turn": 14},
        {"kind": "unhandled", "customer_turn": 49}
    ]
}

notes_021 = "Agent efficiently diagnosed physical 5G antenna misalignment and provided an emergency mobile hotspot pass, but failed to show empathy across two separate customer outbursts regarding business disruption and property damage."
hard_cases_021 = ["Active listening", "Empathy & Acknowledgment Statement", "Hold time and Dead Air"]

build_call(cid_021, cname_021, dur_021, "5G home broadband outdoor antenna misaligned after severe gale force winds", "good", raw_021, ratings_021, coaching_021, evidence_021, markers_021, hard_cases_021, notes_021)


# =========================================================================
# agt_022: Danica, Smart thermostat band-steering, 12:57 (777s)
# 3-4 faults (okay), score 65.0, Empathy FAIL, Active listening FAIL, Probing FAIL
# =========================================================================
cid_022 = "agt_022"
cname_022 = "Danica"
dur_022 = 777

raw_022 = [
    ("Agent", "Thank you for calling S-Net broadband technical support, my name is Liam. How can I help you today?", None),
    ("Customer", "Hello Liam, my name is Danica Bailey. I bought a Hive smart thermostat and four smart radiator valves, and none of them will connect to our new S-Net Hub 5 router.", -22.1),
    ("Agent", "Good morning Danica. I can certainly help look into Wi-Fi connectivity. Before we access your router gateway, could you please confirm your full postal address and your account security PIN?", None),
    ("Customer", "Yes, it is 15 St John's Road, Tunbridge Wells, TN4 9UU, and my security PIN is 8402. The thermostat is the Hive Active Heating v3 kit.", 1.5),
    ("Agent", "Thank you Danica, that confirms your account details. What happens on the Hive smartphone app when you try to pair the thermostat hub?", None),
    ("Customer", "The app spins for two minutes and says 'Unable to find 2.4 GHz network'. Both my phone and the thermostat are in the same room as the router.", -18.4),
    ("Agent", "So what you are experiencing is that your Hive smart thermostat and IoT devices are failing to complete pairing because the Hub 5 broadcasts a unified single SSID with band-steering enabled, is that right?", None),
    ("Customer", "Yes, exactly! Hive customer support told me smart heating hardware requires an isolated 2.4 GHz Wi-Fi channel.", -6.2),
    ("Agent", "Have you noticed whether other smart home devices like smart plugs or security cameras also struggle to connect?", None),
    ("Customer", "Yes, our smart security doorbell also drops offline intermittently whenever the router auto-optimizes channels.", -12.4),
    ("Agent", "And are your laptop and mobile phones connecting without issues to the internet?", None),
    ("Customer", "Yes, laptops, tablets, and mobile phones stream 4K video perfectly. It is strictly smart home hardware.", 4.2),
    ("Agent", "Bear with me for a couple of minutes while I connect to your Hub 5 management interface to review your radio frequency configuration.", None),
    ("Agent", "Thank you for waiting, Danica. I have accessed your router's wireless settings ledger. Currently Smart Wi-Fi band-steering is active, which merges 2.4 GHz and 5 GHz into a single network name.", None),
    ("Customer", "Our house is freezing cold! It is the middle of November, my elderly grandmother lives with us, and the radiators are completely shut off because this hub won't connect! We have been shivering under blankets for two days and I am furious that a brand new router broke our heating!", -56.3),
    ("Agent", "The router settings show band-steering is enabled by default across all residential firmware releases.", None),
    ("Customer", "Can you just split the frequencies or disable the 5 GHz band so my thermostat can connect and turn the boiler on?", -28.1),
    ("Agent", "Yes, we can split the network into two distinct SSIDs: SNet-Home-2.4 and SNet-Home-5G.", None),
    ("Customer", "Please do that right now, I need the radiators turned on immediately.", -14.2),
    ("Agent", "Obviously legacy smart home microcontrollers lack dual-band radios, so separating the network names resolves pairing handshakes.", None),
    ("Customer", "Okay, how long does the router take to reboot once you split the channels?", -8.5),
    ("Agent", "The Wi-Fi radio module restarts in approximately sixty seconds without interrupting the underlying broadband sync.", None),
    ("Customer", "That sounds very fast. Will the Wi-Fi password remain the same for both frequencies?", 2.4),
    ("Agent", "Yes, we will retain your existing WPA2 security passkey for both the 2.4 GHz and 5 GHz networks so existing phones reconnect automatically.", None),
    ("Customer", "That is convenient, so I don't have to re-type passwords across six family devices.", 8.5),
    ("Agent", "Before I split the bands on your gateway, that contact telephone number for SMS alerts was 01892 510934, correct?", None),
    ("Customer", "Yes, 01892 510934, that is my home landline.", 2.1),
    ("Agent", "I am applying the radio split command now. The Hub 5 will broadcast two separate network SSIDs.", None),
    ("Customer", "I see SNet-Home-2.4 appearing on my iPhone Wi-Fi list now.", 14.2),
    ("Agent", "Connect your iPhone to SNet-Home-2.4 and open the Hive app to initiate setup.", None),
    ("Customer", "I am connected to 2.4. Tapping 'Add New Device' in the Hive app now.", 8.4),
    ("Agent", "Bear with me for two minutes while the DHCP server binds the new MAC address lease for your heating controller.", None),
    ("Agent", "Thank you for waiting, Danica. The DHCP table is ready to accept the thermostat registration.", None),
    ("Customer", "The Hive app is asking for the exact model number of the heating kit to configure firmware sync.", -4.1),
    # Active listening repeat: Customer gave Hive Active Heating v3 in turn 3! Now at turn 34:
    ("Agent", "Which exact model of smart thermostat are you trying to pair again?", None),
    ("Customer", "I told you that at the very beginning of the call! It is the Hive Active Heating v3 kit!", -31.4),
    ("Agent", "I have logged the Hive v3 hardware identifier in your device profile.", None),
    ("Customer", "Tapping 'Pair Receiver' now... The amber pairing light on the Hive box just turned solid green! And the smartphone screen says 'Thermostat Connected Successfully'!", 34.2),
    ("Agent", "That confirms the Hive hub is receiving a stable IP lease on the 2.4 GHz channel.", None),
    ("Customer", "I just boosted the heating to 21 degrees and the boiler fired right up! The radiators are getting warm!", 41.5),
    ("Agent", "Are the smart radiator thermostatic valves also displaying connected status inside the app?", None),
    ("Customer", "Yes, all four radiator valves show online and synced with the hub.", 28.4),
    ("Agent", "And how is your smart security doorbell performing now on the 2.4 GHz network?", None),
    ("Customer", "The doorbell video feed loaded immediately without any buffering.", 22.1),
    ("Agent", "And just to verify before we wrap up, your laptops and tablets can still connect to the 5 GHz network for high-speed streaming?", None),
    ("Customer", "Yes, my iPad and laptop are both on SNet-Home-5G and working fast.", 18.2),
    ("Agent", "We have separated your Wi-Fi frequency bands, assigned the smart thermostat to 2.4 GHz, and confirmed the heating is operational.", None),
    ("Customer", "Thank you Liam, the house is warming up already.", 19.5),
    ("Agent", "You should also check that the Hive receiver firmware updates automatically overnight.", None),
    ("Customer", "Yes, Hive pushes updates over the 2.4 GHz connection automatically.", 12.1),
    ("Agent", "Remember that if you ever add new smart plugs or IoT bulbs in the future, select SNet-Home-2.4 during their initial pairing wizard.", None),
    ("Customer", "Understood, I have made a note in my smart home folder.", 6.1),
    ("Agent", "Is there any other smart device or broadband setting you would like me to configure today, Danica?", None),
    ("Customer", "No, getting the heating working was the critical issue.", 12.3),
    ("Agent", "Thank you for choosing S-Net broadband support, Danica. Have a warm and pleasant afternoon. Goodbye.", None),
    ("Customer", "Goodbye Liam.", 7.4),
    ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
]

ratings_022 = {
    "Branding and Survey Check": "PASS",
    "Hold time and Dead Air": "PASS",
    "Verified customer": "PASS",
    "Personalized the call/ticket appropriately": "PASS",
    "Empathy & Acknowledgment Statement": "FAIL",
    "Paraphrasing": "PASS",
    "Active listening": "FAIL",
    "Took ownership of the problem": "PASS",
    "Build rapport and observed professionalism": "PASS",
    "Probing": "FAIL",
    "Confirmed the issue is resolved": "PASS"
}

coaching_022 = {
    "Empathy & Acknowledgment Statement": "Failed to acknowledge customer distress at [03:15] when she explained her freezing house and elderly grandmother shivering under blankets.",
    "Active listening": "Asked for the smart thermostat model again at [08:10] after customer explicitly stated 'Hive Active Heating v3 kit' at [00:45].",
    "Probing": "Failed to ask diagnostic questions about 2.4 GHz interference or legacy security modes before splitting bands."
}

evidence_022 = {
    "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net broadband technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
    "Hold time and Dead Air": "Holds announced with bear with me and thanked upon return without unmanaged dead air.",
    "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
    "Personalized the call/ticket appropriately": "Agent addressed customer as Danica throughout the call.",
    "Empathy & Acknowledgment Statement": "[03:15] Customer: 'Our house is freezing cold! It is the middle of November, my elderly grandmother lives with us, and the radiators are completely shut off... we have been shivering under blankets for two days...' ... [03:35] Agent: 'The router settings show band-steering is enabled by default across all residential firmware releases.'",
    "Paraphrasing": "Agent accurately restated the band-steering pairing incompatibility at [01:30].",
    "Active listening": "[00:45] Customer: 'The thermostat is the Hive Active Heating v3 kit.' ... [08:10] Agent: 'Which exact model of smart thermostat are you trying to pair again?'",
    "Took ownership of the problem": "Agent split the Wi-Fi frequencies and assisted with device connection.",
    "Build rapport and observed professionalism": "Agent remained professional and polite throughout.",
    "Probing": "Agent did not probe into signal attenuation or wireless channel congestion.",
    "Confirmed the issue is resolved": "Customer confirmed thermostat paired, boiler fired up, and radiators warmed up."
}

markers_022 = {
    "active_listening": [
        {"kind": "repeat", "premise_turn": 3, "agent_turn": 34, "reworded": True},
        {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 25}
    ],
    "paraphrasing": [
        {"kind": "restatement", "agent_turn": 6},
        {"kind": "not_a_restatement", "agent_turn": 4}
    ],
    "rapport": [
        {"kind": "blunt_but_ok", "agent_turn": 19}
    ],
    "empathy": [
        {"kind": "unhandled", "customer_turn": 14}
    ]
}

notes_022 = "Agent successfully resolved smart home IoT pairing by splitting 2.4GHz and 5GHz Wi-Fi frequencies, but ignored customer distress over a freezing household and asked for the thermostat model again after it was already given."
hard_cases_022 = ["Active listening", "Empathy & Acknowledgment Statement"]

build_call(cid_022, cname_022, dur_022, "Smart thermostat and 2.4GHz IoT devices failing to connect due to band-steering", "okay", raw_022_expanded, ratings_022, coaching_022, evidence_022, markers_022, hard_cases_022, notes_022)

print("agt_021 and agt_022 written!")
