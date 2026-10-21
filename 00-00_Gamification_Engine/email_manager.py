import os
import sys
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from pathlib import Path
import re

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

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

GMAIL_USER = os.environ.get('GMAIL_USER', '').strip()
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', '').replace(' ', '').strip()
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

def _decode_mime_header(header_text):
    """安全解碼 MIME 標題文字"""
    if not header_text:
        return ""
    decoded_fragments = decode_header(header_text)
    header_str = ""
    for fragment, charset in decoded_fragments:
        if isinstance(fragment, bytes):
            charset = charset or 'utf-8'
            try:
                header_str += fragment.decode(charset, errors='replace')
            except Exception:
                header_str += fragment.decode('utf-8', errors='replace')
        else:
            header_str += str(fragment)
    return header_str

def _clean_body_text(text):
    """清理 HTML 標籤與多餘空行，還原乾淨純文字"""
    if not text:
        return ""
    # 移除 CSS 與 JS
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # 移除 HTML 標籤
    text = re.sub(r'<[^>]+>', ' ', text)
    # 還原常見實體符號
    text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '"')
    # 壓縮多餘空白
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def connect_imap():
    """建立安全的 IMAP SSL 連線"""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        raise ValueError("尚未配置 GMAIL_USER 或 GMAIL_APP_PASSWORD。請在 .secrets.env 中填入您的 Gmail 與 16 位應用程式密碼。")
    
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    return mail

def get_recent_emails(days=3, limit=15, unread_only=False):
    """
    抓取近期郵件
    :param days: 抓取過去幾天內的郵件（預設 3 天）
    :param limit: 最多抓取幾封（預設 15 封）
    :param unread_only: 是否只抓取未讀郵件
    """
    mail = connect_imap()
    mail.select('INBOX', readonly=True)

    since_date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
    if unread_only:
        search_criteria = f'(UNSEEN SINCE {since_date})'
    else:
        search_criteria = f'(SINCE {since_date})'

    status, response = mail.search(None, search_criteria)
    if status != 'OK':
        mail.logout()
        return []

    email_ids = response[0].split()
    if not email_ids:
        mail.logout()
        return []

    # 取最新的 N 封
    latest_ids = email_ids[-limit:]
    latest_ids.reverse()

    results = []
    for e_id in latest_ids:
        res_status, msg_data = mail.fetch(e_id, '(RFC822)')
        if res_status != 'OK':
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = _decode_mime_header(msg.get('Subject', '無主旨'))
                sender = _decode_mime_header(msg.get('From', '未知寄件者'))
                date_str = msg.get('Date', '')

                body = ""
                attachments = []

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if "attachment" in content_disposition:
                            filename = _decode_mime_header(part.get_filename() or "")
                            if filename:
                                attachments.append(filename)
                        elif content_type == "text/plain" and not body:
                            payload = part.get_payload(decode=True)
                            charset = part.get_content_charset() or 'utf-8'
                            body = payload.decode(charset, errors='replace')
                        elif content_type == "text/html" and not body:
                            payload = part.get_payload(decode=True)
                            charset = part.get_content_charset() or 'utf-8'
                            body = _clean_body_text(payload.decode(charset, errors='replace'))
                else:
                    payload = msg.get_payload(decode=True)
                    charset = msg.get_content_charset() or 'utf-8'
                    body = payload.decode(charset, errors='replace')
                    if msg.get_content_type() == "text/html":
                        body = _clean_body_text(body)

                # 分類識別
                category = "一般日常"
                body_lower = (subject + " " + body[:500]).lower()
                if any(k in body_lower for k in ['報價', '出貨', '對帳', '發票', '匯款', '金額', 'price', 'invoice', 'quote']):
                    category = "🧮 算盤財務審計"
                elif any(k in body_lower for k in ['公文', '法規', '政府', '勞動', '稅捐', '契約', '合約', '外送專法', '平台政策']):
                    category = "🦅 獵鷹政策合規"
                elif any(k in body_lower for k in ['合作', '活動', '展覽', '行銷', '社群', '推廣', '媒體']):
                    category = "🎤 泰勒絲品牌行銷"

                results.append({
                    'id': e_id.decode('utf-8', errors='ignore'),
                    'subject': subject,
                    'from': sender,
                    'date': date_str,
                    'category': category,
                    'attachments': attachments,
                    'snippet': body.strip()[:300] + ('...' if len(body.strip()) > 300 else '')
                })

    mail.logout()
    return results

def generate_executive_briefing(days=1, limit=10):
    """為創辦人生成高層郵件日報"""
    emails = get_recent_emails(days=days, limit=limit)
    if not emails:
        return "📭 近期收件匣內無新郵件。"

    report = [f"# 📬 品碩專屬 · 郵件情資日報 ({datetime.now().strftime('%Y-%m-%d %H:%M')})", ""]
    for idx, m in enumerate(emails, 1):
        report.append(f"### {idx}. [{m['category']}] {m['subject']}")
        report.append(f"* **寄件者**：`{m['from']}`")
        report.append(f"* **時間**：{m['date']}")
        if m['attachments']:
            report.append(f"* **附件**：📎 `{', '.join(m['attachments'])}`")
        report.append(f"* **內文摘要**：")
        report.append(f"> {m['snippet']}")
        report.append("")
    return "\n".join(report)

if __name__ == '__main__':
    try:
        print("連線測試中...")
        emails = get_recent_emails(days=2, limit=5)
        print(f"成功取得 {len(emails)} 封郵件！")
        for e in emails:
            print(f"- [{e['category']}] {e['subject']} (來自: {e['from']})")
    except Exception as ex:
        print(f"測試狀態: {ex}")
