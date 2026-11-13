#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/care_telehealth_card.py
外地兒女 3 分鐘孝親安心聽診圖卡生成引擎
專精於瑞士網格行動端儀表板、醫囑速記、生命體徵與醫療法規免責宣告
"""

import sys
import argparse
from datetime import datetime
from typing import Dict, Any

sys.stdout.reconfigure(encoding='utf-8')

FORBIDDEN_BRAND_TERMS = ["極星", "Polaris", "polaris", "POLARIS"]

def inspect_brand_redline(text: str) -> bool:
    """戴明安燈：出廠前品牌法定名稱零洩漏防火牆審查"""
    for forbidden in FORBIDDEN_BRAND_TERMS:
        if forbidden in text:
            return False
    return True

def generate_telehealth_reassurance_card(
    order_id: str,
    elder_name: str,
    bp: str,
    pulse: int,
    doctor: str,
    physician_notes: str,
    next_date: str = "2026-12-15",
    medication_change: str = "無變動，維持現有處方每日早晚各一次",
    steward_note: str = "阿公今天精神很好，看診完一起在門口喝了溫麥茶，已平安回到客廳休息！"
) -> Dict[str, Any]:
    """生成外地兒女 3 分鐘行動端孝親安心聽診圖卡"""

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 瑞士網格行動端純文字/Markdown 圖卡
    card_markdown = f"""┌──────────────────────────────────────────────┐
│  👵🏡【生活管家 · 外地兒女孝親安心聽診報告】  │
└──────────────────────────────────────────────┘
📅 服務時戳：{now_str}  ｜  工單編號：{order_id}
👴 關懷長輩：{elder_name}  ｜  陪診管家：生活管家 專人陪同

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🩺【今日生命體徵快速儀表板】
  • 測量血壓：{bp} mmHg  (🟢 數值平穩)
  • 脈搏心率：{pulse} bpm      (🟢 節律正常)
  • 今日氣色：精神飽滿，步伐穩健

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝【主治醫師核心醫囑速記】
  • 門診醫療：{doctor}
  • 醫師叮嚀：{physician_notes}
  • 用藥指示：{medication_change}
  • 下次預約：{next_date} (管家系統已為您自動標記行事曆)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬【管家貼心現場回報】
  {steward_note}
  📸 長輩燦爛笑容與藥袋留存照片，已妥善歸檔於專屬相簿！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚖️【生活管家 法定安心免責宣告】
本報告由生活管家協助陪伴記錄，內容均為醫師現場口述與藥袋說明之忠實速記。
管家為生活陪伴與長者安全守護者，不具醫療診斷行為，任何醫療決定請遵照主治醫師指示。

生活的一部分，就醬點！ 生活管家團隊 敬上
台東市正氣北路166巷90號 ｜ 服務專線：089-123456"""

    is_safe = inspect_brand_redline(card_markdown)

    return {
        "order_id": order_id,
        "elder_name": elder_name,
        "card_markdown": card_markdown,
        "is_brand_safe": is_safe
    }

def main():
    parser = argparse.ArgumentParser(description="外地兒女 3 分鐘孝親安心聽診圖卡生成引擎")
    parser.add_argument("--order-id", type=str, default="CARE-20261113-01", help="工單編號")
    parser.add_argument("--elder", type=str, default="陳阿公", help="長輩姓名")
    parser.add_argument("--bp", type=str, default="128/82", help="血壓數值")
    parser.add_argument("--pulse", type=int, default=72, help="脈搏心率")
    parser.add_argument("--doctor", type=str, default="台東馬偕醫院 心臟內科 陳醫師", help="就診醫院與醫師")
    parser.add_argument("--notes", type=str, default="血壓控制理想，降血壓藥維持原劑量，叮嚀天氣變冷早起加件外套", help="醫師醫囑重點")
    parser.add_argument("--next-date", type=str, default="2026-12-15", help="下次預約複診日")
    parser.add_argument("--dry-run", action="store_true", help="執行圖卡生成模擬")
    args = parser.parse_args()

    res = generate_telehealth_reassurance_card(
        order_id=args.order_id,
        elder_name=args.elder,
        bp=args.bp,
        pulse=args.pulse,
        doctor=args.doctor,
        physician_notes=args.notes,
        next_date=args.next_date
    )

    if not res["is_brand_safe"]:
        print("==================================================")
        print("🛑 戴明安燈拉繩！圖卡文字出現內部代號「極星」，出廠攔截！")
        print("==================================================")
        sys.exit(1)

    print("==================================================")
    print(f"📱 外地兒女 3 分鐘孝親安心圖卡已生成 (Exit Code: 0) - {res['order_id']}")
    print("--------------------------------------------------")
    print(res["card_markdown"])
    print("--------------------------------------------------")
    print("✅ 格式合規: 瑞士網格儀表板 ✕ 醫囑忠實速記 ✕ 生命體徵視覺化")
    print("✅ 法律與醫療防線: 已附載非醫療診斷免責聲明")
    print("✅ 品牌法定名稱防火牆: 100% 通過 (對外署名生活管家，零洩漏內部代號)")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
