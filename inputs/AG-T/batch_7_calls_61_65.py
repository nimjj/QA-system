import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from batch_engine import compile_call

# =========================================================================
# Call 061: Malcolm, Fibre ONT Ethernet port auto-negotiation dropping to 100 Mbps, 10:35 (635s)
# 3-4 faults (okay), score 60.0, Empathy PASS, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL
# =========================================================================
def get_call_061():
    raw = [
        ("Agent", "Thank you for calling S-Net full fibre technical support, my name is Connor. How can I help you today?", None),
        ("Customer", "Hello Connor, my name is Malcolm Fraser. I subscribe to your 1 Gbps full fibre package, but ever since yesterday morning the LAN1 Ethernet port on the Nokia ONT wall box will only negotiate at 100 Mbps Fast Ethernet with my Asus router, throttling our entire home network to under ninety megabits!", -32.4),
        ("Agent", "Good afternoon Malcolm. I can inspect your optical terminal port parameters. Before we check the interface telemetry, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 42 Meadowcroft Lane, Edinburgh, EH12 7TY, security PIN 6614. My router is an Asus ROG Rapture GT-AX6000 and the ONT is mounted in our hallway cupboard.", -5.2),
        ("Agent", "Thank you Malcolm, that confirms your account details. Have you tried swapping the Cat6 patch cable between the ONT port 1 and your router's 2.5G WAN port?", None),
        ("Customer", "I replaced the cable with two brand new certified Cat6A cables, and both negotiate at exactly 100 Mbps Full Duplex instead of 1000 Mbps!", -22.4),
        ("Agent", "Could I place you on hold for two minutes while I query the Nokia ONT optical port telemetry and remote interface register?", None),
        ("Agent", "Thank you for holding, Malcolm. The remote physical management interface confirms that LAN port 1 PHY speed is currently locked at 100BASE-TX.", None),
        ("Customer", "Why is the optical terminal locking the physical Ethernet port down to 100BASE-TX?", -14.2),
        ("Agent", "The port hardware registers report intermittent impedance mismatches on pin pairs 4 and 5.", None),
        ("Customer", "Could the physical RJ45 socket on the ONT be faulty or dirty?", -10.4),
        ("Agent", "Well if you chose to hook up a bulky third-party gaming router with stiff shielded patch cables instead of our standard S-Net Hub, you probably bent the gold contact pins inside the socket.", None),
        ("Customer", "I used a standard patch lead with zero strain on the socket! Why are you blaming me for a hardware fault on your ONT?", -48.2),
        ("Agent", "I am explaining how physical pin deformation occurs when non-standard hardware is repeatedly inserted.", None),
        ("Customer", "Can you dispatch a field engineer to replace the Nokia ONT box?", -32.4),
        ("Agent", "Field engineering visits incur a standard callout charge of ninety-five pounds if physical socket pin damage is identified.", None),
        ("Customer", "I am not paying ninety-five pounds for your equipment failing after three months!", -38.2),
        ("Agent", "Those are our corporate engineering dispatch policies for third-party router integrations.", None),
        ("Customer", "Can we at least try forcing Gigabit full duplex from your remote optical management system?", -24.2),
        ("Agent", "Obviously Gigabit Ethernet interfaces drop down to Fast Ethernet whenever any pin in an eight-core Cat6 cable fails continuity testing.", None),
        ("Customer", "I know that Gigabit requires all four twisted pairs! What I want is a working gigabit port!", -28.4),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Malcolm speaking, I am paying eighty pounds a month for your gigabit package specifically for high-speed cloud backups, and your ONT is bottlenecking my entire office to ninety megabits! It has destroyed our productivity all morning and I am furious that we are losing billable client hours!", -58.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I understand how intensely frustrating it is to pay for gigabit speeds and find your connection restricted to under one hundred megabits during work hours, Malcolm. Let us diagnose the physical Ethernet negotiation on port 1 immediately.", None),
        ("Customer", "What options do we have to restore gigabit speed today?", -14.2),
        ("Agent", "The Nokia ONT unit features four physical Gigabit Ethernet ports on the bottom panel.", None),
        ("Customer", "Can we provision our internet connection over LAN port 2 instead of LAN port 1?", -4.2),
        ("Agent", "The optical network profile can be remapped to bridge WAN traffic across LAN port 2.", None),
        ("Customer", "Please execute that bridge remapping right now.", 2.4),
        ("Agent", "I am submitting the port remapping command to the optical line terminal.", None),
        ("Customer", "How long does the OLT take to push the provisioning profile to the ONT?", 4.2),
        ("Agent", "The provisioning script updates the local ONT flash configuration in approximately ninety seconds.", None),
        ("Customer", "The PON light is blinking green... now it has turned solid green again.", 8.4),
        ("Agent", "Please move your Cat6 patch cable from LAN port 1 into LAN port 2.", None),
        ("Customer", "Plugging the Cat6 cable into LAN port 2 now... The port LED turned solid amber and now bright green!", 18.2),
        ("Agent", "Check the Asus router administration GUI to inspect the negotiated link speed on the WAN interface.", None),
        ("Customer", "Opening Asus router dashboard... WAN port status displays: '1 Gbps Full Duplex'!", 24.5),
        ("Agent", "Please run a live speed test to confirm bandwidth throughput across the remapped port.", None),
        ("Customer", "Running speed test now... Download speed is 940 Mbps and upload is 910 Mbps with 4 milliseconds ping!", 32.4),
        ("Agent", "That confirms full gigabit line rate performance restored across the secondary optical interface.", None),
        ("Customer", "That completely bypasses the faulty port 1. Thank goodness we tested port 2.", 28.2),
        ("Agent", "I have permanently locked the WAN bridge profile to LAN port 2 on your optical line record.", None),
        ("Customer", "Will this port mapping remain active permanently?", 14.2),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before I dispatch the optical engineer, what third-party router model did you say was connected to port 1 again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start, it is an Asus ROG Rapture GT-AX6000.", -12.2),
        ("Agent", "I have logged the router model and port remap under network ticket reference FIB-44918-M.", None),
        ("Customer", "FIB-44918-M, noted down in my network diary.", 18.4),
        ("Agent", "Because port 2 is delivering full gigabit throughput, we can cancel the ninety-five-pound engineer callout.", None),
        ("Customer", "Excellent, definitely cancel any paid callout. Port 2 is working flawlessly.", 22.4),
        ("Agent", "The engineer dispatch ticket has been formally cancelled.", None),
        ("Customer", "Thank you Connor, I appreciate you remapping that port for me.", 20.2),
        ("Agent", "Is there any other aspect of your full fibre service I can assist you with today, Malcolm?", None),
        ("Customer", "No, everything is working at full speed now.", 18.2),
        ("Agent", "Thank you for calling S-Net full fibre technical support, Malcolm. Have a great day. Goodbye.", None),
        ("Customer", "Goodbye Connor.", 14.5),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 10.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 8.0)
    ]

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "PASS",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "FAIL",
        "Active listening": "FAIL",
        "Took ownership of the problem": "FAIL",
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "PASS"
    }

    coaching = {
        "Paraphrasing": "Failed to paraphrase customer's ONT Ethernet negotiation issue in own words.",
        "Active listening": "Asked customer at turn 42 for his router model which was already stated at turn 3.",
        "Took ownership of the problem": "Initially threatened customer with a £95 fee and blamed his equipment rather than proactively offering port 2 remapping.",
        "Build rapport and observed professionalism": "Spoke rudely at turn 11 blaming customer for damaging socket pins by using third-party hardware."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net full fibre technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Malcolm throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I understand how intensely frustrating it is to pay for gigabit speeds and find your connection restricted...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent never restated the ONT negotiation problem in his own words.",
        "Active listening": "Agent asked for router model at turn 42 despite customer stating Asus ROG Rapture GT-AX6000 at turn 3.",
        "Took ownership of the problem": "Agent initially blamed customer and threatened charges before remapping port.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'Well if you chose to hook up a bulky third-party gaming router with stiff shielded patch cables instead of our standard S-Net Hub, you probably bent the gold contact pins inside the socket.'",
        "Probing": "Agent gathered necessary details regarding cable specs and port LED behaviors.",
        "Confirmed the issue is resolved": "Speed test verified 940 Mbps download and 910 Mbps upload over remapped LAN port 2."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 42, "reworded": True}
        ],
        "paraphrasing": [
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
        "cid": "agt_061",
        "cname": "Malcolm",
        "target_dur": 635,
        "scenario": "Fibre ONT Ethernet port 1 failing to auto-negotiate at 1 Gbps with third-party router; resolved via LAN port 2 remap",
        "tier": "okay",
        "expected_score": 60.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Build rapport and observed professionalism", "Took ownership of the problem"],
        "notes": "Okay call where agent was rude and unhelpful initially regarding third-party router, redeemed by port 2 remapping with handled empathy in the middle third and repeat in the final third."
    }

