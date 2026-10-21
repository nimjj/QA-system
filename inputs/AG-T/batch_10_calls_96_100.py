import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from batch_engine import compile_call

# =========================================================================
# Call 096: Wesley, Optical ONT red alarm light after power surge, 16:35 (995s)
# 6+ faults (poor), score 11.7, Dead Air FAIL, Verified FAIL, Personalized FAIL, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Probing FAIL, Confirmed resolved FAIL
# Features TWO outbursts (turn 8 handled, turn 21 unhandled)
# =========================================================================
def get_call_096():
    raw = [
        ("Agent", "Thank you for calling S-Net fiber technical faults, my name is Craig. How can I help you today?", None),
        ("Customer", "Hello, my name is Wesley Cox. Following an electrical lightning storm and power surge in our street last night, our fiber broadband has died completely and the wall-mounted optical network terminal has a solid red 'LOS' alarm light shining on the front, leaving our entire family with zero internet!", -45.2),
        # Paraphrasing FAIL: agent does not restate; Verified FAIL: agent fails to ask for PIN/address/security question
        ("Agent", "I can check the optical status. What is your fiber ONT serial number and account number?", None),
        ("Customer", "The ONT serial is SN-ONT-449102, account SN-771920, registered to 15 Orchard Close, Taunton, TA1 4NE, security PIN 8812.", -12.4),
        # Personalized FAIL: agent never uses "Wesley" anywhere in call
        ("Agent", "Let me open the Taunton fiber headend optical distribution console.", None),
        ("Customer", "Please check why the red LOS light is on.", -18.2),
        ("Agent", "Could I place you on hold for two minutes while I query the passive optical splitter port registers?", None),
        ("Agent", "Thank you for holding. The optical line terminal at the telephone exchange shows an unrecoverable signal fault on your fiber port.", None),
        # Outburst 1 at turn 8 (handled)
        ("Customer", "An unrecoverable signal fault?! S-Net charged us two hundred pounds for this fiber installation and guaranteed uninterrupted gigabit reliability! Now a single rainstorm knocks out our internet and leaves a red light on my wall! This equipment is flimsy rubbish and I am furious!", -72.4),
        # Agent handled empathy 1 at turn 9
        ("Agent", "I completely understand your frustration and anger, especially having invested two hundred pounds in fiber installation and expecting resilient gigabit service only to have a power surge disrupt your connection. Let us investigate what happened so we can get your line restored.", None),
        ("Customer", "Thank you Craig, please fix it as soon as possible.", -8.2),
        # Turn 11: diagnostic remark
        ("Agent", "Power surges can damage internal optoelectronic diodes on the ONT board.", None),
        ("Customer", "Can you replace the damaged optical hardware as soon as possible?", -24.2),
        ("Agent", "I am stating the standard causes of optical receiver burnout.", None),
        # Turn 14 is dead air gap 1 (40s)
        ("Customer", "Craig? Are you still there? The line was dead for forty seconds!", -28.4),
        ("Agent", "I was waiting for the Taunton OLT line card diagnostics to refresh.", None),
        ("Customer", "Can you reset the fiber port from your end?", -22.4),
        ("Agent", "Obviously optical LOS indicates complete loss of incoming laser light that cannot be fixed by software reboots.", None),
        ("Customer", "So the laser fiber cable itself is severed or dead?", -14.2),
        ("Agent", "The optical receiver diode inside your ONT has failed or the external fiber pigtail is broken.", None),
        ("Customer", "Can you dispatch an engineer to replace the ONT today?", -18.4),
        # Outburst 2 at turn 21: Customer second outburst in middle third (unhandled)
        ("Customer", "Wesley speaking, I am a freelance digital animator and 3D visual effects director, and at five o'clock today I have a non-negotiable delivery deadline for a thirty-second Super Bowl television commercial render! If I fail to upload these visual effects files to the Hollywood studio servers by five o'clock, the advertising agency will cancel our six-figure contract, our production studio will go bankrupt, and all seven of my staff will be laid off! I am having severe chest pains and a complete panic breakdown!", -88.4),
        # Turn 22: Agent MISSED/UNHANDLED empathy (agent completely ignores panic and talks about field engineer schedules)
        ("Agent", "The earliest Openreach specialized optical repair appointment is Monday afternoon between one and six o'clock.", None),
        ("Customer", "Monday afternoon?! Did you not hear a single word I just said about Hollywood studio servers and bankruptcy?! Are you completely deaf or do you just enjoy watching customers suffer?!", -82.4),
        # Rapport FAIL at turn 24 (middle third)
        ("Agent", "If you run a commercial digital animation studio from a residential broadband line, that is your own reckless negligence and poor planning.", None),
        ("Customer", "Can you not offer an emergency mobile broadband backup or 4G router right now?", -44.2),
        ("Agent", "Emergency 4G backup dongles can be collected from an S-Net retail store.", None),
        ("Customer", "Where is the nearest retail store with stock?", -12.4),
        ("Agent", "The nearest store is at the Taunton Orchard Shopping Centre.", None),
        ("Customer", "Will they hand me a 4G router if I show my account number?", -8.2),
        ("Agent", "They require photo identification and account confirmation.", None),
        ("Customer", "I will drive to the shopping centre immediately.", -14.2),
        # Turn 34 is dead air gap 2 (40s)
        ("Customer", "Craig?! Hello?! Did you vanish again?! Why does your phone line keep going silent for forty seconds?!", -44.2),
        ("Agent", "I was booking the Monday afternoon optical engineering appointment.", None),
        ("Customer", "Is the appointment confirmed?", -24.2),
        ("Agent", "The engineering visit is booked for Monday between 1:00 PM and 6:00 PM.", None),
        ("Customer", "Give me the booking reference number.", -18.2),
        ("Agent", "Your engineering appointment reference is FBR-REP-88192-T.", None),
        ("Customer", "FBR-REP-88192-T, noted down.", -12.4),
        ("Agent", "The engineer will replace the wall-mounted optical terminal.", None),
        ("Customer", "I will collect the 4G backup unit from the retail store right now.", -14.2),
        # Turn 42: Active listening repeat in last third
        ("Agent", "Before we conclude, what was that fiber ONT serial number again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start of our call, it is SN-ONT-449102.", -18.2),
        ("Agent", "Thank you, serial number confirmed on the ticket.", None),
        ("Customer", "Your customer service was cold and appalling.", -32.2),
        ("Agent", "Is there any other query today?", None),
        ("Customer", "No, goodbye.", -20.0),
        ("Agent", "Thank you for calling S-Net fiber technical faults. Goodbye.", None),
        ("Customer", "Goodbye.", -14.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -10.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -6.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", -2.0),
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
        "Personalized the call/ticket appropriately": "Agent failed to address customer by name 'Wesley' during the call.",
        "Empathy & Acknowledgment Statement": "Failed to acknowledge customer's severe distress and panic at turn 21 regarding Hollywood Super Bowl commercial delivery.",
        "Paraphrasing": "Failed to paraphrase customer's fiber ONT failure at the beginning of the call.",
        "Active listening": "Asked customer at turn 42 for ONT serial number which was already provided at turn 3.",
        "Build rapport and observed professionalism": "Insulted customer at turn 11: 'If you don't plug your sensitive fiber hardware into surge-protected mains sockets, electrical damage is your own fault.'",
        "Probing": "Failed to probe effectively regarding surge damage or local circuit breaker tripping.",
        "Confirmed the issue is resolved": "Optical terminal remained completely dead with red LOS alarm; physical repair pending Monday appointment."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net fiber technical faults' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Agent allowed two separate unmanaged dead air gaps of 40 seconds at turns 14 and 33.",
        "Verified customer": "Agent failed to ask for postal address or security PIN during verification.",
        "Personalized the call/ticket appropriately": "Agent never addressed customer as Wesley throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent handled first outburst at turn 8, but completely ignored severe panic breakdown at turn 21 regarding Hollywood contract and studio bankruptcy.",
        "Paraphrasing": "Agent offered no restatement of the customer's problem.",
        "Active listening": "Agent asked for ONT serial at turn 42 despite customer stating SN-ONT-449102 at turn 3.",
        "Took ownership of the problem": "Agent booked Monday optical engineer and directed customer to retail store for 4G backup.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you don't plug your sensitive fiber hardware into surge-protected mains sockets, electrical damage is your own fault.'",
        "Probing": "Agent asked no diagnostic questions about electrical or pigtail conditions.",
        "Confirmed the issue is resolved": "Fiber remained inoperative with LOS red light; resolution unconfirmed on call."
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
        "cid": "agt_096",
        "cname": "Wesley",
        "target_dur": 995,
        "scenario": "Fiber ONT optical LOS red alarm light after power surge; 2 customer outbursts (one handled, one unhandled); 6+ faults (poor)",
        "tier": "poor",
        "expected_score": 11.7,
        "dead_air_indices": [14, 33],
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Build rapport and observed professionalism", "Empathy & Acknowledgment Statement", "Confirmed the issue is resolved", "Verified customer", "Personalized the call/ticket appropriately", "Probing", "Paraphrasing"],
        "notes": "Poor call featuring dead air breaches, two customer outbursts (first handled, second unhandled), rude remarks, failed verification and personalization, and active listening repeat."
    }

print("get_call_096 defined.")

# =========================================================================
# Call 097: Wilma, Mobile visual voicemail app failing to sync audio messages, 11:50 (710s)
# 0 faults (excellent), score 100.0, All PASS
# =========================================================================
def get_call_097():
    raw = [
        ("Agent", "Thank you for calling S-Net mobile technical support, my name is Liam. How can I help you today?", None),
        ("Customer", "Hello Liam, my name is Wilma Price. On my iPhone 15, the S-Net Visual Voicemail tab has stopped synchronizing audio messages: whenever a caller leaves a voicemail, I get an SMS notification saying I have a new message, but the Visual Voicemail screen stays completely empty and says 'Visual Voicemail is currently unavailable'!", -34.8),
        ("Agent", "Good afternoon Wilma. If I understand correctly, your iPhone 15 Visual Voicemail interface has stopped downloading incoming audio messages, presenting an 'unavailable' error message while standard SMS alerts continue to arrive. Before we inspect your mobile subscriber voicemail profile and carrier telemetry, could you please confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 42 High Street, Shrewsbury, SY1 1ST, security PIN 5192, mobile number 07700 900512.", -5.2),
        ("Agent", "Thank you Wilma, that confirms your account details. Have you attempted dialing 1571 directly from your phone keypad to listen to the voicemails manually?", None),
        ("Customer", "Yes, when I dial 1571 I can hear three unplayed messages over the phone line, but Visual Voicemail will not load them as audio files in iOS.", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query your carrier voicemail IMAP synchronization gateway and cellular data provisioning profile?", None),
        ("Agent", "Thank you for holding, Wilma. Looking at the voicemail server telemetry, your line has an orphaned session token on the carrier Visual Voicemail IMAP sync daemon.", None),
        ("Customer", "Why would an orphaned session token cause Visual Voicemail to show as unavailable?", -10.4),
        ("Agent", "When iOS installs a carrier bundle update, the local cryptographic authentication handshake occasionally falls out of sync with our voicemail IMAP cluster.", None),
        ("Customer", "Can you clear the orphaned session token and reset the carrier handshake?", 2.4),
        ("Agent", "Yes, we can perform a remote carrier voicemail profile reprovisioning and push a fresh secure sync token directly to your iPhone.", None),
        ("Customer", "Will that erase my saved voice messages or greeting?", -8.2),
        ("Agent", "Not at all: your recorded messages and personalized voicemail greeting remain completely intact on our central server.", None),
        ("Customer", "That is a huge relief.", 12.2),
        ("Agent", "I am sending the carrier bundle profile reprovisioning command now.", None),
        ("Agent", "Obviously Visual Voicemail relies on cellular packet data tunnels rather than standard voice signaling.", None),
        ("Customer", "I understand cellular data is required for the visual interface.", 18.4),
        ("Agent", "I am pushing the carrier token reset signal directly to your device.", None),
        ("Customer", "My iPhone screen briefly flashed 'Carrier Settings Updated'.", 24.2),
        # Outburst at turn 20 in middle third (handled - late acknowledgement 3 turns after)
        ("Customer", "Wilma speaking, I am an executor for my late sister's estate and today is the absolute final deadline to file the probate estate documentation with the High Court probate registry! The estate solicitor left an urgent voicemail three hours ago regarding a disputed inheritance bequest, but because the audio file was trapped on my phone, I could not transcribe the exact case reference numbers! If this probate filing is missed, the High Court will freeze the family estate in litigation for years! I am sick with grief and terror!", -84.2),
        ("Agent", "I am querying the carrier voicemail IMAP synchronization daemon right now.", None),
        ("Customer", "Please do Liam, I am desperate to reach the solicitor before the registry closes.", 14.2),
        # Agent handled empathy at turn 23 (3 turns after outburst) with refusal
        ("Agent", "I completely understand the acute grief, terror, and intense pressure you are experiencing regarding your late sister's estate and the High Court probate deadline today, Wilma. While our carrier policy cannot dispatch a field technician to your home for mobile application issues, I will stay on the line with you right now and personally verify that every single audio message downloads onto your screen immediately.", None),
        ("Customer", "Thank you Liam! Let us open the phone app and check the messages right now.", 14.2),
        ("Agent", "Open the Phone app on your iPhone, tap the Voicemail tab in the bottom right corner, and pull down to refresh.", None),
        ("Customer", "Opening Phone app... Tapping Voicemail tab... Pulling down to refresh... Liam! Three voicemail cards just popped onto the screen with caller names and exact timestamps! It loaded!", 36.8),
        ("Agent", "Tap on the top message from your estate solicitor and press the Play button.", None),
        ("Customer", "Tapping solicitor message... Pressing play... The audio is playing loud and clear through the phone speaker! The automated text transcription is scrolling underneath! I can see the exact probate reference number: PRB-4491-X!", 39.2),
        ("Agent", "Fantastic! That confirms full Visual Voicemail audio downloading and real-time transcription completely restored.", None),
        ("Customer", "You have completely saved my sister's estate today, Liam.", 38.4),
        ("Agent", "I have locked the carrier IMAP configuration in your subscriber profile to prevent any future sync drops.", None),
        ("Customer", "That will keep it running smoothly for all future legal calls.", 34.2),
        ("Agent", "I have documented the carrier token refresh under ticket reference VVM-IOS-88192-S.", None),
        ("Customer", "VVM-IOS-88192-S, noted down.", 30.2),
        ("Agent", "Please accept my deepest condolences on the loss of your sister, Wilma. Best of luck with the probate filing today.", None),
        ("Customer", "Thank you Liam, your kindness and urgency have made all the difference.", 36.2),
        ("Agent", "Our team is honored to support you during such an important time.", None),
        ("Customer", "I can now email the solicitor and file the High Court paperwork immediately.", 34.8),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just making sure our premises records match perfectly: that was 42 High Street, Shrewsbury, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, 42 High Street, Shrewsbury.", 32.4),
        ("Agent", "Thank you Wilma, all account and device parameters are fully synchronized.", None),
        ("Customer", "Thank you again Liam for your brilliant, rapid, and reassuring support.", 36.2),
        ("Agent", "It has been an absolute pleasure assisting you, Wilma. Have a peaceful afternoon.", None),
        ("Customer", "Have a wonderful afternoon, Liam. Goodbye.", 32.4),
        ("Agent", "Is there any other mobile issue I can assist you with today, Wilma?", None),
        ("Customer", "No Liam, everything is working flawlessly.", 30.2),
        ("Agent", "Thank you for calling S-Net mobile technical support, Wilma. Goodbye.", None),
        ("Customer", "Goodbye Liam.", 28.4),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 24.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 20.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net mobile technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Wilma throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated profound empathy at turn 22 regarding customer's late sister's estate and High Court probate deadline, and no unhandled outbursts occurred.",
        "Paraphrasing": "Agent accurately paraphrased the Visual Voicemail synchronization failure at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer address at turn 42.",
        "Took ownership of the problem": "Agent executed carrier profile reprovisioning, pushed token reset, locked IMAP settings, and verified live audio playback.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, warm, and highly supportive professional demeanor throughout.",
        "Probing": "Agent probed about direct 1571 keypad dialing and carrier update history.",
        "Confirmed the issue is resolved": "Customer refreshed the Voicemail tab live on call, saw three message cards, and played the solicitor's audio message perfectly."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 39}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 2},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 16}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 20, "agent_turn": 23, "with_refusal": True}
        ]
    }

    return {
        "cid": "agt_097",
        "cname": "Wilma",
        "target_dur": 710,
        "scenario": "Mobile Visual Voicemail interface failing to sync audio messages on iPhone 15; resolved via carrier token refresh and IMAP profile reprovisioning",
        "tier": "excellent",
        "expected_score": 100.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": [],
        "notes": "Flawless call featuring deep empathy in middle third, carrier token reprovisioning, harmless recheck in final third, and complete live audio playback verification."
    }

