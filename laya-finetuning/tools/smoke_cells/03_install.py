# CELL 3: install laya (same commit as the local v0.4.0 checkout) and the same transformers as local.
# EXPECT: no errors, then "laya 0.4.0" and "transformers 5.16.1".
# If pip says a restart is needed: restart the kernel, re-run cell 1, SKIP this cell, continue at cell 4.
!pip -q install "laya @ git+https://github.com/NandhaKishorM/laya.git@{LAYA_COMMIT}" "transformers==5.16.1"
from importlib.metadata import version
print("laya", version("laya"), "| transformers", version("transformers"), "| torch", version("torch"))
