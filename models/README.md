# models/: the production Laya weights

The QA service grades with a fine-tuned Laya model. Its weights live here and **never go to GitHub** (everything in this folder except this file is git-ignored).

| Folder | What it is |
|---|---|
| `final-softce-3/` | **Production.** The fine-tune the service runs (about 808 MB on disk, about 2 GB in RAM). Files: `model.safetensors`, `encoder/`, `tokenizer/`, `questions.json`, `rl_agent_config.json` |

## Use it

Put this line in your `.env` (the file is git-ignored; a relative path is read from the repo root):

```
LAYA_CHECKPOINT=models/final-softce-3
```

With that set, the service serves these weights, applies the fine-tuned cutoffs and uses the flow-v2 snippets. Without it the service falls back to the stock model, which is much less accurate. If the path is wrong the service refuses to start (pipeline v3) or fails on the first call (pipeline v2).

## Check that your copy is intact

```
python Scripts/verify_weights.py
```

It needs nothing but Python and must end with `ALL FILES MATCH`. (The same check from the Laya repo, if you have it: `python ../laya-finetuning/tools/checkpoint_manifest.py verify models/final-softce-3 --manifest ../laya-finetuning/runs/ft3-stage3/final-softce-3.manifest.json`.)

## Getting the weights onto a new machine (every clone needs this once)

Git cannot carry the weights: `model.safetensors` is 842 MB and GitHub refuses files over 100 MB. They also must not go to GitHub in any form (including Releases and Git LFS), by project rule. So the code comes from `git clone` and the weights come separately, once per machine:

1. **Owner, once:** zip the folder `models/final-softce-3` (about 800 MB) and put the zip on company storage that the team can already reach and that is not public: SharePoint/OneDrive, Google Drive, S3/Azure Blob, or a shared server folder. Share the link with the people who need it. The originals of every checkpoint are also on the Colab Google Drive folders (see below).
2. **Everyone else:** download the zip, unzip it so the files sit directly in `models/final-softce-3/` (inside this repo, next to this README), then run `python Scripts/verify_weights.py`.
3. **Docker:** nothing extra. `docker-compose.v3.yml` mounts the `models/` folder, so the same copy is used. On a server, copy the folder there once and keep it; updating the code does not touch it. (Alternative for a server farm: bake the weights into a private image in your own private registry. Never a public one.)
4. **If the weights ever change** (a new fine-tune): put the new zip in the same place, update the sizes and hashes in `Scripts/verify_weights.py`, and tell the team to re-download.

## Where the other weights are

* The stock Laya model (needed only for stock-model runs and for building training data) is in your Hugging Face cache; see `.env.example` (`LAYA_HF_HOME`).
* The experiment checkpoints (`ft5-...`, `ft6-...`) are in `../laya-finetuning/checkpoints/`, part of the separate Laya project (the folder `laya-finetuning` next to this one, its own repo). The catalogue is `../laya-finetuning/runs/CHECKPOINTS.md`.
* The originals of every checkpoint are on Google Drive (the Colab output folders). New machine: `../laya-finetuning/docs/NEW_PC_SETUP.md`.
