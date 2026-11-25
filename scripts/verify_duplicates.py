# -*- coding: utf-8 -*-
import re
from collections import Counter

with open("SKILL_MAP.md", "r", encoding="utf-8") as f:
    text = f.read()

# 比對 Markdown 表格第一欄的技能名稱
matches = re.findall(r"\|\s*\*\*`([^`]+)`\*\*\s*\|", text)
counts = Counter(matches)
dups = {k: v for k, v in counts.items() if v > 1}

print(f"Total skills listed in SKILL_MAP: {len(matches)}")
print(f"Unique skills: {len(counts)}")
print(f"Duplicate skills count: {len(dups)}")
if dups:
    print("Duplicates:", dups)
else:
    print("✅ 驗收通過：重複名稱項目為 0！全內閣現役技能完全無同名重複！")
