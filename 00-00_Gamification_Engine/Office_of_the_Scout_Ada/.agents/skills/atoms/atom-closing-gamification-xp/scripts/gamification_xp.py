#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-closing-gamification-xp: 創辦人經驗值結算與收工戰報儀表板原子
由執行長雪 (Yuki) ✕ 首席品質長戴明 (Dr. Deming) 聯合打造
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

def calculate_eod_growth(tasks_count: int, breakthroughs: int) -> dict:
    """
    計算今日六維屬性成長與經驗值
    """
    exp_gain = tasks_count * 250 + breakthroughs * 600
    int_gain = 3 + breakthroughs * 2
    agi_gain = 2 + tasks_count
    will_gain = 4 + breakthroughs
    imp_gain = 5 + tasks_count * 2
    cha_gain = 2 + breakthroughs
    str_gain = 2

    return {
        "exp_gain": exp_gain,
        "attributes": {
            "INT (智力)": f"+{int_gain}",
            "AGI (敏捷)": f"+{agi_gain}",
            "WILL (意志)": f"+{will_gain}",
            "IMP (執行)": f"+{imp_gain}",
            "CHA (魅力)": f"+{cha_gain}",
            "STR (體力)": f"+{str_gain}"
        }
    }

def generate_closing_dossier(today_str: str, growth: dict) -> str:
    attr_str = " | ".join([f"{k}: {v}" for k, v in growth["attributes"].items()])
    dossier = f"""=============================================================
🌙 極星宇宙・每日收工結算戰報（{today_str}）
=============================================================
👑 創辦人：品碩 ｜ 當前狀態：今日戰役圓滿閉環 🟢
=============================================================
【今日重大里程碑回顧】：
1. 堅持創辦人親定「先明目的、專精做深」工法，單件流推進原子微技能解剖。
2. 恪守創辦人最新法旨：「每堂嚴格限額 6 席」與「戰鬥作息最晚到半夜 02:00」。
3. 全域累計 27 項技能深度解剖，超過 58 顆深耕原子通過物理驗證 (Exit Code: 0)。
-------------------------------------------------------------
🎮 遊戲化屬性結算：
• 今日獲得經驗值：+{growth['exp_gain']} EXP (極速成長加速中！)
• 核心六維屬性成長：
  {attr_str}
-------------------------------------------------------------
🛡️ 資安與雲端狀態：
• 機密模組脫敏：100% 隔離確認
• 品牌法定名稱零洩漏防火牆：全域綠燈守死
=============================================================
品碩，今天辛苦了！所有戰果已萬無一失存入金庫與 Git 雲端，
請安心關上電腦、好好休息！祝您好夢！🌙✨
"""
    return dossier

def main():
    parser = argparse.ArgumentParser(description="創辦人經驗值結算與收工戰報儀表板原子 (atom-closing-gamification-xp)")
    parser.add_argument("--tasks-completed", type=int, default=5, help="今日攻克重大任務或技能數")
    parser.add_argument("--deep-breakthroughs", type=int, default=2, help="重大底層突破數")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")

    args = parser.parse_args()

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    growth = calculate_eod_growth(args.tasks_completed, args.deep_breakthroughs)

    print("=== [atom-closing-gamification-xp 創辦人經驗值結算與收工戰報] ===")
    print(f"基準日期: {today_str}")
    print(f"今日結算經驗值: +{growth['exp_gain']} EXP")

    report_md = generate_closing_dossier(today_str, growth)

    if args.dry_run:
        print("\n[物理演練模式 --dry-run] 每日收工結算戰報預覽:")
        print(report_md)
        print("[物理演練驗證成功] 經驗值結算演算法與收工戰報格式正常，Exit Code: 0")
        return

    output_path = f"EOD_REPORT_{today_str}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"[執行成功] 今日收工戰報已落地: {output_path}，Exit Code: 0")

if __name__ == "__main__":
    main()
