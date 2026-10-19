"""Speech-to-text-style roughening of a transcript, seeded so it is reproducible.

Real ASR output is messier than written dialogue: missing commas and apostrophes, lower-case sentence starts,
fillers, stutters, homophone slips. Applied to about 30% of generated calls so the model does not learn
"clean prose = label". Question marks are kept because the production extractors split questions on them.

IMPORTANT: roughness is decided per PAIR (or per item when unpaired), never per member of a pair, otherwise
"rough or clean" would leak the label (see build_rows.use_rough).

    python tools/roughen.py "So, it keeps dropping every evening, I'm not sure why?" 7
"""
import random
import re
import sys

FILLERS = ["um", "uh", "you know", "like", "i mean", "so yeah", "okay so"]
HOMOPHONES = [(r"\btheir\b", "there"), (r"\bthere\b", "their"), (r"\byour\b", "youre"), (r"\bits\b", "it's"),
              (r"\bto\b", "too"), (r"\bwe're\b", "were"), (r"\bhear\b", "here")]
CONTRACTION_DROP = {"i'm": "im", "don't": "dont", "can't": "cant", "it's": "its", "that's": "thats", "i've": "ive",
                    "didn't": "didnt", "doesn't": "doesnt", "won't": "wont", "i'll": "ill", "isn't": "isnt",
                    "you're": "youre", "what's": "whats", "let's": "lets", "i'd": "id"}


def roughen_text(text: str, rng: random.Random, strength: float = 1.0) -> str:
    s = text
    # 1. drop commas (most of them) and some apostrophes in contractions
    if rng.random() < 0.8 * strength:
        s = re.sub(r",", "" if rng.random() < 0.7 else " ", s)
    if rng.random() < 0.6 * strength:
        s = re.sub(r"\b[A-Za-z]+'[a-z]+\b", lambda m: CONTRACTION_DROP.get(m.group(0).lower(), m.group(0)), s)
    # 2. lower-case some sentence starts and the pronoun I
    if rng.random() < 0.6 * strength:
        s = re.sub(r"(^|[.!?]\s+)([A-Z])", lambda m: m.group(1) + (m.group(2).lower() if rng.random() < 0.7 else m.group(2)), s)
        s = re.sub(r"\bI\b", lambda m: "i" if rng.random() < 0.5 else "I", s)
    # 3. fillers before a clause
    words = s.split(" ")
    out = []
    for i, w in enumerate(words):
        if i > 0 and rng.random() < 0.05 * strength and not w.endswith("?"):
            out.append(rng.choice(FILLERS))
        out.append(w)
        # 4. stutter: repeat a short word
        if len(w) <= 4 and w.isalpha() and rng.random() < 0.025 * strength:
            out.append(w)
    s = " ".join(out)
    # 5. one homophone slip, rarely
    if rng.random() < 0.25 * strength:
        pat, rep = rng.choice(HOMOPHONES)
        s = re.sub(pat, rep, s, count=1, flags=re.IGNORECASE)
    # 6. drop a final period sometimes (keeps ? and !)
    if s.endswith(".") and rng.random() < 0.5 * strength:
        s = s[:-1]
    return re.sub(r"\s{2,}", " ", s).strip()


if __name__ == "__main__":
    print(roughen_text(sys.argv[1], random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 0)))
