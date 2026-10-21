import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("inputs/AG-T"))
from batch_engine import compile_call

# =========================================================================
# Call 031: Faisal, mDNS client isolation on Hub Pro, 10:25 (625s)
# 3-4 faults (okay), score 71.7, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL
# =========================================================================
def get_call_031():
    raw = [
        ("Agent", "Thank you for calling S-Net technical support, my name is Liam. How can I help you today?", None),
        ("Customer", "Hello Liam, my name is Faisal Qureshi. I upgraded to your Hub Pro router yesterday, and now none of our laptops or iPhones can discover our HP wireless printer on the home Wi-Fi network!", -31.2),
        ("Agent", "Good morning Faisal. I can inspect your Hub Pro local network configuration and subnet routing. Before we check your settings, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 47 Richmond Road, Sheffield, S13 8TB, and my security PIN is 2981. My printer IP address is 192.168.1.150.", -6.5),
        ("Agent", "Thank you Faisal, that confirms your account details. What happens when you try to print a test document from one of your laptops?", None),
        ("Customer", "The print queue says 'Printer Offline' or 'Printer Not Found', even though the blue Wi-Fi light on the HP printer is glowing solid blue.", -22.4),
        ("Agent", "Is the printer connected to the main 2.4 gigahertz Wi-Fi network or the separate Guest network?", None),
        ("Customer", "It is connected to the primary Wi-Fi network, the exact same SSID that our laptops and phones are connected to.", -14.2),
        ("Agent", "Bear with me for a couple of minutes while I query your Hub Pro gateway configuration tables on our provisioning server.", None),
        ("Agent", "Thank you for waiting, Faisal. I have pulled up your Hub Pro profile. The wireless local area network settings have Client Isolation enabled by default.", None),
        ("Customer", "My wife and I run an architectural consultancy from home, and we have tender documents that must be printed and signed by courier in forty minutes! We are completely stuck and panicking! Why would your router ship with settings that break basic printing?!", -56.8),
        ("Agent", "Client isolation is a baseline security protocol designed to prevent infected smart home devices from executing lateral network reconnaissance across consumer subnets.", None),
        ("Customer", "I do not need a cybersecurity lecture, Liam! I need my HP printer to show up on my laptop so I can print our contract before the courier arrives!", -48.2),
        ("Agent", "To enable peer-to-peer discovery across connected wireless clients, client isolation must be deactivated within the advanced gateway GUI.", None),
        ("Customer", "Can you turn it off remotely from your screen right now?", -18.5),
        ("Agent", "Frontline technical support agents cannot alter private LAN subnet isolation flags remotely for customer privacy reasons.", None),
        ("Customer", "Then tell me exactly how to log into the Hub Pro and change the setting myself.", -12.4),
        ("Agent", "Obviously local subnet isolation prevents broadcast packets like mDNS and Bonjour from crossing wireless access point interfaces.", None),
        ("Customer", "I understand that, please just give me the IP address and admin login.", -16.2),
        ("Agent", "Open an internet browser tab on your laptop and type 192.168.1.254 into the address bar.", None),
        ("Customer", "Typed 192.168.1.254. A page titled 'S-Net Hub Pro Manager' has loaded asking for the admin password.", 8.5),
        ("Agent", "Look at the removable plastic settings card slotted into the back of the Hub Pro router to find the admin password.", None),
        ("Customer", "Got the card... Admin password is 'Echo-992-Delta'. Typing it in now and clicking Login.", 14.2),
        ("Agent", "Once logged in, click on the 'Advanced Settings' tab along the top navigation bar.", None),
        ("Customer", "Clicked Advanced Settings. It shows Wireless, Firewall, DHCP, and System.", 18.4),
        ("Agent", "Click on 'Wireless', and then select 'WLAN Configuration' from the sub-menu.", None),
        ("Customer", "Selected WLAN Configuration. I see SSIDs and advanced toggles. Liam, I am having a complete panic attack right now! The courier van just pulled up outside! If this printer doesn't spit out the tender pages in three minutes, we lose a forty-thousand-pound contract!", -62.4),
        ("Agent", "Locate the toggle switch labeled 'AP Client Isolation' or 'Station Isolation'.", None),
        ("Customer", "Found it! 'AP Client Isolation' is currently toggled to ON in green.", 16.5),
        ("Agent", "Click that toggle to switch it to OFF, and then click 'Save Changes' at the bottom of the page.", None),
        ("Customer", "Toggled to OFF and clicked Save Changes... The router page says 'Settings saved successfully.'", 32.4),
        ("Agent", "What was that printer IP address again?", None),
        ("Customer", "As I said earlier, it is 192.168.1.150.", -14.2),
        ("Agent", "Now open your printer queue on your laptop and try printing your document again.", None),
        ("Customer", "Opening print queue... It says 'HP LaserJet Ready'! Clicking Print... Yes! I can hear the printer warming up and spitting out the pages right now!", 62.4),
        ("Agent", "And let us check an iPhone to verify that Apple AirPrint discovery is functioning across the wireless network as well.", None),
        ("Customer", "Testing on my iPhone... Opened a PDF, tapped Share, tapped Print... Yes! The HP printer appeared instantly under AirPrint! Printing page two now!", 68.5),
        ("Agent", "That confirms mDNS and multicast Bonjour traffic are broadcasting freely between all your household devices.", None),
        ("Customer", "What a relief! The tender contract is printed, signed, and ready for the courier. Thank you Liam.", 44.2),
        ("Agent", "If you ever factory reset the Hub Pro in the future, remember that AP Client Isolation will default back to ON.", None),
        ("Customer", "I have written a note on the admin card: remember to disable AP Client Isolation.", 24.5),
        ("Agent", "We have accessed your Hub Pro manager, deactivated AP Client Isolation, and confirmed both Windows and AirPrint discovery work normally.", None),
        ("Customer", "Everything is working perfectly. You have saved my working day.", 36.8),
        ("Agent", "Is there any other aspect of your Hub Pro wireless network I can help you with today, Faisal?", None),
        ("Customer", "No, that was the only problem. Thank you for your assistance.", 28.2),
        ("Agent", "Thank you for choosing S-Net technical support, Faisal. Have a great day and good luck with the tender. Goodbye.", None),
        ("Customer", "Goodbye Liam.", 22.1),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Your Hub Pro router will automatically optimize wireless channel selection during quiet hours overnight.", None))
        raw.insert(-4, ("Customer", "That will keep our Wi-Fi interference low from neighboring flats.", 14.5))
        raw.insert(-4, ("Agent", "The dual-band antennas provide high throughput across both 2.4 and 5 gigahertz spectra.", None))
        raw.insert(-4, ("Customer", "The wireless speeds have been excellent across all our rooms.", 18.2))

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
        "Empathy & Acknowledgment Statement": "Failed to acknowledge customer panic at [02:40] when facing critical business contract printing deadlines.",
        "Paraphrasing": "Offered no paraphrasing of the wireless printer discovery issue in own words.",
        "Active listening": "Asked customer at [07:20] for his printer IP address which had already been supplied at [00:45]."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net technical support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Faisal throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute stress over an impending courier deadline; agent completely ignored feelings and defended network security policy.",
        "Paraphrasing": "Agent never restated the customer's printing discovery failure in his own words.",
        "Active listening": "Agent asked for printer IP address at turn 31 despite customer providing it at turn 3.",
        "Took ownership of the problem": "Agent guided customer through router GUI to disable AP Client Isolation.",
        "Build rapport and observed professionalism": "Agent maintained a professional instructional tone throughout.",
        "Probing": "Agent asked diagnostic questions regarding print queues, SSIDs, and device visibility.",
        "Confirmed the issue is resolved": "Customer confirmed HP LaserJet printed contract pages and verified AirPrint on iPhone."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 31, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 17}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 10},
            {"kind": "unhandled", "customer_turn": 20}
        ]
    }

    return {
        "cid": "agt_031",
        "cname": "Faisal",
        "target_dur": 625,
        "scenario": "mDNS client isolation on Hub Pro preventing wireless printer discovery across VLANs",
        "tier": "okay",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Paraphrasing"],
        "notes": "Good technical walk-through of AP Client Isolation on Hub Pro, but agent failed empathy on impending business deadline, offered no paraphrase, and repeated a question about printer IP address."
    }

