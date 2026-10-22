import threading
import unittest

from tests.unit.helpers import call  # noqa: F401  (puts the repo root on sys.path)
from src.v3.jobs import JobQueue, QueueFull


class Bad(ValueError):
    pass


def status_of(exc):
    return 422 if isinstance(exc, Bad) else None


def wait_until_running(job):
    while job.status == "queued":
        threading.Event().wait(0.005)


class Queue(unittest.TestCase):
    def make(self, run, **kw):
        q = JobQueue(run, status_of, **kw)
        q.start()
        self.assertTrue(q.ready.wait(5))
        return q

    def test_jobs_run_in_order_and_results_come_back(self):
        order = []
        q = self.make(lambda p: order.append(p) or {"echo": p})
        jobs = [q.submit(i, {"call_id": f"c{i}"}) for i in range(5)]
        for j in jobs:
            self.assertTrue(j.done.wait(5))
        self.assertEqual(order, [0, 1, 2, 3, 4])
        self.assertEqual(jobs[2].view()["result"], {"echo": 2})
        self.assertEqual(jobs[2].view()["call_id"], "c2")

    def test_a_full_line_says_busy_instead_of_hanging(self):
        gate = threading.Event()
        q = self.make(lambda p: gate.wait(5) or {}, max_queue=2)
        wait_until_running(q.submit("a"))                       # taken by the worker, which then blocks on the gate
        q.submit("b")
        q.submit("c")
        with self.assertRaises(QueueFull):
            q.submit("d")
        gate.set()

    def test_position_counts_only_jobs_ahead(self):
        gate = threading.Event()
        q = self.make(lambda p: gate.wait(5) or {})
        first = q.submit("a")
        wait_until_running(first)
        b, c = q.submit("b"), q.submit("c")
        self.assertEqual((q.position(b), q.position(c), q.position(first)), (0, 1, None))
        gate.set()

    def test_cancelled_job_never_runs(self):
        gate, ran = threading.Event(), []
        q = self.make(lambda p: ran.append(p) or gate.wait(5) or {})
        first = q.submit("a")
        wait_until_running(first)
        b = q.submit("b")
        self.assertTrue(q.cancel(b))
        self.assertFalse(q.cancel(first))                      # already running
        gate.set()
        self.assertTrue(first.done.wait(5))
        self.assertTrue(q.submit("c").done.wait(5))
        self.assertEqual(ran, ["a", "c"])

    def test_known_errors_keep_their_status_and_unknown_ones_are_hidden(self):
        def run(p):
            if p == "bad":
                raise Bad("the transcript has no turns")
            raise RuntimeError("secret internals: C:\\path\\to\\weights")
        q = self.make(run)
        bad, boom = q.submit("bad"), q.submit("boom")
        self.assertTrue(bad.done.wait(5) and boom.done.wait(5))
        self.assertEqual(bad.view()["error"], {"status": 422, "detail": "the transcript has no turns"})
        self.assertEqual(boom.view()["error"], {"status": 500, "detail": "evaluation failed"})
        self.assertEqual(q.stats()["failed"], 2)
        self.assertTrue(q.submit("bad").done.wait(5))          # the worker survived both failures

    def test_the_transcript_is_forgotten_once_grading_starts(self):
        seen = []
        q = self.make(lambda p: seen.append(p) or {})
        j = q.submit({"transcript": "secret words"})
        j.done.wait(5)
        self.assertIsNone(j.payload)
        self.assertEqual(seen, [{"transcript": "secret words"}])
        self.assertNotIn("secret", str(j.view()))

    def test_a_model_that_fails_to_load_fails_fast_and_refuses_work(self):
        def warm():
            raise FileNotFoundError("LAYA_CHECKPOINT is not a folder")
        q = JobQueue(lambda p: {}, status_of, warm=warm)
        q.start()
        for _ in range(500):
            if q.load_error:
                break
            threading.Event().wait(0.01)
        self.assertIn("LAYA_CHECKPOINT", q.load_error)
        self.assertFalse(q.ready.is_set())
        with self.assertRaises(QueueFull):
            q.submit("x")

    def test_finished_jobs_are_forgotten_after_the_ttl(self):
        q = self.make(lambda p: {}, ttl_seconds=0.05)
        j = q.submit("a")
        j.done.wait(5)
        threading.Event().wait(0.1)
        q.submit("b")                                           # any submit sweeps old jobs
        self.assertIsNone(q.get(j.id))


if __name__ == "__main__":
    unittest.main()
