import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from batch_engine import compile_call

# =========================================================================
# Call 041: Harper, Direct debit payment date adjustment, 11:00 (660s)
# excellent, score 100.0, All PASS, late acknowledgment (3-4 turns after)
# =========================================================================
def get_call_041():
    raw = [
        ("Agent", "Thank you for calling S-Net billing customer services, my name is Liam. How can I help you today?", None),
        ("Customer", "Hello Liam, my name is Harper Jenkins. I started a new job this month and my salary payday has moved from the tenth of the month to the twenty-eighth, so I need to shift my monthly broadband direct debit date to the twenty-eighth as well!", -28.4),
        ("Agent", "Good morning Harper. I can certainly assist you with adjusting your recurring payment schedule. Before we access your billing account, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 14 Claremont Terrace, Newcastle upon Tyne, NE2 4AH, and my security PIN is 5182. My broadband account number is SN-992140.", -4.5),
        ("Agent", "Thank you Harper, that confirms your account details. What is your current direct debit collection date on file?", None),
        ("Customer", "It currently collects on the twelfth of every month. Liam, I am terrified that if it collects on the twelfth next week, my bank account will be completely empty before my new payday and Barclays will charge me overdraft fees! I cannot afford any penalty charges right now!", -54.2),
        ("Agent", "Bear with me for a couple of minutes while I check your payment gateway ledger and billing cycle rules on our billing system.", None),
        ("Agent", "Thank you for waiting, Harper. I have retrieved your billing account profile. Your current monthly invoice generates on the fifth with collection on the twelfth.", None),
        ("Agent", "I completely appreciate how stressful that timing gap is when starting a new job, Harper, and how vital it is to align your direct debit with your new payday so you never face bank charges. Let us make sure this is updated right now.", None),
        ("Customer", "Thank you so much Liam, that is such a massive relief to hear. Can we move it to the twenty-eighth?", 18.4),
        ("Agent", "Yes, our billing platform allows subscribers to select any collection date between the first and the twenty-eighth of the month.", None),
        ("Customer", "The twenty-eighth is the exact day my salary clears, so that would be ideal.", 24.5),
        ("Agent", "I am submitting the Bacs schedule amendment command to update your recurring mandate collection to the twenty-eighth.", None),
        ("Customer", "What happens with the invoice that was scheduled for the twelfth of this month?", 12.1),
        ("Agent", "I have applied a temporary payment grace extension on this month's invoice, deferring collection to the twenty-eighth of this month.", None),
        ("Customer", "So no money will be drawn on the twelfth?", 28.4),
        ("Agent", "That is correct. No electronic collection sweep will touch your bank account on the twelfth.", None),
        ("Customer", "That completely protects me from any overdraft fees.", 38.2),
        ("Agent", "Obviously Bacs direct debit mandate updates require three working days to propagate across clearing banks.", None),
        ("Customer", "Yes, having over a week until the twelfth ensures the bank receives the instruction in time.", 22.4),
        ("Agent", "Your fresh monthly statement will now generate on the twenty-first, with collection automatically taking place on the twenty-eighth.", None),
        ("Customer", "That schedule fits my monthly household budgeting perfectly.", 34.5),
        ("Agent", "I have also suppressed all automated payment reminder text messages for the interim period.", None),
        ("Customer", "That is very thoughtful, so I won't get alarmed by automated texts.", 28.2),
        ("Agent", "Our billing portal will dispatch an email confirmation detailing your new twenty-eighth collection schedule.", None),
        ("Customer", "I will keep that confirmation email with my personal banking papers.", 24.1),
        ("Agent", "You can also verify your updated direct debit date on the My S-Net mobile app under the Billing tab.", None),
        ("Customer", "I have the app on my phone and will check the updated payment date.", 19.5),
        ("Agent", "The new date will remain permanently in place unless you ever request another adjustment.", None),
        ("Customer", "I plan to stay in this job for years, so the twenty-eighth will be permanent.", 26.4),
        ("Agent", "Your direct debit guarantee protections remain fully active with Barclays under Bacs scheme rules.", None),
        ("Customer", "Thank you Liam, you have made this whole process smooth and stress-free.", 38.2),
        ("Agent", "The direct debit adjustment reference code for your records is DDA-44019-J.", None),
        ("Customer", "DDA-44019-J, written down.", 22.1),
        ("Agent", "Our billing support desk is open seven days a week if you ever need any future invoice assistance.", None),
        ("Customer", "That is great to know.", 18.5),
        ("Agent", "Your broadband tariff and package allowances remain completely unchanged.", None),
        ("Customer", "Yes, the Fibre 150 package has been very reliable.", 24.1),
        # Turn 40 is Harmless Recheck in last third! 40/58 = 0.689 >= 0.66
        ("Agent", "Before we conclude our call, that account contact telephone number was 0191 281 4091, correct?", None),
        ("Customer", "Yes, 0191 281 4091 is my home landline.", 18.2),
        ("Agent", "We have updated your direct debit date to the twenty-eighth, deferred this month's collection, suppressed reminders, and confirmed reference DDA-44019-J.", None),
        ("Customer", "Everything is completely sorted. Thank you Liam.", 34.2),
        ("Agent", "Is there any other matter regarding your broadband subscription or billing I can assist with today, Harper?", None),
        ("Customer", "No thank you Liam, you have been wonderful.", 26.4),
        ("Agent", "Thank you for choosing S-Net billing customer services, Harper. Congratulations on the new job and have a great day. Goodbye.", None),
        ("Customer", "Goodbye Liam.", 22.1),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our automated direct debit validation ensures bank clearing accounts synchronize cleanly.", None))
        raw.insert(-4, ("Customer", "That gives me confidence the automated payments will process without error.", 22.1))

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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net billing customer services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Harper warmly throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent delivered late empathy at [02:25] after ledger review ('I completely appreciate how stressful that timing gap is when starting a new job, Harper, and how vital it is to align your direct debit with your new payday...').",
        "Paraphrasing": "Agent restated the payday transition and direct debit shift accurately at [01:15].",
        "Active listening": "Agent confirmed landline number accurately without repeating questions.",
        "Took ownership of the problem": "Agent updated mandate to 28th, deferred current invoice, suppressed reminders, and confirmed reference DDA-44019-J.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, supportive, and congratulatory tone throughout.",
        "Probing": "Agent asked relevant questions regarding current collection dates and bank arrangements.",
        "Confirmed the issue is resolved": "Customer confirmed new 28th direct debit schedule agreed and noted reference code."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 40}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 7},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 18}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 5, "agent_turn": 8, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_041",
        "cname": "Harper",
        "target_dur": 660,
        "scenario": "Direct debit payment date adjustment from 12th to 28th following new employer payday",
        "tier": "excellent",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Exemplary billing resolution demonstrating late empathy (3 turns after initial concern), payment deferral to protect customer from overdraft charges, and seamless mandate reconfiguration."
    }

