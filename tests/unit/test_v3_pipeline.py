import os
import unittest
from unittest import mock

from tests.unit.helpers import call
from src.v3 import pipeline, scoring
from src.v3.normalise import InvalidTranscript, normalise
from src.v3.text import add_question_marks

ALL = ["Branding and Survey Check", "Hold time and Dead Air", "Verified customer", "Personalized the call/ticket appropriately",
       "Empathy & Acknowledgment Statement", "Paraphrasing", "Active listening", "Took ownership of the problem",
       "Build rapport and observed professionalism", "Probing", "Confirmed the issue is resolved"]


def criteria(names=ALL, soft=("Branding and Survey Check", "Empathy & Acknowledgment Statement"), cat_soft="Soft Skills", cat_tech="Technical Knowledge"):
    s = [{"name": n, "deduction_value": 10} for n in names if n in soft]
    t = [{"name": n, "deduction_value": 10} for n in names if n not in soft]
    cats = [{"name": cat_soft, "line_items": s}, {"name": cat_tech, "line_items": t}]
    return {"categories": cats, "category_weights": {cat_soft: 0.5, cat_tech: 0.5}}


CALL = [
    {"speaker": "Agent", "text": "Thank you for calling S-Net, my name is Sam", "start_time_sec": 0},
    {"speaker": "Customer", "text": "My internet is down and I am furious", "start_time_sec": 8, "sentiment_score": -40},
    {"speaker": "Agent", "text": "So you are saying your internet is down and you are very upset about it", "start_time_sec": 11},
    {"speaker": "Customer", "text": "Yes exactly", "start_time_sec": 14, "sentiment_score": -30},
    {"speaker": "Agent", "text": "Can you confirm your PIN", "start_time_sec": 15},
    {"speaker": "Customer", "text": "It is 1234", "start_time_sec": 22, "sentiment_score": -10},
    {"speaker": "Agent", "text": "Thanks Alex. What colour are the lights on the router", "start_time_sec": 30},
    {"speaker": "Customer", "text": "Red", "start_time_sec": 38, "sentiment_score": -15},
    {"speaker": "Agent", "text": "I have reset it, is it working now", "start_time_sec": 50},
    {"speaker": "Customer", "text": "Yes thanks", "start_time_sec": 60, "sentiment_score": 20},
    {"speaker": "Agent", "text": "Thank you for choosing S-Net, goodbye", "start_time_sec": 70},
]


class QuestionMarks(unittest.TestCase):
    def test_bare_questions_get_a_mark(self):
        for t in ("what colour are the lights", "Can you confirm your PIN", "okay so when did it start", "tell me what the error says"):
            self.assertTrue(add_question_marks(t).endswith("?"), t)

    def test_statements_and_punctuated_turns_are_left_alone(self):
        for t in ("I have reset it", "Have a good day", "What is that? I mean the light.", "Thanks. When did it start", "Already a question?", ""):
            self.assertEqual(add_question_marks(t), t)

    def test_no_double_mark(self):
        self.assertEqual(add_question_marks("how are you?"), "how are you?")


class SourceIndex(unittest.TestCase):
    def test_empty_turns_are_dropped_but_the_original_position_is_kept(self):
        raw = [{"speaker": "Agent", "text": "hi", "start_time_sec": 0}, {"speaker": "Agent", "text": "  ", "start_time_sec": 1},
               {"speaker": "Customer", "text": "hello", "start_time_sec": 2}]
        c = normalise(raw)
        self.assertEqual([t.index for t in c.turns], [0, 1])
        self.assertEqual([t.source_index for t in c.turns], [0, 2])


