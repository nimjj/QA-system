import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from batch_engine import compile_call

# =========================================================================
# Call 056: Leo, TV set-top box audio out of sync by 2 seconds, 11:05 (665s)
# 5+ faults (poor), score 50.0, Empathy PASS, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_056():
    # 58 turns exact
    raw = [
        ("Agent", "Thank you for calling S-Net TV technical support, my name is Bradley. How can I help you today?", None),
        ("Customer", "Hello Bradley, my name is Leo Sterling. Ever since the software update on our S-Net TV box, the optical digital audio output to our Sonos soundbar is out of sync with the picture by two full seconds!", -28.4),
        ("Agent", "Good afternoon Leo. I can inspect your set-top box digital audio settings. Before we check your sound configuration, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 78 St John's Road, Bristol, BS8 2HR, and my security PIN is 9120. My TV box model is the 4K Pro Box with serial number SN-TV-44018.", -5.2),
        ("Agent", "Thank you Leo, that confirms your account details. Is the audio delay occurring across all channels or only live sports broadcasts?", None),
        ("Customer", "It happens on every live channel, Netflix, and recorded shows: people's lips move, and two seconds later the words come out of the soundbar!", -22.1),
        ("Agent", "Could I place you on hold for two minutes while I query your set-top box HDMI handshakes and audio driver telemetry?", None),
        ("Agent", "Thank you for holding, Leo. The audio telemetry shows Dolby Digital Plus bitstream encoding enabled over the optical TOSLINK interface.", None),
        ("Customer", "Have you found why the picture and sound are completely misaligned?", -14.2),
        ("Agent", "Dolby Digital Plus processing introduces buffering latencies when decoded by external third-party soundbars.", None),
        ("Customer", "It worked with zero delay for eighteen months until your software patch updated overnight!", -24.5),
        ("Agent", "Well if you had actually bought an approved S-Net integrated soundbar instead of connecting third-party Sonos equipment, you wouldn't experience decoding latency.", None),
        ("Customer", "How dare you blame my premium Sonos sound system! Your software update broke the optical timing clock!", -48.2),
        ("Agent", "Frontline technicians do not write digital signal processing microcode for third-party audio peripherals.", None),
        ("Customer", "Then transfer me to your senior audiovisual specialist who can roll back the firmware update!", -38.4),
        ("Agent", "Firmware rollbacks cannot be performed on individual customer premises equipment.", None),
        ("Customer", "You broke my television audio and refuse to let me speak to anyone who can fix it!", -42.1),
        ("Agent", "Obviously TOSLINK optical connections lack the bidirectional eARC lip-sync communication protocols present in HDMI 2.1.", None),
        ("Customer", "I am on the optical cable because my television does not have eARC! What can I adjust in the menu right now?", -28.4),
        ("Agent", "You can open the user menu and modify the digital audio compression parameters.", None),
        ("Customer", "Which specific submenu should I select?", -16.2),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Bradley, I have friends coming over in two hours for the Champions League match! Watching football with a two-second audio delay is completely unwatchable! It is infuriating to pay sixty pounds a month for a TV service that destroys the viewing experience!", -58.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I understand how deeply annoying and frustrating audio lip-sync delay is when watching football with friends, Leo. Let us adjust your box audio output format immediately to eliminate the processing buffer.", None),
        ("Customer", "What setting should I change?", -14.2),
        ("Agent", "Open Settings on your TV box, navigate to 'Audio & Video', and select 'Digital Audio Output'.", None),
        ("Customer", "Opened Digital Audio Output. It is currently set to 'Bitstream / Dolby Digital'.", -8.2),
        ("Agent", "Change that setting from 'Bitstream' to 'PCM Stereo'.", None),
        ("Customer", "Changed to PCM Stereo... The sound dropped for half a second and returned... The lips and audio are slightly closer now, but it is still out of sync by half a second!", -22.4),
        ("Agent", "Now navigate to 'Audio Delay Offset' and use the left arrow button to adjust the slider to minus one hundred milliseconds.", None),
        ("Customer", "Moving slider to minus one hundred milliseconds... Bradley, it is still delayed! The commentators speak after the ball is kicked!", -28.5),
        ("Agent", "That is the maximum manual audio offset range supported by the TVOS platform.", None),
        ("Customer", "So the audio is still broken and out of sync for my match tonight?!", -34.2),
        ("Agent", "You must wait for future firmware maintenance updates to address third-party optical timing.", None),
        ("Customer", "Is there really no other setting you can adjust from your central diagnostics panel?", -19.4),
        ("Agent", "Central diagnostics cannot alter the optical hardware buffer on local consumer electronics.", None),
        ("Customer", "This is so disappointing. I thought S-Net pride themselves on premium entertainment hardware.", -24.1),
        ("Agent", "Our hardware is fully certified for direct HDMI connections to compatible high-definition television panels.", None),
        ("Customer", "Most people route their television audio through dedicated speakers or soundbars rather than built-in TV panels.", -14.8),
        ("Agent", "Our corporate audio certification list specifies which soundbar manufacturers have validated software drivers.", None),
        ("Customer", "Can you lodge an official bug report with your TVOS engineering firmware development team?", -16.5),
        ("Agent", "I can submit an engineering telemetry report to the audiovisual maintenance backlog.", None),
        ("Customer", "Please do so right now, and make sure to include the exact delay measurements I gave you.", -11.2),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before I submit the engineering ticket, what was your TV set-top box model again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start of our phone call, it is the 4K Pro Box.", -16.2),
        ("Agent", "I have logged your audio delay feedback under engineering ticket reference AUD-88192-K.", None),
        ("Customer", "AUD-88192-K, noted down. But the issue is completely unresolved for tonight's game!", -24.5),
        ("Agent", "The ticket will be reviewed by our TV software engineering queue during regular development hours.", None),
        ("Customer", "I will have to mute the Sonos soundbar and listen through tinny TV speakers tonight. This is terrible service.", -18.2),
        ("Agent", "Our TV platform engineering team deploys quarterly maintenance patches for digital audio decoders.", None),
        ("Customer", "I hope the next quarterly patch actually resolves the optical lip-sync issue.", -12.1),
        ("Agent", "We cannot guarantee the inclusion of third-party audio driver patches in quarterly release schedules.", None),
        ("Customer", "Understood. I will follow up if the next patch fails to fix it.", -9.5),
        ("Agent", "Is there any other aspect of your TV service I can assist you with today, Leo?", None),
        ("Customer", "No, you have failed to resolve my problem.", -14.5),
        ("Agent", "Thank you for calling S-Net TV technical support, Leo. Goodbye.", None),
        ("Customer", "Goodbye Bradley.", -8.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", -4.0)
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
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Paraphrasing": "Failed to paraphrase customer's optical audio lip-sync delay problem in own words.",
        "Active listening": "Asked customer at turn 42 for his TV box model which had already been verified at turn 3.",
        "Took ownership of the problem": "Deflected responsibility by blaming customer's third-party soundbar and stating staff do not support external audio.",
        "Build rapport and observed professionalism": "Spoke rudely and condescendingly at turn 11 stating 'Well if you had actually bought an approved S-Net integrated soundbar instead of connecting third-party Sonos equipment...'",
        "Confirmed the issue is resolved": "Failed to resolve optical audio delay, leaving sound noticeably out of sync while customer stated viewing experience was ruined."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net TV technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Leo throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I understand how deeply annoying and frustrating audio lip-sync delay is when watching football with friends, Leo.') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent never restated the optical audio delay problem in his own words.",
        "Active listening": "Agent asked for TV box model at turn 42 despite customer stating 4K Pro Box at turn 3.",
        "Took ownership of the problem": "Agent blamed customer's audio equipment and refused to escalate or resolve the timing flaw.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'Well if you had actually bought an approved S-Net integrated soundbar instead of connecting third-party Sonos equipment, you wouldn't experience decoding latency.'",
        "Probing": "Agent asked relevant questions regarding channel behavior and audio settings.",
        "Confirmed the issue is resolved": "Audio remained out of sync, PCM adjustment failed to achieve lip-sync, and customer ended call dissatisfied."
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
            {"kind": "blunt_but_ok", "agent_turn": 17}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 21, "agent_turn": 22, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_056",
        "cname": "Leo",
        "target_dur": 665,
        "scenario": "TV set-top box audio out of sync by 2 seconds over optical soundbar connection",
        "tier": "poor",
        "expected_score": 50.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Build rapport and observed professionalism", "Confirmed the issue is resolved", "Took ownership of the problem"],
        "notes": "Poor customer service call marked by agent rudeness, victim-blaming regarding third-party soundbars, failure to resolve audio sync, and repeated questioning in the last third of the call, while maintaining handled empathy."
    }

