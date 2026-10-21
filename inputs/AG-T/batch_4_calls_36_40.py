import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from batch_engine import compile_call

# =========================================================================
# Call 036: Gemma, Severed overhead drop cable after storm, 11:30 (690s)
# 1-2 faults (good), score 88.3, Empathy FAIL
# =========================================================================
def get_call_036():
    raw = [
        ("Agent", "Thank you for calling S-Net fault reporting customer services, my name is Callum. How can I help you today?", None),
        ("Customer", "Hello Callum, my name is Gemma Sutherland. A severe gale last night brought a heavy oak tree branch down across our lane, and it has physically torn down our overhead telephone cable and left the wire dangling across our fence!", -34.2),
        ("Agent", "Good afternoon Gemma. I can log an emergency Openreach engineering repair ticket for external plant damage. Before we raise the infrastructure fault, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is Highfield Farm, Bwlchgwyn, Wrexham, LL11 5UH, and my security PIN is 8402. Our landline circuit identifier is SN-661024.", -6.1),
        ("Agent", "Thank you Gemma, that confirms your account details. Is the severed wire creating any physical obstruction across a public highway or vehicle carriageway?", None),
        ("Customer", "It is hanging about three feet above our farm access track, dangling over the wooden gate post and touching the grass verge.", -22.4),
        ("Agent", "So what has occurred is that storm damage and a fallen tree limb have physically severed your overhead subscriber drop cable, leaving the line detached from your premises and causing total loss of broadband and telephony service, is that right?", None),
        ("Customer", "Yes, that is exactly what happened! Our Hub router is completely dead with a flashing red broadband indicator light.", -18.2),
        ("Agent", "Bear with me for a couple of minutes while I query the local Openreach copper loop topology and external line card telemetry.", None),
        ("Agent", "Thank you for waiting, Gemma. Our metallic line test detects a complete galvanic open circuit zero metres from the local distribution pole, confirming the physical cable severance.", None),
        ("Customer", "Can you get an emergency engineer out to re-string the cable today?", -12.4),
        ("Agent", "Under standard network repair guidelines, external overhead tree damage requires a planned Openreach overhead engineering team dispatch within forty-eight hours.", None),
        ("Customer", "Forty-eight hours?! Callum, I am an organic sheep farmer in the middle of our autumn lambing season! I live completely alone on this hillside, and my electric boundary fence alarms, lambing barn cameras, and veterinary telemetry are all completely down! If an animal gets sick or escapes, I have zero mobile signal up here to call our vet! I am frantic with worry!", -64.2),
        ("Agent", "Engineering dispatch priority queues are governed strictly by national Openreach infrastructure scheduling matrices.", None),
        ("Customer", "This is an emergency safety issue with live livestock on a hill farm! You have to escalate this ticket as urgent!", -48.2),
        ("Agent", "I am populating the engineer booking request right now with a safety hazard tag.", None),
        ("Customer", "When is the earliest appointment slot the system is giving you?", -22.1),
        ("Agent", "Obviously high-level overhead wire repairs require specialist cherry-picker hydraulic lift equipment rather than standard roadside vans.", None),
        ("Customer", "I have plenty of turning space for a cherry-picker in our farmyard.", -14.2),
        ("Agent", "The earliest available specialist hoist slot is tomorrow morning between eight o'clock and one o'clock.", None),
        ("Customer", "Tomorrow morning is much better than forty-eight hours. What will the engineer need to do?", 8.4),
        ("Agent", "The engineer will clear the snagged limb, inspect the distribution pole bracket, pull fresh drop wire from the pole to your house eaves, and terminate into a new master socket.", None),
        ("Customer", "Do I need to be present on the farm for them to carry out the work?", 12.1),
        ("Agent", "Yes, an adult must be on site to allow internal access to verify sync at the master socket.", None),
        ("Customer", "I will stay in the farmhouse tomorrow morning to let them in.", 18.5),
        ("Agent", "I have confirmed the engineer booking for tomorrow morning between eight and one, appointment reference ENG-44019-W.", None),
        ("Customer", "ENG-44019-W, noted down.", 22.4),
        ("Agent", "I have also activated a temporary unlimited emergency data bundle on your registered S-Net mobile SIM card.", None),
        ("Customer", "That will help if I walk up the ridge where there is a bit of mobile reception.", 32.1),
        ("Agent", "Please take care around the dangling cable and do not attempt to handle the wire yourself.", None),
        ("Customer", "I will leave the wire completely alone until the engineer arrives.", 24.1),
        ("Agent", "The Openreach engineer will send an automated SMS update thirty minutes prior to arrival tomorrow morning.", None),
        ("Customer", "That will give me time to put our working sheepdogs into their kennels before the van arrives.", 24.5),
        ("Agent", "Our automated fault tracking system will monitor circuit continuity once the new drop wire is spliced.", None),
        ("Customer", "That will confirm the broadband signal reaches all our barn devices.", 28.1),
        ("Agent", "The replacement heavy-duty drop cable includes steel tensile support wire designed to resist branch impacts.", None),
        ("Customer", "That will give us much greater resilience during future winter storms.", 22.4),
        ("Agent", "We also recommend trimming back tree branches that encroach within two metres of the overhead span.", None),
        ("Customer", "I will ask our local tree surgeon to prune back those oak branches next week.", 18.2),
        ("Agent", "The engineer will also replace the external drop bracket anchored to your farmhouse brickwork.", None),
        ("Customer", "The old mortar around the chimney was getting a bit loose, so a fresh bracket is very welcome.", 24.5),
        # Turn 42 is Harmless Recheck in last third! 42/60 = 0.70 >= 0.66
        ("Agent", "Before we complete our call, that account contact telephone number was 01978 752109, correct?", None),
        ("Customer", "Yes, 01978 752109 is our farm landline.", 16.2),
        ("Agent", "We have confirmed the severed line fault, scheduled the specialist overhead engineer for tomorrow morning, and issued appointment reference ENG-44019-W.", None),
        ("Customer", "Thank you Callum, I appreciate you securing tomorrow morning's slot.", 34.5),
        ("Agent", "Your account will automatically receive a statutory service credit under Ofcom automatic compensation rules.", None),
        ("Customer", "That compensation credit will help offset the disruption to our farm routine.", 22.1),
        ("Agent", "The credit will appear on your next monthly billing statement following fault closure.", None),
        ("Customer", "I will look out for that on next month's invoice.", 18.4),
        ("Agent", "Is there any other aspect of your broadband or farm service I can assist you with today, Gemma?", None),
        ("Customer", "No thank you Callum, you have booked what was needed.", 28.2),
        ("Agent", "Thank you for choosing S-Net fault reporting customer services, Gemma. Stay safe on the farm and have a good day. Goodbye.", None),
        ("Customer", "Goodbye Callum.", 22.1),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our engineering field coordination centre will monitor road conditions across Wrexham overnight.", None))
        raw.insert(-4, ("Customer", "The main roads are clear, only our farm track has minor debris.", 18.2))

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
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [03:45] when customer voiced extreme panic regarding isolated hill farm livestock safety and veterinary communication loss."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net fault reporting customer services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Gemma throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute distress regarding hill farm isolation and veterinary emergency risks; agent completely ignored feelings and cited Openreach matrix rules.",
        "Paraphrasing": "Agent restated the severed drop wire and loss of service accurately at [01:30].",
        "Active listening": "Agent confirmed farm landline number without repeating questions.",
        "Took ownership of the problem": "Agent secured next-morning specialist cherry-picker appointment and provided reference ENG-44019-W.",
        "Build rapport and observed professionalism": "Agent maintained a courteous and safety-conscious tone throughout.",
        "Probing": "Agent asked targeted safety and diagnostic questions regarding cable obstruction and roadside risks.",
        "Confirmed the issue is resolved": "Customer confirmed next-morning engineer appointment agreed and noted reference code."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 41}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 6},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 17}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 12}
        ]
    }

    return {
        "cid": "agt_036",
        "cname": "Gemma",
        "target_dur": 690,
        "scenario": "Overhead drop cable severed by falling tree branch on rural lane during storm",
        "tier": "good",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Empathy & Acknowledgment Statement"],
        "notes": "Solid technical fault booking for external overhead drop wire damage, but agent failed empathy when customer voiced severe anxiety regarding isolated hill farm livestock safety."
    }

