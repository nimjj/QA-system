# CELL 9b: TIMING RUN (nothing from it is kept). ~320 dummy rows padded to realistic lengths, 2 epochs,
# the real settings (micro-batch 8 x grad-accum 8). Labels are random: only the speed matters.
# It replaces the "1.5-2.5 h" guess for the full run with a measured number.
# EXPECT (about 3-8 min): "mean state tokens ~...", the epoch lines, then
#   "seconds per epoch: epoch 1 = ..., epoch 2 = ... (epoch 2 includes the epoch-1 checkpoint save)"
#   "estimate for 3,400 rows x 4 epochs: about X.X h" and a TIMING dict.
import random

import laya.common as lc
import laya.train as lt
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained(f"{BASE}/tokenizer")
rng = random.Random(0)
FILLER = [
    "Agent: Thanks for bearing with me, I'm just pulling up the notes on your line now.",
    "Customer: No problem, take your time, I'm at my desk anyway.",
    "Agent: I can see the last technician visit was logged on the ninth, does that sound right?",
    "Customer: Yes, he came out in the afternoon and swapped the cable at the wall.",
    "Agent: Great, that helps. I'm checking whether the signal level changed after that visit.",
    "Customer: It was fine for a few days after he left and then it started dropping again.",
    "Agent: Understood. Let me run a quick line test from here, it takes about a minute.",
    "Customer: Sure, go ahead. The laptop is on the same Wi-Fi if you need it.",
    "Agent: The test shows some noise on the line in the evening hours, nothing at midday.",
    "Customer: That matches what I've seen, it's always worst after dinner.",
    "Agent: I'll note that on the ticket so the next team sees it without asking you again.",
    "Customer: Good, I really don't want to repeat all of this a third time.",
]
bases = [r for r in ROWS if "expected" in r]          # the 18 check rows


def padded(state, target):
    s = state
    for _ in range(60):
        if len(tok(s, add_special_tokens=False)["input_ids"]) >= target:
            break
        s += "\n" + rng.choice(FILLER)
    return s


timing_rows, lengths = [], []
for i in range(320):
    b = bases[i % len(bases)]
    q = b["questions"]["q"]
    room = lc.state_room(tok, lt.to_internal("q", q), 512, 192)      # state tokens that fit in the window
    state = padded(b["state"], int(room * rng.uniform(0.6, 0.97)))
    lengths.append(len(tok(state, add_special_tokens=False)["input_ids"]))
    timing_rows.append({"state": state, "questions": {"q": q}, "expected": {"q": rng.random() < 0.5}})
TIMING_DATA = f"{WORK}/timing.jsonl"
with open(TIMING_DATA, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(json.dumps(r, ensure_ascii=False) for r in timing_rows) + "\n")
print(f"320 rows | state tokens: mean {sum(lengths) / len(lengths):.0f}, min {min(lengths)}, max {max(lengths)} (window room about {room})")

T_OUT = f"{WORK}/timing-ckpt"
shutil.rmtree(T_OUT, ignore_errors=True)
t_cmd = [sys.executable, "-u", LAUNCHER, "--data", TIMING_DATA, "--base", BASE, "--out", T_OUT,
         "--loss", "soft-ce", "--epochs", "2", "--micro-batch", "8", "--grad-accum", "8", "--seed", "0",
         "--max-len", "512", "--head-max-len", "192"]
t0 = time.time()
rc, ev = run_logged(t_cmd, f"{WORK}/timing_train.log")
wall = time.time() - t0
assert rc == 0, "timing run failed: paste the output"

t_start = next(t for t, l in ev if l.startswith("train items"))
n_train = int(re.search(r"train items (\d+)", next(l for t, l in ev if l.startswith("train items"))).group(1))
t_e = [t for t, l in ev if EPOCH_RE.search(l)]
ep1, ep2 = t_e[0] - t_start, t_e[1] - t_e[0]
overhead = wall - ep1 - ep2
est_h = (ep2 / n_train * 0.9 * 3400 * 4 + overhead) / 3600
TIMING = {"rows": 320, "train_items": n_train, "mean_state_tokens": round(sum(lengths) / len(lengths)),
          "epoch1_s": round(ep1), "epoch2_s": round(ep2), "other_s": round(overhead),
          "est_hours_3400rows_4epochs": round(est_h, 2)}
print(f"seconds per epoch: epoch 1 = {ep1:.0f}, epoch 2 = {ep2:.0f} (epoch 2 includes the epoch-1 checkpoint save)")
print(f"load + calibration + final save = {overhead:.0f}s; items per second in epoch 2: {n_train / ep2:.1f}")
print(f"estimate for 3,400 rows x 4 epochs: about {est_h:.1f} h  (assumes similar row length; longer rows take longer)")
print("TIMING =", TIMING)
shutil.rmtree(T_OUT, ignore_errors=True)
