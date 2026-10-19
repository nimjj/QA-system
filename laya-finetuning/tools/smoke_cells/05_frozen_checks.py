# CELL 5: the real production questions, frozen from qa-analysis LAYA_CHECKS (tools/export_checks.py).
# EXPECT: "checks sha OK: ac9a5f3c019a..." and "9 questions" followed by the check names.
FROZEN = json.loads(r"""{{FROZEN_JSON}}""")


def canonical_sha(obj):
    text = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


assert canonical_sha(FROZEN["frozen"]) == FROZEN["sha256"], "frozen checks were altered"
CHECKS = FROZEN["frozen"]["checks"]
print("checks sha OK:", FROZEN["sha256"][:12] + "...", "| from qa-analysis commit", FROZEN["qa_analysis_commit"][:10])
print(len(CHECKS), "questions:", ", ".join(CHECKS))