print("get_call_031 defined.")


# =========================================================================
# Call 032: Fatima, Exemption request for paper billing fee, 13:12 (792s)
# 1-2 faults (good), score 88.3, Empathy FAIL
# =========================================================================
def get_call_032():
    raw = [
        ("Agent", "Thank you for calling S-Net billing customer services, my name is Chloe. How can I help you today?", None),
        ("Customer", "Hello Chloe, my name is Fatima Begum. I am calling because my latest monthly broadband bill has an extra three pounds fifty charge for paper billing, but I am registered partially sighted and cannot read digital bills on a smartphone screen!", -34.5),
        ("Agent", "Good morning Fatima. I can review your billing fees and account accessibility flags. Before we access your billing records, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 19 Wellington Street, Leeds, LS1 4EQ, and my security PIN is 7731. My customer account number is SN-551029.", -6.2),
        ("Agent", "Thank you Fatima, that confirms your account details. When did you first notice the paper invoice charge on your monthly bill?", None),
        ("Customer", "I opened my large print paper bill yesterday morning, and right below my broadband charge it says 'Paper Invoice Administration Charge: £3.50'.", -22.1),
        ("Agent", "So what has occurred is that a three pound fifty paper invoice administration fee was applied to your monthly statement, and you are requesting an accessibility fee waiver and refund because you require printed large-print correspondence due to visual impairment, is that right?", None),
        ("Customer", "Yes, that is exactly right! I was promised when I signed up three years ago that large-print paper bills would always be free for disabled customers!", -16.8),
        ("Agent", "Bear with me for a couple of minutes while I inspect your billing profile and accessibility concession registers on our database.", None),
        ("Agent", "Thank you for waiting, Fatima. Our billing platform underwent an automated tariff upgrade last month, and accounts without a refreshed Equality Concession Flag had the standard paper fee automatically applied.", None),
        ("Customer", "It makes me so angry and humiliated to be penalised financially just because I cannot see well enough to use an online app! Three pounds fifty might not seem like much to S-Net, but for an elderly pensioner on a fixed disability pension, every pound matters! It is so distressing!", -56.4),
        ("Agent", "The fee was applied uniformly across all legacy paper-billing subscribers by our automated financial batch run.", None),
        ("Customer", "Can you refund that three pounds fifty immediately and make sure S-Net never charges it to me again?", -28.2),
        ("Agent", "Yes, I am opening our accessibility concessions management module right now.", None),
        ("Customer", "What details do you need to add to my account so the computer stops adding the fee?", -12.4),
        ("Agent", "I am applying the formal RNIB Accessibility Exemption flag to your billing account.", None),
        ("Customer", "Does that cover large print format permanently?", 12.1),
        ("Agent", "Yes, it attaches a permanent zero-cost waiver to all physical correspondence and locks your invoice template to eighteen-point large print format.", None),
        ("Customer", "Eighteen-point font is so much easier for me to read with my magnifying glass.", 24.5),
        ("Agent", "Obviously automated billing systems execute standard charges unless an active concession code is populated in the master ledger.", None),
        ("Customer", "I understand that, as long as the exemption code is permanently attached now. Chloe, it has been deeply distressing and humiliating having to fight for basic accessibility as a blind pensioner! Managing alone on a disability pension is already terrifying without S-Net penalising me!", -58.4),
        ("Agent", "I have submitted a credit adjustment of three pounds fifty directly onto your current ledger balance.", None),
        ("Customer", "Will that reduce my next direct debit payment automatically?", 14.5),
        ("Agent", "Yes, your next monthly collection will be discounted by three pounds fifty, reducing it to twenty-six pounds fifty instead of thirty pounds.", None),
        ("Customer", "That is wonderful, thank you Chloe.", 28.4),
        ("Agent", "I have also set a high-contrast text flag on your customer file so any written notices or letters arrive in eighteen-point high-contrast typeface.", None),
        ("Customer", "That will make such a massive difference to my daily independence.", 34.2),
        ("Agent", "You can also request audio CD format or braille statements in the future if your visual needs ever change, Fatima.", None),
        ("Customer", "Large print is perfect for now, but it is comforting to know audio format is available.", 22.1),
        ("Agent", "Before we conclude our call, that account contact telephone number was 0113 496 0882, correct?", None),
        ("Customer", "Yes, 0113 496 0882 is my landline.", 16.5),
        ("Agent", "We have waived the three pound fifty fee, credited your ledger, and attached the permanent large-print accessibility exemption to your profile.", None),
        ("Customer", "You have sorted out everything I needed. Thank you so much for your help.", 32.1),
        ("Agent", "Is there any other aspect of your S-Net billing or services I can assist you with today, Fatima?", None),
        ("Customer", "No thank you Chloe, everything is completely resolved.", 24.5),
        ("Agent", "Thank you for choosing S-Net billing customer services, Fatima. Have a lovely and peaceful afternoon. Goodbye.", None),
        ("Customer", "Goodbye Chloe.", 18.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Your next monthly paper statement will dispatch on the twelfth of next month in your large print format.", None))
        raw.insert(-4, ("Customer", "I will look out for the postman bringing the large print envelope next month.", 16.4))
        raw.insert(-4, ("Agent", "Our customer care team remains available seven days a week for any future accessibility adjustments.", None))
        raw.insert(-4, ("Customer", "It is very reassuring to know S-Net has dedicated accessibility support.", 19.5))

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
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [03:15] when customer expressed emotional distress and humiliation over being penalised for visual impairment."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net billing customer services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Fatima throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute distress and humiliation regarding disability fee penalties; agent completely ignored feelings and defended batch runs.",
        "Paraphrasing": "Agent restated the £3.50 fee waiver request and large-print accessibility requirements accurately at [01:25].",
        "Active listening": "Agent confirmed contact landline number without repeating questions.",
        "Took ownership of the problem": "Agent applied £3.50 ledger credit and attached permanent RNIB Accessibility Exemption flag.",
        "Build rapport and observed professionalism": "Agent maintained a courteous and helpful tone throughout.",
        "Probing": "Agent asked relevant questions regarding statement dates and invoice details.",
        "Confirmed the issue is resolved": "Customer confirmed ledger credit applied and accepted large-print exemption setup."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 29}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 6},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 19}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 10},
            {"kind": "unhandled", "customer_turn": 20}
        ]
    }

    return {
        "cid": "agt_032",
        "cname": "Fatima",
        "target_dur": 792,
        "scenario": "Exemption request for £3.50 monthly paper billing fee for visual impairment accessibility",
        "tier": "good",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Empathy & Acknowledgment Statement"],
        "notes": "Excellent technical and procedural handling of accessibility fee waiver and large-print flag, but agent failed empathy when customer voiced humiliation and distress over disability charges."
    }

