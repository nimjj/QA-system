import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from batch_engine import compile_call

# =========================================================================
# Call 076: Philip, TV box error CS-201 'Subscription Required' on sports, 10:40 (640s)
# 3-4 faults (okay), score 66.7, Branding FAIL, Dead Air FAIL, Rapport FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_076():
    raw = [
        # Branding FAIL: Missing standard greeting
        ("Agent", "S-Net TV digital services, my name is Gary.", None),
        ("Customer", "Hello Gary, my name is Philip Vance. I pay thirty pounds a month for your S-Net Sports HD package, but our TV set-top box is blocking all four sports channels with an on-screen error CS-201 saying 'Subscription Required - Contact Customer Care', even though the package is active on my online account!", -34.8),
        ("Agent", "Good afternoon Philip. If I understand correctly, your TV set-top box is blocking all your sports channels with error CS-201 stating a subscription is required, despite your package being fully active. Before we query your card entitlements, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 19 Crescent Road, Sheffield, S7 1HN, security PIN 4419, smartcard ID SN-TV-881902.", -5.2),
        ("Agent", "Thank you Philip, that confirms your account details. Have you tried power-cycling the TV set-top box from the wall socket for thirty seconds?", None),
        ("Customer", "I rebooted the box three times this morning and rescanned for channels; every other channel works, but the sports channels display error CS-201!", -22.4),
        ("Agent", "Could I place you on hold for two minutes while I query your subscription entitlement pairing on the conditional access gateway?", None),
        ("Agent", "Thank you for holding, Philip. The conditional access gateway indicates that your sports package digital tier encryption key has expired.", None),
        ("Customer", "Why would our encryption key expire when our monthly direct debit is paid up to date?", -14.2),
        ("Agent", "Subscription tier encryption keys refresh automatically via satellite and fiber carousels once every thirty calendar days.", None),
        ("Customer", "Can you send an over-the-air entitlement refresh command to reactivate the keys right now?", -6.4),
        ("Agent", "If you leave your TV set-top box powered down at the wall plug overnight to save electricity, the box misses the automated overnight security refresh cycles.", None),
        ("Customer", "I turn off wall sockets at night to reduce our carbon footprint! Why are you blaming me for your software missing its refresh?!", -52.4),
        ("Agent", "I am stating the operational reality of encrypted broadcast conditional access systems.", None),
        ("Customer", "Will you transmit the manual entitlement refresh signal or not?!", -38.2),
        # Turn 14 is dead air gap 1 (40s)
        ("Agent", "Manual entitlement refresh commands can be dispatched across our broadband return path.", None),
        ("Customer", "Hello? Gary? Are you still on the phone? The line went completely silent for over thirty seconds!", -28.4),
        ("Agent", "I was authenticating the broadcast security certificate on the central multiplexer.", None),
        ("Customer", "Please send the activation command immediately.", -18.2),
        ("Agent", "Obviously encrypted broadcast video channels require valid cryptoperiod authorization blocks to decode high-definition streams.", None),
        ("Customer", "I know encryption requires authorization; I am asking you to transmit the keys!", -24.2),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Philip speaking, I have twenty friends arriving at my house in two hours for the North London derby match! I bought six hundred pounds worth of food and drinks for this gathering, and my sixty-five-inch screen is showing error CS-201! If my guests arrive and cannot watch the match after paying thirty pounds a month, I will look like an absolute fool and my weekend will be destroyed! I am furious and panicking!", -68.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand the intense panic and fury this is causing with twenty guests arriving for the derby match in two hours, Philip. Preparing a major gathering with friends only to see error CS-201 on the screen is extremely stressful, and I will force an immediate entitlement re-hit to restore your sports channels right now.", None),
        ("Customer", "Thank you Gary. How long does the re-hit take to clear error CS-201?", -14.2),
        ("Agent", "I am dispatching an emergency Tier-1 over-the-air entitlement signal directly to your smartcard ID SN-TV-881902.", None),
        ("Customer", "The TV screen just flashed black for two seconds and returned to error CS-201.", -16.4),
        ("Agent", "The conditional access subsystem takes between sixty and one hundred and twenty minutes to cycle through the cryptographic key rings.", None),
        ("Customer", "Sixty to one hundred and twenty minutes?! My guests arrive in one hundred and twenty minutes!", -48.2),
        ("Agent", "Cryptographic key cycles are governed by broadcast carousel frequency schedules.", None),
        ("Customer", "So we cannot verify right now while we are on this call whether the sports channels will actually turn on?!", -38.4),
        ("Agent", "Correct. The entitlement re-hit has been sent, but the channels will remain locked until the key ring cycle completes.", None),
        ("Customer", "Can I watch the match on the S-Net TV mobile app on my tablet as a temporary backup?", -18.2),
        ("Agent", "Yes, your online account credentials allow immediate live streaming on the S-Net TV mobile application.", None),
        ("Customer", "Let me check the mobile app on my phone... S-Net Sports 1 is streaming live on my phone right now!", 18.4),
        # Turn 34 is dead air gap 2 (40s)
        ("Customer", "Gary? Hello? Did the phone cut out again? Why does your line keep dropping into complete dead air?", -24.2),
        ("Agent", "I was documenting your mobile streaming workaround under case reference TV-SPORT-88192-V.", None),
        ("Customer", "TV-SPORT-88192-V, noted down.", 8.4),
        ("Agent", "You can cast the mobile stream from your tablet directly to your television via AirPlay or Chromecast if the box key cycle takes longer than expected.", None),
        ("Customer", "That provides a viable emergency backup if the TV box is still updating at kick-off.", 22.4),
        ("Agent", "I have also set an automated re-verification prompt on your set-top box profile.", None),
        ("Customer", "Thank you for that backup option, Gary.", 18.2),
        ("Agent", "Keep the TV box tuned to channel 501 without changing channels to allow the broadcast stream to deliver the key packets.", None),
        # Turn 42: Active listening harmless recheck in last third
        ("Agent", "Just ensuring our premises records match perfectly: that was 18 Westmorland Road, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, 18 Westmorland Road, Newcastle.", 18.4),
        ("Agent", "Thank you Philip, all premises and hardware records are fully synchronized.", None),
        ("Customer", "I will leave the TV on channel 501 and prepare the AirPlay casting just in case.", 18.4),
        ("Agent", "I have also applied a five-pound goodwill credit to your bill for the inconvenience.", None),
        ("Customer", "Thank you, that is appreciated.", 20.2),
        ("Agent", "Enjoy the derby match with your friends, Philip.", None),
        ("Customer", "Thank you Gary. Goodbye.", 16.2),
        ("Agent", "Is there any other aspect of your TV service I can assist with today?", None),
        ("Customer", "No, goodbye.", 14.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 10.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 6.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 2.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 0.0)
    ]

    ratings = {
        "Branding and Survey Check": "FAIL",
        "Hold time and Dead Air": "FAIL",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "PASS",
        "Active listening": "PASS",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Branding and Survey Check": "Failed standard opening and closing branding scripts.",
        "Hold time and Dead Air": "Dead Air Breach: Agent had 2 occurrences of >30s unmanaged dead air.",
        "Build rapport and observed professionalism": "Spoke rudely at turn 11 blaming customer for turning off wall sockets to save electricity.",
        "Confirmed the issue is resolved": "Failed to confirm resolution of TV box error CS-201 on call due to 1-2 hour key cycle delay."
    }

    evidence = {
        "Branding and Survey Check": "Agent failed standard opening branding ('S-Net TV digital services...') and closing branding.",
        "Hold time and Dead Air": "Agent allowed two separate unmanaged dead air gaps of 40 seconds at turns 14 and 34.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Philip throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand the intense panic and fury this is causing with twenty guests arriving for the derby match in two hours, Philip...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased sports subscription error CS-201.",
        "Active listening": "Agent completed harmless recheck of customer address at turn 42.",
        "Took ownership of the problem": "Agent dispatched entitlement re-hit, verified mobile streaming workaround, and provided goodwill credit.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you leave your TV set-top box powered down at the wall plug overnight to save electricity, the box misses the automated overnight security refresh cycles.'",
        "Probing": "Agent gathered details on error codes and reboot steps.",
        "Confirmed the issue is resolved": "TV box still displayed error CS-201 with customer advised to wait 1-2 hours for key ring propagation."
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
            {"kind": "rude", "agent_turn": 11},
            {"kind": "blunt_but_ok", "agent_turn": 19}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 21, "agent_turn": 22, "with_refusal": True}
        ]
    }

    return {
        "cid": "agt_076",
        "cname": "Philip",
        "target_dur": 640,
        "scenario": "TV box error CS-201 on subscribed sports channels; entitlement refresh sent but propagation prevents live confirmation",
        "tier": "okay",
        "expected_score": 66.7,
        "dead_air_indices": [14, 33],
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Branding and Survey Check", "Build rapport and observed professionalism", "Confirmed the issue is resolved"],
        "notes": "Okay call featuring failed branding, dead air breaches, rude accusations, unverified resolution due to key propagation delay, and handled empathy."
    }

