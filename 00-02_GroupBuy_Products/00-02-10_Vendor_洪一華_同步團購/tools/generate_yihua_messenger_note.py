# -*- coding: utf-8 -*-
"""
一華臉書私訊留貨便條生成器 (Yihua Messenger Note Generator)
功能：
1. 接收訂單品項與數量
2. 秒級組裝出符合臉書社團商家習慣的禮貌私訊文字
3. 輸出每週三 15:00~18:00 統一提貨付款備註
"""

import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def format_messenger_note(product_name: str, spec: str, quantity: int, customer_ref: str = "") -> str:
    note = f"""一華您好！就醬點客人下單：
📌【{product_name}】{spec} x {quantity} 包
麻煩先幫我留現場現貨庫存，我統一於「本週三下午 15:00～18:00」過去整批取貨結算，感謝您！"""
    return note

if __name__ == "__main__":
    # 範例測試
    p_name = "大成安心雞・土雞去皮清肉 500g"
    spec = "A.安心土雞"
    qty = 1
    if len(sys.argv) > 1:
        p_name = sys.argv[1]
    if len(sys.argv) > 2:
        spec = sys.argv[2]
    if len(sys.argv) > 3:
        qty = int(sys.argv[3])
        
    print("=" * 50)
    print("💬 【一華臉書私訊 (Messenger) 留貨便條】")
    print("=" * 50)
    print(format_messenger_note(p_name, spec, qty))
    print("=" * 50)
    print("👉 請直接複製上方訊息，私訊發送給洪一華即可！")
