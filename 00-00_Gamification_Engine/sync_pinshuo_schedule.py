"""
極星創辦人（品碩）專屬作息行事曆批量同步腳本 (Founder Schedule Syncer)
====================================================================
依據品碩日常作息定錨：
1. 10:00 - 14:00 🛵 午間外送前線出勤 (4 hr)
2. 14:00 - 17:30 🏛️ 家宅營運與戰略研發中樞 (3.5 hr)
3. 17:30 - 次日 01:00 🛵 晚間與深夜外送前線出勤 (7.5 hr)
"""

import sys
import os
import time
from datetime import datetime, date, timedelta
from pathlib import Path

# 自適應路徑載入
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))

from calendar_manager import add_calendar_event

def sync_schedule_range(start_date: date, days: int = 7):
    print(f"🚀 開始為創辦人（品碩）批量排定 Google 日曆行程...")
    print(f"📅 起始日期：{start_date}，天數：{days} 天\n")
    
    total_added = 0
    
    for i in range(days):
        current_day = start_date + timedelta(days=i)
        day_str = current_day.strftime("%Y-%m-%d")
        next_day_str = (current_day + timedelta(days=1)).strftime("%Y-%m-%d")
        
        print(f"--- 處理日期：{day_str} ({current_day.strftime('%A')}) ---")
        
        # 1. 午間外送出勤 (10:00 - 14:00)
        s1_start = f"{day_str}T10:00:00+08:00"
        s1_end = f"{day_str}T14:00:00+08:00"
        ok1 = add_calendar_event(
            title="🛵【生活管家】午間外送前線出勤",
            start_iso=s1_start,
            end_iso=s1_end,
            description="生活管家第一線午間外送出勤 (機動護航模式：秒級 5D 報價支援)。",
            location="台東市區"
        )
        if ok1: total_added += 1
        time.sleep(0.5)
        
        # 2. 家宅營運與戰略中樞 (14:00 - 17:30)
        s2_start = f"{day_str}T14:00:00+08:00"
        s2_end = f"{day_str}T17:30:00+08:00"
        ok2 = add_calendar_event(
            title="🏛️【生活管家】家宅營運與戰略研發中樞",
            start_iso=s2_start,
            end_iso=s2_end,
            description="家宅總部坐鎮：選品進銷存、TastyIgniter 點餐、ERP 對帳與極星內閣深度協同 (戰略推進黃金窗口)。",
            location="生活管家·家宅總部 (台東市正氣北路166巷90號)"
        )
        if ok2: total_added += 1
        time.sleep(0.5)
        
        # 3. 晚間與深夜外送出勤 (17:30 - 次日 01:00)
        s3_start = f"{day_str}T17:30:00+08:00"
        s3_end = f"{next_day_str}T01:00:00+08:00"
        ok3 = add_calendar_event(
            title="🛵【生活管家】晚間與深夜外送前線出勤",
            start_iso=s3_start,
            end_iso=s3_end,
            description="生活管家第一線晚間與深夜外送出勤。注意保暖與行車安全 (深夜守護模式，01:00 收工閉環)。",
            location="台東市區"
        )
        if ok3: total_added += 1
        time.sleep(0.5)
        
    print(f"\n🎉 批量同步完成！共成功排入 {total_added} 個標準工作行程區塊。")

if __name__ == "__main__":
    # 從明天 2026-10-25 (週日) 開始排入接下來 7 天
    start = date(2026, 10, 25)
    sync_schedule_range(start_date=start, days=7)
