#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/tactical_negotiator.py
供應商商業心理戰預判與高情商議價話術引擎
分析盤商心理動機、產出四步閉環高情商談判文本、落實品牌零洩漏審查
"""

import sys
import argparse
from typing import Dict, Any

sys.stdout.reconfigure(encoding='utf-8')

FORBIDDEN_BRAND_TERMS = ["極星", "Polaris", "polaris", "POLARIS"]

STRATEGY_TEMPLATES = {
    "panic_inflation": {
        "name": "破解恐慌性虛報溢價",
        "opponent_mindset": "對方操盤手試圖利用近期海運貨櫃或產地氣候新聞製造稀缺感，掩蓋其高達 20% 以上的隱形超額毛利。",
        "script": """「業務經理您好！非常感謝您第一時間為我們調配這批【{item_name}】的報價。
這陣子市場上確實有一些海運與產地浮動的雜音，不過我們固定每週都在追蹤國際大宗期貨與到港 CIF 落地常規成本。
以目前產地 FOB 與正常冷鏈關稅測算，每公斤 NT$ {quote_price} 元的開盤價，對終端常民推廣來說阻力確實偏大。
我們是台東正氣北路的實體門市與專屬生活管家，合作一向以穩定長效、現金週週清算為原則。
如果首批我們固定每週定量拉貨，希望能以 NT$ {target_price} 元的戰略底價配合，讓雙方把量能穩穩做大，您看是否能向公司爭取這個雙贏專案？」"""
    },
    "turnover": {
        "name": "針對庫存現金流週轉壓力",
        "opponent_mindset": "對方可能面臨冷凍庫存租金、臨期週轉或月結現金流壓力，表面強硬但實質上極度渴望快速變現。",
        "script": """「經理您好！我們仔細看過【{item_name}】這批貨的規格，品質維持得很棒。
我們很清楚目前倉儲冷凍與全台幹線調度的成本壓力，所以生活管家進貨一向不拖泥帶水、驗收即入庫、帳款準時結清。
與其讓好貨放在凍庫裡承擔折舊風險，不如讓我們在東部生活圈直接為您快速消化。
我們願意以 NT$ {target_price} 元的乾脆底價直接吃下這批配額，讓貴司立刻回籠現金流。這份誠意請經理評估一下，合適的話我們今天就安排派車！」"""
    },
    "testing_high": {
        "name": "化解試探性開高報價",
        "opponent_mindset": "對新合作通路採取慣性『試探性開高』，觀察採購方是否熟稔大盤行規與加工損耗細節。",
        "script": """「經理好！【{item_name}】這份報價我們研讀過了。
我們本身在生鮮冷鏈、失水率與修清耗損這塊都是長期實務操作的行家，對於大盤的利潤結構我們非常尊重，但也十分清楚各個環節的真實成本。
NT$ {quote_price} 元的試探價我們理解是常規開盤，但若要建立長期緊密的合作夥伴關係，我們期待看到具備競爭力的真實底牌。
我們評估後的健康進貨目標是 NT$ {target_price} 元。若是這個價格，我們能立刻列入生活管家每週的優先主推清單！」"""
    }
}

def inspect_brand_redline(text: str) -> bool:
    """戴明安燈：出廠前品牌法定名稱零洩漏防火牆審查"""
    for forbidden in FORBIDDEN_BRAND_TERMS:
        if forbidden in text:
            return False
    return True

def generate_tactical_negotiation(
    item_name: str,
    quote_price: float,
    target_price: float,
    strategy_key: str = "panic_inflation"
) -> Dict[str, Any]:
    """生成商業心理戰分析與高情商談判文本"""
    strat = STRATEGY_TEMPLATES.get(strategy_key, STRATEGY_TEMPLATES["panic_inflation"])

    raw_script = strat["script"].format(
        item_name=item_name,
        quote_price=quote_price,
        target_price=target_price
    )

    is_safe = inspect_brand_redline(raw_script)

    return {
        "item_name": item_name,
        "vendor_quote": quote_price,
        "target_price": target_price,
        "negotiation_gap": round(quote_price - target_price, 1),
        "strategy_name": strat["name"],
        "opponent_mindset_analysis": strat["opponent_mindset"],
        "negotiation_script": raw_script,
        "brand_redline_check": "PASS (自稱生活管家，零洩漏內部代號)" if is_safe else "FAIL"
    }

def main():
    parser = argparse.ArgumentParser(description="供應商商業心理戰預判與高情商議價話術引擎")
    parser.add_argument("--item", type=str, default="智利冷凍鮭魚 (整尾原箱)", help="商品名稱")
    parser.add_argument("--quote", type=float, default=450.0, help="廠商報價")
    parser.add_argument("--target", type=float, default=370.0, help="我方目標底價")
    parser.add_argument("--strategy", type=str, default="panic_inflation", choices=["panic_inflation", "turnover", "testing_high"], help="心理戰戰術模式")
    parser.add_argument("--dry-run", action="store_true", help="執行談判文本模擬")
    args = parser.parse_args()

    res = generate_tactical_negotiation(args.item, args.quote, args.target, args.strategy)

    if res["brand_redline_check"] != "PASS (自稱生活管家，零洩漏內部代號)":
        print("==================================================")
        print("🛑 戴明安燈拉繩！談判話術出現內部代號「極星」，出廠攔截！")
        print("==================================================")
        sys.exit(1)

    print("==================================================")
    print(f"🧠 商業心理戰與高情商談判方案完成 (Exit Code: 0) - {res['item_name']}")
    print(f"報價對比: 廠商開盤 NT$ {res['vendor_quote']} 元 ➔ 我方目標 NT$ {res['target_price']} 元 (爭取降幅: NT$ {res['negotiation_gap']} 元)")
    print(f"戰術策略: {res['strategy_name']}")
    print("--------------------------------------------------")
    print("🔍 對手商業心理戰剖析:")
    print(f"  {res['opponent_mindset_analysis']}")
    print("--------------------------------------------------")
    print("🤝 老闆專用四步閉環高情商談判文本:")
    print(res["negotiation_script"])
    print("--------------------------------------------------")
    print(f"🛡️ 品牌法定名稱防火牆: {res['brand_redline_check']}")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
