import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from batch_engine import compile_call

# =========================================================================
# Call 066: Miriam, Landline Caller ID not displaying names on cordless phone, 11:40 (700s)
# 1-2 faults (good), score 83.3, Paraphrasing FAIL, Active listening FAIL
# =========================================================================
def get_call_066():
    raw = [
        ("Agent", "Thank you for calling S-Net landline customer services, my name is Liam. How can I help you today?", None),
        ("Customer", "Hello Liam, my name is Miriam Jenkins. I subscribe to your Caller Display feature on our landline, but for the past week every single incoming telephone call displays 'Incoming Call' or 'Number Withheld' on our Panasonic cordless phones, even when family members call from their mobile numbers!", -32.4),
        ("Agent", "Good afternoon Miriam. I can inspect your calling line identity presentation profile on the local exchange. Before we test your line features, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 14 Woodlands Crescent, Harrogate, HG2 7PN, security PIN 3891, landline number 01423 881204.", -5.2),
        ("Agent", "Thank you Miriam, that confirms your account details. Have you noticed any crackling, buzzing, or static noise on the voice line when speaking on the phone?", None),
        ("Customer", "The voice call audio is crystal clear; it is solely the caller display information that never appears on the handset screens.", -18.2),
        ("Agent", "Could I place you on hold for two minutes while I query the local exchange switch calling line identity profile?", None),
        ("Agent", "Thank you for holding, Miriam. The exchange line profile indicates that the Calling Line Identification Presentation feature flag was switched to passive mode during an automated line card migration.", None),
        ("Customer", "Why would an automated migration turn off a feature we pay for every month?", -14.2),
        ("Agent", "During regional digital exchange card migrations, supplementary telephony features occasionally default to inactive until re-provisioned.", None),
        ("Customer", "Can you switch the Calling Line Identification feature back to active right now?", -6.4),
        ("Agent", "Yes, I am submitting an immediate provisioning command to re-enable active FSK caller display signaling.", None),
        ("Customer", "Does my Panasonic cordless telephone need any special settings configured for your network?", -2.4),
        ("Agent", "Standard UK cordless telephone equipment adheres to the British Telecom SIN 227 FSK caller identification specification.", None),
        ("Customer", "Our Panasonic phone has always worked with S-Net until this week.", 2.4),
        ("Agent", "The re-provisioning signal takes approximately three minutes to cycle through the line card registers.", None),
        ("Customer", "Will re-enabling this feature wipe any of my stored speed-dial numbers or directory contacts?", 6.2),
        ("Agent", "No, directory contacts and stored speed-dial numbers are saved in local handset memory and remain unaffected.", None),
        ("Customer", "That is reassuring to know.", 8.4),
        ("Agent", "Obviously Caller Display equipment cannot decode incoming telephone numbers if the exchange switch flag is provisioned as passive.", None),
        ("Customer", "Right, I understand the technical requirement now.", 10.2),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Miriam speaking, my seventy-nine-year-old sister is recovering from hip surgery at home, and she gets targeted by fraudulent telephone scammers five times a day! We specifically pay for Caller Display so she can screen calls before picking up the receiver! Because your service says 'Call Withheld' on every incoming call, she answered a rogue builder who frightened her to tears! This failure is putting an elderly woman in direct danger!", -64.2),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand how deeply alarming and dangerous that is for your sister, Miriam. Having an elderly family member harassed by scammers when Caller Display should protect her is unacceptable, and I will verify and restore the Calling Line Identity feature on her exchange line right now.", None),
        ("Customer", "Thank you Liam, that is very comforting to hear.", -6.2),
        ("Agent", "The exchange switchboard confirms that the active FSK signaling profile is now fully enabled on 01423 881204.", None),
        ("Customer", "Can we test an incoming call right now to see if the caller number actually shows up on the screen?", 2.4),
        ("Agent", "Yes, I will initiate an automated loopback test call from our central test gateway.", None),
        ("Customer", "I have the Panasonic cordless handset right here in my hand.", 6.2),
        ("Agent", "Sending test call now... The line should ring in approximately ten seconds.", None),
        ("Customer", "The phone is ringing... Liam! The screen says: '0800 012 3456 - S-Net Network Test'! It worked!", 28.4),
        ("Agent", "Excellent! The FSK caller identification packets are successfully synchronizing between the exchange and your handset.", None),
        ("Customer", "Let me check with my mobile phone as well: dialing our landline from my mobile right now...", 24.2),
        ("Agent", "The secondary line ring should decode your mobile number between the first and second ring bursts.", None),
        ("Customer", "The phone is ringing again... Screen displays: 'Miriam Mobile - 07700 900381'! It even pulled the contact name from the handset phonebook!", 34.2),
        ("Agent", "That confirms full name and number presentation functionality across both fixed and mobile networks.", None),
        ("Customer", "My sister will be able to see exactly who is calling before picking up the receiver again.", 32.4),
        ("Agent", "I have also applied a five-pound goodwill credit to your bill to cover the days Caller Display was inactive.", None),
        ("Customer", "Thank you, that is very fair and appreciated.", 28.4),
        ("Agent", "I will also lock a permanent flag on the exchange database preventing future migration overrides.", None),
        ("Customer", "That will ensure the feature stays active permanently.", 26.2),
        ("Agent", "All line parameters are documented under technical reference TEL-99214-M.", None),
        ("Customer", "TEL-99214-M, noted down.", 22.4),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before I complete the feature activation, what was that Harrogate landline number again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you at the start of our call, it is 01423 881204.", -10.2),
        ("Agent", "Thank you Miriam, the profile update has been permanently committed to our exchange logs.", None),
        ("Customer", "Everything is working perfectly now.", 24.5),
        ("Agent", "Is there any other aspect of your landline service I can assist you with today, Miriam?", None),
        ("Customer", "No Liam, you have resolved our problem completely.", 26.4),
        ("Agent", "Thank you for calling S-Net landline customer services, Miriam. Have a wonderful and peaceful day. Goodbye.", None),
        ("Customer", "Goodbye Liam.", 22.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
        ("Customer", "Goodbye.", 18.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", 14.0),
        ("Agent", "Goodbye.", None),
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
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "PASS"
    }

    coaching = {
        "Paraphrasing": "Failed to paraphrase customer's landline Caller ID presentation issue in own words.",
        "Active listening": "Asked customer at turn 42 for landline number which was already provided at turn 3."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net landline customer services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Miriam throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand how deeply alarming and dangerous that is for your sister, Miriam...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent never restated the Caller ID fault in own words.",
        "Active listening": "Agent asked for landline number at turn 42 despite customer stating 01423 881204 at turn 3.",
        "Took ownership of the problem": "Agent re-provisioned FSK signaling, ran automated loopback test, applied goodwill credit, and locked permanent profile flag.",
        "Build rapport and observed professionalism": "Agent maintained polite, supportive, and professional demeanor throughout.",
        "Probing": "Agent asked about line noise and handset settings.",
        "Confirmed the issue is resolved": "Test call from network test number and mobile call both displayed correctly on Panasonic handset screen."
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
        "cid": "agt_066",
        "cname": "Miriam",
        "target_dur": 700,
        "scenario": "Landline Caller ID service not displaying names on Panasonic cordless phone; resolved via FSK re-provisioning",
        "tier": "good",
        "expected_score": 83.3,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening"],
        "notes": "Good call where agent was polite, empathetic, and resolved Caller ID fault, failing only paraphrasing and active listening repeat in the final third."
    }

print("get_call_066 defined.")

# =========================================================================
# Call 067: Nadia, Broadband intermittent disconnections from faulty power adapter, 15:24 (924s)
# 5+ faults (poor), score 35.0, Branding FAIL, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_067():
    raw = [
        # Branding FAIL: Missing standard greeting
        ("Agent", "Good afternoon, broadband technical line, my name is Greg.", None),
        ("Customer", "Hello Greg, my name is Nadia Patel. Our broadband router has started rebooting itself six or seven times an hour: whenever anyone walks past the hallway table or brushes against the power lead, the lights on the router die completely and it takes five minutes to reconnect to the internet!", -34.5),
        ("Agent", "I can inspect your router power supply and line uptime logs. Before we test your connection, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 83 Victoria Road, Cambridge, CB4 3BW, security PIN 5521, router model S-Net Hub 4.", -5.2),
        ("Agent", "Thank you Nadia, that confirms your account details. Have you inspected the black power adapter plug connected to the rear of the router?", None),
        ("Customer", "The round barrel plug is loose inside the socket on the back of the hub: if I touch the wire with a single finger, the hub loses power immediately!", -24.2),
        ("Agent", "Could I place you on hold for two minutes while I check your router power and uptime telemetry?", None),
        ("Agent", "Thank you for holding, Nadia. The network telemetry confirms forty-two sudden router power loss events over the past twenty-four hours.", None),
        ("Customer", "Can you dispatch a replacement twelve-volt power supply adapter to replace this loose one?", -14.2),
        ("Agent", "Power supply accessories are classified as consumable customer premises equipment and are not covered under free replacement policies.", None),
        ("Customer", "Not covered?! The router is only five months old! S-Net supplied the power plug!", -34.2),
        ("Agent", "If you place your sensitive broadband router on a wobbly hallway table where people kick the cables, of course the power plug is going to loosen.", None),
        ("Customer", "No one kicked the cable! It is sitting on a solid console table! Why are you blaming me for a loose factory power connector?", -52.4),
        ("Agent", "I am stating the standard causes of physical strain damage on DC barrel sockets.", None),
        ("Customer", "So what is your solution for a five-month-old router that keeps losing power?", -36.2),
        ("Agent", "You can order an official S-Net replacement power adapter through our customer shop for thirty-nine pounds ninety-nine.", None),
        ("Customer", "I am not paying forty pounds for a power lead when I pay sixty pounds a month for your service!", -46.2),
        ("Agent", "That is our standard accessory replacement policy for consumer premises hardware.", None),
        ("Customer", "Can I speak with a manager who has the authority to waive a forty-pound power plug charge?", -38.2),
        ("Agent", "Obviously twelve-volt barrel connectors require a snug mechanical fit into the internal chassis socket.", None),
        ("Customer", "I know it requires a snug fit! That is why I am asking for a working plug!", -42.4),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Nadia speaking, our internet cuts out every twenty minutes whenever anyone walks past the hall table! I work from home as an intensive care triage dispatcher and my remote database session drops in the middle of emergency bed allocations! It is terrifying and unacceptable that S-Net provides hardware that shuts off at the slightest vibration!", -64.5),
        # Turn 22: Agent handled empathy
        ("Agent", "I understand how terrifying and stressful it is to have your connection cut out during intensive care hospital bed allocations, Nadia. Experiencing power loss from slight vibrations is completely unacceptable for mission-critical work, so let us troubleshoot the physical power adapter immediately.", None),
        ("Customer", "Will you dispatch a replacement power adapter today?", -18.2),
        ("Agent", "As I advised, frontline agents cannot override accessory dispatch charges without supervisory approval.", None),
        ("Customer", "Then get supervisory approval right now while I am on the phone!", -28.4),
        ("Agent", "Team supervisors do not take telephony escalations for power supply accessories.", None),
        ("Customer", "Is there any temporary fix I can use to prevent the hub from dying during my shifts?", -14.2),
        ("Agent", "You could wrap insulating tape around the plastic barrel neck to increase friction inside the socket.", None),
        ("Customer", "You want an NHS critical care dispatcher to tape a faulty electrical plug with insulating tape?!", -52.4),
        ("Agent", "I am offering a practical zero-cost suggestion to prevent lateral movement.", None),
        ("Customer", "That is a fire hazard and an insult. What happens when the hub reboots during an emergency call tonight?", -46.2),
        ("Agent", "S-Net cannot accept liability for critical service interruptions on residential consumer contracts.", None),
        ("Customer", "You pride yourself on reliable broadband in your advertising, but your equipment is falling apart.", -34.2),
        ("Agent", "Our advertising reflects network availability across our external telecommunications infrastructure.", None),
        ("Customer", "Can you at least log an official hardware complaint regarding the build quality of the Hub 4 power socket?", -18.2),
        ("Agent", "I can submit a hardware defect feedback form to our quality assurance team.", None),
        ("Customer", "What is the reference number for that hardware complaint?", -12.4),
        ("Agent", "The defect feedback tracking reference is DEF-88190-C.", None),
        ("Customer", "DEF-88190-C, noted down.", -8.2),
        ("Agent", "Defect feedback forms are reviewed by product engineering within thirty business days.", None),
        ("Customer", "Thirty business days does not help me tonight.", -22.4),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before I document the hardware fault, what model router did you say was on the hall table again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "As I told you at the start of our call, it is the S-Net Hub 4.", -18.2),
        ("Agent", "I have recorded the Hub 4 model on the hardware defect report.", None),
        ("Customer", "So the internet will continue cutting out every twenty minutes and S-Net refuses to send a five-pound power lead.", -28.4),
        ("Agent", "You retain the option to purchase the replacement power adapter via our website.", None),
        ("Customer", "I will be purchasing an adapter from Amazon for eight pounds and submitting the receipt to the Small Claims Court.", -24.2),
        ("Agent", "That is your prerogative as a consumer.", None),
        ("Customer", "This has been the most appalling customer service I have ever encountered.", -28.5),
        ("Agent", "Is there any other aspect of your broadband connection I can assist you with today, Nadia?", None),
        ("Customer", "No, you have completely failed to resolve my problem.", -32.4),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -20.2),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -16.0),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -12.0)
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
        "Branding and Survey Check": "Failed standard opening and closing branding scripts.",
        "Paraphrasing": "Failed to paraphrase customer's router power disconnection fault in own words.",
        "Active listening": "Asked customer at turn 42 for router model which was already provided at turn 3.",
        "Took ownership of the problem": "Refused to replace faulty power adapter on a 5-month-old router, demanded £39.99, and suggested taping the power plug.",
        "Build rapport and observed professionalism": "Spoke rudely at turn 11 blaming customer for wobbly furniture and kicking cables.",
        "Confirmed the issue is resolved": "Issue was left completely unresolved with router continuing to lose power intermittently."
    }

    evidence = {
        "Branding and Survey Check": "Agent failed standard opening branding ('Good afternoon, broadband technical line...') and closing branding.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Nadia throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I understand how terrifying and stressful it is to have your connection cut out during intensive care hospital bed allocations...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent never restated the power plug fault in own words.",
        "Active listening": "Agent asked for router model at turn 42 despite customer stating S-Net Hub 4 at turn 3.",
        "Took ownership of the problem": "Agent stonewalled customer and demanded £39.99 for replacement adapter.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you place your sensitive broadband router on a wobbly hallway table where people kick the cables, of course the power plug is going to loosen.'",
        "Probing": "Agent gathered details on power drops and barrel socket behavior.",
        "Confirmed the issue is resolved": "Hardware remained loose, no replacement was dispatched, and customer disconnected dissatisfied."
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
        "cid": "agt_067",
        "cname": "Nadia",
        "target_dur": 924,
        "scenario": "Broadband intermittent disconnections caused by faulty power supply adapter barrel plug; unresolved",
        "tier": "poor",
        "expected_score": 35.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Branding and Survey Check", "Build rapport and observed professionalism", "Confirmed the issue is resolved", "Took ownership of the problem"],
        "notes": "Poor call marked by failed branding, rude accusations, refusal to replace faulty power adapter, and repeated questioning in the last third, with handled empathy."
    }

