"""Check that a copy of the production weights is complete and unchanged (no model, no network, standard library only).

    python Scripts/verify_weights.py                          # checks models/final-softce-3
    python Scripts/verify_weights.py path/to/final-softce-3

Prints OK or the problem for every file and ends with ALL FILES MATCH when the folder is exactly the production fine-tune.
The sizes and SHA-256 hashes below are the same as ../laya-finetuning/runs/ft3-stage3/final-softce-3.manifest.json.
"""
import hashlib
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXPECTED = {
    "encoder/config.json": (2084, "4d31981e52fcbf329542b1be74989bd46fcceda83e747ae003ee8dc7a1cc13c6"),
    "model.safetensors": (842609220, "fc6a3f1b793aa38e5e78543a10be5626064f420d1f5b5abcf77095ff72582dad"),
    "questions.json": (4794, "75e2e56357014e307786c4df542e35398b2ca4924ba306d334d50959c8b9e25d"),
    "rl_agent_config.json": (4873, "a8b3869e9ed66ffd0fe44115a83a9dcb70bb029733a1a4e2fbea457c58f3a7c9"),
    "tokenizer/tokenizer.json": (3583325, "0b3214f8efe1327290428b84e5d344ff3f2442686c1b89fb7b42c13a79ce6779"),
    "tokenizer/tokenizer_config.json": (337, "08d4cf3ac4dca381759441b85b91a6d40e688471dcd33d15d6649eb0a9a854d1"),
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    folder = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ROOT, "models", "final-softce-3")
    if not os.path.isdir(folder):
        print(f"No such folder: {folder}\nPut the weights there first (see models/README.md).")
        return 1
    bad = 0
    for rel, (size, digest) in EXPECTED.items():
        path = os.path.join(folder, *rel.split("/"))
        if not os.path.isfile(path):
            print(f"MISSING   {rel}")
            bad += 1
        elif os.path.getsize(path) != size:
            print(f"WRONG SIZE {rel}: {os.path.getsize(path)} bytes, expected {size} (incomplete download?)")
            bad += 1
        elif sha256(path) != digest:
            print(f"CHANGED   {rel}: contents differ from the production file")
            bad += 1
        else:
            print(f"OK        {rel}")
    print("ALL FILES MATCH" if not bad else f"{bad} problem(s): do not use this copy")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
