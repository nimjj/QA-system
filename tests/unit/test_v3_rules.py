import unittest

from tests.unit.helpers import call
from src.v3 import rules


class AutoFail(unittest.TestCase):
    def check(self, line):
        c = call(("Agent", "Thank you for calling S-Net.", 0), ("Agent", line, 20), ("Customer", "ok", 30, -5.0))
        return rules.check_auto_fail(c)[0]

    def test_real_abuse_fails(self):
        for line in ("Oh shut up and listen", "You are an idiot", "That is a stupid thing to say", "Just get lost", "I'm going to hang up on you",
                     "This is f***ing ridiculous", "shut-up please", "fucking hell"):
            self.assertTrue(self.check(line), line)

    def test_insults_found_in_the_dev_sets_are_not_missed(self):
        # each pattern below once slipped past a first draft of the rule
        for line in ("Look, don't be an idiot, the page is down", "If you don't like it you can get lost and wait for the cheque",
                     "Feel free to get lost and try a competitor", "Just hang up and stop wasting my time", "Stop being stupid about this"):
            self.assertTrue(self.check(line), line)

    def test_polite_hang_up_instructions_are_fine(self):
        for line in ("Please hang up and call us back on 0800", "Just hang up the phone and redial", "You can hang up the old line now"):
            self.assertFalse(self.check(line), line)

    def test_harmless_phrases_do_not_zero_the_call(self):
        for line in ("That's not a stupid question", "I'll hang up the old line, then call back", "Please don't get lost in the menu",
                     "Don't hang up, I'll transfer you", "There are no stupid questions here", "you might get lost in the settings page",
                     "The idiot-proof setup takes two minutes"):
            self.assertFalse(self.check(line), line)

    def test_customer_language_never_fails_the_agent(self):
        c = call(("Agent", "Thank you for calling S-Net.", 0), ("Customer", "You are a stupid idiot, shut up!", 10, -60.0))
        self.assertFalse(rules.check_auto_fail(c)[0])

    def test_labelled_agent_two_is_checked(self):
        c = call(("Agent 2", "shut up", 0), ("Customer", "hello?", 10, -10.0))
        self.assertTrue(rules.check_auto_fail(c)[0])


class Branding(unittest.TestCase):
    def run_b(self, first, last="Thank you for choosing S-Net, goodbye."):
        lines = [("Agent", first, 0), ("Customer", "My internet is down", 10, -20.0), ("Agent", "Let me check", 20),
                 ("Customer", "ok", 40, -10.0), ("Agent", "Fixed", 60), ("Customer", "thanks", 70, 10.0), ("Agent", "Great", 80),
                 ("Agent", "Anything else", 90), ("Customer", "No", 95, 5.0), ("Agent", last, 100)]
        return rules.evaluate_branding(call(*lines))["rating"]

    def test_asr_variants_pass(self):
        for g in ("Thank you for calling S-Net, my name is Sam", "thank you for calling, S-Net", "Thank you for calling S net",
                  "Thank you for calling Snet", "Thank you for calling s dash net", "THANK YOU FOR CALLING S‑NET"):
            self.assertEqual(self.run_b(g), "PASS", g)

    def test_script_still_required(self):
        self.assertEqual(self.run_b("Thanks for calling S-Net"), "FAIL")
        self.assertEqual(self.run_b("Hello, how can I help"), "FAIL")
        self.assertEqual(self.run_b("Thank you for calling S-Net", last="Bye now"), "FAIL")

    def test_ivr_line_does_not_use_up_a_slot(self):
        c = call(("IVR", "Welcome. Your call may be recorded.", 0), ("Bot", "Please hold while we connect you", 4),
                 ("Agent", "Hi.", 10), ("Agent", "Hello again", 12), ("Agent", "Thank you for calling S-Net", 14),
                 ("Customer", "hi", 20, 0.5), ("Agent", "Thank you for choosing S-Net", 40))
        self.assertEqual(rules.evaluate_branding(c)["rating"], "PASS")

    def test_one_line_cannot_serve_as_both_greeting_and_closing(self):
        c = call(("Agent", "Thank you for calling S-Net and thank you for choosing S-Net", 0), ("Customer", "ok", 10, 0.5))
        self.assertEqual(rules.evaluate_branding(c)["rating"], "FAIL")


