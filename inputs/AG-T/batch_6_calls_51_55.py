import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from batch_engine import compile_call

# =========================================================================
# Call 051: Kasim, Double charge for pay-per-view boxing match, 11:35 (695s)
# 5+ faults (poor), score 50.0, Empathy PASS, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL, Confirmed resolved FAIL
# =========================================================================
def get_call_051():
    raw = [
        ("Agent", "Thank you for calling S-Net TV billing customer services, my name is Marcus. How can I help you today?", None),
        ("Customer", "Hello Marcus, my name is Kasim Thorne. I ordered the pay-per-view heavyweight boxing match on my TV box last Saturday for twenty-four pounds ninety-five, and when I checked my bank account statement this morning, S-Net has billed me twice for the exact same event!", -32.5),
        ("Agent", "Good morning Kasim. I can inspect your pay-per-view transaction ledger. Before we look at your purchase records, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 19 Gloucester Crescent, Leeds, LS1 4EQ, and my security PIN is 7731. My TV box device serial number is SNET-TV-99120.", -5.2),
        ("Agent", "Thank you Kasim, that confirms your account details. What specific transaction descriptions are showing on your statement?", None),
        ("Customer", "There are two identical charges of twenty-four pounds ninety-five, both timestamped at ten past ten on Saturday night for S-Net Box Office!", -22.1),
        ("Agent", "Bear with me for a couple of minutes while I check the pay-per-view purchase authorization logs on our media billing server.", None),
        ("Agent", "Thank you for waiting, Kasim. The media billing gateway records show two purchase authorization tokens generated twelve seconds apart from your TV box.", None),
        ("Customer", "I only pressed the purchase button once, Marcus! The screen froze for ten seconds displaying a spinning buffer icon, so I pressed select again! Taking fifty pounds for one boxing fight is completely unfair! I understand technical glitches happen, but please refund the duplicate twenty-four pounds ninety-five right now.", -14.2),
        ("Agent", "I understand that double charges cause immediate concern, Kasim. Let us examine the duplicate token.", None),
        ("Customer", "Can you reverse the duplicate charge from your computer screen immediately?", -12.4),
        ("Agent", "Well if you had actually waited for the electronic purchase confirmation instead of repeatedly hammering the remote control, you wouldn't have generated duplicate transactions.", None),
        ("Customer", "How dare you speak to me like that! The screen was frozen solid! Your television box malfunctioned!", -48.2),
        ("Agent", "Frontline telephony representatives do not have administrative permissions to reverse live pay-per-view transaction records.", None),
        ("Customer", "Then transfer me to your billing supervisor who can authorise the card refund!", -38.4),
        ("Agent", "Supervisors do not take inbound calls for digital content disputes. You must submit a written dispute ticket through the S-Net TV mobile app.", None),
        ("Customer", "I am on the phone with customer services right now! Take responsibility and fix your billing mistake!", -42.1),
        ("Agent", "Obviously electronic pay-per-view tokens are encrypted and reconciled by external sports broadcasting rights holders.", None),
        ("Customer", "S-Net charged my Visa card, not the boxing promoter! I want my twenty-four ninety-five back!", -34.5),
        ("Agent", "I can submit an offline billing review request to our digital content audit queue.", None),
        ("Customer", "What is the turnaround time for that audit review?", -18.2),
        ("Agent", "The digital content audit queue has a turnaround timescale of seven to ten business days.", None),
        ("Customer", "Ten business days to fix a duplicate charge that happened twelve seconds apart?! That is appalling!", -38.2),
        ("Agent", "What was that TV box device serial number again?", None),
        ("Customer", "As I told you right at the start of the call, it is SNET-TV-99120.", -16.2),
        ("Agent", "I have attached serial number SNET-TV-99120 to review ticket PPV-88192-K.", None),
        ("Customer", "PPV-88192-K, noted down. And you refuse to issue the refund today?", -18.4),
        ("Agent", "Discretionary refunds cannot be authorized until third-party rights reconciliation completes.", None),
        ("Customer", "This is utterly disgraceful customer care. I will be disputing the duplicate transaction with my bank.", -28.2),
        ("Agent", "You are entitled to raise a chargeback dispute through your card issuer.", None),
        ("Customer", "I certainly will. Goodbye.", -18.2),
        ("Agent", "Is there any other matter regarding your S-Net TV account I can assist you with today, Kasim?", None),
        ("Customer", "No, you have been unhelpful and rude.", -14.5),
        ("Agent", "Thank you for choosing S-Net TV billing customer services, Kasim. Goodbye.", None),
        ("Customer", "Goodbye Marcus.", -8.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our digital box office agreements comply with national broadcasting pay-per-view standards.", None))
        raw.insert(-4, ("Customer", "I expect S-Net to have automated duplicate transaction suppression.", -12.1))

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
        "Paraphrasing": "Failed to paraphrase customer's duplicate pay-per-view billing dispute in own words.",
        "Active listening": "Asked customer at [07:20] for his TV box serial number which had already been verified at [00:45].",
        "Took ownership of the problem": "Deflected responsibility at [04:40] by telling customer to use app forms or raise a bank chargeback rather than resolving refund directly.",
        "Build rapport and observed professionalism": "Spoke rudely and condescendingly at [03:40] stating 'Well if you had actually waited... instead of repeatedly hammering the remote control...'",
        "Confirmed the issue is resolved": "Failed to resolve duplicate charge, leaving £24.95 unresolved while customer stated intention to dispute with bank."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net TV billing customer services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Kasim throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent acknowledged double-charge concern at [02:40] ('I understand that double charges cause immediate concern, Kasim. Let us examine the duplicate token.') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent never restated the duplicate charge problem in his own words.",
        "Active listening": "Agent asked for TV box serial number at turn 23 despite customer providing SNET-TV-99120 at turn 3.",
        "Took ownership of the problem": "Agent repeatedly deflected ownership telling customer to use mobile app or file chargeback with his bank.",
        "Build rapport and observed professionalism": "Agent insulted customer at [03:40]: 'Well if you had actually waited... instead of repeatedly hammering the remote control, you wouldn't have generated duplicate transactions.'",
        "Probing": "Agent asked relevant questions regarding statement descriptions and purchase timestamps.",
        "Confirmed the issue is resolved": "Duplicate charge was not refunded, customer disconnected expressing intention to dispute through bank."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 23, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "rude", "agent_turn": 11},
            {"kind": "blunt_but_ok", "agent_turn": 17}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 8, "agent_turn": 9, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_051",
        "cname": "Kasim",
        "target_dur": 695,
        "scenario": "Double charge for pay-per-view boxing match on TV set-top box bill",
        "tier": "poor",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Build rapport and observed professionalism", "Confirmed the issue is resolved", "Took ownership of the problem"],
        "notes": "Poor customer service call marked by agent rudeness, victim-blaming, deflection of ownership, repeated questioning, and failure to resolve monetary dispute, while maintaining baseline empathy acknowledgment."
    }

