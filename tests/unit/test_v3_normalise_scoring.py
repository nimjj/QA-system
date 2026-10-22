import unittest

from tests.unit.helpers import call
from src.v3.normalise import InvalidTranscript, TranscriptTooLarge, classify_role, normalise, parse_seconds
from src.v3.scoring import NoCriteria, score


class Seconds(unittest.TestCase):
    def test_formats(self):
        self.assertEqual(parse_seconds(75), 75.0)
        self.assertEqual(parse_seconds(12.5), 12.5)
        self.assertEqual(parse_seconds("1:15"), 75.0)
        self.assertEqual(parse_seconds("[01:15]"), 75.0)
        self.assertEqual(parse_seconds("[01:05:30]"), 3930.0)      # v2 read this as 65 s
        self.assertIsNone(parse_seconds(None))
        self.assertIsNone(parse_seconds("soon"))
        self.assertIsNone(parse_seconds(-3))
        self.assertIsNone(parse_seconds(float("nan")))


class Roles(unittest.TestCase):
    def test_labels(self):
        for label, role in (("Agent", "agent"), ("Rep", "agent"), ("Agent 2", "agent"), ("Rep-3", "agent"), ("Specialist", "agent"),
                            ("Customer", "customer"), ("Client", "customer"), ("Caller", "customer"), ("Customer (Mr Smith)", "customer"),
                            ("IVR", "other"), ("Bot", "other"), ("System", "other"), ("Speaker 1", "other"), ("", "other")):
            self.assertEqual(classify_role(label), role, label)


class Normalise(unittest.TestCase):
    def test_null_float_and_missing_times_do_not_crash(self):
        c = normalise([{"speaker": "Agent", "text": "hello there", "start_time_sec": None},
                       {"speaker": "Customer", "text": "hi", "start_time_sec": 12.5, "sentiment_score": None},
                       {"speaker": "Agent", "text": "how can I help", "start_time": "[00:20]"}])
        self.assertEqual([t.start for t in c.turns][1:], [12.5, 20.0])
        self.assertIsNone(c.turns[1].sentiment)
        self.assertFalse(c.sentiment_available)

    def test_end_time_is_kept_when_given_and_estimated_when_not(self):
        c = normalise([{"speaker": "Agent", "text": "one two three four five", "start_time_sec": 0, "end_time": "[00:30]"},
                       {"speaker": "Customer", "text": "ok", "start_time_sec": 31}])
        self.assertEqual(c.turns[0].end, 30.0)
        self.assertFalse(c.turns[0].end_estimated)
        self.assertTrue(c.turns[1].end_estimated)

    def test_agents_never_carry_sentiment(self):
        c = normalise([{"speaker": "Agent", "text": "hello", "start_time_sec": 0, "sentiment_score": 12.0},
                       {"speaker": "Customer", "text": "hi", "start_time_sec": 5, "sentiment_score": -30.0}] * 3)
        self.assertTrue(all(t.sentiment is None for t in c.turns if t.role == "agent"))
        self.assertTrue(c.sentiment_available)

    def test_all_zero_sentiment_is_reported_as_unavailable(self):
        c = normalise([{"speaker": "Customer", "text": "hi", "start_time_sec": i * 5, "sentiment_score": 0.0} for i in range(6)])
        self.assertFalse(c.sentiment_available)

    def test_string_transcript(self):
        c = normalise("[00:00] Agent: Hello there. [00:07] Customer: My internet is down\n[00:15] Rep: Let me look")
        self.assertEqual([(t.role, t.start) for t in c.turns], [("agent", 0.0), ("customer", 7.0), ("agent", 15.0)])

    def test_limits_and_bad_shapes(self):
        with self.assertRaises(TranscriptTooLarge):
            normalise([{"speaker": "Agent", "text": "x", "start_time_sec": i} for i in range(1501)])
        with self.assertRaises(TranscriptTooLarge):
            normalise([{"speaker": "Agent", "text": "x" * 4001, "start_time_sec": 0}])
        with self.assertRaises(InvalidTranscript):
            normalise([])
        with self.assertRaises(InvalidTranscript):
            normalise("   ")
        with self.assertRaises(InvalidTranscript):
            normalise(["not a turn"])
        with self.assertRaises(InvalidTranscript):
            normalise({"speaker": "Agent"})

    def test_unknown_speaker_is_other_and_flagged_when_no_agent(self):
        c = normalise([{"speaker": "Speaker 1", "text": "hello", "start_time_sec": 0}])
        self.assertEqual(c.turns[0].role, "other")
        self.assertTrue(any("no agent" in w for w in c.warnings))


