import requests
import json
import csv
import os
import sys
from pathlib import Path
from datetime import datetime

# 確保同目錄模組 order_parser 可被正確匯入 (無論自何處調用)
_CUR_DIR = Path(__file__).resolve().parent
if str(_CUR_DIR) not in sys.path:
    sys.path.insert(0, str(_CUR_DIR))

try:
    from order_parser import process_raw_comments
except ImportError:
    from .order_parser import process_raw_comments

# ==========================================
# 👑 【生活管家】+1 留言訂單收割機 (Order Harvester)
# 功能：從粉專抓取貼文留言 -> 自動解析訂單 -> 匯出 CSV 訂單總表
# ==========================================

# 自動載入 .secrets.env
def _load_env():
    p = Path(__file__).resolve()
    for parent in [p] + list(p.parents):
        env_file = parent / '.secrets.env'
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        os.environ.setdefault(k.strip(), v.strip())
            break
_load_env()

PAGE_ID = os.environ.get('FB_PAGE_ID', '110505444816362')
TOKEN = os.environ.get('FB_PAGE_ACCESS_TOKEN', '')

def fetch_post_comments(post_id):
    """從 Facebook API 抓取指定貼文的所有留言"""
    url = f'https://graph.facebook.com/v20.0/{post_id}/comments?fields=id,from,message,created_time&limit=100&access_token={TOKEN}'
    try:
        r = requests.get(url)
        data = r.json()
        if 'data' in data:
            return True, data['data']
        else:
            return False, data
    except Exception as e:
        return False, str(e)

def harvest_orders(post_id, product_name="台東舒肥雞胸肉", output_dir=None):
    """
    執行訂單收割流程
    :param post_id: Facebook 貼文 ID
    :param product_name: 該貼文的主打商品名稱
    :param output_dir: 匯出 CSV 的目錄
    """
    print(f"📡 正在連線 Facebook 抓取貼文 [{post_id}] 的留言...")
    success, result = fetch_post_comments(post_id)
    
    if not success:
        print(f"⚠️ API 讀取留言未成功: {result}")
        print("💡 提示：若出現權限錯誤 (#10)，代表目前 Token 缺少 'pages_read_user_content' 權限。")
        return []

    raw_comments = result
    print(f"📥 成功抓取到 {len(raw_comments)} 則留言！正在啟動智慧訂單解析...")
    
    parsed_orders = process_raw_comments(raw_comments, default_sku=product_name)
    
    # 匯出 CSV 報表
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = os.path.join(output_dir, f"訂單總表_{post_id}_{timestamp}.csv")
    
    with open(csv_filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['status', 'customer_name', 'sku', 'quantity', 'raw_message', 'timestamp', 'customer_id'])
        writer.writeheader()
        for row in parsed_orders:
            writer.writerow(row)
            
    print(f"✅ 訂單統計完成！已匯出至：{csv_filename}")
    return parsed_orders

if __name__ == '__main__':
    print("【生活管家】+1 留言訂單收割機模組載入完成。")