print("get_call_036 defined.")
# =========================================================================
# Call 037: George, Erroneous £220 early termination fee, 16:14 (974s)
# 5+ faults (poor), score 48.3, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL
# =========================================================================
def get_call_037():
    raw = [
        ("Agent", "Thank you for calling S-Net billing and collections, my name is Craig. How can I help you today?", None),
        ("Customer", "Hello Craig, my name is George Campbell. I moved house last month to a remote cottage where S-Net does not provide broadband, your moving agent told me no cancellation fees would apply, and yesterday you direct-debited two hundred and twenty pounds from my account as an early termination fee!", -36.4),
        ("Agent", "Good afternoon George. I can inspect your contract termination ledger. Before we look at the billing adjustments, could you confirm your full previous postal address and your account security PIN?", None),
        ("Customer", "Yes, my old address was 15 Millfield Road, York, YO23 1NQ, and my security PIN is 7018. My previous broadband contract number was SN-771920.", -5.4),
        ("Agent", "Thank you George, that confirms your account details. What specific charge description is listed on the direct debit invoice?", None),
        ("Customer", "It says 'Early Contract Termination Fee - 11 Months Remaining: £220.00' taken on November 14th without my consent!", -28.2),
        ("Agent", "Bear with me for a couple of minutes while I check your contract terms and moving team ticket notes on our database.", None),
        ("Agent", "Thank you for waiting, George. Your account profile shows an eighteen-month minimum term commenced in May, meaning eleven unserved contract months remained at cancellation.", None),
        ("Customer", "I know eleven months remained, Craig, but I moved to a rural village in North Yorkshire where S-Net has zero cable or fibre network coverage! Your customer charter explicitly states that if S-Net cannot provide service at a customer's new home, no early termination fees are charged! Taking two hundred and twenty pounds has pushed my current account into unarranged overdraft! I am furious!", -64.5),
        ("Agent", "The fee waiver policy requires proof of residency documentation to be formally validated before the billing account is closed.", None),
        ("Customer", "I sent a copy of my signed tenancy agreement and council tax bill to your address validation email three weeks ago, as instructed by your telephone agent!", -52.1),
        ("Agent", "Well if you actually paid attention to your contract terms instead of assuming moving house cancels financial obligations for free, you wouldn't be shocked by legitimate early termination fees.", None),
        ("Customer", "How dare you speak to me like that! I complied with every single requirement your company gave me!", -58.4),
        ("Agent", "Frontline telephony agents do not have administrative authority to waive or refund contract termination fees exceeding fifty pounds.", None),
        ("Customer", "Then transfer me immediately to your finance manager or billing complaints supervisor who can reverse this illegal charge!", -44.2),
        ("Agent", "Supervisors do not take inbound telephone disputes regarding early termination billing. You must submit a written dispute via our complaints web portal.", None),
        ("Customer", "You take two hundred and twenty pounds from my bank without authorization, and you refuse to let me speak to anyone who can fix it?! This is outright theft and disgraceful service!", -49.6),
        ("Agent", "Obviously fixed-term consumer broadband agreements carry contractual early exit liability under Ofcom regulations.", None),
        ("Customer", "I want this two hundred and twenty pounds refunded directly back to my debit card today!", -38.2),
        ("Agent", "As I stated, frontline customer care cannot execute discretionary card refunds for closed accounts.", None),
        ("Customer", "My bank has charged me twenty-five pounds in unarranged overdraft penalty fees because of this direct debit raid! This is causing me extreme financial hardship!", -62.4),
        ("Agent", "I am documenting your disputed tenancy proof on ticket reference TKT-88192-M.", None),
        ("Customer", "What will happen with that ticket?", -18.4),
        ("Agent", "Our back-office billing audit team will review the tenancy agreement within five to ten business days.", None),
        ("Customer", "A voucher?! I need my cash refunded to my bank account to clear the overdraft!", -32.1),
        ("Agent", "Refunds for closed accounts are processed by automated Bacs credit transfer within ten working days following audit approval.", None),
        ("Customer", "Give me the direct complaint escalation number for Ofcom and the Communications Ombudsman.", -24.5),
        ("Agent", "Our formal dispute reference number is CMP-99021-G, which you can quote to the ombudsman after eight weeks.", None),
        ("Customer", "CMP-99021-G, noted down. I will be escalating this immediately.", -12.4),
        ("Agent", "I have attached your tenancy agreement document to the ombudsman file.", None),
        ("Customer", "Very well. I will expect that Bacs refund within ten days.", -8.2),
        ("Agent", "Your closed account record will remain archived in our regulatory compliance repository for seven years.", None),
        ("Customer", "Please make sure no further direct debit mandates remain active on that closed account.", -12.1),
        ("Agent", "All electronic collection mandates with your bank have been formally cancelled in the Bacs clearing register.", None),
        ("Customer", "Good, because I will not permit another unauthorized penny to be taken.", -8.4),
        ("Agent", "Our credit collections department has applied an administrative hold to prevent debt escalation.", None),
        ("Customer", "That will keep debt recovery agencies from sending letters to my new cottage.", 12.1),
        ("Agent", "The ombudsman escalation paperwork will be archived under case identifier CMP-99021-G.", None),
        ("Customer", "I have filed all those references in my personal records folder.", 14.5),
        ("Agent", "Our compliance department reviews all disputed early termination collections monthly.", None),
        ("Customer", "I hope they review this case and realise how unfairly I have been treated.", 11.2),
        # Turn 42 is Repeat in last third! 42/58 = 0.724 >= 0.66
        ("Agent", "What was that previous postal address again?", None),
        ("Customer", "As I told you during verification, it was 15 Millfield Road, York, YO23 1NQ.", -16.2),
        ("Agent", "I have confirmed the 15 Millfield Road address on your archive record.", None),
        ("Customer", "Make sure all refund notifications go to my email address.", 14.1),
        ("Agent", "Is there any other matter regarding your closed account I can assist you with today, George?", None),
        ("Customer", "No, you have been unhelpful and rude.", -14.5),
        ("Agent", "Thank you for choosing S-Net billing and collections, George. Goodbye.", None),
        ("Customer", "Goodbye Craig.", -6.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Your data protection records will be held in strict compliance with GDPR standards.", None))
        raw.insert(-4, ("Customer", "Thank you, please ensure all marketing preferences are fully suppressed.", 8.4))

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
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [03:15] and [07:10] when customer expressed acute financial hardship and overdraft distress.",
        "Paraphrasing": "Failed to paraphrase customer's moving and early termination dispute in own words.",
        "Active listening": "Asked customer at [09:40] to repeat his previous address which had already been verified at [00:45].",
        "Took ownership of the problem": "Deflected responsibility at [05:20] by refusing to process refund or transfer to manager, telling customer to use web portal.",
        "Build rapport and observed professionalism": "Spoke rudely and condescendingly at [04:15] stating 'Well if you actually paid attention to your contract terms... you wouldn't be shocked by legitimate early termination fees.'"
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net billing and collections' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as George throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute distress over £220 taken and bank overdraft fees; agent completely ignored feelings.",
        "Paraphrasing": "Agent never restated the contractual moving dispute in his own words.",
        "Active listening": "Agent asked for previous address at turn 42 despite customer providing it at turn 3.",
        "Took ownership of the problem": "Agent refused to process refund or escalate to manager, stating frontline staff cannot waive fees.",
        "Build rapport and observed professionalism": "Agent insulted customer at [04:15]: 'Well if you actually paid attention to your contract terms... you wouldn't be shocked by legitimate early termination fees.'",
        "Probing": "Agent asked relevant questions regarding statement invoice descriptions and dates.",
        "Confirmed the issue is resolved": "Customer noted dispute ticket TKT-88192-M and ombudsman complaint reference CMP-99021-G."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 41, "reworded": True}
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
            {"kind": "unhandled", "customer_turn": 20}
        ]
    }

    return {
        "cid": "agt_037",
        "cname": "George",
        "target_dur": 974,
        "scenario": "Erroneous £220 early termination fee charged after moving to non-serviceable rural area",
        "tier": "poor",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Build rapport and observed professionalism", "Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Poor customer service call featuring agent rudeness, deflection of ownership, failure of empathy regarding bank overdraft charges, and repeated questioning regarding previous address in the last third of the call."
    }

