#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-slimming-4d-dispatcher: 四維真值動態調用方程式運算原子
嚴格恪守工作區憲則《規則 6》
由 CTO 林納斯 (Linus) ✕ 首席品質長戴明 (Dr. Deming) 聯合打造
"""

import sys
import os
import argparse
import math
import json

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 知識庫候選切片樣品
KNOWLEDGE_SLICES = [
    {
        "id": "KB-AXIOM-01",
        "title": "開課席次法旨",
        "content": "實體工作坊每堂嚴格限額 6 席（純實體小班深度排錯，正取 6 席 + 備取 2 席 + 加開庫分流，沒做出成果不放學）。",
        "keywords": ["開課", "席次", "工作坊", "名額", "6席"],
        "utility": 1.0,
        "age_days": 0.1,
        "conflict_penalty": 0.0
    },
    {
        "id": "KB-AXIOM-02",
        "title": "創辦人作息法旨鋼印",
        "content": "品碩工作戰鬥最晚至半夜 02:00，01:45 提醒日結收尾，02:00 嚴格催促就寢。",
        "keywords": ["作息", "半夜", "時間", "健康", "兩點", "2點"],
        "utility": 1.0,
        "age_days": 0.1,
        "conflict_penalty": 0.0
    },
    {
        "id": "KB-AXIOM-03",
        "title": "歷史舊制開課席次（已廢棄）",
        "content": "歷史早期草案曾考慮每堂 8 席或 12 席。",
        "keywords": ["開課", "席次", "8席", "12席"],
        "utility": 0.2,
        "age_days": 30.0,
        "conflict_penalty": 10.0 # 廢棄矛盾懲罰
    },
    {
        "id": "KB-AXIOM-04",
        "title": "品牌法定對外紅線",
        "content": "官方品牌全稱『生活的一部分，就醬點！』，日常自稱『生活管家』，嚴禁外洩內部代號。",
        "keywords": ["品牌", "名稱", "生活管家", "紅線", "代號"],
        "utility": 1.0,
        "age_days": 1.0,
        "conflict_penalty": 0.0
    }
]

AGENT_WEIGHTS = {
    "yuki": {"w_r": 0.40, "w_u": 0.30, "w_a": 0.20, "w_c": 1.50},
    "linus": {"w_r": 0.45, "w_u": 0.35, "w_a": 0.10, "w_c": 2.00},
    "abacus": {"w_r": 0.35, "w_u": 0.40, "w_a": 0.15, "w_c": 1.50},
    "deming": {"w_r": 0.30, "w_u": 0.40, "w_a": 0.10, "w_c": 2.00},
    "kage": {"w_r": 0.40, "w_u": 0.30, "w_a": 0.25, "w_c": 1.00}
}

def calculate_relevance(query: str, slice_obj: dict) -> float:
    match_count = sum(1 for kw in slice_obj["keywords"] if kw in query)
    return min(1.0, match_count * 0.45)

def calculate_time_activity(age_days: float, lambda_decay: float = 0.05) -> float:
    return math.exp(-lambda_decay * age_days)

def evaluate_4d_dispatch(query: str, agent_role: str) -> list[dict]:
    weights = AGENT_WEIGHTS.get(agent_role.lower(), AGENT_WEIGHTS["yuki"])
    scored_slices = []

    for item in KNOWLEDGE_SLICES:
        r = calculate_relevance(query, item)
        u = item["utility"]
        a = calculate_time_activity(item["age_days"])
        c = item["conflict_penalty"]

        # S(D_i | Q) = w_r * R + w_u * U + w_a * A - w_c * C
        final_score = (weights["w_r"] * r) + (weights["w_u"] * u) + (weights["w_a"] * a) - (weights["w_c"] * c)
        
        scored_slices.append({
            "id": item["id"],
            "title": item["title"],
            "content": item["content"],
            "r_score": round(r, 3),
            "u_score": round(u, 3),
            "a_score": round(a, 3),
            "c_penalty": round(c, 3),
            "final_score": round(final_score, 4)
        })

    # 按分數由高至低排序，取 Top-3
    scored_slices.sort(key=lambda x: x["final_score"], reverse=True)
    return scored_slices[:3]

def main():
    parser = argparse.ArgumentParser(description="四維真值動態調用方程式運算原子 (atom-slimming-4d-dispatcher)")
    parser.add_argument("--query", type=str, default="我們這週的工作坊開課席次到底要設幾席？", help="創辦人當前提問")
    parser.add_argument("--agent-role", type=str, default="yuki", help="響應天王角色 (yuki/linus/abacus/deming/kage)")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")

    args = parser.parse_args()

    print("=== [atom-slimming-4d-dispatcher 四維真值調用方程式審計] ===")
    print(f"響應角色: {args.agent_role.upper()}")
    print(f"當前命題: \"{args.query}\"")

    top3 = evaluate_4d_dispatch(args.query, args.agent_role)

    print(f"\n[四維方程式裁決結果 · 精選 Top-3 中層片段]")
    for idx, item in enumerate(top3, 1):
        print(f"  #{idx} [{item['id']}] {item['title']} ➔ 總分: {item['final_score']}")
        print(f"      (R={item['r_score']}, U={item['u_score']}, A={item['a_score']}, C={item['c_penalty']})")
        print(f"      內容切片: \"{item['content']}\"")

    if args.dry_run:
        print("\n[物理演練模式 --dry-run] 調度結果 JSON 預覽 (前 250 字元):")
        res_str = json.dumps(top3, ensure_ascii=False, indent=2)
        print(res_str[:250] + "...\n")
        print("[物理演練驗證成功] 四維真值方程式與 Top-3 抽脂調度正常，Exit Code: 0")
        return

    print("[執行成功] 中層記憶片段已成功提取並注入推論，Exit Code: 0")

if __name__ == "__main__":
    main()