print("get_call_097 defined.")

# =========================================================================
# Call 098: Xavier, TV 4K HDR color banding on OLED display, 19:05 (1145s)
# 4 faults (okay), score 55.0, Dead Air FAIL, Verified FAIL, Personalized FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_098():
    raw = [
        ("Agent", "Thank you for calling S-Net TV technical operations, my name is Richard. How can I help you today?", None),
        ("Customer", "Hello Richard, my name is Xavier Dupont. We have an S-Net TV 4K box connected to a new LG OLED television, and whenever we watch 4K HDR sports or blockbuster movies, the picture displays terrible posterization and color banding with harsh jagged rings around dark shadows and skies instead of smooth gradations!", -34.8),
        ("Agent", "Good afternoon. If I understand correctly, your TV 4K box is experiencing severe color banding and posterization artifacts during 4K HDR playback on your LG OLED display, creating visible rings around dark scenes and skies. Let me query your set-top box HDMI handshake registers.", None),
        # Verified FAIL: agent asks only for TV box serial, omitting PIN/address
        ("Customer", "Our TV box serial is SN-TV-551029, account reference SN-881920, registered at 12 Trinity Square, Cambridge, CB2 1TT, security PIN 3391.", -5.2),
        # Personalized FAIL: agent never uses "Xavier" anywhere in call
        ("Agent", "Thank you, that brings up the Cambridge TV equipment record.", None),
        ("Customer", "Why would a 4K box produce color banding on an OLED screen?", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query your set-top box HDMI EDID video payload and chroma subsampling telemetry?", None),
        ("Agent", "Thank you for holding. Looking at the HDMI EDID link diagnostics, the set-top box is negotiating an 8-bit YCbCr 4:2:0 color space rather than a 10-bit HDR10 color format.", None),
        ("Customer", "Why is it negotiating 8-bit color instead of 10-bit HDR?", -10.4),
        ("Agent", "The HDMI cable between your box and the television is failing high-speed TMDS clock validation, causing the hardware to throttle down from 18 Gbps to 10.2 Gbps.", None),
        ("Customer", "Can we change the HDMI settings on the TV box to force 10-bit color?", 2.4),
        ("Agent", "Forcing 10-bit color over an insufficient HDMI cable causes complete screen blackouts; however, we can switch the box to YCbCr 4:2:2 10-bit limited range as a temporary stabilizing profile.", None),
        ("Customer", "How do we adjust that setting?", 6.2),
        # Turn 14 is dead air gap 1 (40s)
        ("Customer", "Richard? Are you still there? The phone line went completely silent for forty seconds!", -28.4),
        ("Agent", "I was pushing the HDMI profile modification payload to your set-top box.", None),
        ("Customer", "Will changing the profile eliminate the jagged rings?", -14.2),
        ("Agent", "Obviously 4K HDR video requires high-bandwidth certified Ultra High Speed HDMI cabling to transmit uncompressed 10-bit color matrices.", None),
        ("Customer", "Right, I understand high bandwidth is necessary for 10-bit HDR.", -8.2),
        ("Agent", "I am sending a certified Ultra High Speed 48 Gbps HDMI 2.1 braided cable from our equipment logistics center.", None),
        ("Customer", "That will permanently solve the bandwidth bottleneck.", 8.4),
        # Outburst at turn 20 in middle third (handled)
        ("Customer", "I am a retired film editor and tonight my grandchildren are coming over to our house to watch the 4K HDR premiere of an animated movie that I personally edited the color grading for before I retired! This family movie night is the first time my young grandchildren will see their grandfather's cinematic work on television! If the screen displays ugly jagged pixel rings and ruinous posterization, my grandchildren will be disappointed and my heart will break! I am so distressed!", -78.4),
        # Agent handled empathy at turn 21
        ("Agent", "I completely understand how deeply important this family movie night is for you, especially with your grandchildren visiting to watch your own color grading work on an animated classic. Having your cinematic work marred by HDMI bandwidth compression is heartbreaking, and I will make sure we optimize your TV box settings right now so tonight's film displays beautiful, smooth color gradations, and dispatch a certified HDMI 2.1 cable for tomorrow morning.", None),
        ("Customer", "Thank you Richard, let's optimize the settings right now.", 14.2),
        ("Agent", "On your TV box remote, open Settings, go to Picture & Sound, select HDMI Resolution, and choose '4K 10-Bit YCbCr 4:2:2'.", None),
        ("Customer", "Selecting '4K 10-Bit YCbCr 4:2:2'... Pressing confirm... Screen went black for two seconds and returned.", 22.4),
        ("Agent", "Now play a scene from your animated movie that previously showed severe banding.", None),
        ("Customer", "Loading movie scene with the sunset and dark shadows... Richard! The sunset is rendering smoothly with 90% of the banding completely eliminated! The colors look vibrant and natural!", 36.8),
        ("Agent", "That interim profile stabilizes the 10-bit color depth within your existing cable's bandwidth limit.", None),
        ("Customer", "My grandchildren will be able to enjoy the film in gorgeous quality tonight.", 38.4),
        ("Agent", "Once our certified Ultra High Speed HDMI 2.1 cable arrives tomorrow, you can enable full uncompressed 12-bit RGB 4:4:4 color.", None),
        ("Customer", "That will achieve absolute reference studio perfection.", 34.2),
        ("Agent", "Your HDMI 2.1 cable dispatch consignment reference is CAB-HDMI-88192-C.", None),
        ("Customer", "CAB-HDMI-88192-C, noted down.", 28.4),
        # Turn 34 is dead air gap 2 (40s)
        ("Customer", "Hello? Richard? Did the line drop again? Why does your headset keep cutting out?", -28.2),
        ("Agent", "I was waiving the standard thirty-pound cable dispatch charge on your account.", None),
        ("Customer", "Thank you for waiving the charge, Richard.", 24.2),
        ("Agent", "The new cable will arrive via Royal Mail Tracked 24 tomorrow morning.", None),
        ("Customer", "Tomorrow morning, excellent.", 26.2),
        ("Agent", "I have included step-by-step OLED calibration guidance inside the package.", None),
        ("Customer", "That will be very useful for my TV settings.", 28.4),
        ("Agent", "Have a magical family movie night with your grandchildren tonight.", None),
        ("Customer", "You have brought immense happiness to our home today.", 32.4),
        # Turn 42: Active listening harmless recheck in last third
        ("Agent", "Just making sure our premises records match perfectly: that was 12 Trinity Square, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, 12 Trinity Square, Cambridge.", 28.4),
        ("Agent", "Thank you, hardware serial confirmed on the logistics order.", None),
        ("Customer", "Thank you Richard for your expert help.", 28.4),
        ("Agent", "It has been my pleasure assisting. Enjoy the premiere tonight.", None),
        ("Customer", "Goodbye Richard.", 26.2),
        ("Agent", "Is there any other TV issue today?", None),
        ("Customer", "No, goodbye.", 24.0),
        ("Agent", "Thank you for calling S-Net TV technical operations. Goodbye.", None),
        ("Customer", "Goodbye.", 20.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 16.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 12.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 8.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 4.0)
    ]

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "FAIL",
        "Verified customer": "FAIL",
        "Personalized the call/ticket appropriately": "FAIL",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "PASS",
        "Active listening": "PASS",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Hold time and Dead Air": "Dead Air Breach: Agent had 2 occurrences of >30s unmanaged dead air.",
        "Verified customer": "Agent failed to ask for a PIN, address, or security question within the first 4 minutes of the call.",
        "Personalized the call/ticket appropriately": "Agent failed to address customer by name 'Xavier' during the call.",
        "Confirmed the issue is resolved": "Interim profile improved banding, but permanent HDMI 2.1 cable was dispatched by post, unconfirmed on call."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net TV technical operations' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Agent allowed two separate unmanaged dead air gaps of 40 seconds at turns 14 and 33.",
        "Verified customer": "Agent failed to ask for address or security PIN during verification.",
        "Personalized the call/ticket appropriately": "Agent never addressed customer as Xavier throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated deep empathy at turn 21 regarding customer's grandchildren movie premiere, and no unhandled outbursts occurred.",
        "Paraphrasing": "Agent accurately paraphrased the 4K HDR posterization and color banding issue at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer address at turn 42.",
        "Took ownership of the problem": "Agent configured interim 10-bit profile, dispatched free certified HDMI 2.1 cable, and verified animated scene.",
        "Build rapport and observed professionalism": "Agent maintained polite, knowledgeable, and professional demeanor throughout.",
        "Probing": "Agent gathered details on OLED television model and HDR settings.",
        "Confirmed the issue is resolved": "Interim settings provided temporary improvement, but complete hardware resolution requires tomorrow's cable installation."
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
            {"kind": "blunt_but_ok", "agent_turn": 16}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 20, "agent_turn": 21, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_098",
        "cname": "Xavier",
        "target_dur": 1145,
        "scenario": "TV 4K HDR color banding and posterization on OLED display due to HDMI TMDS clock throttling; interim profile applied and HDMI 2.1 cable dispatched",
        "tier": "okay",
        "expected_score": 55.0,
        "dead_air_indices": [14, 33],
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Confirmed the issue is resolved", "Verified customer", "Personalized the call/ticket appropriately"],
        "notes": "Okay call featuring dead air breaches, failed verification and personalization, handled empathy in middle third, HDMI 2.1 cable dispatch, and pending physical resolution."
    }

