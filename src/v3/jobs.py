"""In-process job queue with ONE worker thread.

The model can only answer one request at a time (it is one 1.7 GB CPU model behind a lock), so 20 simultaneous requests used to make the last
one wait about five minutes with no timeout and no way to cancel. Here a call becomes a job: it waits in a bounded queue (full queue = a clean
"busy" answer, not a hang), one worker grades jobs in order, and the caller either waits for its result for a limited time or polls later.

A job drops its transcript the moment grading starts, and finished jobs are forgotten after `ttl_seconds`, so personal data does not pile up
in memory. State is in-process: a restart loses queued jobs (a DB job table is the next step if that matters).
"""
import logging
import queue
import threading
import time
import uuid
from typing import Any, Callable, Dict, Optional

log = logging.getLogger("v3.jobs")


class QueueFull(Exception):
    """The waiting line is full; try again later (HTTP 503)."""


class Job:
    def __init__(self, payload: Any, meta: Dict[str, Any]):
        self.id = uuid.uuid4().hex
        self.payload = payload
        self.meta = meta                         # tenant_id, call_id: safe to show, no transcript
        self.status = "queued"                   # queued | running | done | failed | cancelled
        self.created = time.time()
        self.started: Optional[float] = None
        self.finished: Optional[float] = None
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[Dict[str, Any]] = None
        self.done = threading.Event()

    def view(self, position: Optional[int] = None) -> Dict[str, Any]:
        out = {"job_id": self.id, "status": self.status, **self.meta}
        if position is not None:
            out["queue_position"] = position
        if self.started:
            out["waited_seconds"] = round(self.started - self.created, 1)
        if self.finished and self.started:
            out["run_seconds"] = round(self.finished - self.started, 1)
        if self.status == "done":
            out["result"] = self.result
        if self.status == "failed":
            out["error"] = self.error
        return out


class JobQueue:
    def __init__(self, run: Callable[[Any], Dict[str, Any]], error_status: Callable[[BaseException], Optional[int]],
                 max_queue: int = 50, ttl_seconds: float = 3600.0, max_kept: int = 2000, warm: Optional[Callable[[], None]] = None):
        self._run, self._error_status, self._warm = run, error_status, warm
        self._q: "queue.Queue[Job]" = queue.Queue(maxsize=max_queue)
        self._jobs: Dict[str, Job] = {}
        self._lock = threading.Lock()
        self._ttl, self._max_kept = ttl_seconds, max_kept
        self._thread: Optional[threading.Thread] = None
        self.ready = threading.Event()
        self.load_error: Optional[str] = None
        self.completed = self.failed = 0

    # --- lifecycle -------------------------------------------------------------------------------------------------
    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._loop, name="v3-worker", daemon=True)
        self._thread.start()

    def _loop(self) -> None:
        try:
            if self._warm:
                self._warm()                                  # load the model now, so a bad path fails at startup, not on the first call
            self.ready.set()
        except Exception as e:
            self.load_error = f"{type(e).__name__}: {e}"
            log.error("model failed to load: %s", self.load_error)
            self._fail_everything_queued()
            return
        while True:
            job = self._q.get()
            with self._lock:                                  # cancel() takes the same lock, so a job is either cancelled or started
                if job.status == "cancelled":
                    continue
                job.status, job.started = "running", time.time()
                payload, job.payload = job.payload, None      # forget the transcript as soon as it is being graded
            try:
                job.result = self._run(payload)
                job.status = "done"
                self.completed += 1
            except Exception as e:
                code = self._error_status(e)
                job.error = ({"status": code, "detail": str(e)} if code else {"status": 500, "detail": "evaluation failed"})
                if not code:
                    log.exception("job %s failed", job.id)
                job.status = "failed"
                self.failed += 1
            finally:
                payload = None
                job.finished = time.time()
                job.done.set()

    def _fail_everything_queued(self) -> None:
        while True:
            try:
                job = self._q.get_nowait()
            except queue.Empty:
                return
            job.status, job.error, job.finished = "failed", {"status": 503, "detail": "model not available"}, time.time()
            job.payload = None
            job.done.set()

    # --- use -------------------------------------------------------------------------------------------------------
    def submit(self, payload: Any, meta: Optional[Dict[str, Any]] = None) -> Job:
        if self.load_error:
            raise QueueFull("model not available: " + self.load_error)
        job = Job(payload, meta or {})
        try:
            self._q.put_nowait(job)
        except queue.Full:
            raise QueueFull("the waiting line is full")
        with self._lock:
            self._jobs[job.id] = job
            self._forget_old()
        return job

    def get(self, job_id: str) -> Optional[Job]:
        with self._lock:
            return self._jobs.get(job_id)

    def position(self, job: Job) -> Optional[int]:
        """0 when it is next in line; None once it is running or finished."""
        if job.status != "queued":
            return None
        with self._q.mutex:
            waiting = [j for j in self._q.queue if j.status == "queued"]
        return waiting.index(job) if job in waiting else None

    def cancel(self, job: Job) -> bool:
        """Cancel a job that has not started. Returns False if it is already running or finished."""
        with self._lock:
            if job.status != "queued":
                return False
            job.status, job.payload, job.finished = "cancelled", None, time.time()
            job.done.set()
            return True

    def _forget_old(self) -> None:
        now = time.time()
        old = [k for k, j in self._jobs.items() if j.finished and now - j.finished > self._ttl]
        for k in old:
            del self._jobs[k]
        if len(self._jobs) > self._max_kept:
            finished = sorted((j for j in self._jobs.values() if j.finished), key=lambda j: j.finished)
            for j in finished[: len(self._jobs) - self._max_kept]:
                del self._jobs[j.id]

    def stats(self) -> Dict[str, Any]:
        return {"ready": self.ready.is_set(), "load_error": self.load_error, "waiting": self._q.qsize(), "capacity": self._q.maxsize,
                "completed": self.completed, "failed": self.failed}
