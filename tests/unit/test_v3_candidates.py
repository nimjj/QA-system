import unittest

from tests.unit.helpers import call
from src.v3.candidates import common, ownership, paraphrase, resolved


def turns(*lines):
    """('A'|'C', text) -> a normalised call, 10 s apart; customer lines carry a flat sentiment of -5."""
    out = []
    for i, (who, text) in enumerate(lines):
        out.append(("Agent", text, i * 10) if who == "A" else ("Customer", text, i * 10, -5.0))
    return call(*out)


class ClosingLines(unittest.TestCase):
    def test_pure_pleasantries_are_closing_lines(self):
        for t in ("Thanks Craig, take care.", "Goodbye.", "Thank you for choosing S-Net. Goodbye.", "Have a productive day, Arthur. Take care.",
                  "You are very welcome, Arthur.", "Thanks again, bye."):
            self.assertTrue(common.is_closing_line(t), t)

    def test_lines_about_the_problem_or_the_fix_are_kept(self):
        for t in ("Thanks, it is working now.", "Thank you, the issue is fixed.", "Is there anything else I can help with?",
                  "No, that is everything, thanks.", "Your refund ticket reference is INC-882194, thank you for holding.",
                  "I have fixed it", "x " * 20 + "thanks"):
            self.assertFalse(common.is_closing_line(t), t)


class ResolvedWindows(unittest.TestCase):
    def call(self):
        lines = [("C", "My internet keeps dropping every evening and it is driving me mad"), ("A", "I will reset your line now"),
                 ("C", "Okay"), ("A", "I have fixed the line fault and your router is back online. Is it working for you now?"),
                 ("C", "Yes it is working now, thanks"), ("A", "Is there anything else I can help with today?"), ("C", "No that is all"),
                 ("A", "Thank you for choosing S-Net, goodbye."), ("C", "Thanks, take care."), ("A", "Have a lovely day."),
                 ("C", "Goodbye."), ("A", "Goodbye now."), ("C", "Bye."), ("A", "Bye bye."), ("C", "Cheers."), ("A", "Take care now.")]
        return turns(*lines)

    def test_v2_tail_is_mostly_goodbyes_while_v3_reaches_the_fix(self):
        c = self.call()
        v2 = resolved.tail10(c)[0]
        v3 = resolved.subst16(c)[0]
        self.assertNotIn("back online", v2)
        self.assertIn("back online", v3)
        self.assertIn("Is it working for you now", v3)

    def test_the_end_of_the_call_stays_visible(self):
        w = resolved.subst16(self.call())[0].split("\n")
        self.assertEqual(w[-1], "Agent: Take care now.")
        self.assertEqual(w[-2], "Customer: Cheers.")
        self.assertEqual(len(w), len(set(w)) + 0)                         # nothing is listed twice

    def test_ivr_lines_are_not_in_the_window(self):
        c = call(("IVR", "Your call may be recorded", 0), ("Agent", "Hello", 5), ("Customer", "Hi, my box is broken", 10, -5.0))
        self.assertNotIn("recorded", resolved.subst16(c)[0])

    def test_window_respects_the_word_cap(self):
        long = [("C" if i % 2 else "A", "word " * 40) for i in range(30)]
        self.assertLessEqual(len(resolved.subst16(turns(*long))[0].split()) , 320 + 2 * 45)


class Mood(unittest.TestCase):
    def call_with(self, sentiments):
        lines = []
        for i, s in enumerate(sentiments):
            lines += [("Agent", f"agent line {i}", i * 20), ("Customer", f"customer line {i}", i * 20 + 10, s)]
        return call(*lines)

    def test_ending_happier_than_the_call_average_scores_above_half(self):
        c = self.call_with([-30, -25, -20, -15, 10, 20, 25])
        self.assertGreater(resolved.mood_score(c), 0.5)

    def test_ending_worse_than_the_call_average_scores_below_half(self):
        c = self.call_with([5, 10, 12, 8, -30, -40, -45])
        self.assertLess(resolved.mood_score(c), 0.5)

    def test_it_is_relative_to_the_call_not_an_absolute_scale(self):
        a = self.call_with([-30, -25, -20, -15, 10, 20, 25])
        b = self.call_with([s * 0.3 for s in [-30, -25, -20, -15, 10, 20, 25]])
        self.assertAlmostEqual(resolved.end_mood(b), resolved.end_mood(a) * 0.3, places=6)
        self.assertTrue(resolved.mood_score(b) > 0.5)

    def test_without_enough_sentiment_the_model_score_is_used_unchanged(self):
        c = call(("Agent", "Hi", 0), ("Customer", "Hello", 5, -5.0), ("Agent", "Fixed", 10), ("Customer", "Thanks", 15, 5.0))
        self.assertFalse(resolved.mood_usable(c))
        self.assertEqual(resolved.blended_score(0.7, c, 0.5), 0.7)

    def test_blend_is_the_weighted_average(self):
        c = self.call_with([-30, -25, -20, -15, 10, 20, 25])
        self.assertAlmostEqual(resolved.blended_score(0.8, c, 0.5), 0.5 * 0.8 + 0.5 * resolved.mood_score(c), places=9)


