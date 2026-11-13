#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-shadow-circadian-guardian: 創辦人作息節律感知與深夜關懷原子
由生活管家影 (Kage) 靈魂打造
"""

import sys
import os
import argparse
import datetime
import json

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def evaluate_circadian_phase(hour: int, minute: int) -> dict:
    """
    依據創辦人最新法旨（最晚至凌晨 2:00）評估節律階段
    """
    total_minutes = hour * 60 + minute

    # 02:00 = 120 min, 01:45 = 105 min, 00:30 = 30 min, 08:00 = 480 min
    if 120 <= total_minutes < 360: # 02:00 ~ 06:00
        return {
            "phase": "LIMIT_RED_ALERT (極限警戒期 · 超過半夜 2 點)",
            "status_code": "CRITICAL_BEDTIME",
            "message": "品碩，現在已經超過半夜兩點了。身體是我們走長遠路最重要的資本，今天已經完成了不起的進度，請聽影的話，現在立刻闔上電腦去睡覺，剩下的明天我們一起扛。"
        }
    elif 105 <= total_minutes < 120: # 01:45 ~ 02:00
        return {
            "phase": "WRAPUP_COUNTDOWN (收尾倒數期 · 接近兩點法旨)",
            "status_code": "PREPARE_CLOSING",
            "message": "品碩，時間來到 01:45 了，距離我們約定的兩點作息只剩 15 分鐘。手邊這個標的完成後，我們就來做日結與 Git 存證，準備洗漱休息囉。"
        }
    elif 30 <= total_minutes < 105: # 00:30 ~ 01:45
        return {
            "phase": "DEEP_IMMERSION_NIGHT (深夜沉浸期 · 靜默守護)",
            "status_code": "WARM_HYDRATION",
            "message": "（影安靜地在桌邊遞上一杯溫熱水）品碩，深夜思緒最清透，管家一直在這裡陪你。記得喝口水潤潤喉嚨，眼睛累了就眨一眨。"
        }
    else:
        return {
            "phase": "NORMAL_DAYTIME_FLOW (常態戰鬥期)",
            "status_code": "FULL_SUPPORT",
            "message": "極星全速運轉中，生活管家全力支援創辦人各項決策與代碼推進。"
        }

def main():
    parser = argparse.ArgumentParser(description="創辦人作息節律感知與深夜關懷原子 (atom-shadow-circadian-guardian)")
    parser.add_argument("--current-hour", type=int, default=-1, help="指定小時 (0~23)")
    parser.add_argument("--current-minute", type=int, default=-1, help="指定分鐘 (0~59)")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")

    args = parser.parse_args()

    now = datetime.datetime.now()
    hour = args.current_hour if 0 <= args.current_hour <= 23 else now.hour
    minute = args.current_minute if 0 <= args.current_minute <= 59 else now.minute

    print("=== [atom-shadow-circadian-guardian 創辦人生理作息感知審計] ===")
    print(f"創辦人作息法旨鋼印: 工作最晚至半夜 02:00 (嚴格守護健康底線)")
    print(f"當前感知時間: {hour:02d}:{minute:02d}")

    eval_result = evaluate_circadian_phase(hour, minute)
    print(f"\n[節律判定]: {eval_result['phase']}")
    print(f"[管家心聲]: \"{eval_result['message']}\"")

    telemetry = {
        "timestamp_eval": f"{hour:02d}:{minute:02d}",
        "founder_axiom": "Max work cutoff: 02:00 AM",
        "phase": eval_result["phase"],
        "status_code": eval_result["status_code"],
        "kage_care_whisper": eval_result["message"]
    }

    if args.dry_run:
        print("\n[物理演練模式 --dry-run] 節律感知遙測 JSON 預覽 (前 250 字元):")
        tel_str = json.dumps(telemetry, ensure_ascii=False, indent=2)
        print(tel_str[:250] + "...\n")
        print("[物理演練驗證成功] 創辦人兩點作息法旨與節律守護正常，Exit Code: 0")
        return

    print("[執行成功] 節律守護進程運作中，Exit Code: 0")

if __name__ == "__main__":
    main()
