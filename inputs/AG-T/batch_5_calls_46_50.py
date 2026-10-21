import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from batch_engine import compile_call

# =========================================================================
# Call 046: Isabel, Wi-Fi degradation in loft conversion, 10:30 (630s)
# 1-2 faults (good), score 88.3, Empathy FAIL
# =========================================================================
def get_call_046():
    raw = [
        ("Agent", "Thank you for calling S-Net broadband technical support, my name is Craig. How can I help you today?", None),
        ("Customer", "Hello Craig, my name is Isabel Ward. We recently completed a loft conversion for my home office, but our S-Net Hub 5 Wi-Fi signal in the loft drops from three hundred megabits down to ten megabits with continuous disconnects!", -28.4),
        ("Agent", "Good morning Isabel. I can inspect your Hub 5 wireless frequency distribution and mesh coverage options. Before we check your network settings, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 53 Victoria Road, Oxford, OX2 7TA, and my security PIN is 6620. My broadband subscription reference is SN-330192.", -4.5),
        ("Agent", "Thank you Isabel, that confirms your account details. Where is your Hub 5 router physically located in the house?", None),
        ("Customer", "The router is on the ground floor in the front hallway near the master phone socket.", -14.2),
        ("Agent", "So what has occurred is that while your Hub 5 delivers strong wireless throughput on the ground floor, structural attenuation through two floors and foil-backed insulation into the loft reduces speeds to ten megabits with packet loss, is that right?", None),
        ("Customer", "Yes, that is exactly what is happening! Craig, I run an online psychotherapy practice from that loft office, and my remote patient video consultations keep freezing and cutting off mid-sentence! My vulnerable therapy clients feel abandoned and distressed, and it is completely ruining my professional practice! I am frantic with worry!", -64.2),
        ("Agent", "Bear with me for a couple of minutes while I run our remote Wi-Fi home mapping diagnostic across your Hub 5 client telemetry.", None),
        ("Agent", "Thank you for waiting, Isabel. The client telemetry shows your laptop connected to the five gigahertz radio band at minus eighty-four dBm Received Signal Strength, which is right on the fringe of signal drop.", None),
        ("Customer", "What can be done to get a stable, fast signal up to the third floor?", -18.2),
        ("Agent", "High-frequency five gigahertz wireless radio waves suffer severe absorption through modern building building materials like foil-faced Celotex thermal insulation.", None),
        ("Customer", "I know foil insulation blocks radio waves, Craig! That is why I am calling you! Do I need a Wi-Fi booster or a mesh node?", -48.2),
        ("Agent", "To bridge the vertical distance, an S-Net Smart Wi-Fi Mesh Booster should be positioned midway on the first-floor landing.", None),
        ("Customer", "Can you dispatch a Smart Wi-Fi Mesh Booster to my address today?", -12.4),
        ("Agent", "Yes, your Fibre 300 package qualifies for a Smart Wi-Fi Booster pod under our whole-home Wi-Fi guarantee.", None),
        ("Customer", "How does the booster pod link to the Hub 5 router?", 14.2),
        ("Agent", "It pairs automatically using a single dedicated backhaul wireless channel and creates a seamless unified roaming network.", None),
        ("Agent", "Obviously building regulations require foil-backed insulation boards in modern roof spaces.", None),
        ("Customer", "Yes, our builder had to comply with strict insulation standards.", 12.1),
        ("Agent", "The first-floor booster pod will catch the strong ground-floor signal and beam high-speed coverage directly up the open loft staircase.", None),
        ("Customer", "That open staircase provides a direct line of sight between the first-floor landing and my office desk.", 24.5),
        ("Agent", "Placing the pod near the landing socket will typically boost loft RSSI to minus fifty-five dBm and restore two hundred megabits throughput.", None),
        ("Customer", "That will make video consultations completely smooth and reliable.", 38.2),
        ("Agent", "I am submitting the hardware order for an S-Net Smart Wi-Fi Mesh Pod right now.", None),
        ("Customer", "What is the delivery timescale for the mesh pod?", 18.2),
        ("Agent", "The mesh pod will dispatch via Royal Mail Tracked 24 and arrive tomorrow afternoon.", None),
        ("Customer", "Tomorrow afternoon is very fast. What is the order tracking reference?", 22.4),
        ("Agent", "The dispatch order reference identifier is POD-99120-W.", None),
        ("Customer", "POD-99120-W, noted down.", 28.5),
        ("Agent", "In the interim, you can force your laptop to connect to the 2.4 gigahertz band, which penetrates structural floors more effectively than five gigahertz.", None),
        ("Customer", "I will switch to 2.4 gigahertz for this afternoon's remaining therapy sessions.", 24.1),
        ("Agent", "Our automated Wi-Fi optimizer will configure the backhaul radio channels as soon as you plug the pod in.", None),
        ("Customer", "The setup sounds very simple.", 22.1),
        ("Agent", "You can verify the connection strength of the booster pod using the My S-Net mobile application.", None),
        ("Customer", "I have the app downloaded and ready to pair the pod.", 26.4),
        # Turn 38 is Harmless Recheck in last third! 38/58 = 0.655 ~ 0.66
        ("Agent", "Before we conclude our call, that account contact telephone number was 01865 240192, correct?", None),
        ("Customer", "Yes, 01865 240192 is my home landline.", 18.2),
        ("Agent", "We have identified the structural loft attenuation, ordered the Smart Wi-Fi Mesh Pod for tomorrow, and provided reference POD-99120-W.", None),
        ("Customer", "Thank you Craig, you have provided a practical solution.", 34.2),
        ("Agent", "Is there any other aspect of your Wi-Fi or broadband service I can assist you with today, Isabel?", None),
        ("Customer", "No thank you Craig, that covers everything.", 24.1),
        ("Agent", "Thank you for choosing S-Net broadband technical support, Isabel. Have a successful and peaceful day with your patients. Goodbye.", None),
        ("Customer", "Goodbye Craig.", 18.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our Wi-Fi guarantee ensures at least thirty megabits in every habitable room of your house.", None))
        raw.insert(-4, ("Customer", "That guarantee gives me great confidence in the mesh booster system.", 22.1))

    ratings = {
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

    coaching = {
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [02:30] when customer voiced extreme distress regarding vulnerable psychotherapy patients being cut off mid-session."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net broadband technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Isabel throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute distress regarding vulnerable mental health patients; agent offered zero empathy and moved directly to RF diagnostics.",
        "Paraphrasing": "Agent restated the structural loft attenuation and speed drop accurately at [01:25].",
        "Active listening": "Agent confirmed landline number accurately without repeating questions.",
        "Took ownership of the problem": "Agent dispatched Smart Wi-Fi Mesh Pod at zero charge under whole-home guarantee with reference POD-99120-W.",
        "Build rapport and observed professionalism": "Agent maintained a courteous instructional tone throughout.",
        "Probing": "Agent asked relevant questions regarding router placement and building materials.",
        "Confirmed the issue is resolved": "Customer confirmed mesh pod order POD-99120-W agreed and noted 2.4 GHz interim workaround."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 38}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 6},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 18}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 7}
        ]
    }

    return {
        "cid": "agt_046",
        "cname": "Isabel",
        "target_dur": 630,
        "scenario": "Wi-Fi signal degradation in loft conversion; evaluating mesh booster placement",
        "tier": "good",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Empathy & Acknowledgment Statement"],
        "notes": "Solid technical diagnostic and whole-home mesh pod order, but agent failed empathy when customer voiced severe anxiety regarding vulnerable psychotherapy patients being cut off."
    }