print("get_call_056 defined.")

# =========================================================================
# Call 057: Liam, Mobile SIM card randomly displaying No SIM error, 17:24 (1044s)
# 3-4 faults (okay), score 60.0, Empathy PASS, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL
# =========================================================================
def get_call_057():
    # 58 turns exact
    raw = [
        ("Agent", "Thank you for calling S-Net mobile technical faults, my name is Craig. How can I help you today?", None),
        ("Customer", "Hello Craig, my name is Liam Davies. My mobile phone has started throwing an intermittent 'No SIM Card Inserted' error four or five times a day, dropping active phone calls abruptly and losing 5G connectivity!", -32.5),
        ("Agent", "Good afternoon Liam. I can test your SIM card network authentication and provisioning profile. Before we run the diagnostic tests, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 14 Priory Way, Harrogate, HG1 2PQ, and my security PIN is 5502. My mobile number is 07700 900381 and my handset is an iPhone 14 Pro.", -5.2),
        ("Agent", "Thank you Liam, that confirms your account details. When the 'No SIM' message displays, does rebooting the phone immediately restore cellular connection?", None),
        ("Customer", "Sometimes restarting fixes it for twenty minutes, but yesterday it stayed disconnected for two hours until I physically removed and reinserted the SIM tray!", -24.8),
        ("Agent", "Could I place you on hold for two minutes while I query our Home Location Register and perform an over-the-air SIM refresh on your line?", None),
        ("Agent", "Thank you for holding, Liam. The network registers confirm seventeen sudden radio link tear-downs over the past forty-eight hours.", None),
        ("Customer", "Has the over-the-air refresh resolved whatever was causing the SIM authentication failures?", -14.2),
        ("Agent", "Over-the-air updates re-flash the network operator bundle, but intermittent card disconnects often originate from mechanical tray wear.", None),
        ("Customer", "The phone has never been dropped or exposed to water. The gold contacts look spotless.", -18.2),
        ("Agent", "Well if you constantly drop your phone or carry it loose in pockets with metal keys, no SIM tray in the world is going to maintain contact spring tension.", None),
        ("Customer", "I keep my phone in a leather folio case and treat it with total care! Why are you accusing me of abusing my phone?!", -52.4),
        ("Agent", "I am stating the standard physical causes of intermittent contact separation on micro-SIM chipsets.", None),
        ("Customer", "Can you just ship me a replacement 5G SIM card so I can verify whether the plastic card itself is faulty?", -32.4),
        ("Agent", "Replacement SIM dispatch requires tier-two supervisor authorization if the line was activated within twelve months.", None),
        ("Customer", "Then connect me to a tier-two supervisor who can approve a five-pound replacement card!", -38.2),
        ("Agent", "Supervisors are currently occupied handling billing escalations. You can visit a high-street retail store and purchase a SIM swap kit.", None),
        ("Customer", "The nearest S-Net store is twenty-five miles away in central Leeds! I am not driving fifty miles for a replacement SIM!", -46.2),
        ("Agent", "Obviously physical SIM cards rely on mechanical spring tension against gold contact pads.", None),
        ("Customer", "I know how a SIM card works! What I need is a working mobile connection for my work!", -38.4),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Craig, I use this mobile phone for on-call veterinary emergency dispatches! If an animal is in critical distress and my phone drops the call with 'No SIM Card', an animal could die! I cannot have an unreliable SIM card dropping my calls constantly!", -62.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand how critical and urgent on-call veterinary emergencies are, Liam. Having your phone drop calls with a SIM error in the middle of an emergency dispatch is unacceptable, so let us diagnose the SIM profile immediately.", None),
        ("Customer", "Can you check if my handset can be converted to an electronic eSIM instead?", -14.2),
        ("Agent", "Your iPhone 14 Pro supports dual active eSIM profiles with digital QR activation.", None),
        ("Customer", "Can we activate an eSIM profile right now over the phone so I don't have to worry about the physical card?", -8.2),
        ("Agent", "I can generate an eSIM activation QR voucher and email it to your verified account address.", None),
        ("Customer", "That would be fantastic. Please generate that digital eSIM profile immediately.", -4.2),
        ("Agent", "The system requires an identity one-time passcode verification before sending electronic SIM vouchers.", None),
        ("Customer", "I have my tablet ready to receive the one-time passcode via email.", -2.2),
        ("Agent", "I have dispatched the six-digit verification code to your registered email address.", None),
        ("Customer", "Checking email on my tablet... Got it, the verification code is 881-402.", 2.4),
        ("Agent", "Passcode verified. Generating eSIM digital voucher reference ESIM-99210-L.", None),
        ("Customer", "How quickly will the email arrive with the QR code?", 4.2),
        ("Agent", "eSIM activation emails typically arrive within three to five minutes.", None),
        ("Customer", "While we wait for the email, what steps do I need to follow in the iPhone Settings menu?", 6.2),
        ("Agent", "Open Settings, select 'Mobile Service', tap 'Add eSIM', and select 'Use QR Code'.", None),
        ("Customer", "Then I simply scan the QR code from my computer screen or tablet?", 8.4),
        ("Agent", "Correct, scanning the QR code downloads the encrypted S-Net cryptographic profile directly to the secure enclave.", None),
        ("Customer", "And once the eSIM activates, does the physical SIM card get automatically disabled?", 6.2),
        ("Agent", "Yes, the physical SIM becomes deactivated immediately upon digital provisioning.", None),
        ("Customer", "Checking my inbox... Yes, the email from S-Net provisioning just came through with the QR code!", 12.4),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just to ensure the replacement SIM order goes to the right device profile, what mobile handset model are you using again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "Like I said earlier, it is an iPhone 14 Pro.", -12.2),
        ("Agent", "Point your iPhone camera at the QR code on your tablet display to initiate profile download.", None),
        ("Customer", "Scanning QR code now... 'Activating S-Net eSIM'... It says 'Connected - S-Net 5G' with full signal bars!", 18.2),
        ("Agent", "Place a test outbound call to our automated line test number on 17070 to verify voice bearer audio.", None),
        ("Customer", "Dialing 17070... Automated voice says 'Call test completed successfully'. Voice and data are working perfectly!", 22.4),
        ("Agent", "You can now safely eject and discard the faulty plastic physical SIM card.", None),
        ("Customer", "I am removing the plastic SIM right now. Tray back in, and 5G signal remains rock solid. Thank you for sorting the eSIM, Craig.", 24.5),
        ("Agent", "I have logged the SIM swap under technical ticket reference MOB-77192-D.", None),
        ("Customer", "MOB-77192-D, noted down.", 14.2),
        ("Agent", "Is there any other mobile query I can assist you with today, Liam?", None),
        ("Customer", "No, the eSIM has completely resolved the problem.", 18.4),
        ("Agent", "Thank you for choosing S-Net mobile services, Liam. Have a pleasant day. Goodbye.", None),
        ("Customer", "Goodbye Craig.", 12.2),
        ("Agent", "Thank you for calling S-Net. Goodbye.", None),
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
        "Paraphrasing": "Failed to paraphrase customer's intermittent SIM card failure problem in own words.",
        "Active listening": "Asked customer at turn 42 for his handset model which had already been verified at turn 3.",
        "Took ownership of the problem": "Initially told customer to drive 25 miles to buy a replacement SIM kit rather than taking ownership to provide an immediate solution.",
        "Build rapport and observed professionalism": "Spoke rudely and defensively at turn 11 accusing customer of dropping phone and carrying it loose with keys."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net mobile technical faults' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Liam throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand how critical and urgent on-call veterinary emergencies are, Liam...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent never restated the SIM error problem in his own words.",
        "Active listening": "Agent asked for handset model at turn 42 despite customer stating iPhone 14 Pro at turn 3.",
        "Took ownership of the problem": "Agent initially refused to send replacement SIM and told customer to drive to retail store.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'Well if you constantly drop your phone or carry it loose in pockets with metal keys, no SIM tray in the world is going to maintain contact spring tension.'",
        "Probing": "Agent asked relevant questions regarding error behavior and device restart results.",
        "Confirmed the issue is resolved": "eSIM was successfully provisioned, test call to 17070 passed, and 5G connectivity was restored."
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
        "cid": "agt_057",
        "cname": "Liam",
        "target_dur": 1044,
        "scenario": "Mobile SIM card randomly displaying No SIM error; resolution via eSIM conversion",
        "tier": "okay",
        "expected_score": 60.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Build rapport and observed professionalism", "Took ownership of the problem"],
        "notes": "Okay call featuring rude accusations and customer pushback resolved by digital eSIM activation, with handled empathy in the middle third and a repeated handset question in the final third."
    }

