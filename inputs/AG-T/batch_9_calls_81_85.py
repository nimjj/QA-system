import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from batch_engine import compile_call

# =========================================================================
# Call 081: Sabrina, Dispute over £50 engineer callout fee charged for external line fault, 11:45 (705s)
# 1-2 faults (good), score 83.3, Active listening FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_081():
    raw = [
        ("Agent", "Thank you for calling S-Net customer billing resolutions, my name is Fiona. How can I help you today?", None),
        ("Customer", "Hello Fiona, my name is Sabrina Clark. My October broadband bill includes a fifty-pound engineer callout fee, but when the Openreach engineer attended two weeks ago, he confirmed in writing that the fault was water ingress inside the street footway joint box, which is external network infrastructure and explicitly free of charge!", -34.8),
        ("Agent", "Good afternoon Sabrina. If I understand correctly, your October statement includes a fifty-pound engineer callout charge despite the engineer confirming the fault was external water ingress in a street joint box. Before we inspect your engineering ledger, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 12 Victoria Parade, Harrogate, HG1 5AA, security PIN 4491, customer account BB-991204.", -5.2),
        ("Agent", "Thank you Sabrina, that confirms your account details. What date was the engineer visit completed?", None),
        ("Customer", "The technician attended on September 28th between nine and eleven in the morning.", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query the Openreach contractor closure code and billing notes?", None),
        ("Agent", "Thank you for holding, Sabrina. The engineering closure report confirms that the technician logged closure code EXT-JOINT-WTR, which designates external street infrastructure water damage.", None),
        ("Customer", "So why did your billing system charge me fifty pounds if the code proves it was an external street fault?", -18.2),
        ("Agent", "When the automated invoice generated, the billing system incorrectly mapped the job to code MISC-CHARGE-50 due to a clerical typo by the contractor dispatcher.", None),
        ("Customer", "Can you reverse the fifty-pound fee and remove it from my direct debit today?", -8.4),
        ("Agent", "I can submit a formal billing dispute credit request for fifty pounds to our finance team.", None),
        ("Customer", "Why does an obvious clerical typo require a dispute request instead of an immediate refund?", -18.2),
        ("Agent", "Charges over thirty pounds that have already locked into automated Bacs direct debit cycles require supervisor audit approval.", None),
        ("Customer", "How long will it take for the supervisor to approve the fifty-pound credit?", -12.4),
        ("Agent", "Supervisor billing audits take between three and five business days to clear.", None),
        ("Customer", "Will the fifty pounds still be debited from my account on Friday?", -24.2),
        ("Agent", "Because Friday's direct debit file has already transmitted to the clearing house, the full payment will be drawn and the fifty pounds will be returned as an immediate bank credit upon approval.", None),
        ("Customer", "I see. As long as the fifty pounds is definitely returned to my account.", -8.2),
        ("Agent", "Obviously automated direct debit clearing batches cannot be modified once transmitted to Bacs.", None),
        ("Customer", "Right, I understand the banking transmission cutoff.", 6.2),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Sabrina speaking, I took a half-day unpaid off work to wait for that engineer, I sat in a freezing house for three hours, and then your company slaps a fifty-pound penalty on my bill for a flooded street junction! It feels like S-Net tries to charge customers for Openreach's rotting infrastructure and hopes we won't notice! It is infuriating and completely unfair!", -64.8),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand how unfair and infuriating that feels, Sabrina, especially after losing half a day's wages from work and sitting in the cold waiting for the repair. You should never have been charged fifty pounds for external street maintenance, and I will personally track this refund until every penny is safely returned to your bank account.", None),
        ("Customer", "Thank you Fiona, I appreciate your honesty and reassurance.", -4.2),
        ("Agent", "I have logged the fifty-pound credit under finance reference CR-88192-S.", None),
        ("Customer", "CR-88192-S, noted down.", 4.2),
        ("Agent", "I have also attached a digital copy of the engineer's handwritten job sheet stating external water ingress to the audit file.", None),
        ("Customer", "That will make the approval completely open and shut.", 12.2),
        ("Agent", "I am adding an alert to my personal diary to follow up with the finance supervisor on Monday morning.", None),
        ("Customer", "Thank you, that gives me great confidence it won't be forgotten.", 18.4),
        ("Agent", "Once approved, the fifty-pound credit will transfer directly back into your Santander account.", None),
        ("Customer", "Will I receive an email confirmation once the supervisor signs off?", 22.4),
        ("Agent", "Yes, an automated remittance advice email will be dispatched to your registered address.", None),
        ("Customer", "Excellent. And there are no other unexpected charges on the account?", 24.5),
        ("Agent", "Your recurring monthly subscription remains fixed at thirty-five pounds per month with zero additional fees.", None),
        ("Customer", "That matches our original contract agreement.", 26.2),
        ("Agent", "I have also applied a five-pound courtesy credit to your account for the billing inconvenience.", None),
        ("Customer", "Thank you Fiona, that is very generous of you.", 28.4),
        ("Agent", "Our priority is ensuring that contractor billing errors are corrected transparently.", None),
        ("Customer", "You have handled this call with great professionalism.", 30.2),
        ("Agent", "Thank you Sabrina, I am glad I could assist in rectifying the charge.", None),
        ("Customer", "So the credit is logged, and I will wait for Monday's update.", 24.5),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before we conclude, what was that customer account reference again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you at the start of our call, it is BB-991204.", -10.2),
        ("Agent", "Thank you Sabrina, the account reference is permanently linked to the refund request.", None),
        ("Customer", "Thank you for all your help today, Fiona.", 26.4),
        ("Agent", "It has been my pleasure assisting you, Sabrina. Have a wonderful weekend.", None),
        ("Customer", "Have a lovely weekend too. Goodbye.", 24.2),
        ("Agent", "Is there any other billing query I can assist you with today?", None),
        ("Customer", "No Fiona, that covers everything.", 20.0),
        ("Agent", "Thank you for calling S-Net customer billing resolutions, Sabrina. Goodbye.", None),
        ("Customer", "Goodbye Fiona.", 18.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 14.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 10.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 6.0)
    ]

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "PASS",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "PASS",
        "Active listening": "FAIL",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Active listening": "Asked customer at turn 42 for account reference which was already provided at turn 3.",
        "Confirmed the issue is resolved": "Failed to confirm refund credit resolution on call due to 3-5 day supervisor audit approval process."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net customer billing resolutions' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Sabrina throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand how unfair and infuriating that feels, Sabrina...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased the £50 callout dispute at turn 2.",
        "Active listening": "Agent asked for account reference at turn 42 despite customer stating BB-991204 at turn 3.",
        "Took ownership of the problem": "Agent attached engineer notes, submitted credit request, set follow-up diary alert, and applied courtesy credit.",
        "Build rapport and observed professionalism": "Agent maintained polite, supportive, and professional demeanor throughout.",
        "Probing": "Agent gathered details on engineer dates and closure codes.",
        "Confirmed the issue is resolved": "Credit required 3-5 business days for supervisor audit approval and could not be verified on call."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 42, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 2},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 19}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 21, "agent_turn": 22, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_081",
        "cname": "Sabrina",
        "target_dur": 705,
        "scenario": "Billing dispute over £50 engineer callout fee charged for external line fault; credit logged but audit approval pending",
        "tier": "good",
        "expected_score": 83.3,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Confirmed the issue is resolved"],
        "notes": "Good call where agent was courteous, empathetic, and resolved billing dispute, failing active listening repeat and confirmed resolved due to supervisor signoff window."
    }

