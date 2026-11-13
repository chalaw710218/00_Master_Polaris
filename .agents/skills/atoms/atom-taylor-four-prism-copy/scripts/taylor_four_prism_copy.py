#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-taylor-four-prism-copy: 四面向高轉化行銷長文與文案矩陣原子腳本
專職負責行銷長泰勒絲 (Taylor) 貫徹四大面向折射鐵律（專業/歷程/三觀/選品）與禁語防呆。
"""

import sys
import os
import argparse
import json
import re

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 廉價叫賣促銷禁語庫 (一票否決)
BANNED_CHEAP_SALES_WORDS = [
    r"團購",
    r"便宜",
    r"划算",
    r"俗擱大碗",
    r"\+1",
    r"限時搶購",
    r"狂歡大促",
    r"買到賺到",
]

def check_banned_copy_words(text: str) -> list:
    """檢查是否含有廉價叫賣禁語"""
    violations = []
    for pattern in BANNED_CHEAP_SALES_WORDS:
        matches = re.findall(pattern, text)
        if matches:
            violations.append(pattern)
    return violations

def generate_four_prism_copy_matrix(product: str, terroir: str, price: str = None) -> dict:
    """生成四大面向高轉化行銷文案矩陣"""
    price_info = f"NT$ {price} 元" if price else "明碼標價，扣除跑腿費無隱形加成"

    # 1. 專業知識面
    copy_knowledge = (
        f"【熱力學與風土真值 · 為什麼我們死守 0.0% 包冰？】\n\n"
        f"很多人問我們，為什麼挑選【{product}】時，連 1% 的保護冰衣都不肯鍍？\n"
        f"因為在料理熱力學裡，自來水冰衣融化後的氯水會直接滲入魚肉肌理，破壞 Omega-3 脂肪酸鏈，"
        f"下鍋油煎時水氣炸開，魚皮梅納反應直接泡湯。\n"
        f"我們依循【{terroir}】，堅持深冷急速真空鎖鮮。實重就是淨重，手摸得著緊緻魚肉的彈性。\n"
        f"懂吃的掌廚人，鍋熱油熱魚擦乾，15 分鐘端出一盤酥脆金黃，這就是物理真值。"
    )

    # 2. 成長歷程面
    copy_journey = (
        f"【凌晨三點的港口海風，與我們踩過的那些坑】\n\n"
        f"為了把【{product}】帶上台東都會與西部家庭餐桌，我們在港口吹了三個月的冷風。\n"
        f"曾以為只要找大盤商最省事，直到親眼看見滿載退冰再急凍的混亂，我們決定回歸源頭，"
        f"跟著具名漁船的船長一箱一箱摸刺品檢。\n"
        f"手指逆紋摸過三次，挑掉最細微的暗刺。老討海人笑我們傻：『多做這些誰看得到？』\n"
        f"但看見媽媽放心夾給孩子吃的那一刻，我們知道，所有的泥土與寒風都值得了。"
    )

    # 3. 三觀哲學面
    copy_values = (
        f"【柴米油鹽不是苟且，是生活最體面的修行】\n\n"
        f"現代人太常被數字推著跑，連吃飯都變成熱量填充。\n"
        f"生活管家始終相信：一口真正乾淨的原形美味，是抵禦大都市疲憊最強的神經避風港。\n"
        f"我們不炒作短命爆款，老老實實做好【{product}】的物理履約，守護一份土地真實的尊嚴。\n"
        f"生活的一部分，就醬點！在細水長流的日常裡，陪你把每一頓飯吃得從容體面。"
    )

    # 4. 選品宣告面
    copy_announcement = (
        f"【生活管家選品宣告 · {product}】\n\n"
        f"本批【{product}】現流抵港完成品檢：\n"
        f"  * 產地工法：{terroir}\n"
        f"  * 物理承諾：包冰率 0.0%，實重淨重核驗\n"
        f"  * 價值定價：{price_info}\n"
        f"  * 自提服務：海特咖啡等友店星系 -18°C 智能自提，零失溫零等待。\n"
        f"本批配額售完即止，認領請洽生活管家私域客廳。"
    )

    matrix = {
        "knowledge_prism": copy_knowledge,
        "journey_prism": copy_journey,
        "values_prism": copy_values,
        "announcement_prism": copy_announcement
    }

    # 執行禁語審查
    all_text = " ".join(matrix.values())
    violations = check_banned_copy_words(all_text)

    return {
        "product": product,
        "terroir": terroir,
        "price": price_info,
        "copy_matrix": matrix,
        "violations": violations,
        "passed": len(violations) == 0
    }

def main():
    parser = argparse.ArgumentParser(description="四面向高轉化行銷長文與文案矩陣原子")
    parser.add_argument("--product", type=str, default="成功港急凍午仔魚", help="推廣商品或服務")
    parser.add_argument("--terroir", type=str, default="東台灣黑潮低溫熟成", help="產地風土工法")
    parser.add_argument("--price", type=str, default="450", help="商品價格")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")

    args = parser.parse_args()

    print("=== [atom-taylor-four-prism-copy] 泰勒絲四面向行銷文案矩陣折射 ===")
    res = generate_four_prism_copy_matrix(args.product, args.terroir, args.price)

    print(f"\n商品名稱: 『{res['product']}』 | 核心工法: {res['terroir']} | 價格: {res['price']}")
    print(f"廉價促銷禁語審查: {'[100% 通過]' if res['passed'] else f'[攔截違規: {res['violations']}]'}")

    if not res["passed"]:
        print("[-] 違反四大面向高階行銷準則，一票否決！")
        sys.exit(1)

    print("\n📚 **【四大面向文案矩陣預覽】**")
    print(f"\n1. 🔬 【專業知識面】\n{res['copy_matrix']['knowledge_prism']}")
    print(f"\n2. 👣 【成長歷程面】\n{res['copy_matrix']['journey_prism']}")
    print(f"\n3. 🍵 【三觀哲學面】\n{res['copy_matrix']['values_prism']}")
    print(f"\n4. 🛒 【選品宣告面】\n{res['copy_matrix']['announcement_prism']}")

    print("\n[+] 四面向高轉化行銷長文折射完畢 (Exit Code: 0)！")
    sys.exit(0)

if __name__ == "__main__":
    main()