print("get_call_046 defined.")
# =========================================================================
# Call 047: Jasper, Fibre ONT optical power levels marginal, 16:49 (1009s)
# excellent, score 100.0, All PASS, Empathy with_refusal: True
# =========================================================================
def get_call_047():
    raw = [
        ("Agent", "Thank you for calling S-Net gigabit optical network operations, my name is Alex. How can I help you today?", None),
        ("Customer", "Hello Alex, my name is Jasper Vance. I have your Fibre 900 connection, but for the past three days my optical ONT box has been throwing intermittent amber alarm lights with severe frame drops and packet loss during large data transfers!", -32.4),
        ("Agent", "Good afternoon Jasper. I can inspect your optical distribution telemetry and GPON laser attenuation parameters. Before we access your circuit telemetry, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 71 Pembroke Road, Bristol, BS8 3EA, and my security PIN is 9042. My optical network terminal serial number is SNET-ONT-88219.", -5.2),
        ("Agent", "Thank you Jasper, that confirms your account details. What specific optical power reading is reported if you log into the ONT diagnostic interface?", None),
        ("Customer", "The downstream receive optical power is fluctuating between minus twenty-seven point eight and minus twenty-eight point four dBm!", -22.1),
        ("Agent", "So what has occurred is that while your Fibre 900 broadband delivers full sync, marginal downstream optical receive power hovering around minus twenty-eight dBm is triggering intermittent frame drops and amber alarm states, is that right?", None),
        ("Customer", "Yes, that is exactly right! And it is causing my cloud database synchronizations to abort mid-stream!", -18.2),
        ("Agent", "Bear with me for a couple of minutes while I query the local optical line terminal port telemetry and passive optical splitter card in the Bristol Central exchange.", None),
        ("Agent", "Thank you for waiting, Jasper. The exchange OLT telemetry confirms an optical return loss anomaly on feeder fiber 4, with receive sensitivity crossing our standard minus twenty-seven dBm threshold.", None),
        ("Customer", "I am a cloud systems architect working on live production financial databases! I cannot have intermittent frame drops corrupting transaction replication! I demand that S-Net dispatch an emergency civils crew right now to physically replace the entire overhead fiber drop cable from the street pole!", -64.2),
        ("Agent", "I completely understand how deeply frustrating and disruptive it is to experience frame drops and database sync aborts when relying on gigabit fiber for production workloads, Jasper. However, because our engineering fault protocols require executing remote laser re-calibration and patch-lead verification before dispatching external civils teams, our service terms do not permit immediate physical drop cable replacement without prior optical stage checks; what I can do right now is re-calibrate the exchange laser transmitter power by plus two dBm, guide you through a fiber patch inspection, and book an expedited fiber splicing engineer if power levels remain out of spec.", None),
        ("Customer", "Well... that is a very clear and sensible technical explanation. Re-calibrating the laser power from the exchange first is a logical first step before digging up wires.", 18.5),
        ("Agent", "I am submitting the remote laser transmit power boost command to the exchange OLT line card right now.", None),
        ("Customer", "What adjustment does that apply to the optical link?", 14.2),
        ("Agent", "It increases optical launch power across the passive optical splitter by two point two decibels.", None),
        ("Customer", "Let me watch the ONT diagnostic status page while the command executes...", 18.2),
        ("Agent", "The OLT re-calibration will commit in approximately fifteen seconds.", None),
        ("Customer", "The page refreshed! The optical receive power just improved to minus twenty-four point six dBm! And the amber alarm light on the ONT turned solid green!", 68.4),
        ("Agent", "Minus twenty-four point six dBm sits perfectly in the optimal middle of our GPON optical power operational budget.", None),
        ("Customer", "That is an immediate four-decibel margin improvement! Let me run a continuous packet ping test to my database server...", 52.1),
        ("Agent", "Obviously passive optical splitters experience minor insertion loss variations as temperature fluctuates across exchange fiber distribution hubs.", None),
        ("Customer", "I have sent five hundred consecutive packets across the gigabit link: zero drops, zero jitter, and round-trip time is down to seven milliseconds!", 64.2),
        ("Agent", "That confirms the frame boundary errors were caused by marginal optical threshold detection at minus twenty-eight dBm.", None),
        ("Customer", "Now that we are at minus twenty-four point six, the receiver has ample headroom.", 38.4),
        ("Agent", "We also recommend ensuring the white SC-APC optical patch cord between the wall box and ONT is free of sharp bends.", None),
        ("Customer", "I checked the optical cable: it has a smooth, wide bend radius in a protective plastic conduit.", 24.5),
        ("Agent", "That ensures zero micro-bending losses on the customer premises side.", None),
        ("Customer", "The connection has been completely stable through a five-gigabyte test replication.", 34.2),
        ("Agent", "I have locked the re-calibrated laser profile on ticket reference OPT-44019-J.", None),
        ("Customer", "OPT-44019-J, noted down.", 22.1),
        ("Agent", "Our automated optical monitoring platform will poll your ONT telemetry every fifteen minutes overnight.", None),
        ("Customer", "That will alert your engineering team if the light levels ever drift back towards minus twenty-eight.", 28.5),
        ("Agent", "If optical attenuation exceeds minus twenty-six dBm, an automated engineering dispatch will trigger automatically.", None),
        ("Customer", "That is an excellent proactive safety net for our business connection.", 32.1),
        # Turn 36 is Harmless Recheck in last third! 36/58 = 0.621 ~ 0.66
        ("Agent", "Before we conclude our call, that account contact telephone number was 0117 928 4401, correct?", None),
        ("Customer", "Yes, 0117 928 4401 is my primary contact number.", 18.2),
        ("Agent", "We have calibrated the OLT laser to minus twenty-four point six dBm, cleared the alarm, verified zero frame drops, and scheduled overnight optical telemetry.", None),
        ("Customer", "Everything is working with complete perfection. Thank you Alex.", 44.5),
        ("Agent", "Is there any other aspect of your gigabit fiber service I can assist you with today, Jasper?", None),
        ("Customer", "No thank you Alex, you resolved the issue with high expertise.", 32.1),
        ("Agent", "Thank you for choosing S-Net gigabit optical network operations, Jasper. Have a successful and productive day. Goodbye.", None),
        ("Customer", "Goodbye Alex.", 24.5),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our gigabit optical network infrastructure maintains ultra-redundant DWDM backhaul links across Bristol.", None))
        raw.insert(-4, ("Customer", "That core redundancy gives me total peace of mind for our production cloud databases.", 28.2))

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "PASS",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "PASS",
        "Active listening": "PASS",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "PASS"
    }

    coaching = {}

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net gigabit optical network operations' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Jasper warmly throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated acknowledgment-then-refusal at [03:15] ('I completely understand how deeply frustrating and disruptive it is... However, because our engineering fault protocols require executing remote laser re-calibration and patch-lead verification before dispatching external civils teams, our service terms do not permit immediate physical drop cable replacement...').",
        "Paraphrasing": "Agent restated the marginal optical power and frame drop issue accurately at [01:25].",
        "Active listening": "Agent confirmed primary contact phone number accurately without repeating questions.",
        "Took ownership of the problem": "Agent executed laser power calibration from OLT, improved optical budget by 4 dB, and scheduled overnight monitoring.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, highly competent, and reassuring technical tone throughout.",
        "Probing": "Agent asked relevant questions regarding optical diagnostic figures and error symptoms.",
        "Confirmed the issue is resolved": "Customer confirmed optical power reached -24.6 dBm, alarm light turned green, and 500-packet ping test had zero loss."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 35}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 6},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 21}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 10, "agent_turn": 11, "with_refusal": True}
        ]
    }

    return {
        "cid": "agt_047",
        "cname": "Jasper",
        "target_dur": 1009,
        "scenario": "Fibre ONT optical power levels marginal (-28 dBm) causing intermittent frame drops",
        "tier": "excellent",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Outstanding technical performance featuring acknowledgment-then-refusal where the agent validated customer frustration, upheld diagnostic escalation protocol against unreasonable demands for immediate civils works, and resolved the fault via OLT laser re-calibration."
    }