print("get_call_061 defined.")

# =========================================================================
# Call 062: Marcus, Contract renewal loyalty discount missing from invoice, 13:57 (837s)
# 1-2 faults (good), score 80.0, Paraphrasing FAIL, Active listening FAIL
# =========================================================================
def get_call_062():
    raw = [
        ("Agent", "Thank you for calling S-Net customer accounts and billing, my name is Chloe. How can I help you today?", None),
        ("Customer", "Hello Chloe, my name is Marcus Fletcher. I renewed my broadband contract last month with an agreed loyalty tariff of thirty-five pounds per month, but my October bank statement arrived today and S-Net have charged me fifty pounds, omitting the fifteen-pound monthly loyalty discount completely!", -34.5),
        ("Agent", "Good afternoon Marcus. I can look into your contract schedule and correct that invoice for you. Before we inspect your billing ledger, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 19 Castle View, Durham, DH1 3NW, security PIN 2841, account reference SN-550182.", -5.2),
        ("Agent", "Thank you Marcus, that confirms your account details. What specific contract date did you complete the renewal agreement on?", None),
        ("Customer", "It was agreed on September 14th with an agent named David in your retentions department.", -18.2),
        ("Agent", "Could I place you on hold for two minutes while I query your promotional billing contract schedule and retentions call log?", None),
        ("Agent", "Thank you for holding, Marcus. I have reviewed the retentions order from September 14th, and I can see the fifteen-pound loyalty discount promo code LOYAL-15 was generated but failed to attach to the recurring direct debit schedule.", None),
        ("Customer", "Why did the discount code fail to attach to my direct debit?", -14.2),
        ("Agent", "The order management system encountered an API timeout with the automated banking billing scheduler during the overnight batch run.", None),
        ("Customer", "So S-Net took an extra fifteen pounds from my Santander account purely because of a computer glitch?", -24.2),
        ("Agent", "Yes, that is correct, and I will manually attach the discount promotion and issue an immediate refund for the fifteen-pound overcharge.", None),
        ("Customer", "How quickly will that fifteen pounds be refunded back to my bank account?", -10.4),
        ("Agent", "I can apply an immediate fifteen-pound credit to your S-Net account balance, or process an electronic refund directly to your Santander bank card within three working days.", None),
        ("Customer", "Please process the refund directly to my bank card; I don't want it sitting as bill credit.", -6.2),
        ("Agent", "I have submitted an electronic card refund of fifteen pounds via our Bacs gateway, reference REF-88192-M.", None),
        ("Customer", "REF-88192-M, noted down. And what about next month's bill?", 2.4),
        ("Agent", "I am manually appending promotional discount code LOYAL-15 directly to your monthly recurring billing schedule.", None),
        ("Customer", "Will that guarantee that every future invoice for the next seventeen months shows thirty-five pounds?", 6.2),
        ("Agent", "Obviously billing systems process standard tariff rates unless a verified promotion code is formally attached to the billing cycle.", None),
        ("Customer", "Yes, and now that it is attached, it should stay at thirty-five pounds.", 8.4),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "I specifically agreed to renew my contract for eighteen months because your retentions agent promised in writing that my bill would stay at thirty-five pounds! Seeing fifty pounds taken from my bank account makes me feel completely lied to and cheated! I am sick and tired of having to fight telecom companies over false promises!", -56.2),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand your frustration and disappointment at seeing a higher amount deducted after being promised a specific renewal rate, Marcus. You should never have to fight for agreed terms, and I will correct your monthly discount and credit the overcharge right now.", None),
        ("Customer", "Thank you Chloe, I appreciate you understanding why that was so upsetting.", -4.2),
        ("Agent", "I have locked the recurring thirty-five-pound charge into your account profile, valid through March 2026.", None),
        ("Customer", "Can you email me a formal revised contract confirmation displaying thirty-five pounds?", 4.2),
        ("Agent", "I am generating an updated PDF contract summary and emailing it to your registered address right now.", None),
        ("Customer", "Checking email on my phone... Yes, the PDF arrived: 'Contract Renewal Summary - Monthly Tariff £35.00'.", 16.4),
        ("Agent", "The document also confirms your fifteen-pound card refund reference on page two.", None),
        ("Customer", "Page two confirms the fifteen-pound refund to card ending 4401. That is wonderful.", 20.2),
        ("Agent", "I have also added a persistent note to your billing ledger preventing any automated rate adjustments.", None),
        ("Customer", "That gives me great peace of mind for the rest of my contract term.", 22.4),
        ("Agent", "Your direct debit for November 1st will automatically collect exactly thirty-five pounds.", None),
        ("Customer", "And the fifteen-pound refund should arrive in my Santander account by Friday?", 18.2),
        ("Agent", "Yes, banking clearing cycles take between two and three working days, so Friday at the latest.", None),
        ("Customer", "Perfect. Everything is completely transparent and documented.", 24.5),
        ("Agent", "I have also waived the five-pound paper billing fee that was erroneously added to your profile.", None),
        ("Customer", "Thank you, that is an extra five pounds saved.", 26.2),
        ("Agent", "Our priority is ensuring that promotional agreements made during contract renewal are honored precisely.", None),
        ("Customer", "You have handled this with fantastic efficiency, Chloe.", 28.4),
        ("Agent", "Thank you Marcus, I am glad we could resolve the billing discrepancy swiftly.", None),
        ("Customer", "It is refreshing when customer service actually fixes the mistake on the first call.", 30.2),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just before I apply the account credit, what was your customer account reference number again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I mentioned earlier, it is SN-550182.", -10.2),
        ("Agent", "Thank you Marcus, that closes out our formal billing ledger reconciliation.", None),
        ("Customer", "Everything looks completely sorted on my end.", 22.4),
        ("Agent", "You will also receive an SMS confirmation containing your refund tracking number.", None),
        ("Customer", "Just received the text message: 'S-Net Refund £15.00 processed successfully'.", 24.8),
        ("Agent", "Is there any other aspect of your billing account I can assist you with today, Marcus?", None),
        ("Customer", "No Chloe, you have resolved everything perfectly.", 26.4),
        ("Agent", "Thank you for calling S-Net customer accounts and billing, Marcus. Have a wonderful day. Goodbye.", None),
        ("Customer", "Goodbye Chloe.", 22.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 18.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 14.0)
    ]

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "PASS",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "FAIL",
        "Active listening": "FAIL",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "PASS"
    }

    coaching = {
        "Paraphrasing": "Failed to paraphrase customer's missing loyalty discount problem in own words.",
        "Active listening": "Asked customer at turn 42 for his account reference which was already provided at turn 3."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net customer accounts and billing' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Marcus throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand your frustration and disappointment at seeing a higher amount deducted...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent never restated the billing discount issue in own words.",
        "Active listening": "Agent asked for account reference at turn 42 despite customer stating SN-550182 at turn 3.",
        "Took ownership of the problem": "Agent manually attached discount, issued refund, sent PDF confirmation, and waived paper billing fee.",
        "Build rapport and observed professionalism": "Agent maintained polite, empathetic, and highly professional demeanor throughout.",
        "Probing": "Agent gathered necessary dates and discount amounts.",
        "Confirmed the issue is resolved": "Customer received PDF confirmation, verified £35 tariff, and received refund SMS confirmation."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 42, "reworded": True}
        ],
        "paraphrasing": [
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
        "cid": "agt_062",
        "cname": "Marcus",
        "target_dur": 837,
        "scenario": "Contract renewal loyalty discount missing from invoice; resolved via manual promotion attachment and refund",
        "tier": "good",
        "expected_score": 80.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening"],
        "notes": "Good call where agent was courteous, empathetic, and resolved billing error completely, failing only paraphrasing and active listening repeat in the final third."
    }

