import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from batch_engine import compile_call

# =========================================================================
# Call 026: Dorothy, Stream TV puck remote pairing, 10:55 (655s)
# 1-2 faults (good), score 88.3, Empathy FAIL
# =========================================================================
def get_call_026():
    raw = [
        ("Agent", "Thank you for calling S-Net TV customer support, my name is Toby. How can I help you today?", None),
        ("Customer", "Hello Toby, my name is Dorothy Evans. My S-Net Stream TV puck is stuck on a screen with a spinning circle telling me to pair the remote control, and nothing happens when I press the buttons!", -28.5),
        ("Agent", "Good morning Dorothy. I can certainly help you pair your remote control and get your TV puck working. Before we begin troubleshooting, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 14 Meadow View, Harrogate, HG1 4QW, and my security PIN is 7150. My account reference is SN-302918.", -4.2),
        ("Agent", "Thank you Dorothy, that confirms your account details. What color is the small light on the front of the remote flashing when you press any key?", None),
        ("Customer", "It flashes a fast red light three times and then turns off, and the TV screen just keeps showing the remote pairing instruction graphic.", -24.1),
        ("Agent", "So what is happening is that your Stream puck is stuck on the remote pairing screen displaying the setup graphic, and the remote LED is flashing red three times indicating Bluetooth unpairing rather than solid blue, is that right?", None),
        ("Customer", "Yes, that is exactly what it is doing! My twelve-year-old grandson reset the TV box before school, and now I have no television at all!", -18.4),
        ("Agent", "Let us check the remote hardware first. Have you tried putting a brand new pair of AAA alkaline batteries into the remote?", None),
        ("Customer", "Yes, I put two fresh Duracell batteries in just ten minutes ago, but it made no difference whatsoever.", -12.2),
        ("Agent", "Bear with me for a couple of minutes while I check the firmware version registered to your Stream puck on our device management server.", None),
        ("Agent", "Thank you for waiting, Dorothy. Your puck is on the latest TVOS 4.2 firmware build, so the issue is simply an unlinked Bluetooth pairing profile.", None),
        ("Customer", "I am having my daughter and grandchildren over in less than an hour for our weekly family movie night, and having a blank television is driving me to tears! I am so frantic that the evening will be ruined!", -54.2),
        ("Agent", "Check if the small plastic infrared sensor window on the front edge of the puck is physically blocked by any books or photo frames.", None),
        ("Customer", "No, the puck sits completely clear on the wooden TV stand directly underneath the screen.", -18.5),
        ("Agent", "We are going to perform a hard hardware reset on the remote control itself to clear its Bluetooth memory cache.", None),
        ("Customer", "Alright Toby, tell me what buttons I need to press.", -6.2),
        ("Agent", "Press and hold the number seven and number nine buttons together simultaneously until the light at the top flashes red four times.", None),
        ("Customer", "Holding seven and nine down now... one, two, three... Yes, it just flashed red four times!", 14.5),
        ("Agent", "Excellent. That has completely wiped the old pairing connection from the remote control.", None),
        ("Customer", "Now what is the next step?", 8.2),
        ("Agent", "Now pick up the remote and point it directly at the S-Net puck from about one metre away.", None),
        ("Customer", "Pointing it directly at the front of the puck now.", 12.1),
        ("Agent", "Obviously consumer remotes cannot bind while Bluetooth discovery mode is timed out.", None),
        ("Customer", "I am standing right in front of the TV unit.", 15.4),
        ("Agent", "Now press and hold the number one and number three buttons together simultaneously for three seconds.", None),
        ("Customer", "Holding one and three together... The light is flashing blue! And the screen just popped up saying 'Remote Connected'!", 56.8),
        ("Agent", "Brilliant! Now use the directional arrow buttons to highlight 'Continue' on your TV screen.", None),
        ("Customer", "Pressing Continue... The home screen has loaded! All my apps and channel tiles are visible!", 64.2),
        ("Agent", "Let us select BBC iPlayer or live broadcast to make sure video and audio stream with perfect synchronization.", None),
        ("Customer", "I have clicked on BBC One... Yes, the midday news is playing with clear picture and perfect sound!", 48.6),
        ("Agent", "And does the volume rocker on the right side of the remote control adjust your television volume properly?", None),
        ("Customer", "Yes, turning it up and down works seamlessly. It controls my TV set volume directly.", 32.4),
        ("Agent", "That confirms the infrared TV CEC volume code was retained successfully during pairing.", None),
        ("Customer", "That is such a relief. My movie night with my family is completely saved now.", 28.5),
        ("Agent", "Just remember that if your grandson ever triggers a factory reset in the future, pressing one and three together will immediately re-pair the remote.", None),
        ("Customer", "I have written that down on a piece of paper stuck behind the TV: press one and three together.", 19.4),
        ("Agent", "That is a very sensible place to keep the instruction note, Dorothy.", None),
        ("Customer", "Thank you Toby, you explained everything so clearly and patiently.", 24.1),
        ("Agent", "Before we complete our call, that account contact telephone number was 01423 884190, correct?", None),
        ("Customer", "Yes, 01423 884190 is my home landline.", 14.2),
        ("Agent", "We have cleared the remote memory, re-established Bluetooth pairing, and confirmed live TV and volume control function normally.", None),
        ("Customer", "Everything is working like new. I am so grateful for your help.", 31.2),
        ("Agent", "You can also control your Stream puck using the S-Net TV companion app on an iPad if the physical remote ever runs out of batteries.", None),
        ("Customer", "My daughter has an iPad, so I will ask her to download that app tonight as a backup.", 16.5),
        ("Agent", "Is there anything else regarding your S-Net Stream TV service or broadband I can help you with today, Dorothy?", None),
        ("Customer", "No thank you Toby, you have resolved my problem completely.", 22.4),
        ("Agent", "Thank you for choosing S-Net customer services, Dorothy. Have a fantastic movie night with your grandchildren. Goodbye.", None),
        ("Customer", "Goodbye Toby.", 18.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Your Stream puck will perform automatic software maintenance checks at three o'clock every morning.", None))
        raw.insert(-4, ("Customer", "That is very reassuring to know it updates itself while we are sleeping.", 11.2))
        raw.insert(-4, ("Agent", "You can always leave the puck in low-power standby mode when you finish watching television.", None))
        raw.insert(-4, ("Customer", "I will be sure to put it into standby with the power button tonight.", 14.6))

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
        "Empathy & Acknowledgment Statement": "Failed to acknowledge customer distress at [02:50] when she expressed severe panic about family movie night being ruined."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net TV customer support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Dorothy throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute worry and distress about impending family movie night; agent ignored feelings and moved directly to TV stand clearance.",
        "Paraphrasing": "Agent restated the remote unpairing and flashing red light accurately at [01:25].",
        "Active listening": "Agent maintained accurate details and confirmed contact phone number without repetition.",
        "Took ownership of the problem": "Agent guided customer step-by-step through remote reset and pairing commands.",
        "Build rapport and observed professionalism": "Agent maintained a calm, polite, and helpful tone throughout.",
        "Probing": "Agent asked targeted diagnostic questions regarding LED status, battery health, and infrared obstruction.",
        "Confirmed the issue is resolved": "Customer confirmed remote paired, home screen loaded, BBC One stream played, and volume control worked."
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
            {"kind": "blunt_but_ok", "agent_turn": 23}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 12}
        ]
    }

    return {
        "cid": "agt_026",
        "cname": "Dorothy",
        "target_dur": 655,
        "scenario": "S-Net Stream TV puck stuck on remote pairing screen after factory reset",
        "tier": "good",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Empathy & Acknowledgment Statement"],
        "notes": "Solid technical resolution of Bluetooth remote pairing on Stream puck, but agent failed to acknowledge customer's family movie night distress."
    }