print("get_call_051 defined.")


# =========================================================================
# Call 052: Keira, Mobile eSIM installation failing on S24, 13:42 (822s)
# 1-2 faults (good), score 90.0, Paraphrasing FAIL, All other 10 PASS
# =========================================================================
def get_call_052():
    raw = [
        ("Agent", "Thank you for calling S-Net mobile technical support, my name is Chloe. How can I help you today?", None),
        ("Customer", "Hello Chloe, my name is Keira Hughes. I received my new Samsung Galaxy S24 this morning, but when I scan the QR code to install my S-Net eSIM profile, the phone keeps throwing an error saying 'eSIM profile invalid or already redeemed'!", -32.4),
        ("Agent", "Good morning Keira. I can certainly assist you with generating a fresh eSIM profile and verifying your cellular attachment. Before we access your mobile subscription, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 83 Victoria Road, Swindon, SN1 3BD, and my security PIN is 4491. My mobile phone number is 07700 900518.", -5.2),
        ("Agent", "Thank you Keira, that confirms your account details. What happens when you tap 'Retry' on the Samsung SIM manager screen?", None),
        ("Customer", "It attempts to connect to the profile server for five seconds and then displays the exact same error: 'Profile invalid or already redeemed'.", -22.1),
        ("Agent", "Bear with me for a couple of minutes while I query your digital SIM reservation token on our GSMA subscription manager data center.", None),
        ("Agent", "Thank you for waiting, Keira. The GSMA subscription manager indicates that your initial eSIM activation token was invalidated during an automated factory test handshake prior to dispatch.", None),
        ("Customer", "I need to travel to our Birmingham office for client presentations this afternoon, and having zero mobile data or phone calls is giving me massive anxiety! I really hope we can get this eSIM connected before my train leaves!", -44.5),
        ("Agent", "I completely appreciate how stressful that is when preparing for important client travel, Keira. Let us get a fresh eSIM generated and downloaded onto your phone right now.", None),
        ("Customer", "Thank you Chloe, that is very reassuring. What do we need to do?", 14.2),
        ("Agent", "I am revoking the damaged activation token and generating a brand new digital eSIM profile on our SM-DP server.", None),
        ("Customer", "Does that produce a new QR code or a manual activation code?", 18.5),
        ("Agent", "I can provide the thirty-two-character SM-DP activation code directly over the phone so you can paste it without scanning a second screen.", None),
        ("Customer", "Entering the manual code directly into my Samsung would be much easier.", 24.1),
        ("Agent", "On your Samsung S24, open Settings, tap 'Connections', and tap 'SIM Manager'.", None),
        ("Customer", "Opened SIM Manager. I see 'Add eSIM'.", 18.2),
        ("Agent", "Tap 'Add eSIM', and then select 'Enter activation code' at the bottom of the screen.", None),
        ("Customer", "Tapped Enter activation code. A text box titled 'Activation code' is open.", 22.4),
        ("Agent", "The SM-DP server address is 'smdp.snet-mobile.co.uk', followed by a dollar sign, and matching code 'LPA:1$smdp.snet-mobile.co.uk$SNET-88219-X'.", None),
        ("Customer", "Typed in the activation code carefully... Tapping 'Add'...", 28.5),
        ("Agent", "The Samsung handset will now query the SM-DP server and download your encrypted profile keys.", None),
        ("Customer", "A progress bar says 'Downloading your S-Net eSIM profile... 80%... 100%! S-Net eSIM ready to use!'", 64.2),
        ("Agent", "Splendid! Now tap 'Turn on' to enable the new eSIM profile.", None),
        ("Customer", "Tapped Turn on... The 5G icon just lit up in the top right corner! And two bars of signal appeared!", 68.4),
        ("Agent", "Obviously eSIM profiles require an active Wi-Fi connection to download the initial cryptographic certificates.", None),
        ("Customer", "Yes, I am connected to our home broadband Wi-Fi right now.", 22.1),
        ("Agent", "Now let us turn off Wi-Fi for thirty seconds and test loading a web page over cellular data.", None),
        ("Customer", "Turned off Wi-Fi... Loading BBC News over 5G... It loaded instantly! And my WhatsApp messages are syncing!", 74.2),
        ("Agent", "Let us also make a test phone call to ensure voice authentication is fully provisioned on the network core.", None),
        ("Customer", "I am dialling our office reception number... It is ringing... Reception answered! The call quality is crystal clear!", 68.5),
        ("Agent", "That confirms voice, SMS, and high-speed 5G data are operating seamlessly on your Samsung S24.", None),
        ("Customer", "What a relief! I am completely set for my Birmingham client trip now.", 52.1),
        ("Agent", "I have locked your fresh eSIM profile to device IMEI 358901234567890.", None),
        ("Customer", "Thank you, that keeps the profile securely registered to this handset.", 34.2),
        ("Agent", "You can also view your active eSIM ICCID at any time in the My S-Net mobile app.", None),
        ("Customer", "I have the app installed and will check it once on the train.", 28.5),
        # Turn 38 is Harmless Recheck in last third! 38/58 = 0.655 ~ 0.66
        ("Agent", "Before we conclude our call, that mobile phone number was 07700 900518, correct?", None),
        ("Customer", "Yes, 07700 900518.", 18.2),
        ("Agent", "We have generated the fresh eSIM profile, downloaded the certificates, and verified 5G data and voice calling.", None),
        ("Customer", "Everything is working with complete perfection. Thank you Chloe.", 44.5),
        ("Agent", "Is there any other aspect of your mobile plan or new phone I can assist you with today, Keira?", None),
        ("Customer", "No thank you Chloe, you have been brilliant.", 32.1),
        ("Agent", "Thank you for choosing S-Net mobile technical support, Keira. Safe travels to Birmingham and have a great day. Goodbye.", None),
        ("Customer", "Goodbye Chloe.", 24.5),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our eSIM infrastructure supports rapid international data roaming profiles when travelling abroad.", None))
        raw.insert(-4, ("Customer", "That will make adding European travel data bundles very convenient in the future.", 26.4))

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "PASS",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "FAIL",
        "Active listening": "PASS",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "PASS"
    }

    coaching = {
        "Paraphrasing": "Failed to paraphrase customer's eSIM activation failure in own words, proceeding directly to explain technical token issues."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net mobile technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Keira warmly throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent handled travel anxiety with empathy at [02:50]: 'I completely appreciate how stressful that is when preparing for important client travel, Keira. Let us get a fresh eSIM generated and downloaded onto your phone right now.'",
        "Paraphrasing": "Agent never restated the eSIM invalid code error in her own words.",
        "Active listening": "Agent confirmed mobile number accurately without repeating questions.",
        "Took ownership of the problem": "Agent generated manual SM-DP code, walked customer through Samsung SIM Manager, and verified 5G voice and data.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, reassuring, and supportive tone throughout.",
        "Probing": "Agent asked relevant questions regarding SIM manager error messages and Wi-Fi status.",
        "Confirmed the issue is resolved": "Customer downloaded eSIM, turned off Wi-Fi, loaded web page over 5G, and completed test phone call."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 37}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 25}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 8, "agent_turn": 9, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_052",
        "cname": "Keira",
        "target_dur": 822,
        "scenario": "Mobile eSIM installation failing on new Samsung Galaxy S24 with QR invalid error",
        "tier": "good",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Excellent operational walk-through of manual SM-DP eSIM provisioning for a customer with urgent travel needs, achieving 10 passing criteria while cleanly omitting a paraphrasing restatement."
    }