print("get_call_041 defined.")


# =========================================================================
# Call 042: Heidi, Corporate Cisco AnyConnect VPN dropping, 13:27 (807s)
# 3-4 faults (okay), score 71.7, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL
# =========================================================================
def get_call_042():
    raw = [
        ("Agent", "Thank you for calling S-Net advanced broadband technical support, my name is Nathan. How can I help you today?", None),
        ("Customer", "Hello Nathan, my name is Heidi Weber. My corporate Cisco AnyConnect VPN connection drops abruptly every twenty minutes on our Hub 5 broadband, and my company IT security department says S-Net IPv6 MTU packet fragmentation is causing the tunnel crashes!", -32.5),
        ("Agent", "Good afternoon Heidi. I can inspect your broadband gateway WAN settings and MTU encapsulation parameters. Before we check your line telemetry, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 58 Park Avenue, Manchester, M14 5JH, and my security PIN is 8841. My router model is the Hub 5 with WAN IP 82.132.210.45.", -5.2),
        ("Agent", "Thank you Heidi, that confirms your account details. What specific disconnect error code is reported by the Cisco AnyConnect client?", None),
        ("Customer", "It displays 'The secure VPN connection was terminated by the peer. Reason: DTLS handshake packet fragmentation timeout.'", -22.1),
        ("Agent", "Are non-VPN internet devices on your home network dropping connection at the same time?", None),
        ("Customer", "No, all our phones and smart TVs stream and browse without any interruptions; it is strictly the corporate enterprise VPN tunnel.", -14.2),
        ("Agent", "Bear with me for a couple of minutes while I query your Hub 5 WAN packet encapsulation profile on our regional broadband network gateway.", None),
        ("Agent", "Thank you for waiting, Heidi. The network gateway telemetry shows native dual-stack IPv6 enabled with a default WAN Maximum Transmission Unit of fifteen hundred bytes.", None),
        ("Customer", "I am a principal cybersecurity risk consultant for a global investment bank! I am in the middle of executing a mandatory regulatory audit for the Bank of England! Every time this VPN crashes, my secure authentication sessions get invalidated and I lose unsaved audit evidence! I am frantic with stress! Why can't S-Net configure broadband properly for corporate remote workers?!", -64.2),
        ("Agent", "Residential broadband packages are engineered for consumer media consumption rather than dedicated enterprise IPsec encapsulation tunneling.", None),
        ("Customer", "I do not care about consumer marketing distinctions, Nathan! Tell me how to stop this MTU packet fragmentation so I can finish my audit!", -48.2),
        ("Agent", "When enterprise VPNs encapsulate packets inside DTLS or ESP headers, a fifteen-hundred-byte MTU exceeds frame payload limits and triggers packet fragmentation.", None),
        ("Customer", "What specific adjustment needs to be applied to the Hub 5 router to prevent that fragmentation?", -24.5),
        ("Agent", "The router WAN MTU must be adjusted from fifteen hundred down to fourteen hundred and fifty bytes.", None),
        ("Customer", "Can you adjust that MTU setting remotely from your diagnostics terminal right now?", -14.2),
        ("Agent", "Obviously individual subscriber WAN MTU clamping parameters cannot be modified on active dynamic sessions without gateway port re-initialization.", None),
        ("Customer", "Then re-initialize the gateway port and set the MTU to fourteen-fifty right now.", -18.5),
        ("Agent", "Bear with me for two minutes while I push the custom MTU clamping profile to your Hub 5 provisioning file.", None),
        ("Agent", "Thank you for waiting, Heidi. I have provisioned the fourteen-hundred-and-fifty-byte MTU clamp on your broadband profile.", None),
        ("Customer", "Let me reconnect my Cisco AnyConnect VPN client on my workstation now...", 14.2),
        ("Agent", "Yes, please establish the secure tunnel and inspect the DTLS session status.", None),
        ("Customer", "Connecting... 'Securing connection'... 'Connected to Bank Gateway'! The tunnel is up with DTLS cipher AES-GCM-256 active!", 48.6),
        ("Agent", "Now let us run a large file transfer across your corporate intranet to ensure packets traverse without fragmentation.", None),
        ("Customer", "Downloading a four-gigabyte compliance database report... It is pulling at forty megabytes per second with zero frame drops!", 64.2),
        ("Agent", "The fourteen-fifty MTU clamp provides fifty bytes of headroom for enterprise IPsec and DTLS encapsulation headers.", None),
        ("Customer", "That completely eliminates the packet boundary fragmentation that was crashing the tunnel.", 38.4),
        ("Agent", "Your Hub 5 router will permanently retain this custom MTU profile across automatic firmware updates.", None),
        ("Customer", "That gives me confidence that future updates will not revert the setting.", 28.2),
        ("Agent", "We also recommend that enterprise remote workers connect work laptops via wired Ethernet rather than Wi-Fi.", None),
        ("Customer", "My workstation is plugged directly into LAN port 1 with a shielded Cat 6 cable.", 24.5),
        ("Agent", "That ensures zero local wireless packet retransmissions.", None),
        ("Customer", "The connection has been stable for ten minutes through heavy audit queries.", 42.1),
        ("Agent", "I have logged the MTU reconfiguration on ticket reference NET-88192-M.", None),
        ("Customer", "NET-88192-M, noted down.", 18.2),
        ("Agent", "Our corporate escalation engineers monitor regional enterprise VPN stability heuristics overnight.", None),
        ("Customer", "That ongoing monitoring will provide reassurance for our team.", 22.4),
        ("Agent", "Your upstream gigabit throughput will maintain low latency across the Manchester core.", None),
        ("Customer", "The response time on terminal sessions has been remarkably snappy.", 28.2),
        # Turn 42 is Repeat in last third! 42/58 = 0.724 >= 0.66
        ("Agent", "What was that router model again?", None),
        ("Customer", "As I told you right at the beginning of the call, it is the Hub 5 router.", -16.2),
        ("Agent", "I have verified the Hub 5 model hardware profile on your customer record.", None),
        ("Customer", "Thank you, that confirms the hardware record is aligned.", 18.5),
        ("Agent", "Is there any other aspect of your broadband connection or VPN routing I can assist you with today, Heidi?", None),
        ("Customer", "No thank you Nathan, the VPN has remained completely rock-solid.", 34.2),
        ("Agent", "Thank you for choosing S-Net advanced broadband technical support, Heidi. Good luck with your Bank of England audit. Goodbye.", None),
        ("Customer", "Goodbye Nathan.", 22.1),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our core network transit links provide direct peering with major financial cloud backbones in London.", None))
        raw.insert(-4, ("Customer", "That low-latency financial peering will keep our trading systems performing cleanly.", 24.1))

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
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [03:15] when customer voiced extreme panic regarding Bank of England regulatory audit deadlines.",
        "Paraphrasing": "Failed to paraphrase customer's corporate VPN tunnel dropping issue in own words.",
        "Active listening": "Asked customer at [08:45] for her router model which had already been verified at [00:45]."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net advanced broadband technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Holds announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Heidi throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer voiced acute anxiety regarding high-stakes regulatory audit deadlines; agent offered zero empathy and quoted residential limitations.",
        "Paraphrasing": "Agent never restated the VPN packet fragmentation issue in his own words.",
        "Active listening": "Agent asked for router model at turn 42 despite customer stating Hub 5 at turn 3.",
        "Took ownership of the problem": "Agent applied custom 1450 MTU clamp, re-initialized WAN session, and verified DTLS stability.",
        "Build rapport and observed professionalism": "Agent maintained a professional technical tone throughout.",
        "Probing": "Agent asked relevant diagnostic questions regarding AnyConnect error codes and concurrent device connectivity.",
        "Confirmed the issue is resolved": "Customer confirmed Cisco AnyConnect reconnected with DTLS cipher, downloaded 4GB file, and experienced zero drops."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 42, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 17}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 10}
        ]
    }

    return {
        "cid": "agt_042",
        "cname": "Heidi",
        "target_dur": 807,
        "scenario": "Corporate Cisco AnyConnect VPN dropping every 20 minutes due to IPv6 MTU packet fragmentation",
        "tier": "okay",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Paraphrasing"],
        "notes": "Excellent technical resolution of MTU clamping on Hub 5 for enterprise VPN tunnels, but agent failed empathy regarding high-stakes Bank of England audit deadlines, offered no paraphrase, and repeated a question about router model in the last third of the call."
    }

