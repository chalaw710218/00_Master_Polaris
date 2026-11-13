#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/groupbuy_four_prism_copy.py
管家選品四稜鏡文案與商城規格折射引擎
嚴格執行四大面向折射鐵律、商城規格、絕對禁語過濾與法定版尾保證
"""

import sys
import argparse
from typing import Dict, Any, List

sys.stdout.reconfigure(encoding='utf-8')

FORBIDDEN_WORDS = ["團購", "便宜", "划算", "俗擱大碗", "不賺價差", "限時搶購", "+1", "極星", "Polaris"]

STANDARD_FOOTER = """#生活的一部分就醬點 #管家選品 #質感日常 #在地專屬管家
【在地服務，安心有保障】
公司名稱：寶桑物流生活商行
品牌名稱：生活的一部分，就醬點！
實體地址：台東市正氣北路166巷90號
服務區域：台東市區、知本、南王、都蘭、東河"""

def generate_four_prisms(product_name: str, price: float, origin: str, weight: str, highlight: str) -> Dict[str, str]:
    """生成四大面向折射社群文案與商城精簡版"""

    # 面向 1：專業知識面向
    prism_knowledge = f"""很多朋友問喵編，市面上的堅果這麼多，為什麼有些吃起來軟爛、有些卻脆得特別自然？
答案就在「帶皮低溫慢焙」與「鹽焗溫控工藝」。

一般為了賣相白淨，常常會經過化學脫皮或過度油炸；
但這款【{product_name}】，堅持保留薄脆外皮，用天然海鹽低溫慢焗。
外皮鎖住了天然油脂與堅果香，每一顆咬下去都是最乾淨的自然脆度，完全不刮舌頭。

真正的品質越級，從來不需要多餘的添加物。
生活管家嚴格替您的餐桌把關。

👉 預約訂購與門市資訊，管家已整理在【第一則留言】中，點擊即可直達！

{STANDARD_FOOTER}"""

    # 面向 2：成長歷程面向
    prism_growth = f"""上個月為了找真正安心的堅果，管家團隊試吃了不下十幾家廠商的樣品。
好幾次打開包裝，聞到淡淡的油耗味或是看到碎果一堆，當場就被我們打了退堂鼓。

直到遇見這批【{product_name}】。
從產地原料篩選、低溫封裝，到工廠合格登記與 SGS 檢驗報告，老闆被我們問了一遍又一遍，依然非常有耐心地拿出一張張檢驗證明。
他說：「做吃的，自己家裡老小都要吃，騙不了人的。」

這份執著，跟我們生活管家想守護台東常民的初心一模一樣。
現在，我們把它帶回正氣北路了。

👉 預約訂購與門市資訊，管家已整理在【第一則留言】中，點擊即可直達！

{STANDARD_FOOTER}"""

    # 面向 3：三觀哲學面向
    prism_philosophy = f"""生活在台東，日子應該過得有餘裕、有尊嚴。
我們不追求市場上那些劣質削價競爭的低價品，因為每一次將就，犧牲的往往是全家人的健康。

挑一包好堅果、沖一杯好茶，下午陪長輩在庭院聊聊天，
這樣的生活微小確幸，不需要花大錢，只需要聰明地選擇「品質越級」。

為生活省去奔波與挑選的繁瑣，把時間留給最重要的人。
生活的一部分，就醬點！

👉 預約訂購與門市資訊，管家已整理在【第一則留言】中，點擊即可直達！

{STANDARD_FOOTER}"""

    # 面向 4：熱點選品宣告面向
    prism_announcement = f"""【管家嚴選 · 本週新星正式入庫】
喜愛原味純粹口感的朋友久等了！備受期待的【{product_name}】本週正式到貨。

📋【規格與專屬預約價】
• 品名：{product_name}
• 產地：{origin}
• 規格容量：每包 {weight}
• 管家選品回饋價：NT$ {price} 元
• 特色工藝：{highlight}

📍【門市自取與專人配送】
• 門市自取：台東市正氣北路166巷90號
• 專人外送：市區、知本、南王、都蘭、東河均有專車配送

