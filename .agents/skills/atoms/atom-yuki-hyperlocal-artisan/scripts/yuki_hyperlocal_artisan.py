#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-yuki-hyperlocal-artisan: 台東微型實體生態守護與非標服務產品化原子腳本
專職負責執行長雪 (Yuki) 台東在地守護新律（紅外治未病、工具共享客流、修容回憶錄）工單封裝。
"""

import sys
import os
import argparse
import json
from datetime import datetime

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def generate_hyperlocal_work_order(service_type: str, client_name: str, tool_name: str = None, neighbor: str = None) -> dict:
    """生成台東在地微型商業生態守護工單"""
    today_str = datetime.now().strftime("%Y%m%d")
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    if service_type == "thermal":
        order_id = f"THM-{today_str}-01"
        title = "大醫治未病 · 居家配電盤紅外熱像儀預防檢測工單"
        checklist = [
            "1. 總開關無熔絲開關（NFB）接線端子紅外測溫（標準 < 55°C，> 60°C 即刻鎖緊）",
            "2. 冷氣、電熱水器高功耗分路端子測溫",
            "3. 漏電斷路器（ELCB）物理測試按鈕跳脫功能確證",
            "4. 弱電箱與 Wi-Fi 變壓器發熱排風檢查"
        ]
        value_proposition = "花 5 分鐘消除電線走火隱患，賣給家庭的是一輩子的安寧，而非事後滅火！"
        assigned_artisan = "生活管家 · 居安巡檢專員"

    elif service_type == "tool_share":
        order_id = f"TLS-{today_str}-01"
        tool = tool_name if tool_name else "喜利得衝擊式電鑽箱"
        target_neighbor = neighbor if neighbor else "台東在地友店/鄰舍"
        title = f"客流工具共享零成本槓桿登錄 · 【{tool}】出借卡"
        checklist = [
            f"1. 工具品項確證：{tool}（配件齊全、電池充飽）",
            f"2. 借用對象登記：{target_neighbor}（免押金、無償出借）",
            "3. 進門接觸點建立：歸還時主動關心修繕成果，了解生鮮或家政需求",
            "4. 轉化機會備註：探詢友店員工餐或家庭食材團購需求"
        ]
        value_proposition = "一台 2,000 元工具出借 50 次，換來 50 次真實進門信任，轉化高毛利訂單！"
        assigned_artisan = "生活管家 · 友店關係經理"

    elif service_type == "grooming_history":
        order_id = f"MEM-{today_str}-01"
        title = "高齡尊嚴修容與口述傳家回憶錄工單"
        checklist = [
            "1. 舒爽修容：溫熱毛巾敷臉、鬢角鬢毛細軟修整、修整指甲",
            "2. 傾聽採訪：紀錄長輩早年開拓台東風土之口述故事（錄音 20 分鐘）",
            "3. 食療暖胃：提供一小盅熱騰騰成功港老薑黑潮旗魚原湯",
            "4. 外地兒女反饋：拍攝長輩清爽燦爛笑容生活照，附於安心圖卡發送"
        ]
        value_proposition = "肉體照護有極限，心靈尊嚴無止境；為老農家族留下不可磨滅的傳家史詩！"
        assigned_artisan = "生活管家 · 暖心陪伴工匠"

    else:
        order_id = f"ENG-{today_str}-01"
        title = "自提站平戰結合社區儲能與應急微光綠洲檢核"
        checklist = [
            "1. 離峰夜充日放充放電排程核驗",
            "2. 儲能電池健康度 (SOH >= 95%) 確證",
            "3. 颱風斷電 72 小時應急手機充電排插與微光照明測試"
        ]
        value_proposition = "平時賺取電價差回收成本，災時成為整條街區的生命微光綠洲！"
        assigned_artisan = "生活管家 · 能源站守護員"

    return {
        "order_id": order_id,
        "title": title,
        "client_or_neighbor": client_name if client_name else "台東在地住戶",
        "created_at": timestamp_str,
        "assigned_artisan": assigned_artisan,
        "value_proposition": value_proposition,
        "checklist": checklist
    }

def main():
    parser = argparse.ArgumentParser(description="台東微型實體生態守護工單生成原子")
    parser.add_argument("--service-type", type=str, choices=["thermal", "tool_share", "grooming_history", "energy"], default="thermal", help="守護服務類型")
    parser.add_argument("--client-name", type=str, default="寶桑路陳老伯伯", help="服務對象或住戶")
    parser.add_argument("--tool-name", type=str, default="喜利得四溝衝擊電鑽組", help="工具名稱")
    parser.add_argument("--neighbor", type=str, default="光明路早午餐友店", help="友店名稱")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")

    args = parser.parse_args()

    print("=== [atom-yuki-hyperlocal-artisan] 台東微型實體生態守護工單生成 ===")
    res = generate_hyperlocal_work_order(
        service_type=args.service_type,
        client_name=args.client_name,
        tool_name=args.tool_name,
        neighbor=args.neighbor
    )

    print(f"\n📋 **【工單編號：{res['order_id']}】**")
    print(f"服務項目: {res['title']}")
    print(f"服務對象: {res['client_or_neighbor']} | 派工專員: {res['assigned_artisan']}")
    print(f"核心價值: {res['value_proposition']}")
    print("\n執行檢驗清單:")
    for item in res["checklist"]:
        print(f"  {item}")

    print("\n[+] 台東在地微型守護工單封裝完成 (Exit Code: 0)！")
    sys.exit(0)

if __name__ == "__main__":
    main()
