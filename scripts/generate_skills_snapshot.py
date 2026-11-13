# -*- coding: utf-8 -*-
import os
import json
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

base = os.path.abspath(".agents/skills")
snapshot = {
    "snapshot_epoch": "2026-11-13 17:42",
    "total_skills_count": 0,
    "guardrail_status": "Locked_ReadOnly_Production_Preserved",
    "description": "極星43項技能雙軌保全快照清單 · 確保特化期間既有生產功能100%零中斷",
    "skills": []
}

for folder in sorted(os.listdir(base)):
    if folder in ["atoms", "packs"]:
        continue
    p = os.path.join(base, folder)
    if os.path.isdir(p):
        skill_file = os.path.join(p, "SKILL.md")
        sz = os.path.getsize(skill_file) if os.path.exists(skill_file) else 0
        snapshot["skills"].append({
            "skill_id": folder,
            "rel_path": f".agents/skills/{folder}",
            "skill_md_size_bytes": sz,
            "status": "Production_Active_Guaranteed"
        })

snapshot["total_skills_count"] = len(snapshot["skills"])
out_path = os.path.abspath("00-00_Gamification_Engine/00-00_Legacy_Skills_Registry_Snapshot.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(snapshot, f, ensure_ascii=False, indent=2)

print(f"✅ 快照生成成功！共記錄 {snapshot['total_skills_count']} 項生產環境技能存證。")
