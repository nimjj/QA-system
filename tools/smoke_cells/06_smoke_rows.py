# CELL 6: write smoke.jsonl, 20 hand-written rows (2 per check, plus 2 "replay" rows with soft targets).
# Each row asks the REAL frozen question; the cell checks that. One row has two questions, so 20 rows = 21 questions.
# EXPECT: "wrote 20 rows, 21 questions", "all check rows use the frozen production question", and a small table.
SMOKE_JSONL = r"""{{SMOKE_JSONL}}"""
SMOKE = f"{WORK}/smoke.jsonl"
with open(SMOKE, "w", encoding="utf-8", newline="\n") as f:
    f.write(SMOKE_JSONL)
ROWS = [json.loads(line) for line in SMOKE_JSONL.splitlines() if line.strip()]

for r in ROWS:
    check = r["meta"].get("check")
    if check:
        assert r["questions"]["q"] == CHECKS[check]["question"], f"{r['meta']['id']} does not use the frozen question"
n_q = sum(len(r["questions"]) for r in ROWS)
print(f"wrote {len(ROWS)} rows, {n_q} questions to {SMOKE}")
print("all check rows use the frozen production question")
for r in ROWS:
    label = r["expected"]["q"] if "expected" in r else "gold"
    print(f"  {r['meta']['id']:<16} expected(yes)={label}")
SMOKE_SHA256 = hashlib.sha256(SMOKE_JSONL.encode("utf-8")).hexdigest()