print("get_call_062 defined.")

# =========================================================================
# Call 063: Maya, TV set-top box recording storage showing 100% full despite deletions, 16:43 (1003s)
# 5+ faults (poor), score 35.0, Branding FAIL, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_063():
    raw = [
        # Branding FAIL: Missing standard greeting
        ("Agent", "Good afternoon, TV technical services, my name is Darren.", None),
        ("Customer", "Hello Darren, my name is Maya Al-Mansoor. My S-Net TV box recording disk says 'Storage 100% Full' and refuses to record any programs, even though I spent two hours yesterday manually deleting over thirty hours of old recordings from the library!", -32.4),
        ("Agent", "I can inspect your set-top box storage diagnostics. Before we check your disk telemetry, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 15 St George's Terrace, Newcastle, NE2 2DN, security PIN 8419, TV box serial SN-TV-99201.", -5.2),
        ("Agent", "Thank you Maya, that confirms your account details. Have you tried power-cycling the box by unplugging the mains power lead for thirty seconds?", None),
        ("Customer", "I pulled the plug three times, left it unplugged overnight, and when it booted back up, it still displayed 'Storage 100% Full - 0 GB Available'!", -24.2),
        ("Agent", "Could I place you on hold for two minutes while I query your TV box internal hard drive sector health and file allocation telemetry?", None),
        ("Agent", "Thank you for holding, Maya. The remote disk diagnostic telemetry indicates a corrupted master file allocation table on the internal one-terabyte mechanical hard drive.", None),
        ("Customer", "Can you repair the disk allocation table remotely so the box recognizes the free space?", -14.2),
        ("Agent", "Frontline representatives do not have access to run disk partition repair utilities across the broadband network.", None),
        ("Customer", "Then how do I get the box to clear the deleted shows and let me record?", -22.4),
        ("Agent", "Well if you had actually followed the on-screen storage maintenance prompts instead of filling the hard drive to the brim, the database wouldn't have corrupted.", None),
        ("Customer", "How dare you blame me! The TV box has a delete button for a reason, and I used it! Why should deleting recordings corrupt your machine?!", -52.4),
        ("Agent", "Mechanical drives experience sector corruption when write buffers overflow during large sequential deletion tasks.", None),
        ("Customer", "Can you dispatch a replacement TV set-top box that actually works?", -34.2),
        ("Agent", "Replacement boxes can only be dispatched after an on-site engineer verifies hardware disk failure.", None),
        ("Customer", "When is the earliest an engineer can come out to Newcastle?", -24.2),
        ("Agent", "The earliest available technician appointment in your postal sector is next Tuesday morning.", None),
        ("Customer", "Next Tuesday?! Today is Thursday! I cannot wait five days without television recording!", -44.2),
        ("Agent", "Obviously magnetic hard disk allocation tables cannot reclaim sectors if the file index has become desynchronized.", None),
        ("Customer", "Stop reciting technical excuses and give me a solution for tonight!", -38.2),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Maya speaking, I have deleted thirty hours of saved series to make room for my daughter's dance recital recording tonight, and your box still says 'Storage 100% Full - Recording Prohibited'! If this box fails to record her championship recital tonight after I deleted all my favorite programs for nothing, I will throw this TV box through your shop window! I am furious!", -64.8),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand your immense frustration and worry about losing the recording of your daughter's dance championship tonight, Maya. Having deleted hours of cherished programs only to see the disk still full is deeply stressful, so let us troubleshoot the drive index immediately.", None),
        ("Customer", "What can we do right now without waiting until Tuesday?", -16.2),
        ("Agent", "There is a hidden recovery menu option called 'Full Hard Disk Reformat' accessible via the box front panel.", None),
        ("Customer", "What happens if I execute a Full Hard Disk Reformat?", -8.4),
        ("Agent", "A full reformat wipes every single recording, scheduled series link, and cached movie, restoring the drive to factory zero state.", None),
        ("Customer", "Wipe everything?! I still have my late grandmother's televised interview saved on that drive! I cannot wipe the drive and lose her voice forever!", -54.2),
        ("Agent", "That is the only operational method to rebuild a desynchronized master allocation table.", None),
        ("Customer", "Can I back up my grandmother's recording to a USB memory stick first before reformatting?", -22.4),
        ("Agent", "S-Net TV set-top boxes enforce encrypted digital rights management; recordings cannot be exported to external USB storage.", None),
        ("Customer", "So you are giving me a choice between losing my grandmother's video forever or not recording my daughter tonight?!", -58.2),
        ("Agent", "Those are the cryptographic constraints engineered into the TVOS operating system.", None),
        ("Customer", "This is an appalling piece of hardware design. Why don't you have cloud recording backups?!", -42.4),
        ("Agent", "Cloud recording features are only included on our premium Fiber TV 360 subscription tier.", None),
        ("Customer", "Can I upgrade to Fiber TV 360 right now to save her recording?", -18.2),
        ("Agent", "Fiber TV 360 upgrades require an engineer visit to install new hybrid coaxial hardware.", None),
        ("Customer", "So that doesn't solve tonight either.", -24.2),
        ("Agent", "Correct. You would have to accept the Tuesday engineer visit.", None),
        ("Customer", "I refuse to format this drive and delete my grandmother's memories. I will have to record my daughter on my smartphone instead.", -28.4),
        ("Agent", "I have documented your refusal to format the drive under maintenance ticket TV-88210-D.", None),
        ("Customer", "TV-88210-D, noted down.", -14.2),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before I close this diagnostic file, what was that TV box serial number again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start of our call, it is SN-TV-99201.", -18.2),
        ("Agent", "I have logged the serial number against the Tuesday technician appointment slot.", None),
        ("Customer", "Book the Tuesday appointment then, but tell the technician he is not to format the drive without my express permission.", -16.2),
        ("Agent", "The technician will assess whether the hardware chassis can be replaced without formatting the drive.", None),
        ("Customer", "I am completely disgusted by this entire experience. S-Net has ruined our family evening.", -28.5),
        ("Agent", "The technician appointment is scheduled for Tuesday between eight in the morning and one in the afternoon.", None),
        ("Customer", "Tuesday morning, noted. Goodbye.", -18.2),
        ("Agent", "Is there any other TV issue I can assist you with today, Maya?", None),
        ("Customer", "No, you have been thoroughly unhelpful.", -22.4),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -14.2),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -10.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -8.0)
    ]

    ratings = {
        "Branding and Survey Check": "FAIL",
        "Hold time and Dead Air": "PASS",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "FAIL",
        "Active listening": "FAIL",
        "Took ownership of the problem": "FAIL",
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Branding and Survey Check": "Failed opening branding script by omitting company greeting and closing branding.",
        "Paraphrasing": "Failed to paraphrase customer's TV recording disk corruption issue in own words.",
        "Active listening": "Asked customer at turn 42 for TV box serial number which was already provided at turn 3.",
        "Took ownership of the problem": "Failed to find any viable workaround or escalate, leaving customer facing either loss of irreplaceable family video or inability to record.",
        "Build rapport and observed professionalism": "Spoke rudely at turn 11 blaming customer for filling hard drive to the brim.",
        "Confirmed the issue is resolved": "Issue was left completely unresolved; TV box still refused to record and customer ended call in deep distress."
    }

    evidence = {
        "Branding and Survey Check": "Agent failed standard opening branding ('Good afternoon, TV technical services...') and closing branding.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Maya throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand your immense frustration and worry about losing the recording of your daughter's dance championship...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent never restated the TV disk storage fault in own words.",
        "Active listening": "Agent asked for serial number at turn 42 despite customer stating SN-TV-99201 at turn 3.",
        "Took ownership of the problem": "Agent blamed customer and offered only destructive reformatting.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'Well if you had actually followed the on-screen storage maintenance prompts instead of filling the hard drive to the brim, the database wouldn't have corrupted.'",
        "Probing": "Agent asked relevant questions regarding power-cycling and error codes.",
        "Confirmed the issue is resolved": "Box remained unable to record, reformat was rejected due to data loss, and issue remained unresolved."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 42, "reworded": True}
        ],
        "paraphrasing": [
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
        "cid": "agt_063",
        "cname": "Maya",
        "target_dur": 1003,
        "scenario": "TV set-top box recording storage showing 100% full despite deletions; corrupt file allocation table unresolved",
        "tier": "poor",
        "expected_score": 35.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Branding and Survey Check", "Build rapport and observed professionalism", "Confirmed the issue is resolved", "Took ownership of the problem"],
        "notes": "Poor call marked by failed branding, rude victim-blaming, failure to resolve disk corruption, and repeated serial questioning in the last third, alongside handled empathy."
    }