print("get_call_098 defined.")

# =========================================================================
# Call 099: Yasmin, Wi-Fi interference from industrial radio equipment, 14:00 (840s)
# 1-2 faults (good), score 83.3, Active listening FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_099():
    raw = [
        ("Agent", "Thank you for calling S-Net broadband advanced technical support, my name is Fiona. How can I help you today?", None),
        ("Customer", "Hello Fiona, my name is Yasmin Patel. We live adjacent to a commercial light-industrial estate in Birmingham, and every morning at eight o'clock when the workshops power up their machinery, our home Wi-Fi network completely collapses across both 2.4 GHz and 5 GHz bands, dropping our connections and making remote work impossible!", -34.8),
        ("Agent", "Good afternoon Yasmin. If I understand correctly, your home Wi-Fi network experiences catastrophic interference and connection collapse across both 2.4 GHz and 5 GHz radio bands every morning at eight o'clock coinciding with neighboring industrial machinery powering up. Before we examine your hub's RF spectrum analyzer telemetry, could you please confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 19 Forge Lane, Birmingham, B12 0JJ, security PIN 7192, router model S-Net Hub 5.", -5.2),
        ("Agent", "Thank you Yasmin, that confirms your account details. Have you noticed whether devices connected via Ethernet cable maintain internet connectivity during the Wi-Fi drop?", None),
        ("Customer", "Yes, our desktop computer connected via Ethernet cable stays online at 500 Mbps, but every smartphone, tablet, and wireless laptop in the house drops off Wi-Fi completely.", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query your Hub 5 real-time wireless channel noise floor and non-Wi-Fi RF energy telemetry?", None),
        ("Agent", "Thank you for holding, Yasmin. Looking at the RF spectrum analyzer telemetry, your Hub 5 is detecting massive radio frequency interference with a noise floor of minus 62 dBm across standard UNII-1 wireless channels 36 to 48.", None),
        ("Customer", "What would cause a minus 62 dBm noise floor on channels 36 to 48?", -10.4),
        ("Agent", "Heavy electromagnetic pulse radiation from high-frequency industrial arc welding or motor drives radiates broad-spectrum noise that blinds the hub's standard receiver channels.", None),
        ("Customer", "Can we move our Wi-Fi to frequencies outside the welding interference?", 2.4),
        ("Agent", "Yes, we can migrate your Hub 5 to protected Dynamic Frequency Selection channels in the upper UNII-2 Extended band between channels 100 and 128.", None),
        ("Customer", "Do the industrial welding machines reach into channels 100 to 128?", 12.2),
        ("Agent", "No, the DFS frequency block operates at higher carrier frequencies completely isolated from industrial electromagnetic induction harmonics.", None),
        ("Customer", "That sounds like the perfect technical solution.", 18.4),
        ("Agent", "I am locking your Hub 5 5 GHz radio to DFS Channel 104 with 80 MHz channel width.", None),
        ("Agent", "Obviously high-frequency industrial induction requires advanced channel allocation rather than standard factory auto-tuning.", None),
        ("Customer", "I understand specialized channel tuning is essential near factories.", 22.4),
        ("Agent", "I am pushing the DFS channel assignment payload directly to your router.", None),
        ("Customer", "The hub's center light flashed amber for three seconds and returned to solid white.", 26.2),
        # Outburst at turn 20 in middle third (handled - late acknowledgement 3 turns after)
        ("Customer", "Yasmin speaking, I am a pediatric cardiology nurse practitioner, and this morning at ten o'clock I am running a critical remote telemetry clinic monitoring eighteen vulnerable infants recovering at home from neonatal heart surgery! If my Wi-Fi drops while I am reviewing these infants' cardiac arrhythmias, a baby could enter cardiac arrest without warning and die before an ambulance is dispatched! I am terrified and shaking with anxiety!", -86.4),
        ("Agent", "I am querying the RF spectrum analyzer telemetry on your Hub 5 right now.", None),
        ("Customer", "Please do Fiona, I am desperate to reach my infant patients before ten o'clock.", 14.2),
        # Agent handled empathy at turn 23 (3 turns after outburst) with refusal
        ("Agent", "I completely understand the acute terror, shaking anxiety, and profound responsibility you are bearing, Yasmin, especially with eighteen vulnerable infants recovering from neonatal heart surgery relying on your remote cardiac monitoring today. While our carrier policy cannot dispatch an emergency field technician within one hour to investigate external industrial factories, I will stay on the line with you right now and personally verify that your wireless devices connect to the new DFS channels with zero packet drop.", None),
        ("Customer", "Thank you Fiona! Let us test connecting our wireless devices right now.", 14.2),
        ("Agent", "On your smartphone or laptop, open your Wi-Fi settings and ensure you are connected to your S-Net network.", None),
        ("Customer", "Checking Wi-Fi settings... Connected to 'S-Net Hub 5 5G'... Signal bars are full!", 28.4),
        ("Agent", "Now run a live wireless speed and ping jitter test while I monitor the RF spectrum noise floor on our console.", None),
        ("Customer", "Running speed test on laptop over Wi-Fi... Fiona! Download speed is 490 Mbps, upload is 52 Mbps, ping latency is 8 milliseconds with 0% packet loss! The connection is lightning fast!", 38.4),
        ("Agent", "Looking at our console, the noise floor on Channel 104 is an ultra-clean minus 94 dBm with zero interference from the industrial workshops.", None),
        ("Customer", "Minus 94 dBm! That is pristine!", 36.2),
        ("Agent", "That confirms your remote cardiac telemetry session will operate with absolute stability.", None),
        ("Customer", "All eighteen infants will receive safe and uninterrupted cardiac monitoring today.", 38.4),
        ("Agent", "I have locked Channel 104 permanently into your hub cloud profile so the automated night-time channel hopper never reverts to standard channels.", None),
        ("Customer", "That will protect my clinical clinic every single morning.", 34.2),
        ("Agent", "I have documented the industrial RF mitigation under ticket reference RF-DFS-88192-B.", None),
        ("Customer", "RF-DFS-88192-B, recorded in my medical clinic book.", 30.2),
        ("Agent", "I have also scheduled our network automation to poll your hub's noise floor at eight o'clock tomorrow morning to confirm ongoing clearance.", None),
        ("Customer", "Thank you Fiona, that automated morning check is wonderful reassurance.", 34.8),
        ("Agent", "Please give my heartfelt best wishes to the infants and families in your care today, Yasmin.", None),
        ("Customer", "You have brought immense peace of mind to our hospital team today.", 36.2),
        ("Agent", "It is our absolute honor to support your vital pediatric nursing work.", None),
        ("Customer", "I can now log into the cardiac telemetry server with complete confidence.", 34.8),
        # Turn 42: Active listening repeat in last third
        ("Agent", "Before we conclude, what was that Birmingham postal address again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start of our call, it is 19 Forge Lane, Birmingham.", -10.2),
        ("Agent", "Thank you Yasmin, address confirmed on the monitoring ticket.", None),
        ("Customer", "Thank you again Fiona for your compassionate and urgent help.", 36.2),
        ("Agent", "It has been an absolute pleasure assisting you, Yasmin. Have a wonderful and successful clinic.", None),
        ("Customer", "Goodbye Fiona.", 32.4),
        ("Agent", "Is there any other technical issue I can assist with today, Yasmin?", None),
        ("Customer", "No Fiona, everything is working flawlessly.", 30.2),
        ("Agent", "Thank you for calling S-Net broadband advanced technical support, Yasmin. Goodbye.", None),
        ("Customer", "Goodbye Fiona.", 28.4),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 24.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 20.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
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
        "Active listening": "FAIL",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Active listening": "Asked customer at turn 42 for postal address which was already provided at turn 3.",
        "Confirmed the issue is resolved": "DFS channel migration performed, but long-term clearance across morning industrial shifts requires tomorrow's 8am monitoring confirmation."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net broadband advanced technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Yasmin throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated deep empathy at turn 22 regarding customer's pediatric cardiology clinic and infant heart patients, and no unhandled outbursts occurred.",
        "Paraphrasing": "Agent accurately paraphrased the industrial radio frequency interference issue at turn 2.",
        "Active listening": "Agent asked for postal address at turn 42 despite customer stating 19 Forge Lane at turn 3.",
        "Took ownership of the problem": "Agent migrated hub to DFS Channel 104, locked cloud profile, verified 490 Mbps speed, and scheduled 8am monitoring.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, warm, and highly supportive professional demeanor throughout.",
        "Probing": "Agent probed about wired Ethernet stability versus wireless dropouts.",
        "Confirmed the issue is resolved": "Immediate speed test was flawless, but long-term resolution during industrial operations requires tomorrow morning's 8am audit."
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
            {"kind": "blunt_but_ok", "agent_turn": 16}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 20, "agent_turn": 23, "with_refusal": True}
        ]
    }

    return {
        "cid": "agt_099",
        "cname": "Yasmin",
        "target_dur": 840,
        "scenario": "Wi-Fi interference from adjacent commercial industrial welding machinery; resolved via DFS Channel 104 migration with 8am audit scheduled",
        "tier": "good",
        "expected_score": 83.3,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Confirmed the issue is resolved"],
        "notes": "Good call featuring deep empathy in middle third, DFS channel migration, active listening repeat in final third, and pending long-term morning audit confirmation."
    }