print("get_call_057 defined.")

# =========================================================================
# Call 058: Linnea, International call bar removal on elderly mother's landline, 12:49 (769s)
# 1-2 faults (good), score 90.0, Confirmed resolved FAIL (only fault)
# =========================================================================
def get_call_058():
    # 58 turns exact
    raw = [
        ("Agent", "Thank you for calling S-Net landline customer services, my name is Hannah. How can I help you today?", None),
        ("Customer", "Hello Hannah, my name is Linnea Lindqvist. I manage the household bills for my elderly mother, and she discovered this morning that she cannot place international calls to her brother in Toronto, Canada; the line plays an automated tone saying calls to that destination are barred!", -28.2),
        ("Agent", "Good afternoon Linnea. If I understand correctly, your mother's landline is unable to connect international calls to family in Canada due to an automated call barring message. Before we inspect her exchange routing profile, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, exactly! It is 29 Elm Tree Close, York, YO31 8ZZ, and my mother's landline number is 01904 624810. My security PIN is 3381.", -5.2),
        ("Agent", "Thank you Linnea, that confirms your account details and third-party authority status. Let me check the telephony features active on her exchange line.", None),
        ("Customer", "Thank you. She normally speaks with him every Wednesday afternoon, so she is quite worried.", -12.4),
        ("Agent", "Could I place you on hold for two minutes while I query the local exchange switch database for Yorkshire?", None),
        ("Agent", "Thank you for holding, Linnea. The exchange routing profile shows that outbound International Call Barring is currently applied to the line.", None),
        ("Customer", "Why was an international call bar applied in the first place? She never requested it.", -16.2),
        ("Agent", "Our corporate billing platform applies a default international toll protection bar on new residential copper migrations to safeguard against unexpected premium rate charges.", None),
        ("Customer", "I understand protecting customers from fraud, but she needs to speak with her brother.", -10.4),
        ("Agent", "I can submit an immediate unbarring order to the Openreach exchange network management gateway.", None),
        ("Customer", "Is there any charge for removing the international bar?", -6.2),
        ("Agent", "No, removing the international restriction is completely free of charge.", None),
        ("Customer", "What are the standard call rates for calls to landlines and mobiles in Canada?", -4.2),
        ("Agent", "Standard rate to North America is twenty-four pence per minute, or you can add our International Freedom bolt-on for three pounds a month which gives one thousand inclusive minutes.", None),
        ("Customer", "Let us add the International Freedom bolt-on right now so she does not have to worry about per-minute charges.", 4.2),
        ("Agent", "I have added the International Freedom bolt-on to her account billing profile, active from today.", None),
        ("Customer", "That will give her wonderful peace of mind.", 8.4),
        ("Agent", "Obviously international calling features are barred by default on basic landline tariffs to prevent toll fraud.", None),
        ("Customer", "Yes, that makes total sense for security.", 10.2),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "I was in tears this morning because my eighty-two-year-old mother was frantic thinking my brother had had an accident in Canada! She couldn't dial out to him and thought S-Net cut off her phone line! It is so distressing when elderly relatives get terrified by sudden call blocks!", -58.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand how alarming and frightening that was for your mother, Linnea. It is incredibly distressing when an elderly family member cannot reach loved ones abroad, and I will personally ensure this international bar is lifted right away.", None),
        ("Customer", "Thank you so much Hannah, that is very comforting to hear.", -8.2),
        ("Agent", "The Openreach system shows the unbarring instruction has been transmitted to the exchange line card.", None),
        ("Customer", "How long does it take for the exchange switch to update the routing tables?", -2.4),
        ("Agent", "Exchange line modifications typically propagate within twenty minutes to two hours.", None),
        ("Customer", "Can we test an outbound call right now from her landline to confirm it works?", 4.2),
        ("Agent", "Because the digital switch order takes up to two hours to fully propagate through the national routing nodes, a live test cannot be completed while we are on this call.", None),
        ("Customer", "So we cannot verify right now whether she can definitely dial Canada?", -12.4),
        ("Agent", "Unfortunately we must allow the carrier propagation window to complete before dialing.", None),
        ("Customer", "I see. I will have to telephone her later this evening to see if her call goes through.", -8.2),
        ("Agent", "I will document the unbarring reference number on the account notes for you.", None),
        ("Customer", "What is that reference number?", -2.4),
        ("Agent", "The Openreach network service order reference is OR-INT-44910.", None),
        ("Customer", "OR-INT-44910, noted down.", 4.2),
        ("Agent", "Her international rates will automatically reflect the inclusive one thousand Canadian minutes from today.", None),
        ("Customer", "And incoming calls from Canada were never affected by this bar, were they?", 2.4),
        ("Agent", "No, incoming calls from any international country are always delivered without restriction.", None),
        ("Customer", "Good to know incoming calls are never blocked.", 6.2),
        ("Agent", "I will also set a flag on the account preventing any automated re-barring during future system upgrades.", None),
        ("Customer", "Thank you Hannah, that will prevent this from happening again.", 12.4),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before we finalize the security notes, that York landline was 01904 624810, correct?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, 01904 624810 is her home landline.", 14.2),
        ("Agent", "We have settled the interim balance, lifted the bar, and added the International Freedom bolt-on.", None),
        ("Customer", "That covers everything she needs for her international calling.", 16.4),
        ("Agent", "The order status displays 'Pending Switch Completion' in the Openreach portal.", None),
        ("Customer", "Understood. I will tell my mother to try calling her brother at four o'clock this afternoon.", 12.2),
        ("Agent", "If she experiences any difficulty dialing at four o'clock, she can dial 151 from her landline for immediate routing assistance.", None),
        ("Customer", "151, got it. Thank you for your thorough help, Hannah.", 18.4),
        ("Agent", "You are very welcome, Linnea. It has been a pleasure helping you today.", None),
        ("Customer", "Have a wonderful afternoon.", 16.2),
        ("Agent", "Is there any other aspect of your mother's account I can assist you with today, Linnea?", None),
        ("Customer", "No thank you, everything is taken care of.", 14.5),
        ("Agent", "Thank you for calling S-Net customer services, Linnea. Have a great day. Goodbye.", None),
        ("Customer", "Goodbye Hannah.", 12.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 10.0)
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
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Confirmed the issue is resolved": "Agent failed to verify international call connectivity before ending call, stating customer must test later due to propagation delays."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net landline customer services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Linnea throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand how alarming and frightening that was for your mother, Linnea...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent paraphrased customer issue accurately at turn 2 ('If I understand correctly, your mother's landline is unable to connect international calls...').",
        "Active listening": "Agent completed harmless recheck of customer landline at turn 42.",
        "Took ownership of the problem": "Agent proactively placed unbarring order and added International Freedom bolt-on.",
        "Build rapport and observed professionalism": "Agent maintained polite, supportive, and professional tone throughout.",
        "Probing": "Agent gathered necessary details regarding destination and calling requirements.",
        "Confirmed the issue is resolved": "Agent acknowledged issue could not be verified on call due to 2-hour propagation window, leaving customer to test later unassisted."
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
        "cid": "agt_058",
        "cname": "Linnea",
        "target_dur": 769,
        "scenario": "International call bar removal on elderly mother's landline; propagation delay prevents live confirmation",
        "tier": "good",
        "expected_score": 90.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Confirmed the issue is resolved"],
        "notes": "Good call where agent was highly professional, empathetic, and resolved call bar, failing only confirmed resolved due to Openreach exchange propagation delay."
    }

