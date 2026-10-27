# models/: the production Laya weights

The QA service grades with a fine-tuned Laya model. Its weights live here and **never go to GitHub** (everything in this folder except this file is git-ignored). The weights are **not in the Docker image either**: `docker-compose.yml` mounts this folder into the container, read-only.

| Folder | What it is |
|---|---|
| `final-softce-3/` | **Production.** The fine-tune the service runs (about 808 MB on disk, about 2 GB in RAM). Files: `model.safetensors`, `encoder/config.json`, `tokenizer/tokenizer.json`, `tokenizer/tokenizer_config.json`, `questions.json`, `rl_agent_config.json` |

## Get the weights (once per machine: laptop, test server, production server)

**Download:** the Google Drive folder `final-softce-3`
<https://drive.google.com/drive/folders/16a8ibMjEJ9CUwDURHmjLPu0fBUhWhdIj>
It is shared inside the company's Google account only (sign in with your work account). It is not public, and neither is any copy of the weights.

1. Open the link, right-click the folder `final-softce-3`, choose **Download**. Drive prepares a zip (about 800 MB).
2. Unzip it so the files sit directly in `models/final-softce-3/` inside this repo, next to this README. When you are done this file must exist: `models/final-softce-3/model.safetensors` (not `models/final-softce-3/final-softce-3/model.safetensors`).
3. Check the copy (below). It must end with `ALL FILES MATCH`.
4. Start the service (`DEPLOYMENT_PLAN.md`). On a server, copy the folder there once and keep it: updating the code with `git pull` does not touch it.

For a server without a browser, download on a laptop and copy the unzipped folder over (`scp -r models/final-softce-3 user@server:/path/to/QA-system/models/`).

## Check that your copy is intact

With Docker (nothing else to install; run it from the repo root, with the weights already in `models/final-softce-3`):

```
docker compose run --rm --no-deps qa-service python Scripts/verify_weights.py
```

Or with plain Python 3 (standard library only): `python Scripts/verify_weights.py`

Every file prints `OK` and the last line must be `ALL FILES MATCH`. Anything else (`MISSING`, `WRONG SIZE` = incomplete download, `CHANGED`) means: download again, do not run the service on that copy.

## What the service does with them

`docker-compose.yml` sets `LAYA_CHECKPOINT=models/final-softce-3` by default (`.env.example` has the same line). With that set the service serves these weights, applies the fine-tuned cutoffs and uses the flow-v2 snippets. If the folder is missing or unreadable the service **does not grade**: `GET /ready` answers 503 with the reason and `POST /api/evaluate` answers 503 with a message that points back here. It never quietly switches to another model.

The stock Laya model (what you get outside Docker with an empty `LAYA_CHECKPOINT`; compose always falls back to `final-softce-3`) needs internet access to Hugging Face on first start and grades less accurately (38 of 44 items against the reference answer key, against 42 of 44 for `final-softce-3`). It is not for production.

## If the weights change (a new fine-tune)

Put the new folder in the same Drive location (or a new one), update the sizes and SHA-256 hashes in `Scripts/verify_weights.py`, update the link above, and tell everyone to download again. Weights must not go to GitHub in any form (including Releases and Git LFS), by project rule: `model.safetensors` is 842 MB and GitHub refuses files over 100 MB anyway.

## Where the other weights are

* The experiment checkpoints (`ft5-...`, `ft6-...`) are in `../laya-finetuning/checkpoints/`, part of the separate Laya project (the folder `laya-finetuning` next to this one, its own repo). The catalogue is `../laya-finetuning/runs/CHECKPOINTS.md`.
* The originals of every checkpoint are on Google Drive (the Colab output folders). New machine: `../laya-finetuning/docs/NEW_PC_SETUP.md`.
* The same integrity check from the Laya repo, if you have it: `python ../laya-finetuning/tools/checkpoint_manifest.py verify models/final-softce-3 --manifest ../laya-finetuning/runs/ft3-stage3/final-softce-3.manifest.json`.
