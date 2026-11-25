#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-yuki-cabinet-orchestrator: 全天王十一方非同步路由排程與自由能最小化原子腳本
專職負責執行長雪 (Yuki) 對全體十一大天王首長與看板娘喵編之 DAG 任務路由協同。
"""

import sys
import os
import argparse
import json
import re
from datetime import datetime

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CABINET_CHIEFS = {
    "Linus": {"title": "工程長 (CTO)", "keywords": ["代碼", "api", "系統", "底層", "架構", "自動化", "性能", "腳本"]},
    "Abacus": {"title": "財務長 (CFO)", "keywords": ["成本", "定價", "5d", "毛利", "水庫", "現金流", "帳本", "審計"]},
    "Taylor": {"title": "行銷長 (CMO)", "keywords": ["行銷", "文案", "敘事", "社群", "共鳴", "宣傳", "招生"]},
    "Deming": {"title": "首席品質長 (CQO)", "keywords": ["品質", "安燈", "防呆", "poka-yoke", "sop", "檢驗", "質檢"]},
    "Josef": {"title": "首席視覺長 (CVO)", "keywords": ["視覺", "海報", "排版", "印刷", "網格", "字體", "300dpi"]},
    "Falcon": {"title": "法務兼情報長 (CLO/CIO)", "keywords": ["法規", "合約", "合規", "情報", "專法", "特許", "護城河"]},
    "Kage": {"title": "首席特務兼管家", "keywords": ["threads", "漫遊", "私域", "管家", "巡邏", "關懷", "生活"]},
    "Neo": {"title": "首席前端體驗師", "keywords": ["前端", "ui", "app", "烈日", "離線", "service worker", "交互"]},
    "Ada": {"title": "首席科技偵察官", "keywords": ["ai", "端側", "偵察", "雷達", "模型", "邊緣", "硬體"]},
    "Raven": {"title": "首席黑色調查官", "keywords": ["調查", "徵信", "反詐", "司法", "判決", "穿透", "背調"]},
    "Meow": {"title": "門面吉祥物 (喵編)", "keywords": ["貓", "本喵", "接梗", "治癒", "吉祥物", "傲嬌"]},
}

def analyze_task_dispatch(task_desc: str) -> dict:
    """分析任務特徵，匹配相關內閣首長並生成有向無環圖 (DAG)"""
    task_lower = task_desc.lower()
    involved_chiefs = []

    for chief, info in CABINET_CHIEFS.items():
        if any(k in task_lower for k in info["keywords"]):
            involved_chiefs.append({
                "chief": chief,
                "title": info["title"],
                "role": chief
            })

    # 若未匹配到特定首長，預設基礎戰略鐵三角 (Abacus, Taylor, Deming)
    if not involved_chiefs:
        involved_chiefs = [
            {"chief": "Abacus", "title": CABINET_CHIEFS["Abacus"]["title"], "role": "Abacus"},
            {"chief": "Taylor", "title": CABINET_CHIEFS["Taylor"]["title"], "role": "Taylor"},
            {"chief": "Deming", "title": CABINET_CHIEFS["Deming"]["title"], "role": "Deming"},
        ]

    # 構建多階非同步排程管線 (Pipeline Stages)
    stages = [
        {"stage": 1, "phase": "情報徵信與法規前置", "members": [c["chief"] for c in involved_chiefs if c["chief"] in ["Raven", "Falcon", "Ada"]]},
        {"stage": 2, "phase": "底層架構與成本定價", "members": [c["chief"] for c in involved_chiefs if c["chief"] in ["Linus", "Abacus"]]},
        {"stage": 3, "phase": "前端交互與視覺排版", "members": [c["chief"] for c in involved_chiefs if c["chief"] in ["Neo", "Josef"]]},
        {"stage": 4, "phase": "社群敘事與溫度人設", "members": [c["chief"] for c in involved_chiefs if c["chief"] in ["Taylor", "Kage", "Meow"]]},
        {"stage": 5, "phase": "戴明安燈出廠終審", "members": ["Deming"]},
        {"stage": 6, "phase": "CEO 雪統籌審批與創辦人呈報", "members": ["Yuki"]}
    ]

    # 過濾空階層
    active_stages = [s for s in stages if len(s["members"]) > 0]

    return {
        "task": task_desc,
        "timestamp": datetime.now().isoformat(),
        "involved_chiefs_count": len(involved_chiefs),
        "involved_chiefs": involved_chiefs,
        "dag_pipeline": active_stages
    }

def main():
    parser = argparse.ArgumentParser(description="全天王十一方非同步路由排程原子")
    parser.add_argument("--task", type=str, default="台東在地友店-18度C自提櫃與生鮮選品上線", help="商業任務描述")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")

    args = parser.parse_args()

    print("=== [atom-yuki-cabinet-orchestrator] 啟動全天王十一方非同步路由協同 ===")
    res = analyze_task_dispatch(args.task)

    print(f"\n任務名稱: 『{res['task']}』")
    print(f"動員內閣天王首長數: {res['involved_chiefs_count']} 位")
    for c in res["involved_chiefs"]:
        print(f"  * 【{c['chief']}】{c['title']}")

    print("\n🗺️ **【執行長雪 · 任務依賴圖 (DAG) 管弦樂排程】**")
    for stage in res["dag_pipeline"]:
        members_str = ", ".join(stage["members"])
        print(f"  第 {stage['stage']} 階: 【{stage['phase']}】 ➔ 責任首長: [{members_str}]")

    print("\n[+] 全域自由能最小化排程建構完畢 (Exit Code: 0)！")
    sys.exit(0)

if __name__ == "__main__":
    main()