class Pipeline(unittest.TestCase):
    def setUp(self):
        self.asked = []

        def fake(check_key, text, label):
            self.asked.append((check_key, label, text))
            return "PASS"
        self.p_yes = 0.9                                                   # what the stand-in model answers when asked for a probability
        self.asked_p = []
        for p in (mock.patch.object(pipeline.de, "_laya_verdict", side_effect=fake),
                  mock.patch.object(pipeline.de, "predict_yes", side_effect=self.fake_probability),
                  mock.patch.dict(os.environ, {"LAYA_FLOW": "v2"})):       # the production window flow; importing the web app loads .env
            p.start()
            self.addCleanup(p.stop)

    def fake_probability(self, text, questions, label=""):
        self.asked_p.append(label)
        return {"q": self.p_yes}

    def run_call(self, transcript=CALL, crit=None, **kw):
        return pipeline.evaluate_v3(transcript, crit or criteria(), "t1", "Call", kw.get("caller", "Alex"))

    def test_response_shape_matches_v2(self):
        r = self.run_call()
        self.assertEqual(set(r) - {"meta"}, {"final_score", "auto_failed_count", "category_summary", "scorecard", "is_auto_fail", "auto_fail_reason"})
        self.assertEqual(len(r["scorecard"]), len(ALL))
        for e in r["scorecard"]:
            self.assertIn(e["rating"], ("PASS", "FAIL"))
            self.assertTrue({"category", "name", "rating", "coaching"} <= set(e))

    def test_a_clean_call_scores_100_with_a_stubbed_model(self):
        r = self.run_call()
        self.assertEqual(r["final_score"], 100.0, [(e["name"], e["rating"]) for e in r["scorecard"] if e["rating"] == "FAIL"])
        self.assertFalse(r["is_auto_fail"])

    def test_meta_reports_flow_and_cost(self):
        m = self.run_call()["meta"]
        self.assertEqual(m["flow"], "v3")
        self.assertGreater(m["model_rows"], 0)
        self.assertEqual(m["model_rows"], len(self.asked) + len(self.asked_p))
        self.assertTrue(m["sentiment_available"])

    def test_bare_agent_questions_reach_probing(self):
        self.run_call()
        probing = [a for a in self.asked if a[0] == "probing"]
        self.assertEqual(len(probing), 1)
        self.assertIn("?", probing[0][2])

    def test_only_requested_checks_cost_model_rows(self):
        r = self.run_call(crit=criteria(["Branding and Survey Check", "Verified customer"]))
        self.assertEqual(self.asked, [])
        self.assertEqual(r["meta"]["model_rows"], 0)

    def test_tenant_category_names_are_respected(self):
        crit = criteria(cat_soft="Behaviour", cat_tech="Process")
        crit["category_weights"] = {"Behaviour": 0.5, "Process": 0.5}
        bad = [dict(t) for t in CALL]
        bad[0]["text"] = "Hello"                                         # no branding
        r = self.run_call(bad, crit)
        self.assertEqual(r["final_score"], 95.0)                          # 10 off one of two equally weighted categories

    def test_no_criteria_is_refused_not_scored_100(self):
        with self.assertRaises(scoring.NoCriteria):
            self.run_call(crit={"categories": [], "category_weights": {}})

    def test_empty_transcript_is_refused(self):
        with self.assertRaises(InvalidTranscript):
            self.run_call([])

    def test_abuse_zeroes_the_call(self):
        bad = [dict(t) for t in CALL]
        bad[4]["text"] = "Shut up and listen. What colour are the lights"
        r = self.run_call(bad)
        self.assertTrue(r["is_auto_fail"])
        self.assertEqual(r["final_score"], 0.0)

    def test_unknown_item_names_become_a_custom_question_not_a_substring_guess(self):
        crit = criteria(["Branding and Survey Check", "Offered a callback"], soft=("Branding and Survey Check",))
        with mock.patch.object(pipeline.de, "predict_yes", return_value={"q": 0.9}) as py:
            r = self.run_call(crit=crit)
        self.assertEqual(py.call_count, 1)                                # one question, built from the item's own name
        self.assertIn("Offered a callback", py.call_args[0][1]["q"]["instructions"])
        self.assertEqual(self.asked, [])                                  # custom items bypass the built-in check keys
        self.assertEqual(next(e for e in r["scorecard"] if e["name"] == "Offered a callback")["rating"], "PASS")

    def test_evidence_points_to_the_callers_own_turn_numbers(self):
        r = self.run_call()
        v = next(e for e in r["scorecard"] if e["name"] == "Verified customer")
        self.assertEqual(v["rating"], "PASS")
        self.assertEqual(v["evidence_turns"], [4])

    def resolved(self, transcript=CALL):
        r = self.run_call(transcript)
        return next(e for e in r["scorecard"] if e["name"] == "Confirmed the issue is resolved")

    def test_resolved_v3_gate_blends_model_and_customer_mood(self):
        good = self.resolved()
        self.assertEqual(good["rating"], "PASS")
        self.assertIn("customer end mood", good["note"])
        sad_end = [dict(t) for t in CALL]
        sad_end[-2]["sentiment_score"] = -60                              # the customer ends far below how they spoke on average
        sad_end[-4]["sentiment_score"] = -55
        sad_end[-6]["sentiment_score"] = -50
        self.p_yes = 0.6                                                  # and the model is only lukewarm
        self.assertEqual(self.resolved(sad_end)["rating"], "FAIL")

    def test_resolved_without_customer_sentiment_uses_the_model_alone(self):
        flat = [{k: v for k, v in t.items() if k != "sentiment_score"} for t in CALL]
        self.p_yes = 0.9
        r = self.resolved(flat)
        self.assertEqual(r["rating"], "PASS")
        self.assertIn("no usable customer sentiment", r["note"])
        self.p_yes = 0.5
        self.assertEqual(self.resolved(flat)["rating"], "FAIL")           # below the 0.65 cutoff

    def test_the_resolved_gate_can_be_switched_back_to_v2(self):
        from src.v3 import load_config
        cfg = dict(load_config(), gates={"resolved": {"mode": "v2"}})
        with mock.patch.object(pipeline, "load_config", return_value=cfg):
            r = self.run_call()
        self.assertIn("resolved", [a[0] for a in self.asked])
        self.assertEqual(r["meta"]["gates"], {"resolved": "v2"})

    def ownership(self, cfg_gate=None):
        bad = [dict(t) for t in CALL]
        bad[6]["text"] = "Anything wrong on the street cabinet is Openreach's responsibility, not ours. What colour are the lights on the router"
        self.p_yes = 0.9                                                  # the stand-in model says: yes, this agent deflects
        if cfg_gate is None:
            r = self.run_call(bad)
        else:
            from src.v3 import load_config
            cfg = dict(load_config(), gates={"ownership": cfg_gate})
            with mock.patch.object(pipeline, "load_config", return_value=cfg):
                r = self.run_call(bad)
        return next(e for e in r["scorecard"] if e["name"] == "Took ownership of the problem")["rating"]

    def test_ownership_wide_gate_shows_the_model_a_deflection_the_v2_phrases_miss(self):
        self.assertEqual(self.ownership(), "FAIL")
        self.assertEqual(self.ownership({"mode": "v2"}), "PASS")           # v2 opens no window, so the item passes unseen

    def test_null_and_float_times_do_not_crash(self):
        odd = [dict(t) for t in CALL]
        odd[1]["start_time_sec"] = 8.5
        odd[3]["sentiment_score"] = None
        odd[5]["start_time_sec"] = None
        r = self.run_call(odd)
        self.assertEqual(len(r["scorecard"]), len(ALL))


if __name__ == "__main__":
    unittest.main()
