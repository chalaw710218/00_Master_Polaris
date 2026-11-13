#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/bulletproof_clause.py
生活管家高情商防彈合約與防勒索客服話術引擎
落地防彈衣四大鐵律、二次出勤加收通知、客戶嫌貴高情商溝通與品牌零洩漏審查
"""

import sys
import argparse
from typing import Dict, Any

sys.stdout.reconfigure(encoding='utf-8')

FORBIDDEN_BRAND_TERMS = ["極星", "Polaris", "polaris", "POLARIS"]

def generate_bulletproof_quotation(service_name: str, service_price: int, item_advance: int = 0) -> str:
    """生成兼具溫度與法律/營運防彈衣之生活管家明碼報價單"""
    total = service_price + item_advance
    advance_note = f"• 代墊商品貨款：NT$ {item_advance:,} 元 (憑店家實體發票或免用統一發票收據實報實銷)\n" if item_advance > 0 else ""

    quote = f"""【生活管家 服務確認與明碼預約單】
感謝您的託付！為守護雙方權益與服務品質，為您呈報本次服務明細：

📋【費用明細】
• 委託項目：{service_name}
• 管家專業服務費：NT$ {service_price:,} 元
{advance_note}----------------------------------------
💰 本次合計預估：NT$ {total:,} 元

🛡️【貼心服務約定（防彈安心條款）】
1. 【實報實銷完全透明】：代買商品均憑發票或店家收據實報實銷，款項與管家勞務費分立計算。
2. 【現場等候 5 分鐘上限】：管家抵達現場後將主動致電聯繫，若因故未能接聽，現場等候上限為 5 分鐘。若需二次出勤配送，將酌收 NT$ 100~150 元二次交通補貼。
3. 【安心守護保證】：低溫生鮮保溫箱全程防護，專人送達，給您最從容的生活守護！

生活的一部分，就醬點！ 敬上"""
    return quote

def generate_timeout_second_dispatch_notice(customer_name: str, wait_minutes: int = 6) -> str:
    """生成現場等候超時之溫暖且堅定二次出勤通知"""
    return f"""{customer_name} 您好：
生活管家已抵達約定地址，並於現場等候約 {wait_minutes} 分鐘且多次嘗試電話聯繫，目前暫時無法與您或收件人取得聯繫。

為確保其他長輩與委託案件準時送達，管家目前已先將您的物品妥善收存（低溫商品均保溫保鮮保管）。
稍後您方便時請隨時於此留言告知，我們將為您重新排程安排【二次出勤配送】（將酌收 NT$ 100 元二次出勤交通補貼），請您完全放心！

生活的一部分，就醬點！ 生活管家關心您"""

def generate_high_eq_objection_handling(objection_type: str = "expensive") -> str:
    """客戶嫌貴或質疑價格時之高情商常民話術"""
    if objection_type == "expensive":
        return """「大哥/大姐您好！完全能理解您的考量～
一般的跑腿外送可能只是把東西丟在門口；但生活管家是專人為您到現場挑選品質最好的生鮮/物品，全程低溫保鮮裝箱，幫您排隊等候，並親手交給長輩或家人。
我們收取的費用，實質上是幫您把『排隊時間、路程風險、挑貨眼光與長輩安全』全包下來。很多熟客都說，省下這一個多小時陪家人或好好休息，這份安心真的非常值得！」"""
    else:
        return """「您好！生活管家的所有服務均為透明明碼標價，每一次出勤都有完整的低溫防護與專人責任。若您本次有預算考量，我們也可以為您調整為離峰常規配送，讓您用最合適的方式享受管家守護！」"""

def inspect_brand_redline(text: str) -> bool:
    """出廠前品牌法定名稱零洩漏防火牆審查"""
    for forbidden in FORBIDDEN_BRAND_TERMS:
        if forbidden in text:
            return False
    return True

def main():
    parser = argparse.ArgumentParser(description="生活管家高情商防彈合約與防勒索客服話術引擎")
    parser.add_argument("--service-name", type=str, default="跨區生鮮採買與長輩到府交付", help="服務名稱")
    parser.add_argument("--price", type=int, default=380, help="管家服務費")
    parser.add_argument("--item-value", type=int, default=1250, help="代墊商品費用")
    parser.add_argument("--type", type=str, default="quote", choices=["quote", "timeout", "handling"], help="話術類型")
    parser.add_argument("--dry-run", action="store_true", help="執行防彈話術模擬")
    args = parser.parse_args()

    if args.type == "quote":
        content = generate_bulletproof_quotation(args.service_name, args.price, args.item_value)
    elif args.type == "timeout":
        content = generate_timeout_second_dispatch_notice("陳大哥", 6)
    else:
        content = generate_high_eq_objection_handling("expensive")

    # 品牌紅線審查
    is_safe = inspect_brand_redline(content)
    if not is_safe:
        print("==================================================")
        print("🛑 戴明安燈拉繩！話術出現內部代號「極星」，出廠阻斷！")
        print("==================================================")
        sys.exit(1)

    print("==================================================")
    print(f"🛡️ 生活管家高情商防彈話術生成完畢 (Exit Code: 0) - [{args.type}]")
    print("--------------------------------------------------")
    print(content)
    print("--------------------------------------------------")
    print("✅ 品牌法定名稱防火牆審查: 100% 通過 (對外自稱生活管家，零洩漏內部代號)")
    print("✅ 防勒索機制: 白紙黑字載明 5 分鐘等候上限與二次出勤補貼，保障利潤底線")
    print("==================================================")

if __name__ == "__main__":
    main()
