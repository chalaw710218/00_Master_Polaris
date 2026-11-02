#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Care Artisan CLI (生活管家·孝親安居與高齡溫暖服務封裝器 CLI)
提供孝親工單建立、5D 報價精算、與外地兒女安心聽診圖卡自動渲染。
"""

import sys
import os
import argparse
import json
from datetime import datetime

# Windows terminal encoding defense
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

MODULES = {
    "safety": {
        "name": "居安無憂·浴室防滑奈米塗層＋扶手＋配電熱像巡檢",
        "base_price": 2999,
        "tools": ["FLIR 紅外熱像儀", "304 不鏽鋼一字扶手", "德國奈米級隱形止滑劑", "水平儀", "衝擊電鑽"],
        "estimated_duration": "1.5 ~ 2 小時",
        "d_breakdown": {"D1工時": 120, "D2風險": 40, "D3專業": 50, "D4急迫": 10, "D5安心": 80}
    },
    "escort": {
        "name": "孝親暖心·長輩就醫陪診與 3 分鐘安心聽診圖卡",
        "base_price": 1200,
        "hourly_extra": 400,
        "tools": ["就診隨行筆記夾", "血壓記錄本", "水壺與保暖毯", "代步機車/代叫車隊"],
        "estimated_duration": "2 小時 (超時每小時 +400)",
        "d_breakdown": {"D1工時": 120, "D2風險": 20, "D3專業": 30, "D4急迫": 20, "D5安心": 100}
    },
    "grooming": {
        "name": "體面長青·臥床與行動不便長輩到府尊嚴修容",
        "base_price": 600,
        "tools": ["醫療級靜音集塵電剪", "純棉拋棄式圍兜", "草本軟鬚泡與安全刮刀", "溫和蘆薈潤膚露"],
        "estimated_duration": "45 ~ 60 分鐘",
        "d_breakdown": {"D1工時": 60, "D2風險": 15, "D3專業": 35, "D4急迫": 10, "D5安心": 70}
    },
    "memoir": {
        "name": "傳家之寶·老農口述歷史與一生回憶錄印製",
        "base_price": 6800,
        "tools": ["高音質立體聲錄音筆", "高解析度照片掃描儀", "布紋精裝硬殼本範樣", "刺蔥迎賓暖茶"],
        "estimated_duration": "兩次深度訪談 + 排版印製 (週期 14 天)",
        "d_breakdown": {"D1工時": 360, "D2風險": 10, "D3專業": 120, "D4急迫": 0, "D5安心": 150}
    },
    "nutrition": {
        "name": "暖胃風土·常溫燉湯與長輩低 GI 軟質養生膳 (每週套組)",
        "base_price": 750,
        "monthly_sub": 2800,
        "tools": ["寶桑物流冷熱溫控配送箱", "常溫高壓軟袋 (刺蔥排骨/剝皮辣椒雞)", "低 GI 洛神糙米糕"],
        "estimated_duration": "每週五定期隨車配送",
        "d_breakdown": {"D1工時": 30, "D2風險": 5, "D3專業": 20, "D4急迫": 0, "D5安心": 60}
    }
}

def list_modules():
    print("\n========================================================")
    print("生活管家 · 孝親安居五大旗艦模組目錄")
    print("========================================================")
    for code, m in MODULES.items():
        print(f"\n【模組代碼: {code}】 {m['name']}")
        print(f"  • 基準定價: NT$ {m['base_price']}")
        print(f"  • 預估工時: {m['estimated_duration']}")
        print(f"  • 配備工具: {', '.join(m['tools'])}")
        print(f"  • 5D 點數: {m['d_breakdown']}")

def create_order(args):
    code = args.type
    if code not in MODULES:
        print(f"錯誤：無效模組代碼 '{code}'。請使用 list 命令查看有效代碼。")
        sys.exit(1)

    m = MODULES[code]
    order_id = f"CARE-{datetime.now().strftime('%Y%m%d%H%M')}"
    total_price = m['base_price']
    if code == "escort" and args.hours and args.hours > 2:
        extra_hours = args.hours - 2
        total_price += int(extra_hours * m['hourly_extra'])

    order = {
        "order_id": order_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "module_code": code,
        "module_name": m["name"],
        "client_name": args.client or "外地委託人",
        "elder_name": args.elder or "台東在地長輩",
        "address": args.address or "台東市正氣北路周邊",
        "scheduled_time": args.time or datetime.now().strftime("%Y-%m-%d 14:00"),
        "estimated_hours": args.hours or 2,
        "total_price": total_price,
        "statutory_ledger": "生活管家_系統化管理_V2",
        "poka_yoke_checks": [
            "工作人員穿戴乾淨鞋套與管家制服",
            "現場照片記錄（未經授權絕不外流）",
            "施作/陪診前確認長輩身體狀況無急性不適",
            "服務完成後出示長輩確認並奉茶叮嚀",
            "30 分鐘內生成安心聽診/施工圖卡發送外地兒女"
        ]
    }

    output_dir = "00-03_Brand_LifeButler/00-03-05_Brand_Content_Hub/Care_Orders"
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{order_id}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(order, f, ensure_ascii=False, indent=2)

    print("\n========================================================")
    print(f"孝親工單建立成功！工單編號: {order_id}")
    print(f"• 服務項目: {m['name']}")
    print(f"• 委託兒女: {order['client_name']}")
    print(f"• 服務長輩: {order['elder_name']}")
    print(f"• 服務地址: {order['address']}")
    print(f"• 5D 結算金額: NT$ {total_price}")
    print(f"• 法定登記帳本: 《生活管家_系統化管理_V2》")
    print(f"• 工單檔案: {out_path}")
    print("========================================================\n")
    return order

def generate_card(args):
    order_id = args.order_id
    doctor = args.doctor or "馬偕醫院主治醫師"
    diagnosis = args.diagnosis or "血壓平穩，心肺功能正常，維持目前慢性病處方。"
    next_date = args.next_date or "未定"
    vitals = args.vitals or "血壓 128/82 mmHg ｜ 心跳 72 bpm"
    note = args.note or "阿公今天精神很好，陪診路上笑著說昨天晚上睡得很香，回程吃了管家帶的溫熱洛神糙米糕。"

    md_card = f"""# 💌 生活管家 · 孝親安心聽診回報卡 (Filial Care Report)