CRITERIA = {"category_weights": {"Customer Experience": 0.4, "Compliance": 0.6},
            "categories": [{"name": "Customer Experience", "line_items": [{"name": "Branding and Survey Check", "deduction_value": 15},
                                                                           {"name": "Empathy & Acknowledgment Statement", "deduction_value": 35}]},
                           {"name": "Compliance", "line_items": [{"name": "Verified customer", "deduction_value": 25}]}]}


class Scoring(unittest.TestCase):
    def test_tenant_with_other_category_names_is_still_penalised(self):
        # v2 returned 100.0 here because the rating carried the hard-coded categories "Soft Skills"/"Technical Knowledge"
        ratings = [{"name": "Branding and Survey Check", "rating": "FAIL", "category": "Soft Skills"},
                   {"name": "Verified customer", "rating": "FAIL", "category": "Technical Knowledge"},
                   {"name": "Empathy & Acknowledgment Statement", "rating": "PASS"}]
        cats, final = score(ratings, CRITERIA)
        self.assertEqual(cats, {"Customer Experience": 85.0, "Compliance": 75.0})
        self.assertEqual(final, round(0.4 * 85 + 0.6 * 75, 1))

    def test_reference_tenant_numbers_match_v2(self):
        ref = {"category_weights": {"Soft Skills": 0.333, "Technical Knowledge": 0.667},
               "categories": [{"name": "Soft Skills", "line_items": [{"name": "Branding and Survey Check", "deduction_value": 15},
                                                                      {"name": "Empathy & Acknowledgment Statement", "deduction_value": 35}]},
                              {"name": "Technical Knowledge", "line_items": [{"name": "Active listening", "deduction_value": 10}]}]}
        self.assertEqual(score([{"name": "Branding and Survey Check", "rating": "FAIL"}, {"name": "Active listening", "rating": "FAIL"},
                                {"name": "Empathy & Acknowledgment Statement", "rating": "PASS"}], ref)[1], 88.3)

    def test_no_criteria_is_an_error_not_a_perfect_score(self):
        with self.assertRaises(NoCriteria):
            score([], {"categories": []})
        with self.assertRaises(NoCriteria):
            score([], {})

    def test_bad_deductions_and_weights_are_handled(self):
        crit = {"category_weights": {"A": 0, "B": 0}, "categories": [{"name": "A", "line_items": [{"name": "x", "deduction_value": -50}]},
                                                                   {"name": "B", "line_items": [{"name": "y", "deduction_value": None}]}]}
        cats, final = score([{"name": "x", "rating": "FAIL"}, {"name": "y", "rating": "FAIL"}], crit)
        self.assertEqual(cats, {"A": 100.0, "B": 90.0})          # negative deduction counts as 0, missing as the default 10
        self.assertEqual(final, 95.0)                              # zero weights fall back to an equal split

    def test_item_names_containing_solution_are_scored(self):
        crit = {"categories": [{"name": "A", "line_items": [{"name": "Offered a solution", "deduction_value": 20}]}]}
        self.assertEqual(score([{"name": "Offered a solution", "rating": "FAIL"}], crit)[1], 80.0)

    def test_auto_fail_zeroes_everything(self):
        self.assertEqual(score([], CRITERIA, is_auto_fail=True)[1], 0.0)


if __name__ == "__main__":
    unittest.main()