class DeadAir(unittest.TestCase):
    def test_long_agent_monologues_with_immediate_replies_are_not_dead_air(self):
        # v2 assumed 10 s per turn and failed this call; real end times show no silence at all
        c = call(("Agent", "x", 0, None, 45), ("Customer", "ok", 45, -5.0, 49), ("Agent", "y", 50, None, 95), ("Customer", "ok", 96, -5.0, 99),
                 ("Agent", "z", 100, None, 140))
        self.assertEqual(rules.evaluate_dead_air(c)["rating"], "PASS")

    def test_real_silences_after_short_turns_are_found(self):
        c = call(("Agent", "hi", 0, None, 2), ("Customer", "hello", 37, -5.0, 39), ("Agent", "right", 76, None, 78), ("Customer", "yes", 112, -5.0, 114))
        self.assertEqual(rules.evaluate_dead_air(c)["rating"], "FAIL")

    def test_one_ten_minute_silence_fails(self):
        c = call(("Agent", "hi", 0, None, 2), ("Customer", "hello", 4, -5.0, 6), ("Agent", "one sec", 602, None, 604), ("Customer", "ok", 606, -5.0, 608))
        self.assertEqual(rules.evaluate_dead_air(c)["rating"], "FAIL")

    def test_announced_holds_are_excused_in_every_common_wording(self):
        for phrase in ("I'm putting you on hold", "Please hold", "Give me a minute to check that", "One moment please", "Bear with me",
                       "Let me place you on a brief hold"):
            c = call(("Agent", phrase, 0, None, 3), ("Agent", "Thank you for holding.", 60, None, 63), ("Customer", "no problem", 64, -5.0, 66),
                     ("Agent", phrase, 70, None, 73), ("Agent", "Sorry for the wait.", 140, None, 143))
            self.assertEqual(rules.evaluate_dead_air(c)["rating"], "PASS", phrase)

    def test_customer_chasing_the_agent_is_not_a_managed_hold(self):
        c = call(("Agent", "Bear with me", 0, None, 3), ("Customer", "Hello? Are you still there?", 50, -20.0, 53), ("Agent", "Bear with me", 60, None, 63),
                 ("Customer", "Hello?", 115, -20.0, 117))
        self.assertEqual(rules.evaluate_dead_air(c)["rating"], "FAIL")

    def test_customer_looking_something_up_is_not_blamed_on_the_agent(self):
        c = call(("Agent", "Can you check the lights on your router?", 0, None, 4), ("Customer", "Yes it's red", 60, -5.0, 63),
                 ("Agent", "Can you read me the model number on the sticker?", 66, None, 71), ("Customer", "It's a Hub 4", 130, -5.0, 133))
        self.assertEqual(rules.evaluate_dead_air(c)["rating"], "PASS")

    def test_a_plain_instruction_gives_the_customer_time_to_act(self):
        c = call(("Agent", "Just reboot it. Unplug it, wait, plug it back in.", 0, None, 6), ("Customer", "Okay, doing it now", 41, -5.0, 44),
                 ("Agent", "Now check the light.", 46, None, 49), ("Customer", "It is green", 90, -5.0, 92))
        self.assertEqual(rules.evaluate_dead_air(c)["rating"], "PASS")

    def test_start_times_only_still_works_with_estimated_ends(self):
        c = call(("Agent", "word " * 5, 0), ("Customer", "word " * 5, 10, -5.0), ("Agent", "word " * 5, 20))
        self.assertEqual(rules.evaluate_dead_air(c)["rating"], "PASS")


