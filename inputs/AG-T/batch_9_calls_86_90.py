import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from batch_engine import compile_call

# =========================================================================
# Call 086: Sonia, Direct debit cancellation by bank causing restriction warning, 10:35 (635s)
# 6 faults (poor), score 20.0, Dead Air FAIL, Verified FAIL, Personalized FAIL, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Probing FAIL, Confirmed resolved FAIL
# Features TWO outbursts (turn 8 handled, turn 21 unhandled)
# =========================================================================
def get_call_086():
    raw = [
        ("Agent", "Thank you for calling S-Net accounts and billing department, my name is Marcus. How can I help you today?", None),
        ("Customer", "Hello, my name is Sonia Richardson. I received an urgent text message and email warning me that our broadband service will be disconnected in twenty-four hours because our monthly direct debit bounced, but my bank says they cancelled the mandate by clerical error during a branch merger and I need you to restore the account and stop any disconnection!", -45.2),
        # Paraphrasing FAIL: agent does not restate; Verified FAIL: agent fails to ask for PIN/address/security question
        ("Agent", "I can inspect the billing status. What is the billing account number listed on your warning notice?", None),
        ("Customer", "The account number is SN-991204, postal address 14 Highfield Lane, St Albans, AL1 4XX, security PIN 4491.", -12.4),
        # Personalized FAIL: agent never calls her Sonia anywhere in call
        ("Agent", "Let me pull up account SN-991204 on the collections ledger.", None),
        ("Customer", "Please check why the system flagged immediate disconnection.", -18.2),
        ("Agent", "Could I place you on hold for two minutes while I query the Automated Clearing House direct debit return code?", None),
        ("Agent", "Thank you for holding. The direct debit returned code 'Instruction Cancelled by Payer' on Monday morning.", None),
        # Outburst 1 at turn 8 (handled)
        ("Customer", "Instruction cancelled by payer?! That is an absolute lie by Barclays Bank! I never told them to cancel anything! I have been a loyal S-Net customer for twelve years and I am furious that your automated system threatens to cut off my service like I am a criminal debtor!", -72.4),
        # Agent handled empathy 1 at turn 9
        ("Agent", "I completely understand your frustration and anger at receiving a disconnection threat when your bank made a clerical mistake, especially given your twelve years of loyalty with S-Net. Let us get this sorted so your broadband remains fully active.", None),
        ("Customer", "Thank you Marcus, I appreciate that.", -8.2),
        # Turn 11: diagnostic remark
        ("Agent", "Delinquent billing accounts are subject to automatic clearing house rejection routines.", None),
        ("Customer", "Barclays said they would reimburse any penalty fee, but I need you to reinstate the direct debit.", -24.2),
        ("Agent", "I am explaining alternative payment methods available for billing accounts.", None),
        # Turn 14 is dead air gap 1 (40s)
        ("Customer", "Marcus? Are you still on the phone? The line went completely dead for forty seconds!", -28.4),
        ("Agent", "I was waiting for the billing ledger database to populate.", None),
        ("Customer", "Can you waive the twenty-pound direct debit rejection penalty fee?", -24.2),
        ("Agent", "Obviously banking rejection fees are generated automatically by our financial clearing software.", None),
        ("Customer", "Barclays said they would reimburse any penalty fee, but I need you to reinstate the direct debit.", -14.2),
        ("Agent", "Direct debit reinstatement requires seven working days to verify banking credentials.", None),
        ("Customer", "Seven working days? What happens to my broadband connection in the meantime?", -22.4),
        # Outburst 2 at turn 21: Customer second outburst in middle third (unhandled)
        ("Customer", "I am a single mother working as an emergency 999 dispatcher from my kitchen table! If my broadband is disconnected tomorrow because of this bureaucratic mess, I will be unable to log into the emergency dispatch console, callers in life-or-death situations will get no answer, and I will be suspended from my job! I am having a complete panic attack right now!", -88.4),
        # Turn 22: Agent MISSED/UNHANDLED empathy (agent completely ignores panic and talks about debit cards)
        ("Agent", "You can make an immediate debit card payment of sixty-four pounds and fifty pence over our telephone keypad.", None),
        ("Customer", "Did you even hear what I just said about dispatching 999 emergency calls?! You have zero empathy!", -76.2),
        # Rapport FAIL at turn 24 (middle third)
        ("Agent", "If you cannot manage your personal bank account standing orders responsibly, you have only yourself to blame.", None),
        ("Customer", "Fine, take the debit card payment right now so my service doesn't drop!", -44.2),
        ("Agent", "Please enter your sixteen-digit card number followed by the hash key.", None),
        ("Customer", "Entering card number now...", -12.4),
        ("Agent", "Payment authorization received for sixty-four pounds and fifty pence.", None),
        ("Customer", "Has the disconnection notice been removed from my file?", -8.2),
        ("Agent", "The card payment settles the outstanding invoice balance.", None),
        ("Customer", "Can you guarantee that the automated disconnection scheduled for tomorrow is cancelled?", -14.2),
        # Turn 34 is dead air gap 2 (40s)
        ("Customer", "Marcus?! Hello?! Did you put me on mute again?! Why do you keep vanishing for forty seconds?!", -42.4),
        ("Agent", "I was refreshing the service profile on the billing database.", None),
        ("Customer", "Is the service safe from disconnection tomorrow?", -18.4),
        ("Agent", "The payment has cleared on the transaction record.", None),
        ("Customer", "What about setting up the new direct debit mandate so this doesn't happen next month?", -12.2),
        ("Agent", "You will need to re-enter your bank sort code and account number via the online web portal.", None),
        ("Customer", "Can you not set it up over the phone right now?", -14.2),
        ("Agent", "Our telephone team does not take bank account numbers for new mandates.", None),
        ("Customer", "Okay, I will log into the website this evening.", -4.2),
        # Turn 42: Active listening repeat in last third
        ("Agent", "Before we wrap up, what was that postal address again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start, it is 14 Highfield Lane, St Albans.", -18.2),
        ("Agent", "Thank you, postal address verified.", None),
        ("Customer", "Can you give me a reference number for the payment?", -6.2),
        ("Agent", "Your payment reference is PAY-88192-S.", None),
        ("Customer", "PAY-88192-S.", 2.4),
        ("Agent", "Is there any other billing query today?", None),
        ("Customer", "No, but your customer service was appalling.", -28.2),
        ("Agent", "Thank you for calling S-Net accounts and billing. Goodbye.", None),
        ("Customer", "Goodbye.", -12.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", -8.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -4.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 0.0)
    ]

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "FAIL",
        "Verified customer": "FAIL",
        "Personalized the call/ticket appropriately": "FAIL",
        "Empathy & Acknowledgment Statement": "FAIL",
        "Paraphrasing": "FAIL",
        "Active listening": "FAIL",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "FAIL",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Hold time and Dead Air": "Dead Air Breach: Agent had 2 occurrences of >30s unmanaged dead air.",
        "Verified customer": "Agent failed to ask for a PIN, address, or security question within the first 4 minutes of the call.",
        "Personalized the call/ticket appropriately": "Agent failed to address customer by name 'Sonia' during the call.",
        "Empathy & Acknowledgment Statement": "Failed to acknowledge customer's severe distress and panic at turn 21 regarding 999 dispatch work.",
        "Paraphrasing": "Failed to paraphrase customer's direct debit issue at the beginning of the call.",
        "Active listening": "Asked customer at turn 41 for postal address which was already provided at turn 3.",
        "Build rapport and observed professionalism": "Insulted customer at turn 11: 'If you cannot manage your bank account standing orders responsibly, you should pay by cash at a Post Office counter.'",
        "Probing": "Failed to probe effectively regarding bank merger details or direct debit return specifics.",
        "Confirmed the issue is resolved": "Failed to confirm that automated disconnection had been cancelled in the provisioning system."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net accounts and billing department' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Agent allowed two separate unmanaged dead air gaps of 40 seconds at turns 14 and 33.",
        "Verified customer": "Agent failed to ask for postal address or security PIN during initial verification.",
        "Personalized the call/ticket appropriately": "Agent never addressed customer as Sonia throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent handled first outburst at turn 8, but completely ignored severe panic outburst at turn 21 regarding 999 dispatch work.",
        "Paraphrasing": "Agent offered no restatement of the customer's problem.",
        "Active listening": "Agent asked for postal address at turn 42 despite customer stating 14 Highfield Lane at turn 3.",
        "Took ownership of the problem": "Agent processed card payment and provided transaction reference.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you cannot manage your bank account standing orders and direct debits responsibly, you should pay by cash at a Post Office counter every month.'",
        "Probing": "Agent asked no diagnostic questions about the banking notice.",
        "Confirmed the issue is resolved": "Agent took card payment but failed to verify that the automated disconnection workflow had been halted."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 41, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 2},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "rude", "agent_turn": 24},
            {"kind": "blunt_but_ok", "agent_turn": 17}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 8, "agent_turn": 9, "with_refusal": False},
            {"kind": "unhandled", "customer_turn": 21}
        ]
    }

    return {
        "cid": "agt_086",
        "cname": "Sonia",
        "target_dur": 635,
        "scenario": "Direct debit cancelled by bank clerical error causing urgent disconnection warning; 2 outbursts (one handled, one unhandled); 6+ faults (poor)",
        "tier": "poor",
        "expected_score": 20.0,
        "dead_air_indices": [14, 33],
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Build rapport and observed professionalism", "Empathy & Acknowledgment Statement", "Confirmed the issue is resolved", "Verified customer", "Personalized the call/ticket appropriately", "Probing", "Paraphrasing"],
        "notes": "Poor call featuring multiple dead air breaches, two customer outbursts (first handled, second unhandled), rude remarks, failed verification and personalization, and active listening repeat."
    }