print("get_call_052 defined.")


# =========================================================================
# Call 053: Kieran, Synology NAS DDNS blocked behind CGNAT, 16:08 (968s)
# excellent, score 100.0, All PASS, Empathy with_refusal: True
# =========================================================================
def get_call_053():
    raw = [
        ("Agent", "Thank you for calling S-Net network infrastructure technical operations, my name is Toby. How can I help you today?", None),
        ("Customer", "Hello Toby, my name is Kieran Walsh. I run a Synology NAS storage server for my architectural firm, but ever since my broadband upgraded to your Fibre 500 package, external DDNS remote access has completely stopped working because my WAN IP is trapped behind Carrier-Grade NAT!", -32.4),
        ("Agent", "Good afternoon Kieran. I can inspect your broadband WAN routing and public IP allocation parameters. Before we access your gateway telemetry, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 58 Park Avenue, Manchester, M14 5JH, and my security PIN is 8841. My router model is the Hub 5 with WAN IP starting with one hundred dot sixty-four.", -5.2),
        ("Agent", "Thank you Kieran, that confirms your account details. What specific error is reported by the Synology DDNS service?", None),
        ("Customer", "The Synology DiskStation manager displays 'External IP 100.64.182.49 does not match public DNS resolution. Port forwarding unreachable.'", -22.1),
        ("Agent", "So what has occurred is that following your optical line upgrade, your Hub 5 was provisioned with a shared RFC 6598 Carrier-Grade NAT address in the 100.64 block, preventing inbound port forwarding to your local Synology NAS server, is that right?", None),
        ("Customer", "Yes, that is exactly what happened! I have three freelance draughtsmen working remotely across the UK who cannot access our thirty-gigabyte CAD blueprints! We have planning permission submissions due by midnight, and our external workflow is completely crippled! I demand that S-Net assign a dedicated permanent static IPv4 address to my connection right now at zero charge!", -64.2),
        ("Agent", "Bear with me for a couple of minutes while I check our regional CGNAT gateway pools and subscriber IP assignment profiles in the Manchester aggregation core.", None),
        ("Agent", "Thank you for waiting, Kieran. The Manchester broadband network gateway confirms your dynamic session is routed through a CGNAT carrier translation pool.", None),
        ("Agent", "I completely understand how critical and urgent it is to maintain seamless remote file access for your architectural draughtsmen when major planning deadlines are pending tonight, Kieran. However, because our residential broadband service tier utilizes CGNAT pooling to conserve global IPv4 space, our service terms do not permit issuing permanent static IP addresses on standard consumer subscriptions; what I can do right now is assign an immediate CGNAT opt-out profile to your account, giving your Hub 5 a dedicated public dynamic IPv4 address from our unrestricted pool, and enable automated UPnP port mapping.", None),
        ("Customer", "A dedicated public dynamic IPv4 address will work completely fine with my Synology DDNS! As long as inbound port forwarding is unrestricted, DDNS will update automatically!", 22.4),
        ("Agent", "I am applying the CGNAT Opt-Out Public IP profile to your broadband circuit on our RADIUS provisioning server right now.", None),
        ("Customer", "How do we bind the new public IP to my Hub 5 router?", 16.4),
        ("Agent", "I will send a remote port bounce command to re-negotiate your PPPoE WAN session.", None),
        ("Customer", "The router internet light just turned amber for a moment...", 12.1),
        ("Agent", "The WAN interface is requesting a fresh IP lease from our public carrier pool.", None),
        ("Customer", "The light is back to solid white! Let me check the Hub 5 WAN status page... It has been assigned IP address 82.132.214.88! That is a genuine public IP address!", 68.4),
        ("Agent", "82.132.214.88 is a fully routable public IPv4 address with completely unrestricted inbound port forwarding.", None),
        ("Customer", "Let me check the Synology DiskStation DDNS status page right now... Clicking 'Update Now'...", 48.2),
        ("Agent", "The Synology client should query public DNS and bind port five thousand and one.", None),
        ("Customer", "The Synology screen says 'Status: Normal'! External IP matched successfully! Let me test remote access from my mobile phone on 5G...", 64.2),
        ("Agent", "Obviously Carrier-Grade NAT is implemented across residential access networks in accordance with Ofcom IPv4 exhaustion guidelines.", None),
        ("Customer", "I am connecting via 5G... Tapped our firm's DDNS URL... Toby! The DiskStation web portal opened immediately! I am logging into our CAD projects folder!", 78.4),
        ("Agent", "That confirms inbound port 5001 and secure SSL traffic are routing directly through to your NAS.", None),
        ("Customer", "What a massive relief! My draughtsmen can resume downloading the blueprints immediately. The midnight deadline is saved.", 58.2),
        ("Agent", "Your Hub 5 will permanently retain this public dynamic IP allocation across all future router reboots.", None),
        ("Customer", "That will keep our DDNS service working permanently without unexpected reverts.", 38.4),
        ("Agent", "We also recommend setting your Synology router port forwarding rules to enforce HTTPS encryption.", None),
        ("Customer", "All our remote connections are forced over secure TLS 1.3.", 32.1),
        ("Agent", "I have locked the CGNAT opt-out flag on engineering ticket NET-44019-V.", None),
        ("Customer", "NET-44019-V, noted down.", 24.5),
        ("Agent", "Our Manchester gateway platform will maintain your public IP pool allocation permanently.", None),
        ("Customer", "Thank you Toby, you understood the technical networking problem immediately.", 42.1),
        # Turn 36 is Harmless Recheck in last third! 36/58 = 0.621 ~ 0.66
        ("Agent", "Before we conclude our call, that account contact telephone number was 0161 248 8841, correct?", None),
        ("Customer", "Yes, 0161 248 8841 is my office landline.", 18.2),
        ("Agent", "We have removed CGNAT carrier translation, provisioned public IP 82.132.214.88, verified Synology DDNS resolution, and confirmed remote CAD access.", None),
        ("Customer", "Everything is working with complete perfection. Thank you Toby.", 48.2),
        ("Agent", "Is there any other aspect of your broadband WAN routing I can assist you with today, Kieran?", None),
        ("Customer", "No thank you Toby, you have resolved my issue completely.", 34.2),
        ("Agent", "Thank you for choosing S-Net network infrastructure technical operations, Kieran. Good luck with your planning submission tonight and have a great day. Goodbye.", None),
        ("Customer", "Goodbye Toby.", 24.5),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our Manchester aggregation core maintains dual-homed optical transits for enterprise reliability.", None))
        raw.insert(-4, ("Customer", "That core transit reliability is vital for our architectural studio data transfers.", 28.2))

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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net network infrastructure technical operations' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Kieran warmly throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated acknowledgment-then-refusal at [03:15] ('I completely understand how critical and urgent it is... However, because our residential broadband service tier utilizes CGNAT pooling to conserve global IPv4 space, our service terms do not permit issuing permanent static IP addresses on standard consumer subscriptions; what I can do right now is assign an immediate CGNAT opt-out profile...').",
        "Paraphrasing": "Agent restated the 100.64 CGNAT block and Synology port forwarding failure accurately at [01:25].",
        "Active listening": "Agent confirmed office landline number accurately without repeating questions.",
        "Took ownership of the problem": "Agent assigned CGNAT opt-out profile, bounced WAN port to assign public IP 82.132.214.88, and verified DDNS access.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, highly competent, and encouraging tone throughout.",
        "Probing": "Agent asked relevant questions regarding DiskStation error logs and external IP reporting.",
        "Confirmed the issue is resolved": "Customer confirmed public IP assigned, DDNS status returned to Normal, and accessed DiskStation portal over 5G."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 36}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 6},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 22}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 7, "agent_turn": 10, "with_refusal": True}
        ]
    }

    return {
        "cid": "agt_053",
        "cname": "Kieran",
        "target_dur": 968,
        "scenario": "Synology NAS external DDNS remote access blocked behind CGNAT carrier IP",
        "tier": "excellent",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Outstanding technical performance featuring acknowledgment-then-refusal where the agent validated deadline urgency, firmly explained why residential tiers cannot provide free permanent static IPs, and delivered a perfect CGNAT opt-out public IP solution."
    }

