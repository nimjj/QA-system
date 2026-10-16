"""Assemble 00_smoke_test.ipynb from tools/smoke_cells/*.py|md.

The cells live as small files so they can be read and diffed. This script glues them into a notebook and
embeds two data blobs, so the notebook is self-contained on Colab:
    {{FROZEN_JSON}}  data/frozen/checks_frozen.json  (the production questions, from tools/export_checks.py)
    {{SMOKE_JSONL}}  the 20 smoke rows built by tools/smoke_rows.py from those questions
    {{LAUNCHER_PY}}  tools/laya_train_cuda.py (laya-train with the GPU fix)

Usage (any Python 3):
    python tools/build_smoke_notebook.py            # writes 00_smoke_test.ipynb
    python tools/build_smoke_notebook.py --check    # exit 1 if the notebook on disk is out of date
"""
import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import smoke_rows  # noqa: E402


def lines(text):
    parts = text.split("\n")
    return [p + "\n" for p in parts[:-1]] + ([parts[-1]] if parts[-1] else [])


def build():
    with open(os.path.join(REPO, "data", "frozen", "checks_frozen.json"), encoding="utf-8") as f:
        frozen_text = f.read().rstrip("\n")
    frozen = json.loads(frozen_text)
    smoke_text = smoke_rows.to_jsonl(smoke_rows.build_rows(frozen))
    with open(os.path.join(HERE, "laya_train_cuda.py"), encoding="utf-8") as f:
        launcher_text = f.read().rstrip("\n") + "\n"
    assert '"""' not in frozen_text and '"""' not in smoke_text and "'''" not in launcher_text

    cells = []
    for i, path in enumerate(sorted(glob.glob(os.path.join(HERE, "smoke_cells", "*")))):
        with open(path, encoding="utf-8") as f:
            src = f.read()
        src = (src.replace("{{FROZEN_JSON}}", frozen_text).replace("{{SMOKE_JSONL}}", smoke_text)
               .replace("{{LAUNCHER_PY}}", launcher_text))
        cell = {"id": f"smoke{i:02d}", "metadata": {}, "source": lines(src.rstrip("\n"))}
        if path.endswith(".md"):
            cell["cell_type"] = "markdown"
        else:
            cell.update({"cell_type": "code", "execution_count": None, "outputs": []})
        cells.append(cell)

    return {"cells": cells, "metadata": {"language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    out = os.path.join(REPO, "00_smoke_test.ipynb")
    text = json.dumps(build(), indent=1, ensure_ascii=False) + "\n"
    if args.check:
        same = os.path.exists(out) and open(out, encoding="utf-8").read() == text
        print("UP TO DATE" if same else "OUT OF DATE")
        sys.exit(0 if same else 1)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"wrote {out} ({len(build()['cells'])} cells)")


if __name__ == "__main__":
    main()