print("get_call_026 defined.")
# =========================================================================
# Call 027: Dylan, Outlook rejecting webmail password, 15:39 (939s)
# 3-4 faults (okay), score 71.7, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL
# =========================================================================
def get_call_027():
    raw = [
        ("Agent", "Thank you for calling S-Net broadband technical support, my name is Marcus. How can I help you today?", None),
        ("Customer", "Hello Marcus, my name is Dylan Price. My desktop Outlook application has completely stopped sending and receiving emails for my S-Net account, and keeps throwing an invalid password error prompt every thirty seconds!", -32.5),
        ("Agent", "Good afternoon Dylan. I can inspect your email mailbox routing and IMAP authentication parameters. Before we access your mailbox configuration, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 83 Castle Street, Cardiff, CF10 1BS, and my security PIN is 4429. My S-Net email address is dylan.accountant@snet-mail.co.uk.", -6.4),
        ("Agent", "Thank you Dylan, that confirms your account details. What specific error message or diagnostic code appears in Microsoft Outlook?", None),
        ("Customer", "A pop-up window keeps appearing saying 'Enter your user name and password for the following server: imap.snet-mail.co.uk.' I type my regular webmail password, click OK, and the exact same box immediately pops up again!", -28.2),
        ("Agent", "Can you still log into your webmail account through an internet browser on our website using that exact password?", None),
        ("Customer", "Yes, I logged into webmail on Google Chrome ten minutes ago without any problem using that password, but Outlook on my desktop keeps rejecting it.", -14.5),
        ("Agent", "Bear with me for a couple of minutes while I check your email account status and modern authentication security flags on our mail cluster.", None),
        ("Agent", "Thank you for waiting, Dylan. Your mailbox account is active, but our mail system completed an automated security migration to mandatory dedicated application passwords last weekend.", None),
        ("Customer", "I am a chartered accountant with corporation tax filings due to HMRC before five o'clock this evening! If I cannot send client tax returns through Outlook, I will incur substantial financial and professional penalties! I am frantic with worry!", -58.4),
        ("Agent", "When third-party desktop mail applications connect to S-Net mailboxes, they can no longer authenticate using your primary webmail login password.", None),
        ("Customer", "Why wasn't I informed of this change before my email abruptly stopped working during my busiest tax week of the quarter?!", -44.2),
        ("Agent", "Notification emails were dispatched to all primary mailbox accounts thirty days prior to security protocol enforcement.", None),
        ("Customer", "I never received any such email! What do I actually need to do in Outlook right now to fix this?", -32.1),
        ("Agent", "You must generate an encrypted sixteen-character application password within your webmail account security settings.", None),
        ("Customer", "I have my webmail open in Chrome right now. Where do I click to generate this app password?", -12.4),
        ("Agent", "Obviously older desktop clients do not support OAuth modern authentication without generating dedicated app passwords.", None),
        ("Customer", "I understand that, Marcus, but please guide me through the menu on the screen.", -18.2),
        ("Agent", "Click on the gear icon in the top right corner of the webmail window to access Settings.", None),
        ("Customer", "Clicked on Settings. Now what?", -4.1),
        ("Agent", "On the left navigation sidebar, select 'Security & Connected Devices'.", None),
        ("Customer", "Selected Security and Connected Devices. I see a section called 'Application Passwords'.", 12.4),
        ("Agent", "Click on the blue button that says 'Generate New App Password'.", None),
        ("Customer", "Clicked it. It asks for a label name for the application.", 14.2),
        ("Agent", "Enter 'Desktop Outlook' in the label box and click 'Generate'.", None),
        ("Customer", "Entered Desktop Outlook and clicked Generate. A sixteen-character password has appeared in bold text.", 22.1),
        ("Agent", "Do not close that web browser tab because that password is only displayed once for security reasons.", None),
        ("Customer", "Keeping the browser tab open. Now how do I put it into Microsoft Outlook?", 16.4),
        ("Agent", "Open Microsoft Outlook and bring up that server password pop-up prompt.", None),
        ("Customer", "The pop-up box is in front of me right now.", 8.2),
        ("Agent", "Clear whatever password is currently typed into the password field.", None),
        ("Customer", "Cleared the password box completely.", 4.5),
        ("Agent", "What was that S-Net email address again?", None),
        ("Customer", "As I told you earlier, it's dylan.accountant@snet-mail.co.uk.", -16.2),
        ("Agent", "Copy the sixteen-character application password from your webmail screen and paste it into the Outlook password box.", None),
        ("Customer", "Pasting the sixteen-character password now... It filled with asterisks.", 18.2),
        ("Agent", "Make sure the checkbox labeled 'Save this password in your password list' or 'Remember password' is ticked.", None),
        ("Customer", "Ticked Remember password.", 14.5),
        ("Agent", "Now click the 'OK' button.", None),
        ("Customer", "Clicked OK... The pop-up box vanished! And in the bottom right corner of Outlook it says 'Connected' and 'Updating Inbox'!", 58.4),
        ("Agent", "Click 'Send / Receive All Folders' at the top of Outlook to ensure the message queue processes.", None),
        ("Customer", "Clicking Send and Receive now... Yes! Forty-two new emails just flooded into my inbox, and the outgoing HMRC submission email in my Outbox just sent successfully!", 66.8),
        ("Agent", "Let us verify your outgoing SMTP port parameters to ensure outgoing dispatch remains completely stable.", None),
        ("Customer", "I opened Account Settings: outgoing server is smtp.snet-mail.co.uk on port 587 with STARTTLS encryption.", 24.5),
        ("Agent", "Those are our exact recommended secure port specifications, Dylan.", None),
        ("Customer", "What a massive relief! My client tax return is officially delivered to HMRC on time.", 42.1),
        ("Agent", "If you also synchronize S-Net email on a mobile smartphone mail app, you will need to generate a separate app password labeled 'Mobile Phone'.", None),
        ("Customer", "I only access business email on this desktop workstation, so this single app password is all I need.", 18.2),
        ("Agent", "We have generated a dedicated sixteen-character app password, saved it in Microsoft Outlook, and confirmed both inbound and outbound synchronization work.", None),
        ("Customer", "Yes, everything is working flawlessly now. Thank you Marcus.", 26.5),
        ("Agent", "Is there any other technical matter regarding your broadband connection or email accounts I can assist you with today, Dylan?", None),
        ("Customer", "No, that was the only critical issue. Thank you for walking me through the setup.", 19.4),
        ("Agent", "Thank you for choosing S-Net broadband customer services, Dylan. Have a successful and productive afternoon. Goodbye.", None),
        ("Customer", "Goodbye Marcus.", 14.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 62:
        raw.insert(-4, ("Agent", "You can revoke that application password at any time from your webmail security dashboard if you ever replace your computer.", None))
        raw.insert(-4, ("Customer", "That is good to know for when I upgrade my office PC next year.", 12.1))
        raw.insert(-4, ("Agent", "Our mail server spam filtering heuristics will continue operating transparently in the background across all your devices.", None))
        raw.insert(-4, ("Customer", "Excellent, the junk mail filter does a very reliable job with accounting spam.", 15.4))

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
        "Empathy & Acknowledgment Statement": "Failed to acknowledge customer panic at [03:10] when facing critical HMRC tax submission deadlines.",
        "Paraphrasing": "Did not paraphrase customer's problem in own words, proceeding directly to explain technical policy.",
        "Active listening": "Asked customer at [08:50] to repeat his email address which had already been verified at [00:45]."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net broadband technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Dylan throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute stress regarding impending HMRC corporate tax deadlines; agent completely ignored feelings and defended company policy.",
        "Paraphrasing": "Agent offered no paraphrasing of the issue in his own words.",
        "Active listening": "Agent asked for customer's email handle again at turn 34 despite customer having provided it during verification at turn 3.",
        "Took ownership of the problem": "Agent guided customer through webmail settings to successfully create and apply an app password.",
        "Build rapport and observed professionalism": "Agent maintained a professional instructional tone despite minor defensiveness.",
        "Probing": "Agent asked relevant diagnostic questions about webmail access and desktop error prompts.",
        "Confirmed the issue is resolved": "Customer confirmed 42 emails downloaded and HMRC filing sent successfully from Outbox."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 33, "reworded": True}
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
        "cid": "agt_027",
        "cname": "Dylan",
        "target_dur": 939,
        "scenario": "Desktop Outlook client rejecting S-Net webmail password after app-password security migration",
        "tier": "okay",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Paraphrasing"],
        "notes": "Effective procedural resolution of application password generation, but agent failed empathy on HMRC tax deadline panic, failed paraphrasing, and repeated an email question previously answered."
    }

