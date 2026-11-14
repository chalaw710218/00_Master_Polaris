#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threads 資料集向後相容轉接器 (Threads Sample Adapter for Bionic Core v6.4)
將舊版 insights_history.jsonl (posts/title/er) 轉化為 v6.4 純數學標準樣本列:
{"id": str, "text": str, "metric": float, "ts": str}
"""

import sys
import json
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
INSIGHTS_SRC = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\threads-growth-auditor\data\insights_history.jsonl")
STANDARD_OUT = DATA_DIR / "kage_standard_samples.jsonl"

def adapt_threads_samples():
    if not INSIGHTS_SRC.exists():
        print(f"❌ 來源資料集不存在: {INSIGHTS_SRC}")
        return False

    samples = []
    seen_ids = set()

    for line in INSIGHTS_SRC.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        ts = obj.get("captured_at", "")
        for p in obj.get("posts", []):
            pid = str(p.get("id"))
            text = p.get("title", "")
            metric = float(p.get("er", 0.0))
            if pid and text:
                samples.append({
                    "id": pid,
                    "text": text,
                    "metric": metric,
                    "ts": ts
                })

    STANDARD_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(STANDARD_OUT, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"✅ 成功產出標準通用樣本列: {STANDARD_OUT.name}，共 {len(samples)} 筆樣本")
    return True

if __name__ == "__main__":
    adapt_threads_samples()