print("get_call_032 defined.")
# =========================================================================
# Call 033: Felix, Nuisance marketing calls flood, 17:33 (1053s)
# 5+ faults (poor), score 48.3, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL, Rapport FAIL, Ownership FAIL
# =========================================================================
def get_call_033():
    raw = [
        ("Agent", "Thank you for calling S-Net landline customer services, my name is Simon. How can I help you today?", None),
        ("Customer", "Hello Simon, my name is Felix Vance. For the past two weeks our landline telephone has been ringing twelve to fifteen times a day with automated scam calls, recorded robo-callers, and PPI marketing pitches!", -36.5),
        ("Agent", "Good afternoon Felix. I can check your telephone exchange provisioning profile. Before we look at call management features, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 72 Kingsway, Dundee, DD2 3PT, and my security PIN is 6309. My landline telephone handset is a BT 8600 Call Guardian unit.", -5.2),
        ("Agent", "Thank you Felix, that confirms your account details. Are the incoming nuisance calls showing up with international numbers, withheld numbers, or spoofed UK geographic codes?", None),
        ("Customer", "They show up with random UK mobile numbers and local area codes, and when you pick up it is an automated voice pretending to be HMRC or bank fraud departments!", -28.4),
        ("Agent", "Bear with me for a couple of minutes while I check your line routing and digital call features on our exchange switch.", None),
        ("Agent", "Thank you for waiting, Felix. The exchange switch records show standard CLI presentation active, but your line has no network-level spam screening subscription enabled.", None),
        ("Customer", "My ninety-one-year-old mother lives with me and suffers from dementia! She gets terrified every time the phone rings, thinking someone is coming to arrest her! She fell in the hallway rushing to answer one of these scam calls! I am completely stressed out and desperate! Why don't you block these criminals at the network exchange?!", -64.2),
        ("Agent", "Telecommunications carriers cannot legally intercept or filter public telephony traffic without specific court orders or statutory warrants.", None),
        ("Customer", "Other network providers offer free automatic spam call blocking! Why can't S-Net protect vulnerable elderly people from predatory scammers?!", -52.4),
        ("Agent", "Well if you had actually bothered to register your number with the Telephone Preference Service, you would have stopped the majority of legitimate marketing calls already instead of complaining to us.", None),
        ("Customer", "These are not legitimate marketing companies, Simon, they are criminal fraudsters! The TPS does not stop illegal spoofed scam calls!", -58.6),
        ("Agent", "Frontline telephony agents do not have administrative network firewalls to blacklist dynamic calling numbers.", None),
        ("Customer", "Then what can S-Net actually do to protect my mother's landline right now?", -38.2),
        ("Agent", "You need to purchase an external call blocker hardware box from Amazon or visit our online shop to buy our premium call guardian service.", None),
        ("Customer", "I am asking you to activate whatever call barring features exist on my line right now!", -42.1),
        ("Agent", "Frontline support lines do not activate commercial add-on bundles without sales team transfer.", None),
        ("Customer", "Then transfer me to the sales team or supervisor who can activate call blocking on this line!", -34.5),
        ("Agent", "Sales queues are currently busy with a forty-five minute hold queue. You should activate call features via your online account portal.", None),
        ("Customer", "You refuse to help me, you refuse to transfer me, and you blame me for criminal scam calls! My ninety-one-year-old mother is sitting in the corner trembling with terror because of your complete negligence! This is utterly disgraceful and intolerable!", -64.2),
        ("Agent", "I am stating the operational boundaries of frontline technical support.", None),
        ("Customer", "Can you at least activate Anonymous Caller Rejection on the exchange line so withheld numbers cannot ring the house?", -24.5),
        ("Agent", "Bear with me for two minutes while I check if Anonymous Caller Rejection is provisioned on your copper profile.", None),
        ("Agent", "Thank you for waiting, Felix. Anonymous Caller Rejection is available on your exchange line.", None),
        ("Customer", "Please turn it on immediately.", -14.2),
        ("Agent", "I have submitted the network command to activate Anonymous Caller Rejection. Withheld numbers will hear an automated rejection announcement.", None),
        ("Agent", "Which model of landline telephone handset is plugged into the wall socket?", None),
        ("Customer", "As I said right at the beginning of the call, it is a BT 8600 Call Guardian unit.", -18.4),
        ("Agent", "Obviously hardware handset call screening works independently of exchange-level call routing.", None),
        ("Customer", "I will program my family and doctor numbers into the VIP whitelist on the BT 8600 handset so only known callers can ring.", 14.2),
        ("Agent", "That will block any caller not listed in your VIP memory directory.", None),
        ("Customer", "What is the reference code for the Anonymous Caller Rejection you activated?", -4.2),
        ("Agent", "The order reference identifier is ACR-99120-D.", None),
        ("Customer", "ACR-99120-D, noted down.", 8.4),
        ("Agent", "The feature will become active on your exchange circuit within twenty-four hours.", None),
        ("Customer", "That will at least eliminate the silent withheld calls.", 16.5),
        ("Agent", "I have documented your complaint on customer ticket SN-440182.", None),
        ("Customer", "Very well, I will set up the handset whitelist tonight.", 12.1),
        ("Agent", "Is there any other aspect of your landline telephone connection I can help you with today, Felix?", None),
        ("Customer", "No, I will handle the rest with the handset manual.", 8.2),
        ("Agent", "Thank you for choosing S-Net landline customer services, Felix. Goodbye.", None),
        ("Customer", "Goodbye Simon.", 4.5),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Your landline telephone billing plan will reflect the Anonymous Caller Rejection feature on your next cycle.", None))
        raw.insert(-4, ("Customer", "Please make sure no unexpected hidden fees are added for this safety feature.", 8.2))
        raw.insert(-4, ("Agent", "The feature is provided at zero additional recurring charge under our vulnerable customer policy.", None))
        raw.insert(-4, ("Customer", "That is appreciated given my mother's health condition.", 14.1))

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
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [03:20] when customer expressed acute distress regarding his vulnerable mother with dementia falling in the hallway.",
        "Paraphrasing": "Did not paraphrase customer's nuisance call problem in own words.",
        "Active listening": "Asked customer at [09:15] for his telephone handset model which had already been stated at [00:45].",
        "Took ownership of the problem": "Deflected responsibility at [05:40] by telling customer to buy hardware from Amazon or use online forms rather than assisting.",
        "Build rapport and observed professionalism": "Spoke rudely and aggressively at [04:10] stating 'Well if you had actually bothered to register your number with the Telephone Preference Service... instead of complaining to us.'"
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net landline customer services' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Holds announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Felix throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute distress and fear regarding elderly mother with dementia falling; agent offered zero empathy.",
        "Paraphrasing": "Agent never restated the nuisance call situation in his own words.",
        "Active listening": "Agent asked for handset model at turn 28 despite customer stating BT 8600 Call Guardian at turn 3.",
        "Took ownership of the problem": "Agent repeatedly deflected ownership telling customer to buy third-party devices or use online portal.",
        "Build rapport and observed professionalism": "Agent insulted customer at [04:10]: 'Well if you had actually bothered to register... instead of complaining to us.'",
        "Probing": "Agent asked diagnostic questions regarding caller ID display and scam call presentation.",
        "Confirmed the issue is resolved": "Customer confirmed Anonymous Caller Rejection activated with reference ACR-99120-D and agreed to configure handset whitelist."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 27, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "rude", "agent_turn": 11},
            {"kind": "blunt_but_ok", "agent_turn": 29}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 8},
            {"kind": "unhandled", "customer_turn": 20}
        ]
    }

    return {
        "cid": "agt_033",
        "cname": "Felix",
        "target_dur": 1053,
        "scenario": "Nuisance marketing calls flood; configuring S-Net Call Guardian VIP whitelist",
        "tier": "poor",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Build rapport and observed professionalism", "Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Poor customer service call featuring agent rudeness, victim-blaming regarding TPS, deflection of ownership, failure of empathy regarding a vulnerable dementia patient, and repeated questioning."
    }

