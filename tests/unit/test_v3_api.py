import os
import threading
import unittest
from unittest import mock

from tests.unit.helpers import call  # noqa: F401  (puts the repo root on sys.path)
from tests.unit.test_v3_pipeline import ALL, CALL, criteria

try:
    from fastapi.testclient import TestClient
    from src.api import web_app
    from src.v3 import pipeline
    from src.v3.jobs import JobQueue
except Exception as e:                                                   # pragma: no cover
    web_app = None


@unittest.skipIf(web_app is None, "web app cannot be imported here")
class EvaluateEndpoint(unittest.TestCase):
    """Flow v3 through the real API, with the model stubbed (no weights are loaded)."""

    def setUp(self):
        self.client = TestClient(web_app.app)
        for p in (mock.patch.dict(os.environ, {"LAYA_FLOW": "v3"}),
                  mock.patch.object(web_app, "_model_ready", True),
                  mock.patch.object(pipeline.de, "_laya_verdict", return_value="PASS"),
                  mock.patch.object(pipeline.de, "predict_yes", return_value={"q": 0.9})):
            p.start()
            self.addCleanup(p.stop)

    def body(self, transcript, crit=None):
        return {"transcript": transcript, "criteria_data": crit or criteria(), "tenant_id": "t1", "customer_name": "Alex"}

    def post(self, transcript, crit=None):
        return self.client.post("/api/evaluate", json=self.body(transcript, crit))

    def test_v3_response_keeps_the_v2_envelope(self):
        r = self.post(CALL)
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertEqual(body["status"], "completed")
        self.assertEqual(len(body["result"]["scorecard"]), len(ALL))
        self.assertEqual(body["result"]["meta"]["flow"], "v3")

    def test_fractional_and_null_values_are_accepted(self):
        odd = [dict(t) for t in CALL]
        odd[1]["start_time_sec"] = 8.5
        odd[3]["sentiment_score"] = None
        odd[5]["start_time_sec"] = None
        self.assertEqual(self.post(odd).status_code, 200)

    def test_bad_input_is_refused(self):
        self.assertEqual(self.post([]).status_code, 422)
        big = [{"speaker": "Agent", "text": "x", "start_time_sec": i} for i in range(1600)]
        self.assertEqual(self.post(big).status_code, 413)

    def test_v3_uses_the_built_in_criteria_and_never_the_database(self):
        boom = RuntimeError("the database must not be used in flow v3")
        with mock.patch.object(web_app, "get_active_criteria_for_evaluation", side_effect=boom), \
                mock.patch.object(web_app, "get_all_tenants", side_effect=boom):
            r = self.client.post("/api/evaluate", json={"transcript": CALL, "tenant_id": "anything"})       # no criteria_data at all
            self.assertEqual(r.status_code, 200, r.text)
            self.assertEqual([e["name"] for e in r.json()["result"]["scorecard"]], [
                "Branding and Survey Check", "Hold time and Dead Air", "Personalized the call/ticket appropriately",
                "Empathy & Acknowledgment Statement", "Build rapport and observed professionalism", "Paraphrasing", "Verified customer",
                "Probing", "Took ownership of the problem", "Active listening", "Confirmed the issue is resolved"])
            self.assertEqual(self.client.get("/ready").status_code, 200)

    def test_criteria_sent_in_the_request_are_ignored(self):
        only_two = criteria(["Branding and Survey Check", "Verified customer"])
        r = self.post(CALL, only_two)
        self.assertEqual(len(r.json()["result"]["scorecard"]), len(ALL))

    def test_ready_reports_model_status(self):
        self.assertEqual(self.client.get("/ready").status_code, 200)
        with mock.patch.object(web_app, "_model_ready", False):
            r = self.client.get("/ready")
            self.assertEqual(r.status_code, 503)
            self.assertEqual(r.json()["status"], "model loading")


if __name__ == "__main__":
    unittest.main()