print("get_call_037 defined.")


# =========================================================================
# Call 038: Grace, Mobile dropping to No Service indoors; Wi-Fi Calling, 12:19 (739s)
# 3-4 faults (okay), score 71.7, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL
# =========================================================================
def get_call_038():
    raw = [
        ("Agent", "Thank you for calling S-Net mobile customer care, my name is Lewis. How can I help you today?", None),
        ("Customer", "Hello Lewis, my name is Grace Mitchell. My mobile phone has completely stopped getting any signal inside my home, dropping from 4G down to 'No Service' as soon as I walk through the front door!", -32.5),
        ("Agent", "Good afternoon Grace. I can check your regional mast coverage and cellular network provisioning. Before we access your handset profile, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 29 St Mary's Road, Southampton, SO14 0AH, and my security PIN is 3819. My handset model is a Samsung Galaxy S23 with mobile number 07700 900619.", -5.2),
        ("Agent", "Thank you Grace, that confirms your account details. When did the indoor signal drop to No Service begin?", None),
        ("Customer", "It started four days ago when local council roadworks began digging on the main avenue near our street.", -22.1),
        ("Agent", "Bear with me for a couple of minutes while I check our cell mast telemetry and base station alarms in the SO14 postal sector.", None),
        ("Agent", "Thank you for waiting, Grace. The local sector mast on St Mary's Road has an active power fault following council utility cable strikes, operating on emergency low power.", None),
        ("Customer", "I am a community NHS midwife on night triage call this entire week! Pregnant mothers in active labor phone my mobile number directly when emergencies happen! If my phone drops to No Service indoors, I could miss a critical maternity delivery call! It could literally be life-threatening! I am beside myself with anxiety!", -64.2),
        ("Agent", "Local cellular mast power repairs are managed by regional telecommunications grid engineers with an estimated fix time of seventy-two hours.", None),
        ("Customer", "Seventy-two hours is completely useless when I have babies due tonight, Lewis! What can be done right now on my phone so I can receive incoming hospital calls inside my house?!", -52.4),
        ("Agent", "You need to activate S-Net Wi-Fi Calling on your smartphone to route voice calls across your home broadband wireless router.", None),
        ("Customer", "How do I set that up on my Samsung Galaxy?", -18.2),
        ("Agent", "Obviously modern 5G handsets support seamless voice over Wi-Fi when cellular signal drops below minimum reception thresholds.", None),
        ("Customer", "Please just guide me through the settings menu so I know it is working.", -14.5),
        ("Agent", "Open the 'Phone' app on your Samsung, tap the three dots in the top right corner, and select 'Settings'.", None),
        ("Customer", "Tapped Phone, three dots, Settings. I see Call Settings.", 12.1),
        ("Agent", "Scroll down to 'Wi-Fi Calling' and switch the toggle from OFF to ON.", None),
        ("Customer", "Toggling Wi-Fi Calling to ON... It says 'Enabling Wi-Fi Calling service with S-Net...'", 18.5),
        ("Customer", "Lewis, I am trembling with panic right now! If an emergency triage labor call comes through and drops, I will never forgive myself! Please make sure this connects!", -58.2),
        ("Agent", "A small telephone receiver icon with a Wi-Fi wave should appear in your top status notification bar.", None),
        ("Customer", "Looking at the top bar... Yes! A little telephone handset icon with a Wi-Fi symbol just appeared next to the Wi-Fi fan!", 44.5),
        ("Agent", "Now let us set the Wi-Fi Calling preference to prioritize Wi-Fi whenever you are connected to your home network.", None),
        ("Customer", "Tapped on Wi-Fi Calling... I see 'Calling preference'. Selected 'Wi-Fi preferred'.", 28.4),
        ("Agent", "Now let us execute a test call right now to verify voice quality across your broadband router.", None),
        ("Customer", "I will dial my husband's phone in the living room... Ringing now... He picked up! Sound is crystal clear!", 68.2),
        ("Agent", "That confirms voice calls and SMS text messages are routing seamlessly over your home Wi-Fi network.", None),
        ("Customer", "What a massive relief! My NHS maternity labor calls will come straight through to my handset now.", 54.1),
        ("Agent", "Our automated network operations centre will send an SMS alert once the local cell mast repairs complete.", None),
        ("Customer", "That will be helpful so I know when standard outdoor cellular coverage is restored.", 22.1),
        ("Agent", "Wi-Fi Calling requires no additional subscription charges on your S-Net unlimited tariff.", None),
        ("Customer", "It is reassuring that all calls remain included in my standard allowance.", 26.4),
        ("Agent", "You can also verify that emergency 999 calling routes your registered home address over Wi-Fi Calling.", None),
        ("Customer", "That is vital for our home safety during the cellular outage.", 31.2),
        ("Agent", "The handset will automatically switch back to 5G cellular once you step outside your front door.", None),
        ("Customer", "That handover between Wi-Fi and mobile data will be very smooth.", 28.5),
        ("Agent", "Remember to keep your home Wi-Fi router powered on continuously overnight.", None),
        ("Customer", "I always leave the router switched on in the hallway.", 24.1),
        ("Agent", "The router's 5 gigahertz frequency band provides optimal voice latency for clear audio.", None),
        ("Customer", "The audio sounded completely natural when I spoke to my husband.", 32.1),
        # Turn 42 is Repeat in last third! 42/58 = 0.724 >= 0.66
        ("Agent", "What was that mobile handset model again?", None),
        ("Customer", "As I told you right at the start of the call, it is a Samsung Galaxy S23.", -16.2),
        ("Agent", "I have updated your device profile with the Samsung Galaxy S23 model code.", None),
        ("Customer", "Thank you, that ensures device compatibility is noted.", 18.5),
        ("Agent", "Before we conclude our call, that mobile phone number was 07700 900619, correct?", None),
        ("Customer", "Yes, 07700 900619.", 22.4),
        ("Agent", "We have identified the local mast outage, activated Wi-Fi Calling on your Samsung S23, verified incoming call routing, and confirmed voice clarity.", None),
        ("Customer", "Everything is working smoothly now. Thank you Lewis.", 36.5),
        ("Agent", "Is there any other aspect of your mobile plan or reception I can help you with today, Grace?", None),
        ("Customer", "No thank you Lewis, you have resolved my urgent issue.", 24.1),
        ("Agent", "Thank you for choosing S-Net mobile customer care, Grace. Have a safe and restful shift with your maternity patients. Goodbye.", None),
        ("Customer", "Goodbye Lewis.", 18.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our mobile core network provides priority packet queuing for all active Wi-Fi Calling sessions.", None))
        raw.insert(-4, ("Customer", "That priority queuing will ensure patient calls never buffer or distort.", 22.1))

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
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [03:20] and [06:40] when customer voiced extreme panic regarding NHS midwife labor triage calls.",
        "Paraphrasing": "Failed to paraphrase customer's indoor signal loss issue in own words.",
        "Active listening": "Asked customer at [08:50] for her handset model which had already been verified at [00:45]."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net mobile customer care' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Grace throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer voiced acute anxiety regarding on-call maternity labor emergencies; agent offered no empathy and recited technical protocols.",
        "Paraphrasing": "Agent never restated the indoor mobile signal problem in his own words.",
        "Active listening": "Agent asked for handset model at turn 42 despite customer stating Samsung Galaxy S23 at turn 3.",
        "Took ownership of the problem": "Agent guided customer step-by-step through Samsung settings to enable Wi-Fi Calling.",
        "Build rapport and observed professionalism": "Agent maintained a courteous instructional tone throughout.",
        "Probing": "Agent asked relevant questions regarding outage timing and indoor signal behavior.",
        "Confirmed the issue is resolved": "Customer confirmed Wi-Fi Calling icon active, set Wi-Fi preferred, and verified test call with husband."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 42, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 13}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 8},
            {"kind": "unhandled", "customer_turn": 19}
        ]
    }

    return {
        "cid": "agt_038",
        "cname": "Grace",
        "target_dur": 739,
        "scenario": "Mobile handset dropping from 4G to No Service indoors; Wi-Fi Calling setup required",
        "tier": "okay",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Paraphrasing"],
        "notes": "Good technical walk-through of Samsung Wi-Fi Calling setup during a local mast outage, but agent failed empathy regarding on-call NHS midwife labor emergencies, offered no paraphrase, and repeated a question about handset model in the last third of the call."
    }