print("get_call_053 defined.")


# =========================================================================
# Call 054: Lara, Broadband speed halved after lightning strike, 14:16 (856s)
# 3-4 faults (okay), score 60.0, Empathy PASS, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL
# =========================================================================
def get_call_054():
    raw = [
        ("Agent", "Thank you for calling S-Net broadband network faults, my name is Ryan. How can I help you today?", None),
        ("Customer", "Hello Ryan, my name is Lara Croft. Ever since the intense electrical thunderstorm yesterday evening, my broadband download speed has plummeted from seventy megabits down to twenty-eight megabits, and the connection drops every time the wind blows!", -32.5),
        ("Agent", "Good afternoon Lara. I can test your copper loop electrical parameters and DSLAM line card telemetry. Before we initiate the diagnostic tests, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 41 St Anne's Well Road, Nottingham, NG3 3EW, and my security PIN is 5502. My Hub router model is the Hub 4 with serial number SN-88210.", -5.2),
        ("Agent", "Thank you Lara, that confirms your account details. Have you noticed any physical damage or scorching around your master telephone socket?", None),
        ("Customer", "No physical scorching, but the broadband synchronization light on the Hub router keeps cycling between amber and white.", -22.1),
        ("Agent", "Bear with me for a couple of minutes while I query the local Openreach street cabinet telemetry and line retrain logs.", None),
        ("Agent", "Thank you for waiting, Lara. The street cabinet test head confirms that cabinet 14 suffered a direct lightning surge yesterday, tripping line cards into emergency high-attenuation protective profiles.", None),
        ("Customer", "I understand electrical storms happen, Ryan, but I run an online accounting business from home and my quarterly tax client deadlines are this Friday! Twenty-eight megabits with continuous drops makes running client accounting portals impossible! Please tell me when an engineer will repair the cabinet card!", -18.2),
        ("Agent", "I completely understand that speed drops during busy tax accounting periods cause immediate stress, Lara. Let us see what repair schedule Openreach has established.", None),
        ("Customer", "When will the cabinet engineer arrive to restore full seventy-megabit speeds?", -12.4),
        ("Agent", "Well if you had actually installed a surge protector plug on your modem power supply, your router wouldn't be retraining every fifteen minutes.", None),
        ("Customer", "How dare you blame my power plug, Ryan! You just told me the Openreach cabinet in the street was struck by lightning! My internal power has zero surge damage!", -52.4),
        ("Agent", "Frontline technical agents do not oversee wholesale external cabinet civil repairs.", None),
        ("Customer", "Then transfer me to your network operations manager who can escalate the street cabinet repair!", -38.4),
        ("Agent", "Network operations supervisors do not take customer phone calls. You need to wait for the wholesale engineering teams to clear the storm queue.", None),
        ("Customer", "You refuse to escalate the repair and you blame my surge protector! This is appalling service!", -46.2),
        ("Agent", "Obviously electrical surge transients travel across underground copper pairs regardless of subscriber equipment.", None),
        ("Customer", "Then what can S-Net actually do to support my home business connection today?", -28.4),
        ("Agent", "I can submit an automated profile reset to attempt clearing the protective line card profile.", None),
        ("Customer", "Go ahead and try the reset.", -14.2),
        ("Agent", "Bear with me for two minutes while I push the profile reset command to cabinet 14.", None),
        ("Agent", "Thank you for waiting, Lara. The DSLAM port has been reset, but sync speed remains locked at thirty-two megabits due to upstream copper pair capacitance imbalance.", None),
        ("Customer", "So speeds remain halved and unstable until an engineer visits the cabinet?", -22.1),
        ("Agent", "The estimated resolution timeframe for the storm backlog is three to five business days.", None),
        ("Agent", "What was that Hub router serial number again?", None),
        ("Customer", "As I told you during verification, it is SN-88210.", -16.2),
        ("Agent", "I have attached serial number SN-88210 to monitoring ticket TKT-44019-L.", None),
        ("Customer", "TKT-44019-L, noted down. And you cannot dispatch an engineer any faster?", -18.4),
        ("Agent", "Cabinet lightning repairs are handled strictly according to regional Openreach queue priorities.", None),
        ("Customer", "I will have to tether my laptop to my mobile phone to finish my accounting work.", -12.1),
        ("Agent", "I have documented your business usage on the fault record.", None),
        ("Customer", "Very well. I will monitor the line over the coming days.", -8.2),
        ("Agent", "Is there any other aspect of your broadband connection I can assist you with today, Lara?", None),
        ("Customer", "No, you have been unhelpful and rude.", -14.5),
        ("Agent", "Thank you for choosing S-Net broadband network faults, Lara. Goodbye.", None),
        ("Customer", "Goodbye Ryan.", -8.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our automated fault tracking system will poll sync speeds every morning at six o'clock.", None))
        raw.insert(-4, ("Customer", "I will check the router connection lights each morning.", 8.4))

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
        "Paraphrasing": "Failed to paraphrase customer's storm-related speed drop and sync instability in own words.",
        "Active listening": "Asked customer at [08:15] for her router serial number which had already been verified at [00:45].",
        "Took ownership of the problem": "Deflected responsibility at [04:45] by refusing to escalate ticket and telling customer frontline staff cannot assist with wholesale repairs.",
        "Build rapport and observed professionalism": "Spoke rudely and defensively at [03:45] stating 'Well if you had actually installed a surge protector plug... your router wouldn't be retraining...'"
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net broadband network faults' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Holds announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Lara throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated empathy at [02:50] ('I completely understand that speed drops during busy tax accounting periods cause immediate stress, Lara.') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent never restated the thunderstorm damage and halved speed in his own words.",
        "Active listening": "Agent asked for router serial number at turn 25 despite customer stating SN-88210 at turn 3.",
        "Took ownership of the problem": "Agent refused to escalate ticket to management, deflecting responsibility to wholesale queues.",
        "Build rapport and observed professionalism": "Agent insulted customer at [03:45]: 'Well if you had actually installed a surge protector plug... your router wouldn't be retraining every fifteen minutes.'",
        "Probing": "Agent asked relevant questions regarding physical damage and router sync light status.",
        "Confirmed the issue is resolved": "Customer noted monitoring ticket TKT-44019-L and agreed to 3-5 day engineering timeframe."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 25, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "rude", "agent_turn": 11},
            {"kind": "blunt_but_ok", "agent_turn": 17}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 8, "agent_turn": 9, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_054",
        "cname": "Lara",
        "target_dur": 856,
        "scenario": "Broadband sync speed dropped by half following Openreach cabinet lightning strike",
        "tier": "okay",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Build rapport and observed professionalism", "Took ownership of the problem"],
        "notes": "Good demonstration of an 'okay' 4-fault call where the agent demonstrated appropriate empathy regarding tax accounting deadlines, but failed paraphrasing, active listening, rapport, and ownership."
    }