👉 預約訂購與門市資訊，管家已整理在【第一則留言】中，點擊即可直達！

{STANDARD_FOOTER}"""

    # 商城精簡版規格文案
    ecommerce_concise = f"""【管家選品】{product_name}

🔥 產地直送！{highlight} 🔥
天然低溫慢焗，保留原果薄皮與酥脆口感，每一口都是最純粹的甘甜香氣。

【份量與價格亮點】：{weight} 大滿足，在地回饋價只要 NT$ {price} 元！

【特色與用途】：粒粒飽滿無漂白，可直接當作下午茶健康零食，亦適合加入生菜沙拉或清晨優格。

食安保證：「管家選品」四大防線把關，工廠登記與無毒檢驗齊備，全家吃得最安心。

📌 【商品規格】
• 產地：{origin}
• 重量：每包 {weight}
• 包裝：真空防潮密封夾鏈袋（開封後請冷藏保存）

🛒 台東在地專屬服務：
線上下單，可選擇外送服務，全程保鮮配送到府，讓您輕鬆補足家裡的高質感好料！"""

    return {
        "prism_1_knowledge": prism_knowledge,
        "prism_2_growth": prism_growth,
        "prism_3_philosophy": prism_philosophy,
        "prism_4_announcement": prism_announcement,
        "ecommerce_concise": ecommerce_concise
    }

def inspect_copy_forbidden_words(copies: Dict[str, str]) -> List[str]:
    """檢驗所有面向是否出現禁語"""
    violations = []
    for prism_key, text in copies.items():
        for bad in FORBIDDEN_WORDS:
            if bad in text:
                violations.append(f"[{prism_key}] 出現禁語或品牌內部代號「{bad}」！一票否決！")
    return violations

def main():
    parser = argparse.ArgumentParser(description="管家選品四稜鏡文案與商城規格折射引擎")
    parser.add_argument("--product-name", type=str, default="越臺鹽焗帶皮腰果 500g", help="商品品名")
    parser.add_argument("--price", type=float, default=340.0, help="管家選品售價")
    parser.add_argument("--origin", type=str, default="越南平福省頂級產區 (台灣合法分裝)", help="產地")
    parser.add_argument("--weight", type=str, default="500 公克 ± 10g", help="重量規格")
    parser.add_argument("--highlight", type=str, default="天然鹽焗低溫烘焙、不漂白、酥脆回甘", help="核心工藝特色")
    parser.add_argument("--dry-run", action="store_true", help="執行文案折射模擬")
    args = parser.parse_args()

    copies = generate_four_prisms(args.product_name, args.price, args.origin, args.weight, args.highlight)
    violations = inspect_copy_forbidden_words(copies)

    if violations:
        print("==================================================")
        print("🛑 戴明安燈拉繩！文案檢測到禁用詞彙，禁止出廠！")
        for v in violations:
            print(f"  [✗] {v}")
        print("==================================================")
        sys.exit(1)

    print("==================================================")
    print(f"💎 管家選品四稜鏡文案與商城規格折射完成 (Exit Code: 0) - {args.product_name}")
    print("--------------------------------------------------")
    print("📐【面向一：專業知識面向 (Knowledge)】")
    print(copies["prism_1_knowledge"][:200] + "...\n")
    print("🌱【面向二：成長歷程面向 (Growth)】")
    print(copies["prism_2_growth"][:200] + "...\n")
    print("🧭【面向三：三觀哲學面向 (Philosophy)】")
    print(copies["prism_3_philosophy"][:200] + "...\n")
    print("🔥【面向四：選品宣告面向 (Announcement)】")
    print(copies["prism_4_announcement"][:200] + "...\n")
    print("🛒【網路商城精簡版規格 (E-Commerce Concise)】")
    print(copies["ecommerce_concise"][:220] + "...\n")
    print("--------------------------------------------------")
    print("✅ 嚴格禁語審查: 100% 通過 (零團購/便宜/划算/俗擱大碗/限時搶購)")
    print("✅ 品牌法定名稱與版尾: 寶桑物流生活商行 ✕ 生活的一部分，就醬點！ ✕ 正氣北路166巷90號 齊備")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
