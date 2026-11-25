#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/course_syllabus_scaffolder.py
實體工作坊教案規格與 10 題防呆表單裝配引擎
完全遵循創辦人最新法旨：【純實體小班 · 每堂嚴格限額 6 席】
"""

import sys
import json
import argparse
from typing import Dict, Any, List

sys.stdout.reconfigure(encoding='utf-8')

STANDARD_SEATS = 6 # 創辦人親定最新法旨：每堂嚴格限額 6 席

FORM_QUESTIONS_SCHEMA = [
    {"qid": 1, "title": "學員姓名", "type": "SHORT_TEXT", "required": True},
    {"qid": 2, "title": "聯絡 Email（本課程唯一核心通知憑證，Google 日曆將以此發送邀請）", "type": "SHORT_TEXT", "required": True},
    {"qid": 3, "title": "聯絡手機號碼（課前 24 小時簡訊/LINE 點名確認）", "type": "SHORT_TEXT", "required": True},
    {"qid": 4, "title": "您的身分資格", "type": "MULTIPLE_CHOICE", "options": ["老學員回娘家（享學費 0 元免單）", "全新夥伴實戰價（單堂 NT$ 500 元）"], "required": True},
    {"qid": 5, "title": "自備筆記型電腦型號與作業系統", "type": "SHORT_TEXT", "required": True},
    {"qid": 6, "title": "【硬體與環境自檢】請確認以下 4 項皆已備妥：", "type": "CHECKBOXES", "options": ["已安裝 Google Chrome 瀏覽器", "確定記得自己的 Google 帳號與密碼", "已確認筆電可正常連上 Wi-Fi", "當天會自備筆電充電器與延長線"], "required": True},
    {"qid": 7, "title": "您的產業與職稱（如：餐飲店長、旅宿老闆、行政公務、自由工作者）", "type": "SHORT_TEXT", "required": True},
    {"qid": 8, "title": "本次課堂您最想帶來的『真實業務資料痛點』是什麼？", "type": "PARAGRAPH", "options": ["菜單設計與商品文案", "繁瑣進貨單與廠商對帳表", "冗長公文與法規摘要", "海量客戶常見問題與客服紀錄"], "required": True},
    {"qid": 9, "title": "【實體入席承諾】每堂嚴格僅限額 6 席，您是否承諾若獲錄取必準時出席？", "type": "MULTIPLE_CHOICE", "options": ["是，我承諾準時出席並自備筆電實作", "時間未定，若有名額請先聯絡我"], "required": True},
    {"qid": 10, "title": "【分流意願】若本場次 6 席名額已滿，您是否願意保留至【第二梯次加開場】優先遞補？", "type": "MULTIPLE_CHOICE", "options": ["願意，請將我列入第二梯次加開場優先名單", "先不用，謝謝"], "required": True}
]

def scaffold_course_package(title: str, date_str: str, time_str: str = "14:00 - 16:00") -> Dict[str, Any]:
    """裝配完整的課程教案規格、10 題表單 Schema 與招生文案"""

    # 招生貼文 (FB 溫暖長文，零外連防降權)
    marketing_copy = f"""生活在台東，工作與業務總是有忙不完的繁瑣雜事。
進貨單對帳花上一整個下午、菜單與商品介紹文案想破頭、
或是手上堆滿了長篇公文與客戶資料，不知道如何快速整理成重點。

生活管家創辦人（闆仔）親自開班，把我們日常營運在跑的實戰工具，毫無保留手把手教給大家。
這堂課我們堅持【純實體現場教學 · 每堂嚴格限額 {STANDARD_SEATS} 席】，絕無線上同步！
因為只有在現場看著你的筆電螢幕，巡桌一步步幫你排錯，
才能保證你帶著自己的真實業務資料，做出一模一樣的成品才准下課！

👉 實體席位申請表與門市導航，管家已整理在【第一則留言】中，點擊即可直達！"""

    # 第一則留言置頂
    first_comment = f"""🐾 《{title}》實體手把手工作坊
📅 時間：{date_str}（週三）{time_str}
📍 地點：生活管家家宅總部（台東市正氣北路166巷90號）
⚠️ 席位嚴格限額：【每堂僅限 {STANDARD_SEATS} 席】（額滿即關門，依表單硬體準備度審查入席）

📝 實體入席審查表：[點此填寫 Google 表單]
👑 老學員回娘家：表單內勾選「老學員」即享學費 0 元免單！
🌟 全新夥伴實戰價：單堂 NT$ 500 元（審查通過後發送正式日曆邀請）

💬 官方 LINE 諮詢：https://lin.ee/z83YSq6"""

    return {
        "title": title,
        "date": date_str,
        "time": time_str,
        "capacity": STANDARD_SEATS,
        "location": "台東市正氣北路166巷90號 (生活管家家宅總部)",
        "pricing": {
            "regular": 500,
            "alumni": 0,
            "currency": "NT$"
        },
        "curriculum_120m": [
            {"time": "14:00 - 15:00", "phase": "核心實戰精講", "content": "痛點拆解、心智模型、作戰紙現場拆解"},
            {"time": "15:00 - 16:00", "phase": "巡桌手把手實作排錯", "content": "學員自備筆電實操、逐一達成 3 個 Checkpoints (沒做出成品不准下課)"},
            {"time": "16:00 - 16:05", "phase": "3分鐘 NPS 與續報閉環", "content": "成果拍照存證、下一講優先席位預約"}
        ],
        "form_schema_10_questions": FORM_QUESTIONS_SCHEMA,
        "marketing_copy": marketing_copy,
        "first_comment": first_comment
    }

def main():
    parser = argparse.ArgumentParser(description="實體工作坊教案規格與 10 題防呆表單裝配引擎")
    parser.add_argument("--title", type=str, default="AI 實戰業務提效工作坊", help="課程主題名稱")
    parser.add_argument("--date", type=str, default="2026-11-25", help="上課日期 (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="執行教案與表單裝配模擬")
    args = parser.parse_args()

    pkg = scaffold_course_package(args.title, args.date)

    print("==================================================")
    print(f"🎓 實體工作坊教案規格裝配完成 (Exit Code: 0) - 《{pkg['title']}》")
    print(f"上課時程: {pkg['date']} {pkg['time']} | 實體上課地點: {pkg['location']}")
    print(f"👉 席位法旨: 【每堂嚴格限額 {pkg['capacity']} 席】 (極致手把手小班深度排錯)")
    print(f"收費定價: 全新學員 NT$ {pkg['pricing']['regular']} 元 ｜ 老學員回娘家 NT$ {pkg['pricing']['alumni']} 元免單")
    print("--------------------------------------------------")
    print("⏳ 120 分鐘雙核課綱架構:")
    for c in pkg["curriculum_120m"]:
        print(f"  - [{c['time']}] {c['phase']}: {c['content']}")
    print("--------------------------------------------------")
    print(f"📋 10 道防呆 Google 表單 Schema 已就緒 (共 {len(pkg['form_schema_10_questions'])} 題):")
    print("  [✓] 必考題：Email 核心憑證、身分資格、筆電自備自檢、業務資料痛點、入席承諾、加開場意願")
    print("--------------------------------------------------")
    print("💬 Facebook 招生長文與第一則留言已就緒 (零外連防降權閉環)")
    print("==================================================")

if __name__ == "__main__":
    main()