print("get_call_033 defined.")


# =========================================================================
# Call 034: Fiona, TV voice remote Bluetooth pairing failure, 13:46 (826s)
# 3-4 faults (okay), score 71.7, Empathy FAIL, Paraphrasing FAIL, Active listening FAIL
# =========================================================================
def get_call_034():
    raw = [
        ("Agent", "Thank you for calling S-Net TV support, my name is Oscar. How can I help you today?", None),
        ("Customer", "Hello Oscar, my name is Fiona MacLeod. My S-Net TV voice remote control stopped working after the automated firmware update last night, and the microphone button does absolutely nothing when I try to search for programmes!", -32.4),
        ("Agent", "Good afternoon Fiona. I can look into your TV box pairing and voice remote telemetry. Before we inspect your remote profile, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 18 Rosemount Viaduct, Aberdeen, AB25 1NT, and my security PIN is 4092. My TV box model is the S-Net 4K Hub Box with serial number SN-88201.", -6.2),
        ("Agent", "Thank you Fiona, that confirms your account details. What happens on the TV screen when you press the microphone button on the remote?", None),
        ("Customer", "Nothing happens at all! No microphone listening icon appears, and speech search does not activate. But the regular channel up and down buttons work.", -24.5),
        ("Agent", "Can you see the small LED light at the top of the remote when you press the voice button?", None),
        ("Customer", "It flashes a slow orange light twice and then turns off.", -14.2),
        ("Agent", "Bear with me for a couple of minutes while I check the remote firmware patch status on our digital television gateway.", None),
        ("Agent", "Thank you for waiting, Fiona. The gateway logs indicate firmware update 3.14 was applied overnight, which de-coupled the Bluetooth Low Energy voice channel into fallback infrared mode.", None),
        ("Customer", "I am severely arthritic in both my hands and I rely entirely on voice search commands to navigate channels and find my recorded programmes! Having to physically press tiny plastic buttons repeatedly causes me severe physical joint pain! I am in tears with frustration right now!", -58.4),
        ("Agent", "Firmware version 3.14 required all peripheral voice accessories to re-handshake encrypted Bluetooth security tokens.", None),
        ("Customer", "I do not care about security tokens, Oscar! Tell me how to get the microphone working so I can use my TV without hurting my hands!", -48.2),
        ("Agent", "To restore voice functionality, the remote must be switched out of infrared fallback mode back into Bluetooth LE mode.", None),
        ("Customer", "How do I do that?", -18.5),
        ("Agent", "You must perform a simultaneous two-button handshake sequence while pointing the remote at the TV box.", None),
        ("Customer", "Which buttons do I need to press?", -11.2),
        ("Agent", "Obviously voice search requires bidirectional Bluetooth bandwidth rather than unidirectional infrared pulses.", None),
        ("Customer", "I understand that, please just tell me the buttons.", -15.4),
        ("Agent", "Press and hold the 'Voice' button and the 'OK' button together simultaneously for five seconds.", None),
        ("Customer", "Holding Voice and OK together... One, two, three, four, five... Oscar, my fingers are swollen and throbbing with agony trying to hold these stiff buttons down! Why do you make technology so painful for disabled customers?! The light is flashing rapid blue!", -52.4),
        ("Agent", "Now release both buttons. The TV screen should display a pairing prompt.", None),
        ("Customer", "Yes! A box popped up saying 'Voice Remote Paired Successfully - Battery 90%'.", 32.1),
        ("Agent", "Now press and hold the voice button, speak 'BBC One', and release the button.", None),
        ("Customer", "Holding button... 'BBC One'... Releasing button... Yes! A blue listening bar appeared and BBC One immediately tuned in!", 64.2),
        ("Agent", "Splendid! Let us try another voice command to search recorded shows.", None),
        ("Customer", "Holding voice button... 'Open Recordings'... Yes! It opened my recorded series list instantly without pressing any arrow keys!", 72.5),
        ("Agent", "What was that TV box model again?", None),
        ("Customer", "As I told you during verification, it is the S-Net 4K Hub Box.", -16.4),
        ("Agent", "That confirms full Bluetooth Low Energy voice profile re-establishment with your 4K Hub Box.", None),
        ("Customer", "Thank goodness. I can navigate my television comfortably again without pain in my hands.", 42.1),
        ("Agent", "If your remote ever loses Bluetooth connection in the future, holding Voice and OK together for five seconds will re-bind the channel immediately.", None),
        ("Customer", "I have written that down on my TV guide notepad.", 24.5),
        ("Agent", "We have re-established the Bluetooth voice connection, confirmed voice channel switching, and verified recorded shows search.", None),
        ("Customer", "Everything is working smoothly now. Thank you Oscar.", 34.2),
        ("Agent", "Is there any other technical matter regarding your TV box or remote I can assist you with today, Fiona?", None),
        ("Customer", "No thank you, that was the only problem.", 22.1),
        ("Agent", "Thank you for choosing S-Net TV support, Fiona. Have a wonderful and restful afternoon. Goodbye.", None),
        ("Customer", "Goodbye Oscar.", 18.2),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Your 4K Hub Box will retain the paired Bluetooth device profile through future automatic software updates.", None))
        raw.insert(-4, ("Customer", "That gives me peace of mind that it will not unpair again next week.", 18.2))
        raw.insert(-4, ("Agent", "The Bluetooth remote provides thirty feet of wireless range without requiring line of sight.", None))
        raw.insert(-4, ("Customer", "That is very convenient from my armchair across the living room.", 22.4))

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
        "Empathy & Acknowledgment Statement": "Failed to show empathy at [02:50] when customer expressed acute physical pain and distress from arthritis when unable to use voice search.",
        "Paraphrasing": "Failed to paraphrase customer's voice remote failure in own words.",
        "Active listening": "Asked customer at [07:15] for her TV box model which had already been verified at [00:45]."
    }

    evidence = {
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net TV support' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Fiona throughout the call.",
        "Empathy & Acknowledgment Statement": "Customer expressed acute distress and joint pain from severe arthritis; agent offered no empathy and recited Bluetooth protocols.",
        "Paraphrasing": "Agent never restated the voice remote failure in his own words.",
        "Active listening": "Agent asked for TV box model at turn 26 despite customer providing S-Net 4K Hub Box at turn 3.",
        "Took ownership of the problem": "Agent guided customer through Bluetooth re-pairing sequence to successfully restore voice commands.",
        "Build rapport and observed professionalism": "Agent maintained a courteous instructional tone throughout.",
        "Probing": "Agent asked diagnostic questions regarding remote LED behavior and button responses.",
        "Confirmed the issue is resolved": "Customer confirmed voice remote paired, tuned to BBC One, and opened recordings via voice."
    }

    markers = {
        "active_listening": [
            {"kind": "repeat", "premise_turn": 3, "agent_turn": 27, "reworded": True}
        ],
        "paraphrasing": [
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 17}
        ],
        "empathy": [
            {"kind": "unhandled", "customer_turn": 10},
            {"kind": "unhandled", "customer_turn": 20}
        ]
    }

    return {
        "cid": "agt_034",
        "cname": "Fiona",
        "target_dur": 826,
        "scenario": "TV voice remote Bluetooth pairing failure and dead microphone after firmware patch",
        "tier": "okay",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Paraphrasing"],
        "notes": "Good technical walk-through of Bluetooth voice remote pairing, but agent failed empathy regarding physical arthritis pain, failed paraphrasing, and repeated a question about TV box model."
    }