print("get_call_027 defined.")
# =========================================================================
# Call 028: Elena, Speed guarantee credit claim, 14:39 (879s)
# 5+ faults (poor), score 48.3, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL
# =========================================================================
def get_call_028():
    raw = [
        ("Agent", "Thank you for calling S-Net broadband cancellations and billing, my name is Ryan. How can I help you today?", None),
        ("Customer", "Hello Ryan, my name is Elena Rostova. I am calling to claim my speed guarantee compensation credit and penalty-free contract exit because my broadband download speed has been twenty-eight megabits for two weeks when my contract guarantees a minimum of forty-five!", -34.8),
        ("Agent", "Good afternoon Elena. I can look into your line speed profile. Before we inspect your broadband circuit telemetry, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 51 Victoria Road, Oxford, OX2 7TA, and my security PIN is 8014. My router model is the Hub 4 with serial number SNET-44018.", -5.2),
        ("Agent", "Thank you Elena, that confirms your account details. What speed testing tool have you been running to record twenty-eight megabits?", None),
        ("Customer", "I used the official S-Net broadband speed checker app on my desktop computer via a direct Ethernet cable, as instructed in your welcome pack.", -16.4),
        ("Agent", "And how many speed tests have you registered through the desktop application over those two weeks?", None),
        ("Customer", "I ran fourteen separate tests across morning, afternoon, and night, and every single test clocked between twenty-six and twenty-eight megabits per second.", -22.1),
        ("Agent", "Bear with me for a couple of minutes while I check the Openreach copper loop length and sync rate telemetry from our exchange test head.", None),
        ("Agent", "Thank you for waiting, Elena. The line sync history shows an automated profile cap of thirty megabits applied following multiple line retrains.", None),
        ("Customer", "I am an architect working with thirty-gigabyte BIM rendering files! I have missed two major client planning deadlines because file downloads are taking hours! Your contract explicitly promises twenty pounds automatic credit or penalty-free cancellation if speeds stay below forty-five megabits! It is outrageous being misled like this!", -62.4),
        ("Agent", "Residential speed guarantee terms require thirty consecutive days of diagnostic observation before contract exit clauses can be considered.", None),
        ("Customer", "Your website and welcome leaflet say three consecutive days below minimum guaranteed speed! Don't invent thirty-day rules to avoid paying my credit!", -51.2),
        ("Agent", "Well if you had actually bothered to read section 8 of our terms and conditions, speed guarantees require consecutive engineer visits before credits apply, so don't accuse customer service of misleading you.", None),
        ("Customer", "How dare you speak to me like that! I am quoting the exact wording from your speed guarantee charter!", -56.8),
        ("Agent", "If you wish to dispute contractual speed terms, you must submit a written dispute ticket through our online web portal.", None),
        ("Customer", "I am on the phone with customer services right now! Open a speed dispute ticket and book an engineer to inspect the line!", -42.1),
        ("Agent", "Frontline telephony agents do not submit engineer dispatch requests or speed guarantee compensation credits.", None),
        ("Customer", "Then transfer me immediately to a manager who has the authority to book an engineer and credit my account!", -38.4),
        ("Agent", "Team supervisors do not take speed guarantee dispute calls. You need to log into your online account and fill out the automated speed claim form.", None),
        ("Customer", "You refuse to book an engineer, you refuse to issue the contract credit, and you refuse to let me speak to a supervisor! This is appalling service!", -46.2),
        ("Agent", "I am informing you of the mandatory administrative procedure for speed guarantee disputes.", None),
        ("Customer", "Can you at least reset the automated profile cap on the exchange port to see if my speed increases back to forty-five megabits right now?", -24.5),
        ("Agent", "Bear with me for two minutes while I send a remote profile reset command to the DSLAM port card.", None),
        ("Agent", "Thank you for waiting, Elena. The DSLAM port has been re-initialized and the speed cap removed.", None),
        ("Customer", "Let me run another speed test on the desktop app right now... It is syncing at forty-six megabits! Forty-six point two megabits download!", 24.5),
        ("Agent", "Which model of Hub router is currently plugged into the master socket?", None),
        ("Customer", "As I said right at the start of the call, it is the Hub 4 router.", -14.2),
        ("Agent", "Obviously copper attenuation increases significantly over long line runs from the street cabinet.", None),
        ("Customer", "Well, the remote line reset has brought the speed above the forty-five megabit threshold for the moment.", 12.4),
        ("Agent", "Now that your download speed has recovered to forty-six megabits, the speed guarantee exit clause is no longer applicable.", None),
        ("Customer", "I will monitor it closely over the weekend. What is the ticket reference for the line reset you performed?", -4.2),
        ("Agent", "The reference code for the port reset is TKT-77019-S.", None),
        ("Customer", "TKT-77019-S, noted down.", 8.2),
        ("Agent", "I have logged the diagnostic results on your customer profile.", None),
        ("Customer", "If the speed drops below forty-five megabits again, I will be straight back on the phone demanding an engineer visit.", 2.1),
        ("Agent", "The line profile is set to dynamic rate adaptation to maintain stability.", None),
        ("Customer", "Very well, thank you for at least resetting the port.", 11.2),
        ("Agent", "Is there any other aspect of your broadband connection I can help you with today, Elena?", None),
        ("Customer", "No, as long as forty-six megabits holds, I can finish my architectural uploads today.", 14.5),
        ("Agent", "Thank you for choosing S-Net broadband cancellations and billing, Elena. Goodbye.", None),
        ("Customer", "Goodbye Ryan.", 8.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our automated network management systems will monitor your line stability parameters over the next forty-eight hours.", None))
        raw.insert(-4, ("Customer", "Please make sure those automated monitoring logs are retained on my customer file.", 8.4))
        raw.insert(-4, ("Agent", "All telemetry readings are permanently attached to ticket reference TKT-77019-S.", None))
        raw.insert(-4, ("Customer", "That provides a clear audit trail if speeds degrade again.", 12.1))

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
        "Empathy & Acknowledgment Statement": "Ignored customer distress and deadline frustration at [03:15] regarding architect file upload failures.",
        "Paraphrasing": "Failed to paraphrase customer's speed dispute in own words.",
        "Active listening": "Asked customer at [08:40] for her router model which had already been stated at [00:40].",
        "Took ownership of the problem": "Deflected responsibility at [05:20] by refusing to process engineer booking or claim and insisting customer use web form.",
        "Build rapport and observed professionalism": "Spoke defensively and aggressively at [04:20] stating 'Well if you had actually bothered to read section 8... don't accuse customer service of misleading you.'"
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net broadband cancellations and billing' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Holds announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Elena throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute distress over missed architectural deadlines; agent offered no empathy.",
        "Paraphrasing": "Agent never restated the customer's speed guarantee dispute in his own words.",
        "Active listening": "Agent asked for router model at turn 26 despite customer providing Hub 4 serial number at turn 3.",
        "Took ownership of the problem": "Agent refused to book an engineer or raise claim, telling customer frontline staff do not handle disputes.",
        "Build rapport and observed professionalism": "Agent insulted customer at [04:20]: 'Well if you had actually bothered to read section 8... don't accuse customer service of misleading you.'",
        "Probing": "Agent asked relevant diagnostic questions about speed test methods and test frequency.",
        "Confirmed the issue is resolved": "Customer confirmed download speed reached 46.2 Mbps following DSLAM port reset and accepted ticket reference."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 26, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "rude", "agent_turn": 13},
            {"kind": "blunt_but_ok", "agent_turn": 28}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 10}
        ]
    }

    return {
        "cid": "agt_028",
        "cname": "Elena",
        "target_dur": 879,
        "scenario": "Broadband speed guarantee credit claim after sync speed remained below 45 Mbps minimum",
        "tier": "poor",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Build rapport and observed professionalism", "Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Poor customer service call marked by agent rudeness, deflection of contractual ownership, failure of empathy, and repeated questioning, despite port reset temporarily resolving speed."
    }

