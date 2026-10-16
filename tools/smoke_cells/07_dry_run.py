# CELL 7: --dry-run. Builds the training items with the real tokenizer; loads no weights, trains nothing.
# EXPECT: "dry-run: 20 rows read, 21 valid items, skipped: {}" (skipped must be empty).
!python -m laya.train_cli --data {SMOKE} --base {BASE} --dry-run --max-len 512 --head-max-len 192