print("get_call_081 defined.")

# =========================================================================
# Call 082: Samira, Mobile VoLTE calls dropping immediately upon Wi-Fi to cellular handover, 14:27 (867s)
# 5+ faults (poor), score 35.0, Dead Air FAIL, Verified FAIL, Personalized FAIL, Probing FAIL, Rapport FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_082():
    raw = [
        ("Agent", "Thank you for calling S-Net mobile technical faults, my name is Marcus. How can I help you today?", None),
        ("Customer", "Hello, my name is Samira Khan. Every single time I leave our house while on an active mobile phone call, the voice call cuts off abruptly the exact second my handset disconnects from our home Wi-Fi and attempts to hand over to 4G VoLTE, dropping critical client calls every morning!", -34.8),
        # Verified FAIL: Agent never asks for PIN, address, or security question in the first 240s!
        # Personalized FAIL: Agent never uses customer name 'Samira' anywhere in call!
        ("Agent", "I can inspect your cellular network registration logs. What mobile phone number is experiencing call handover drops?", None),
        ("Customer", "It is 07700 900891, registered to 42 Lansdown Road, Cheltenham, GL51 6QJ, security PIN 7712.", -5.2),
        # Probing FAIL: Agent asks superficial question, failing to probe effectively
        ("Agent", "Does the phone drop calls when you are sitting completely still inside your living room?", None),
        ("Customer", "No, as I just explained, it happens specifically when walking out the front door as Wi-Fi disconnects and switches to cellular!", -18.2),
        ("Agent", "Could I place you on hold for two minutes while I query the mobile IMS core routing logs?", None),
        ("Agent", "Thank you for holding. The network logs show an IMS Session Initiation Protocol timeout during ePDG to eNodeB voice bearer handover.", None),
        ("Customer", "Why is the SIP protocol timing out when handing over the voice call?", -14.2),
        ("Agent", "Handover latency exceeds standard threshold timers when local cell towers operate with low radio signal-to-noise ratios.", None),
        ("Customer", "Can you update our cellular provisioning profile to eliminate the handover delay?", -6.4),
        ("Agent", "If you insist on making phone calls while walking through metal-reinforced front porches that shield radio signals, your call is obviously going to drop.", None),
        ("Customer", "Our porch is made of standard glass and wood! There is no metal shielding! Why are you inventing excuses instead of fixing the handover?", -52.4),
        ("Agent", "I am stating the physics of cellular radio propagation through structural building materials.", None),
        ("Customer", "Can you re-provision the VoLTE profile on my SIM card right now?", -34.2),
        # Turn 14 is dead air gap 1 (40s)
        ("Agent", "VoLTE provisioning updates can be submitted through our radio management gateway.", None),
        ("Customer", "Hello? Are you still on the phone? The line went completely silent for over thirty seconds!", -28.4),
        ("Agent", "I was accessing the regional Cheltenham eNodeB cellular mast configuration.", None),
        ("Customer", "Please send that VoLTE profile refresh immediately.", -18.2),
        ("Agent", "Obviously Voice over LTE handover requires seamless cryptographic re-keying between Wi-Fi security gateways and cellular towers.", None),
        ("Customer", "I know it requires re-keying; that is why I am calling technical support!", -24.2),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "I am an independent corporate tax attorney, and my call dropped this morning while advising a client on a multi-million-pound merger! The client thought I hung up on them in frustration, the deal was put on hold, and my professional credibility was shredded! Paying sixty pounds a month for a phone that cannot walk out of a front door without dropping calls is disgraceful and terrifying! I am shaking with stress!", -68.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand the immense professional anxiety, stress, and reputational risk this has caused you with your tax client, especially during multi-million-pound merger negotiations. Having calls drop abruptly when walking out your front door is completely unacceptable, and I will force an immediate IMS voice profile reconfiguration right now.", None),
        ("Customer", "Thank you, please push that reconfiguration right away.", -12.2),
        ("Agent", "I am transmitting the IMS VoLTE bearer refresh packet to your SIM card.", None),
        ("Customer", "The phone signal bars dropped to zero... and now '4G VoLTE' has reappeared.", 8.4),
        ("Agent", "The new VoLTE handover profile has been provisioned on the HLR.", None),
        ("Customer", "Can we test walking out the front door right now while on this call to verify that the handover works?", 12.2),
        ("Agent", "Because our incoming support line operates across fixed PSTN interconnects, testing a live Wi-Fi to cellular handover will terminate our current active diagnostic call.", None),
        ("Customer", "So we cannot verify while on this call whether the handover problem is actually fixed?", -18.2),
        ("Agent", "Correct, you must test placing a test call to an external party after we conclude this diagnostic session.", None),
        ("Customer", "I see. So I will have to test it on my own with a friend later.", -12.4),
        ("Agent", "I have logged the VoLTE profile update under ticket reference MOB-VOLTE-88192-K.", None),
        ("Customer", "MOB-VOLTE-88192-K, noted down.", -4.2),
        # Turn 34 is dead air gap 2 (40s)
        ("Customer", "Hello? Marcus? Did the line drop again? Why is there total silence on your end?", -24.2),
        ("Agent", "I am here. I was committing the handover profile parameters to the Cheltenham mast controller.", None),
        ("Customer", "I hope that mast update actually solves the drops.", -8.2),
        ("Agent", "If drops persist, you can toggle 'Wi-Fi Calling' to OFF in your iPhone settings to force all calls onto cellular.", None),
        ("Customer", "Turning off Wi-Fi Calling defeats the purpose of having Wi-Fi calling in our house.", -14.2),
        ("Agent", "That is an alternative operational setting.", None),
        ("Customer", "I will test walking outside after this call.", -6.2),
        ("Agent", "I have added a monitoring flag to your cellular line profile.", None),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before we conclude, what was that mobile telephone number again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you at the start of our call, it is 07700 900891.", -12.4),
        ("Agent", "Thank you, the mobile number is confirmed on the ticket.", None),
        ("Customer", "I will place a test call to my colleague now.", -4.2),
        ("Agent", "I have also applied a five-pound goodwill credit to your mobile account.", None),
        ("Customer", "Thank you for the credit.", 2.4),
        ("Agent", "Is there any other mobile query I can assist with today?", None),
        ("Customer", "No, goodbye.", 0.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -2.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -4.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -6.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -8.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -10.0)
    ]

    ratings = {
        "Branding and Survey Check": "FAIL",
        "Hold time and Dead Air": "FAIL",
        "Verified customer": "FAIL",
        "Personalized the call/ticket appropriately": "FAIL",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "PASS",
        "Active listening": "FAIL",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "FAIL",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Branding and Survey Check": "Failed standard closing branding script.",
        "Hold time and Dead Air": "Dead Air Breach: Agent had 2 occurrences of >30s unmanaged dead air.",
        "Verified customer": "Agent failed to ask for a PIN, address, or security question within the first 4 minutes of the call.",
        "Personalized the call/ticket appropriately": "Agent failed to use the customer's verified name 'Samira' during the call.",
        "Active listening": "Asked customer at turn 42 for her mobile number which was already provided at turn 3.",
        "Build rapport and observed professionalism": "Spoke rudely at turn 11 blaming customer for walking through metal-reinforced porches.",
        "Probing": "Failed to probe effectively regarding handset model or operating system version.",
        "Confirmed the issue is resolved": "Failed to confirm VoLTE handover resolution on call, advising customer to test independently later."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net mobile technical faults' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Agent allowed two separate unmanaged dead air gaps of 40 seconds at turns 14 and 34.",
        "Verified customer": "Agent failed to ask for address or security PIN during verification.",
        "Personalized the call/ticket appropriately": "Agent never addressed customer as Samira anywhere in the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand the immense professional anxiety, stress, and reputational risk this has caused you...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased the VoLTE handover drop issue at turn 2.",
        "Active listening": "Agent asked for mobile number at turn 42 despite customer stating 07700 900891 at turn 3.",
        "Took ownership of the problem": "Agent refreshed VoLTE profile, applied monitoring flag, and credited account.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you insist on making phone calls while walking through metal-reinforced front porches that shield radio signals, your call is obviously going to drop.'",
        "Probing": "Agent asked a superficial question about sitting still rather than probing device settings.",
        "Confirmed the issue is resolved": "Customer was advised that testing handover would drop support call, leaving issue unverified on call."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 42, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 2},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "rude", "agent_turn": 11},
            {"kind": "blunt_but_ok", "agent_turn": 19}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 21, "agent_turn": 22, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_082",
        "cname": "Samira",
        "target_dur": 867,
        "scenario": "Mobile VoLTE calls dropping immediately upon handover from Wi-Fi to cellular; 6 faults (poor)",
        "tier": "poor",
        "expected_score": 35.0,
        "dead_air_indices": [14, 33],
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Build rapport and observed professionalism", "Confirmed the issue is resolved", "Verified customer", "Personalized the call/ticket appropriately", "Probing"],
        "notes": "Poor call marked by dead air breaches, failed verification, failed personalization, failed probing, rude remarks, and unverified resolution, alongside handled empathy."
    }

