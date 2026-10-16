"""Stage 2: length-robust rows. The first training run saw snippets about half as long as real calls
(Rapport chunks 44 vs 86 words, Paraphrasing 58 vs 164, Resolved 52 vs 101), and the tuned model flagged
12% of clearly polite real chunks as rude. This script takes the existing Rapport / Paraphrasing / Resolved pairs
and pads them with NEUTRAL agent lines (a fixed bank of procedural explanations: no apology, no insult, no
restating of the customer's problem, no resolution wording) so the decision line sits in a realistic-length snippet.
The label of a pair never changes: only the shared context gets longer.

    python tools/build_long.py --split train   # trl_* rows from train pairs (not pilot)
    python tools/build_long.py --split dev     # dvl_*
    python tools/build_long.py --split test    # tsl_*  (reported separately as "test_long")
"""
import argparse
import glob
import hashlib
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from build_rows import Builder, parse_file  # noqa: E402

PREFIX = {"train": "trl", "dev": "dvl", "test": "tsl"}
GLOB = {"train": "train_*.txt", "dev": "dev_*.txt", "test": "test_*.txt"}
CHECKS = ("rapport", "paraphrasing", "resolved")

BANK = [
    "I'm pulling up the details on my screen now, and it will take a moment to load completely.",
    "What I can see on my side is a record of the last few changes, and the most recent one was made earlier this week.",
    "The next step is to run a quick test from our end, and it usually takes about a minute to come back.",
    "Those settings are stored in two places, so I'll check both of them before changing anything.",
    "Our system keeps a history of every update, so I can go back through it and find exactly when things changed.",
    "I'll walk you through each step as I go, so you can see what I'm doing and stop me at any point.",
    "The diagnostics are still running, and they check the connection, the configuration and the recent activity one after another.",
    "There are a few possible causes for this, and the quickest way to narrow them down is to check them in order.",
    "I've opened the account notes, and there are a couple of entries from earlier contacts that I'll read through first.",
    "That part of the process is automatic, so once the update is sent it normally applies within a few minutes.",
    "I'm going to send a refresh signal to the account, which makes the system re-read all of the current settings.",
    "The report shows the status of each component, and most of them are reading normally at the moment.",
    "Let me check the schedule for that, because the available times change during the day.",
    "I'm entering the new details now, and the screen asks me to confirm each field before it saves.",
    "The system has a built-in check that compares what is on file with what was last sent out, so I'll run that next.",
    "Give me a few seconds while the page loads, it is a little slow on my side this afternoon.",
    "I'll add a note to the account with everything we've covered, so the next person who looks at it has the full picture.",
    "Once the request goes through, you will get a message with a reference number that you can keep for your records.",
    "The settings on that screen control how often the information is updated, and the default is every fifteen minutes.",
    "I'm looking at the usage figures for the last month now, and I'll go through them with you one at a time.",
    "There's a short delay between submitting a change and seeing it applied, which is normal for this kind of request.",
    "I can see the order history, and each entry shows the date, the item and the current status.",
    "The next screen lists the options that are available on your plan, so I'll read through them in order.",
    "I'll start with the simplest explanation first, because it is the most common one and the easiest to rule out.",
    "The log shows a series of entries from the early morning, and I'm reading through them to see what they say.",
    "I've sent the request to the right queue, and it shows up on my screen as submitted with today's date.",
    "That option is under the advanced menu, which is why it is easy to miss when you first look through the list.",
    "I'm comparing the two records side by side, and most of the fields match apart from a couple of dates.",
    "The process has three stages, which are the request, the review and the update, and I'll tell you where each one stands.",
    "I'll read out the information on file so you can tell me if any of it has changed since you last updated it.",
    "The tool is loading the latest data, and while it does that I'll pull up the previous results for comparison.",
    "Our records go back about two years, so I can look at the pattern over a longer period if that would help.",
    "There's a field here for additional notes, and I'm filling it in with the details of today's contact.",
    "The confirmation message is generated as soon as the request is accepted, and it is sent to the address on file.",
    "I'm opening the technical page for this now, which lists the standard steps for this type of situation.",
    "The results come back in a few parts, so I'll go through the first part and then the rest.",
    "I can see two entries for that date, and I'm opening each one to check what it says.",
    "That setting is controlled from the main profile, so I'm switching to that view to look at it.",
    "I'll take this one step at a time, so each change is clear and we can see the effect of each one.",
    "While the system processes that, I can explain how the next part works so it makes sense when it appears.",
    "The data on this screen refreshes every few minutes, so what you see now may differ slightly from earlier.",
    "I've found the right section of the record, and it shows the plan, the start date and the current options.",
    "The next check looks at the equipment details on file, such as the model, the version and the last time it reported in.",
    "Every request is given a priority based on the details provided, and I'm filling in those details now.",
    "I'm scrolling back through the history to find the entry from the start, because it shows how things were originally set up.",
    "Our process asks for a short summary of the situation, which I'm typing in as we speak.",
    "The numbers on that page are updated overnight, which is why they can lag behind what happened today.",
    "I'm going to open a second window so I can compare the current state with the previous one.",
    "The request form has a few required fields, and I've filled in the ones I already have from the account.",
    "There is a standard checklist for this, and I'm working through it from the top so nothing gets missed.",
    "That information is held in a separate system, so I'm switching over to it now.",
    "The system shows when each change was made and who made it, which helps me follow the sequence of events.",
    "I'll give you a quick overview of what the next few minutes look like, so you know what to expect.",
    "I'm checking the notes attached to the account, because they sometimes include details that do not show on the main page.",
    "The update takes place in the background, and nothing is needed from you while it runs.",
    "I'm reading through the terms that apply to this, and I'll point out the parts that matter for what you need.",
    "That screen shows a summary at the top and the detailed entries below, so I'll start with the summary.",
    "I'm running the same check a second time to make sure the first result was not a one-off.",
    "The tool gives me a code for each result, and I'm looking up what each code stands for.",
    "Most of this is routine, and I'm just verifying each item so that nothing is left out of the record.",
    "There's an option to receive updates by message or by email, and I'll set whichever you prefer.",
    "I've located the relevant policy page, and it lists the steps, the timeframes and the information we need to collect.",
    "The page is still loading, but I can already see the first few lines of the information, so I'll start there.",
    "I'm exporting the details so I can read them in a clearer layout than the default view.",
    "The latest entry was created automatically by the system, so I'm checking what triggered it.",
    "Each of these items has its own status, and I'll go through them from the oldest to the newest.",
    "I'm opening the settings page for the account, which has a section for each of the services attached to it.",
    "The way this works is that the request is queued, processed, and then confirmed, and it is currently in the queue.",
    "I'll enter the information in the order the form asks for it, so it is easier to review afterwards.",
    "The window on my screen shows the progress, and it has moved on to the second of the three steps.",
    "There's a section on the page that explains how the charges are calculated, and I'm opening it now.",
    "I'm taking a look at the connection details in the record, such as the type, the speed and the last update.",
    "To keep things in order, I'll note down the time of each step as I go along.",
    "I can see the last few interactions on the account, and I'm reading the summaries one by one.",
    "That check usually finishes quickly, and while it runs I'll prepare the next one.",
    "The system lets me preview the change before I apply it, so I'll show you what it will look like first.",
    "I'm filtering the list by date so that only the relevant entries are shown on the screen.",
    "The reference for this appears at the top right of my screen, and I'll read it out when it's complete.",
    "I'm going into the admin view now, which has a few extra details that the standard view leaves out.",
    "It takes a moment for the numbers to appear because the system gathers them from several sources.",
    "I'll go through the main points of the plan, and you can stop me if you would like me to slow down.",
    "There's a detailed breakdown on the next tab, and I'm opening it to see how the figures are made up.",
    "I'm reviewing the settings that were applied last time, to see how they compare with the current ones.",
    "Let me note the important details as we go, so nothing is left to memory later.",
]
ACKS = ["Right.", "I see.", "Mm-hmm.", "Got it.", "Sure.", "Yes, go on.", "Alright then."]