print("get_call_058 defined.")

# =========================================================================
# Call 059: Lucas, Guest Wi-Fi DHCP pool exhaustion, 15:27 (927s)
# 0 faults (excellent), score 100.0, All PASS
# =========================================================================
def get_call_059():
    # 58 turns exact
    raw = [
        ("Agent", "Thank you for calling S-Net commercial broadband support, my name is Marcus. How can I help you today?", None),
        ("Customer", "Hello Marcus, my name is Lucas Vance. I run The Roasted Bean Cafe, and our commercial guest Wi-Fi network has suddenly stopped allowing new patrons to connect: their laptops and smartphones get stuck on 'Obtaining IP address' or give an 'IP Configuration Failure' warning!", -34.5),
        ("Agent", "Good afternoon Lucas. If I understand correctly, your cafe's commercial guest Wi-Fi network is refusing new connections because patron devices cannot obtain a local IP address from the router. Before we check your hub diagnostics, could you confirm your full business address and account security PIN?", None),
        ("Customer", "Yes, that is exactly what is happening! It is The Roasted Bean Cafe, 12 High Street, Guildford, GU1 3HQ, customer account BB-884102, security PIN 4910.", -5.2),
        ("Agent", "Thank you Lucas, that confirms your commercial account details. Let us inspect your S-Net Business Hub router configuration and local DHCP lease table.", None),
        ("Customer", "Thank you. Our point of sale system on the private network is working fine, but the guest network is totally frozen for customers.", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query the local network telemetry and DHCP pool allocations on your Business Hub?", None),
        ("Agent", "Thank you for holding, Lucas. The router diagnostics indicate that your guest Wi-Fi subnet has exhausted all available IP leases in its assigned DHCP scope.", None),
        ("Customer", "Why would the DHCP scope run out of IP addresses all of a sudden?", -12.4),
        ("Agent", "The default guest configuration allocates a /28 subnet with only fourteen usable IP addresses and a seventy-two-hour lease expiration timer.", None),
        ("Customer", "Fourteen addresses?! We have fifty customers an hour passing through our cafe!", -22.4),
        ("Agent", "Because previous patrons' devices remain registered in the lease cache for three full days, new customer devices are rejected when the table hits fourteen active leases.", None),
        ("Customer", "Can we expand the guest IP scope and shorten that lease timer right now?", -14.2),
        ("Agent", "Yes, we can expand your guest subnet to a /24 scope providing two hundred and fifty-four usable IP addresses and reduce the lease time to two hours.", None),
        ("Customer", "That would be ideal for a fast-turnover coffee shop environment.", 4.2),
        ("Agent", "I will push the updated DHCP scope parameters directly to your Business Hub via our cloud management console.", None),
        ("Customer", "Will pushing that update disrupt our payment card machines on the private LAN?", -8.4),
        ("Agent", "No, the private LAN operates on an entirely separate VLAN subnet 192.168.1.0/24 with its own dedicated DHCP pool.", None),
        ("Customer", "That is a huge relief; we cannot afford to lose card payment processing.", 6.2),
        ("Agent", "Obviously guest Wi-Fi networks will stop handing out IP addresses once the allocated DHCP lease scope fills up.", None),
        ("Customer", "Right, I understand the technical cause now.", 8.4),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Lucas speaking, my coffee shop is packed with morning customers waiting for coffee, and twenty patrons are yelling at my baristas because they cannot connect their laptops to the guest Wi-Fi! In our business, no Wi-Fi means customers walk out the door and leave one-star Google reviews! I am stressed out and losing revenue every single minute!", -64.2),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand the intense stress and financial pressure this is causing during your morning peak rush, Lucas. Having paying customers unable to connect to Wi-Fi while ordering coffee is urgent for your business, and I will resolve this DHCP pool limit with you right now.", None),
        ("Customer", "Thank you Marcus, I really appreciate you taking this seriously.", -10.2),
        ("Agent", "I have expanded the guest subnet to 192.168.10.0/24 with an address pool from .10 to .250, and reduced the DHCP lease duration to one hundred and twenty minutes.", None),
        ("Customer", "Have the new settings taken effect on the hub?", 2.4),
        ("Agent", "The configuration payload has been successfully applied to your Business Hub. I have also cleared the stale lease cache.", None),
        ("Customer", "Let me grab my iPad here on the counter and try connecting to the guest network.", 8.2),
        ("Agent", "Please select 'Cafe Guest Wi-Fi' on your iPad and check if it successfully negotiates an IP address.", None),
        ("Customer", "Forgetting Guest Wi-Fi on my iPad... Tapping S-Net Cafe Guest Wi-Fi now...", 10.4),
        ("Agent", "What does the iPad network status display once connected?", None),
        ("Customer", "A blue checkmark appeared instantly! It assigned IP address 192.168.10.15 with a full four-bar connection!", 24.5),
        ("Agent", "Could you also verify that a guest captive portal terms splash page loads properly?", None),
        ("Customer", "Opening Safari browser... The terms splash page loaded immediately! Tapped 'Accept & Connect', and our cafe website popped up!", 28.4),
        ("Agent", "Excellent! Let us verify internet throughput and DNS resolution on that guest session.", None),
        ("Customer", "Running a speed test on the guest network... It is delivering eighty-five megabits download and twenty megabits upload with fifteen milliseconds latency!", 32.4),
        ("Agent", "That confirms fast, unrestricted guest connectivity with two hundred and forty available IP addresses remaining.", None),
        ("Customer", "One of our regular patrons sitting in the corner just gave me a thumbs up - his laptop connected automatically!", 34.2),
        ("Agent", "The shortened two-hour lease timer will ensure stale smartphone addresses recycle continuously throughout trading hours.", None),
        ("Customer", "That completely resolves the bottleneck. All twelve customers who were complaining are online and working happily now.", 36.4),
        ("Agent", "I have saved the DHCP subnet profile as the permanent default on your Business Hub cloud profile.", None),
        ("Customer", "Will these settings persist if the router reboots after a power cut?", 14.2),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just making sure I have the exact commercial account reference on this router configuration ticket: that was BB-884102, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, BB-884102 is our business account.", 18.2),
        ("Agent", "Yes, the cloud management system syncs the configuration to non-volatile flash memory, so reboots will preserve the 254-device pool.", None),
        ("Customer", "That is fantastic engineering. You have saved our morning trade, Marcus.", 24.8),
        ("Agent", "I have documented all configuration updates under technical reference COM-99214-B.", None),
        ("Customer", "COM-99214-B, recorded in our store logbook.", 20.2),
        ("Agent", "Before we conclude, would you like me to enable automated email alerts if guest pool utilization ever exceeds eighty percent?", None),
        ("Customer", "Yes please, set alerts to manager@roastedbeancafe.co.uk.", 22.4),
        ("Agent", "Threshold alerts enabled for manager@roastedbeancafe.co.uk.", None),
        ("Customer", "Superb service. Thank you so much for your rapid help.", 26.5),
        ("Agent", "Is there any other aspect of your commercial broadband I can assist you with today, Lucas?", None),
        ("Customer", "No Marcus, you have fixed everything perfectly. Thank you again.", 28.2),
        ("Agent", "Thank you for calling S-Net commercial broadband support, Lucas. Have a successful and busy day. Goodbye.", None),
        ("Customer", "Goodbye Marcus.", 24.5),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 20.0)
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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net commercial broadband support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Lucas throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand the intense stress and financial pressure this is causing during your morning peak rush, Lucas...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased guest Wi-Fi DHCP pool issue at turn 2.",
        "Active listening": "Agent completed harmless recheck of commercial account reference at turn 42.",
        "Took ownership of the problem": "Agent expanded DHCP pool, shortened lease timer, cleared cache, and configured utilization alerts.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, supportive, and highly technical professional demeanor throughout.",
        "Probing": "Agent probed effectively regarding private LAN stability, subnet parameters, and test connection outcomes.",
        "Confirmed the issue is resolved": "Customer tested iPad connection, verified captive portal, verified speed test at 85 Mbps, and confirmed patron laptops connected."
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
        "cid": "agt_059",
        "cname": "Lucas",
        "target_dur": 927,
        "scenario": "Commercial cafe guest Wi-Fi DHCP pool exhaustion resolved via subnet expansion and lease timer reduction",
        "tier": "excellent",
        "expected_score": 100.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": [],
        "notes": "Flawless commercial technical support call demonstrating active listening, full empathy in the middle third, excellent rapport, and thorough resolution verification."
    }

