#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polaris 4x4 K-Slot Latin Square Rotator (發文時段每日輪換排程器)
作者: 影 (Shadow · 首席特務兼生活管家)

創辦人（品碩）親定 4 天循環輪換規則：
確保對照組 []、K-014、K-025、K-031 均勻分布於 4 個時段 (09:07、12:34、17:36、22:33)，
讓評估程式能在相同時段進行公平比較：
- 第 1 天：09:07 對照組 []、12:34 K-025、17:36 K-031、22:33 K-014
- 第 2 天：09:07 K-014、12:34 對照組 []、17:36 K-025、22:33 K-031
- 第 3 天：09:07 K-031、12:34 K-014、17:36 對照組 []、22:33 K-025
- 第 4 天：09:07 K-025、12:34 K-031、17:36 K-014、22:33 對照組 []
- 之後每 4 天循環一次。
"""

import sys
import argparse
from datetime import date, datetime, timedelta

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

# 以 2026-11-24 為第 1 天基準日 (Epoch Date)
ROTATION_EPOCH = date(2026, 11, 24)

# 每日 4 個法定發文時段
SLOTS = [
    {"index": 0, "time": "09:07", "label": "晨間檔"},
    {"index": 1, "time": "12:34", "label": "午間檔"},
    {"index": 2, "time": "17:36", "label": "傍晚檔"},
    {"index": 3, "time": "22:33", "label": "夜間檔"},
]

# 第 1 天 (day_offset = 0) 的基準序列
BASE_SEQUENCE = ["control", "K-025", "K-031", "K-014"]


def format_k_display(k_id: str) -> str:
    if k_id in ("control", "[]"):
        return "對照組 []"
    return k_id


def infer_slot_index_from_hour(hour: int) -> int:
    """依執行當下小時自動判定所屬時段 (0~3)"""
    if hour < 11:
        return 0  # 09:07
    elif hour < 15:
        return 1  # 12:34
    elif hour < 20:
        return 2  # 17:36
    else:
        return 3  # 22:33


def get_k_id_for_date_and_slot(target_date: date, slot_index: int) -> str:
    """
    依日期與時段索引 (0~3) 自動決定當下應發哪一種 K-ID：
    公式：BASE_SEQUENCE[(slot_index - day_offset) % 4]
    """
    day_offset = (target_date - ROTATION_EPOCH).days % 4
    idx = (slot_index - day_offset) % 4
    return BASE_SEQUENCE[idx]


def get_daily_schedule(target_date: date) -> list[dict]:
    """取得指定日期全天 4 個時段的完整排程配置"""
    day_offset = (target_date - ROTATION_EPOCH).days % 4
    schedule = []
    for s in SLOTS:
        k_id = get_k_id_for_date_and_slot(target_date, s["index"])
        schedule.append({
            "date": target_date.isoformat(),
            "cycle_day": day_offset + 1,
            "slot_index": s["index"],
            "time": s["time"],
            "label": s["label"],
            "k_id": k_id,
            "display": format_k_display(k_id)
        })
    return schedule


def print_4day_schedule(start_date: date = None, days: int = 4):
    if start_date is None:
        start_date = ROTATION_EPOCH

    print("==========================================================================")
    print("📅 生活管家 Threads 未來 4 天發文時段自動輪換排程表 (程式動態計算輸出)")
    print("==========================================================================")
    print(f"{'日期':<12} | {'循環日':<6} | {'09:07 (晨間)':<12} | {'12:34 (午間)':<12} | {'17:36 (傍晚)':<12} | {'22:33 (夜間)':<12}")
    print("-" * 74)
    for i in range(days):
        d = start_date + timedelta(days=i)
        sched = get_daily_schedule(d)
        c_day = f"第 {sched[0]['cycle_day']} 天"
        s0 = sched[0]["display"]
        s1 = sched[1]["display"]
        s2 = sched[2]["display"]
        s3 = sched[3]["display"]
        print(f"{d.isoformat():<12} | {c_day:<6} | {s0:<12} | {s1:<12} | {s2:<12} | {s3:<12}")
    print("==========================================================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="4x4 發文時段自動輪換排程器")
    parser.add_argument("--start-date", type=str, default="2026-11-24", help="起始日期 (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=4, help="預覽天數")
    args = parser.parse_args()
    print_4day_schedule(date.fromisoformat(args.start_date), args.days)
