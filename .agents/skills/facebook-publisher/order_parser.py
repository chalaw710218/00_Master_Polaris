import re
from datetime import datetime

# ==========================================
# 👑 【生活管家】+1 留言訂單智慧解析器
# 支援解析格式：
#  - "+1", "＋1", "+2"
#  - "原味+1, 辣味+2"
#  - "黑胡椒*2, 蒜味+1"
#  - "我要兩包原味，一包辣味"
# ==========================================

DEFAULT_SKU = "預設商品"

def parse_order_from_comment(comment_text, default_sku=DEFAULT_SKU):
    """
    解析顧客留言文字，回傳訂購品項與數量清單
    :return: list of dict, e.g. [{'sku': '原味', 'qty': 2}]
    """
    text = comment_text.strip()
    orders = []

    # 1. 統一全形字元為半形
    text = text.replace('＋', '+').replace('＊', '*').replace('，', ',').replace('、', ',')
    
    # 2. 常見模式一：明確帶有規格或品項的組合，例如 "原味+2, 辣味+1" 或 "黑胡椒+1"
    # 匹配模式：[文字/規格] + 符號(+/*) + [數字]
    pattern_spec = r'([^\d\+\*\,，\s]+)\s*[\+\*xX]\s*(\d+)'
    matches_spec = re.findall(pattern_spec, text)
    
    if matches_spec:
        for sku, qty in matches_spec:
            orders.append({
                'sku': sku.strip(),
                'qty': int(qty)
            })
        return orders

    # 3. 常見模式二：純喊數量，例如 "+1", "+2", "*3"
    pattern_pure_qty = r'[\+\*xX]\s*(\d+)'
    matches_pure = re.findall(pattern_pure_qty, text)
    if matches_pure:
        total_qty = sum(int(q) for q in matches_pure)
        orders.append({
            'sku': default_sku,
            'qty': total_qty
        })
        return orders

    # 4. 常見模式三：中文數字表述，例如 "原味兩包", "一包"
    cn_num_map = {'一': 1, '二': 2, '兩': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
    for cn_char, num_val in cn_num_map.items():
        if f"{cn_char}包" in text or f"{cn_char}份" in text:
            orders.append({
                'sku': default_sku,
                'qty': num_val
            })
            return orders

    # 無法自動辨識
    return []

def process_raw_comments(comments_data, default_sku="舒肥雞胸肉"):
    """
    處理一批留言資料，產出結構化訂單清單
    comments_data: list of dict [{'id': '...', 'from': {'name': '王小明', 'id': '...'}, 'message': '原味+2', 'created_time': '...'}]
    """
    parsed_results = []
    
    for item in comments_data:
        author = item.get('from', {}).get('name', '未知顧客')
        author_id = item.get('from', {}).get('id', '')
        message = item.get('message', '')
        time_str = item.get('created_time', datetime.now().isoformat())
        
        parsed_items = parse_order_from_comment(message, default_sku=default_sku)
        
        if parsed_items:
            for ord_item in parsed_items:
                parsed_results.append({
                    'customer_name': author,
                    'customer_id': author_id,
                    'raw_message': message,
                    'sku': ord_item['sku'],
                    'quantity': ord_item['qty'],
                    'timestamp': time_str,
                    'status': '✅ 辨識成功'
                })
        else:
            # 留存未辨識成功的留言供人工檢查（例如提問「請問什麼時候到貨？」）
            parsed_results.append({
                'customer_name': author,
                'customer_id': author_id,
                'raw_message': message,
                'sku': '無 (一般詢問/需人工核對)',
                'quantity': 0,
                'timestamp': time_str,
                'status': '⚠️ 需人工審查'
            })
            
    return parsed_results

if __name__ == '__main__':
    # 模擬測試
    test_cases = [
        {'from': {'name': '陳品碩'}, 'message': '+1', 'created_time': '2026-10-14 09:00'},
        {'from': {'name': '林小美'}, 'message': '原味+2, 蒜味+1', 'created_time': '2026-10-14 09:05'},
        {'from': {'name': '張阿姨'}, 'message': '我要兩包', 'created_time': '2026-10-14 09:12'},
        {'from': {'name': '李大同'}, 'message': '請問可以送到知本嗎？', 'created_time': '2026-10-14 09:20'},
    ]
    
    results = process_raw_comments(test_cases, default_sku="台東舒肥雞胸肉")
    print(f"📊 測試解析結果 (共 {len(results)} 筆記錄)：\n")
    for r in results:
        print(f"[{r['status']}] {r['customer_name']} | 留言: '{r['raw_message']}' -> 品項: {r['sku']}, 數量: {r['quantity']}")