print("get_call_086 defined.")

# =========================================================================
# Call 087: Sorcha, Wi-Fi mesh range insufficient for detached garage office, 13:45 (825s)
# 1-2 faults (good), score 83.3, Active listening FAIL, Confirmed resolved FAIL
# Features TWO handled outbursts (turn 15 handled, turn 21 handled)
# =========================================================================
def get_call_087():
    raw = [
        ("Agent", "Thank you for calling S-Net broadband technical support, my name is Liam. How can I help you today?", None),
        ("Customer", "Hello Liam, my name is Sorcha Gallagher. I work from a detached garage office in our back garden twenty meters from the house, and our home S-Net Wi-Fi signal does not reach into the garden office, constantly dropping video conferences with clients and making remote working impossible!", -34.8),
        ("Agent", "Good afternoon Sorcha. If I understand correctly, your home Wi-Fi signal is failing to penetrate into your detached garden office twenty meters away, causing continuous dropped video calls with clients. Before we examine your hub's wireless coverage and mesh extension options, could you please confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 22 Millfield Crescent, Harrogate, HG2 8PT, security PIN 7714.", -5.2),
        ("Agent", "Thank you Sorcha, that brings up your account details. What router model are you currently using in the main house?", None),
        ("Customer", "It is the tall white S-Net Hub 5 situated in our ground floor living room.", -12.4),
        ("Agent", "Could I place you on hold for two minutes while I query your Hub 5 wireless telemetry and radio power output?", None),
        ("Agent", "Thank you for holding, Sorcha. Looking at the wireless diagnostics, your Hub 5 is transmitting at full legal EIRP power, but the exterior stone cavity walls and double-glazed garden doors attenuate the 5 GHz signal by over 35 decibels.", None),
        ("Customer", "Is there a way to boost the signal across the garden lawn into the garage?", -10.2),
        ("Agent", "Yes, our S-Net Intelligent Mesh Wi-Fi Pods are designed specifically to extend whole-home wireless coverage into garden studios and outbuildings.", None),
        ("Customer", "How does the mesh pod connect to the main router?", 2.4),
        ("Agent", "The mesh pod utilizes a dedicated 5 GHz backhaul channel or can be connected via an external Cat6 Ethernet cable.", None),
        ("Customer", "I do have an exterior Cat6 Ethernet cable already running under the lawn from the house into the garage!", 18.4),
        ("Agent", "That is an ideal setup: connecting the mesh pod via Ethernet creates a full-speed zero-loss wireless access point inside your office.", None),
        ("Customer", "That sounds brilliant!", 24.2),
        # Outburst 1 at turn 15 (handled - late acknowledgement 3 turns after)
        ("Customer", "Sorcha speaking, I run a freelance architectural consultancy, and I lost a twelve-thousand-pound commercial design tender yesterday because my video call froze during the client presentation! I was mortified and terrified that my business reputation is ruined! I have been crying with frustration all morning!", -64.2),
        ("Agent", "I am querying our equipment logistics warehouse inventory right now.", None),
        ("Customer", "Please do Liam, I am desperate to protect our architectural projects.", 8.4),
        # Agent handled empathy 1 at turn 18 (3 turns after outburst) with refusal
        ("Agent", "I am truly sorry to hear that, Sorcha. Losing a twelve-thousand-pound client tender due to Wi-Fi drops is completely heartbreaking. While our engineering policy does not permit dispatching an onsite technician this evening to run external cabling, I will make sure we get a high-performance mesh pod dispatched immediately and set up so your client calls are rock-solid.", None),
        ("Customer", "Thank you Liam, that reassurance means a lot.", 12.4),
        ("Agent", "Obviously thick masonry and foil-backed insulation block high-frequency radio waves, so physical backhaul solves the issue permanently.", None),
        ("Customer", "Yes, the garage walls have heavy foil insulation.", 14.2),
        # Outburst 2 at turn 22 in middle third (handled)
        ("Customer", "Sorcha speaking, I have another critical presentation on Monday morning with the regional planning board! If this mesh pod doesn't arrive before Monday and work flawlessly, the planning board will reject our planning appeal and my client will sue me! I am under extreme pressure!", -68.4),
        # Agent handled empathy 2 at turn 23
        ("Agent", "I completely understand the high stakes and immense pressure of your Monday planning board appeal, Sorcha. To ensure you are fully protected, I am dispatching the mesh pod via Royal Mail Special Delivery Guaranteed by 1pm tomorrow, Friday, and I will include my direct desk extension so you can reach me if you need help plugging it in.", None),
        ("Customer", "Thank you so much Liam! Having it arrive tomorrow Friday gives me the whole weekend to set it up.", 32.4),
        ("Agent", "Once the pod arrives, simply plug one end of your garage Ethernet cable into the pod's LAN port and connect the power adapter.", None),
        ("Customer", "Does the pod use the exact same Wi-Fi network name and password as the house?", 22.4),
        ("Agent", "Yes, it clones your Hub 5 SSID and security key automatically, enabling seamless device roaming.", None),
        ("Customer", "So my laptop will connect automatically without changing settings?", 28.4),
        ("Agent", "Exactly: your laptop will roam seamlessly to the garage pod with full gigabit throughput.", None),
        ("Customer", "That will make client video calls silky smooth.", 34.2),
        ("Agent", "I have waived the standard fifty-pound equipment and express delivery fee on your account.", None),
        ("Customer", "You waived the fee? Liam, you have been incredible!", 38.4),
        ("Agent", "Your dispatch consignment number is POD-SPEC-99120-H.", None),
        ("Customer", "POD-SPEC-99120-H, noted down.", 32.4),
        ("Agent", "The parcel will arrive before 1pm tomorrow, Friday.", None),
        ("Customer", "I will look out for the postman tomorrow.", 28.4),
        ("Agent", "I have also noted your planning appeal deadline on your account record.", None),
        ("Customer", "Thank you for understanding how crucial this deadline is.", 34.2),
        ("Agent", "Our technical support team is available twenty-four seven should you have any questions over the weekend.", None),
        ("Customer", "That provides total peace of mind.", 36.2),
        ("Agent", "We want to ensure your architectural consultancy thrives, Sorcha.", None),
        ("Customer", "You have completely restored my confidence today.", 38.4),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before we finish up, what was that Harrogate postal address again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start of our call, it is 22 Millfield Crescent, Harrogate.", -8.4),
        ("Agent", "Thank you Sorcha, the delivery address is confirmed for tomorrow's dispatch.", None),
        ("Customer", "Thank you again Liam for your amazing help today.", 34.2),
        ("Agent", "It has been an absolute pleasure assisting you, Sorcha. Best of luck with your planning board presentation on Monday.", None),
        ("Customer", "Thank you Liam, goodbye.", 30.2),
        ("Agent", "Is there any other broadband query I can assist you with today, Sorcha?", None),
        ("Customer", "No Liam, you have resolved everything perfectly.", 28.4),
        ("Agent", "Thank you for calling S-Net broadband technical support, Sorcha. Goodbye.", None),
        ("Customer", "Goodbye Liam.", 26.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 22.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 18.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 14.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 10.0)
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
        "Active listening": "Asked customer at turn 41 for postal address which was already provided at turn 3.",
        "Confirmed the issue is resolved": "Wi-Fi pod dispatched via postal delivery; resolution cannot be confirmed until hardware arrives and is installed."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net broadband technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Sorcha throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent handled two separate customer outbursts with profound empathy at turns 16 and 22, and no unhandled outbursts occurred.",
        "Paraphrasing": "Agent accurately paraphrased the Wi-Fi attenuation into detached garage office at turn 2.",
        "Active listening": "Agent asked for postal address at turn 42 despite customer stating 22 Millfield Crescent at turn 3.",
        "Took ownership of the problem": "Agent arranged express Friday delivery for mesh pod, waived £50 fee, and provided direct instructions.",
        "Build rapport and observed professionalism": "Agent maintained an encouraging, highly professional, and supportive demeanor throughout.",
        "Probing": "Agent probed about hub model, garden distance, and Ethernet cable availability.",
        "Confirmed the issue is resolved": "Resolution is contingent upon tomorrow's physical delivery and setup of the mesh pod, unverified on call."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 43, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 2},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 20}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 15, "agent_turn": 18, "with_refusal": True},
            {"kind": "handled", "customer_turn": 22, "agent_turn": 23, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_087",
        "cname": "Sorcha",
        "target_dur": 825,
        "scenario": "Wi-Fi signal unable to penetrate detached garage studio; mesh pod dispatched express with fee waived; two handled outbursts",
        "tier": "good",
        "expected_score": 83.3,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Confirmed the issue is resolved"],
        "notes": "Good call featuring two handled customer outbursts, express hardware dispatch, fee waiver, active listening repeat, and pending resolution."
    }