print("get_call_076 defined.")

# =========================================================================
# Call 077: Rachel, Smart doorbell failing to reconnect after router auto-channel shift, 15:59 (959s)
# 1-2 faults (good), score 83.3, Active listening FAIL, Rapport FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_077():
    raw = [
        ("Agent", "Thank you for calling S-Net wireless technical support, my name is Craig. How can I help you today?", None),
        ("Customer", "Hello Craig, my name is Rachel Morgan. Our Ring smart video doorbell disconnected from our S-Net Hub 5 router two nights ago and will not reconnect: the doorbell app says 'Cannot Find Wi-Fi Network', even though all our smartphones and laptops connect to the router without any trouble!", -32.4),
        ("Agent", "Good afternoon Rachel. If I understand correctly, your smart video doorbell has dropped off your S-Net Hub 5 wireless network and fails to discover the Wi-Fi SSID, despite your other household devices connecting normally. Before we inspect your router's wireless telemetry, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 14 Richmond Crescent, Cardiff, CF24 3RN, security PIN 7701, router model S-Net Hub 5.", -5.2),
        ("Agent", "Thank you Rachel, that confirms your account details. Have you tried taking the doorbell off the front door bracket and holding it right next to the router?", None),
        ("Customer", "I brought the doorbell into the living room three feet from the hub, entered setup mode, and it still fails to see our network!", -22.4),
        ("Agent", "Could I place you on hold for two minutes while I query your router's 2.4 GHz channel assignment and beacon logs?", None),
        ("Agent", "Thank you for holding, Rachel. The router diagnostics indicate that our automated dynamic channel optimization feature shifted your 2.4 GHz radio from channel 6 to channel 13 during Wednesday's overnight interference scan.", None),
        ("Customer", "Why would shifting to channel 13 prevent our smart doorbell from seeing the Wi-Fi?", -14.2),
        ("Agent", "Many smart home IoT devices manufactured for global markets only support North American standard Wi-Fi channels 1 through 11, lacking hardware firmware support for European channels 12 and 13.", None),
        ("Customer", "Can you lock our S-Net Hub 5 to channel 1 or 6 so the doorbell can see the network again?", -6.4),
        ("Agent", "If you choose to purchase cheap imported smart home gadgets online that don't adhere to European telecommunications standards, you create compatibility headaches for yourself.", None),
        ("Customer", "It is an official Ring Video Doorbell bought from Currys in Cardiff! It is not a cheap grey import! Why are you insulting my home security equipment?!", -52.4),
        ("Agent", "I am stating the regulatory frequency differences between regional IEEE 802.11 specifications.", None),
        ("Customer", "Please disable the automatic channel shift and lock our 2.4 GHz radio to channel 1 right now.", -28.4),
        ("Agent", "I can disable dynamic channel hopping and fix your 2.4 GHz broadcast permanently on channel 1.", None),
        ("Customer", "Please push that configuration update to our hub.", -14.2),
        ("Agent", "I am transmitting the static channel 1 assignment command to your Hub 5 cloud profile.", None),
        ("Customer", "The light on the front of the router pulsed white for a moment and has returned to solid green.", 8.2),
        ("Agent", "Obviously legacy 2.4 GHz wireless devices require compatible broadcast beacon channels to negotiate WPA2 pre-shared keys.", None),
        ("Customer", "Right, I understand it cannot see channels outside 1 to 11.", 10.4),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Rachel speaking, I live alone on a ground floor flat in central Cardiff and I was the victim of a stalking incident two months ago! That smart video doorbell is my only early warning system when someone approaches my front door at night! Sitting here for two days without working front door security has left me terrified, unable to sleep, and jumping at every shadow! I need my security camera working tonight!", -68.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand the acute fear, vulnerability, and lack of sleep this has caused you, Rachel, especially following that terrifying stalking incident. Having your front door security camera knocked offline when you rely on it for your personal safety is completely unacceptable, and I will ensure your router is permanently configured to keep that doorbell connected.", None),
        ("Customer", "Thank you Craig, you have no idea how much of a relief it is to hear you understand.", -4.2),
        ("Agent", "Channel 1 is now locked as the permanent frequency on your 2.4 GHz radio with dynamic hopping permanently disabled.", None),
        ("Customer", "Let me press the orange setup button on the back of the Ring doorbell... It says 'Entering Setup Mode'.", 6.2),
        ("Agent", "Open the Ring application on your phone and tap 'Join Network'.", None),
        ("Customer", "Looking at the network list in the app... Craig! Our home Wi-Fi network 'S-Net-Morgan' appeared in the list instantly!", 24.5),
        ("Agent", "Please select 'S-Net-Morgan' and enter your Wi-Fi password.", None),
        ("Customer", "Entering password... The doorbell spun white... but now it flashed red three times and gave a voice prompt saying: 'Battery critically low, shutting down'!", -22.4),
        ("Agent", "The internal rechargeable lithium-ion battery has fully depleted after forty-eight hours of continuous network searching.", None),
        ("Customer", "Oh no! So the doorbell died because it spent two days searching for channel 13?!", -18.2),
        ("Agent", "Yes, when IoT devices lose network synchronization, the continuous RF beacon searching drains the battery rapidly.", None),
        ("Customer", "How long does the battery take to charge before I can mount it back on the door?", -12.4),
        ("Agent", "A standard micro-USB charge on that model requires approximately six to eight hours to reach full operating capacity.", None),
        ("Customer", "So we cannot complete the final live video streaming verification while we are on this call?", -16.2),
        ("Agent", "Correct, the battery must charge before the camera can power its Wi-Fi transmitter.", None),
        ("Customer", "I have plugged the battery into the wall charger right now; the amber charging LED is illuminated.", 8.4),
        ("Agent", "Once the battery shows a solid green light in six hours, sliding it back into the doorbell will connect automatically to channel 1.", None),
        ("Customer", "And because channel 1 is permanently locked, it won't drop off the network again?", 14.2),
        ("Agent", "Yes, dynamic auto-channel hopping is permanently disabled on your profile.", None),
        ("Customer", "I have documented the channel lock in my notes.", 16.4),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before we conclude, what model smart doorbell was that again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start of our call, it is a Ring smart video doorbell.", -10.2),
        ("Agent", "Thank you Rachel, that completes the technical documentation under case reference SEC-RING-88192-M.", None),
        ("Customer", "SEC-RING-88192-M, noted down.", 14.5),
        ("Agent", "If the doorbell does not connect automatically after charging tonight, our technical support line is available twenty-four hours a day.", None),
        ("Customer", "Thank you Craig, I will leave it to charge fully this afternoon.", 18.2),
        ("Agent", "Please stay safe, Rachel, and sleep well tonight once the camera is mounted.", None),
        ("Customer", "Thank you for your empathy and help, Craig.", 20.2),
        ("Agent", "Is there any other wireless query I can assist you with today, Rachel?", None),
        ("Customer", "No Craig, that covers everything.", 18.4),
        ("Agent", "Thank you for calling S-Net wireless technical support, Rachel. Have a safe and peaceful evening. Goodbye.", None),
        ("Customer", "Goodbye Craig.", 16.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 12.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 8.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 4.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 0.0)
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
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Active listening": "Asked customer at turn 42 for doorbell model which was already provided at turn 3.",
        "Build rapport and observed professionalism": "Spoke rudely at turn 11 blaming customer for purchasing cheap imported gadgets online.",
        "Confirmed the issue is resolved": "Failed to confirm camera streaming resolution on call due to depleted doorbell battery requiring 6-8 hours of charging."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net wireless technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Rachel throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand the acute fear, vulnerability, and lack of sleep this has caused you, Rachel...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased the smart doorbell Wi-Fi disconnection at turn 2.",
        "Active listening": "Agent asked for doorbell model at turn 42 despite customer stating Ring smart video doorbell at turn 3.",
        "Took ownership of the problem": "Agent identified channel 13 root cause, disabled dynamic hopping, and locked channel 1.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you choose to purchase cheap imported smart home gadgets online that don't adhere to European telecommunications standards, you create compatibility headaches for yourself.'",
        "Probing": "Agent probed about distance from router and setup mode behavior.",
        "Confirmed the issue is resolved": "Network appeared in app but doorbell battery died and required 6-8 hours charging, preventing live resolution verification."
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
        "cid": "agt_077",
        "cname": "Rachel",
        "target_dur": 959,
        "scenario": "Smart doorbell failing to reconnect after router auto-channel shift; channel locked to 1 but depleted battery prevents live verification",
        "tier": "good",
        "expected_score": 83.3,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Build rapport and observed professionalism", "Confirmed the issue is resolved"],
        "notes": "Good call where agent resolved channel 13 incompatibility with deep empathy in the middle third, failing rapport for rude remark and confirmed resolved due to depleted doorbell battery."
    }