class Verified(unittest.TestCase):
    def verdict(self, line, at=30):
        c = call(("Agent", "Thank you for calling S-Net.", 0), ("Agent", line, at), ("Customer", "ok", at + 10, -5.0))
        return rules.evaluate_verified(c)["rating"]

    def test_real_requests_pass(self):
        for line in ("Can you confirm your PIN?", "What is the security answer on your account?", "Could you confirm your billing address?",
                     "May I take your full billing address please", "Can you give me your security questions answer", "Please provide the P.I.N."):
            self.assertEqual(self.verdict(line), "PASS", line)

    def test_other_kinds_of_address_do_not_count(self):
        for line in ("What's your email address?", "Can you read me the IP address on the screen?", "Please give me the MAC address",
                     "What is your web address?"):
            self.assertEqual(self.verdict(line), "FAIL", line)

    def test_negated_mentions_do_not_count(self):
        self.assertEqual(self.verdict("I don't need your PIN today."), "FAIL")

    def test_a_voicemail_passcode_is_not_identity_verification(self):
        self.assertEqual(self.verdict("When did you last update your four-digit voicemail passcode?"), "FAIL")
        self.assertEqual(self.verdict("Can you confirm your security passcode?"), "PASS")

    def test_postcode_counts_only_when_the_business_allows_it(self):
        line = "Give me your account number and your postcode so I can bring up your profile"
        self.assertEqual(self.verdict(line), "FAIL")
        cfg = {"verification": {"window_seconds": 240, "accept_postcode": True, "accept_account_number": True}}
        c = call(("Agent", "Hello", 0), ("Agent", line, 20), ("Customer", "ok", 30, -5.0))
        self.assertEqual(rules.evaluate_verified(c, cfg)["rating"], "PASS")

    def test_window_counts_from_the_first_agent_line_not_from_zero(self):
        c = call(("IVR", "Welcome", 0), ("Agent", "Hello", 400), ("Agent", "Can you confirm your PIN?", 430), ("Customer", "1234", 440, -5.0))
        self.assertEqual(rules.evaluate_verified(c)["rating"], "PASS")
        late = call(("Agent", "Hello", 0), ("Agent", "Can you confirm your PIN?", 300), ("Customer", "1234", 310, -5.0))
        self.assertEqual(rules.evaluate_verified(late)["rating"], "FAIL")

    def test_date_of_birth_and_account_number_count_only_when_the_business_allows_it(self):
        self.assertEqual(self.verdict("What is your date of birth?"), "FAIL")
        cfg = {"verification": {"window_seconds": 240, "accept_date_of_birth": True, "accept_account_number": True}}
        c = call(("Agent", "Hello", 0), ("Agent", "What is your account number?", 20), ("Customer", "123", 30, -5.0))
        self.assertEqual(rules.evaluate_verified(c, cfg)["rating"], "PASS")


class Personalized(unittest.TestCase):
    def verdict(self, name, line):
        c = call(("Agent", "Thank you for calling S-Net.", 0), ("Agent", line, 20), ("Customer", "ok", 30, -5.0), name=name)
        return rules.evaluate_personalized(c)["rating"]

    def test_whole_word_match(self):
        self.assertEqual(self.verdict("Sam", "Hi Sam, how can I help"), "PASS")
        self.assertEqual(self.verdict("Sam Smith", "Hi Sam, how can I help"), "PASS")
        self.assertEqual(self.verdict("Sam Smith", "Thanks, Mr Smith"), "PASS")

    def test_substrings_inside_other_words_do_not_count(self):
        self.assertEqual(self.verdict("Sam", "Is it a Samsung phone?"), "FAIL")
        self.assertEqual(self.verdict("Al", "We also offer that"), "FAIL")
        self.assertEqual(self.verdict("Ann", "That is another channel"), "FAIL")

    def test_small_asr_spelling_errors_are_tolerated_on_longer_names(self):
        self.assertEqual(self.verdict("Priyanka", "Hi Priyanca, how can I help"), "PASS")

    def test_customer_saying_their_own_name_does_not_count(self):
        c = call(("Agent", "Hello", 0), ("Customer", "Hi it's Sam here", 10, -5.0), ("Agent", "How can I help", 20), name="Sam")
        self.assertEqual(rules.evaluate_personalized(c)["rating"], "FAIL")

    def test_no_name_supplied_is_not_penalised_and_says_so(self):
        c = call(("Agent", "Hello", 0), ("Customer", "hi", 10, -5.0))
        r = rules.evaluate_personalized(c)
        self.assertEqual(r["rating"], "PASS")
        self.assertIn("not checked", r["note"])


if __name__ == "__main__":
    unittest.main()