def pad(frag, rng):
    """New fragment: same label, same decision line, longer neutral context."""
    turns = [dict(t) for t in frag["turns"]]
    agent = lambda text: {"speaker": "Agent", "text": text, "focus": False, "sentiment": 6.0, "gap": 0}
    cust = lambda text: {"speaker": "Customer", "text": text, "focus": False, "sentiment": -4.0, "gap": 0}
    lines = rng.sample(BANK, 8)
    check = frag["check"]
    if check == "rapport":
        fi = next(i for i, t in enumerate(turns) if t["focus"])
        before, after = rng.choice([1, 2, 2, 3]), rng.choice([0, 1, 1, 2])
        turns[fi:fi] = [agent(l) for l in lines[:before]]
        fi += before
        turns[fi + 1:fi + 1] = [agent(l) for l in lines[before:before + after]]
    elif check == "paraphrasing":
        turns += [agent(l) for l in lines[:rng.choice([3, 4, 5, 6])]]
    elif check == "resolved":
        at = 1 if turns and turns[0]["speaker"] == "Customer" else 0
        extra = []
        for l in lines[:rng.choice([2, 3, 3])]:
            extra += [agent(l), cust(rng.choice(ACKS))]
        turns[at:at] = extra
    return turns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True, choices=list(PREFIX))
    args = ap.parse_args()
    b = Builder(source="claude-long")
    frags = []
    for path in sorted(glob.glob(os.path.join(REPO, "data", "fragments", "claude", GLOB[args.split]))):
        frags += parse_file(path)
    pairs = {}
    for f in frags:
        if f["check"] in CHECKS:
            pairs.setdefault(f.get("pair") or f["id"], []).append(f)
    rows, dropped = [], []
    for pid, members in sorted(pairs.items()):
        rng = random.Random(int(hashlib.md5(pid.encode()).hexdigest()[:8], 16))
        seed_state = rng.getstate()
        for f in members:
            rng.setstate(seed_state)                     # both members get the same padding
            g = dict(f)
            g["turns"] = pad(f, rng)
            g["id"] = PREFIX[args.split] + "_" + f["id"]
            g["pair"] = PREFIX[args.split] + "_" + pid
            row, why = b.row(g)
            if row:
                row["meta"]["long"] = True
                rows.append(row)
            else:
                dropped.append(why)
    # keep only pairs where both members survived
    by_pair = {}
    for r in rows:
        by_pair.setdefault(r["meta"]["pair_id"], []).append(r)
    rows = [r for p in by_pair.values() if len(p) == 2 for r in p]
    out = os.path.join(REPO, "data", "rows", f"long_{args.split}.jsonl")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    import collections
    cnt = collections.Counter((r["meta"]["check"], r["meta"]["label"]) for r in rows)
    words = collections.defaultdict(list)
    for r in rows:
        words[r["meta"]["check"]].append(len(r["state"].split()))
    print(f"{args.split}: {len(rows)} rows from {len(pairs)} pairs, dropped {len(dropped)} fragments")
    print(dict(cnt))
    print({k: round(sum(v) / len(v)) for k, v in words.items()}, "mean words per snippet")
    reasons = collections.Counter(d["reason"][:60] for d in dropped)
    print(dict(reasons))


if __name__ == "__main__":
    main()
