import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from batch_engine import compile_call

# =========================================================================
# Call 091: Tariq, Mobile data roaming blocked in Europe, 10:45 (645s)
# 6+ faults (poor), score 11.7, Dead Air FAIL, Verified FAIL, Personalized FAIL, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Probing FAIL, Confirmed resolved FAIL
# Features TWO outbursts (turn 8 handled, turn 21 unhandled)
# =========================================================================
def get_call_091():
    raw = [
        ("Agent", "Thank you for calling S-Net mobile roaming support, my name is Jason. How can I help you today?", None),
        ("Customer", "Hello, my name is Tariq Mansoor. I landed at Frankfurt Airport in Germany two hours ago for an urgent European trade exhibition, but my mobile data roaming is completely blocked and shows 'PDP authentication failure', leaving me stranded with no maps, no email, and no connection!", -45.2),
        # Paraphrasing FAIL: agent does not restate; Verified FAIL: agent fails to ask for PIN/address/security question
        ("Agent", "I can query the European roaming subscriber registers. What is the mobile phone number and account number?", None),
        ("Customer", "My mobile number is 07700 900381, account number SN-881920, registered to 14 Wellington Street, Slough, SL1 1YP, security PIN 5521.", -12.4),
        # Personalized FAIL: agent never uses "Tariq" anywhere in call
        ("Agent", "Let me open mobile subscriber record 07700 900381 on the international gateway.", None),
        ("Customer", "Please check why mobile data is barred.", -18.2),
        ("Agent", "Could I place you on hold for two minutes while I query the Deutsche Telekom roaming partner HLR database?", None),
        ("Agent", "Thank you for holding. The international roaming database indicates that an automated roaming cap bar was applied.", None),
        # Outburst 1 at turn 8 (handled)
        ("Customer", "An automated roaming cap bar?! I specifically paid forty pounds last week for the unlimited European Roaming Pass before leaving the UK! Why did S-Net take my forty pounds and then bar my data the moment my plane touched down?! This is sheer incompetence!", -72.4),
        # Agent handled empathy 1 at turn 9
        ("Agent", "I completely understand your frustration and anger, especially having paid forty pounds for the European Roaming Pass in advance and arriving in Frankfurt only to find your data barred. Let us get this restriction lifted so your mobile data connects immediately.", None),
        ("Customer", "Thank you Jason, please lift it immediately.", -8.2),
        # Turn 11: diagnostic remark
        ("Agent", "International cellular handovers require clearance from foreign host network servers.", None),
        ("Customer", "Deutsche Telekom is Germany's largest network; it should take seconds to clear.", -14.2),
        ("Agent", "I am stating that international data tariffs require proper device provisioning.", None),
        # Turn 14 is dead air gap 1 (40s)
        ("Customer", "Jason? Are you still on the phone? The line went completely dead for forty seconds!", -28.4),
        ("Agent", "I was waiting for the roaming gateway interface to respond.", None),
        ("Customer", "Can you remove the cap bar from my SIM card right now?", -22.4),
        ("Agent", "Obviously international cellular handovers require clearance from foreign host network servers.", None),
        ("Customer", "Deutsche Telekom is Germany's largest network; it should take seconds to clear.", -14.2),
        ("Agent", "I am sending a roaming bar removal command to the Frankfurt gateway.", None),
        ("Customer", "How long will that command take to execute?", -18.4),
        # Outburst 2 at turn 21: Customer second outburst in middle third (unhandled)
        ("Customer", "I am the managing director of a renewable energy manufacturing firm, and in thirty minutes I have a live pitch presentation to German infrastructure investors at the Frankfurt Messe convention center! The presentation deck, my client contact files, and the venue entry QR codes are all stored in our cloud drive! If I cannot access my data, our multi-million-euro investment deal will collapse and thirty jobs in our factory will be lost! I am having a severe panic attack!", -88.4),
        # Turn 22: Agent MISSED/UNHANDLED empathy (agent completely ignores panic and talks about APN)
        ("Agent", "You should check your Access Point Name settings in your smartphone mobile data menu.", None),
        ("Customer", "Did you even hear what I just said about thirty factory jobs and an investment deal?! You don't give a damn about my crisis!", -78.4),
        # Rapport FAIL at turn 24 (middle third)
        ("Agent", "If you travel across Europe on multi-million-euro business without verifying international roaming in advance, that is your own reckless carelessness.", None),
        ("Customer", "Fine! What should the APN be set to?", -44.2),
        ("Agent", "The APN field should be set to 'mobile.snet.co.uk' with username blank.", None),
        ("Customer", "Entering 'mobile.snet.co.uk' into APN... Saving profile...", -12.4),
        ("Agent", "Now restart your smartphone to initiate re-authentication with Deutsche Telekom.", None),
        ("Customer", "Restarting phone now... Screen is rebooting...", -8.2),
        ("Agent", "The gateway will attempt to re-provision the data session.", None),
        ("Customer", "Phone has rebooted... Signal bars show 'Telekom.de 4G' but there is an exclamation mark next to data and web pages still won't load!", -34.2),
        # Turn 34 is dead air gap 2 (40s)
        ("Customer", "Jason?! Hello?! Did you put me on mute again?! Why do you keep vanishing for forty seconds?!", -44.2),
        ("Agent", "I was polling the Frankfurt roaming switch for an authentication handshake.", None),
        ("Customer", "Why is data still blocked?", -24.2),
        ("Agent", "The international partner switch requires up to four hours to propagate bar removals across European cellular towers.", None),
        ("Customer", "Four hours?! My investor meeting starts in fifteen minutes!", -48.2),
        ("Agent", "There is no way to bypass foreign carrier propagation cycles.", None),
        ("Customer", "Can I connect to Frankfurt Airport Wi-Fi in the meantime?", -14.2),
        ("Agent", "Airport Wi-Fi is managed by the airport operator.", None),
        ("Customer", "This has been an absolute disaster.", -38.2),
        # Turn 42: Active listening repeat in last third (42 is Customer answer, 41 is Agent)
        ("Agent", "Before we conclude, what was that mobile phone number again?", None),
        ("Customer", "As I told you right at the start of our call, it is 07700 900381.", -18.2),
        ("Agent", "Thank you, mobile number confirmed.", None),
        ("Customer", "Can you provide a ticket number for the complaint?", -12.4),
        ("Agent", "Your roaming ticket reference is ROAM-ERR-88192-F.", None),
        ("Customer", "ROAM-ERR-88192-F.", -4.2),
        ("Agent", "Is there any other query today?", None),
        ("Customer", "No, your service has been utterly unacceptable.", -32.2),
        ("Agent", "Thank you for calling S-Net mobile roaming support. Goodbye.", None),
        ("Customer", "Goodbye.", -14.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", -10.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -6.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -2.0)
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
        "Personalized the call/ticket appropriately": "Agent failed to address customer by name 'Tariq' during the call.",
        "Empathy & Acknowledgment Statement": "Failed to acknowledge customer's severe distress and panic at turn 21 regarding European investor presentation.",
        "Paraphrasing": "Failed to paraphrase customer's roaming issue at the beginning of the call.",
        "Active listening": "Asked customer at turn 41 for mobile number which was already provided at turn 3.",
        "Build rapport and observed professionalism": "Insulted customer at turn 11: 'If you don't read international roaming terms before flying abroad, that is your own carelessness.'",
        "Probing": "Failed to probe effectively regarding APN settings or roaming error details.",
        "Confirmed the issue is resolved": "Data roaming remained blocked at the end of the call with up to 4 hours propagation delay."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net mobile roaming support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Agent allowed two separate unmanaged dead air gaps of 40 seconds at turns 14 and 33.",
        "Verified customer": "Agent failed to ask for postal address or security PIN during verification.",
        "Personalized the call/ticket appropriately": "Agent never addressed customer as Tariq throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent handled first outburst at turn 8, but completely ignored severe panic outburst at turn 21 regarding trade presentation and factory jobs.",
        "Paraphrasing": "Agent offered no restatement of the customer's problem.",
        "Active listening": "Agent asked for mobile number at turn 41 despite customer stating 07700 900381 at turn 3.",
        "Took ownership of the problem": "Agent sent roaming unbar command and provided ticket reference.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you don't read international roaming terms before flying abroad, that is your own carelessness.'",
        "Probing": "Agent asked no diagnostic questions about roaming settings.",
        "Confirmed the issue is resolved": "Data remained non-functional with exclamation mark, requiring 4 hours propagation."
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
        "cid": "agt_091",
        "cname": "Tariq",
        "target_dur": 645,
        "scenario": "Mobile data roaming unexpectedly blocked in Europe before major business pitch; 2 customer outbursts (one handled, one unhandled); 6+ faults (poor)",
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

print("get_call_091 defined.")

# =========================================================================
# Call 092: Ursula, Landline caller display showing 'International' for local medical clinic, 15:20 (920s)
# 4-5 faults (okay), score 45.0, Dead Air FAIL, Verified FAIL, Personalized FAIL, Probing FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_092():
    raw = [
        ("Agent", "Thank you for calling S-Net landline technical operations, my name is Simon. How can I help you today?", None),
        ("Customer", "Hello Simon, my name is Ursula Bennett. On our home landline telephone, whenever our local NHS medical clinic or pharmacy calls us, the telephone caller display screen says 'International' instead of showing their local 01423 phone number, causing us to ignore the calls thinking they are foreign telemarketers!", -34.8),
        ("Agent", "Good afternoon. If I understand correctly, your landline caller display is incorrectly identifying incoming calls from your local NHS clinic and pharmacy as 'International' rather than displaying their local 01423 telephone number. Let me query your line routing profile.", None),
        # Verified FAIL: agent asks only for landline number, omitting PIN/address
        ("Customer", "Our landline number is 01423 881902, account reference SN-551029, registered at 33 Duchy Road, Harrogate, HG1 2ER, security PIN 7180.", -5.2),
        # Personalized FAIL: agent never uses "Ursula" anywhere in call
        ("Agent", "Thank you, that brings up the Yorkshire exchange record.", None),
        ("Customer", "Why would a Harrogate NHS clinic appear as international?", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query the SS7 signaling translation tables at the Leeds regional tandem switch?", None),
        ("Agent", "Thank you for holding. The tandem switchboard indicates that the incoming Presentation Number translation rule has an incorrect carrier prefix parsing flag.", None),
        ("Customer", "How does a carrier prefix parsing flag cause local calls to show as international?", -10.4),
        ("Agent", "When NHS hospital trusts route calls through multi-site VoIP SIP trunks, the tandem switch misinterprets the 01423 prefix as an international E.164 country code.", None),
        ("Customer", "Can you correct the translation rule on the tandem switch?", 2.4),
        ("Agent", "Yes, I am submitting a translation profile correction order to the regional exchange engineering team.", None),
        ("Customer", "How long does it take for exchange engineering to apply the correction?", 6.2),
        # Turn 14 is dead air gap 1 (40s)
        ("Customer", "Simon? Are you there? The line was completely silent for forty seconds!", -28.4),
        ("Agent", "I was waiting for the exchange work order system to assign a technician reference.", None),
        ("Customer", "Will the translation rule fix all NHS incoming calls?", -14.2),
        ("Agent", "Obviously telephone signaling protocols require synchronized SS7 translation tables to unmask SIP trunk presentation numbers.", None),
        ("Customer", "Right, I understand the switch tables need synchronizing.", -8.2),
        ("Agent", "The engineering work order has been assigned under reference EX-SS7-99120-Y.", None),
        ("Customer", "EX-SS7-99120-Y, noted down.", 8.4),
        # Outburst at turn 19 in middle third (handled - late acknowledgement 3 turns after)
        ("Customer", "I am seventy-eight years old and my husband is recovering at home after open-heart surgery! The cardiac rehabilitation team from Harrogate District Hospital tried to call us three times yesterday with critical medication dosage changes, but because the caller ID said 'International', we didn't pick up the phone! Having his hospital calls disguised as foreign scam calls is endangering my husband's life! I am in complete tears and agony over this!", -78.4),
        ("Agent", "I am querying the SS7 translation tables on the Leeds tandem switch right now.", None),
        ("Customer", "Please do Simon, my husband's life depends on these hospital calls.", 4.2),
        # Agent handled empathy at turn 22 (3 turns after outburst) with refusal
        ("Agent", "I completely understand the profound anguish, tears, and severe worry you are experiencing, especially with your husband recovering from open-heart surgery and needing critical medication changes from Harrogate Hospital. While our exchange network SLA cannot propagate tandem switch changes instantaneously, I will place an urgent medical priority expedite flag on this exchange order and personally monitor it with network control.", None),
        ("Customer", "Thank you Simon, that reassurance brings me so much comfort.", 4.2),
        ("Agent", "I am adding an emergency medical priority flag to the tandem switch job ticket.", None),
        ("Customer", "How long will the medical priority expedite take to propagate?", 12.2),
        ("Agent", "Regional tandem switch translation updates propagate across the local loop in approximately two hours.", None),
        ("Customer", "So we cannot verify the caller ID display on this phone call right now?", -14.2),
        ("Agent", "Correct, the tandem switch requires the two-hour propagation window before incoming clinic calls display the 01423 number.", None),
        ("Customer", "What should we do if the clinic calls during the two hours?", 4.2),
        ("Agent", "In the interim, I recommend answering any call showing 'International' or 'Withheld' until two o'clock this afternoon.", None),
        ("Customer", "I will keep a pen and notepad next to the handset and answer all calls today.", 18.4),
        ("Agent", "Can I assist with any other feature on your landline handset?", None),
        ("Customer", "Is our voicemail working properly if we miss a call?", 12.2),
        ("Agent", "Yes, standard 1571 voicemail is active and will record messages if the line is engaged.", None),
        ("Customer", "That provides an additional safety net for the hospital team.", 22.4),
        # Turn 34 is dead air gap 2 (40s)
        ("Customer", "Hello? Simon? Did the line drop again? Why does your headset keep going dead?", -28.2),
        ("Agent", "I was applying a ten-pound goodwill credit to your landline account.", None),
        ("Customer", "Thank you for the credit, Simon.", 18.4),
        ("Agent", "I have documented your husband's cardiac recovery status on your account records.", None),
        ("Customer", "That will ensure all future agents understand our medical situation.", 24.2),
        ("Agent", "Our exchange engineering supervisor will monitor the SS7 table update at two o'clock.", None),
        ("Customer", "Thank you, that is very thorough.", 26.2),
        ("Agent", "We want to ensure your husband receives all clinical communications without disruption.", None),
        ("Customer", "You have been very kind and helpful today.", 28.4),
        # Turn 44: Active listening repeat in last third
        ("Agent", "Before we conclude, what was that Harrogate landline number again?", None),
        # Turn 45: Customer answers repeat
        ("Customer", "As I told you right at the start of our call, it is 01423 881902.", -12.4),
        ("Agent", "Thank you, landline number verified on the engineering ticket.", None),
        ("Customer", "Thank you Simon for your urgent help today.", 24.2),
        ("Agent", "It has been my pleasure assisting. Please give my warmest wishes to your husband for his recovery.", None),
        ("Customer", "Goodbye Simon.", 22.0),
        ("Agent", "Is there any other landline issue today?", None),
        ("Customer", "No, goodbye.", 20.0),
        ("Agent", "Thank you for calling S-Net landline technical operations. Goodbye.", None),
        ("Customer", "Goodbye.", 16.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 12.0),
        ("Agent", "Goodbye.", None),
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
        "Active listening": "FAIL",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "FAIL",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Hold time and Dead Air": "Dead Air Breach: Agent had 2 occurrences of >30s unmanaged dead air.",
        "Verified customer": "Agent failed to ask for a PIN, address, or security question within the first 4 minutes of the call.",
        "Personalized the call/ticket appropriately": "Agent failed to address customer by name 'Ursula' during the call.",
        "Active listening": "Asked customer at turn 44 for landline number which was already provided at turn 3.",
        "Probing": "Failed to probe about handset brand or specific clinic incoming numbers.",
        "Confirmed the issue is resolved": "SS7 tandem switch translation required a 2-hour propagation window; resolution unconfirmed on call."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net landline technical operations' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Agent allowed two separate unmanaged dead air gaps of 40 seconds at turns 14 and 33.",
        "Verified customer": "Agent failed to ask for address or security PIN during verification.",
        "Personalized the call/ticket appropriately": "Agent never addressed customer as Ursula throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated deep empathy at turn 21 regarding customer's husband's cardiac recovery and hospital calls, and no unhandled outbursts occurred.",
        "Paraphrasing": "Agent accurately paraphrased the caller display international misidentification issue at turn 2.",
        "Active listening": "Agent asked for landline number at turn 44 despite customer stating 01423 881902 at turn 3.",
        "Took ownership of the problem": "Agent submitted medical priority order, applied £10 credit, advised workaround, and documented cardiac status.",
        "Build rapport and observed professionalism": "Agent maintained polite, reassuring, and professional demeanor throughout.",
        "Probing": "Agent failed to probe about clinic incoming numbers or handset display settings.",
        "Confirmed the issue is resolved": "Tandem switch update required 2 hours to take effect; incoming caller ID remained unverified on call."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 46, "reworded": True}
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
        "cid": "agt_092",
        "cname": "Ursula",
        "target_dur": 920,
        "scenario": "Landline caller ID showing 'International' for local NHS cardiac clinic; SS7 tandem switch update ordered; 4-5 faults (okay)",
        "tier": "okay",
        "expected_score": 45.0,
        "dead_air_indices": [14, 33],
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Confirmed the issue is resolved", "Verified customer", "Personalized the call/ticket appropriately", "Probing"],
        "notes": "Okay call featuring dead air breaches, failed verification and personalization, handled empathy in middle third, medical expedite order, and pending resolution."
    }

print("get_call_092 defined.")

# =========================================================================
# Call 093: Valerie, TV box audio description voice synthesizer stuck on, 13:00 (780s)
# 0 faults (excellent), score 100.0, All PASS
# Features TWO handled outbursts (turn 15 handled, turn 21 handled)
# =========================================================================
def get_call_093():
    raw = [
        ("Agent", "Thank you for calling S-Net TV technical support, my name is Chloe. How can I help you today?", None),
        ("Customer", "Hello Chloe, my name is Valerie Wood. We have an S-Net TV 4K box, and for the past three days the automated audio description voice synthesizer has been permanently stuck on across every single channel, narrating every actor movement over movie dialogue even though Audio Description is toggled 'Off' in our settings!", -34.8),
        ("Agent", "Good afternoon Valerie. If I understand correctly, your TV 4K box has its audio description voice narration permanently stuck on across all live and on-demand channels, continuing to narrate programs even with the accessibility toggle switched to off in your user settings. Before we query your set-top box accessibility profile, could you please confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 19 Queensgate, Inverness, IV1 1DF, security PIN 3381, TV box serial SN-TV-881902.", -5.2),
        ("Agent", "Thank you Valerie, that confirms your account details. Have you tried power cycling the TV box at the mains wall socket?", None),
        ("Customer", "I switched it off at the wall for ten minutes last night, but as soon as BBC One loaded, the narration voice started describing the news anchor's clothes immediately!", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query your set-top box firmware accessibility state tables and audio PID stream decoders?", None),
        ("Agent", "Thank you for holding, Valerie. Looking at the audio decoder registers, your box firmware has a persistent secondary audio program stream lock on the NAR audio PID.", None),
        ("Customer", "Why would a secondary audio program stream lock onto the narration PID?", -10.4),
        ("Agent", "When an over-the-air firmware patch updates the Dolby Digital audio driver, the default audio stream index occasionally fails to clear the broadcast narrative flag.", None),
        ("Customer", "Can you clear the secondary audio stream lock remotely?", 2.4),
        ("Agent", "Yes, we can transmit an immediate audio PID re-initialization command directly to your TV box.", None),
        ("Customer", "Will that reset our recorded shows or channel favorites?", -8.2),
        ("Agent", "Not at all: recorded programs, scheduled timers, and channel favorites remain completely intact; only the live audio stream multiplexer is re-initialized.", None),
        ("Customer", "That is brilliant news.", 12.2),
        # Outburst 1 at turn 15 (handled - late acknowledgement 3 turns after)
        ("Customer", "Valerie speaking, I am hosting our village film club tonight at six o'clock to watch a subtitled French classic drama that we have planned for six months! If a mechanical robotic voice keeps narrating every single camera angle and cough over the delicate French dialogue, the entire screening will be completely ruined and all my neighbors will be irritated! I am so stressed and embarrassed!", -68.4),
        ("Agent", "I am querying your set-top box audio stream decoders right now.", None),
        ("Customer", "Please do Chloe, I am desperate to avoid embarrassing our guests.", 14.2),
        # Agent handled empathy 1 at turn 18 (3 turns after outburst) with refusal
        ("Agent", "I completely understand how stressful and embarrassing this is, Valerie, especially with your village film club arriving tonight for a screening you have planned for six months. While our engineering policy does not permit dispatching an emergency field technician to your home within two hours, I will make sure this audio stream is completely fixed and verified live on call right now so your evening is a complete success.", None),
        ("Customer", "Thank you Chloe, that is such a relief to hear.", 18.4),
        ("Agent", "I am sending the audio multiplexer reset payload to your TV box now.", None),
        ("Agent", "Obviously broadcast multiplex streams carry separate narrative and stereo audio PIDs that require clean decoder allocation.", None),
        ("Customer", "The TV screen flashed black for two seconds and returned to BBC One.", 22.4),
        # Outburst 2 at turn 23 in middle third (handled)
        ("Customer", "Valerie speaking, our film club chairman is eighty-four years old and has very sensitive hearing aids! Last week when a loud automated voice boomed through the speakers unexpectedly, his hearing aids shrieked with high-pitched feedback and he had to leave the room in severe pain! If that happens in my home tonight, I would never forgive myself! I am terrified of hurting his ears!", -76.2),
        # Agent handled empathy 2 at turn 24
        ("Agent", "I completely understand your deep concern and protective care for your eighty-four-year-old film club chairman and his sensitive hearing aids, Valerie. Preventing any harsh feedback or unexpected narration is an absolute priority. Let us unmute your TV right now, switch through multiple channels together, and confirm that only pristine, clean stereo dialogue is broadcasting.", None),
        ("Customer", "Unmuting the television on BBC One now...", 18.4),
        ("Agent", "Listen carefully to the live broadcast: do you hear any narrative voice describing the presenters?", None),
        ("Customer", "The news presenters are speaking... Chloe! Only their natural voices are coming through! Zero narration! Zero robotic audio!", 36.8),
        ("Agent", "Wonderful! Now let us switch to Channel 4 and test a drama with heavy audio description.", None),
        ("Customer", "Changing to Channel 4... A drama is playing... The actors are whispering... No narration voice at all! Pristine audio!", 38.4),
        ("Agent", "Now let us test your on-demand player or a saved French film recording to be one hundred percent certain.", None),
        ("Customer", "Loading the French film from our library... Playing... Chloe, the French dialogue and original soundtrack are playing in crystal-clear high definition with zero background voice! It works flawlessly!", 39.2),
        ("Agent", "That confirms full audio PID allocation restored and secondary narrative stream permanently deactivated.", None),
        ("Customer", "Your film club chairman will be able to enjoy the screening in complete comfort tonight.", 38.4),
        ("Agent", "I have locked the audio stream decoder configuration in your hub profile to prevent any recurrence.", None),
        ("Customer", "That will protect us from future firmware glitches.", 34.2),
        ("Agent", "I have documented the audio PID purge under service reference TV-AUD-88192-I.", None),
        ("Customer", "TV-AUD-88192-I, recorded in my diary.", 30.2),
        ("Agent", "Please give my warmest regards to your village film club and your chairman tonight, Valerie.", None),
        ("Customer", "I will tell all my neighbors what a wonderful technician Chloe from S-Net is.", 36.2),
        ("Agent", "It has been our pleasure ensuring your cultural evening is a triumph.", None),
        ("Customer", "I can now bake the refreshments with complete peace of mind.", 34.8),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just making sure our premises records match perfectly: that was 19 Queensgate, Inverness, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, 19 Queensgate, Inverness.", 32.4),
        ("Agent", "Thank you Valerie, all equipment and premises records are fully synchronized.", None),
        ("Customer", "Thank you again Chloe for your wonderful, rapid, and reassuring support.", 36.2),
        ("Agent", "It has been an absolute pleasure assisting you, Valerie. Have a magnificent film screening tonight.", None),
        ("Customer", "Have a wonderful afternoon, Chloe. Goodbye.", 32.4),
        ("Agent", "Is there any other TV or broadband issue I can assist you with today, Valerie?", None),
        ("Customer", "No Chloe, everything is working flawlessly.", 30.2),
        ("Agent", "Thank you for calling S-Net TV technical support, Valerie. Goodbye.", None),
        ("Customer", "Goodbye Chloe.", 28.4),
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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net TV technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Valerie throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent handled two separate customer emotional outbursts with deep empathy at turns 16 and 22, and no unhandled outbursts occurred.",
        "Paraphrasing": "Agent accurately paraphrased the persistent audio description voice narration issue at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer address at turn 42.",
        "Took ownership of the problem": "Agent transmitted audio multiplexer reset, locked decoder configuration, and verified multiple channels and recordings live.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, warm, and highly supportive professional demeanor throughout.",
        "Probing": "Agent probed about power cycling history and specific channel behavior.",
        "Confirmed the issue is resolved": "Live testing on BBC One, Channel 4, and French on-demand recording confirmed pristine audio with zero voice narration."
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
            {"kind": "blunt_but_ok", "agent_turn": 20}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 15, "agent_turn": 18, "with_refusal": True},
            {"kind": "handled", "customer_turn": 23, "agent_turn": 24, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_093",
        "cname": "Valerie",
        "target_dur": 780,
        "scenario": "TV 4K box audio description voice synthesizer stuck on across all channels; cleared via remote audio PID multiplexer reset; two handled outbursts",
        "tier": "excellent",
        "expected_score": 100.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": [],
        "notes": "Flawless call featuring two handled outbursts with deep empathy, remote audio multiplexer reset, harmless recheck in the final third, and complete live resolution verification."
    }

print("get_call_093 defined.")

# =========================================================================
# Call 094: Victor, Parental web safety filters blocking legitimate university research portal, 11:20 (680s)
# 0 faults (excellent), score 100.0, All PASS
# =========================================================================
def get_call_094():
    raw = [
        ("Agent", "Thank you for calling S-Net broadband customer services, my name is Natalie. How can I help you today?", None),
        ("Customer", "Hello Natalie, my name is Victor Vance. I am a postgraduate medical researcher at Imperial College London working from home, and your automated S-Net SafeSearch web safety filter is aggressively blocking our university's official cancer genetics epidemiology database, displaying an 'Adult Content Blocked' screen and halting my research!", -34.8),
        ("Agent", "Good afternoon Victor. If I understand correctly, our S-Net SafeSearch web filter is miscategorizing your Imperial College cancer genetics research database as adult content, presenting a block screen and preventing you from accessing essential academic resources. Before we inspect your broadband account safety filter configuration, could you please confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 14 Kensington Park Gardens, London, W11 3HD, security PIN 6619.", -5.2),
        ("Agent", "Thank you Victor, that confirms your account details. What is the exact domain URL of the university database being blocked?", None),
        ("Customer", "The domain is genetics.imperial.ac.uk/oncology-epidemiology.", -12.4),
        ("Agent", "Could I place you on hold for two minutes while I query your broadband profile web protection classification tables?", None),
        ("Agent", "Thank you for holding, Victor. Looking at the content filter classification engine, the keyword 'reproductive oncology' in the database metadata triggered a false positive match under our strict adult filter heuristic.", None),
        ("Customer", "Why would reproductive oncology be flagged as adult content by an automated filter?", -10.4),
        ("Agent", "Heuristic content filters use automated pattern recognition that occasionally conflates medical and reproductive terminology with restricted content categories.", None),
        ("Customer", "Can you whitelist the entire imperial.ac.uk academic domain on our broadband line?", 2.4),
        ("Agent", "Yes, we can add a custom domain exception directly to your S-Net SafeSearch cloud profile.", None),
        ("Customer", "Will that whitelist apply to all devices connected to our home router?", 12.2),
        ("Agent", "Yes, network-level domain exceptions apply instantaneously across all wired and Wi-Fi devices in your household.", None),
        ("Customer", "That is exactly what I need.", 18.4),
        ("Agent", "I am adding '*.imperial.ac.uk' and 'genetics.imperial.ac.uk' to your permanent trusted exception list.", None),
        ("Agent", "Obviously automated heuristic filters require human fine-tuning when specialized scientific research is involved.", None),
        ("Customer", "I completely understand that heuristics need manual exception tuning.", 22.4),
        ("Agent", "I am pushing the whitelist policy update directly to your Hub 5 cloud policy cache.", None),
        ("Customer", "The router center LED blinked green twice.", 26.2),
        # Outburst at turn 20 in middle third (handled - late acknowledgement 3 turns after)
        ("Customer", "Victor speaking, I have our doctoral dissertation submission deadline at midnight tonight, and if I cannot extract the patient cohort genetics tables from this database before three o'clock, my four years of clinical doctoral research will be rejected and my university medical fellowship will be terminated! I am in sheer panic and terror over this blockage!", -82.4),
        ("Agent", "I am querying the cloud policy filter exception engine right now.", None),
        ("Customer", "Please do Natalie, I am desperate to download the genetics dataset before three o'clock.", 14.2),
        # Agent handled empathy at turn 23 (3 turns after outburst) with refusal
        ("Agent", "I completely understand the acute terror, panic, and immense career stakes of your midnight dissertation deadline, Victor. While our cybersecurity policy does not permit disabling the master network firewall completely for residential accounts, I will stay on the line with you right now and personally verify that you can log in and download your patient cohort genetics tables immediately.", None),
        ("Customer", "Thank you Natalie! Let us test accessing the database right now.", 14.2),
        ("Agent", "Please refresh your web browser on genetics.imperial.ac.uk/oncology-epidemiology.", None),
        ("Customer", "Refreshing browser now... Natalie! The Imperial College Single Sign-On portal loaded instantly with zero block screen! Logging in with my university smart card...", 36.8),
        ("Agent", "Verify that you can query the database and download your data tables.", None),
        ("Customer", "Entering query: 'Oncology patient cohort 2024'... Query executed! Downloading the 250-megabyte genetics dataset... Download completed! All tables intact!", 39.2),
        ("Agent", "Fantastic! That confirms full unrestricted access restored across all Imperial College research gateways.", None),
        ("Customer", "You have completely saved my doctoral degree today, Natalie.", 38.4),
        ("Agent", "I have also submitted a classification override to our central cybersecurity threat intelligence team to prevent imperial.ac.uk from ever being flagged globally.", None),
        ("Customer", "That will protect all other medical researchers across the country.", 34.2),
        ("Agent", "I have documented the exception whitelist under reference FLT-MED-88192-K.", None),
        ("Customer", "FLT-MED-88192-K, noted down.", 30.2),
        ("Agent", "Best of luck with your midnight dissertation submission and your fellowship, Victor.", None),
        ("Customer", "Thank you so much Natalie, you have been an absolute lifesaver.", 36.2),
        ("Agent", "Our team is proud to support essential clinical medical research.", None),
        ("Customer", "I can now finish writing my doctoral conclusion with complete confidence.", 34.8),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just making sure our premises records match perfectly: that was 14 Kensington Park Gardens, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, 14 Kensington Park Gardens, London.", 32.4),
        ("Agent", "Thank you Victor, all account and security records are fully synchronized.", None),
        ("Customer", "Thank you again Natalie for your brilliant, rapid, and reassuring support.", 36.2),
        ("Agent", "It has been an absolute pleasure assisting you, Victor. Go get that doctorate!", None),
        ("Customer", "Have a wonderful afternoon, Natalie. Goodbye.", 32.4),
        ("Agent", "Is there any other broadband or security issue I can assist you with today, Victor?", None),
        ("Customer", "No Natalie, everything is working flawlessly.", 30.2),
        ("Agent", "Thank you for calling S-Net broadband customer services, Victor. Goodbye.", None),
        ("Customer", "Goodbye Natalie.", 28.4),
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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net broadband customer services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Victor throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated profound empathy at turn 22 regarding customer's doctoral dissertation deadline and medical fellowship, and no unhandled outbursts occurred.",
        "Paraphrasing": "Agent accurately paraphrased the content filter misclassification issue at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer address at turn 42.",
        "Took ownership of the problem": "Agent applied custom domain exception, pushed cloud policy update, submitted central heuristic override, and verified live dataset download.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, warm, and highly supportive professional demeanor throughout.",
        "Probing": "Agent probed about the exact URL and domain triggering the block screen.",
        "Confirmed the issue is resolved": "Customer logged in via Single Sign-On and successfully downloaded the 250MB dataset live on call."
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
        "cid": "agt_094",
        "cname": "Victor",
        "target_dur": 680,
        "scenario": "Parental web safety filter blocking university medical genetics research portal; resolved via custom domain exception and policy push",
        "tier": "excellent",
        "expected_score": 100.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": [],
        "notes": "Flawless call featuring deep empathy in middle third, custom domain whitelist provisioning, harmless recheck in final third, and complete live download verification."
    }

print("get_call_094 defined.")

# =========================================================================
# Call 095: Wendy, Intermittent crackling noise on telephone line during wet weather, 18:40 (1120s)
# 1-2 faults (good), score 83.3, Active listening PASS, Confirmed resolved FAIL
# =========================================================================
def get_call_095():
    raw = [
        ("Agent", "Thank you for calling S-Net landline network operations, my name is George. How can I help you today?", None),
        ("Customer", "Hello George, my name is Wendy Patterson. We have had an ongoing issue with our home landline telephone for the past month: whenever it rains heavily outside, the line develops severe crackling, static, and intermittent hum, causing our telephone calls to drop and making conversations completely inaudible!", -34.8),
        ("Agent", "Good afternoon Wendy. If I understand correctly, your home landline develops severe static, crackling, and dropped calls specifically during heavy rainfall, rendering phone conversations inaudible while the weather is wet. Before we initiate a line condition test and resistance balance query, could you please confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 28 Meadow Lane, Northallerton, DL6 1TR, security PIN 4912, landline number 01609 771920.", -5.2),
        ("Agent", "Thank you Wendy, that confirms your account details. What happens to your broadband connection when the telephone line crackles?", None),
        ("Customer", "The broadband router speed drops slightly from 60 Mbps to 45 Mbps, but the landline handset suffers terrible buzzing and crackling.", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I execute an automated Metallic Loop Test across your copper pair from the local Northallerton telephone exchange?", None),
        ("Agent", "Thank you for holding, Wendy. The metallic loop diagnostic indicates a severe low-insulation resistance fault between the B-leg of your copper pair and earth ground.", None),
        ("Customer", "What does low-insulation resistance between the B-leg and earth ground mean?", -10.4),
        ("Agent", "It indicates that rainwater is seeping into an external joint box or telegraph pole DP terminal block, allowing electrical moisture ingress across the copper wire insulation.", None),
        ("Customer", "Can you fix the moisture ingress on the telegraph pole remotely?", -8.2),
        ("Agent", "Moisture ingress in external copper plant requires a dedicated Openreach underground and overhead cable engineer to inspect the drop-wire and re-seal the external junction box.", None),
        ("Customer", "How soon can an Openreach cable engineer inspect the external wiring?", 2.4),
        ("Agent", "I can book an external Openreach cable repair engineer for Monday morning between eight and one o'clock.", None),
        ("Customer", "Monday morning would be ideal.", 8.4),
        ("Agent", "Obviously physical rainwater seeping into underground copper joints cannot be repaired by exchange software reboots.", None),
        ("Customer", "I understand that wet wires require physical engineering.", 12.2),
        ("Agent", "I am booking the Monday morning engineering slot right now.", None),
        ("Customer", "Do I need to stay home from work on Monday morning?", 4.2),
        ("Agent", "No, because the insulation fault is located on the external distribution pole in the street, the engineer can complete all external joint repairs without entering your home.", None),
        ("Customer", "That is a huge convenience.", 14.2),
        # Outburst at turn 20 in middle third (handled - late acknowledgement 3 turns after)
        ("Customer", "Wendy speaking, my eighty-nine-year-old mother lives with me and she wears an emergency telecare panic pendant around her neck that connects directly to the NHS county ambulance control via our telephone landline! When the line crackles with static during rainstorms, the telecare monitoring hub beeps with error codes and fails to send emergency signals! If she falls down the stairs in the rain and the alarm fails, she could lie on the floor for hours! I am sick with terror and anxiety!", -84.2),
        ("Agent", "I am querying the metallic loop resistance telemetry from the Northallerton exchange right now.", None),
        ("Customer", "Please do George, I am terrified of my mother being left without ambulance contact.", 14.2),
        # Agent handled empathy at turn 23 (3 turns after outburst) with refusal
        ("Agent", "I completely understand the acute terror, constant anxiety, and profound worry you are experiencing, Wendy, especially with your eighty-nine-year-old mother relying on her telecare panic pendant for emergency ambulance monitoring. While our engineering policy cannot dispatch an emergency cable technician during active rainstorms this evening, I am attaching an urgent NHS Vulnerable Lifeline Customer safety escalation flag to the engineering work order and dispatching our emergency mobile cellular telecare backup adapter today.", None),
        ("Customer", "Thank you George! An emergency mobile telecare backup adapter would protect her completely!", 28.4),
        ("Agent", "The emergency telecare backup adapter uses a roaming multi-network 4G SIM that plugs directly between her pendant hub and the wall, ensuring her alarm signals route over cellular even if the landline has static.", None),
        ("Customer", "That will keep her safe regardless of the weather.", 34.2),
        ("Agent", "I am sending the adapter via Royal Mail Tracked 24 for delivery tomorrow morning, Friday.", None),
        ("Customer", "Tomorrow morning? That is fantastic!", 36.8),
        ("Agent", "Your Openreach cable engineering appointment is confirmed for Monday between 8:00 AM and 1:00 PM under job reference EXT-COP-99120-N.", None),
        ("Customer", "EXT-COP-99120-N, noted down.", 30.2),
        ("Agent", "I have waived all engineering visit fees and equipment delivery charges on your account.", None),
        ("Customer", "Thank you George, you have been remarkably kind and thorough.", 34.2),
        ("Agent", "I have documented your mother's vulnerable telecare status on the permanent network profile.", None),
        ("Customer", "That will guarantee that our line is prioritized in all future adverse weather events.", 32.4),
        ("Agent", "Our emergency operations team will also monitor the copper loop test following Monday's repair.", None),
        ("Customer", "Thank you, that gives me total reassurance.", 36.2),
        ("Agent", "Please give my warmest wishes to your mother, Wendy. We want her to stay safe and well.", None),
        ("Customer", "I will tell her how wonderfully S-Net has taken care of us today.", 38.4),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just making sure our premises records match perfectly: that was 28 Meadow Lane, Northallerton, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, 28 Meadow Lane, Northallerton.", 32.4),
        ("Agent", "Thank you Wendy, all premises and safety records are fully synchronized.", None),
        ("Customer", "Thank you again George for your compassionate and urgent help.", 36.2),
        ("Agent", "It has been an absolute pleasure assisting you, Wendy. Have a safe and peaceful weekend.", None),
        ("Customer", "Goodbye George.", 30.2),
        ("Agent", "Is there any other landline or broadband issue I can assist with today, Wendy?", None),
        ("Customer", "No George, you have resolved everything brilliantly.", 28.0),
        ("Agent", "Thank you for calling S-Net landline network operations, Wendy. Goodbye.", None),
        ("Customer", "Goodbye George.", 26.2),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 22.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 18.0),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
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
        "Active listening": "PASS",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Confirmed the issue is resolved": "External Openreach cable engineer booked for Monday morning; physical copper moisture fault remains unresolved on call."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net landline network operations' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Wendy throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated deep empathy at turn 22 regarding customer's mother's telecare lifeline alarm, and no unhandled outbursts occurred.",
        "Paraphrasing": "Agent accurately paraphrased the weather-dependent line crackling issue at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer address at turn 42.",
        "Took ownership of the problem": "Agent executed metallic loop test, booked priority Monday Openreach engineer, arranged express 4G telecare backup adapter, and waived fees.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, warm, and highly supportive professional demeanor throughout.",
        "Probing": "Agent probed about broadband performance during rainfall and handset noise characteristics.",
        "Confirmed the issue is resolved": "Physical external copper moisture ingress requires Monday morning's engineering visit and repair; unverified on call."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 40}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 2},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 15}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 21, "agent_turn": 24, "with_refusal": True}
        ]
    }

    return {
        "cid": "agt_095",
        "cname": "Wendy",
        "target_dur": 1120,
        "scenario": "Landline telephone severe crackling during rainfall due to low-insulation resistance fault; Monday Openreach cable repair and express 4G telecare adapter booked",
        "tier": "good",
        "expected_score": 90.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Confirmed the issue is resolved"],
        "notes": "Good call featuring deep empathy in middle third, priority external engineer booking, express telecare cellular backup adapter, harmless recheck in final third, and pending physical resolution."
    }

print("get_call_095 defined.")

if __name__ == "__main__":
    for fn in [get_call_091, get_call_092, get_call_093, get_call_094, get_call_095]:
        c = fn()
        compile_call(c)