print("get_call_063 defined.")

# =========================================================================
# Call 064: Megan, Mobile roaming in USA failing to connect to partner networks, 14:31 (871s)
# 0 faults (excellent), score 100.0, All PASS
# =========================================================================
def get_call_064():
    raw = [
        ("Agent", "Thank you for calling S-Net international roaming support, my name is Oliver. How can I help you today?", None),
        ("Customer", "Hello Oliver, my name is Megan Brooks. I landed at JFK Airport in New York an hour ago, but my iPhone displays 'No Service' and refuses to register on AT&T or T-Mobile, leaving me completely stranded without maps or data!", -34.8),
        ("Agent", "Good afternoon Megan. If I understand correctly, your mobile phone is displaying 'No Service' after arriving at JFK Airport and is failing to latch onto partner cellular networks in the United States. Before we check your roaming profile, could you confirm your full UK postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 58 Park Avenue, Manchester, M14 5TP, security PIN 1192, mobile number 07700 900542.", -5.2),
        ("Agent", "Thank you Megan, that confirms your account details. Let us inspect your SIM card's international roaming provisioning status immediately.", None),
        ("Customer", "Thank you Oliver. I am using the free airport terminal Wi-Fi to make this call via Wi-Fi calling.", -12.4),
        ("Agent", "Could I place you on hold for two minutes while I query your international roaming provisions on the US partner gateway?", None),
        ("Agent", "Thank you for holding, Megan. The international gateway indicates that your domestic S-Net line has the Roam Abroad pass active, but the IMSI profile was locked to UK terrestrial bands.", None),
        ("Customer", "Why would the IMSI profile be locked to UK frequencies?", -10.2),
        ("Agent", "When traveling across international regulatory domains, the SIM sometimes caches the previous home network frequency table and fails to initiate global PLMN discovery.", None),
        ("Customer", "Can you trigger a global network profile reset from your console?", -6.4),
        ("Agent", "Yes, I have sent an over-the-air network profile refresh and lifted the international registration bar on your HLR record.", None),
        ("Customer", "What manual settings should I adjust on my iPhone right now?", 2.4),
        ("Agent", "Please open Settings, select 'Mobile Service', and ensure that 'Data Roaming' is toggled to ON.", None),
        ("Customer", "Checking... 'Data Roaming' is toggled to ON.", 6.2),
        ("Agent", "Now tap 'Network Selection' and turn off the 'Automatic' slider switch.", None),
        ("Customer", "Toggled 'Automatic' to OFF... A spinning loading wheel appeared.", 8.4),
        ("Agent", "The phone will scan local broadcast beacons for nearby US carrier networks.", None),
        ("Customer", "The carrier list just populated: AT&T, T-Mobile, and Verizon.", 12.2),
        ("Agent", "Obviously foreign cellular networks reject SIM authentication requests if international data roaming bolt-ons have not completed handshake negotiation.", None),
        ("Customer", "Right, I understand the carrier handshake requirement.", 14.5),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Megan speaking, I just landed at JFK after an eight-hour flight, I am standing in the arrival terminal alone with three suitcases, and my phone says 'No Service'! I cannot book an Uber, I cannot message my hotel, and I cannot access my mobile banking! I am stranded in an international airport with no way to communicate and I am having a panic attack!", -65.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand how frightening and terrifying it is to be stranded at an overseas airport with no mobile signal and no way to arrange transport or reach your hotel, Megan. Please take a deep breath; you have reached the right person, and I will stay on the line with you until your phone is fully connected to the US network.", None),
        ("Customer", "Thank you so much Oliver, I really need to get to my hotel safely.", -8.2),
        ("Agent", "Please tap 'T-Mobile' on the carrier list to force registration on our primary US roaming partner.", None),
        ("Customer", "Tapping 'T-Mobile'... The spinning icon is running...", -2.4),
        ("Agent", "The gateway is processing the international diameter authentication packet.", None),
        ("Customer", "Oliver! 'No Service' just vanished! It now displays: 'T-Mobile - 5G' with four solid signal bars!", 28.4),
        ("Agent", "Fantastic! Let us now verify mobile data throughput by loading an external web page with Wi-Fi turned off.", None),
        ("Customer", "Turning off airport Wi-Fi now... Opening Safari... Loaded Google Maps instantly! It shows my exact location at Terminal 4!", 32.4),
        ("Agent", "Now let us verify outbound voice calling by dialing our international roaming test number on +44 800 012 3456.", None),
        ("Customer", "Dialing +44 800 012 3456... Automated voice answered immediately: 'S-Net Roaming Line Test Successful'!", 36.2),
        ("Agent", "That confirms voice, SMS, and high-speed 5G mobile data are all fully operational across the United States.", None),
        ("Customer", "I just opened my Uber app and it found drivers right outside the arrivals curb!", 38.4),
        ("Agent", "Your Roam Abroad pass gives you full access to your UK domestic data allowance of thirty gigabytes while traveling.", None),
        ("Customer", "That is incredible relief. I was so panicked standing here alone.", 32.4),
        ("Agent", "I have documented your T-Mobile carrier registration under roaming case reference US-99182-M.", None),
        ("Customer", "US-99182-M, noted down.", 26.2),
        ("Agent", "If your handset ever loses signal when traveling between states, keeping Network Selection on T-Mobile will ensure priority roaming.", None),
        ("Customer", "I will leave it locked to T-Mobile throughout my trip.", 24.8),
        ("Agent", "I have also set an automated high-usage alert on your roaming profile to prevent unexpected charges.", None),
        ("Customer", "Thank you, that is so thoughtful and protective.", 28.2),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just ensuring my roaming verification ticket has your exact UK mobile number: that was 07700 900542, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, 07700 900542 is my number.", 24.5),
        ("Agent", "Thank you Megan, all roaming records and diagnostic logs are fully updated.", None),
        ("Customer", "You have completely saved my trip to New York, Oliver. Thank you from the bottom of my heart.", 34.8),
        ("Agent", "It has been an absolute pleasure assisting you, Megan. Safe travels to your hotel.", None),
        ("Customer", "Have a wonderful rest of your day, Oliver.", 30.2),
        ("Agent", "Is there any other mobile roaming query I can assist you with today, Megan?", None),
        ("Customer", "No Oliver, everything is working flawlessly.", 28.4),
        ("Agent", "Thank you for calling S-Net international roaming support, Megan. Enjoy your stay in the United States. Goodbye.", None),
        ("Customer", "Goodbye Oliver.", 26.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 22.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 18.0)
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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net international roaming support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Megan throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated exceptional empathy at turn 22 ('I completely understand how frightening and terrifying it is to be stranded at an overseas airport...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased US mobile roaming fault at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer mobile number at turn 42.",
        "Took ownership of the problem": "Agent refreshed HLR, guided manual network selection, verified data and voice, and added usage alerts.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, comforting, and highly professional demeanor throughout.",
        "Probing": "Agent gathered necessary details regarding error messages, handset model, and roaming settings.",
        "Confirmed the issue is resolved": "Customer tested 5G data on Google Maps, completed test call on +44 800 012 3456, and loaded Uber app successfully."
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
        "cid": "agt_064",
        "cname": "Megan",
        "target_dur": 871,
        "scenario": "Mobile roaming in USA failing to connect to partner networks; resolved via OTA refresh and manual T-Mobile registration",
        "tier": "excellent",
        "expected_score": 100.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": [],
        "notes": "Flawless international support call demonstrating deep empathy in the middle third, reassuring rapport, harmless recheck in the final third, and complete resolution verification."
    }