print("get_call_077 defined.")

# =========================================================================
# Call 078: Reuben, Mobile voicemail greeting stuck on robot voice, 13:19 (799s)
# 5+ faults (poor), score 35.0, Branding FAIL, Dead Air FAIL, Verified FAIL, Personalized FAIL, Rapport FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_078():
    raw = [
        # Branding FAIL: Missing standard greeting
        ("Agent", "Voicemail support desk, agent 202.", None),
        ("Customer", "Hello, my name is Reuben Gallagher. I run a commercial plumbing and heating consultancy, and ever since S-Net upgraded its mobile voicemail system over the weekend, my professional business greeting has disappeared: callers now get a tinny synthesized robotic voice saying 'You have reached 07700 900882', which sounds completely unprofessional and makes clients think my business has closed down!", -34.8),
        # Verified FAIL: Agent fails to ask for PIN, address, or security question in the first 240s!
        # Personalized FAIL: Agent never addresses customer by name 'Reuben' anywhere!
        ("Agent", "I can inspect your cellular voicemail profile. What mobile telephone number is registered to this voicemail box?", None),
        ("Customer", "It is 07700 900882, registered to 12 Station Road, Carlisle, CA1 1RD, security PIN 3310.", -5.2),
        ("Agent", "Thank you, that brings up the voicemail account record. What happens when you dial 1571 to record a new custom greeting?", None),
        ("Customer", "I dial 1571, record my professional greeting, press hash to save, and the automated voice confirms 'Greeting saved successfully', but when anyone calls my mobile, it continues playing the robotic number greeting!", -22.4),
        ("Agent", "Could I place you on hold for two minutes while I query the central voicemail media server database?", None),
        ("Agent", "Thank you for holding. The media gateway indicates that your subscriber mailbox has a corrupted pointer record linking the subscriber profile to the audio storage partition.", None),
        ("Customer", "Can you repair that pointer record so the system plays the custom greeting I recorded?", -14.2),
        ("Agent", "Frontline representatives do not have access to edit raw database pointer records on the central media storage architecture.", None),
        ("Customer", "Then how do I get my professional business greeting to play for my customers?", -24.2),
        ("Agent", "If you run an independent commercial trade business, you should be subscribing to our business mobile plan rather than using a standard consumer retail SIM card.", None),
        ("Customer", "I have had this exact same number for seven years and paid you every month! Don't tell me what tariff I should buy when your system corrupted my greeting!", -52.4),
        ("Agent", "I am stating our service level agreement distinctions between consumer retail and business accounts.", None),
        ("Customer", "Can you escalate this to a database engineer who can fix the media pointer?", -34.2),
        # Turn 14 is dead air gap 1 (40s)
        ("Agent", "Database support escalations can be submitted through our server maintenance portal.", None),
        ("Customer", "Hello? Are you still there? The phone went completely dead for forty seconds!", -28.4),
        ("Agent", "I was accessing the regional telecommunications server maintenance queue.", None),
        ("Customer", "Can the server maintenance team fix the pointer today?", -22.4),
        ("Agent", "Obviously voicemail audio partitions operate on centralized distributed file systems that sync during scheduled maintenance windows.", None),
        ("Customer", "I need my business greeting working during trading hours, not in the middle of the night!", -32.4),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "I have lost two boiler installation contracts worth eight thousand pounds this morning because prospective clients called my number, heard that synthesized robot voice, and hung up thinking my company was a fraudulent shell operation! Eight thousand pounds of work lost because S-Net corrupted my voicemail! I am shaking with fury and facing financial disaster!", -68.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I understand how intensely furious and devastating it is to lose eight thousand pounds in client contracts this morning over a synthesized robot greeting, and the immense financial stress this has caused your trade business. Having prospective clients turn away because of a corrupted voicemail pointer is completely unacceptable, and I will submit an emergency server re-sync ticket immediately.", None),
        ("Customer", "Can they fix the pointer before the end of business today?", -18.2),
        ("Agent", "Server maintenance teams review database sync queues during our overnight batch cycle at two in the morning.", None),
        ("Customer", "So the robot voice will continue turning away clients for the rest of today?!", -44.2),
        ("Agent", "Yes, active database partition pointer corrections cannot be executed on live daytime server nodes.", None),
        ("Customer", "Is there any temporary workaround I can use so callers don't hear the robot?", -18.2),
        ("Agent", "You can disable voicemail call forwarding on your mobile handset by dialing hash hash zero zero two hash.", None),
        ("Customer", "What happens if I dial hash hash zero zero two hash?", 2.4),
        ("Agent", "Unanswered calls will ring out rather than diverting to the corrupted voicemail robot, allowing you to return missed calls from your call log.", None),
        ("Customer", "Dialing hash hash zero zero two hash now... Phone displays: 'All conditional call forwarding disabled'.", 12.2),
        ("Agent", "Callers will now hear standard ringing tones and will not be greeted by the robotic prompt.", None),
        ("Customer", "That is better than a robot telling them my number doesn't exist, but it doesn't solve my voicemail.", -8.2),
        # Turn 34 is dead air gap 2 (40s)
        ("Customer", "Hello? Did you disconnect? Why is there zero background sound on this call?", -24.2),
        ("Agent", "I was logging your server escalation under technical ticket VM-DB-88192-K.", None),
        ("Customer", "VM-DB-88192-K, noted down.", -4.2),
        ("Agent", "The overnight batch script will purge the corrupted pointer and rebuild your mailbox index at two in the morning.", None),
        ("Customer", "So tomorrow morning at eight o'clock, will my custom greeting play?", 6.2),
        ("Agent", "You will need to dial 1571 tomorrow morning and record your business greeting one more time to populate the fresh partition.", None),
        ("Customer", "I will re-record it at eight o'clock tomorrow.", 8.4),
        ("Agent", "I have documented your account notes with a priority audit flag.", None),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before I close this file, what was that mobile telephone number again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "Like I told you earlier, it is 07700 900882.", -12.4),
        ("Agent", "Thank you, the mobile number is attached to the ticket.", None),
        ("Customer", "I will test the voicemail tomorrow morning.", -6.2),
        ("Agent", "I have also applied a ten-pound goodwill credit to your mobile account.", None),
        ("Customer", "Thank you for the credit, but the priority is having a professional voicemail.", -8.4),
        ("Agent", "Is there any other cellular issue I can assist with today?", None),
        ("Customer", "No, that is all.", -10.2),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -8.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -6.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -4.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -2.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 0.0)
    ]

    ratings = {
        "Branding and Survey Check": "FAIL",
        "Hold time and Dead Air": "FAIL",
        "Verified customer": "FAIL",
        "Personalized the call/ticket appropriately": "FAIL",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "FAIL",
        "Active listening": "FAIL",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Branding and Survey Check": "Failed standard opening and closing branding scripts.",
        "Hold time and Dead Air": "Dead Air Breach: Agent had 2 occurrences of >30s unmanaged dead air.",
        "Verified customer": "Agent failed to ask for a PIN, address, or security question within the first 4 minutes of the call.",
        "Personalized the call/ticket appropriately": "Agent failed to use the customer's verified name 'Reuben' during the call.",
        "Paraphrasing": "Failed to paraphrase customer's corrupted voicemail greeting issue in own words.",
        "Active listening": "Asked customer at turn 42 for his mobile number which was already provided at turn 3.",
        "Build rapport and observed professionalism": "Spoke rudely at turn 11 blaming customer for using a consumer SIM card for trade business.",
        "Confirmed the issue is resolved": "Failed to resolve voicemail greeting on call; issue deferred to overnight batch processing."
    }

    evidence = {
        "Branding and Survey Check": "Agent failed standard opening branding ('Voicemail support desk...') and closing branding.",
        "Hold time and Dead Air": "Agent allowed two separate unmanaged dead air gaps of 40 seconds at turns 14 and 34.",
        "Verified customer": "Agent failed to ask for full postal address or security PIN during verification.",
        "Personalized the call/ticket appropriately": "Agent never addressed customer as Reuben anywhere in the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I understand how intensely furious and devastating it is to lose eight thousand pounds in client contracts this morning...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased the corrupted voicemail greeting issue.",
        "Active listening": "Agent asked for mobile number at turn 42 despite customer stating 07700 900882 at turn 3.",
        "Took ownership of the problem": "Agent provided ##002# forwarding disable workaround, logged database ticket, and applied goodwill credit.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you run an independent commercial trade business, you should be subscribing to our business mobile plan rather than using a standard consumer retail SIM card.'",
        "Probing": "Agent gathered details on 1571 greeting setup and symptoms.",
        "Confirmed the issue is resolved": "Voicemail greeting remained corrupted with customer advised to re-record after overnight batch processing."
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
        "cid": "agt_078",
        "cname": "Reuben",
        "target_dur": 799,
        "scenario": "Mobile voicemail greeting stuck on robot voice; 6 faults (poor)",
        "tier": "poor",
        "expected_score": 35.0,
        "dead_air_indices": [14, 33],
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Branding and Survey Check", "Build rapport and observed professionalism", "Confirmed the issue is resolved", "Verified customer", "Personalized the call/ticket appropriately"],
        "notes": "Poor call marked by failed branding, dead air breaches, failed verification, failed personalization, rude remarks, and unresolved voicemail greeting, alongside handled empathy."
    }