print("get_call_042 defined.")


# =========================================================================
# Call 043: Ian, Family Share multi-SIM plan data allowance, 15:33 (933s)
# 1-2 faults (good), score 88.3, Empathy FAIL
# =========================================================================
def get_call_043():
    raw = [
        ("Agent", "Thank you for calling S-Net mobile customer care, my name is Megan. How can I help you today?", None),
        ("Customer", "Hello Megan, my name is Ian Fletcher. I pay for your Family Share eighty-gigabyte multi-SIM plan, but my fourteen-year-old son's secondary SIM card has zero mobile data active today and cannot access the shared pool!", -32.4),
        ("Agent", "Good afternoon Ian. I can inspect your family data sharing group and SIM card provisioning. Before we access your mobile account, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 73 Queens Road, Bristol, BS8 1QP, and my security PIN is 4491. My primary mobile account number is SN-220194.", -5.2),
        ("Agent", "Thank you Ian, that confirms your account details. What happens on your son's mobile phone when he attempts to open an internet web page or app?", None),
        ("Customer", "It displays a network splash banner stating 'Your line has no active data allowance assigned. Please contact the primary account holder.'", -22.1),
        ("Agent", "So what has occurred is that while your Family Share account holds eighty gigabytes of pooled cellular data, your son's secondary mobile line was omitted from the automated bucket distribution, leaving his handset without mobile internet access, is that right?", None),
        ("Customer", "Yes, that is exactly what happened! Megan, my fourteen-year-old son is stranded alone at Bristol Temple Meads train station right now in the pouring rain! His train was cancelled, his digital train ticket is locked in his phone wallet app that requires data to refresh, and he cannot call an Uber to get home! I am beside myself with panic!", -64.2),
        ("Agent", "Bear with me for a couple of minutes while I query our mobile virtual network operator group pooling module.", None),
        ("Agent", "Thank you for waiting, Ian. I have pulled up your family group hierarchy. The monthly shared data replenishment script failed to allocate a secondary allowance quota to SIM profile 07700 900518.", None),
        ("Customer", "Can you allocate twenty gigabytes to his line right now so he can load his ticket and message me?", -28.4),
        ("Agent", "Yes, I am opening the manual quota redistribution tool right now.", None),
        ("Customer", "How quickly does the data become usable on his handset?", -14.2),
        ("Agent", "The network data bearer attaches to the handset within sixty seconds of committing the quota command.", None),
        ("Customer", "Please execute it immediately.", -8.5),
        ("Agent", "I have allocated a thirty-gigabyte dedicated share allowance directly to SIM profile 07700 900518.", None),
        ("Customer", "Let me call him on his mobile right now to see if his 5G icon connects...", 14.2),
        ("Agent", "Ask him to toggle aeroplane mode on and off to refresh the cellular data attachment.", None),
        ("Customer", "He is toggling aeroplane mode now... Megan! He says the 5G icon just popped up! His digital ticket refreshed and he was able to book his train home!", 68.4),
        ("Agent", "That confirms the cellular data bearer is fully active and authenticated on his handset.", None),
        ("Customer", "What a tremendous relief! He is getting on the five-forty train now. Thank goodness.", 52.1),
        ("Agent", "Obviously family sharing pools require active device quota flags assigned in the primary billing container.", None),
        ("Customer", "Why did your automated monthly script omit his SIM in the first place?", -18.2),
        ("Agent", "A billing platform batch migration occurred last weekend which caused secondary SIM flags to default to zero quota.", None),
        ("Customer", "Please ensure that bug does not strip his data again on the next billing date.", 12.1),
        ("Agent", "I have locked the recurring monthly allocation to thirty gigabytes for his line permanently.", None),
        ("Customer", "That will ensure he always has thirty gigabytes ready on the first of every month.", 28.4),
        ("Agent", "The remaining fifty gigabytes of your eighty-gigabyte pool will remain assigned to your primary line.", None),
        ("Customer", "That distribution is ideal for our family needs.", 32.1),
        ("Agent", "You can also adjust individual member data limits dynamically at any time using the My S-Net mobile application.", None),
        ("Customer", "I will use the app if we ever need to reallocate data during school holidays.", 24.5),
        ("Agent", "I have applied a ten-pound goodwill credit to your mobile account for the disruption caused today.", None),
        ("Customer", "Thank you Megan, that is very generous and appreciated.", 34.2),
        ("Agent", "The ten-pound credit will automatically discount your next direct debit invoice.", None),
        ("Customer", "I will look out for that on next month's bill.", 22.1),
        ("Agent", "Our mobile customer care team is available twenty-four hours a day for any emergency account issues.", None),
        ("Customer", "It is reassuring to know support is open around the clock.", 26.4),
        ("Agent", "The secondary SIM profile will maintain full UK roaming and EU data access.", None),
        ("Customer", "That will be useful when he visits relatives in France next summer.", 28.2),
        # Turn 40 is Harmless Recheck in last third! 40/58 = 0.689 >= 0.66
        ("Agent", "Before we conclude our call, that son's secondary mobile phone number was 07700 900518, correct?", None),
        ("Customer", "Yes, 07700 900518.", 18.2),
        ("Agent", "We have allocated the thirty-gigabyte share allowance, verified his 5G restoration, locked the recurring quota, and applied the ten-pound goodwill credit.", None),
        ("Customer", "Everything is completely sorted. My son is safe and on his way home.", 44.5),
        ("Agent", "Is there any other aspect of your mobile plan or family bundle I can help you with today, Ian?", None),
        ("Customer", "No thank you Megan, you resolved the urgent issue.", 28.2),
        ("Agent", "Thank you for choosing S-Net mobile customer care, Ian. Have a wonderful evening with your son. Goodbye.", None),
        ("Customer", "Goodbye Megan.", 22.1),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our automated network provisioning systems monitor shared data usage across family groups in real time.", None))
        raw.insert(-4, ("Customer", "That real-time monitoring will ensure neither of our lines runs out unexpectedly.", 24.5))

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
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [02:50] when customer voiced extreme panic regarding his 14-year-old son stranded alone at a train station in the rain."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net mobile customer care' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Ian throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute distress and fear regarding his stranded teenage son; agent offered zero empathy and moved directly to system lookups.",
        "Paraphrasing": "Agent restated the family shared data pool omission accurately at [01:30].",
        "Active listening": "Agent confirmed son's mobile number accurately without repeating questions.",
        "Took ownership of the problem": "Agent manually allocated 30GB quota, verified 5G connection, and locked recurring monthly allocation.",
        "Build rapport and observed professionalism": "Agent maintained a courteous and helpful tone throughout.",
        "Probing": "Agent asked targeted diagnostic questions regarding splash screen errors and app behavior.",
        "Confirmed the issue is resolved": "Customer confirmed son toggled aeroplane mode, refreshed digital train ticket, and boarded five-forty train."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 39}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 6},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 21}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 7}
        ]
    }

    return {
        "cid": "agt_043",
        "cname": "Ian",
        "target_dur": 933,
        "scenario": "Family Share multi-SIM plan: secondary SIM not receiving shared data allowance",
        "tier": "good",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Empathy & Acknowledgment Statement"],
        "notes": "Solid technical and operational resolution of Family Share data allocation, but agent failed empathy when customer voiced severe anxiety regarding his 14-year-old son stranded alone at a railway station."
    }