print("get_call_064 defined.")

# =========================================================================
# Call 065: Miles, Suspected UDP DDoS attack flooding residential connection, 19:22 (1162s)
# 3-4 faults (okay), score 60.0, Empathy PASS, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL
# =========================================================================
def get_call_065():
    raw = [
        ("Agent", "Thank you for calling S-Net broadband network security, my name is Toby. How can I help you today?", None),
        ("Customer", "Hello Toby, my name is Miles Henderson. Our residential broadband connection has been completely frozen for the last four hours: the router's internet LED is flashing amber wildly, our latency has jumped to fifteen hundred milliseconds, and packet loss is at ninety-five percent; I believe our public IP address is being targeted by a distributed denial-of-service UDP flood after a dispute during an online Discord gaming tournament!", -34.8),
        ("Agent", "Good afternoon Miles. I can inspect your WAN interface flow statistics and packet drop rates. Before we inspect your connection telemetry, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 112 Richmond Road, Bath, BA1 5TU, security PIN 4430, customer account SN-882190.", -5.2),
        ("Agent", "Thank you Miles, that confirms your account details. Have you attempted a thirty-second power restart on your S-Net Hub to request a new dynamic IP allocation?", None),
        ("Customer", "I power-cycled the hub twice, but the BRAS gateway assigned the exact same 82.132.x.x public IP address both times because the DHCP lease hasn't expired!", -22.4),
        ("Agent", "Could I place you on hold for two minutes while I query the broadband edge router flow telemetry and packet drop statistics?", None),
        ("Agent", "Thank you for holding, Miles. Our edge monitoring shows an inbound traffic spike of four hundred megabits per second consisting entirely of fragmented UDP packets directed at port 27015 on your public IP.", None),
        ("Customer", "Four hundred megabits of junk UDP traffic! That is saturating our entire download bandwidth! Can you drop that traffic at your upstream BRAS gateway?", -24.2),
        ("Agent", "Residential broadband packages do not include automated volumetric DDoS mitigation or upstream traffic scrubbing.", None),
        ("Customer", "Well if you cannot scrub the traffic upstream, can you force-release my WAN IP address and lease me a clean IP right now?", -18.2),
        ("Agent", "If you choose to run unsecured public gaming servers from a residential broadband connection, you bring DDoS attacks on yourself.", None),
        ("Customer", "I was playing a standard multiplayer video game on my PC! I did not run an illegal server! Why are you blaming me for cyber-attacks against my home?", -52.4),
        ("Agent", "Exposing local gaming ports to public Discord lobbies invites distributed packet flooding from adversaries.", None),
        ("Customer", "I don't care about the attackers' motives! I have an entire household with zero internet access! Will you release my IP address or not?!", -44.2),
        ("Agent", "WAN dynamic IP releases require a physical line sync tear-down from our central exchange port controller.", None),
        ("Customer", "Then initiate the physical line sync tear-down right now!", -36.2),
        ("Agent", "Line sync tear-downs drop active telephony connections and can trigger automated line profile rate adaptations.", None),
        ("Customer", "My connection is already ninety-five percent packet loss! A rate adaptation is far better than a total outage!", -28.4),
        ("Agent", "Obviously residential consumer broadband tiers do not include enterprise-grade BGP scrubbing centers to filter distributed denial-of-service floods.", None),
        ("Customer", "I am not asking for enterprise BGP scrubbing! I am asking for an IP address renewal!", -32.4),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Miles speaking, my entire household internet has been completely paralyzed for four hours! My wife cannot conduct her telehealth medical consultations, my smart home security is offline, and every light on your router is blinking frantically! Paying seventy pounds a month for a connection that collapses because someone online attacks our IP address is totally unacceptable! We need this stopped right now!", -62.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand the immense frustration and disruption this is causing to your household, Miles, especially with your wife unable to carry out essential telehealth consultations and home security knocked offline. Let us inspect the edge firewall traffic and reset your external IP address immediately.", None),
        ("Customer", "Thank you Toby. What is the exact process to force a new IP lease?", -12.2),
        ("Agent", "I will send a remote administrative flush command to the BRAS gateway session manager, terminating your current PPPoE session.", None),
        ("Customer", "Will that force the gateway to allocate a new IP from a different subnet block?", -4.2),
        ("Agent", "Yes, terminating the PPPoE session clears the MAC binding cache and triggers a fresh IP allocation from the Bath regional pool.", None),
        ("Customer", "Please execute the PPPoE flush command immediately.", 2.4),
        ("Agent", "Sending PPPoE session termination command to the exchange node now.", None),
        ("Customer", "The internet light on the hub turned red... now it has gone completely dark.", 4.2),
        ("Agent", "The old session has been cleared from the edge routing table. The hub will now re-authenticate.", None),
        ("Customer", "The hub light is pulsing orange... and now it turned solid white!", 16.4),
        ("Agent", "Please open your browser, navigate to whatismyipaddress.com, and check your assigned public IP.", None),
        ("Customer", "Checking whatismyipaddress.com... The new IP is 148.252.190.84! It was 82.132.44.12 earlier!", 24.8),
        ("Agent", "Now run a ping test to our primary DNS server on 8.8.8.8 to verify packet loss and latency.", None),
        ("Customer", "Opening command prompt: pinging 8.8.8.8... Zero percent packet loss! Average round-trip latency is 11 milliseconds!", 32.4),
        ("Agent", "The inbound four-hundred-megabit UDP flood was directed at the old IP address, leaving your new IP completely unburdened.", None),
        ("Customer", "The router traffic meter has dropped back down to baseline. Everything is loading instantaneously!", 34.2),
        ("Agent", "I will also enable stealth mode on your hub's SPI firewall to silently discard unexpected ICMP and UDP probes.", None),
        ("Customer", "That will prevent prospective attackers from scanning open gaming ports in the future.", 28.4),
        ("Agent", "Firewall stealth mode is now active on WAN interface 148.252.190.84.", None),
        ("Customer", "My wife just reconnected her telehealth portal and her video consult is streaming smoothly.", 32.4),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before I request the dynamic IP lease flush, what was your customer account reference number again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start of the call, it is SN-882190.", -12.4),
        ("Agent", "Thank you Miles, that closes out our security session audit under reference SEC-88190-H.", None),
        ("Customer", "SEC-88190-H, noted down in our home network notes.", 22.4),
        ("Agent", "Your dynamic IP lease is valid for fourteen days and will rotate automatically on normal router restarts.", None),
        ("Customer", "Understood. If another attack ever happens, I know to ask for a PPPoE session flush.", 20.2),
        ("Agent", "Our automated network defense monitors will also flag sustained flood traffic over five hundred megabits.", None),
        ("Customer", "Thank you Toby for flushing that PPPoE session and restoring our family internet.", 24.5),
        ("Agent", "Is there any other security query I can assist you with today, Miles?", None),
        ("Customer", "No, the new IP address has completely resolved the attack.", 26.2),
        ("Agent", "Thank you for calling S-Net broadband network security, Miles. Have a safe and pleasant day. Goodbye.", None),
        ("Customer", "Goodbye Toby.", 22.4),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 18.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 14.0)
    ]

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "PASS",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "FAIL",
        "Active listening": "FAIL",
        "Took ownership of the problem": "FAIL",
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "PASS"
    }

    coaching = {
        "Paraphrasing": "Failed to paraphrase customer's DDoS traffic saturation issue in own words.",
        "Active listening": "Asked customer at turn 42 for his account reference which was already stated at turn 3.",
        "Took ownership of the problem": "Initially deflected responsibility and blamed customer for bringing cyber-attacks on himself rather than immediately offering a session flush.",
        "Build rapport and observed professionalism": "Spoke rudely at turn 11 blaming customer for playing online video games."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net broadband network security' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Miles throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand the immense frustration and disruption this is causing to your household, Miles...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent never restated the UDP packet flood problem in own words.",
        "Active listening": "Agent asked for account reference at turn 42 despite customer stating SN-882190 at turn 3.",
        "Took ownership of the problem": "Agent blamed customer before eventually performing PPPoE flush.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you choose to run unsecured public gaming servers from a residential broadband connection, you bring DDoS attacks on yourself.'",
        "Probing": "Agent checked traffic volume, destination port 27015, and ping statistics.",
        "Confirmed the issue is resolved": "PPPoE session flush allocated new IP 148.252.190.84, latency normalized to 11ms, and 0% packet loss verified."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 42, "reworded": True}
        ],
        "paraphrasing": [
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
        "cid": "agt_065",
        "cname": "Miles",
        "target_dur": 1162,
        "scenario": "Suspected UDP DDoS attack flooding residential connection; resolved via remote PPPoE session flush and IP renewal",
        "tier": "okay",
        "expected_score": 60.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Build rapport and observed professionalism", "Took ownership of the problem"],
        "notes": "Okay call where agent blamed customer for gaming traffic initially, saved by PPPoE flush, with handled empathy in the middle third and repeat in the final third."
    }

print("get_call_065 defined.")

if __name__ == "__main__":
    for fn in [get_call_061, get_call_062, get_call_063, get_call_064, get_call_065]:
        c = fn()
        compile_call(c)
