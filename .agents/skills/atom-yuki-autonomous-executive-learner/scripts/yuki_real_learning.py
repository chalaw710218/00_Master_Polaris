#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yuki_real_learning.py - 雪之內閣真實狀態彙整引擎
執行長學習的真實素材 = 各首長「學習引擎是否存在、證據檔是否存在、筆數、最後更新時間」。
全部由檔案系統即時讀取；不存在就如實標示 NO_EVIDENCE，不補假數據。
狀態：
  REAL_DATA_ACTIVE   - 引擎與證據檔皆存在，且最近 STALE_HOURS 內更新
  STALE              - 證據檔存在但超過 STALE_HOURS 未更新
  ENGINE_READY_NO_DATA - 有真實資料引擎但尚無證據檔
  NO_REAL_ENGINE     - 尚無真實資料引擎（僅有示範骨架）
  BLOCKED(原因)      - 已知外部阻礙（見 BLOCKERS，須人工維護並註明日期）
"""

import sys
import os
import json
import argparse
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.join(os.path.normpath(os.path.join(HERE, "..", "..", "..")), "skills")
HISTORY = os.path.normpath(os.path.join(HERE, "..", "vaults", "cabinet_status_history.jsonl"))
STALE_HOURS = 24 * 7

# 首長 -> (學習原子資料夾, 真實資料引擎腳本, 證據檔 glob 清單)
CABINET = {
    "雪(CEO)":      ("atom-yuki-autonomous-executive-learner", "yuki_real_learning.py", ["cabinet_status_history.jsonl"]),
    "林納斯(CTO)":  ("atom-linus-kernel-evolution-learner", "linus_real_learning.py", ["linus_autophagy_history.jsonl"]),
    "泰勒絲(CMO)":  ("atom-taylor-marketing-psychology-learner", "taylor_real_learning.py", ["taylor_marketing_state.json"]),
    "戴明(CQO)":    ("atom-deming-quality-sopk-learner", "deming_real_learning.py", ["deming_quality_history.jsonl"]),
    "算盤(CFO)":    ("atom-abacus-macro-compound-learner", "abacus_real_learning.py", ["abacus_margin_history.jsonl"]),
    "約瑟夫(CVO)":  ("atom-josef-visual-aesthetics-learner", "josef_real_learning.py", ["josef_contrast_history.jsonl"]),
    "影":           ("atom-kage-synaptic-metabolic-learner", "kage_real_learning.py", ["kage_synaptic_state.json"]),
    "尼奧":         ("atom-neo-frontend-vault-evolver", "neo_real_learning.py", ["neo_weight_history.jsonl"]),
    "艾達":         ("atom-ada-frontier-paper-evaluator", "ada_real_learning.py", ["vault_ada_papers.jsonl"]),
    "渡鴉":         ("atom-raven-investigative-mind-evolver", "raven_real_learning.py", ["raven_provenance_history.jsonl"]),
    "雪柔(律師)":   ("atom-falcon-legal-vault-decadal-evolver", "falcon_real_learning.py", ["falcon_citation_worklist.json"]),
}
# 已知外部阻礙（人工維護；每筆須註明日期與原因）
BLOCKERS = {
    "雪柔(律師)": "2026-11-14 全國法規資料庫 law.moj.gov.tw 自本機連線被拒；裁判書 API 需創辦人本人帳號且僅 0-6 時開放。引擎目前僅能產出『待查證引用清單』。",
}


def count_records(path):
    try:
        if path.endswith(".jsonl"):
            with open(path, "r", encoding="utf-8") as f:
                return sum(1 for l in f if l.strip())
        return 1
    except Exception:
        return None


def status_of(name, folder, engine, evidence):
    base = os.path.join(SKILLS_DIR, folder)
    engine_path = os.path.join(base, "scripts", engine)
    row = {"chief": name, "engine_exists": os.path.exists(engine_path), "evidence": []}
    newest = None
    for ev in evidence:
        p = os.path.join(base, "vaults", ev)
        if os.path.exists(p):
            mt = os.path.getmtime(p)
            newest = mt if newest is None else max(newest, mt)
            row["evidence"].append({"file": ev, "records": count_records(p),
                                    "modified": datetime.fromtimestamp(mt).isoformat(timespec="seconds")})
    if not row["engine_exists"]:
        row["status"] = "NO_REAL_ENGINE"
    elif not row["evidence"]:
        row["status"] = "ENGINE_READY_NO_DATA"
    else:
        age_h = (datetime.now().timestamp() - newest) / 3600
        row["age_hours"] = round(age_h, 1)
        row["status"] = "REAL_DATA_ACTIVE" if age_h <= STALE_HOURS else "STALE"
    if name in BLOCKERS and row["status"] != "REAL_DATA_ACTIVE":
        row["blocker"] = BLOCKERS[name]
        row["status"] = "BLOCKED(" + row["status"] + ")"
    elif name in BLOCKERS:
        row["note"] = BLOCKERS[name]
    return row


def summarize():
    rows = [status_of(n, *v) for n, v in CABINET.items()]
    tally = {}
    for r in rows:
        key = r["status"].split("(")[0] if r["status"].startswith("BLOCKED") else r["status"]
        tally[key] = tally.get(key, 0) + 1
    report = {
        "status": "CABINET_SURVEYED",
        "surveyed_at": datetime.now().isoformat(timespec="seconds"),
        "stale_after_hours": STALE_HOURS,
        "tally": tally,
        "chiefs": rows,
        "note": "狀態僅反映『真實資料引擎與證據檔是否存在及新舊』，不代表內容品質。",
    }
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps({"surveyed_at": report["surveyed_at"], "tally": tally}, ensure_ascii=False) + "\n")
    return report


def main():
    ap = argparse.ArgumentParser(description="雪之內閣真實狀態彙整引擎")
    ap.add_argument("--survey", action="store_true", help="彙整 11 位首長學習引擎與證據檔現況")
    args = ap.parse_args()
    if not args.survey:
        ap.print_help()
        return
    print(json.dumps(summarize(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