class OwnershipGate(unittest.TestCase):
    def agent_says(self, line):
        return turns(("C", "My internet has been down for two days"), ("A", line), ("C", "That is not good enough"), ("A", "Let me see what I can do"))

    def test_the_wider_wordings_open_a_window(self):
        for line in ("Anything wrong down there is Telstra's responsibility, not ours.", "That's essentially Netflix's problem, not S-Net's.",
                     "Cabinet lightning strikes aren't S-Net's responsibility.", "Firmware rollbacks cannot be performed on customer equipment.",
                     "Finance managers do not take customer phone calls. You must wait for the monthly audit cycle.",
                     "I'm afraid that is out of my hands.", "You will need to contact the landlord about that.", "I can't fix a fault on the street node."):
            self.assertTrue(ownership.wide(self.agent_says(line)), line)

    def test_ordinary_helpful_lines_open_nothing(self):
        for line in ("Let me check your line for you.", "I have reset your router and the lights should turn green.",
                     "Can you read me the model number on the sticker?", "Thank you for holding, I have found the fault."):
            self.assertEqual(ownership.wide(self.agent_says(line)), [], line)

    def test_v2_gate_missed_these_and_the_wide_gate_keeps_what_v2_found(self):
        missed = self.agent_says("Anything wrong down there is Telstra's responsibility, not ours.")
        self.assertEqual(ownership.v2gate(missed), [])
        found = self.agent_says("That is not my department, you need to call another team.")
        self.assertTrue(ownership.v2gate(found) and ownership.wide(found))

    def test_only_agent_lines_are_collected_and_at_most_six(self):
        many = [("C", "It is broken")] + [("A", f"That is not our problem, number {i}") for i in range(10)]
        w = ownership.wide(turns(*many))[0].split("\n")
        self.assertEqual(len(w), 6)
        self.assertTrue(all(x.startswith("Agent: ") for x in w))
        cust = turns(("A", "Hello"), ("C", "This is not your problem to solve, it is the provider's problem, not yours"))
        self.assertEqual(ownership.wide(cust), [])


class ParaphraseGate(unittest.TestCase):
    def test_a_restatement_in_other_words_is_found_when_the_customer_agrees(self):
        c = turns(("C", "My broadband keeps dropping every evening around eight and the router lights turn red for a while"),
                  ("A", "Right, so every evening about eight your broadband drops and the router goes red"), ("C", "Yes exactly"),
                  ("A", "Let me check the line"))
        self.assertEqual(paraphrase.v2cue(c), [])
        self.assertTrue(paraphrase.cue_aff(c))

    def test_an_agreement_after_an_unrelated_question_is_not_a_restatement(self):
        c = turns(("C", "My broadband keeps dropping every evening around eight and the router lights turn red for a while"),
                  ("A", "Can I take your full name and date of birth please for the security check"), ("C", "Yes it is Sam Smith"))
        self.assertEqual(paraphrase.cue_aff(c), [])

    def test_context_window_pairs_the_restatement_with_the_lines_just_before_it(self):
        c = turns(("C", "Hi, I cannot get into my email account at all since this morning, it just says the account is locked"),
                  ("A", "I can help with that, let me pull up the account"), ("C", "Okay thanks"),
                  ("C", "The phone asked me to sign in again yesterday and it would not accept my password"),
                  ("A", "So the phone prompted you yesterday and rejected the password, have I got that right?"))
        old = paraphrase.v2cue(c)[0]
        new = paraphrase.v2cue_ctx(c)
        self.assertNotIn("yesterday", old.split("\nAGENT:")[0])
        self.assertEqual(len(new), 1)
        cust, agent = new[0].split("\nAGENT: ")
        self.assertIn("yesterday", cust)
        self.assertNotIn("Okay thanks", cust)                       # backchannels are skipped
        self.assertTrue(agent.startswith("So the phone prompted you"))

    def test_context_windows_one_per_candidate_capped(self):
        lines = []
        for i in range(5):
            lines += [("C", f"The router light number {i} keeps flashing orange every few minutes today"), ("A", f"So light {i} is flashing, is that right?")]
        w = paraphrase.cue_any_ctx(turns(*lines))
        self.assertEqual(len(w), paraphrase.MAX_CTX_WINDOWS)
        self.assertIn("number 0", w[0])
        self.assertIn("So light 0", w[0])

    def test_context_window_needs_a_customer_line_before_the_candidate(self):
        c = turns(("A", "So just to confirm, you are calling about your broadband?"), ("C", "Yes"))
        self.assertEqual(paraphrase.v2cue_ctx(c), [])


if __name__ == "__main__":
    unittest.main()