print("get_call_028 defined.")
# =========================================================================
# Call 029: Elijah, Mobile 40GB data exhausted, 16:17 (977s)
# excellent, score 100.0, All PASS, Empathy with_refusal: True
# =========================================================================
def get_call_029():
    raw = [
        ("Agent", "Thank you for calling S-Net mobile customer care, my name is Sophie. How can I help you today?", None),
        ("Customer", "Hello Sophie, my name is Elijah Ward. My mobile internet connection stopped working this morning, and when I opened the S-Net app it says I have used one hundred percent of my forty-gigabyte monthly data allowance just five days into my billing cycle!", -31.4),
        ("Agent", "Good afternoon Elijah. I can inspect your data usage breakdown and cellular network provisioning. Before we access your mobile account, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 12 Cambridge Road, Bristol, BS6 6ST, and my security PIN is 5519. My mobile number is 07700 900823.", -4.5),
        ("Agent", "Thank you Elijah, that verifies your account details. What happens on your phone right now when you attempt to browse a website or load a web page over mobile data?", None),
        ("Customer", "A web redirect screen pops up stating 'You have consumed your forty gigabytes monthly data allowance. Please purchase a data booster to resume high-speed mobile internet.'", -22.1),
        ("Agent", "So what has occurred is that your monthly forty-gigabyte mobile data allowance was fully exhausted within five days of your billing cycle start, causing the network gateway to redirect your web traffic to our booster landing page, is that right?", None),
        ("Customer", "Yes, that is exactly what happened! But there is no way I used forty gigabytes of data in five days! I only browse social media and read news articles!", -18.4),
        ("Agent", "Bear with me for a couple of minutes while I pull up your granular mobile data session logs from our mobile packet gateway.", None),
        ("Agent", "Thank you for waiting, Elijah. The data session logs show a single continuous background data transmission of thirty-eight point six gigabytes between two o'clock and four o'clock this morning.", None),
        ("Customer", "I was sound asleep between two and four in the morning! I need my mobile data restored right now for client video deliveries, and I want S-Net to credit a free 50GB booster pack immediately!", -52.4),
        ("Agent", "I completely understand how stressful it is to run out of mobile data when you have urgent client deliveries pending, Elijah. However, because our cellular network logs confirm that the full forty gigabytes were uploaded by your handset to Google Drive, our billing terms do not permit issuing a free discretionary data booster; what I can do right now is activate our emergency ten-gigabyte bolt-on at a half-price concession of five pounds, and walk you through restricting your cloud synchronization app to Wi-Fi only so this never recurs.", None),
        ("Customer", "Wait... Google Drive? Oh good heavens! I plugged my 4K drone camera memory card into my phone last night and told Google Drive to back up the footage! My home Wi-Fi must have disconnected overnight!", 18.2),
        ("Agent", "That would explain the entire thirty-eight-point-six-gigabyte transfer. Mobile handsets automatically fail over to cellular data when Wi-Fi drops out unless cloud apps are strictly restricted.", None),
        ("Customer", "I am so relieved to know what actually happened. I thought my phone had been hacked. That half-price ten-gigabyte bolt-on for five pounds sounds very reasonable.", 26.5),
        ("Agent", "I have applied the emergency ten-gigabyte high-speed data bolt-on to your mobile line right now at the discounted rate of five pounds.", None),
        ("Customer", "Let me toggle aeroplane mode on and off to refresh the data connection...", 14.2),
        ("Agent", "Yes, toggling aeroplane mode forces your SIM card to re-attach to our 5G data bearer.", None),
        ("Customer", "Aeroplane mode toggled... The 5G icon is back! And my email just pinged with incoming client messages!", 48.6),
        ("Agent", "Now let us configure your Google Drive settings immediately so your phone never uploads large video files over cellular data again.", None),
        ("Customer", "Opening Google Drive app now. Where do I find the setting?", 12.1),
        ("Agent", "Tap the three horizontal menu lines in the top left, tap 'Settings', and scroll to the bottom.", None),
        ("Customer", "Scrolled to the bottom. I see an option called 'Transfer files only over Wi-Fi'.", 18.4),
        ("Agent", "Obviously background cloud services continue uploading high-resolution video whenever mobile data is enabled.", None),
        ("Customer", "I have toggled 'Transfer files only over Wi-Fi' to ON. A prompt says 'Data usage warning: Uploading and updating will pause when Wi-Fi is unavailable.'", 32.1),
        ("Agent", "That ensures that future drone 4K footage will strictly pause until your phone connects to your home wireless network.", None),
        ("Customer", "That gives me total peace of mind that I won't chew through data unexpectedly again.", 38.2),
        ("Agent", "You can also set a monthly data warning and hard data limit directly in your Android settings menu under 'Network & Internet'.", None),
        ("Customer", "Opening Network and Internet... Data warning and limit... I have set a warning at thirty-five gigabytes.", 28.4),
        ("Agent", "That gives you an early warning five gigabytes before your monthly billing threshold is reached.", None),
        ("Customer", "This ten-gigabyte bolt-on will easily last me the remaining three weeks now that Drive is locked to Wi-Fi.", 34.5),
        ("Agent", "Your standard forty-gigabyte monthly allowance will renew automatically on the first of next month.", None),
        ("Customer", "That is perfect. You have been incredibly helpful and knowledgeable, Sophie.", 42.1),
        ("Agent", "Before we conclude our call, that registered mobile phone number was 07700 900823, correct?", None),
        ("Customer", "Yes, 07700 900823.", 18.2),
        ("Agent", "We have identified the 4K cloud backup cause, activated the emergency ten-gigabyte bolt-on, verified 5G restoration, and secured your upload settings to Wi-Fi only.", None),
        ("Customer", "Everything is completely sorted. Thank you so much Sophie.", 36.4),
        ("Agent", "You can track your real-time daily data usage at any time by logging into the My S-Net mobile application.", None),
        ("Customer", "I have the app installed on my home screen and will check it regularly.", 16.5),
        ("Agent", "Is there any other matter regarding your mobile plan or billing I can assist you with today, Elijah?", None),
        ("Customer", "No thank you, everything is crystal clear.", 22.1),
        ("Agent", "Thank you for choosing S-Net mobile customer care, Elijah. Have a wonderful and creative afternoon. Goodbye.", None),
        ("Customer", "Goodbye Sophie.", 18.4),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Remember that unused bolt-on data does not roll over into subsequent billing cycles.", None))
        raw.insert(-4, ("Customer", "That is fine, I will easily use this bolt-on over the next two weeks.", 14.2))
        raw.insert(-4, ("Agent", "Our 5G network coverage has recently expanded with two new cellular base stations in central Bristol.", None))
        raw.insert(-4, ("Customer", "I noticed the speeds have been significantly faster around Clifton lately.", 19.5))

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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net mobile customer care' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Elijah warmly throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent acknowledged customer distress while politely refusing free credit at [03:45]: 'I completely understand how stressful it is... However, because our cellular network logs confirm... our billing terms do not permit issuing a free discretionary data booster; what I can do right now is activate our emergency ten-gigabyte bolt-on at a half-price concession...'",
        "Paraphrasing": "Agent restated the 40GB allowance exhaustion and landing page redirect accurately at [01:30].",
        "Active listening": "Agent confirmed mobile number accurately without asking for previously supplied information.",
        "Took ownership of the problem": "Agent identified root cause in Google Drive sync, provisioned bolt-on, and guided customer to lock app to Wi-Fi.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, empathetic, and constructive tone throughout.",
        "Probing": "Agent asked effective diagnostic questions regarding device redirect prompts and app behavior.",
        "Confirmed the issue is resolved": "Customer toggled aeroplane mode, verified 5G restored, confirmed email received, and locked Google Drive to Wi-Fi."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 33}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 6},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 23}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 10, "agent_turn": 11, "with_refusal": True}
        ]
    }

    return {
        "cid": "agt_029",
        "cname": "Elijah",
        "target_dur": 977,
        "scenario": "Mobile 40GB data allowance exhausted five days into billing cycle due to 4K cloud sync",
        "tier": "excellent",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Exemplary demonstration of acknowledgment-then-refusal where the agent validated customer stress, firmly upheld billing terms regarding verified data usage, and offered a discounted commercial compromise with practical prevention guidance."
    }