print("get_call_082 defined.")

# =========================================================================
# Call 083: Sean, TV box remote control unresponsive with rapid flashing red LED, 15:18 (918s)
# 3-4 faults (okay), score 66.7, Dead Air FAIL, Verified FAIL, Rapport FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_083():
    raw = [
        ("Agent", "Thank you for calling S-Net TV technical support, my name is Brian. How can I help you today?", None),
        ("Customer", "Hello, my name is Sean Connolly. The remote control for our S-Net TV box has stopped responding completely: whenever I press any button on the remote, the little power LED flashes red rapidly five times and nothing happens on the television screen, leaving us completely unable to change channels or adjust volume!", -34.8),
        # Verified FAIL: Agent fails to ask for PIN, address, or security question in the first 240s!
        ("Agent", "If I understand correctly, your S-Net TV set-top box remote has stopped responding completely and only flashes its red power LED rapidly five times whenever any button is pressed. What is your TV box serial number and registered account number?", None),
        ("Customer", "The box serial is SN-TV-449102, customer account SN-991204, registered to 18 Parkside Avenue, Leeds, LS6 2EH, security PIN 5520.", -5.2),
        ("Agent", "Thank you Sean, that brings up your TV equipment record. Have you tried replacing the two AAA alkaline batteries in the back of the remote control?", None),
        ("Customer", "I inserted two brand new Duracell batteries straight from the packet, and the red LED still flashes rapidly whenever a button is pressed!", -22.4),
        ("Agent", "Could I place you on hold for two minutes while I query the Bluetooth Low Energy pairing registers on your set-top box?", None),
        ("Agent", "Thank you for holding, Sean. The set-top box Bluetooth receiver indicates that the cryptographic pairing key for the voice remote has desynchronized.", None),
        ("Customer", "How do we re-synchronize the Bluetooth pairing between the remote and the TV box?", -14.2),
        ("Agent", "There is a manual hardware re-pairing sequence: you must hold down the 'TV' and 'Rewind' buttons simultaneously for ten seconds.", None),
        ("Customer", "Let me try that right now: holding down 'TV' and 'Rewind'... nothing is happening; the red LED just flashes five times and stops.", -24.2),
        ("Agent", "If you drop your remote control onto hard tiled floors or spill sugary tea into the keypad membrane, the printed circuit board traces short out.", None),
        ("Customer", "No one dropped the remote or spilled tea on it! It sits on a soft sofa cushion! Why are you accusing us of damaging equipment that broke on its own?", -52.4),
        ("Agent", "I am explaining the standard mechanical causes of Bluetooth tactile switch failure.", None),
        ("Customer", "Can you dispatch a replacement remote control today?", -34.2),
        # Turn 14 is dead air gap 1 (40s)
        ("Agent", "Remote control replacements can be requested through our hardware warehouse.", None),
        ("Customer", "Brian? Are you still there? The phone line went dead for over thirty seconds!", -28.4),
        ("Agent", "I was accessing our peripheral dispatch inventory system.", None),
        ("Customer", "Will you dispatch a replacement remote today?", -18.2),
        ("Agent", "Obviously Bluetooth smart remotes require functional microcontrollers to transmit encrypted voice and navigation commands.", None),
        ("Customer", "I know it requires a working remote! That is why I am asking for a replacement!", -24.2),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Sean speaking, my mother is bedridden with terminal cancer in our front room and watching her nature documentaries on the television is the only comfort and distraction she has from her constant pain! Because your remote control died, she is trapped staring at a frozen menu screen and crying with frustration! Seeing my dying mother distressed over a broken piece of plastic is breaking my heart! I am desperate for your help!", -68.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand the profound heartbreak and emotional distress this is causing you, Sean, especially with your mother facing terminal illness and relying on television documentaries for comfort and pain relief. Leaving her unable to watch her programs is completely unacceptable, and I will dispatch an emergency replacement remote and set up a mobile remote app for her right now.", None),
        ("Customer", "What mobile remote app can we use right now?", -12.2),
        ("Agent", "You can download the free S-Net TV Remote application from the Apple App Store or Google Play Store onto your smartphone.", None),
        ("Customer", "I have an iPhone. Downloading S-Net TV Remote app right now...", 4.2),
        ("Agent", "Once installed, the app automatically discovers your S-Net TV box over your home Wi-Fi network.", None),
        ("Customer", "The app opened... It found 'S-Net TV Box SN-TV-449102'! Tapping connect...", 18.4),
        ("Agent", "You will see a full digital directional pad, channel numbers, and volume controls on your phone screen.", None),
        ("Customer", "Brian! I just pressed channel 201 on my iPhone and BBC Earth loaded immediately! My mother smiled!", 34.5),
        ("Agent", "That restores full remote control functionality immediately while the physical replacement is in transit.", None),
        ("Customer", "I can leave an old iPad on her bedside table running this remote app so she can change channels independently.", 36.2),
        ("Agent", "I have ordered a brand new official Bluetooth voice remote under dispatch reference REM-88192-S.", None),
        ("Customer", "REM-88192-S, noted down.", 28.4),
        # Turn 34 is dead air gap 2 (40s)
        ("Customer", "Hello? Brian? Did the call drop again? Why does your headset keep falling silent?", -24.2),
        ("Agent", "I was waiving the standard fifteen-pound peripheral replacement charge on your account.", None),
        ("Customer", "Thank you for waiving the charge, Brian.", 26.2),
        ("Agent", "The new physical remote will arrive via Royal Mail Tracked 24 on Friday morning.", None),
        ("Customer", "Friday morning, perfect. And the iPad app will keep her entertained until then.", 32.4),
        ("Agent", "I have included pairing instructions inside the parcel for when the new remote arrives.", None),
        ("Customer", "You have brought tremendous peace of mind to our home today.", 34.5),
        ("Agent", "Please give my warmest regards and best wishes to your mother, Sean.", None),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before we conclude, what was that TV box serial number again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you at the start of our call, it is SN-TV-449102.", -10.2),
        ("Agent", "Thank you Sean, that confirms the hardware serial on the dispatch record.", None),
        ("Customer", "Thank you again Brian for your help and kindness.", 28.4),
        ("Agent", "It has been my pleasure assisting you, Sean. Stay strong.", None),
        ("Customer", "Goodbye Brian.", 26.2),
        ("Agent", "Is there any other TV issue I can assist with today, Sean?", None),
        ("Customer", "No Brian, thank you.", 22.0),
        ("Agent", "Thank you for calling S-Net TV technical support. Goodbye.", None),
        ("Customer", "Goodbye Brian.", 18.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 14.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 10.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 6.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 2.0)
    ]

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "FAIL",
        "Verified customer": "FAIL",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "PASS",
        "Active listening": "FAIL",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Hold time and Dead Air": "Dead Air Breach: Agent had 2 occurrences of >30s unmanaged dead air.",
        "Verified customer": "Agent failed to ask for a PIN, address, or security question within the first 4 minutes of the call.",
        "Active listening": "Asked customer at turn 42 for TV box serial number which was already provided at turn 3.",
        "Build rapport and observed professionalism": "Spoke rudely at turn 11 blaming customer for dropping remote or spilling sugary tea.",
        "Confirmed the issue is resolved": "Physical remote remained broken with replacement dispatched by post, unverified on call."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net TV technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Agent allowed two separate unmanaged dead air gaps of 40 seconds at turns 14 and 34.",
        "Verified customer": "Agent failed to ask for postal address or security PIN during verification.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Sean throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand the profound heartbreak and emotional distress this is causing you, Sean...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased the remote control pairing failure at turn 2.",
        "Active listening": "Agent asked for TV box serial at turn 42 despite customer stating SN-TV-449102 at turn 3.",
        "Took ownership of the problem": "Agent guided mobile remote app setup, ordered free replacement remote, and waived fee.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you drop your remote control onto hard tiled floors or spill sugary tea into the keypad membrane, the printed circuit board traces short out.'",
        "Probing": "Agent gathered details on battery replacement and LED flashes.",
        "Confirmed the issue is resolved": "App provided temporary workaround but physical remote remained broken pending post delivery."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 42, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 2},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "rude", "agent_turn": 11},
            {"kind": "blunt_but_ok", "agent_turn": 19}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 21, "agent_turn": 22, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_083",
        "cname": "Sean",
        "target_dur": 918,
        "scenario": "TV box remote control buttons unresponsive with rapid flashing red LED; mobile app workaround with replacement dispatched",
        "tier": "okay",
        "expected_score": 66.7,
        "dead_air_indices": [14, 33],
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Build rapport and observed professionalism", "Confirmed the issue is resolved", "Verified customer"],
        "notes": "Okay call featuring dead air breaches, failed verification, rude remarks, mobile app workaround, and handled empathy in the middle third."
    }