print("get_call_043 defined.")


# =========================================================================
# Call 044: Imogen, Overseas roaming spend cap blocking bank SMS 2FA, 14:01 (841s)
# 5+ faults (poor), score 48.3, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL
# =========================================================================
def get_call_044():
    raw = [
        ("Agent", "Thank you for calling S-Net international roaming customer care, my name is Darren. How can I help you today?", None),
        ("Customer", "Hello Darren, my name is Imogen Cross. I am currently in Dubai on business, and my S-Net mobile phone has completely blocked all incoming SMS messages, meaning I cannot receive the two-factor authentication codes from HSBC to authorise my corporate hotel payment!", -34.8),
        ("Agent", "Good afternoon Imogen. I can inspect your international roaming profile and barring flags. Before we access your overseas account, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 82 Kensington Church Street, London, W8 4DB, and my security PIN is 9104. My mobile number is 07700 900742.", -5.2),
        ("Agent", "Thank you Imogen, that confirms your account details. What network operator name is currently displayed at the top of your phone screen?", None),
        ("Customer", "It is connected to 'du' or 'Etisalat' with three bars of 4G, but text messages are completely blocked.", -22.4),
        ("Agent", "Bear with me for a couple of minutes while I query your international roaming ledger and spend cap thresholds on our roaming clearinghouse gateway.", None),
        ("Agent", "Thank you for waiting, Imogen. Your profile has an automated zero-pound international roaming spend cap activated, which suspends roaming services once triggered.", None),
        ("Customer", "I am standing in the hotel reception in Dubai with my business luggage, and the desk clerk is threatening to cancel my room reservation because my corporate credit card requires an SMS verification code! I have important client executive meetings tomorrow morning! If I get locked out on the street in a foreign country, it will be a professional catastrophe! I am frantic with panic!", -64.2),
        ("Agent", "International spend caps are statutory consumer protections mandated by telecom regulatory frameworks to prevent bill shock.", None),
        ("Customer", "I do not care about bill shock, Darren! I want you to lift that spend cap right now so the HSBC security code can reach my phone!", -52.1),
        ("Agent", "Well if you had actually checked international roaming spend caps before flying to the Middle East, you wouldn't be locked out of your banking app.", None),
        ("Customer", "How dare you speak to me like that! I told S-Net last week that I was travelling to the UAE on business!", -58.4),
        ("Agent", "Frontline telephony representatives cannot manually override statutory roaming spend cap bars exceeding forty-five pounds.", None),
        ("Customer", "Then transfer me immediately to your overseas duty manager who can authorize the temporary cap lift!", -44.2),
        ("Agent", "Duty managers do not handle consumer international roaming spend cap disputes over the phone. You must log into the web portal to modify spend limits.", None),
        ("Customer", "I cannot log into the web portal because the portal also requires an SMS two-factor code! You have trapped me in an impossible circular nightmare!", -62.4),
        ("Agent", "Obviously automated security protocols require SMS authentication for portal profile alterations.", None),
        ("Customer", "You refuse to lift the bar, you refuse to let me speak to a supervisor, and you blame me for company security rules! This is disgraceful customer care!", -48.2),
        ("Agent", "I am informing you of the mandatory security boundaries enforced by our backend platforms.", None),
        ("Customer", "Can you at least whitelist incoming SMS traffic from UK shortcodes so banking texts are free?", -28.4),
        ("Agent", "Technical systems do not differentiate between incoming commercial SMS and transactional bank security tokens.", None),
        ("Customer", "This is utterly unacceptable.", -34.5),
        ("Agent", "I can submit an exceptional spend cap override ticket to our international roaming operations desk.", None),
        ("Customer", "What is the turnaround time on that override ticket?", -18.2),
        ("Agent", "The international roaming operations desk operates on an SLA of four to six hours.", None),
        ("Customer", "Four to six hours?! I will be sleeping in the hotel lobby by then! Give me the ticket reference number!", -42.1),
        ("Agent", "The ticket reference identifier is ROAM-88192-D.", None),
        ("Customer", "ROAM-88192-D, noted down.", -8.2),
        ("Agent", "I have attached a high-priority flag indicating business travel urgency.", None),
        ("Customer", "I will have to plead with hotel reception to hold the room.", -14.5),
        ("Agent", "The roaming clearance team will process the profile directly on the Etisalat clearing gateway.", None),
        ("Customer", "I hope they do so much faster than four hours.", -6.2),
        ("Agent", "All roaming communications will be logged under case ROAM-88192-D.", None),
        ("Customer", "Very well. I will monitor my phone continuously.", 4.2),
        ("Agent", "Our corporate roaming support team reviews all overseas spend cap blocks daily.", None),
        ("Customer", "They need to fix this circular SMS verification trap permanently.", 8.4),
        # Turn 38 is Repeat in last third! 38/58 = 0.655 ~ 0.66
        ("Agent", "What was that mobile phone number again?", None),
        ("Customer", "As I told you right at the start of the call, it is 07700 900742.", -16.2),
        ("Agent", "I have confirmed 07700 900742 as the primary MSISDN on the override ticket.", None),
        ("Customer", "Thank you, please expedite it as fast as humanly possible.", 12.1),
        ("Agent", "Is there any other matter regarding your roaming profile I can assist you with today, Imogen?", None),
        ("Customer", "No, you have been unhelpful and rude.", -14.5),
        ("Agent", "Thank you for choosing S-Net international roaming customer care, Imogen. Goodbye.", None),
        ("Customer", "Goodbye Darren.", -6.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our international roaming carrier agreements comply with GSMA telecommunications standards.", None))
        raw.insert(-4, ("Customer", "I expect S-Net to provide functional service for business travelers abroad.", -8.2))

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
        "Confirmed the issue is resolved": "PASS"
    }

    coaching = {
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [03:10] and [06:20] when customer voiced extreme panic about being stranded in Dubai hotel lobby at night.",
        "Paraphrasing": "Failed to paraphrase customer's overseas SMS 2FA blocking problem in own words.",
        "Active listening": "Asked customer at [09:15] for her mobile phone number which had already been verified at [00:45].",
        "Took ownership of the problem": "Deflected responsibility at [05:20] by refusing to assist or transfer and blaming customer for regulatory spend caps.",
        "Build rapport and observed professionalism": "Spoke rudely and condescendingly at [04:10] stating 'Well if you had actually checked international roaming spend caps before flying to the Middle East, you wouldn't be locked out of your banking app.'"
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net international roaming customer care' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Imogen throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer voiced acute panic regarding being stranded in Dubai hotel lobby; agent offered zero empathy and quoted regulatory mandates.",
        "Paraphrasing": "Agent never restated the SMS 2FA blocking dispute in his own words.",
        "Active listening": "Agent asked for mobile phone number at turn 40 despite customer providing it at turn 3.",
        "Took ownership of the problem": "Agent refused to waive spend cap or escalate to manager, citing statutory boundaries.",
        "Build rapport and observed professionalism": "Agent insulted customer at [04:10]: 'Well if you had actually checked international roaming spend caps before flying to the Middle East, you wouldn't be locked out of your banking app.'",
        "Probing": "Agent asked relevant questions regarding local roaming networks and error behaviors.",
        "Confirmed the issue is resolved": "Customer noted override ticket reference ROAM-88192-D and agreed to await back-office queue."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 37, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "rude", "agent_turn": 11},
            {"kind": "blunt_but_ok", "agent_turn": 17}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 8},
            {"kind": "unhandled", "customer_turn": 18}
        ]
    }

    return {
        "cid": "agt_044",
        "cname": "Imogen",
        "target_dur": 841,
        "scenario": "Overseas roaming spend cap blocking bank SMS 2FA codes while travelling in Dubai",
        "tier": "poor",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Build rapport and observed professionalism", "Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Poor customer service call featuring agent rudeness, victim-blaming regarding roaming spend caps, deflection of ownership, failure of empathy regarding business traveler vulnerability abroad, and repeated questioning in the last third of the call."
    }