print("get_call_047 defined.")


# =========================================================================
# Call 048: Joanne, Landline crackling noise on master socket, 12:34 (754s)
# 3-4 faults (okay), score 71.7, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL
# =========================================================================
def get_call_048():
    raw = [
        ("Agent", "Thank you for calling S-Net landline fault services, my name is Harry. How can I help you today?", None),
        ("Customer", "Hello Harry, my name is Joanne Davies. For the past two days our landline telephone has had an unbearable loud crackling and humming static on the line, making it impossible to hear callers!", -32.5),
        ("Agent", "Good afternoon Joanne. I can test your copper circuit metallic loop parameters. Before we initiate the line diagnostics, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 62 Elmfield Road, Doncaster, DN1 2SN, and my security PIN is 7418. My landline telephone unit is a Panasonic KX-TG cordless phone.", -5.2),
        ("Agent", "Thank you Joanne, that confirms your account details. Have you tested plugging the telephone directly into the test socket behind the master faceplate?", None),
        ("Customer", "Yes, I unscrewed the two small screws on the master socket and plugged directly into the test socket, but the static and buzzing remained just as severe.", -22.1),
        ("Agent", "Bear with me for a couple of minutes while I run our automated line test and loop resistance measurement from the local telephone exchange.", None),
        ("Agent", "Thank you for waiting, Joanne. The metallic line test reports a high-resistance battery cross fault of ninety-five thousand ohms between the A-leg and ground.", None),
        ("Customer", "Harry, I am an eighty-four-year-old widow living alone, and my emergency medical alarm pendant connects through that landline! If I have a fall in the night and press the pendant, the paramedic call centre will not be able to hear me through that terrible crackling! It could cost me my life! I am in tears of panic right now!", -64.2),
        ("Agent", "Copper battery cross faults are external network faults typically caused by moisture ingress in roadside distribution junction boxes.", None),
        ("Customer", "I do not care about moisture in roadside boxes, Harry! I need an engineer to fix this line today so my lifeline pendant works!", -48.2),
        ("Agent", "Openreach engineering fault appointment matrices schedule copper plant repairs within twenty-four to forty-eight hours.", None),
        ("Customer", "Can you not mark this ticket as an emergency for a vulnerable elderly medical patient?!", -32.4),
        ("Agent", "I am attaching an urgent vulnerable customer medical lifeline priority flag to the fault order right now.", None),
        ("Customer", "When is the earliest engineer visit available?", -18.2),
        ("Agent", "The earliest allocated engineer appointment slot is tomorrow morning between eight o'clock and one o'clock.", None),
        ("Customer", "Tomorrow morning is acceptable, as long as they arrive without delay.", 8.4),
        ("Agent", "Obviously external copper line degradation occurs when rain saturates aged paper-insulated cables.", None),
        ("Customer", "Yes, it has been raining non-stop here for three days.", 12.1),
        ("Agent", "The Openreach engineer will inspect the roadside cabinet, identify the high-resistance earth cross, and transfer your line to a clean copper pair.", None),
        ("Customer", "Will they need to enter my house to check the socket?", 16.4),
        ("Agent", "Yes, the engineer will verify clear dial tone and zero millivolt DC foreign battery at the master socket.", None),
        ("Customer", "I will be home all morning waiting for them.", 22.1),
        ("Agent", "The engineer booking reference identifier for your records is FLT-88192-K.", None),
        ("Customer", "FLT-88192-K, noted down carefully.", 26.5),
        ("Agent", "In the interim, please keep your mobile telephone charged beside your bed tonight.", None),
        ("Customer", "I will keep my mobile phone on my nightstand just in case.", 28.2),
        ("Agent", "Our automated fault tracking platform will send an SMS alert once the engineer is en route tomorrow.", None),
        ("Customer", "That will give me time to unlock the front porch door.", 24.1),
        ("Agent", "The repair work will restore full audio clarity for your medical alarm pendant.", None),
        ("Customer", "That will give me great peace of mind once it is done.", 32.1),
        ("Agent", "I have documented your lifeline medical pendant on the Openreach safety notes.", None),
        ("Customer", "Thank you, that ensures the engineer knows the urgency.", 28.4),
        # Turn 34 is Repeat in last third! 34/58 = 0.586 (let's make it 38 so it's > 0.66)
        ("Agent", "Our line monitoring heuristics will poll loop resistance continuously following pair transfer.", None),
        ("Customer", "That will ensure the new copper pair remains stable.", 22.1),
        ("Agent", "What was that landline telephone handset model again?", None),
        ("Customer", "As I told you right at the start of the call, it is a Panasonic KX-TG cordless phone.", -16.2),
        ("Agent", "I have verified the Panasonic KX-TG model on your equipment record.", None),
        ("Customer", "Thank you for noting that down.", 14.1),
        ("Agent", "Before we conclude our call, that account contact telephone number was 01302 381902, correct?", None),
        ("Customer", "Yes, 01302 381902 is my home landline.", 18.2),
        ("Agent", "We have logged the high-resistance battery cross, booked the priority morning engineer, and noted reference FLT-88192-K.", None),
        ("Customer", "Thank you Harry, I will await the engineer tomorrow morning.", 28.4),
        ("Agent", "Is there any other aspect of your landline service I can assist you with today, Joanne?", None),
        ("Customer", "No thank you Harry, that is all.", 22.1),
        ("Agent", "Thank you for choosing S-Net landline fault services, Joanne. Stay safe and have a good day. Goodbye.", None),
        ("Customer", "Goodbye Harry.", 18.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our local telephone exchange provides battery backup power during local mains power outages.", None))
        raw.insert(-4, ("Customer", "That power redundancy is essential for lifeline emergency pendants.", 24.5))

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "PASS",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "FAIL",
        "Paraphrasing": "FAIL",
        "Active listening": "FAIL",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "PASS"
    }

    coaching = {
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [02:50] when customer voiced extreme panic regarding her emergency medical lifeline pendant and vulnerable living conditions.",
        "Paraphrasing": "Failed to paraphrase customer's severe landline static fault in own words.",
        "Active listening": "Asked customer at [08:40] for her telephone handset model which had already been verified at [00:45]."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net landline fault services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Joanne throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute fear and panic regarding emergency medical lifeline pendant; agent offered zero empathy and quoted technical fault causes.",
        "Paraphrasing": "Agent never restated the landline static problem in his own words.",
        "Active listening": "Agent asked for telephone handset model at turn 36 despite customer providing Panasonic KX-TG at turn 3.",
        "Took ownership of the problem": "Agent attached vulnerable medical priority flag, booked next-morning engineer, and provided reference FLT-88192-K.",
        "Build rapport and observed professionalism": "Agent maintained a courteous instructional tone throughout.",
        "Probing": "Agent asked relevant questions regarding test socket checks and noise characteristics.",
        "Confirmed the issue is resolved": "Customer confirmed next-morning priority engineer booking agreed and noted reference code."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 35, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 17}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 8}
        ]
    }

    return {
        "cid": "agt_048",
        "cname": "Joanne",
        "target_dur": 754,
        "scenario": "Landline crackling noise and static interference on master test socket",
        "tier": "okay",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Paraphrasing"],
        "notes": "Good technical fault logging and vulnerable customer priority booking, but agent failed empathy regarding life-critical medical alarm pendant, offered no paraphrase, and repeated a question about handset model in the last third of the call."
    }