print("get_call_083 defined.")

# =========================================================================
# Call 084: Selena, Broadband DNS resolution failure for UK banking portals, 12:26 (746s)
# 0 faults (excellent), score 100.0, All PASS
# =========================================================================
def get_call_084():
    raw = [
        ("Agent", "Thank you for calling S-Net broadband advanced technical support, my name is David. How can I help you today?", None),
        ("Customer", "Hello David, my name is Selena Gomez. Our home broadband connects to standard websites like YouTube and BBC without issue, but whenever we attempt to open UK online banking portals such as Barclays, NatWest, or HSBC, the browser times out with a 'DNS_PROBE_FINISHED_NXDOMAIN' error across all computers and smartphones in our house!", -34.8),
        ("Agent", "Good afternoon Selena. If I understand correctly, your home broadband is experiencing DNS resolution failures specifically when accessing UK banking websites with NXDOMAIN errors, while general internet traffic functions normally. Before we inspect your router's domain name resolver telemetry, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 58 St John's Wood Road, London, NW8 7HX, security PIN 8812, router model S-Net Hub 5.", -5.2),
        ("Agent", "Thank you Selena, that confirms your account details. What happens if you attempt to ping the banking domains from a command prompt?", None),
        ("Customer", "Pinging barclays.co.uk returns 'Ping request could not find host', but pinging bbc.co.uk returns reply packets in 8 milliseconds.", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query your S-Net Hub 5 local DNS cache and upstream recursive resolver tables?", None),
        ("Agent", "Thank you for holding, Selena. The resolver diagnostics indicate that your Hub 5 local DNS proxy cache has a desynchronized authoritative root zone record for the UK financial secure TLD namespace.", None),
        ("Customer", "Why would the local DNS proxy cache desynchronize for financial domains?", -10.4),
        ("Agent", "When regional DNSSEC security keys rotate overnight, the local resolver cache occasionally fails to purge expired cryptographic RRSIG validation records.", None),
        ("Customer", "Can you flush the DNS proxy cache and assign fresh upstream resolvers to our Hub 5?", 2.4),
        ("Agent", "Yes, I will remotely flush your hub's DNSSEC cache and configure our ultra-fast primary and secondary recursive resolvers.", None),
        ("Customer", "Which resolver IP addresses will you assign?", 6.2),
        ("Agent", "We will assign our core S-Net recursive DNS at 212.158.248.1 and our ultra-secure backup resolver at 1.1.1.1.", None),
        ("Customer", "1.1.1.1 is known for lightning-fast secure resolution.", 12.2),
        ("Agent", "I am pushing the updated DNS resolver payload directly to your Hub 5 cloud profile.", None),
        ("Customer", "The center light on the Hub 5 blinked white for five seconds and returned to solid green.", 18.4),
        ("Agent", "The local DNS proxy daemon has flushed its cache and reloaded the fresh authoritative root zone.", None),
        ("Customer", "Should I flush the DNS cache on our home computers as well?", 22.4),
        ("Agent", "Obviously operating systems cache host records locally, so running 'ipconfig /flushdns' ensures immediate synchronization.", None),
        ("Customer", "Running 'ipconfig /flushdns' in command prompt right now... 'Successfully flushed the DNS Resolver Cache'.", 26.2),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Selena speaking, I run an import-export logistics business from home, and I have fifty thousand pounds in international customs VAT duty payments that must be cleared through our NatWest business portal by three o'clock today! If our VAT duty payments bounce because our internet can't resolve banking websites, HM Revenue and Customs will impound three shipping containers at Felixstowe docks and my business will face sixty thousand pounds in demurrage penalties! I am terrified and in sheer panic!", -68.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand the intense terror, financial panic, and high stakes of your shipping container deadlines today, Selena. Facing sixty thousand pounds in HMRC port penalties over a DNS resolution failure is a critical emergency, and I will personally verify that your NatWest portal and all banking domains load flawlessly right now.", None),
        ("Customer", "Thank you David, please test the connection right away.", -2.4),
        ("Agent", "Please open your browser, navigate to natwest.com, and attempt to access your business banking login.", None),
        ("Customer", "Navigating to natwest.com... David! The NatWest Business Banking portal loaded instantaneously with full SSL green lock! Zero delay!", 34.8),
        ("Agent", "Fantastic! Now let us test Barclays and HSBC as well to verify comprehensive resolution across all financial domains.", None),
        ("Customer", "Opening barclays.co.uk in a new tab... Loaded immediately! Opening hsbc.co.uk... Loaded in half a second!", 38.4),
        ("Agent", "Now attempt a live test ping to natwest.com from your command prompt terminal.", None),
        ("Customer", "Pinging natwest.com... Four replies received! Round trip latency is 9 milliseconds with 0% packet loss!", 36.2),
        ("Agent", "That confirms full end-to-end DNSSEC cryptographic resolution restored across all secure financial gateways.", None),
        ("Customer", "I am logging into our NatWest portal right now and authorizing the VAT duty wire transfer as we speak.", 34.5),
        ("Agent", "Your customs containers at Felixstowe docks will be cleared with hours to spare.", None),
        ("Customer", "You have completely saved my business from disaster today, David.", 36.8),
        ("Agent", "I have locked these recursive DNS resolvers as the permanent default on your Hub 5 cloud record.", None),
        ("Customer", "That will prevent the router from ever reverting to stale DNS tables.", 32.4),
        ("Agent", "I have documented all network changes under case reference DNS-SEC-88192-S.", None),
        ("Customer", "DNS-SEC-88192-S, recorded in our office IT log.", 28.4),
        ("Agent", "Our automated network monitoring will also poll your DNS latency every sixty minutes.", None),
        ("Customer", "That is fantastic proactive engineering.", 30.2),
        ("Agent", "Thank you Selena, our priority is always safeguarding our business customers' critical connectivity.", None),
        ("Customer", "I can breathe easily now. The transfer has been authorized.", 34.2),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just ensuring my technical audit matches your exact premises: that was 58 St John's Wood Road, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, 58 St John's Wood Road, London.", 28.4),
        ("Agent", "Thank you Selena, all network parameters and premises records are fully synchronized.", None),
        ("Customer", "Thank you David for your brilliant, rapid, and reassuring support.", 36.2),
        ("Agent", "It has been an absolute pleasure assisting you, Selena. Best of luck with your logistics shipments.", None),
        ("Customer", "Have a wonderful afternoon, David.", 32.4),
        ("Agent", "Is there any other advanced technical query I can assist you with today, Selena?", None),
        ("Customer", "No David, everything is working flawlessly.", 30.2),
        ("Agent", "Thank you for calling S-Net broadband advanced technical support, Selena. Goodbye.", None),
        ("Customer", "Goodbye David.", 28.4),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 24.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 20.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 16.0)
    ]

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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net broadband advanced technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Selena throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated exceptional empathy at turn 22 ('I completely understand the intense terror, financial panic, and high stakes of your shipping container deadlines today, Selena...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased the banking portal DNS resolution issue at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer address at turn 42.",
        "Took ownership of the problem": "Agent flushed DNS cache, provisioned 1.1.1.1 resolver, guided OS flush, and verified multiple banking portals.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, comforting, and highly technical professional demeanor throughout.",
        "Probing": "Agent probed about ping outputs and NXDOMAIN error codes.",
        "Confirmed the issue is resolved": "NatWest, Barclays, and HSBC loaded with full SSL locks, and ping verified 9ms latency with 0% packet loss."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 42}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 2},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 19}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 21, "agent_turn": 22, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_084",
        "cname": "Selena",
        "target_dur": 746,
        "scenario": "Broadband DNS resolution failure for UK banking portals; resolved via Hub 5 DNS flush and 1.1.1.1 resolver provision",
        "tier": "excellent",
        "expected_score": 100.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": [],
        "notes": "Flawless technical support call demonstrating deep empathy in the middle third, DNS resolver reconfiguration, harmless recheck in the final third, and complete resolution verification."
    }

