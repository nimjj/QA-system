# CELL 9a: helpers for safe copying to Drive and for running laya-train with live output.
# Also writes laya_train_cuda.py: laya 0.4.0's trainer crashes on a GPU ("tensors on the same device ...") because it
# evaluates before moving the model to the GPU. This wrapper does that move first; the package itself is not edited.
# EXPECT: no output other than "helpers ready".
LAUNCHER = f"{WORK}/laya_train_cuda.py"
with open(LAUNCHER, "w", encoding="utf-8", newline="\n") as f:
    f.write(r'''{{LAUNCHER_PY}}''')

EPOCH_RE = re.compile(r"epoch (\d+)/(\d+) mean loss")


class SourceChanged(Exception):
    pass


class CopyMismatch(Exception):
    pass


def tree_stats(path, ignore=()):
    """Sorted (relative path, size, mtime_ns) for every file under path. Files that vanish mid-scan are skipped."""
    out = []
    for dp, dns, fns in os.walk(path):
        if dp == path:
            dns[:] = [d for d in dns if d not in ignore]
        for fn in fns:
            p = os.path.join(dp, fn)
            try:
                st = os.stat(p)
            except FileNotFoundError:
                continue
            out.append((os.path.relpath(p, path), st.st_size, st.st_mtime_ns))
    return sorted(out)


def wait_stable(path, quiet_s=30, poll_s=3, timeout_s=1800, newer_than=None, ignore=()):
    """Return once no file under path changed size or mtime for quiet_s seconds.

    With newer_than (a time.time() value), also require that something was written at or after it, so an
    older, already-stable copy is never mistaken for the checkpoint that is about to be written.
    """
    t0, last, since = time.time(), None, time.time()
    while time.time() - t0 < timeout_s:
        snap = tree_stats(path, ignore)
        if snap != last:
            last, since = snap, time.time()
        fresh = newer_than is None or (snap and max(m for _, _, m in snap) / 1e9 >= newer_than)
        if snap and fresh and time.time() - since >= quiet_s:
            return snap
        time.sleep(poll_s)
    raise TimeoutError(f"{path} was not stable within {timeout_s}s")


def copy_verified(src, dst, tag, ignore=()):
    """Copy src to a temp folder next to dst, verify it, then rename it into place.

    Raises SourceChanged if src changed while copying, CopyMismatch if the copy differs. dst is only
    replaced after both checks pass, so a half-written copy never sits under the final name.
    Returns (number of files, total bytes).
    """
    tmp = f"{dst}.tmp-{tag}"
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    before = tree_stats(src, ignore)
    shutil.copytree(src, tmp, ignore=shutil.ignore_patterns(*ignore) if ignore else None)
    names_sizes = lambda stats: [(r, z) for r, z, _ in stats]
    if names_sizes(tree_stats(tmp)) != names_sizes(before):
        shutil.rmtree(tmp, ignore_errors=True)
        raise CopyMismatch(f"{tmp} differs from {src}")
    if tree_stats(src, ignore) != before:
        shutil.rmtree(tmp, ignore_errors=True)
        raise SourceChanged(src)
    old = None
    if os.path.exists(dst):
        old = f"{dst}.old-{tag}"
        os.rename(dst, old)
    os.rename(tmp, dst)
    if old:
        shutil.rmtree(old, ignore_errors=True)
    return len(before), sum(z for _, z, _ in before)


class CkptWatcher:
    """Copies src (checkpoint_latest/) to Drive each time an epoch finishes AND the folder has stopped changing.

    laya-train prints the "epoch N/M mean loss" line BEFORE it writes the checkpoint, so the line alone is
    not enough: after it, wait until nothing was written for quiet_s seconds (and something was written
    after the line), copy to a temp folder on Drive, verify, rename. finish() does one last pass after the
    process exits, because laya-train rewrites the config after calibration.
    Messages are queued and printed by the notebook's main thread (flush), never from this thread.
    """

    def __init__(self, src, dst, quiet_s=30):
        self.src, self.dst, self.quiet_s = src, dst, quiet_s
        self.work, self.msgs = queue.Queue(), queue.Queue()
        self.copies, self.errors = [], []
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def say(self, text):
        self.msgs.put(f"[watcher {time.strftime('%H:%M:%S')}] {text}")

    def feed(self, item):
        t, line = item
        m = EPOCH_RE.search(line)
        if m:
            self.work.put(("epoch", int(m.group(1)), t))

    def finish(self):
        self.work.put(("final", 0, time.time()))

    def stop(self):
        """Training failed: end the thread without waiting for a checkpoint that may never come."""
        self.work.put(("stop", 0, time.time()))

    def flush(self):
        while not self.msgs.empty():
            print(self.msgs.get())

    def _loop(self):
        while True:
            kind, n, t = self.work.get()
            if kind == "stop":
                self.say("training failed, nothing more to copy")
                return
            if kind == "final" and not os.path.isdir(self.src):
                self.say("no checkpoint_latest was written, nothing to copy")
                return
            tag = f"epoch{n}" if kind == "epoch" else "final"
            quiet = self.quiet_s if kind == "epoch" else 10
            try:
                for attempt in range(1, 4):
                    wait_stable(self.src, quiet_s=quiet, newer_than=(t - 2) if kind == "epoch" else None)
                    try:
                        files, size = copy_verified(self.src, self.dst, tag)
                    except SourceChanged:
                        self.say(f"{tag}: folder changed while copying, retry {attempt}/3")
                        continue
                    self.say(f"{tag}: quiet for {quiet}s -> copied to tmp -> verified {files} files / "
                             f"{size / 1e6:.0f} MB -> renamed to {os.path.basename(self.dst)}")
                    self.copies.append((tag, files, size))
                    break
                else:
                    raise RuntimeError(f"{tag}: source kept changing")
            except Exception as e:  # reported by the notebook; never kills training
                self.errors.append(f"{tag}: {e!r}")
                self.say(f"ERROR {tag}: {e!r}")
            if kind == "final":
                return


def run_logged(cmd, log_path, on_item=None):
    """Run cmd, echo its output live, save it to log_path. on_item((time, line)) sees every line; on_item(None) is a tick.

    Returns (return code, [(time, line), ...]).
    """
    q, events = queue.Queue(), []
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    def reader():
        for line in proc.stdout:
            q.put((time.time(), line.rstrip("\n")))
        q.put(None)

    threading.Thread(target=reader, daemon=True).start()
    with open(log_path, "w", encoding="utf-8") as log:
        while True:
            try:
                item = q.get(timeout=1)
            except queue.Empty:
                if on_item:
                    on_item(None)
                continue
            if item is None:
                break
            events.append(item)
            log.write(item[1] + "\n")
            log.flush()
            print(item[1])
            if on_item:
                on_item(item)
    return proc.wait(), events


print("helpers ready")
