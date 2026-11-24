import shutil
from pathlib import Path

src = Path("data/fact_bank.md")
dst = Path("scripts/tests/tmp_fact_bank.md")
dst.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(src, dst)
print("Copied fact_bank.md to tmp_fact_bank.md successfully.")