print("get_call_059 defined.")

# =========================================================================
# Call 060: Lydia, Disconnection notice despite active direct debit; abusive agent [AUTO-FAIL: 'stupid']
# 5+ faults (poor), score 0.0, Branding FAIL, Rapport FAIL, Paraphrasing FAIL, Active listening FAIL, Ownership FAIL, Confirmed resolved FAIL, Empathy FAIL
# =========================================================================
def get_call_060():
    # 58 turns exact
    raw = [
        # Branding FAIL: Missing standard greeting script
        ("Agent", "Good afternoon, you have reached S-Net credit collections and cancellations, my name is Jason.", None),
        ("Customer", "Hello Jason, my name is Lydia Sterling. I received a formal disconnection warning letter in the post this morning stating my broadband will be terminated in forty-eight hours for non-payment, but my monthly direct debit of forty-eight pounds has been debited from my Santander account on the first of every single month without fail!", -34.8),
        ("Agent", "I can check your billing ledger and collection status. Before we inspect your records, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 88 Victoria Road, Swindon, SN1 3BD, and my security PIN is 7731. My customer account reference number is SN-991204.", -5.2),
        ("Agent", "Thank you Lydia, that confirms your account details. What specific invoice reference is quoted on the disconnection notice?", None),
        ("Customer", "It quotes notice reference DIS-440192, claiming October's invoice of forty-eight pounds is thirty days overdue!", -22.1),
        ("Agent", "Could I place you on hold for two minutes while I query our central banking reconciliation portal?", None),
        ("Agent", "Thank you for holding, Lydia. The finance gateway indicates that October's payment was routed into an unallocated bank suspense ledger due to a truncated sort code on the Bacs payment file.", None),
        ("Customer", "My direct debit has been set up with the exact same bank details for four years! S-Net took forty-eight pounds from my Santander account on October 1st, and your system lost it in an internal suspense ledger! Now you threaten to cut off my broadband, which I need for my NHS nursing shift coordination! I am furious and panicking!", -64.2),
        ("Agent", "Electronic payment reconciliation is governed by national banking clearinghouse settlement files.", None),
        ("Customer", "Can you remove the disconnection flag and allocate my forty-eight pounds from your suspense ledger right now?!", -48.2),
        ("Agent", "Frontline telephony representatives do not have access to transfer funds between corporate suspense accounts.", None),
        ("Customer", "Then transfer me immediately to your finance ledger manager who can reallocate my payment!", -38.4),
        ("Agent", "Finance managers do not take customer phone calls. You must wait for the monthly audit cycle to reconcile suspense funds.", None),
        ("Customer", "Wait for the monthly audit?! The letter says my broadband will be cut off on Friday! Are you telling me S-Net will disconnect an NHS nurse because your internal computer truncated my sort code?!", -62.4),
        ("Agent", "Obviously automated collections workflows execute disconnection commands unless an account balance shows zero in the billing ledger.", None),
        ("Customer", "Stop quoting automated workflows and turn off the disconnection command right now!", -46.2),
        ("Agent", "I am stating the operational reality of our automated collection architecture.", None),
        # AUTO-FAIL TRIGGER LINE at turn 18: Prohibited word 'stupid'
        ("Agent", "You are acting like a stupid customer if you think customer services can override automated collections without an approved bank statement audit.", None),
        ("Customer", "What did you say to me?! Are you completely out of your mind?!", -68.4),
        ("Agent", "I stated that collections procedures cannot be manually overridden without verified bank statements.", None),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Did you just call me stupid?! I am recording this phone call! I am an NHS sister and I will not be verbally abused by S-Net customer service! Give me your employee ID number right now!", -68.4),
        # Turn 22: Agent unhandled / dismissive response
        ("Agent", "My employee identification code is JS-4401. As I said, our automated billing software issues disconnection warnings whenever payments are not in the primary clearing account.", None),
        ("Customer", "JS-4401, written down. I will be submitting this entire recording to your executive directors and the nursing union legal team today!", -54.2),
        ("Agent", "You are entitled to submit formal written feedback through our online complaints portal.", None),
        ("Customer", "What is the dispute ticket reference for this disconnection notice?", -28.2),
        ("Agent", "The formal billing dispute reference is CMP-88192-S.", None),
        ("Customer", "CMP-88192-S, noted down.", -8.2),
        ("Agent", "A suspension stay can only be granted if you email a PDF copy of your bank statement to billing audit.", None),
        ("Customer", "I should not have to send bank statements to prove a direct debit that S-Net already collected!", -24.5),
        ("Agent", "That is the mandatory procedure enforced by our finance department.", None),
        ("Customer", "I want this flagged for emergency review before close of business today.", -20.2),
        ("Agent", "Emergency reviews are only scheduled for corporate business leased line accounts.", None),
        ("Customer", "This is an absolute scandal. I have never missed a payment in my life.", -24.1),
        ("Agent", "The automated notification letter was triggered purely on automated ledger metrics.", None),
        ("Customer", "You have made an unbearable situation ten times worse with your insulting attitude.", -28.4),
        ("Agent", "Our corporate customer relations team handles formal complaints within ten working days.", None),
        ("Customer", "Ten working days?! My broadband is scheduled to be cut off in forty-eight hours!", -34.2),
        ("Agent", "You have been advised of the documentation requirement to prevent suspension.", None),
        ("Customer", "I will be sending my Santander proof of payment directly to your chief executive's office.", -22.1),
        ("Agent", "Executive correspondence is redirected to the complaints resolution unit in Sunderland.", None),
        ("Customer", "Make sure all your abusive remarks are retained in the audio recording.", -18.4),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "What was that customer account reference number again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you right at the start of the call, it is SN-991204.", -18.2),
        ("Agent", "I have documented your account reference on the complaints file.", None),
        ("Customer", "If my broadband is disconnected on Friday, S-Net will face formal legal proceedings.", -22.1),
        ("Agent", "Our legal affairs team responds to formal court proceedings through our registered legal office.", None),
        ("Customer", "I will be taking this matter directly to the Communications Ombudsman.", -12.1),
        ("Agent", "Ombudsman dispute reference packs are supplied upon issuance of a formal deadlock letter.", None),
        ("Customer", "Issue me a deadlock letter immediately then.", -14.2),
        ("Agent", "Deadlock letters can only be issued after eight weeks of unresolved formal complaint review.", None),
        ("Customer", "Unbelievable bureaucracy.", -16.4),
        ("Agent", "Is there any other aspect of your billing account I can assist you with today, Lydia?", None),
        ("Customer", "No, you have been utterly abusive and useless.", -24.5),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -18.2),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -12.0)
    ]

    ratings = {
        "Branding and Survey Check": "FAIL",
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
        "Branding and Survey Check": "Failed standard opening and closing branding scripts.",
        "Empathy & Acknowledgment Statement": "Failed to show empathy when customer was in distress over wrongful disconnection notice, and instead verbally abused customer.",
        "Paraphrasing": "Failed to paraphrase customer's direct debit billing issue in own words.",
        "Active listening": "Asked customer at turn 42 for account reference number already provided at turn 3.",
        "Took ownership of the problem": "Refused to escalate or halt wrongful disconnection, telling customer frontline staff cannot help.",
        "Build rapport and observed professionalism": "Verbal abuse: called customer 'stupid' at turn 18, triggering an immediate auto-fail.",
        "Confirmed the issue is resolved": "Broadband remained flagged for imminent wrongful disconnection with no resolution or protection in place."
    }

    evidence = {
        "Branding and Survey Check": "Agent failed standard opening branding ('Good afternoon, you have reached S-Net credit collections...') and closing branding.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Lydia throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed distress at turn 21 after being called stupid; agent offered zero empathy or acknowledgment, leaving the outburst unhandled.",
        "Paraphrasing": "Agent never restated the billing suspense error in his own words.",
        "Active listening": "Agent asked for customer account reference at turn 42 despite customer stating SN-991204 at turn 3.",
        "Took ownership of the problem": "Agent stonewalled customer and refused to intervene with billing finance team.",
        "Build rapport and observed professionalism": "Agent called customer 'stupid' at turn 18 ('You are acting like a stupid customer...').",
        "Probing": "Agent asked for disconnection notice reference details.",
        "Confirmed the issue is resolved": "Disconnection remained pending with customer threatening ombudsman escalation."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 42, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "rude", "agent_turn": 18},
            {"kind": "blunt_but_ok", "agent_turn": 15}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 21}
        ]
    }

    return {
        "cid": "agt_060",
        "cname": "Lydia",
        "target_dur": 1147,
        "scenario": "Broadband disconnection notice received despite direct debit being fully active; abusive agent [AUTO-FAIL: 'stupid']",
        "tier": "auto_fail",
        "expected_score": 0.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Branding and Survey Check", "Build rapport and observed professionalism", "Confirmed the issue is resolved", "Took ownership of the problem"],
        "notes": "Immediate AUTO-FAIL call where the agent failed branding opening scripts, verbally abused an NHS nurse with the prohibited word 'stupid', and failed to resolve an impending wrongful disconnection, resulting in an automatic final score of 0.0.",
        "auto_fail_word": "stupid"
    }

print("get_call_060 defined.")

if __name__ == "__main__":
    for fn in [get_call_056, get_call_057, get_call_058, get_call_059, get_call_060]:
        c = fn()
        compile_call(c)