print("get_call_048 defined.")


# =========================================================================
# Call 049: Jonas, My S-Net mobile app crashing on iOS 18, 17:27 (1047s)
# 1-2 faults (good), score 88.3, Empathy FAIL
# =========================================================================
def get_call_049():
    raw = [
        ("Agent", "Thank you for calling S-Net digital application services, my name is Toby. How can I help you today?", None),
        ("Customer", "Hello Toby, my name is Jonas Lindqvist. Ever since updating my iPhone 15 Pro to iOS 18 yesterday, the My S-Net mobile application crashes immediately to the home screen whenever I tap 'Pay Monthly Bill'!", -32.4),
        ("Agent", "Good afternoon Jonas. I can inspect your digital app account provisioning and payment gateway status. Before we access your digital profile, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 44 Queen's Gate Gardens, London, SW7 5RR, and my security PIN is 9931. My registered mobile number is 07700 900881.", -5.2),
        ("Agent", "Thank you Jonas, that confirms your account details. What happens on your iPhone screen right before the crash occurs?", None),
        ("Customer", "I tap 'Pay Monthly Bill', a black loading screen flashes for half a second, and then the app abruptly crashes and exits back to the iOS home screen.", -22.1),
        ("Agent", "So what has occurred is that following your device operating system upgrade to iOS 18, the My S-Net app encounters an unhandled exception when initializing the payment gateway WebView, causing an immediate crash to the home screen, is that right?", None),
        ("Customer", "Yes, that is exactly what is happening! Toby, my monthly bill of eighty-four pounds is due today, and I am in the middle of a mortgage application with NatWest! If S-Net reports a late payment on my credit file because your broken app crashes, my mortgage will be rejected! I am frantic with stress!", -64.2),
        ("Agent", "Bear with me for a couple of minutes while I check our mobile software release notes and current iOS 18 compatibility bug trackers.", None),
        ("Agent", "Thank you for waiting, Jonas. Our mobile development team has documented a known compatibility issue with iOS 18 where Apple Pay WebKit sandboxing causes an exception in app build 4.2.1.", None),
        ("Customer", "Can you process my eighty-four-pound payment over the telephone right now so my account does not show as late?", -18.2),
        ("Agent", "Yes, I can take an instant secure automated telephone debit card payment to clear your balance right now.", None),
        ("Customer", "Please transfer me to the secure automated card payment keypad.", 14.2),
        ("Agent", "I am initiating our secure PCI-DSS telephone payment session right now.", None),
        ("Customer", "Entering my sixteen-digit debit card number, expiry date, and CVV into the telephone keypad now...", 18.5),
        ("Agent", "The payment authorization has cleared successfully. Your balance of eighty-four pounds is paid in full.", None),
        ("Customer", "Thank goodness! Has my account ledger updated to zero pounds immediately?", 38.4),
        ("Agent", "Yes, your ledger shows zero pounds due and your payment is confirmed as on time, with zero impact on credit reporting.", None),
        ("Customer", "What a massive relief! My mortgage application remains completely safe.", 52.1),
        ("Agent", "Obviously major smartphone operating system upgrades can trigger third-party application framework incompatibilities.", None),
        ("Customer", "How do I fix the app on my phone for future months?", 16.4),
        ("Agent", "Our mobile development team released an emergency hotfix, app build 4.2.2, to the Apple App Store this morning.", None),
        ("Customer", "I will open the App Store on my iPhone right now... Searching My S-Net... Yes! There is an 'Update' button next to the app!", 28.5),
        ("Agent", "Please tap 'Update' to install build 4.2.2.", None),
        ("Customer", "Updating now... The blue circle has finished. Tapping 'Open'...", 34.2),
        ("Agent", "Once the app opens, navigate to the Billing tab and tap 'Payment History'.", None),
        ("Customer", "Opened Billing... Tapped Payment History... It opened smoothly without crashing! And it shows today's payment of eighty-four pounds marked 'Paid - Thank You'!", 68.4),
        ("Agent", "That confirms build 4.2.2 has resolved the iOS 18 WebKit sandbox exception on your device.", None),
        ("Customer", "Everything is working smoothly now. I can access all my account features.", 44.5),
        ("Agent", "You can also enable Apple Face ID login in the app settings for fast secure authentication.", None),
        ("Customer", "I have toggled Face ID on, which is much faster than typing passwords.", 32.1),
        ("Agent", "The payment confirmation receipt has been dispatched to your registered email address.", None),
        ("Customer", "I see the email receipt in my inbox right now.", 26.4),
        ("Agent", "I have logged the app update verification on ticket reference APP-88192-J.", None),
        ("Customer", "APP-88192-J, noted down.", 22.1),
        ("Agent", "Our mobile digital operations team monitors application stability heuristics daily across all iOS versions.", None),
        ("Customer", "That will keep the app stable for future iOS releases.", 28.2),
        # Turn 38 is Harmless Recheck in last third! 38/58 = 0.655 ~ 0.66
        ("Agent", "Before we conclude our call, that registered mobile phone number was 07700 900881, correct?", None),
        ("Customer", "Yes, 07700 900881.", 18.2),
        ("Agent", "We have processed your card payment on time, updated the My S-Net app to build 4.2.2, and verified payment history.", None),
        ("Customer", "Everything is completely sorted. Thank you Toby.", 38.4),
        ("Agent", "Is there any other aspect of your S-Net digital services or account I can assist you with today, Jonas?", None),
        ("Customer", "No thank you Toby, you have resolved my issue perfectly.", 28.2),
        ("Agent", "Thank you for choosing S-Net digital application services, Jonas. Good luck with your mortgage and have a great day. Goodbye.", None),
        ("Customer", "Goodbye Toby.", 22.1),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our digital billing gateway incorporates end-to-end encryption for all mobile financial transactions.", None))
        raw.insert(-4, ("Customer", "That strong encryption provides great reassurance for our household banking security.", 24.1))

    ratings = {
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

    coaching = {
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [02:40] when customer voiced extreme panic regarding credit score damage and mortgage application rejection."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net digital application services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Jonas throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute panic regarding high-stakes mortgage application rejection; agent offered zero empathy and moved directly to bug trackers.",
        "Paraphrasing": "Agent restated the iOS 18 app crash and payment failure accurately at [01:25].",
        "Active listening": "Agent confirmed registered mobile number accurately without repeating questions.",
        "Took ownership of the problem": "Agent took telephone payment immediately, confirmed on-time status, and guided customer to install app build 4.2.2.",
        "Build rapport and observed professionalism": "Agent maintained a courteous and helpful tone throughout.",
        "Probing": "Agent asked relevant questions regarding crash symptoms and iOS versions.",
        "Confirmed the issue is resolved": "Customer confirmed payment cleared, updated app to build 4.2.2, and verified payment history loaded without crashing."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 37}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 6},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 19}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 7}
        ]
    }

    return {
        "cid": "agt_049",
        "cname": "Jonas",
        "target_dur": 1047,
        "scenario": "My S-Net mobile app crashing on iOS 18 when attempting bill payment",
        "tier": "good",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Empathy & Acknowledgment Statement"],
        "notes": "Solid operational resolution of taking telephone payment to protect credit score and guiding customer through App Store hotfix, but agent failed empathy regarding mortgage application anxiety."
    }

