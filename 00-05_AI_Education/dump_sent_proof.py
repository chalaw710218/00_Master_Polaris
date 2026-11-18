import imaplib
import email
from email.header import decode_header
from pathlib import Path
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris")
with open(ROOT_DIR / ".secrets.env", "r", encoding="utf-8") as f:
    env = dict(line.strip().split("=", 1) for line in f if "=" in line and not line.strip().startswith("#"))

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(env["GMAIL_USER"], env["GMAIL_APP_PASSWORD"])
mail.select('"[Gmail]/&UWiQ6JD1TvY-"')

target_ids = ['206', '209', '210', '211', '212']

print("=== 官方伺服器全域信件物理憑證審計 ===")
for mid in target_ids:
    _, data = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (TO DATE SUBJECT MESSAGE-ID FROM)])')
    raw_header = data[0][1]
    msg = email.message_from_bytes(raw_header)
    
    sub_parts = decode_header(msg.get("Subject", ""))
    decoded_sub = ""
    for part, enc in sub_parts:
        if isinstance(part, bytes):
            decoded_sub += part.decode(enc or "utf-8", errors="ignore")
        else:
            decoded_sub += part
            
    to_parts = decode_header(msg.get("To", ""))
    decoded_to = ""
    for part, enc in to_parts:
        if isinstance(part, bytes):
            decoded_to += part.decode(enc or "utf-8", errors="ignore")
        else:
            decoded_to += part

    print(f"ID [{mid}]:")
    print(f"  • 收件人 (To): {decoded_to}")
    print(f"  • 發信人 (From): {msg.get('From')}")
    print(f"  • Google 伺服器時間戳 (Date): {msg.get('Date')}")
    print(f"  • 信件主旨 (Subject): {decoded_sub.strip()}")
    print(f"  • 國際標準郵件指紋 (Message-ID): {msg.get('Message-ID').strip()}")
    print("-" * 60)

mail.logout()