print("get_call_038 defined.")


# =========================================================================
# Call 039: Hamza, Streaming bundle token link expired, 16:52 (1012s)
# 5+ faults (poor), score 48.3, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL
# =========================================================================
def get_call_039():
    raw = [
        ("Agent", "Thank you for calling S-Net entertainment customer services, my name is Bradley. How can I help you today?", None),
        ("Customer", "Hello Bradley, my name is Hamza Malik. I added the premium entertainment streaming bundle with Netflix and Disney Plus to my broadband package two weeks ago, but the activation link email expired and every time I click it an error page says 'Token Expired - Contact Provider'!", -34.5),
        ("Agent", "Good afternoon Hamza. I can check your entertainment subscription status. Before we inspect your streaming entitlements, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 63 Victoria Road, Swindon, SN1 3BD, and my security PIN is 9510. My registered S-Net email address is hamza.malik99@gmail.com.", -5.4),
        ("Agent", "Thank you Hamza, that confirms your account details. What happens when you navigate to the URL provided in the original onboarding email?", None),
        ("Customer", "A red banner appears across the screen stating 'Security activation token expired after seven days. Please contact your broadband operator to request a fresh authentication link.'", -24.2),
        ("Agent", "Bear with me for a couple of minutes while I check your digital entertainment order ledger on our third-party partner portal.", None),
        ("Agent", "Thank you for waiting, Hamza. The third-party entertainment portal shows token status 'Expired' because the email link was not redeemed within seven calendar days of order creation.", None),
        ("Customer", "I was in hospital having emergency surgery for a perforated appendix for the past ten days! I wasn't checking promotional emails while in a hospital surgical ward! And you have already charged me eighteen pounds on this month's bill for Netflix and Disney Plus that I cannot even watch! I am furious and stressed out!", -64.2),
        ("Agent", "Digital entertainment activation tokens are governed by automated third-party platform licensing windows.", None),
        ("Customer", "Can you generate a fresh activation token link and email it to me right now?", -28.4),
        ("Agent", "Obviously we are an internet service provider, not Netflix or Disney Plus customer care, so stop expecting frontline broadband agents to manage third-party streaming accounts.", None),
        ("Customer", "I pay eighteen pounds a month to S-Net on my broadband bill for this bundle, Bradley! S-Net sold me the subscription, so S-Net is responsible for activating it!", -58.4),
        ("Agent", "Frontline telephony representatives do not have access to regenerate third-party vendor encryption tokens.", None),
        ("Customer", "Then transfer me to your supervisor or partner relations desk who can re-issue the token!", -44.2),
        ("Agent", "Partner relations do not take customer phone calls. You need to contact Netflix directly via their web live chat to request account linking.", None),
        ("Customer", "Netflix told me earlier today that only S-Net can re-issue the partner activation link! You are passing the buck and refusing to take responsibility!", -48.5),
        ("Agent", "I am stating our internal operational system capabilities.", None),
        ("Customer", "You charged me eighteen pounds, you won't provide the service, you won't generate a link, and you won't let me speak to a manager! This is utterly atrocious service!", -52.4),
        ("Agent", "Obviously automated recurring subscription billing runs in accordance with contract commencement dates regardless of activation status.", None),
        ("Customer", "I am recovering from major surgery and this stress is making my blood pressure skyrocket! I demand you cancel this bundle and refund my eighteen pounds immediately!", -62.4),
        ("Agent", "I can submit an administrative token regeneration ticket to our offline billing operations queue, which has an SLA of three to five business days to re-issue the vendor activation token.", None),
        ("Customer", "And what about the eighteen pounds you charged me while the link was broken?", -24.2),
        ("Agent", "Discretionary billing credits must be reviewed by the offline operations team after token redemption.", None),
        ("Customer", "Give me the reference number for this ticket.", -12.4),
        ("Agent", "The ticket reference identifier is ENT-88192-H.", None),
        ("Customer", "ENT-88192-H, noted down.", 4.5),
        ("Agent", "The fresh activation link will be dispatched directly to your Gmail address once processed.", None),
        ("Customer", "I will watch my inbox closely.", 8.2),
        ("Agent", "Your broadband connection will maintain priority streaming traffic flags once the entertainment account links.", None),
        ("Customer", "I hope so, because paying eighteen pounds for nothing has been a terrible experience.", -8.2),
        ("Agent", "Our streaming bundle terms include 4K UHD streaming access across four household screens simultaneously.", None),
        ("Customer", "That will be good once it actually functions.", 4.2),
        ("Agent", "You can link your existing Netflix profile history to retain viewing recommendations.", None),
        ("Customer", "My family will appreciate keeping our existing profiles.", 12.1),
        ("Agent", "The Disney Plus bundle includes all Star, Marvel, and National Geographic catalogs.", None),
        ("Customer", "The children are eager to watch the new animated releases.", 14.5),
        ("Agent", "Our partner billing platform processes token synchronization sweeps twice daily.", None),
        ("Customer", "Hopefully that speeds up the token re-issuance.", 18.2),
        # Turn 42 is Repeat in last third! 42/58 = 0.724 >= 0.66
        ("Agent", "What is that S-Net registered email address again?", None),
        ("Customer", "As I told you right at the start of the call, it is hamza.malik99@gmail.com.", -16.4),
        ("Agent", "I have verified hamza.malik99@gmail.com as the dispatch target on ticket ENT-88192-H.", None),
        ("Customer", "Thank you, please ensure the email is sent without delay.", 14.1),
        ("Agent", "Is there any other aspect of your broadband account I can help you with today, Hamza?", None),
        ("Customer", "No, you have been unhelpful and defensive.", -12.1),
        ("Agent", "Thank you for choosing S-Net entertainment customer services, Hamza. Goodbye.", None),
        ("Customer", "Goodbye Bradley.", -6.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our partner support team coordinates directly with third-party streaming content networks.", None))
        raw.insert(-4, ("Customer", "I expect S-Net to take full accountability for partner integrations.", 8.2))

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
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [03:15] and [07:40] when customer voiced acute distress following emergency surgery for a perforated appendix.",
        "Paraphrasing": "Failed to paraphrase customer's streaming token expiration dispute in own words.",
        "Active listening": "Asked customer at [10:10] for his email address which had already been verified at [00:45].",
        "Took ownership of the problem": "Deflected responsibility at [05:20] by telling customer to contact Netflix directly rather than owning the bundle issue.",
        "Build rapport and observed professionalism": "Spoke rudely and aggressively at [04:15] stating 'Obviously we are an internet service provider... so stop expecting frontline broadband agents to manage third-party streaming accounts.'"
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net entertainment customer services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Hamza throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute distress and surgery recovery vulnerability; agent offered zero empathy and blamed licensing windows.",
        "Paraphrasing": "Agent never restated the token expiration dispute in his own words.",
        "Active listening": "Agent asked for email address at turn 42 despite customer providing hamza.malik99@gmail.com at turn 3.",
        "Took ownership of the problem": "Agent repeatedly deflected ownership telling customer to contact Netflix directly.",
        "Build rapport and observed professionalism": "Agent insulted customer at [04:15]: 'Obviously we are an internet service provider... so stop expecting frontline broadband agents to manage third-party streaming accounts.'",
        "Probing": "Agent asked relevant questions regarding activation error screens and dates.",
        "Confirmed the issue is resolved": "Customer noted ticket reference ENT-88192-H and accepted offline token re-issuance queue."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 39, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "rude", "agent_turn": 11},
            {"kind": "blunt_but_ok", "agent_turn": 19}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 8},
            {"kind": "unhandled", "customer_turn": 20}
        ]
    }

    return {
        "cid": "agt_039",
        "cname": "Hamza",
        "target_dur": 1012,
        "scenario": "Streaming entertainment bundle (Netflix/Disney+) token link expired before account linking",
        "tier": "poor",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Build rapport and observed professionalism", "Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Poor customer service call featuring agent rudeness, deflection of ownership to third parties, failure of empathy following customer's emergency surgery, and repeated questioning regarding email address in the last third of the call."
    }

