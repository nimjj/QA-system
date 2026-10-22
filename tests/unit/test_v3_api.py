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
    """Flow v3 through the real API and job queue, with the model stubbed (no weights are loaded)."""

    def setUp(self):
        self.client = TestClient(web_app.app)
        self.gate = threading.Event()
        self.gate.set()
        self.slow = False

        def run(p):
            if self.slow:
                self.gate.wait(10)
            return web_app._run_job(p)
        self.queue = JobQueue(run, web_app._error_status, max_queue=2)
        self.queue.start()
        for p in (mock.patch.dict(os.environ, {"LAYA_FLOW": "v3"}), mock.patch.object(web_app, "_jobs", self.queue),
                  mock.patch.object(pipeline.de, "_laya_verdict", return_value="PASS"),
                  mock.patch.object(pipeline.de, "predict_yes", return_value={"q": 0.9})):
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self.gate.set)

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

    def test_bad_input_is_refused_before_it_takes_a_place_in_line(self):
        self.assertEqual(self.post([]).status_code, 422)
        big = [{"speaker": "Agent", "text": "x", "start_time_sec": i} for i in range(1600)]
        self.assertEqual(self.post(big).status_code, 413)
        self.assertEqual(self.queue.stats()["completed"] + self.queue.stats()["failed"] + self.queue.stats()["waiting"], 0)

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

    def test_submit_then_poll(self):
        r = self.client.post("/api/jobs", json=self.body(CALL))
        self.assertEqual(r.status_code, 202, r.text)
        job_id = r.json()["job_id"]
        self.queue.get(job_id).done.wait(5)
        got = self.client.get(f"/api/jobs/{job_id}").json()
        self.assertEqual(got["status"], "done")
        self.assertEqual(got["tenant_id"], "t1")
        self.assertEqual(len(got["result"]["scorecard"]), len(ALL))
        self.assertEqual(self.client.get("/api/jobs/nope").status_code, 404)

    def test_a_slow_model_gives_503_with_a_job_id_to_poll(self):
        self.slow, self.gate = True, threading.Event()
        with mock.patch.dict(os.environ, {"EVALUATE_TIMEOUT_SEC": "0.2"}):
            r = self.post(CALL)
        self.assertEqual(r.status_code, 503)
        self.assertEqual(r.headers["retry-after"], "30")
        job_id = r.json()["detail"]["job_id"]
        self.gate.set()
        self.queue.get(job_id).done.wait(5)
        self.assertEqual(self.client.get(f"/api/jobs/{job_id}").json()["status"], "done")

    def test_a_full_line_gives_503_not_a_hang(self):
        self.slow, self.gate = True, threading.Event()
        ids = []
        for _ in range(3):                                               # one running + two waiting
            r = self.client.post("/api/jobs", json=self.body(CALL))
            self.assertEqual(r.status_code, 202, r.text)
            ids.append(r.json()["job_id"])
        r = self.client.post("/api/jobs", json=self.body(CALL))
        self.assertEqual(r.status_code, 503)
        self.assertIn("Retry-After", r.headers)
        self.gate.set()

    def test_ready_waits_for_the_model(self):
        self.assertEqual(self.client.get("/ready").status_code, 200)
        self.queue.ready.clear()
        r = self.client.get("/ready")
        self.assertEqual(r.status_code, 503)
        self.assertEqual(r.json()["status"], "model loading")

    def test_the_job_endpoints_are_off_in_the_old_flow(self):
        with mock.patch.dict(os.environ, {"LAYA_FLOW": "v2"}):
            self.assertEqual(self.client.post("/api/jobs", json=self.body(CALL)).status_code, 404)


if __name__ == "__main__":
    unittest.main()