print("get_call_099 defined.")

# =========================================================================
# Call 100: Zachary, Multi-room TV whole-home recording sharing desynchronized, 19:35 (1175s)
# 0 faults (excellent), score 100.0, All PASS! THE GRAND FINALE CALL!
# Features TWO handled outbursts (turn 15 handled, turn 21 handled)
# =========================================================================
def get_call_100():
    raw = [
        ("Agent", "Thank you for calling S-Net TV technical support, my name is Benjamin. How can I help you today?", None),
        ("Customer", "Hello Benjamin, my name is Zachary King. We have an S-Net Multi-Room TV setup with a master 4K box in the living room and two mini multi-room boxes in the bedrooms, but for the past two days the whole-home recording sharing feature has stopped working: neither mini box can see or play any recordings stored on the master box, showing error code MR-SYNC-404!", -34.8),
        ("Agent", "Good afternoon Zachary. If I understand correctly, your S-Net Multi-Room TV system is failing to share recordings from your master 4K set-top box to your two bedroom mini boxes, presenting error code MR-SYNC-404 across both remote units. Before we inspect your home network MoCA mesh and cluster synchronization tables, could you please confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 25 Kingsway, Bath, BA2 2ET, security PIN 4821, master box serial SN-TV-991204.", -5.2),
        ("Agent", "Thank you Zachary, that confirms your account details. Are the mini TV boxes connected to your home network via Wi-Fi or via coaxial MoCA cable adapters?", None),
        ("Customer", "They are connected via coaxial cable using the official S-Net MoCA 2.5 network adapters.", -12.4),
        ("Agent", "Could I place you on hold for two minutes while I query your master set-top box MoCA cluster security certificates and DVR discovery broadcast daemon?", None),
        ("Agent", "Thank you for holding, Zachary. Looking at the MoCA mesh telemetry, your master box cryptographic cluster key desynchronized after an automated overnight security certificate rotation.", None),
        ("Customer", "Why would a security certificate rotation desynchronize the mini boxes?", -10.4),
        ("Agent", "When the master box updates its internal security encryption key, the peripheral mini boxes require an authenticated handshake to renew their distributed media streaming credentials.", None),
        ("Customer", "Can you re-key the MoCA mesh and re-authenticate the mini boxes remotely?", 2.4),
        ("Agent", "Yes, we can broadcast an immediate MoCA cluster re-keying payload across your home coaxial network.", None),
        ("Customer", "Will that erase any saved recordings on the master hard drive?", -8.2),
        ("Agent", "Not at all: hard drive recordings, scheduled timers, and series links remain completely untouched; only the local streaming authorization tokens are re-keyed.", None),
        ("Customer", "That is fantastic news.", 12.2),
        # Outburst 1 at turn 15 (handled - late acknowledgement 3 turns after)
        ("Customer", "Zachary speaking, my twelve-year-old son is bedridden in his bedroom recovering from a fractured femur in traction, and watching his recorded science fiction series from the master box is the only distraction keeping his spirits up while he is trapped in bed! When the mini box threw that error code and locked him out of his favorite shows, he burst into tears of frustration! Seeing my injured boy crying in pain and boredom breaks my heart! I am so distressed!", -76.4),
        ("Agent", "I am querying the master set-top box MoCA cluster security certificates right now.", None),
        ("Customer", "Please do Benjamin, I am desperate to comfort my injured son in traction.", 14.2),
        # Agent handled empathy 1 at turn 18 (3 turns after outburst) with refusal
        ("Agent", "I completely understand how deeply heartbreaking and distressing this is, Zachary, especially with your twelve-year-old son in traction recovering from a fractured femur and relying on his favorite sci-fi shows for comfort and distraction. While our engineering policy cannot dispatch an emergency field technician within two hours to rewire coaxial cables, I will walk you through re-keying the MoCA network right now so his shows play flawlessly in his bedroom.", None),
        ("Customer", "Thank you Benjamin, that brings me so much relief.", 14.2),
        ("Agent", "I am sending the MoCA cluster re-keying signal across your coaxial network now.", None),
        ("Agent", "Obviously encrypted multi-room streams demand synchronized cryptographic keys to protect copyright licensing between DVR nodes.", None),
        ("Customer", "The LED light on the coaxial adapter blinked green and turned solid amber.", 22.4),
        # Outburst 2 at turn 21 in middle third (handled)
        ("Customer", "Zachary speaking, his orthopedic pediatric surgeon warned us that severe emotional distress and crying spikes his blood pressure and impairs bone healing! If he stays agitated all weekend without his entertainment, his orthopedic recovery could be set back by weeks! I am in sheer panic over his health and recovery!", -84.2),
        # Agent handled empathy 2 at turn 22
        ("Agent", "I completely understand the acute medical anxiety and intense emotional stakes regarding your son's orthopedic bone healing and blood pressure, Zachary. Protecting his physical recovery and restoring his entertainment immediately is an absolute top priority. Let us walk into your son's bedroom right now, power on his mini TV box together, and verify that his sci-fi recordings load and play perfectly.", None),
        ("Customer", "I am walking into his bedroom right now... Picking up the mini box remote...", 14.2),
        ("Agent", "Turn on the television, press the Home button on the remote, and select 'Recordings'.", None),
        ("Customer", "Pressing Home... Selecting Recordings... Benjamin! The screen says 'Connecting to Master DVR'... Boom! All fifty-two recorded episodes of 'Doctor Who' and 'Star Trek' appeared on his screen immediately! The full library is back!", 38.4),
        ("Agent", "Select an episode of Doctor Who and press Play to verify smooth coaxial streaming.", None),
        ("Customer", "Selecting Doctor Who... Pressing play... Benjamin, the video started instantaneously in crisp high definition with surround sound! My son just laughed and clapped his hands!", 39.4),
        ("Agent", "Look at our telemetry console: your MoCA mesh is streaming at a rock-solid 850 Mbps with 0% packet jitter and zero buffer delay.", None),
        ("Customer", "My son has a giant smile on his face. You have brought joy back into his recovery room today, Benjamin.", 39.0),
        ("Agent", "Now let us check the second mini box in your guest room just to ensure complete whole-home synchronization.", None),
        ("Customer", "Walking to the guest room... Turning on guest mini box... Opening Recordings... The entire DVR library loaded instantly here too!", 38.4),
        ("Agent", "That confirms full whole-home MoCA 2.5 cluster synchronization completely restored across all three television nodes.", None),
        ("Customer", "Every room in our home has seamless access again.", 36.8),
        ("Agent", "I have locked these cryptographic cluster keys in your master hub profile to ensure automated updates preserve synchronization permanently.", None),
        ("Customer", "That will protect us from any future overnight glitches.", 34.2),
        ("Agent", "I have documented the MoCA re-keying under master reference MR-COAX-100-FINALE.", None),
        ("Customer", "MR-COAX-100-FINALE, recorded in our household manual.", 32.4),
        ("Agent", "Please give my warmest wishes and heartfelt encouragement to your brave son for a speedy recovery, Zachary.", None),
        ("Customer", "I will tell him that Benjamin from S-Net saved his weekend.", 38.4),
        ("Agent", "It has been our absolute privilege and honor to assist you and your family today.", None),
        ("Customer", "You have delivered the most outstanding customer service I have ever experienced.", 39.2),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just making sure our premises records match perfectly: that was 25 Kingsway, Bath, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, 25 Kingsway, Bath.", 34.4),
        ("Agent", "Thank you Zachary, all premises and multi-room equipment records are fully verified.", None),
        ("Customer", "Thank you again Benjamin for your brilliant, compassionate, and life-changing support.", 38.4),
        ("Agent", "It has been an absolute pleasure assisting you, Zachary. Have a wonderful weekend with your son.", None),
        ("Customer", "Have a wonderful afternoon, Benjamin. Goodbye.", 34.2),
        ("Agent", "Is there any other TV or broadband issue I can assist you with today, Zachary?", None),
        ("Customer", "No Benjamin, everything is working flawlessly.", 32.2),
        ("Agent", "Thank you for calling S-Net TV technical support, Zachary. Goodbye.", None),
        ("Customer", "Goodbye Benjamin.", 30.4),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 26.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 22.0),
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
        "Personalized the call/ticket appropriately": "Agent addressed customer as Zachary throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent handled two separate customer emotional outbursts with profound empathy and reassuring warmth at turns 16 and 22, and no unhandled outbursts occurred.",
        "Paraphrasing": "Agent accurately paraphrased the multi-room whole-home recording sharing desynchronization issue at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer address at turn 42.",
        "Took ownership of the problem": "Agent executed MoCA cluster re-keying, locked cluster encryption keys, and verified multiple mini boxes live on call.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, warm, and highly supportive professional demeanor throughout.",
        "Probing": "Agent probed about coaxial MoCA cabling versus Wi-Fi connectivity.",
        "Confirmed the issue is resolved": "Customer tested both bedroom mini boxes live on call, loaded full recording library, and streamed Doctor Who smoothly at 850 Mbps."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 44}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 2},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 21}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 15, "agent_turn": 18, "with_refusal": True},
            {"kind": "handled", "customer_turn": 23, "agent_turn": 24, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_100",
        "cname": "Zachary",
        "target_dur": 1175,
        "scenario": "Multi-Room TV whole-home recording sharing desynchronized with error MR-SYNC-404; resolved via MoCA 2.5 cluster re-keying; two handled outbursts; grand finale call",
        "tier": "excellent",
        "expected_score": 100.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": [],
        "notes": "Grand finale call: flawless 100/100 support call featuring two handled outbursts with deep empathy, remote MoCA cluster re-keying, harmless recheck in final third, and complete multi-room live playback verification."
    }

print("get_call_100 defined.")

if __name__ == "__main__":
    for fn in [get_call_096, get_call_097, get_call_098, get_call_099, get_call_100]:
        c = fn()
        compile_call(c)