> **工單編號**：`{order_id}` ｜ **回報時間**：{datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **服務管家**：生活管家 陪伴專員 ✕ 寶桑物流 履約車隊  
> **法定唯一帳本**：登錄於《生活管家_系統化管理_V2》

---

### 🏥 醫院與主治醫師
* **看診院所**：{doctor}
* **生命體徵**：{vitals}

---

### 🩺 醫師重點叮嚀與醫囑 (3分鐘速覽)
* **核心診斷**：{diagnosis}
* **用藥調整**：維持原處方，早晚飯後服藥，隨行管家已協助核對藥袋並分裝標記。
* **下次複診預約**：**{next_date}**（生活管家已自動同步行事曆，屆時將提前一日提醒）。

---

### 🌸 今日長輩生活與心情札記
> *「{note}」*

---

### 🛡️ 守護承諾
您在遠方打拚，故鄉父母由生活管家替您溫柔守候。若有任何生活採買、冷氣清洗或水電檢測需求，隨時於官方 LINE 吩咐我們！

**生活的一部分，就醬點！**
"""

    output_dir = "00-03_Brand_LifeButler/00-03-05_Brand_Content_Hub/Care_Orders"
    os.makedirs(output_dir, exist_ok=True)
    card_path = os.path.join(output_dir, f"{order_id}_ReportCard.md")
    with open(card_path, "w", encoding="utf-8") as f:
        f.write(md_card)

    print("\n========================================================")
    print(f"安心聽診回報卡生成成功！")
    print(f"• 檔案路徑: {card_path}")
    print("• 可直接貼入 LINE 官方帳號推播給外地兒女！")
    print("========================================================\n")

def main():
    parser = argparse.ArgumentParser(description="Care Artisan CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="列出五大孝親安居旗艦模組")

    create_p = subparsers.add_parser("create-order", help="建立孝親工單")
    create_p.add_argument("--type", required=True, choices=["safety", "escort", "grooming", "memoir", "nutrition"], help="模組代碼")
    create_p.add_argument("--client", help="委託人姓名 (如: 台北陳小姐)")
    create_p.add_argument("--elder", help="長輩姓名 (如: 正氣北路陳阿公)")
    create_p.add_argument("--address", help="服務地址")
    create_p.add_argument("--time", help="服務時間")
    create_p.add_argument("--hours", type=float, help="時數")

    card_p = subparsers.add_parser("generate-card", help="產出孝親安心聽診圖卡")
    card_p.add_argument("--order-id", required=True, help="工單編號")
    card_p.add_argument("--doctor", help="醫師或醫院名稱")
    card_p.add_argument("--diagnosis", help="診斷與醫囑摘要")
    card_p.add_argument("--vitals", help="生理數值 (血壓/心跳)")
    card_p.add_argument("--next-date", help="下次預約時間")
    card_p.add_argument("--note", help="長輩心情與生活札記")

    args = parser.parse_args()
    if args.command == "list":
        list_modules()
    elif args.command == "create-order":
        create_order(args)
    elif args.command == "generate-card":
        generate_card(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