print("get_call_067 defined.")

# =========================================================================
# Call 068: Nathan, Mobile text messages (SMS) failing to deliver, 13:04 (784s)
# 3-4 faults (okay), score 60.0, Branding FAIL, Active listening FAIL, Rapport FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_068():
    raw = [
        # Branding FAIL: Missing standard greeting
        ("Agent", "Mobile technical queries, my name is Simon.", None),
        ("Customer", "Hello Simon, my name is Nathan Cross. I cannot receive any incoming text messages or two-factor authentication SMS codes on my Samsung phone: voice calls and 4G data work fine, but text messages have completely stopped delivering for three days!", -32.4),
        ("Agent", "Good afternoon Nathan. If I understand correctly, your mobile phone has stopped delivering all incoming SMS text messages and bank verification passcodes while your voice and data connections remain functional. Before we run diagnostic checks, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 79 Queensway, Southampton, SO14 3BL, security PIN 9914, mobile number 07700 900612.", -5.2),
        ("Agent", "Thank you Nathan, that confirms your account details. Have you checked whether your Samsung Messages app spam filter is intercepting shortcode numbers?", None),
        ("Customer", "I checked the spam folder, cleared the app cache, and even tried a third-party messaging app; no SMS messages are arriving at all!", -22.4),
        ("Agent", "Could I place you on hold for two minutes while I query the mobile SMS router routing gateway?", None),
        ("Agent", "Thank you for holding, Nathan. The core mobile gateway indicates that your SIM card's SMS Center number was cleared during a recent Android system update.", None),
        ("Customer", "Why would an Android system update wipe out my SMS Center number?", -14.2),
        ("Agent", "Operating system patches occasionally overwrite carrier APN and SMSC parameters stored on the SIM card.", None),
        ("Customer", "Can you push the correct SMSC number over the air to my phone?", -6.4),
        ("Agent", "If you keep entering the wrong verification codes into your banking app, the bank blocks your account; that isn't our network's fault.", None),
        ("Customer", "I didn't enter the wrong codes! The codes never arrived because your network isn't delivering SMS! Why are you blaming me?!", -52.4),
        ("Agent", "I am explaining how automated fraud prevention mechanisms lock customer profiles.", None),
        ("Customer", "I don't care about the bank's fraud software right now! I need the SMS Center number updated on my SIM card!", -44.2),
        ("Agent", "The national S-Net SMSC address is plus forty-four seven seven eight five zero one six zero zero zero.", None),
        ("Customer", "Where do I input that number on a Samsung Galaxy S23?", -18.2),
        ("Agent", "Open Samsung Messages, tap the three dots menu, select Settings, tap More Settings, and tap Text Messages.", None),
        ("Customer", "Found it: 'Message Centre'. It is currently set to blank!", 2.4),
        ("Agent", "Obviously mobile handsets route text messages through the international Short Message Service Center address stored on the SIM card.", None),
        ("Customer", "Typing in +447785016000 now... Tapped Set. It is saved.", 8.4),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Nathan speaking, I have missed three urgent SMS security passcodes from my bank, and my online banking account is now locked! I have mortgage settlement funds due today and I cannot authorize the wire transfer because S-Net cannot deliver a simple text message! I am about to lose the purchase of my home and I am beyond furious!", -64.2),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand the intense panic and fury this is causing with your mortgage settlement at stake today, Nathan. Missing bank verification passcodes when buying a home is an emergency, and I will diagnose your mobile text delivery profile immediately.", None),
        ("Customer", "Can you send a test SMS from your network switchboard to see if messages deliver now?", -12.2),
        ("Agent", "I have dispatched an automated gateway test message to your mobile number.", None),
        ("Customer", "I am watching my phone screen... Nothing is coming through.", -16.4),
        ("Agent", "SMSC routing updates require an over-the-air network re-registration cycle.", None),
        ("Customer", "How long does that network re-registration take?", -8.2),
        ("Agent", "The Home Location Register propagates SMS routing updates within two to twenty-four hours.", None),
        ("Customer", "Two to twenty-four hours?! My mortgage wire transfer deadline is at four o'clock this afternoon!", -48.2),
        ("Agent", "Core mobile network routing propagation cannot be accelerated for individual subscriber records.", None),
        ("Customer", "So I cannot receive my bank passcodes before four o'clock today?!", -38.4),
        ("Agent", "You would have to contact your bank and request telephone voice verification instead of SMS passcodes.", None),
        ("Customer", "My bank only offers SMS two-factor authentication for wire transfers over ten thousand pounds.", -24.2),
        ("Agent", "Telecommunications carriers do not control banking security protocols.", None),
        ("Customer", "This delay is putting my entire home purchase at extreme risk.", -28.4),
        ("Agent", "I have verified that the SMSC configuration is now correct on both your SIM and our HLR.", None),
        ("Customer", "So the fix is applied, but the network propagation prevents it working right now.", -18.2),
        ("Agent", "Correct. The messages will deliver once carrier propagation completes.", None),
        ("Customer", "I see. I will have to telephone my solicitor and beg for an extension on the mortgage settlement.", -22.4),
        ("Agent", "I have documented your SMSC update under mobile case reference SMS-88192-N.", None),
        ("Customer", "SMS-88192-N, noted down.", -12.4),
        # Turn 42: Active listening repeat in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Before I update the mobile profile, what was your mobile number again?", None),
        # Turn 43: Customer answers repeat
        ("Customer", "Like I said earlier, it is 07700 900612.", -16.2),
        ("Agent", "I have attached the mobile number to the formal network propagation ticket.", None),
        ("Customer", "I hope the text messages start arriving before the close of business.", -14.2),
        ("Agent", "You can restart your handset every hour to prompt the phone to poll the network for pending SMS queues.", None),
        ("Customer", "I will reboot the phone at the top of every hour.", -8.2),
        ("Agent", "I have also waived this month's mobile line rental charge as a goodwill gesture for the disruption.", None),
        ("Customer", "Thank you for the credit, but the priority was getting those bank passcodes.", -12.4),
        ("Agent", "Is there any other mobile issue I can assist you with today, Nathan?", None),
        ("Customer", "No Simon, that is all.", -14.2),
        ("Agent", "Goodbye.", None),
        ("Customer", "Goodbye.", -12.0),
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
        "Paraphrasing": "PASS",
        "Active listening": "FAIL",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Branding and Survey Check": "Failed standard opening and closing branding scripts.",
        "Active listening": "Asked customer at turn 42 for his mobile number which was already provided at turn 3.",
        "Build rapport and observed professionalism": "Spoke rudely at turn 11 blaming customer for entering wrong codes into banking app.",
        "Confirmed the issue is resolved": "Failed to confirm SMS delivery on call due to 2-24 hour propagation window; test SMS failed to arrive."
    }

    evidence = {
        "Branding and Survey Check": "Agent failed standard opening branding ('Mobile technical queries...') and closing branding.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Nathan throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand the intense panic and fury this is causing with your mortgage settlement at stake today, Nathan...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent paraphrased the SMS issue accurately.",
        "Active listening": "Agent asked for mobile number at turn 42 despite customer stating 07700 900612 at turn 3.",
        "Took ownership of the problem": "Agent guided customer through SMSC reconfiguration, dispatched test message, and waived line rental charge.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you keep entering the wrong verification codes into your banking app, the bank blocks your account; that isn't our network's fault.'",
        "Probing": "Agent asked about messaging app spam filters and error messages.",
        "Confirmed the issue is resolved": "Test SMS did not arrive on call and customer was advised to wait 2-24 hours for carrier propagation."
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
        "cid": "agt_068",
        "cname": "Nathan",
        "target_dur": 784,
        "scenario": "Mobile text messages (SMS) failing to deliver; SMSC restored but carrier propagation prevents live verification",
        "tier": "okay",
        "expected_score": 60.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Branding and Survey Check", "Build rapport and observed professionalism", "Confirmed the issue is resolved"],
        "notes": "Okay call featuring failed branding, rude deflection, and unverified resolution due to network propagation delay, alongside handled empathy in the middle third."
    }

