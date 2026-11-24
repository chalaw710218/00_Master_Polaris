import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
p = HERE / "falcon_recheck_13_24.json"
data = json.loads(p.read_text(encoding="utf-8"))

mismatches = [item for item in data if item.get("label") == "【對不上】"]
print(f"TOTAL_MISMATCHES: {len(mismatches)}")
for m in mismatches:
    r = m.get("rule_no")
    law = m.get("law")
    art = m.get("article")
    print(f"rule_no: {r} | law: {law} | article: {art}")
