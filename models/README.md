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
python ../laya-finetuning/tools/checkpoint_manifest.py verify models/final-softce-3 --manifest ../laya-finetuning/runs/ft3-stage3/final-softce-3.manifest.json
```

It must print `ALL FILES MATCH`.

## Where the other weights are

* The stock Laya model (needed only for stock-model runs and for building training data) is in your Hugging Face cache; see `.env.example` (`LAYA_HF_HOME`).
* The experiment checkpoints (`ft5-...`, `ft6-...`) are in `../laya-finetuning/checkpoints/`, part of the separate Laya project (the folder `laya-finetuning` next to this one, its own repo). The catalogue is `../laya-finetuning/runs/CHECKPOINTS.md`.
* The originals of every checkpoint are on Google Drive (the Colab output folders). New machine: `../laya-finetuning/docs/NEW_PC_SETUP.md`.