print("get_call_054 defined.")


# =========================================================================
# Call 055: Leila, £65 non-return equipment charge for returned router, 18:52 (1132s)
# 1-2 faults (good), score 90.0, Paraphrasing FAIL, All other 10 PASS
# =========================================================================
def get_call_055():
    raw = [
        ("Agent", "Thank you for calling S-Net billing customer services, my name is Gemma. How can I help you today?", None),
        ("Customer", "Hello Gemma, my name is Leila Rossi. I cancelled my broadband contract two months ago and returned my Hub router in your pre-paid tracked bag, but my final invoice has billed me sixty-five pounds for a non-returned equipment fee!", -32.5),
        ("Agent", "Good afternoon Leila. I can inspect your equipment return records and billing ledger. Before we access your closed account, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 12 Lansdowne Road, Cardiff, CF5 1PS, and my security PIN is 9184. My return Royal Mail tracking number was RM-440192-GB.", -5.2),
        ("Agent", "Thank you Leila, that confirms your account details. When was the router scanned as delivered by Royal Mail?", None),
        ("Customer", "Royal Mail tracking confirms it was delivered and signed for at your Northampton returns warehouse on October 12th at nine in the morning.", -22.1),
        ("Agent", "Bear with me for a couple of minutes while I query our warehouse barcode scan database and returns intake ledger.", None),
        ("Agent", "Thank you for waiting, Leila. I have located warehouse intake scan RM-440192-GB. The Hub 4 router was received on October 12th, but the warehouse barcode scanner registered an incomplete asset clearance flag.", None),
        ("Customer", "I was so worried when I saw that sixty-five pound direct debit charge, Gemma! I am a university student on a tight maintenance budget, and an unexpected sixty-five pound deduction causes major financial stress! I really appreciate you locating the package so quickly.", 14.2),
        ("Agent", "I completely understand that unexpected equipment fees cause genuine financial anxiety, Leila, especially when you returned the hardware responsibly. Let us make sure this charge is cancelled and refunded immediately.", None),
        ("Customer", "Thank you so much Gemma, that is a huge relief to hear.", 28.5),
        ("Agent", "I am submitting an immediate fee waiver command to clear the sixty-five pound non-return equipment charge.", None),
        ("Customer", "Has the direct debit already pulled the sixty-five pounds from my Santander account?", -12.4),
        ("Agent", "The direct debit collection mandate was cancelled yesterday, so no funds left your bank account.", None),
        ("Customer", "So my bank account was never debited?", 24.1),
        ("Agent", "That is correct. The sixty-five pound charge existed on the generated invoice, but the payment collection was successfully arrested.", None),
        ("Customer", "That is fantastic news, so I do not have to wait for a refund to clear.", 38.2),
        ("Agent", "I have updated your ledger balance to zero pounds.", None),
        ("Customer", "Will you send me an updated zero-balance statement for my records?", 18.5),
        ("Agent", "Yes, I am generating an updated PDF statement showing zero balance and dispatching it to your email address right now.", None),
        ("Customer", "Let me check my email on my phone... Yes, 'S-Net Final Statement - Balance Due: £0.00' just arrived!", 68.4),
        ("Agent", "Obviously warehouse returns scanning systems reconcile thousands of customer parcels daily and occasional barcode misreads occur.", None),
        ("Customer", "I understand that, as long as it has been cleared up promptly today.", 24.1),
        ("Agent", "Your equipment return record is officially marked 'Returned - Complete' in our national asset database.", None),
        ("Customer", "That gives me confidence that no future collection letters will be sent.", 32.1),
        ("Agent", "The fee waiver reference code for your personal records is EQ-88192-W.", None),
        ("Customer", "EQ-88192-W, noted down.", 22.4),
        ("Agent", "Your closed account profile will transition to permanent archived status within thirty days.", None),
        ("Customer", "That is completely fine since I no longer live at that student address.", 28.5),
        ("Agent", "All marketing permissions and direct debit mandates have been formally purged from our clearing registers.", None),
        ("Customer", "Thank you, that ensures total closure of this account.", 34.2),
        ("Agent", "Our billing care department is open seven days a week if you ever need any historical tax invoices.", None),
        ("Customer", "Good to know.", 18.2),
        # Turn 34 is Harmless Recheck in last third! 34/58 = 0.586
        ("Agent", "Our warehouse returns protocol complies with WEEE environmental recycling standards.", None),
        ("Customer", "I am glad the returned equipment will be recycled responsibly.", 24.1),
        ("Agent", "Before we conclude our call, that account contact telephone number was 029 2038 9184, correct?", None),
        ("Customer", "Yes, 029 2038 9184 was my student flat landline.", 18.2),
        ("Agent", "We have waived the sixty-five pound equipment charge, arrested the direct debit sweep, updated your balance to zero, and dispatched your final zero-balance statement.", None),
        ("Customer", "Everything has been resolved with complete perfection. Thank you Gemma.", 48.2),
        ("Agent", "Is there any other aspect of your closed account I can assist you with today, Leila?", None),
        ("Customer", "No thank you Gemma, you have been wonderful.", 32.1),
        ("Agent", "Thank you for choosing S-Net billing customer services, Leila. Good luck with your university studies and have a lovely day. Goodbye.", None),
        ("Customer", "Goodbye Gemma.", 24.5),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Our automated direct debit suppression ensures no residual payment collection sweeps execute.", None))
        raw.insert(-4, ("Customer", "That provides total reassurance for my student banking records.", 26.4))

    ratings = {
        "Branding and Survey Check": "PASS",
        "Hold time and Dead Air": "PASS",
        "Verified customer": "PASS",
        "Personalized the call/ticket appropriately": "PASS",
        "Empathy & Acknowledgment Statement": "PASS",
        "Paraphrasing": "FAIL",
        "Active listening": "PASS",
        "Took ownership of the problem": "PASS",
        "Build rapport and observed professionalism": "PASS",
        "Probing": "PASS",
        "Confirmed the issue is resolved": "PASS"
    }

    coaching = {
        "Paraphrasing": "Failed to paraphrase customer's equipment return dispute in own words, proceeding directly to warehouse barcode lookups."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net billing customer services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Leila warmly throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent demonstrated warm empathy at [02:50] ('I completely understand that unexpected equipment fees cause genuine financial anxiety, Leila... Let us make sure this charge is cancelled and refunded immediately.') and customer had no unhandled outbursts.",
        "Paraphrasing": "Agent never restated the £65 equipment return fee dispute in her own words.",
        "Active listening": "Agent confirmed student landline number accurately without repeating questions.",
        "Took ownership of the problem": "Agent cleared £65 fee, verified Bacs direct debit was arrested, and emailed updated zero-balance PDF.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, warm, and congratulatory tone throughout.",
        "Probing": "Agent asked relevant questions regarding delivery tracking and return dates.",
        "Confirmed the issue is resolved": "Customer confirmed receipt of zero-balance PDF statement and verified direct debit sweep halted."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 35}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 21}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 8, "agent_turn": 9, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_055",
        "cname": "Leila",
        "target_dur": 1132,
        "scenario": "Billing dispute regarding £65 non-return equipment charge for returned router",
        "tier": "good",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Exemplary billing dispute handling where the agent demonstrated outstanding empathy, verified warehouse receipt, cleared £65 fee, and emailed zero-balance statement, achieving 10 passing criteria while cleanly omitting a paraphrasing restatement."
    }

print("get_call_055 defined.")

if __name__ == "__main__":
    for fn in [get_call_051, get_call_052, get_call_053, get_call_054, get_call_055]:
        c = fn()
        compile_call(c)