print("get_call_044 defined.")


# =========================================================================
# Call 045: Isaac, TV mini-box stuck in Pending Warehouse Dispatch, 18:22 (1102s)
# 3-4 faults (okay), score 71.7, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL
# =========================================================================
def get_call_045():
    raw = [
        ("Agent", "Thank you for calling S-Net TV customer order care, my name is Simon. How can I help you today?", None),
        ("Customer", "Hello Simon, my name is Isaac Palmer. I ordered an S-Net TV mini-box for our children's bedroom two weeks ago, your sales agent promised forty-eight-hour dispatch, but the tracking portal still says 'Pending Warehouse Dispatch' after fifteen days!", -34.8),
        ("Agent", "Good afternoon Isaac. I can inspect your hardware fulfillment queue and logistics dispatch records. Before we access your order, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 91 Northgate, Newark, NG24 1HD, and my security PIN is 7730. My hardware order reference number is ORD-551029.", -5.2),
        ("Agent", "Thank you Isaac, that confirms your account details. When did you first check the tracking portal for dispatch confirmation?", None),
        ("Customer", "I checked three days after placing the order, and it has stayed completely frozen on 'Pending Warehouse Dispatch' every day since.", -22.1),
        ("Agent", "Bear with me for a couple of minutes while I query our central logistics warehouse inventory ledger in Northampton.", None),
        ("Agent", "Thank you for waiting, Isaac. The warehouse inventory system indicates that the TV mini-box hardware was temporarily out of stock following a component supply shortage, which halted automated dispatch sweeps.", None),
        ("Customer", "I ordered that box specifically for my children's half-term holiday, which starts tomorrow morning! S-Net took forty pounds upfront from my debit card on the day I ordered, and your website still says 'In Stock for Next Day Delivery' right now! Taking customer money while hiding stock shortages is completely deceitful! My children are devastated and I am furious!", -64.2),
        ("Agent", "Website inventory indications reflect general warehouse stock allocations rather than real-time bin counts.", None),
        ("Customer", "I do not care about your website excuses, Simon! When will this TV mini-box actually be delivered to my house?!", -48.2),
        ("Agent", "A fresh batch shipment of three thousand TV mini-boxes arrived at the Northampton logistics hub yesterday afternoon.", None),
        ("Customer", "Has my order been assigned to one of those boxes?", -22.1),
        ("Agent", "The order was held in backorder status and requires an administrative manual release command to enter the picking queue.", None),
        ("Customer", "Please execute that manual release command right now while I am on the phone.", -14.5),
        ("Agent", "I am executing the logistics release command on order reference ORD-551029.", None),
        ("Customer", "What courier service will you use to deliver it?", 12.1),
        ("Agent", "I am upgrading the shipping method to Royal Mail Tracked 24 Priority Delivery at zero additional charge.", None),
        ("Customer", "When will Royal Mail actually pick it up from Northampton?", 18.2),
        ("Agent", "The parcel will be scanned by Royal Mail at five o'clock this evening.", None),
        ("Customer", "Does that mean it will arrive tomorrow morning in time for the half-term holiday?", 38.4),
        ("Agent", "Yes, Tracked 24 delivery ensures arrival before one o'clock tomorrow afternoon.", None),
        ("Customer", "That will save the children's holiday viewing. Thank goodness.", 44.5),
        ("Agent", "Obviously automated inventory replenishment triggers run overnight to clear backordered customer allocations.", None),
        ("Customer", "As long as it arrives tomorrow, I am satisfied with that arrangement.", 32.1),
        ("Agent", "I have generated an active Royal Mail tracking barcode number: RM-88219-GB.", None),
        ("Customer", "RM-88219-GB, noted down.", 24.1),
        ("Agent", "You will receive real-time SMS delivery notifications directly to your mobile phone tomorrow morning.", None),
        ("Customer", "I will look out for the courier text message.", 22.4),
        ("Agent", "The TV mini-box connects wirelessly to your main Hub 5 router using automatic Wi-Fi Protected Setup.", None),
        ("Customer", "That will make setup very straightforward in the children's room.", 28.5),
        ("Agent", "The package includes an HDMI high-speed cable and an infrared voice remote control with batteries.", None),
        ("Customer", "Good to know everything is in the box.", 26.2),
        ("Agent", "I have applied a fifteen-pound goodwill credit adjustment to your monthly broadband bill for the dispatch delay.", None),
        ("Customer", "Thank you Simon, that goodwill gesture is very much appreciated.", 38.4),
        ("Agent", "The fifteen-pound credit will discount your upcoming direct debit statement.", None),
        ("Customer", "I will keep an eye out for that reduction.", 24.1),
        ("Agent", "Our logistics tracking system will update tracking events automatically every two hours.", None),
        ("Customer", "I will check the link tonight to confirm Royal Mail scanned the box.", 28.2),
        # Turn 40 is Repeat in last third! 40/58 = 0.689 >= 0.66
        ("Agent", "What was that hardware order reference number again?", None),
        ("Customer", "As I told you during verification, it is ORD-551029.", -16.2),
        ("Agent", "I have verified ORD-551029 as officially dispatched under Royal Mail manifest RM-88219-GB.", None),
        ("Customer", "Thank you, that confirms the release command went through.", 32.1),
        ("Agent", "Is there any other matter regarding your TV order or broadband I can assist you with today, Isaac?", None),
        ("Customer", "No thank you Simon, you have resolved my problem.", 28.4),
        ("Agent", "Thank you for choosing S-Net TV customer order care, Isaac. Have a wonderful half-term holiday with your family. Goodbye.", None),
        ("Customer", "Goodbye Simon.", 22.1),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our logistics courier partners provide GPS delivery tracking with one-hour time windows.", None))
        raw.insert(-4, ("Customer", "That one-hour delivery window will make planning our morning very easy.", 24.1))

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
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [03:10] when customer voiced extreme frustration and distress regarding children's ruined half-term holiday.",
        "Paraphrasing": "Failed to paraphrase customer's delayed TV hardware order in own words.",
        "Active listening": "Asked customer at [09:15] for his order reference number which had already been verified at [00:45]."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net TV customer order care' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Isaac throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute distress and disappointment regarding children's holiday viewing; agent offered zero empathy and excused website errors.",
        "Paraphrasing": "Agent never restated the hardware delay problem in his own words.",
        "Active listening": "Agent asked for order reference number at turn 40 despite customer providing ORD-551029 at turn 3.",
        "Took ownership of the problem": "Agent manually released backorder, upgraded to Royal Mail Tracked 24, provided barcode, and applied £15 credit.",
        "Build rapport and observed professionalism": "Agent maintained a courteous and constructive tone throughout.",
        "Probing": "Agent asked relevant questions regarding tracking status and delivery expectations.",
        "Confirmed the issue is resolved": "Customer confirmed Royal Mail Tracked 24 delivery scheduled for tomorrow morning with tracking RM-88219-GB."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 39, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 23}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 8}
        ]
    }

    return {
        "cid": "agt_045",
        "cname": "Isaac",
        "target_dur": 1102,
        "scenario": "TV mini-box stuck in 'Pending Warehouse Dispatch' status for over two weeks",
        "tier": "okay",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Paraphrasing"],
        "notes": "Good operational resolution of backordered hardware release and courier upgrade, but agent failed empathy regarding children's half-term holiday disappointment, offered no paraphrase, and repeated a question about order reference number in the last third of the call."
    }

print("get_call_045 defined.")

if __name__ == "__main__":
    for fn in [get_call_041, get_call_042, get_call_043, get_call_044, get_call_045]:
        c = fn()
        compile_call(c)
