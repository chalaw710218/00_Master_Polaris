import re
import json
from pathlib import Path

log_path = Path("00-00_Gamification_Engine/00-00_System_Operations_Log.md")
with open(log_path, "r", encoding="utf-8") as f:
    text = f.read()

entries = re.findall(r"###\s*\[(.*?)\](.*?)(?=\n###|\Z)", text, re.DOTALL)
print(f"Total log entries: {len(entries)}")

attr_snapshots = []
for title, body in entries:
    m = re.findall(r"(STR|INT|AGI|WILL|CHA|IMP)\s*[:：]\s*([0-9.]+)", body)
    if len(m) >= 3:
        attr_dict = {k: float(v) for k, v in m}
        lvl = re.findall(r"Lv\.?\s*([0-9]+)", body)
        attr_snapshots.append({
            "timestamp": title,
            "level": lvl[0] if lvl else None,
            "attributes": attr_dict
        })

print(f"Snapshots found: {len(attr_snapshots)}")
for s in attr_snapshots:
    print(f"{s['timestamp']} | Level: {s['level']} | {s['attributes']}")