print("get_call_087 defined.")

# =========================================================================
# Call 088: Stefan, Mobile eSIM transfer timing out on new handset, 16:20 (980s)
# 4-5 faults (okay), score 45.0, Dead Air FAIL, Verified FAIL, Personalized FAIL, Probing FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_088():
    raw = [
        ("Agent", "Thank you for calling S-Net mobile technical services, my name is Rachel. How can I help you today?", None),
        ("Customer", "Hello Rachel, my name is Stefan Varga. I bought a new iPhone 15 and I am attempting to transfer my existing S-Net mobile eSIM from my old iPhone 12, but every time I scan the QR code or initiate the quick transfer, the screen spins for ten minutes and times out with error code SIM-ERR-503!", -34.8),
        # Paraphrasing PASS: restatement
        ("Agent", "Good afternoon. If I understand correctly, your mobile eSIM transfer between your old iPhone 12 and your new iPhone 15 is timing out after ten minutes with error code SIM-ERR-503. Let me inspect your mobile subscriber profile.", None),
        # Verified FAIL: agent asks only for mobile number, omitting PIN/address
        ("Customer", "My mobile number is 07700 900742, account reference SN-449102, registered at 45 Victoria Road, Swindon, SN1 3BD, security PIN 9021.", -5.2),
        # Personalized FAIL: agent never uses "Stefan" anywhere in the call
        ("Agent", "Thank you, that brings up the mobile line.", None),
        ("Customer", "Why is the eSIM transfer timing out?", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query the GSMA eSIM subscription manager server?", None),
        ("Agent", "Thank you for holding. The subscription manager server indicates that the cryptographic eSIM profile is still locked to the EID chip on your old iPhone 12.", None),
        ("Customer", "How do we unlock the profile from the old phone?", -10.4),
        ("Agent", "The previous eSIM profile must be deleted from the old handset, and a brand new SM-DP+ activation code must be generated for the new EID.", None),
        ("Customer", "I deleted the mobile plan from the old iPhone 12 settings just now.", 2.4),
        ("Agent", "I am generating a fresh eSIM profile for your new device.", None),
        ("Customer", "How will I receive the new eSIM profile?", 6.2),
        # Turn 14 is dead air gap 1 (40s)
        ("Customer", "Rachel? Are you there? The line was silent for forty seconds!", -28.4),
        ("Agent", "I was waiting for the GSMA carrier gateway to sign the security certificate.", None),
        ("Customer", "Will the QR code be emailed to me?", -14.2),
        ("Agent", "Obviously carrier eSIM certificates require cryptographic signing before dispatch.", None),
        ("Customer", "Right, I understand security signing is necessary.", -8.2),
        ("Agent", "The new eSIM activation QR code has been emailed to your registered email address.", None),
        ("Customer", "Let me check my email... Yes, email received from S-Net with subject 'Your New S-Net eSIM Activation Code'.", 8.4),
        # Outburst at turn 21 in middle third (handled)
        ("Customer", "I run an emergency heating and plumbing callout service during the winter months, and all our customer breakdown calls are routed directly to this mobile phone number! While this eSIM is stuck, my business is losing hundreds of pounds every single hour and vulnerable elderly residents with broken boilers cannot reach me in freezing temperatures! I am in absolute distress and panic over this outage!", -72.4),
        # Agent handled empathy at turn 22
        ("Agent", "I completely understand the acute distress, financial loss, and severe worry you are experiencing, especially with elderly residents facing broken boilers in freezing temperatures and relying on your emergency heating callouts. Getting your mobile phone back online immediately is an absolute priority, and I will stay on the line to walk you through scanning the QR code right now.", None),
        ("Customer", "Thank you Rachel, let's scan the code now.", 4.2),
        ("Agent", "On your new iPhone 15, open Settings, tap Mobile Service, and tap 'Set Up Mobile Service' or 'Add eSIM'.", None),
        ("Customer", "Tapping 'Add eSIM'... Camera scanner opened... Scanning QR code from my computer screen...", 14.2),
        ("Agent", "The screen should display 'Activating eSIM' and connect to the S-Net carrier profile.", None),
        ("Customer", "The screen says 'Activating...' with a spinning wheel.", 18.4),
        ("Agent", "The new profile is attaching to your device's EID chip.", None),
        ("Customer", "It has been spinning for two minutes now... Is that normal?", 12.2),
        ("Agent", "Network provisioning across the cellular towers can take between thirty minutes and up to four hours to fully propagate.", None),
        ("Customer", "So the phone won't receive incoming calls right away?", -14.2),
        ("Agent", "Correct, the cellular network requires the provisioning cycle to complete before signal bars appear.", None),
        ("Customer", "Can you divert incoming calls to a temporary landline number while it provisions?", 4.2),
        ("Agent", "Yes, I can set up an immediate network call divert to any UK landline or mobile.", None),
        ("Customer", "Please divert all calls to my workshop landline 01793 521890.", 14.2),
        # Turn 34 is dead air gap 2 (40s)
        ("Customer", "Hello? Rachel? Did the call drop? Why does your line keep going silent?", -28.2),
        ("Agent", "I was entering the network diversion parameters into our switch.", None),
        ("Customer", "Is the divert active?", -8.4),
        ("Agent", "Yes, immediate network call diversion to 01793 521890 is fully active.", None),
        ("Customer", "That will protect my emergency boiler breakdown customers while the eSIM completes.", 22.4),
        ("Agent", "Once the eSIM displays signal bars, you can cancel the divert by dialing hash hash 21 hash.", None),
        ("Customer", "Hash hash 21 hash, noted down.", 26.2),
        ("Agent", "I have waived the eSIM replacement charge on your account.", None),
        ("Customer", "Thank you, I appreciate that.", 24.2),
        # Turn 42: Active listening repeat in last third
        ("Agent", "Before we conclude, what was that mobile phone number again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start of our call, it is 07700 900742.", -12.4),
        ("Agent", "Thank you, mobile number confirmed on the ticket.", None),
        ("Customer", "Thank you for setting up the divert so quickly.", 22.4),
        ("Agent", "It has been my pleasure assisting. Stay warm.", None),
        ("Customer", "Goodbye Rachel.", 20.0),
        ("Agent", "Is there any other mobile issue today?", None),
        ("Customer", "No, goodbye.", 18.0),
        ("Agent", "Thank you for calling S-Net mobile technical services. Goodbye.", None),
        ("Customer", "Goodbye.", 14.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
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
        "Personalized the call/ticket appropriately": "FAIL",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "PASS",
        "Active listening": "FAIL",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "FAIL",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Hold time and Dead Air": "Dead Air Breach: Agent had 2 occurrences of >30s unmanaged dead air.",
        "Verified customer": "Agent failed to ask for a PIN, address, or security question within the first 4 minutes of the call.",
        "Personalized the call/ticket appropriately": "Agent failed to address customer by name 'Stefan' during the call.",
        "Active listening": "Asked customer at turn 44 for mobile number which was already provided at turn 3.",
        "Probing": "Failed to probe about error details or device OS version.",
        "Confirmed the issue is resolved": "eSIM provisioning was in progress with up to 4 hours propagation delay; resolution unconfirmed on call."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net mobile technical services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Agent allowed two separate unmanaged dead air gaps of 40 seconds at turns 14 and 33.",
        "Verified customer": "Agent failed to ask for address or security PIN during verification.",
        "Personalized the call/ticket appropriately": "Agent never addressed customer as Stefan throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand the acute distress, financial loss, and severe worry you are experiencing...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased the eSIM activation timeout issue at turn 2.",
        "Active listening": "Agent asked for mobile number at turn 44 despite customer stating 07700 900742 at turn 3.",
        "Took ownership of the problem": "Agent generated new QR code, guided setup, implemented immediate network call divert, and waived fee.",
        "Build rapport and observed professionalism": "Agent maintained polite, helpful, and professional tone throughout.",
        "Probing": "Agent failed to probe regarding error code 503 diagnostics.",
        "Confirmed the issue is resolved": "eSIM activation required 30 minutes to 4 hours to propagate; resolution unverified on call despite divert workaround."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 44, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 2},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 16}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 20, "agent_turn": 21, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_088",
        "cname": "Stefan",
        "target_dur": 980,
        "scenario": "Mobile eSIM transfer timing out on new iPhone 15; network divert workaround established; 4-5 faults (okay)",
        "tier": "okay",
        "expected_score": 45.0,
        "dead_air_indices": [14, 33],
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Confirmed the issue is resolved", "Verified customer", "Personalized the call/ticket appropriately", "Probing"],
        "notes": "Okay call featuring dead air breaches, failed verification and personalization, handled empathy in middle third, call divert workaround, and pending eSIM activation."
    }

