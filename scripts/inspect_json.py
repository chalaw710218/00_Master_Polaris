import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
p = HERE / "falcon_recheck_13_24.json"
data = json.loads(p.read_text(encoding="utf-8"))
for item in data:
    r = item['rule_no']
    law = item['law']
    art = item['article']
    label = item['label']
    url = item['url']
    q = item['quote']
    print(f"{r} | {law} {art} | {label}")
    print(f"  出處：{law} {art} {url}")
    print(f"  原文：「{q}」\n")
