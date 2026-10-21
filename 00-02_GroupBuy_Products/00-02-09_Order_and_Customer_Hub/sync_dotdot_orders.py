import os
import sys
import re
import json
import html
import email
import urllib.request
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 加入 00-00 模組路徑以調用 email_manager
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
sys.path.append(str(REPO_ROOT / '00-00_Gamification_Engine'))

try:
    import email_manager
except ImportError:
    email_manager = None

HISTORY_FILE = SCRIPT_DIR / 'order_history.json'
GAS_ORDER_URL = os.environ.get('ORDER_SHEET_GAS_URL', '').strip()

def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def fetch_order_details_from_ddc_url(ddc_url):
    """輸入 ddc.ai 短網址，自動抓取並解析出完整訂單結構化 JSON"""
    req = urllib.request.Request(ddc_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req) as resp:
        page_html = resp.read().decode('utf-8', errors='replace')

    target_url = ddc_url
    m_url = re.search(r'window\.location\.href\s*=\s*[\"\']([^\"\']+)[\"\']', page_html)
    if not m_url:
        m_url = re.search(r'href=[\"\'](https://line\.quickclick\.cc/[^\"\']+)[\"\']', page_html)
    
    if m_url:
        target_url = m_url.group(1).replace('&amp;', '&')
        req2 = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req2) as resp2:
            page_html = resp2.read().decode('utf-8', errors='replace')

    m = re.search(r'id=[\"\']orderInfo[\"\'][^>]*value=[\"\'](.*?)[\"\']', page_html)
    if not m:
        m = re.search(r'value=[\"\'](.*?)[\"\'][^>]*id=[\"\']orderInfo[\"\']', page_html)

    if m:
        val = html.unescape(m.group(1))
        return json.loads(val)
    return None

def push_order_to_google_sheet(order_payload):
    """透過 Google Apps Script Webhook 寫入 Google Sheet"""
    gas_url = os.environ.get('ORDER_SHEET_GAS_URL', '').strip()
    if not gas_url:
        return False, "尚未設定 ORDER_SHEET_GAS_URL"

    data = json.dumps(order_payload).encode('utf-8')
    req = urllib.request.Request(gas_url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get('status') in ['success', 'exists']:
                return True, res_data.get('status')
            return False, res_data.get('message', '未知錯誤')
    except Exception as e:
        return False, str(e)

def sync_dotdot_orders_to_sheet(limit=10):
    """
    全自動閉環：掃描 Email ➜ 爬取 ddc.ai ➜ 寫入 Google Sheet ➜ 本地歸檔
    """
    if not email_manager:
        print("未找到 email_manager 模組。")
        return []

    mail = email_manager.connect_imap()
    mail.select('INBOX', readonly=True)

    status, response = mail.search(None, 'FROM', '"notify@dotdot.cc"')
    if status != 'OK' or not response[0]:
        mail.logout()
        return []

    email_ids = response[0].split()
    target_ids = email_ids[-limit:]
    target_ids.reverse()

    history = load_history()
    processed_orders = []

    for e_id in target_ids:
        res, data = mail.fetch(e_id, '(RFC822)')
        if res != 'OK':
            continue

        raw_msg = email.message_from_bytes(data[0][1])
        body = ""
        for part in raw_msg.walk():
            if part.get_content_type() in ['text/html', 'text/plain']:
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or 'utf-8'
                body = payload.decode(charset, errors='replace')
                break

        m_link = re.search(r'https://ddc\.ai/[a-zA-Z0-9]+', body)
        if not m_link:
            continue

        ddc_url = m_link.group(0)
        m_order_id = re.search(r'訂單編號[：:]\s*([0-9]+)', body)
        order_id = m_order_id.group(1) if m_order_id else ddc_url

        # 檢查是否已推送到 Google Sheet
        if order_id in history and history[order_id].get('pushed_to_sheet'):
            continue

        try:
            order_data = fetch_order_details_from_ddc_url(ddc_url)
            if order_data:
                record = {
                    'order_id': order_id,
                    'order_number': order_data.get('orderNumber'),
                    'user_name': order_data.get('userName'),
                    'user_phone': order_data.get('userPhone'),
                    'order_time': order_data.get('orderTime'),
                    'take_meal_time': order_data.get('takeMealTime'),
                    'meal_type': order_data.get('mealType', '自取'),
                    'amount': order_data.get('amount'),
                    'payment_type': order_data.get('paymentType'),
                    'products': order_data.get('products', []),
                    'comment': order_data.get('comment', '')
                }

                # 嘗試推送到 Google Sheet
                pushed, msg = push_order_to_google_sheet(record)
                record['processed_at'] = datetime.now().isoformat()
                record['pushed_to_sheet'] = pushed
                record['push_message'] = msg

                history[order_id] = record
                processed_orders.append(record)
                status_icon = "✅ 已同步 Sheet" if pushed else f"⚠️ 僅本地快取 ({msg})"
                print(f"[{status_icon}] 訂單 #{record['order_number']} | 客人: {record['user_name']} | 金額: ${record['amount']}")
        except Exception as ex:
            print(f"處理訂單 {order_id} 失敗: {ex}")

    save_history(history)
    mail.logout()
    return processed_orders

if __name__ == '__main__':
    print("=== 點點全球訂單自動化同步運行 ===")
    results = sync_dotdot_orders_to_sheet(limit=5)
    print(f"運行完成，本次處理/同步訂單數：{len(results)} 筆")