print("get_call_034 defined.")


# =========================================================================
# Call 035: Gabriel, Trade-in credit of £150 missing, 19:32 (1172s)
# excellent, score 100.0, All PASS, 2 handled outbursts (1 late 3-4 turns)
# =========================================================================
def get_call_035():
    raw = [
        ("Agent", "Thank you for calling S-Net mobile customer care and billing, my name is Daniel. How can I help you today?", None),
        ("Customer", "Hello Daniel, my name is Gabriel Miller. I traded in my old iPhone 12 when upgrading to an iPhone 15 thirty days ago, your warehouse confirmed receipt and valuation of one hundred and fifty pounds, but my new invoice has zero credit applied and billed me full price!", -34.8),
        ("Agent", "Good afternoon Gabriel. I can certainly inspect your trade-in ledger and mobile billing statement. Before we access your finance records, could you confirm your full postal address and your account security PIN?", None),
        ("Customer", "Yes, it is 84 Victoria Park Road, Exeter, EX1 3PX, and my security PIN is 5104. My trade-in reference number is TRD-881902.", -5.4),
        ("Agent", "Thank you Gabriel, that confirms your account details. What total amount was billed on your latest monthly statement?", None),
        ("Customer", "The statement billed seventy-five pounds for the handset and tariff, with absolutely no mention of the one hundred and fifty pounds trade-in credit! Daniel, I am furious! I specifically sent my immaculate iPhone 12 in your tracked packaging, Royal Mail signed for it on October 18th, and your automated email promised credit within two billing cycles! I feel completely cheated!", -62.4),
        ("Agent", "Bear with me for a couple of minutes while I query our logistics warehouse intake registry and finance reconciliation portal.", None),
        ("Agent", "Thank you for waiting, Gabriel. I have located warehouse intake report TRD-881902. The iPhone 12 was received, fully inspected, and graded Grade A with the full one hundred and fifty pounds valuation authorized on October 20th.", None),
        ("Agent", "I completely understand how frustrating and alarming it is to see a seventy-five pound invoice without your agreed one hundred and fifty pound trade-in credit, Gabriel, especially after sending in your device on time. Let us make sure this is rectified immediately.", None),
        ("Customer", "Thank you Daniel, I appreciate you looking into that so quickly. Why was it not applied to my statement?", 14.2),
        ("Agent", "A batch transmission delay occurred between our logistics grading database and our recurring subscription billing engine, leaving the credit voucher in unallocated status.", None),
        ("Customer", "Can you pull that credit voucher into my billing account right now?", 18.5),
        ("Agent", "Yes, I am executing the manual ledger binding command to attach voucher TRD-881902 directly to your active mobile account.", None),
        ("Customer", "Does that apply the full one hundred and fifty pounds?", 22.1),
        ("Agent", "Yes, the full one hundred and fifty pounds has been posted to your account as an unallocated credit balance.", None),
        ("Customer", "How will that credit be used against my upcoming payments?", 16.4),
        ("Agent", "It will automatically offset your current seventy-five pound invoice to zero pounds, and the remaining seventy-five pounds will offset your entire December invoice to zero pounds as well.", None),
        ("Customer", "So I will have zero pounds to pay for both November and December?", 38.5),
        ("Agent", "That is correct. You will have two consecutive months of completely free mobile service.", None),
        ("Customer", "That is a huge relief to hear.", 42.1),
        ("Agent", "Let me check the direct debit mandate to make sure no automated sweep attempts to draw funds for November.", None),
        ("Customer", "Yes, please ensure my bank account is not debited seventy-five pounds next week!", -18.2),
        ("Agent", "Obviously automated direct debit sweeps execute unless a zero balance clearance command is submitted to the payment gateway.", None),
        ("Customer", "I had a terrible experience with another network taking direct debits in error before, so I get very anxious about unexpected bank debits!", -32.4),
        ("Agent", "I completely understand that anxiety, Gabriel. I have locked the November debit sweep to zero pounds in the Bacs gateway right now, so no funds will leave your bank.", None),
        ("Customer", "Thank you so much Daniel, that puts my mind completely at ease.", 44.5),
        ("Agent", "I am generating an updated PDF invoice reflecting the one hundred and fifty pound credit voucher and sending it to your email address right now.", None),
        ("Customer", "Let me refresh my email inbox on my phone... Yes! 'S-Net Updated Statement - Balance Due: £0.00'.", 64.2),
        ("Agent", "Splendid! And your December statement will also reflect zero balance automatically.", None),
        ("Customer", "This is outstanding service. You resolved everything in one single call.", 56.4),
        ("Agent", "Before we conclude our call, that registered mobile phone number was 07700 900418, correct?", None),
        ("Customer", "Yes, 07700 900418.", 18.2),
        ("Agent", "We have allocated your one hundred and fifty pound trade-in credit, cleared your November bill to zero, confirmed December will be zero, and locked the direct debit sweep.", None),
        ("Customer", "Everything is completely sorted. Thank you Daniel.", 48.2),
        ("Agent", "You can monitor your remaining credit balance at any time on the My S-Net mobile app.", None),
        ("Customer", "I will check the app to see the remaining seventy-five pounds.", 22.4),
        ("Agent", "Is there any other aspect of your mobile contract or trade-in I can help you with today, Gabriel?", None),
        ("Customer", "No thank you Daniel, you have been first-class.", 31.2),
        ("Agent", "Thank you for choosing S-Net mobile customer care, Gabriel. Enjoy your new iPhone 15 and have a wonderful day. Goodbye.", None),
        ("Customer", "Goodbye Daniel.", 24.5),
        ("Agent", "Thank you for choosing S-Net. Goodbye.", None)
    ]

    while len(raw) < 58:
        raw.insert(-4, ("Agent", "Your iPhone 15 comes with a comprehensive twenty-four month manufacturer warranty through S-Net.", None))
        raw.insert(-4, ("Customer", "That is great reassurance for the entire duration of the two-year contract.", 24.1))
        raw.insert(-4, ("Agent", "Our mobile trade-in program ensures recycled handsets are refurbished to environmental sustainability standards.", None))
        raw.insert(-4, ("Customer", "I am glad my old iPhone 12 will be refurbished responsibly.", 28.5))

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
        "Branding and Survey Check": "Agent opened with 'Thank you for calling S-Net mobile customer care and billing' at [00:00] and closed with 'Thank you for choosing S-Net' in final lines.",
        "Hold time and Dead Air": "Hold was announced with bear with me and thanked upon return without unmanaged dead air.",
        "Verified customer": "Verified full postal address and security PIN within the first 240 seconds.",
        "Personalized the call/ticket appropriately": "Agent addressed customer as Gabriel warmly throughout the call.",
        "Empathy & Acknowledgment Statement": "Agent delivered late empathy at [02:40] after warehouse lookup ('I completely understand how frustrating and alarming it is to see a seventy-five pound invoice without your agreed one hundred and fifty pound trade-in credit...'), and handled second anxiety outburst at [07:15].",
        "Paraphrasing": "Agent restated the trade-in credit omission and billing issue accurately at [01:25].",
        "Active listening": "Agent confirmed mobile number accurately without repeating questions.",
        "Took ownership of the problem": "Agent manually bound trade-in voucher, zeroed invoice, locked Bacs sweep, and emailed updated PDF.",
        "Build rapport and observed professionalism": "Agent maintained an exemplary, reassuring, and professional tone throughout.",
        "Probing": "Agent asked relevant questions regarding statement details and direct debit dates.",
        "Confirmed the issue is resolved": "Customer confirmed receipt of updated zero-balance statement PDF and verified direct debit sweep halted."
    }

    markers = {
        "active_listening": [
            {"kind": "harmless_recheck", "premise_turn": 3, "agent_turn": 30}
        ],
        "paraphrasing": [
            {"kind": "restatement", "agent_turn": 7},
            {"kind": "not_a_restatement", "agent_turn": 4}
        ],
        "rapport": [
            {"kind": "blunt_but_ok", "agent_turn": 22}
        ],
        "empathy": [
            {"kind": "handled", "customer_turn": 5, "agent_turn": 8, "with_refusal": False},
            {"kind": "handled", "customer_turn": 23, "agent_turn": 24, "with_refusal": False}
        ]
    }

    return {
        "cid": "agt_035",
        "cname": "Gabriel",
        "target_dur": 1172,
        "scenario": "Trade-in credit of £150 missing from mobile invoice 30 days post warehouse receipt",
        "tier": "excellent",
        "raw_turns": raw,
        "ratings": ratings,
        "coaching_map": coaching,
        "evidence_map": evidence,
        "markers": markers,
        "hard_cases": ["Active listening", "Empathy & Acknowledgment Statement", "Took ownership of the problem"],
        "notes": "Exemplary billing resolution featuring two handled customer outbursts (including a late acknowledgment 3 turns after initial complaint), manual ledger allocation, direct debit locking, and instant PDF reissue."
    }

print("get_call_035 defined.")

if __name__ == "__main__":
    for fn in [get_call_031, get_call_032, get_call_033, get_call_034, get_call_035]:
        c = fn()
        compile_call(c)