print("get_call_084 defined.")

# =========================================================================
# Call 085: Simon, Landline number withheld feature not working on outgoing NHS calls, 18:42 (1122s)
# 1-2 faults (good), score 83.3, Active listening FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_085():
    raw = [
        ("Agent", "Thank you for calling S-Net landline customer services, my name is Hannah. How can I help you today?", None),
        ("Customer", "Hello Hannah, my name is Simon Taylor. I am a community psychiatric nurse working on-call from home, and I subscribe to your permanent Number Withheld feature on our landline so patients cannot see my private home telephone number, but a patient called me back on my home landline this morning, proving that my outgoing caller identity is being broadcast and unmasked!", -34.8),
        ("Agent", "Good afternoon Simon. If I understand correctly, your permanent Number Withheld privacy feature has failed on your landline, causing your private residential telephone number to be broadcast to patients during outgoing clinical calls. Before we inspect your exchange line privacy profile, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 19 The Oval, Leeds, LS17 6TG, security PIN 3810, landline number 0113 2491024.", -5.2),
        ("Agent", "Thank you Simon, that confirms your account details. Have you attempted dialing prefix 141 before dialing outgoing patient phone numbers?", None),
        ("Customer", "I pay two pounds a month specifically for permanent automated number withholding so I don't have to manually remember 141 on every emergency call!", -18.2),
        ("Agent", "Could I place you on hold for two minutes while I query your line feature profile on the Yorkshire digital telephone exchange switch?", None),
        ("Agent", "Thank you for holding, Simon. The exchange switchboard indicates that the permanent Outgoing Calling Line Identity Restriction feature flag was de-provisioned during an automated system database purge on Sunday.", None),
        ("Customer", "Why would an automated database purge remove a vital security and privacy feature without informing me?", -14.2),
        ("Agent", "System maintenance routines occasionally flag legacy supplementary service profiles for re-validation against the central billing database.", None),
        ("Customer", "Can you re-provision permanent Calling Line Identity Restriction right now?", -4.2),
        ("Agent", "Yes, I am submitting an immediate provisioning order to re-attach permanent CLIR to line 0113 2491024.", None),
        ("Customer", "How long does it take for the exchange switch to re-activate the restriction?", 2.4),
        ("Agent", "Exchange service modifications propagate through the central line card registers in approximately sixty to one hundred and twenty minutes.", None),
        ("Customer", "So until the two hours have elapsed, my private number is still visible if I make a call?", -12.4),
        ("Agent", "Yes, unless you manually dial prefix 141 before the recipient's telephone number.", None),
        ("Customer", "Dialing 141 will guarantee the number stays hidden while the exchange updates?", 4.2),
        ("Agent", "Yes, prefix 141 forces immediate localized call-by-call caller ID suppression on the local exchange loop.", None),
        ("Customer", "I will write 141 on a sticky note on the handset for this afternoon's calls.", 8.4),
        ("Agent", "Obviously permanent CLIR flags require synchronized signaling tables on both local and regional gateway switches.", None),
        ("Customer", "Right, I understand the switch synchronization requirement.", 12.2),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Simon speaking, I handle acute psychiatric crisis patients with severe paranoid delusions and aggressive behavioral histories! Having my private residential home phone number leaked to dangerous patients puts my wife and my young children at immediate risk of stalking and home invasion! I have had to install security locks on my front gate today because S-Net turned off my privacy feature! I am sick with terror and outrage!", -68.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand the acute terror, outrage, and severe safety concerns this has caused for your wife, your young children, and your home, Simon. Having your private home telephone number exposed to psychiatric crisis patients when you rely on confidentiality is a grave security emergency, and I will ensure this restriction is permanently locked and personally verify its status with exchange engineering.", None),
        ("Customer", "Thank you Hannah, you understand why this is a matter of family safety.", -4.2),
        ("Agent", "I am attaching an urgent priority safety escalation flag to the exchange service order.", None),
        ("Customer", "What is the Openreach service order reference for this activation?", 2.4),
        ("Agent", "The exchange order reference is PRIV-CLIR-44910-Y.", None),
        ("Customer", "PRIV-CLIR-44910-Y, noted down.", 8.4),
        ("Agent", "I have also set a permanent administrative lock on your account preventing any automated routine from modifying privacy flags in the future.", None),
        ("Customer", "That will protect my family from future maintenance glitches.", 14.2),
        ("Agent", "Can we test dialing your mobile phone from the landline right now with 141 to verify manual suppression?", 18.4),
        ("Customer", "I am picking up the landline handset right now... Dialing 141 followed by my mobile number...", 22.4),
        ("Agent", "Watch your mobile phone display as the incoming call arrives.", None),
        ("Customer", "My mobile is ringing... Screen displays: 'No Caller ID'! Manual 141 suppression works perfectly!", 32.4),
        ("Agent", "That confirms that manual privacy masking is one hundred percent functional immediately.", None),
        ("Customer", "I will use 141 for all clinical calls until the permanent exchange switch completes in two hours.", 28.4),
        ("Agent", "Once the two-hour propagation window completes, permanent withholding will apply automatically without dialing 141.", None),
        ("Customer", "So we cannot test the permanent automatic withholding until two hours have passed?", 14.2),
        ("Agent", "Correct, the exchange switchboard requires the two-hour window before permanent automated suppression activates.", None),
        ("Customer", "I understand. I will test dialing without 141 at four o'clock this afternoon.", 18.4),
        ("Agent", "I have applied a ten-pound goodwill credit to your landline account for the disruption.", None),
        ("Customer", "Thank you Hannah, that is very kind.", 22.4),
        ("Agent", "I have documented your nursing duty status on the account notes for all future representatives.", None),
        ("Customer", "That will ensure everyone treats the line with clinical confidentiality.", 24.5),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before we conclude, what was that Leeds landline number again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start of our call, it is 0113 2491024.", -10.2),
        ("Agent", "Thank you Simon, the Leeds landline number is confirmed on the engineering order.", None),
        ("Customer", "Thank you Hannah for your compassion and urgent assistance today.", 28.4),
        ("Agent", "It has been my pleasure assisting you, Simon. Please stay safe, and thank you for the vital psychiatric nursing work you do.", None),
        ("Customer", "Have a wonderful afternoon, Hannah. Goodbye.", 26.2),
        ("Agent", "Is there any other landline issue I can assist you with today, Simon?", None),
        ("Customer", "No Hannah, that covers everything.", 24.0),
        ("Agent", "Thank you for calling S-Net landline customer services, Simon. Goodbye.", None),
        ("Customer", "Goodbye Hannah.", 22.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 18.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 14.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 10.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 6.0)
    ]

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "PASS",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "PASS",
        "Active listening": "FAIL",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Active listening": "Asked customer at turn 42 for landline number which was already provided at turn 3.",
        "Confirmed the issue is resolved": "Failed to confirm permanent CLIR activation on call due to 2-hour exchange propagation delay."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net landline customer services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Simon throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand the acute terror, outrage, and severe safety concerns this has caused for your wife, your young children...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased the number withheld failure at turn 2.",
        "Active listening": "Agent asked for landline number at turn 42 despite customer stating 0113 2491024 at turn 3.",
        "Took ownership of the problem": "Agent submitted urgent order, verified 141 workaround, locked permanent flag, and credited account.",
        "Build rapport and observed professionalism": "Agent maintained polite, supportive, and professional demeanor throughout.",
        "Probing": "Agent probed about prefix 141 usage and call scenarios.",
        "Confirmed the issue is resolved": "141 manual test passed, but permanent automated restriction required 2 hours to propagate on exchange, leaving automated feature unverified on call."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 42, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 2},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 19}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 21, "agent_turn": 22, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_085",
        "cname": "Simon",
        "target_dur": 1122,
        "scenario": "Landline number withheld feature not working on outgoing NHS hospital calls; 141 workaround verified, permanent fix propagation pending",
        "tier": "good",
        "expected_score": 83.3,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Confirmed the issue is resolved"],
        "notes": "Good call where agent was highly empathetic and resolved clinical safety issue, failing active listening repeat and confirmed resolved due to exchange propagation window."
    }

print("get_call_085 defined.")

if __name__ == "__main__":
    for fn in [get_call_081, get_call_082, get_call_083, get_call_084, get_call_085]:
        c = fn()
        compile_call(c)