print("get_call_029 defined.")


# =========================================================================
# Call 030: Elisha, Landline number terminated during FTTP switch, 19:17 (1157s)
# 1-2 faults (good), score 88.3, Empathy FAIL (2 outbursts: 1 handled late, 1 unhandled)
# =========================================================================
def get_call_030():
    raw = [
        ("Agent", "Thank you for calling S-Net order provisioning and technical services, my name is Hannah. How can I help you today?", None),
        ("Customer", "Hello Hannah, my name is Elisha Bennett. I had my full-fibre broadband installed yesterday, but the engineer told me my landline telephone number of twenty-five years has been completely terminated and lost! My eighty-eight-year-old mother and my cardiology clinic rely on that number!", -44.2),
        ("Agent", "Good afternoon Elisha. I can investigate your optical order and voice porting record. Before we access your provisioning profile, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 64 Highfield Way, Rickmansworth, WD3 2PP, and my security PIN is 9182. The landline number that was cut off is 01923 774019.", -8.4),
        ("Agent", "Thank you Elisha, that confirms your account details. What happens right now if you dial 01923 774019 from an outside line like a mobile phone?", None),
        ("Customer", "It plays a dead automated recording saying 'The number you have dialled has not been recognized. Please check the number and try again.' Hannah, I am shaking with anxiety! My mother has dementia and cannot remember any other number, and the hospital calls that number for my heart prescriptions! If they can't reach me, it could literally be life-threatening!", -64.5),
        ("Agent", "Bear with me for a couple of minutes while I inspect your Openreach order migration asset records on the national porting portal.", None),
        ("Agent", "Thank you for waiting, Elisha. The migration order notes show that when the full-fibre switchover order was placed, the digital voice porting flag was left unticked by the automated sales form, causing the copper circuit to be marked as stopped rather than ported.", None),
        ("Agent", "I completely appreciate how precious that family number is to you after twenty-five years, Elisha, and how deeply worrying it is for your mother and hospital clinic. Let us get this investigated and recovered without delay.", None),
        ("Customer", "Thank you Hannah, hearing you say that gives me hope. Can you get that number back on my new fibre router?", 12.4),
        ("Agent", "Yes, because the number was ceased less than twenty-four hours ago, it sits in an Openreach quarantine reservation pool and has not been re-allocated.", None),
        ("Customer", "Thank goodness! How do we pull it back from the quarantine pool?", 18.2),
        ("Agent", "We need to submit an Emergency Orphaned Number Porting Recovery ticket directly to the national telecommunications routing desk.", None),
        ("Customer", "Can you submit that recovery ticket right now while I am on the phone?", 8.5),
        ("Agent", "Yes, I am populating the recovery request form right now. It requires the original CLI, which is 01923 774019, and the ONT optical serial number.", None),
        ("Customer", "The ONT box on the wall has a barcode sticker that says ONT-SN-998124.", 14.1),
        ("Agent", "ONT-SN-998124, entered. And we need to assign your voice service to Digital Voice Port 1 on the rear of your Hub 5 router.", None),
        ("Customer", "Yes, my analogue cordless phone base station is plugged directly into the green telephone port on the Hub 5 router right now.", 16.4),
        ("Agent", "Bear with me for two minutes while I submit the emergency porting file through the industry gateway.", None),
        ("Agent", "Thank you for waiting, Elisha. The emergency porting request has been successfully transmitted and accepted by the central routing desk with reference PRT-88192-K.", None),
        ("Customer", "That is wonderful! When will the number actually start ringing again in my house?", 22.1),
        ("Agent", "The central routing desk has an industry turnaround service level agreement of up to five business days to complete routing table propagation across all UK telecom networks.", None),
        ("Customer", "Five business days?! I cannot wait five days without my cardiology clinic or my vulnerable mother being able to reach me! That is completely unacceptable! I am breaking down with stress! What am I supposed to do if there is a medical emergency over the weekend?!", -58.4),
        ("Agent", "Five business days is the standard industry timeframe mandated by Openreach regulations for orphaned number re-allocation.", None),
        ("Customer", "You have to do something right now to connect incoming calls to my mobile phone while we wait for the five days!", -34.2),
        ("Agent", "Obviously legacy copper line routing is permanently decommissioned once full fibre optical service activates.", None),
        ("Customer", "Can you apply an automated network divert from 01923 774019 to my mobile phone 07700 900341?", -18.5),
        ("Agent", "Because the number is currently in quarantine status, automated network call diverts cannot be attached until the digital voice porting completes.", None),
        ("Customer", "So anyone who calls my landline gets a dead number tone for five days?", -22.4),
        ("Agent", "What I can do immediately is place a temporary automated recorded announcement on the number stating your mobile contact number.", None),
        ("Customer", "Can you really do that?! That would solve everything! My clinic and mother's carers will hear the mobile number!", 38.4),
        ("Agent", "Yes, I am configuring the network interception message on 01923 774019 right now to state: 'Please call 07700 900341 to reach Elisha Bennett.'", None),
        ("Customer", "Let me dial my landline from my neighbour's phone right now... Calling 01923 774019... It says: 'Please call 07700 900341 to reach Elisha Bennett'! It works perfectly!", 64.2),
        ("Agent", "The interception message will remain active until the full digital voice service ports to your Hub 5 router.", None),
        ("Customer", "That gives me immense peace of mind. The hospital clinic will hear the message and call my mobile.", 48.6),
        ("Agent", "I have also set an automated high-priority flag on ticket PRT-88192-K with our offline voice engineering queue.", None),
        ("Customer", "Thank you Hannah, you found a practical workaround that keeps me safe.", 34.2),
        ("Agent", "Before we close our call, that mobile telephone number for the divert notification was 07700 900341, correct?", None),
        ("Customer", "Yes, 07700 900341.", 18.2),
        ("Agent", "We have submitted the emergency porting recovery ticket, confirmed reference PRT-88192-K, and established the network interception announcement.", None),
        ("Customer", "I am so grateful for the interception message. Thank you Hannah.", 29.5),
        ("Agent", "We will send an automated SMS confirmation to your mobile as soon as the permanent port completes next week.", None),
        ("Customer", "I will look out for that text message.", 16.4),
        ("Agent", "Is there any other matter regarding your broadband or landline order I can assist with today, Elisha?", None),
        ("Customer", "No thank you Hannah, you have taken care of the most important thing.", 22.1),
        ("Agent", "Thank you for choosing S-Net order provisioning and technical services, Elisha. Take care and goodbye.", None),
        ("Customer", "Goodbye Hannah.", 18.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 62:
        raw.insert(-4, ("Agent", "Your full-fibre gigabit internet connection will continue operating with maximum throughput and stability throughout the porting window.", None))
        raw.insert(-4, ("Customer", "Yes, the broadband itself has been remarkably fast since the engineer left yesterday.", 24.1))
        raw.insert(-4, ("Agent", "Our automated network management systems will monitor the voice SIP registration continuously.", None))
        raw.insert(-4, ("Customer", "Thank you, that ensures total continuity for our household.", 18.5))

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
        "Empathy & Acknowledgment Statement": "While agent acknowledged the initial distress, she completely ignored the customer's severe emotional breakdown at [08:15] when faced with a 5-day medical isolation delay."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net order provisioning and technical services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Holds announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Elisha throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent handled the first outburst with empathy at [02:30], but completely ignored customer's distress and crying at [08:15] regarding 5-day medical emergency exposure, reciting only cold SLA regulations.",
        "Paraphrasing": "Agent restated the digital voice porting omission and cease status accurately at [01:40].",
        "Active listening": "Agent confirmed mobile contact number accurately without repeating questions.",
        "Took ownership of the problem": "Agent submitted emergency recovery ticket and established network interception announcement.",
        "Build rapport and observed professionalism": "Agent maintained a supportive and constructive tone.",
        "Probing": "Agent asked effective diagnostic questions regarding dialed tone, ONT serial number, and phone cabling.",
        "Confirmed the issue is resolved": "Customer dialed landline from neighbor phone and verified interception announcement broadcasted mobile number."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 37}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 7},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 25}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 5, "agent_turn": 8, "with_refusal": False},
            {"kind": "unhandled", "customer_turn": 22}
        ]
    }

    return {
        "cid": "agt_030",
        "cname": "Elisha",
        "target_dur": 1157,
        "scenario": "Landline number of 25 years accidentally terminated during full-fibre switchover",
        "tier": "good",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Classic training case featuring two distinct customer outbursts: the agent handled the first with late empathy (3 turns after), but failed to acknowledge the second severe outburst when quoting a 5-day SLA, resulting in an Empathy FAIL rating."
    }

print("get_call_030 defined.")

if __name__ == "__main__":
    for fn in [get_call_026, get_call_027, get_call_028, get_call_029, get_call_030]:
        c = fn()
        compile_call(c)