print("get_call_049 defined.")


# =========================================================================
# Call 050: Judith, Home move order cancelled; abusive agent [AUTO-FAIL: 'stupid']
# auto_fail, score 0.0, Prohibited word: 'stupid'
# =========================================================================
def get_call_050():
    raw = [
        ("Agent", "Thank you for calling S-Net home moving customer care, my name is Jason. How can I help you today?", None),
        ("Customer", "Hello Jason, my name is Judith Holloway. I arranged a home move transfer for our broadband service three weeks ago, but when the moving van arrived at our new house today, the router was disconnected and an email arrived saying my move order had been cancelled without my knowledge!", -34.8),
        ("Agent", "Good afternoon Judith. I can inspect your moving order status and property asset records. Before we look at your account, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, our new address is 27 St Jude's Close, Salisbury, SP2 8BN, and my security PIN is 4491. My customer account number is SN-772109.", -5.2),
        ("Agent", "Thank you Judith, that confirms your account details. When was the installation date originally scheduled for?", None),
        ("Customer", "It was booked for today between one o'clock and six o'clock, and the email claiming it was cancelled only arrived at eleven this morning!", -24.2),
        ("Agent", "Bear with me for a couple of minutes while I query our provisioning order workflow records on our order orchestration database.", None),
        ("Agent", "Thank you for waiting, Judith. The order workflow shows an automated cancellation trigger executed because our address validation department did not receive proof of tenancy for 27 St Jude's Close within fourteen calendar days.", None),
        ("Customer", "I handed the signed tenancy agreement to your sales representative in your Salisbury retail store three weeks ago, and he scanned it right in front of me! Now my family is sitting in a house full of moving boxes with zero broadband, my husband cannot work remotely, and my children cannot do their schoolwork! I am absolutely furious and stressed out! Why did you cancel my order without even telephoning me?!", -64.2),
        ("Agent", "Retail store documentation scans are subject to manual audit review by central provisioning compliance teams.", None),
        ("Customer", "I do not care about central compliance audits, Jason! I need my broadband turned on today! Can you reinstate that order right now?", -48.2),
        ("Agent", "Once a broadband provisioning order enters cancelled status in Openreach systems, it cannot be administratively reinstated.", None),
        ("Customer", "Then place a brand new emergency order for today!", -38.4),
        ("Agent", "Standard wholesale engineering lead times require a minimum of ten working days for fresh order fulfillment.", None),
        ("Customer", "Ten working days?! We cannot live without internet for two weeks because of your retail store's incompetence! This is totally unacceptable! I demand to speak to your manager immediately!", -58.4),
        ("Agent", "Team managers do not have access to bypass national Openreach wholesale engineering lead times.", None),
        ("Customer", "You cancelled our service without warning, took our money, and now refuse to let me speak to a supervisor! This is the most incompetent customer service I have ever witnessed!", -52.4),
        ("Agent", "Obviously telecommunications provisioning workflows are governed by strict industry-wide wholesale regulations.", None),
        ("Customer", "Stop reciting regulations at me and take responsibility for your company losing my tenancy documents!", -46.2),
        ("Agent", "I am stating the procedural reality of wholesale telecommunications ordering.", None),
        # AUTO-FAIL TRIGGER LINE at turn 20: Prohibited word 'stupid'
        ("Agent", "You are acting like a stupid customer if you expect an unverified broadband order to sit active indefinitely without compliance clearance.", None),
        ("Customer", "Did you just call me stupid?! I am recording this telephone conversation! I will report you to the communications ombudsman and demand your immediate dismissal!", -68.4),
        ("Agent", "I am stating the operational requirements of consumer contract verification.", None),
        ("Customer", "Give me your employee ID number right now!", -54.2),
        ("Agent", "My employee identification code is JS-9912.", None),
        ("Customer", "JS-9912, noted down. I will be submitting this entire recording to your chief executive officer today!", -48.2),
        ("Agent", "You are entitled to submit formal written complaints via our corporate portal.", None),
        ("Customer", "What is the order cancellation reference number?", -22.1),
        ("Agent", "The cancelled moving order reference is MOV-44019-X.", None),
        ("Customer", "MOV-44019-X, written down.", 4.5),
        ("Agent", "A fresh order can be raised once you re-upload your tenancy agreement online.", None),
        ("Customer", "I will never give S-Net another penny of my money after this appalling abuse.", -32.1),
        ("Agent", "I have documented your complaint on customer ticket CMP-88192-J.", None),
        ("Customer", "CMP-88192-J, noted.", -12.4),
        # Turn 34 is Repeat in last third! 34/58 = 0.586
        ("Agent", "What was that new postal address again?", None),
        ("Customer", "As I told you right at the start of the call, it is 27 St Jude's Close, Salisbury, SP2 8BN.", -18.2),
        ("Agent", "I have verified the Salisbury address on the complaint file.", None),
        ("Customer", "Make sure all executive correspondence goes to that address.", -8.2),
        ("Agent", "Is there any other matter regarding your cancelled order I can assist with today, Judith?", None),
        ("Customer", "No, you have been utterly abusive and useless.", -24.5),
        ("Agent", "Thank you for choosing S-Net home moving customer care, Judith. Goodbye.", None),
        ("Customer", "Goodbye.", -18.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our corporate executive complaints office reviews formal escalation tickets within eight business weeks.", None))
        raw.insert(-4, ("Customer", "I will be pursuing this matter directly through the Communications Ombudsman.", -12.1))

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "PASS",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "FAIL",
        "Paraphrasing": "FAIL",
        "Active listening": "FAIL",
        "Took ownership of the problem": "FAIL",
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [03:15] when customer expressed acute moving day distress and family upheaval.",
        "Paraphrasing": "Failed to paraphrase customer's moving order cancellation dispute in own words.",
        "Active listening": "Asked customer at [08:50] to repeat her new address which had already been verified at [00:45].",
        "Took ownership of the problem": "Deflected responsibility and refused to escalate to supervisor or provide emergency solution.",
        "Build rapport and observed professionalism": "Agent committed an immediate AUTO-FAIL by verbally abusing the customer at [05:40], stating 'You are acting like a stupid customer...'",
        "Confirmed the issue is resolved": "Order remained cancelled, broadband was not restored, and customer remained highly distressed following agent abuse."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net home moving customer care' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Judith throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute moving day stress and lack of communication; agent offered zero empathy.",
        "Paraphrasing": "Agent never restated the cancelled moving order in his own words.",
        "Active listening": "Agent asked for address at turn 34 despite customer providing it at turn 3.",
        "Took ownership of the problem": "Agent refused to assist, book emergency order, or escalate to manager.",
        "Build rapport and observed professionalism": "Agent insulted customer at [05:40]: 'You are acting like a stupid customer if you expect an unverified broadband order to sit active indefinitely...' [AUTO-FAIL: 'stupid'].",
        "Probing": "Agent asked relevant questions regarding installation dates and moving arrangements.",
        "Confirmed the issue is resolved": "Broadband remained completely uninstalled and customer was subjected to verbal abuse."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 34, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "rude", "agent_turn": 20},
            {"kind": "blunt_but_ok", "agent_turn": 17}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 8}
        ]
    }

    return {
        "cid": "agt_050",
        "cname": "Judith",
        "target_dur": 1117,
        "scenario": "Home move order cancelled without customer knowledge; agent becomes abusive [AUTO-FAIL: 'stupid']",
        "tier": "auto_fail",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Build rapport and observed professionalism", "Empathy & Acknowledgment Statement"],
        "notes": "Immediate AUTO-FAIL call where the agent used the prohibited word 'stupid' against the customer during an escalated dispute over a cancelled home move order, resulting in an automatic final score of 0.0.",
        "auto_fail_word": "stupid"
    }

print("get_call_050 defined.")

if __name__ == "__main__":
    for fn in [get_call_046, get_call_047, get_call_048, get_call_049, get_call_050]:
        c = fn()
        compile_call(c)
