# Flow v2 window lab on AG50

Old windows: probabilities from the probe files. New windows: scored by `laya-finetuning/eval/window_lab.py`. Key = Antigravity, not human-reviewed. AG50 is a development set, so every number below is for choosing variants, not a final result.

## Empathy

| Variant | Keyed evidence inside the window | Windows per call |
|---|---|---|
| first6 | 29/32 | 1.0 |
| first4 | 29/32 | 1.0 |
| two6 | 29/32 | 1.3 |

**fine-tuned** (deployed cutoff 0.49; faults in key 17 of 50)

| Window | AUC | Balanced accuracy | TP/FN/FP/TN | BA odd calls | BA even calls | BA with cutoff tuned on the other half |
|---|---|---|---|---|---|---|
| old (today) | 0.69 | 0.62 | 17/0/25/8 | 0.60 | 0.65 | 0.58 |
| first6 | 0.95 | 0.76 | 9/8/0/33 | 0.50 | 0.88 | 0.84 |
| first4 | 0.99 | 0.91 | 14/3/0/33 | 0.80 | 0.96 | 0.90 |
| two6 | 0.95 | 0.76 | 9/8/0/33 | 0.50 | 0.88 | 0.84 |

**stock** (deployed cutoff 0.78; faults in key 17 of 50)

| Window | AUC | Balanced accuracy | TP/FN/FP/TN | BA odd calls | BA even calls | BA with cutoff tuned on the other half |
|---|---|---|---|---|---|---|
| old (today) | 0.74 | 0.50 | 17/0/33/0 | 0.50 | 0.50 | 0.66 |
| first6 | 0.84 | 0.64 | 16/1/22/11 | 0.68 | 0.61 | 0.73 |
| first4 | 0.88 | 0.73 | 16/1/16/17 | 0.68 | 0.73 | 0.78 |
| two6 | 0.83 | 0.65 | 16/1/21/12 | 0.68 | 0.65 | 0.73 |

## Paraphrasing

| Variant | Keyed evidence inside the window | Windows per call |
|---|---|---|
| cue_oldwin | 26/31 | 0.8 |
| cue_newwin | 30/31 | 0.8 |

**fine-tuned** (deployed cutoff 0.47; faults in key 16 of 50)

| Window | AUC | Balanced accuracy | TP/FN/FP/TN | BA odd calls | BA even calls | BA with cutoff tuned on the other half |
|---|---|---|---|---|---|---|
| old (today) | 0.63 | 0.58 | 5/11/5/29 | 0.66 | 0.50 | 0.64 |
| cue_oldwin | 0.74 | 0.69 | 9/7/6/28 | 0.69 | 0.69 | 0.68 |
| cue_newwin | 0.90 | 0.86 | 14/2/5/29 | 0.88 | 0.85 | 0.82 |

**stock** (deployed cutoff 0.50; faults in key 16 of 50)

| Window | AUC | Balanced accuracy | TP/FN/FP/TN | BA odd calls | BA even calls | BA with cutoff tuned on the other half |
|---|---|---|---|---|---|---|
| old (today) | 0.63 | 0.54 | 4/12/6/28 | 0.54 | 0.54 | 0.58 |
| cue_oldwin | 0.75 | 0.71 | 10/6/7/27 | 0.69 | 0.72 | 0.65 |
| cue_newwin | 0.84 | 0.79 | 14/2/10/24 | 0.85 | 0.73 | 0.69 |

## Ownership

| Variant | Keyed evidence inside the window | Windows per call |
|---|---|---|
| v2 | 17/17 | 0.4 |

**fine-tuned** (deployed cutoff 0.52; faults in key 17 of 50)

| Window | AUC | Balanced accuracy | TP/FN/FP/TN | BA odd calls | BA even calls | BA with cutoff tuned on the other half |
|---|---|---|---|---|---|---|
| old (today) | 0.82 | 0.79 | 10/7/0/33 | 0.80 | 0.79 | 0.82 |
| v2 | 1.00 | 0.97 | 16/1/0/33 | 1.00 | 0.96 | 0.99 |

**stock** (deployed cutoff 0.52; faults in key 17 of 50)

| Window | AUC | Balanced accuracy | TP/FN/FP/TN | BA odd calls | BA even calls | BA with cutoff tuned on the other half |
|---|---|---|---|---|---|---|
| old (today) | 0.82 | 0.62 | 4/13/0/33 | 0.60 | 0.62 | 0.82 |
| v2 | 0.99 | 0.68 | 6/11/0/33 | 0.70 | 0.67 | 0.90 |

## Resolved

| Variant | Keyed evidence inside the window | Windows per call |
|---|---|---|
| tail300 | 25/31 | 1.0 |
| tail180 | 25/31 | 1.0 |
| last14 | 24/31 | 1.0 |

**fine-tuned** (deployed cutoff 0.42; faults in key 19 of 50)

| Window | AUC | Balanced accuracy | TP/FN/FP/TN | BA odd calls | BA even calls | BA with cutoff tuned on the other half |
|---|---|---|---|---|---|---|
| old (today) | 0.85 | 0.77 | 12/7/3/28 | 0.86 | 0.73 | 0.80 |
| tail300 | 0.92 | 0.79 | 11/8/0/31 | 0.83 | 0.77 | 0.78 |
| tail180 | 0.92 | 0.76 | 10/9/0/31 | 0.83 | 0.73 | 0.85 |
| last14 | 0.86 | 0.73 | 10/9/2/29 | 0.72 | 0.73 | 0.72 |

**stock** (deployed cutoff 0.73; faults in key 19 of 50)

| Window | AUC | Balanced accuracy | TP/FN/FP/TN | BA odd calls | BA even calls | BA with cutoff tuned on the other half |
|---|---|---|---|---|---|---|
| old (today) | 0.92 | 0.82 | 16/3/6/25 | 0.92 | 0.76 | 0.87 |
| tail300 | 0.91 | 0.82 | 14/5/3/28 | 0.78 | 0.84 | 0.77 |
| tail180 | 0.93 | 0.85 | 15/4/3/28 | 0.78 | 0.88 | 0.79 |
| last14 | 0.90 | 0.81 | 15/4/5/26 | 0.95 | 0.72 | 0.69 |