print("get_call_078 defined.")

# =========================================================================
# Call 079: Rhiannon, Hub 5 port forwarding rules disappearing after night reboot, 16:37 (997s)
# 0 faults (excellent), score 100.0, All PASS
# =========================================================================
def get_call_079():
    raw = [
        ("Agent", "Thank you for calling S-Net advanced technical support, my name is Gareth. How can I help you today?", None),
        ("Customer", "Hello Gareth, my name is Rhiannon Davies. Every single night around three in the morning when our S-Net Hub 5 performs its scheduled maintenance reboot, all custom port forwarding rules configured for our TrueNAS file server and security NVR disappear completely from the router's configuration table, severing remote access for our off-site backup servers!", -34.8),
        ("Agent", "Good afternoon Rhiannon. If I understand correctly, your S-Net Hub 5 is failing to retain custom port forwarding rules in non-volatile flash memory across scheduled overnight reboots, severing remote access to your TrueNAS server and security NVR. Before we inspect your router's NVRAM firmware registers, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 28 Cathedral Road, Cardiff, CF11 9LJ, security PIN 5541, customer account BB-881920.", -5.2),
        ("Agent", "Thank you Rhiannon, that confirms your account details. Have you configured static DHCP reservations for both the TrueNAS server and the security NVR on the local subnet?", None),
        ("Customer", "Yes, TrueNAS is statically mapped to 192.168.1.50 and the NVR is mapped to 192.168.1.60 with their MAC addresses bound in the router GUI.", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query your Hub 5 cloud configuration sync state and NVRAM commit logs?", None),
        ("Agent", "Thank you for holding, Rhiannon. The firmware telemetry confirms that while the web GUI accepts port forwarding rules, the local NVRAM commit daemon was encountering a write lock timeout against the TR-069 cloud provisioning profile.", None),
        ("Customer", "Why was the cloud provisioning profile creating a write lock timeout on local NVRAM?", -10.4),
        ("Agent", "When firmware version 4.12 was deployed, an unhandled concurrency bug caused the cloud TR-069 parameter sync to overwrite local firewall tables with the default empty profile upon reboot initialization.", None),
        ("Customer", "Can you patch the firmware or push an updated cloud profile that preserves local firewall rules?", 2.4),
        ("Agent", "Yes, we have released firmware maintenance patch version 4.12.3 which specifically fixes the TR-069 firewall table persistence synchronization.", None),
        ("Customer", "Can we flash firmware patch 4.12.3 to our Hub 5 right now?", 6.2),
        ("Agent", "I am pushing the firmware patch 4.12.3 image directly to your Hub 5 flash memory.", None),
        ("Customer", "The hub center light turned solid orange... now it is flashing cyan.", 12.2),
        ("Agent", "The flash memory write takes approximately ninety seconds to complete.", None),
        ("Customer", "The light has returned to solid green. Has the firmware update succeeded?", 18.4),
        ("Agent", "Firmware version 4.12.3 is now active with commit validation verified.", None),
        ("Customer", "Now can we configure the port forwarding rules directly into the cloud profile?", 22.4),
        ("Agent", "Obviously port forwarding tables require clean TCP and UDP port mappings bound to verified local IP endpoints.", None),
        ("Customer", "Right, I have the exact port numbers ready: port 22 and 443 for TrueNAS, and port 8000 and 8554 for the NVR.", 24.5),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Rhiannon speaking, our medical practice off-site backup server synchronizes confidential patient dental records across that TrueNAS tunnel between midnight and five in the morning! Because your router wiped the port forwarding rules every night this week, four consecutive off-site backups failed and our practice faced an immediate regulatory audit breach under healthcare compliance rules! I have been sick with worry, working until 4 AM trying to re-enter rules manually! We cannot afford another failed backup tonight!", -68.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand the immense pressure, regulatory anxiety, and exhausting late nights this has caused you and your dental practice, Rhiannon. Missing patient record compliance backups is an absolute critical emergency, and I will ensure these port forwarding rules are permanently committed and personally verify their persistence through a live test reboot right now.", None),
        ("Customer", "Thank you Gareth, that is exactly what I need to have total confidence.", -2.4),
        ("Agent", "I am binding port 22 and 443 to 192.168.1.50 for TrueNAS, and port 8000 and 8554 to 192.168.1.60 for the NVR directly on your primary cloud profile.", None),
        ("Customer", "The rules just populated in the hub web GUI!", 18.4),
        ("Agent", "Now I am triggering an explicit hardware write commit to sync the cloud profile to local non-volatile flash memory.", None),
        ("Customer", "Flash commit confirmed: 'NVRAM sync status: SUCCESS'.", 24.5),
        ("Agent", "Now let us initiate a deliberate remote restart of the Hub 5 to simulate the overnight maintenance reboot while we are on the call.", None),
        ("Customer", "Rebooting the hub now... The connection dropped... Hub is restarting.", 14.2),
        ("Agent", "The router will complete its boot initialization and reload its NVRAM tables in approximately two minutes.", None),
        ("Customer", "The hub light is flashing green... and now it turned solid green again! Internet is restored!", 26.2),
        ("Agent", "Please open the hub administration dashboard and check the Port Forwarding tab.", None),
        ("Customer", "Logging into 192.168.1.1... Navigating to Port Forwarding... Gareth! All four rules are still there! TrueNAS ports 22 and 443, and NVR ports 8000 and 8554 are intact!", 34.8),
        ("Agent", "Excellent! Now let us test external connectivity to verify the TrueNAS port from outside your local network.", None),
        ("Customer", "I am using my mobile phone with Wi-Fi turned off to query port 443 on our public IP... Gareth! The TrueNAS SSL login page loaded immediately over cellular!", 38.4),
        ("Agent", "That confirms full bidirectional port forwarding persistence across physical router reboots.", None),
        ("Customer", "Tonight's patient dental record backup will execute with zero errors.", 36.2),
        ("Agent", "I have locked the cloud profile preventing any future firmware updates from overriding user-defined firewall tables.", None),
        ("Customer", "You have completely saved our practice from regulatory audit sanctions, Gareth.", 34.5),
        ("Agent", "I have documented all firmware revisions and port rules under case reference ADV-PORT-99182-R.", None),
        ("Customer", "ADV-PORT-99182-R, recorded in our IT maintenance log.", 28.4),
        ("Agent", "Our automated configuration backup system will also archive your port rules every twenty-four hours.", None),
        ("Customer", "That provides total redundancy.", 26.2),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just making sure I have the exact account reference for our engineering log: that was BB-881920, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, BB-881920 is our business account reference.", 24.5),
        ("Agent", "Thank you Rhiannon, all configuration records and audit logs are fully committed.", None),
        ("Customer", "Thank you for your world-class expertise and rapid resolution today, Gareth.", 32.4),
        ("Agent", "It has been an absolute pleasure assisting you, Rhiannon. Best of luck with your dental practice backups.", None),
        ("Customer", "Have a wonderful rest of your day, Gareth.", 28.4),
        ("Agent", "Is there any other advanced technical query I can assist you with today, Rhiannon?", None),
        ("Customer", "No Gareth, you have fixed everything perfectly.", 26.2),
        ("Agent", "Thank you for calling S-Net advanced technical support, Rhiannon. Goodbye.", None),
        ("Customer", "Goodbye Gareth.", 24.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 20.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 16.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 12.0)
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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net advanced technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Rhiannon throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated exceptional empathy at turn 22 ('I completely understand the immense pressure, regulatory anxiety, and exhausting late nights this has caused you and your dental practice, Rhiannon...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased the NVRAM port forwarding persistence failure at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer account reference at turn 42.",
        "Took ownership of the problem": "Agent flashed firmware patch 4.12.3, bound rules to cloud profile, simulated live reboot, and verified persistence.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, supportive, and highly technical professional demeanor throughout.",
        "Probing": "Agent probed about TrueNAS IP reservations, port ranges, and backup schedules.",
        "Confirmed the issue is resolved": "Router rebooted on call, rules verified persistent in web GUI, and TrueNAS SSL login page accessed over cellular data."
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
        "cid": "agt_079",
        "cname": "Rhiannon",
        "target_dur": 997,
        "scenario": "Hub 5 port forwarding rules disappearing after night reboot; resolved via firmware 4.12.3 flash and NVRAM cloud commit",
        "tier": "excellent",
        "expected_score": 100.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": [],
        "notes": "Flawless advanced technical call demonstrating deep empathy in the middle third, firmware deployment, harmless recheck in the final third, and complete resolution verification."
    }

print("get_call_079 defined.")

# =========================================================================
# Call 080: Rory, Broadband connection dropping specifically during microwave usage, 18:27 (1107s)
# 3-4 faults (okay), score 66.7, Branding FAIL, Dead Air FAIL, Rapport FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_080():
    raw = [
        # Branding FAIL: Missing standard greeting
        ("Agent", "Broadband faults desk, my name is Keith.", None),
        ("Customer", "Hello Keith, my name is Rory McAllister. Whenever anyone in our household turns on the kitchen microwave oven to heat up food or boil a cup of soup, our Wi-Fi broadband connection drops dead instantly across every phone and television in the house, and only reconnects three minutes after the microwave stops!", -34.8),
        ("Agent", "Good afternoon Rory. If I understand correctly, your Wi-Fi broadband connection drops completely every time your kitchen microwave oven is turned on and takes several minutes to recover. Before we test your connection, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 45 Braemar Terrace, Aberdeen, AB10 7EJ, security PIN 6620, router model S-Net Hub 4.", -5.2),
        ("Agent", "Thank you Rory, that confirms your account details. Where is your broadband router physically located in relation to the kitchen microwave?", None),
        ("Customer", "The router sits on a bookshelf in our open-plan living room, about four meters away from the microwave with only a plasterboard partition wall in between.", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query your router's wireless spectrum interference and signal-to-noise ratio logs?", None),
        ("Agent", "Thank you for holding, Rory. The wireless radio telemetry confirms acute microwave radio frequency radiation leakage centered on 2450 megahertz.", None),
        ("Customer", "Why does microwave cooking radiation knock out our internet?", -10.4),
        ("Agent", "Domestic microwave magnetrons emit high-powered radio waves at 2450 MHz, which precisely overlaps Wi-Fi channels 8, 9, and 10 on the 2.4 GHz spectrum.", None),
        ("Customer", "Can you configure the router so it is completely immune to kitchen appliances?", -6.4),
        ("Agent", "If you operate a faulty, unshielded microwave oven with deteriorated door seals that leaks radiation into living areas, that is a domestic appliance hazard, not an S-Net telecommunications fault.", None),
        ("Customer", "Our microwave is a certified Panasonic oven bought brand new last year! Don't tell me my kitchen is hazardous when your router can't handle a microwave!", -52.4),
        ("Agent", "I am explaining how electromagnetic radiation from aging magnetrons overwhelms 2.4 GHz receiver antennas.", None),
        ("Customer", "What can we adjust on the router to prevent these drops?", -28.4),
        # Turn 14 is dead air gap 1 (40s)
        ("Agent", "The router operating frequency can be reconfigured across our remote network management portal.", None),
        ("Customer", "Keith? Hello? The line went completely dead for over thirty seconds! Did we get disconnected?!", -28.4),
        ("Agent", "I was querying the 5 GHz radio availability on your S-Net Hub 4.", None),
        ("Customer", "Please separate the 5 GHz network from the 2.4 GHz network so our devices avoid the microwave.", -18.2),
        ("Agent", "Obviously 5 GHz wireless spectrum operates between 5180 MHz and 5825 MHz, completely immune to microwave oven magnetron emissions.", None),
        ("Customer", "Yes, exactly! So please separate the 5 GHz network right now.", -12.4),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Rory speaking, my teenage daughter is studying for her Scottish Advanced Higher examinations, and her timed online mock exam was abruptly terminated and scored as zero yesterday because my wife turned on the microwave to warm soup! My daughter was in floods of tears, terrified she will fail her university entrance requirements! Having your family's future jeopardized because heating soup cuts the Wi-Fi is unacceptable! We need this solved!", -68.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand how devastating and stressful that was for your daughter and your entire family, Rory, especially with university entrance examinations and mock exams at stake. Having timed exam sessions terminated over cooking appliances is deeply upsetting, and I will reconfigure your router onto clean 5 GHz frequencies right now to protect her exams.", None),
        ("Customer", "Thank you Keith. What steps are required?", -12.2),
        ("Agent", "I am splitting your S-Net Hub 4 Wi-Fi broadcast into separate SSIDs: 'S-Net-McAllister-2.4' and 'S-Net-McAllister-5G'.", None),
        ("Customer", "The router light blinked orange and is now steady green.", 8.2),
        ("Agent", "Your daughter's laptop and household smartphones must be connected exclusively to 'S-Net-McAllister-5G'.", None),
        ("Customer", "I am connecting her laptop to 'S-Net-McAllister-5G' right now... Connected with full signal bars!", 22.4),
        ("Agent", "Because 5 GHz operates gigahertz away from magnetron frequencies, microwave emissions cannot induce packet loss on that SSID.", None),
        ("Customer", "Can we test turning on the microwave right now while she is on 5 GHz to prove it doesn't disconnect?", 14.2),
        ("Agent", "Because running an empty microwave oven causes magnetron arcing damage, testing requires heating a bowl of water or food during active cooking cycles.", None),
        ("Customer", "My wife and daughter are out at the library until six o'clock this evening, and I don't want to run the oven until dinner time.", -12.4),
        ("Agent", "You will need to verify the connection when you use the microwave during dinner preparation tonight.", None),
        ("Customer", "So we cannot confirm right now while we are on this call that the drops have completely stopped?", -18.2),
        # Turn 34 is dead air gap 2 (40s)
        ("Customer", "Keith? Hello? Why does your telephone line keep dropping into total silence for thirty or forty seconds?", -24.2),
        ("Agent", "I was documenting your wireless channel separation under case reference RF-MICROWAVE-88192-A.", None),
        ("Customer", "RF-MICROWAVE-88192-A, noted down.", 8.4),
        ("Agent", "Keep all examination laptops and streaming devices locked to the 5 GHz network to prevent future interference.", None),
        ("Customer", "I will ensure her laptop forgets the 2.4 GHz network so it never roams back.", 22.4),
        ("Agent", "I have also adjusted the 2.4 GHz channel to channel 1, which sits furthest away from the 2450 MHz magnetron peak.", None),
        ("Customer", "That provides extra buffer for legacy 2.4 GHz smart plugs.", 24.8),
        # Turn 41: Active listening harmless recheck in last third
        ("Agent", "Just making sure our premises records match perfectly: that was 44 Lenton Boulevard, Nottingham, wasn't it?", None),
        # Turn 42: Customer answers recheck
        ("Customer", "Yes, 44 Lenton Boulevard, Nottingham.", 18.4),
        ("Agent", "Thank you Rory, that confirms the premises record on the diagnostic profile.", None),
        ("Customer", "I will test the microwave at six o'clock tonight when heating dinner.", 16.2),
        ("Agent", "I have documented your account notes with a follow-up advisory.", None),
        ("Customer", "Thank you Keith for splitting those networks.", 18.4),
        ("Agent", "I have also waived this month's router rental fee as a courtesy for your daughter's exam disruption.", None),
        ("Customer", "That is appreciated. Thank you.", 16.2),
        ("Agent", "Is there any other broadband issue I can assist with today, Rory?", None),
        ("Customer", "No Keith, that covers it.", 14.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 10.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 6.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 2.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 0.0)
    ]

    ratings = {
        "Branding and Survey Check": "FAIL",
        "Hold time and Dead Air": "FAIL",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "PASS",
        "Active listening": "PASS",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Branding and Survey Check": "Failed standard opening and closing branding scripts.",
        "Hold time and Dead Air": "Dead Air Breach: Agent had 2 occurrences of >30s unmanaged dead air.",
        "Build rapport and observed professionalism": "Spoke rudely at turn 11 blaming customer for operating an unshielded appliance hazard.",
        "Confirmed the issue is resolved": "Failed to confirm resolution of microwave interference on call as customer could not test until dinner time."
    }

    evidence = {
        "Branding and Survey Check": "Agent failed standard opening branding ('Broadband faults desk...') and closing branding.",
        "Hold time and Dead Air": "Agent allowed two separate unmanaged dead air gaps of 40 seconds at turns 14 and 34.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Rory throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand how devastating and stressful that was for your daughter and your entire family, Rory...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased microwave interference issue at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer address at turn 41.",
        "Took ownership of the problem": "Agent split SSIDs, shifted 2.4 GHz channel to 1, guided 5 GHz connection, and waived router fee.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you operate a faulty, unshielded microwave oven with deteriorated door seals that leaks radiation into living areas, that is a domestic appliance hazard, not an S-Net telecommunications fault.'",
        "Probing": "Agent asked about router proximity and kitchen layout.",
        "Confirmed the issue is resolved": "Customer was unable to run microwave test until dinner, leaving issue unverified on call."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 41}
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
            {"kind": "handled", "customer_turn": 21, "agent_turn": 22, "with_refusal": True}
        ]
    }

    return {
        "cid": "agt_080",
        "cname": "Rory",
        "target_dur": 1107,
        "scenario": "Broadband connection dropping specifically during microwave usage; resolved via 5 GHz SSID split but unverified on call",
        "tier": "okay",
        "expected_score": 66.7,
        "dead_air_indices": [14, 33],
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Branding and Survey Check", "Build rapport and observed professionalism", "Confirmed the issue is resolved"],
        "notes": "Okay call featuring failed branding, dead air breaches, rude remarks, unverified resolution due to dinner time testing, and handled empathy in the middle third."
    }

print("get_call_080 defined.")

if __name__ == "__main__":
    for fn in [get_call_076, get_call_077, get_call_078, get_call_079, get_call_080]:
        c = fn()
        compile_call(c)