print("get_call_068 defined.")

# =========================================================================
# Call 069: Neil, TV channel guide showing 'No Information Available', 16:02 (962s)
# 1-2 faults (good), score 83.3, Rapport FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_069():
    raw = [
        ("Agent", "Thank you for calling S-Net TV technical support, my name is Fiona. How can I help you today?", None),
        ("Customer", "Hello Fiona, my name is Neil Gallagher. Our S-Net TV box electronic program guide displays 'No Information Available' across every single broadcast channel, which means we cannot see what shows are on, set scheduled recordings, or use the accessibility features for my elderly father!", -32.4),
        ("Agent", "Good afternoon Neil. If I understand correctly, your TV set-top box electronic program guide is displaying 'No Information Available' across all channels, preventing you from viewing schedules or setting recordings. Before we inspect your TV box data stream, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 22 Roman Way, St Albans, AL3 5HB, security PIN 4410, TV box account SN-TV-661204.", -5.2),
        ("Agent", "Thank you Neil, that confirms your account details. Have you tried leaving the box on channel 100 for twenty minutes to download the broadcast carousel?", None),
        ("Customer", "I left it on channel 100 all morning, rebooted the box twice, and the entire guide grid remains completely blank with 'No Information Available'!", -24.2),
        ("Agent", "Could I place you on hold for two minutes while I query your set-top box electronic program guide data stream?", None),
        ("Agent", "Thank you for holding, Neil. The telemetry shows that your box's EPG metadata database cache has desynchronized from our regional terrestrial multiplexer.", None),
        ("Customer", "Can you force an administrative EPG cache rebuild from your console?", -14.2),
        ("Agent", "I can send an over-the-air command to purge the local corrupt EPG database cache and re-subscribe to the live multiplex carousel.", None),
        ("Customer", "That sounds like the exact procedure required.", 2.4),
        ("Agent", "If you leave the TV box in standby mode instead of letting it run its nightly software maintenance cycles, you starve the guide of updates.", None),
        ("Customer", "We leave the box powered on standby every night! The software should maintain itself automatically!", -48.2),
        ("Agent", "I am stating how automatic software synchronization cycles operate on our platform.", None),
        ("Customer", "Please execute the EPG cache rebuild command right now.", -22.4),
        ("Agent", "I am transmitting the EPG cache flush packet to your TV box IP address.", None),
        ("Customer", "The TV screen just flashed black for a second and returned to BBC One.", 6.2),
        ("Agent", "The local EPG database cache has been cleared successfully.", None),
        ("Customer", "Should I press the Guide button on the remote control now?", 12.2),
        ("Agent", "Obviously electronic program guide carousels require continuous background data broadcast reception to populate seven-day schedules.", None),
        ("Customer", "Right, I understand it takes time to download seven days of schedule data.", 14.5),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Neil speaking, my elderly father is partially sighted and relies entirely on the TV program guide speech synthesizer to navigate channels! Because your guide says 'No Information Available' on every channel, he cannot find his evening news and is sitting in the dark confused and distressed! It breaks my heart to see him struggling because of your broken software!", -62.4),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand how distressing and heartbreaking that is for you and your father, Neil. Having an accessible program guide is essential for someone who is partially sighted to enjoy television independently, and I will resolve this EPG data stream with you right away.", None),
        ("Customer", "Thank you Fiona, that means a lot to hear.", -4.2),
        ("Agent", "I have triggered a high-speed broadband metadata push directly over your home Wi-Fi to supplement the broadcast carousel.", None),
        ("Customer", "Checking the Guide now... Channel 1, 2, and 3 now display 'BBC One News', 'BBC Two', and 'ITV1'!", 24.5),
        ("Agent", "The immediate two-hour viewing window has loaded over the IP connection.", None),
        ("Customer", "The speech synthesizer works again for the current channels! My father can hear the show titles!", 32.4),
        ("Agent", "The full seven-day guide grid will populate progressively over the next three to four hours via the background multiplexer.", None),
        ("Customer", "Can we confirm right now whether tomorrow and the weekend will populate properly?", 14.2),
        ("Agent", "Because the full seven-day broadcast carousel broadcasts in twenty-minute cycles across sixty channels, the complete week cannot be verified while we are on this call.", None),
        ("Customer", "So we can confirm today is working, but tomorrow and Friday must be checked later tonight?", 12.2),
        ("Agent", "Correct, the full weekly guide will finish caching by eight o'clock this evening.", None),
        ("Customer", "I understand. As long as tonight's news works for my father right now, that solves his immediate distress.", 22.4),
        ("Agent", "I have added a maintenance flag on your TV profile to monitor guide ingestion over the next forty-eight hours.", None),
        ("Customer", "Thank you Fiona, that is very diligent.", 24.8),
        ("Agent", "I have also documented this ticket under reference TV-GUIDE-88192-G.", None),
        ("Customer", "TV-GUIDE-88192-G, noted down.", 20.2),
        ("Agent", "If the weekend guide shows any missing information tomorrow morning, you can power-cycle the box once to force a refresh.", None),
        ("Customer", "Understood. I will reboot it in the morning if needed.", 18.4),
        ("Agent", "The accessibility speech synthesis settings have also been verified on your account profile.", None),
        ("Customer", "Everything is working smoothly for him right now.", 24.5),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just ensuring my technical notes match your exact customer account: that was SN-TV-661204, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, SN-TV-661204 is our TV box account.", 22.4),
        ("Agent", "Thank you Neil, all diagnostic logs and accessibility flags are permanently committed.", None),
        ("Customer", "Thank you for getting the speech synthesizer working so quickly for my dad.", 28.4),
        ("Agent", "It has been my pleasure assisting you, Neil. Please give my warmest regards to your father.", None),
        ("Customer", "I will do. Have a lovely evening, Fiona.", 26.2),
        ("Agent", "Is there any other TV issue I can assist you with today, Neil?", None),
        ("Customer", "No Fiona, that covers everything.", 24.5),
        ("Agent", "Thank you for calling S-Net TV technical support, Neil. Have a wonderful evening. Goodbye.", None),
        ("Customer", "Goodbye Fiona.", 22.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None),
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
        "Active listening": "PASS",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "FAIL",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "FAIL"
    }

    coaching = {
        "Build rapport and observed professionalism": "Spoke rudely at turn 11 blaming customer for starving the TV box of updates by leaving it on standby.",
        "Confirmed the issue is resolved": "Failed to confirm full seven-day guide resolution on call due to 4-hour background multiplexer broadcast ingestion window."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net TV technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Neil throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at turn 22 ('I completely understand how distressing and heartbreaking that is for you and your father, Neil...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased the EPG issue at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer account at turn 42.",
        "Took ownership of the problem": "Agent flushed EPG cache, pushed IP metadata, verified immediate channels, and logged ticket.",
        "Build rapport and observed professionalism": "Agent insulted customer at turn 11: 'If you leave the TV box in standby mode instead of letting it run its nightly software maintenance cycles, you starve the guide of updates.'",
        "Probing": "Agent gathered details on channel 100 behavior and reboot outcomes.",
        "Confirmed the issue is resolved": "Current channels loaded but full 7-day guide required 3-4 hours to populate and could not be verified on call."
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
            {"kind": "handled", "customer_turn": 21, "agent_turn": 22, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_069",
        "cname": "Neil",
        "target_dur": 962,
        "scenario": "TV channel guide showing 'No Information Available' across all channels; EPG cache rebuilt but full week requires background ingestion",
        "tier": "good",
        "expected_score": 83.3,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Build rapport and observed professionalism", "Confirmed the issue is resolved"],
        "notes": "Good call where agent was mostly polite and empathetic, resolving immediate guide issues, failing rapport for one rude remark and confirmed resolved due to background carousel download duration."
    }

print("get_call_069 defined.")

# =========================================================================
# Call 070: Nora, New tenant unable to order broadband due to ex-tenant asset block, 19:37 (1177s)
# 0 faults (excellent), score 100.0, All PASS
# =========================================================================
def get_call_070():
    raw = [
        ("Agent", "Thank you for calling S-Net customer provisions and moves, my name is Gemma. How can I help you today?", None),
        ("Customer", "Hello Gemma, my name is Nora Thorne. I moved into my new rented flat on Monday, but when I attempted to order full fibre broadband on your website, the system blocked the order with an error saying 'Active Asset In Place - Existing Customer Must Cease Line First', even though the previous tenant moved out two weeks ago and left no forwarding address!", -34.8),
        ("Agent", "Good afternoon Nora. If I understand correctly, you are attempting to order broadband at your new flat, but our order portal is blocking your request because an active asset from the previous tenant is still registered to the property line. Before we inspect the Openreach address database, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is Flat 4B, St Mary's Court, Oxford, OX1 1QD, tenancy start date October 1st, customer reference BB-772910, security PIN 9931.", -5.2),
        ("Agent", "Thank you Nora, that confirms your account details. Do you have a copy of your signed tenancy agreement or utility bill available in digital format?", None),
        ("Customer", "Yes, I have our formal signed tenancy agreement from the Oxford letting agency as a PDF right here on my phone.", -14.2),
        ("Agent", "Could I place you on hold for two minutes while I query the Openreach address matching portal and previous tenancy records?", None),
        ("Agent", "Thank you for holding, Nora. The national asset database confirms that an active copper line belonging to the former occupier remains attached to Flat 4B under a legacy provider.", None),
        ("Customer", "Can that legacy copper service be cancelled so S-Net can install our fibre broadband?", -10.4),
        ("Agent", "Yes, we can initiate a Forced Asset Cessation workflow under the national telecommunications regulator's Right to Provide regulations.", None),
        ("Customer", "How does a Forced Asset Cessation workflow work?", -2.4),
        ("Agent", "I will upload your verified tenancy agreement to the Openreach central clearinghouse to prove change of legal occupancy.", None),
        ("Customer", "Where should I email the PDF tenancy agreement?", 4.2),
        ("Agent", "I have sent a secure document upload link via SMS to your registered mobile phone.", None),
        ("Customer", "Opening SMS link... Uploading Oxford_Tenancy_Flat4B.pdf... Upload complete!", 12.2),
        ("Agent", "I have received and validated page one and the signature page of your tenancy agreement.", None),
        ("Customer", "That was remarkably fast. Does that release the property asset?", 18.4),
        ("Agent", "The Openreach asset validation portal has approved the occupancy override command.", None),
        ("Customer", "So the phantom line has been officially decoupled from Flat 4B?", 22.4),
        ("Agent", "Obviously Openreach copper pairs and optical fibers cannot be double-provisioned to two separate account holders simultaneously.", None),
        ("Customer", "Right, I understand the technical reason for the block.", 24.5),
        # Turn 21: Customer outburst in middle third (21/58 = 0.362 >= 0.33)
        ("Customer", "Nora speaking, I moved into my new flat three days ago and your sales website blocked my broadband order stating an active service is already present! I work as a freelance graphic designer on strict deadlines, and I have had to work out of a noisy coffee shop with no secure internet! I am paying rent on an empty flat while losing client contracts because S-Net cannot turn off an ex-tenant's phantom line! I am stressed to the absolute limit!", -64.8),
        # Turn 22: Agent handled empathy
        ("Agent", "I completely understand the intense stress and financial anxiety this is causing you, Nora, especially when you are trying to settle into your new flat and meet crucial design deadlines for your clients. Being blocked by a previous tenant's dormant line is extremely frustrating, and I will initiate the forced asset cessation and expedite your new connection immediately.", None),
        ("Customer", "Thank you Gemma, I cannot tell you how much of a relief it is to hear that.", -2.4),
        ("Agent", "Now that the occupancy override has been committed, I can build your new Full Fibre 500 broadband order directly.", None),
        ("Customer", "What engineer installation dates are available for Oxford?", 6.2),
        ("Agent", "Standard installation slots are five days out, but because of the delayed asset block, I am applying priority expediting to book an appointment for this Friday morning.", None),
        ("Customer", "This Friday morning?! That is only two days away!", 26.4),
        ("Agent", "Yes, the Openreach optical installer will arrive between eight in the morning and one in the afternoon on Friday.", None),
        ("Customer", "Will the engineer install a brand new optical ONT box inside the flat?", 24.2),
        ("Agent", "Yes, the engineer will run the external fiber drop cable, mount the internal ONT box, and test full gigabit optical light levels.", None),
        ("Customer", "And will the S-Net Hub router arrive before Friday?", 22.4),
        ("Agent", "I have dispatched the S-Net Hub via DPD next-day courier, tracking number DPD-881920-X.", None),
        ("Customer", "DPD-881920-X, noted down. It should arrive tomorrow afternoon then.", 28.2),
        ("Agent", "I have also waived the sixty-pound expedited installation charge and the thirty-pound activation fee.", None),
        ("Customer", "You have saved me ninety pounds! Thank you so much, Gemma.", 34.5),
        ("Agent", "Your monthly tariff will be thirty-four pounds per month on our special new-home promotional tier.", None),
        ("Customer", "That is cheaper than the package I originally tried to order online.", 36.2),
        ("Agent", "I am emailing you the full pre-contract information packet and order confirmation right now.", None),
        ("Customer", "Checking email on my phone... Yes, order confirmation received: 'S-Net Order ORD-449102-N - Installation Friday 17th'.", 38.4),
        ("Agent", "Everything is completely locked in with Openreach national provisioning.", None),
        ("Customer", "I can finally tell my clients that my studio will be fully connected by the weekend.", 36.2),
        # Turn 42: Active listening harmless recheck in last third (42/58 = 0.724 >= 0.66)
        ("Agent", "Just ensuring my tenancy documentation order has your exact flat address: that was Flat 4B, St Mary's Court, Oxford, wasn't it?", None),
        # Turn 43: Customer answers recheck
        ("Customer", "Yes, Flat 4B, St Mary's Court, Oxford.", 28.4),
        ("Agent", "Thank you Nora, all address assets and engineering dispatches are fully synchronized.", None),
        ("Customer", "You have provided absolute top-tier service today, Gemma. You turned an awful situation into a great experience.", 36.8),
        ("Agent", "It has been an absolute delight assisting you, Nora. Congratulations on your new flat in Oxford.", None),
        ("Customer", "Thank you so much. Have a wonderful rest of your week.", 32.4),
        ("Agent", "Is there any other aspect of your new broadband order I can assist you with today, Nora?", None),
        ("Customer", "No Gemma, everything is handled perfectly.", 30.2),
        ("Agent", "Thank you for calling S-Net customer provisions and moves, Nora. Welcome to S-Net. Goodbye.", None),
        ("Customer", "Goodbye Gemma.", 28.4),
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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net customer provisions and moves' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with could I place you on hold and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Nora throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated exceptional empathy at turn 22 ('I completely understand the intense stress and financial anxiety this is causing you, Nora...') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent accurately paraphrased previous occupier line blockage issue at turn 2.",
        "Active listening": "Agent completed harmless recheck of customer flat address at turn 42.",
        "Took ownership of the problem": "Agent verified tenancy agreement, executed forced cessation, expedited Friday installation, and waived £90 in fees.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, comforting, and highly professional demeanor throughout.",
        "Probing": "Agent gathered details on tenancy documentation and occupancy dates.",
        "Confirmed the issue is resolved": "Order confirmed, Friday appointment booked, router tracking provided, and customer received full email contract documentation."
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
        "cid": "agt_070",
        "cname": "Nora",
        "target_dur": 1177,
        "scenario": "New tenant unable to order broadband due to previous occupier asset block; resolved via tenancy verification and expedited install",
        "tier": "excellent",
        "expected_score": 100.0,
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": [],
        "notes": "Flawless move/provisioning call showcasing deep empathy in the middle third, harmless recheck in the final third, ownership, and expedited resolution."
    }

print("get_call_070 defined.")

if __name__ == "__main__":
    for fn in [get_call_066, get_call_067, get_call_068, get_call_069, get_call_070]:
        c = fn()
        compile_call(c)