print("get_call_039 defined.")


# =========================================================================
# Call 040: Hannah, Broadband throttling down to 15 Mbps on Fibre 900, 19:47 (1187s)
# 1-2 faults (good), score 88.3, Empathy FAIL (1 handled with refusal, 1 unhandled)
# =========================================================================
def get_call_040():
    raw = [
        ("Agent", "Thank you for calling S-Net high-speed broadband technical operations, my name is Edward. How can I help you today?", None),
        ("Customer", "Hello Edward, my name is Hannah Morris. I am paying seventy pounds a month for your top-tier Fibre 900 package, but every single evening between eight and eleven o'clock my download speed throttles down to fifteen megabits per second!", -34.8),
        ("Agent", "Good afternoon Hannah. I can inspect your optical gigabit profile and regional distribution gateway telemetry. Before we examine your speed telemetry, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 42 Lansdown Crescent, Bath, BA1 5EX, and my security PIN is 6194. My optical ONT unit serial number is SNET-ONT-88419.", -5.2),
        ("Agent", "Thank you Hannah, that confirms your account details. How are your devices connected to the Hub 5 router during these evening slowdowns?", None),
        ("Customer", "I have an Apple TV 4K connected directly via a Cat 6 Ethernet cable, and three laptops connected via five gigahertz Wi-Fi in the same room.", -16.4),
        ("Agent", "So what has occurred is that while your Fibre 900 subscription delivers gigabit throughput during daytime hours, severe congestion or traffic management reduces your speeds to fifteen megabits during peak evening hours between eight and eleven, is that right?", None),
        ("Customer", "Yes, that is exactly what happens every single night! My family cannot stream 4K movies or play games, and everything buffers continuously!", -24.2),
        ("Agent", "Bear with me for a couple of minutes while I query our core optical line terminal and regional BGP aggregation routers in the Bath exchange.", None),
        ("Agent", "Thank you for waiting, Hannah. The OLT telemetry indicates your physical GPON optical light budget is pristine at minus nineteen dBm, but our regional aggregation edge router is experiencing high capacity utilization during peak streaming hours.", None),
        ("Customer", "I am sick and tired of paying seventy pounds a month for gigabit speeds that turn into dial-up speeds every night! I demand an immediate penalty-free contract exit and a full refund of all broadband fees paid for the past six months right now!", -64.2),
        ("Agent", "I completely understand how deeply disappointing and frustrating it is to experience evening speed degradation when relaxing with family 4K streaming, Hannah. However, because our diagnostic records show your physical connection syncs at full gigabit capacity and the slowdown stems from regional transit node congestion, our service terms require opening an engineering capacity ticket rather than immediate penalty-free termination or full retrospective refunds; what I can do right now is apply an immediate twenty-pound goodwill credit to your bill, re-route your WAN session to our low-latency London peering node, and book a priority node upgrade ticket.", None),
        ("Customer", "Well... at least you acknowledged the problem honestly instead of blaming my home Wi-Fi like the last agent did. Twenty pounds credit and re-routing the session is a fair temporary compromise while you fix the node.", 18.4),
        ("Agent", "I have applied the twenty-pound goodwill credit adjustment directly to your account ledger right now.", None),
        ("Customer", "Thank you Edward. How do we execute the WAN session re-routing?", 22.1),
        ("Agent", "I am sending a remote session termination command to the local broadband remote access server.", None),
        ("Customer", "The internet light on the Hub 5 router just went amber for a moment.", 14.5),
        ("Agent", "Yes, that forces your router to re-negotiate a dynamic IP lease on our alternative low-congestion peering ring.", None),
        ("Customer", "The light is back to solid white. Let me run a speed test on my Ethernet Apple TV...", 28.4),
        ("Agent", "What speed result does the Apple TV speed test application report right now, Hannah?", None),
        ("Customer", "It is showing four hundred and eighty megabits per second! That is thirty times faster than fifteen megabits!", 54.2),
        ("Agent", "That confirms your traffic is successfully traversing our London secondary aggregation core.", None),
        ("Customer", "That is a massive improvement for tonight.", 42.1),
        ("Agent", "Obviously regional bandwidth capacity upgrades require physical line card installation in the telephone exchange.", None),
        ("Customer", "When will the permanent line card upgrade in the Bath exchange actually be completed?", 16.4),
        ("Agent", "Our core network engineering department has scheduled the Bath optical node backhaul expansion for completion within fourteen business days, installing two fresh 100-gigabit DWDM uplink transceivers.", None),
        ("Customer", "That extra backhaul capacity will permanently solve the evening peak bottleneck.", 24.1),
        ("Agent", "I have attached your account to automated monitoring ticket NET-44019-B.", None),
        ("Customer", "What does that automated monitoring ticket do?", 8.5),
        ("Agent", "It will poll your evening speed tests automatically every thirty minutes and trigger an SMS alert if speeds drop below two hundred megabits.", None),
        ("Customer", "That will keep S-Net accountable for maintaining throughput.", 22.1),
        ("Agent", "You can track the Bath exchange engineering progress via your My S-Net mobile app under Network Status.", None),
        ("Customer", "I will keep an eye on the network status page.", 22.1),
        ("Agent", "Your Hub 5 router features Wi-Fi 6 technology with multi-user MIMO capabilities.", None),
        ("Customer", "Yes, all our laptops connect with high wireless link speeds.", 24.5),
        ("Agent", "Our gigabit fiber infrastructure supports ultra-low latency ideal for cloud gaming.", None),
        ("Customer", "The ping times have been under ten milliseconds when speeds are fast.", 28.2),
        ("Agent", "We also recommend enabling Smart Wi-Fi band steering to optimize device frequency allocation.", None),
        ("Customer", "I will ensure band steering remains active on all our mobile handsets.", 22.1),
        ("Agent", "The router will intelligently assign five gigahertz channels to eliminate domestic wireless contention.", None),
        # Turn 40 is second outburst in last third!
        ("Customer", "Edward, fourteen business days is nearly three more weeks of potential evening buffering! I can't believe S-Net sells gigabit packages when your exchange hardware is oversubscribed! It makes me furious to have to wait three weeks for hardware you should have installed months ago!", -58.4),
        ("Agent", "Exchange equipment upgrades are managed according to scheduled engineering maintenance windows.", None),
        ("Customer", "I hope your engineering team adheres strictly to that fourteen-day deadline.", -18.2),
        ("Agent", "Our engineering field supervision team oversees all overnight exchange maintenance cutovers.", None),
        ("Customer", "That gives me confidence the work will actually complete on schedule.", 14.2),
        # Turn 46 is Harmless Recheck in last third! 46/58 = 0.793 >= 0.66
        ("Agent", "Before we conclude our call, that account contact telephone number was 01225 440192, correct?", None),
        ("Customer", "Yes, 01225 440192 is my home landline.", 18.2),
        ("Agent", "We have applied the twenty-pound credit, re-routed your WAN session to the London peering ring, verified 480 Mbps throughput, and logged engineering ticket NET-44019-B.", None),
        ("Customer", "Thank you Edward, the speed is vastly better tonight.", 32.4),
        ("Agent", "Is there any other aspect of your gigabit broadband service I can assist you with today, Hannah?", None),
        ("Customer", "No thank you Edward, you have done what you could for now.", 26.5),
        ("Agent", "Thank you for choosing S-Net high-speed broadband technical operations, Hannah. Have a wonderful evening. Goodbye.", None),
        ("Customer", "Goodbye Edward.", 18.4),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our automated network management systems will monitor line jitter continuously.", None))
        raw.insert(-4, ("Customer", "That continuous monitoring will ensure packet loss remains at zero percent.", 22.4))

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
        "Empathy & Acknowledgment Statement": "While agent handled the initial outburst with empathy and refusal, he completely ignored the customer's severe frustration at [08:20] when informed of a 14-day exchange upgrade wait."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net high-speed broadband technical operations' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Hannah throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated acknowledgment-then-refusal at [03:20] ('I completely understand how deeply disappointing and frustrating... However, because our diagnostic records show... our service terms require opening an engineering capacity ticket rather than immediate penalty-free termination...'), but completely ignored customer's subsequent outburst at [08:20] regarding 14-day hardware delays.",
        "Paraphrasing": "Agent restated the evening throttling and buffering problem accurately at [01:25].",
        "Active listening": "Agent confirmed landline number accurately without repeating questions.",
        "Took ownership of the problem": "Agent applied £20 credit, rerouted WAN session, and opened automated monitoring ticket NET-44019-B.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, constructive, and honest tone throughout.",
        "Probing": "Agent asked targeted diagnostic questions regarding connection types and device behavior.",
        "Confirmed the issue is resolved": "Customer confirmed download speed increased to 480 Mbps following WAN reroute and accepted engineering timeline."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 45}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 6},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 23}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 10, "agent_turn": 11, "with_refusal": True},
            {"kind": "unhandled", "customer_turn": 40}
        ]
    }

    return {
        "cid": "agt_040",
        "cname": "Hannah",
        "target_dur": 1187,
        "scenario": "Broadband throttling down to 15 Mbps on Fibre 900 package during peak hours",
        "tier": "good",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Excellent demonstration of acknowledgment-then-refusal followed by a second unhandled outburst regarding engineering upgrade timeframes in the last third of the call, properly classified as an Empathy FAIL rating."
    }

print("get_call_040 defined.")

if __name__ == "__main__":
    for fn in [get_call_036, get_call_037, get_call_038, get_call_039, get_call_040]:
        c = fn()
        compile_call(c)
