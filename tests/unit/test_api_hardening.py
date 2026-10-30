import os
import unittest
from unittest import mock

from tests.unit.helpers import call  # noqa: F401  (puts the repo root on sys.path)

try:
    from fastapi.testclient import TestClient
    from src.api import web_app
except Exception:                                                         # pragma: no cover
    web_app = None


@unittest.skipIf(web_app is None, "web app cannot be imported here")
class SafeBody(unittest.TestCase):
    def test_transcript_text_and_names_never_reach_the_log(self):
        body = {"transcript": [{"speaker": "Agent", "text": "my card number is 4111"}, {"speaker": "Customer", "text": "ok"}],
                "customer_name": "Alex Smith", "tenant_id": "t1"}
        safe = web_app._safe_body(body)
        self.assertNotIn("4111", str(safe))
        self.assertNotIn("Alex", str(safe))
        self.assertEqual(safe["transcript"], {"turns": 2, "chars": 22 + 2})
        self.assertEqual(safe["tenant_id"], "t1")
        self.assertIn("4111", str(body))                                  # the caller's own dict is untouched

    def test_text_block_transcripts_and_odd_bodies(self):
        self.assertEqual(web_app._safe_body({"transcript": "Agent: hi"})["transcript"], {"chars": 9})
        self.assertEqual(web_app._safe_body("not json at all"), {"omitted_chars": 15})
        self.assertEqual(web_app._safe_body({}), {})

    def test_debug_switch_keeps_full_bodies(self):
        with mock.patch.object(web_app, "LOG_REQUEST_BODIES", True):
            self.assertEqual(web_app._safe_body({"customer_name": "Alex"}), {"customer_name": "Alex"})


@unittest.skipIf(web_app is None, "web app cannot be imported here")
class Guards(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(web_app.app)

    def test_oversized_body_is_413_before_it_is_read(self):
        with mock.patch.object(web_app, "MAX_REQUEST_BYTES", 1000):
            r = self.client.post("/api/evaluate", content=b"x" * 5000, headers={"content-type": "application/json"})
        self.assertEqual(r.status_code, 413)

    def test_api_key_is_enforced_only_when_configured(self):
        with mock.patch.dict(os.environ, {"QA_API_KEY": "s3cret"}):
            self.assertEqual(self.client.get("/api/tenants").status_code, 401)
            self.assertEqual(self.client.get("/api/tenants", headers={"x-api-key": "wrong"}).status_code, 401)
            self.assertEqual(self.client.get("/health").status_code, 200)             # liveness stays open
            with mock.patch.object(web_app, "get_all_tenants", return_value=[]):
                self.assertEqual(self.client.get("/api/tenants", headers={"x-api-key": "s3cret"}).status_code, 200)
        with mock.patch.object(web_app, "get_all_tenants", return_value=[]):
            self.assertEqual(self.client.get("/api/tenants").status_code, 200)         # unset: open as before

    def test_ready_reports_a_missing_database_as_503(self):
        with mock.patch.object(web_app, "get_all_tenants", side_effect=RuntimeError("down")):
            r = self.client.get("/ready")
        self.assertEqual(r.status_code, 503)
        self.assertEqual(r.json()["database"], "unreachable")
        with mock.patch.object(web_app, "get_all_tenants", return_value=[]):
            self.assertEqual(self.client.get("/ready").status_code, 200)


if __name__ == "__main__":
    unittest.main()