print("get_call_088 defined.")

# =========================================================================
# Call 089: Tabitha, TV Catch-up BBC iPlayer continuous buffering on 4K streams, 11:15 (675s)
# 0 faults (excellent), score 100.0, All PASS
# Features TWO handled outbursts (turn 15 handled, turn 21 handled)
# =========================================================================
def get_call_089():
    raw = [
        ("Agent", "Thank you for calling S-Net TV technical support, my name is Edward. How can I help you today?", None),
        ("Customer", "Hello Edward, my name is Tabitha Jenkins. We have an S-Net TV 4K box, and whenever we try to watch high-definition or UHD 4K programs on BBC iPlayer catch-up, the video constantly freezes and displays a spinning purple circle every thirty seconds while audio keeps playing out of sync!", -34.8),
        ("Agent", "Good afternoon Tabitha. If I understand correctly, your TV 4K box experiences continuous video buffering and audio desynchronization every thirty seconds specifically when streaming UHD 4K content on BBC iPlayer catch-up. Before we inspect your set-top box video buffer telemetry, could you please confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 12 Church Lane, Winchester, SO23 9JN, security PIN 4108.", -5.2),
        ("Agent", "Thank you Tabitha, that confirms your account details. What video resolution setting is your TV box currently outputting?", None),
        ("Customer", "It is set to Automatic 2160p UHD resolution connected via a high-speed HDMI cable.", -12.4),
        ("Agent", "Could I place you on hold for two minutes while I query your set-top box hardware decoder telemetry and local cache registers?", None),
        ("Agent", "Thank you for holding, Tabitha. The decoder diagnostics show that the BBC iPlayer application cache on your TV box has accumulated 4.2 gigabytes of fragmented temporary video segment manifests.", None),
        ("Customer", "Why would fragmented temporary video segment manifests cause buffering?", -8.2),
        ("Agent", "When the local flash memory cache fills up, the hardware video buffer struggles to allocate contiguous memory blocks for UHD 4K video frames.", None),
        ("Customer", "Can we clear the application cache on the TV box?", 4.2),
        ("Agent", "Yes, we can perform a remote application cache purge and video hardware buffer reset right now.", None),
        ("Customer", "Will that erase my saved TV recordings or profile settings?", -10.2),
        ("Agent", "Not at all: recordings and user profiles are stored in protected non-volatile partitions; only temporary streaming app cache is purged.", None),
        ("Customer", "That is a huge relief.", 12.2),
        # Outburst 1 at turn 15 (handled)
        ("Customer", "Tabitha speaking, my husband and I are hosting a golden wedding anniversary celebration for my parents tonight, and we have sixty family members arriving at seven o'clock to watch a special commemorative BBC documentary about my father's naval career! If the television buffers and glitches in front of sixty guests, my parents will be devastated and I will die of humiliation! I am completely stressed out!", -68.4),
        # Agent handled empathy 1 at turn 16
        ("Agent", "I completely understand how immensely important your parents' golden wedding anniversary is, Tabitha, and having sixty family members arriving tonight to celebrate your father's naval career makes this an absolute top priority. I will ensure this buffering issue is completely resolved and thoroughly tested right now so tonight's screening runs flawlessly.", None),
        ("Customer", "Thank you Edward, that brings me so much comfort.", 14.2),
        ("Agent", "I am sending the cache purge signal directly to your TV box now.", None),
        ("Agent", "Obviously 4K UHD video streams demand flawless memory management to maintain forty megabits per second throughput.", None),
        ("Customer", "The TV screen blinked blue for three seconds and the S-Net TV main menu reloaded.", 22.4),
        # Outburst 2 at turn 21 in middle third (handled)
        ("Customer", "Tabitha speaking, my father is eighty-two years old and in frail health, and this anniversary screening is the last time all his former naval comrades will gather together in our home! If this documentary fails to stream tonight, there will never be another chance! I am on the verge of tears!", -74.2),
        # Agent handled empathy 2 at turn 22
        ("Agent", "I completely understand the profound emotional importance and once-in-a-lifetime significance of this gathering for your eighty-two-year-old father and his naval comrades, Tabitha. We will not let anything spoil this cherished celebration for your family. Let us open BBC iPlayer together right now and test the 4K stream live.", None),
        ("Customer", "Opening BBC iPlayer on the TV box now...", 18.4),
        ("Agent", "Navigate to any UHD 4K documentary and press Play.", None),
        ("Customer", "Selecting 'Wild Isles 4K UHD'... Pressing play... Edward! The picture loaded in crisp, crystal-clear 4K immediately! Zero buffering!", 36.8),
        ("Agent", "Fantastic! Let it play for sixty seconds while we monitor the live hardware decoder buffer telemetry.", None),
        ("Customer", "It has played for a full minute: not a single pause, jitter, or audio sync glitch! The colors are gorgeous!", 38.4),
        ("Agent", "Looking at our telemetry console, your TV box buffer is holding a solid thirty seconds of pre-fetched UHD video with 0% dropped frames.", None),
        ("Customer", "Now let me search for my father's naval documentary: 'The Royal Navy at Sea'...", 32.4),
        ("Agent", "Press play on the naval documentary to be one hundred percent certain.", None),
        ("Customer", "Playing naval documentary... Edward, it started instantly! The sound of the brass band is roaring with zero lag!", 39.2),
        ("Agent", "That confirms full hardware video decoding and streaming performance completely restored.", None),
        ("Customer", "You have saved our family celebration tonight, Edward.", 38.4),
        ("Agent", "I have locked the iPlayer buffer allocation to high-priority mode in your box firmware.", None),
        ("Customer", "That will keep it running smoothly for all future catch-up programs.", 34.2),
        ("Agent", "I have logged the diagnostic purge under ticket reference TV-4K-88192-W.", None),
        ("Customer", "TV-4K-88192-W, noted down.", 30.2),
        ("Agent", "Please give my heartfelt congratulations to your parents on their golden wedding anniversary, Tabitha.", None),
        ("Customer", "I will tell them how wonderfully you helped us today.", 36.2),
        ("Agent", "Our team is honored to play a small part in making their celebration special.", None),
        ("Customer", "I can breathe now and finish preparing the food for our guests.", 34.8),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just making sure our premises records match perfectly: that was 12 Church Lane, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, 12 Church Lane, Winchester.", 32.4),
        ("Agent", "Thank you Tabitha, premises and equipment records are fully verified.", None),
        ("Customer", "Thank you again Edward for your brilliant support.", 36.2),
        ("Agent", "It has been an absolute pleasure assisting you, Tabitha. Have a magnificent celebration tonight.", None),
        ("Customer", "Have a wonderful afternoon, Edward.", 32.4),
        ("Agent", "Is there any other TV or broadband issue I can assist you with today, Tabitha?", None),
        ("Customer", "No Edward, everything is working flawlessly.", 30.2),
        ("Agent", "Thank you for calling S-Net TV technical support, Tabitha. Goodbye.", None),
        ("Customer", "Goodbye Edward.", 28.4),
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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net TV technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Tabitha throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent handled two separate emotional outbursts with profound empathy and reassurance at turns 16 and 22, and no unhandled outbursts occurred.",
        "Paraphrasing": "Agent accurately paraphrased the 4K iPlayer buffering and desynchronization issue at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer address at turn 42.",
        "Took ownership of the problem": "Agent purged application cache, reset hardware video buffer, locked high-priority mode, and guided live verification.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, warm, and highly professional demeanor throughout.",
        "Probing": "Agent probed about video resolution settings and HDMI cabling.",
        "Confirmed the issue is resolved": "Customer tested 4K streaming and the exact naval documentary live on call with zero buffering and perfect sync."
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
            {"kind": "handled", "customer_turn": 15, "agent_turn": 16, "with_refusal": False},
            {"kind": "handled", "customer_turn": 21, "agent_turn": 22, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_089",
        "cname": "Tabitha",
        "target_dur": 675,
        "scenario": "TV 4K box BBC iPlayer catch-up UHD video buffering and audio desynchronization; resolved via remote app cache purge and buffer reset; two handled outbursts",
        "tier": "excellent",
        "expected_score": 100.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": [],
        "notes": "Flawless call featuring two handled outbursts with deep empathy, remote cache purge, harmless recheck in the final third, and complete live resolution verification."
    }

print("get_call_089 defined.")

# =========================================================================
# Call 090: Talia, Broadband speed fluctuating wildly between 2 Mbps and 500 Mbps, 19:10 (1150s)
# 1-2 faults (good), score 83.3, Active listening FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_090():
    raw = [
        ("Agent", "Thank you for calling S-Net broadband technical operations, my name is Oscar. How can I help you today?", None),
        ("Customer", "Hello Oscar, my name is Talia Brooks. We pay for your Ultrafast 500 Mbps fiber broadband, but over the past week our connection has been fluctuating wildly: one minute it tests at 480 Mbps and the next minute it plunges to 2 Mbps, dropping my work Zoom meetings and making remote working impossible!", -34.8),
        ("Agent", "Good afternoon Talia. If I understand correctly, your Ultrafast 500 Mbps broadband is experiencing severe speed instability, fluctuating dramatically between 480 Mbps and 2 Mbps and causing continuous drops during your remote video meetings. Before we inspect your optical network terminal and line telemetry, could you please confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 18 Hawthorne Road, Cheltenham, GL50 2DN, security PIN 6592, router model S-Net Hub 5.", -5.2),
        ("Agent", "Thank you Talia, that confirms your account details. Have you noticed if the speed drops occur at specific times of day or when certain household devices connect?", None),
        ("Customer", "It happens completely randomly throughout the day, even when only a single laptop is connected via Ethernet cable.", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query your Optical Network Terminal optical power levels and continuous packet error telemetry?", None),
        ("Agent", "Thank you for holding, Talia. Examining the optical line telemetry, your downstream optical receive power fluctuates between minus 16 dBm and minus 29 dBm.", None),
        ("Customer", "What does a fluctuation to minus 29 dBm indicate?", -10.4),
        ("Agent", "The optimal optical window is minus 15 to minus 22 dBm; when the signal drops to minus 29 dBm, the light level is near total optical extinction, causing massive frame drop and speed collapse.", None),
        ("Customer", "What would cause the optical light level to swing so wildly?", -8.2),
        ("Agent", "It typically indicates a contaminated fiber optical connector or a micro-bend stress fracture on the external drop cable between the telegraph pole and your house.", None),
        ("Customer", "Can you clean or repair the optical cable remotely?", -4.2),
        ("Agent", "Physical optical light fluctuations require an Openreach specialized fiber field engineer to clean the SC/APC bulkhead connector and re-splice the fiber joint.", None),
        ("Customer", "How quickly can a fiber engineer attend our property?", 2.4),
        ("Agent", "I can book a priority Openreach fiber repair engineer for tomorrow morning between eight and one o'clock.", None),
        ("Customer", "Tomorrow morning would be fantastic.", 8.4),
        ("Agent", "Obviously physical optical light loss requires precision laser re-splicing equipment that cannot be fixed by software reboots.", None),
        ("Customer", "I understand that hardware light levels require physical attention.", 12.2),
        ("Agent", "In the meantime, I can optimize your Hub 5 downstream channel bonding to stabilize the packets as much as possible.", None),
        ("Customer", "Please do that right away.", 14.2),
        # Outburst at turn 20 in middle third (handled - late acknowledgement 3 turns after)
        ("Customer", "Talia speaking, I am the lead legal counsel for a major medical device corporation, and tomorrow afternoon at two o'clock I am chairing a critical transatlantic patent litigation hearing with international judges and opposing QC barristers! If my internet collapses during that hearing, our multimillion-pound medical patent could be invalidated and my professional career will be permanently ruined! I am in complete sheer panic and anxiety!", -78.4),
        ("Agent", "I am querying the optical power levels and Openreach emergency dispatch slots right now.", None),
        ("Customer", "Please do Oscar, my transatlantic patent hearing is at two o'clock tomorrow.", 14.2),
        # Agent handled empathy at turn 23 (3 turns after outburst) with refusal
        ("Agent", "I completely understand the immense pressure, acute professional anxiety, and enormous career stakes of your transatlantic patent hearing tomorrow afternoon, Talia. While our engineering SLA cannot guarantee an on-site fiber laser repair engineer this evening, I will book the earliest first-slot engineer appointment for tomorrow morning at eight o'clock and dispatch our emergency 4G mobile broadband backup dongle so you have guaranteed dual-path connectivity before two o'clock.", None),
        ("Customer", "Thank you Oscar! Having the engineer at eight in the morning and a 4G backup dongle gives me complete safety.", 28.4),
        ("Agent", "I am booking the Openreach engineer slot under priority reference FBR-ENG-44910-C.", None),
        ("Customer", "FBR-ENG-44910-C, noted down.", 22.4),
        ("Agent", "The engineer will arrive between 8:00 AM and 10:00 AM and has notes to test both the external splice and the internal ONT connector.", None),
        ("Customer", "That will give them plenty of time before my two o'clock hearing.", 28.4),
        ("Agent", "I have also arranged for our local courier to deliver an S-Net 4G Mobile Backup USB Dongle to your door by 11:00 AM tomorrow.", None),
        ("Customer", "A courier delivery by 11:00 AM? Oscar, that is exceptional service!", 36.2),
        ("Agent", "The dongle plugs directly into the rear USB port of your Hub 5 and provides automatic instantaneous cellular failover.", None),
        ("Customer", "So even if the fiber drops for a second, the 4G takes over without disconnecting Zoom?", 32.4),
        ("Agent", "Exactly: the Hub 5 maintains stateful TCP sessions across the 4G tunnel without dropping active video calls.", None),
        ("Customer", "That is an extraordinary relief. I can sleep peacefully tonight.", 38.4),
        ("Agent", "I have waived all engineering callout charges and courier delivery fees on your account.", None),
        ("Customer", "Thank you Oscar, you have gone above and beyond.", 36.8),
        ("Agent", "I have documented your legal hearing deadline on the master incident log.", None),
        ("Customer", "Thank you for taking my situation so seriously.", 32.4),
        ("Agent", "Our priority is ensuring our customers can work with complete confidence.", None),
        ("Customer", "You have restored my faith in S-Net today.", 34.2),
        ("Agent", "Best of luck with your patent litigation hearing tomorrow afternoon, Talia.", None),
        ("Customer", "Thank you so much Oscar.", 32.0),
        # Turn 42: Active listening repeat in last third
        ("Agent", "Before we conclude, what was that Cheltenham postal address again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start of our call, it is 18 Hawthorne Road, Cheltenham.", -10.2),
        ("Agent", "Thank you Talia, the address is verified on the engineer job sheet.", None),
        ("Customer", "Thank you again Oscar for your compassionate and urgent help.", 34.2),
        ("Agent", "It has been my pleasure assisting you, Talia. Have a wonderful evening.", None),
        ("Customer", "Goodbye Oscar.", 30.2),
        ("Agent", "Is there any other broadband technical issue I can assist with today, Talia?", None),
        ("Customer", "No Oscar, that covers everything.", 28.0),
        ("Agent", "Thank you for calling S-Net broadband technical operations, Talia. Goodbye.", None),
        ("Customer", "Goodbye Oscar.", 26.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 22.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 18.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 14.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 10.0)
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
        "Active listening": "Asked customer at turn 44 for postal address which was already provided at turn 3.",
        "Confirmed the issue is resolved": "Physical fiber repair engineer booked for tomorrow morning; issue remains unresolved on call."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net broadband technical operations' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Talia throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated deep empathy and understanding at turn 22 regarding customer's transatlantic patent hearing, and no unhandled outbursts occurred.",
        "Paraphrasing": "Agent accurately paraphrased the broadband speed fluctuation issue at turn 2.",
        "Active listening": "Agent asked for postal address at turn 44 despite customer stating 18 Hawthorne Road at turn 3.",
        "Took ownership of the problem": "Agent booked priority 8am Openreach engineer, arranged courier 4G backup dongle, and waived fees.",
        "Build rapport and observed professionalism": "Agent maintained an exceptionally professional, supportive, and reassuring tone throughout.",
        "Probing": "Agent probed about timing patterns and Ethernet testing.",
        "Confirmed the issue is resolved": "Physical optical fault requires tomorrow morning's engineering visit and repair; unverified on call."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 44, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 2},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 17}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 21, "agent_turn": 24, "with_refusal": True}
        ]
    }

    return {
        "cid": "agt_090",
        "cname": "Talia",
        "target_dur": 1150,
        "scenario": "Ultrafast fiber broadband fluctuating wildly between 2 Mbps and 500 Mbps due to optical light extinction; 8am priority engineer and courier 4G backup booked",
        "tier": "good",
        "expected_score": 83.3,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Confirmed the issue is resolved"],
        "notes": "Good call featuring deep empathy in middle third, emergency engineer and courier 4G dongle booking, fee waiver, active listening repeat, and pending resolution."
    }

print("get_call_090 defined.")

if __name__ == "__main__":
    for fn in [get_call_086, get_call_087, get_call_088, get_call_089, get_call_090]:
        c = fn()
        compile_call(c)
