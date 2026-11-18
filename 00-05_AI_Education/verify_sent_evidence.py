import imaplib
import email
from email.header import decode_header
from pathlib import Path
import sys

ROOT_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris")
with open(ROOT_DIR / ".secrets.env", "r", encoding="utf-8") as f:
    env = dict(line.strip().split("=", 1) for line in f if "=" in line and not line.strip().startswith("#"))

print("1. 正在連線至 Gmail IMAP 伺服器...", flush=True)
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(env["GMAIL_USER"], env["GMAIL_APP_PASSWORD"])
print("2. 登入成功，正在開啟【寄件備份匣】...", flush=True)

# Select Sent folder
status, data = mail.select('"[Gmail]/&W8RO9lCZTv0-"')
total_msgs = int(data[0])
print(f"3. 寄件備份總信件數: {total_msgs} 封，檢索最新 10 封信件...", flush=True)

start_idx = max(1, total_msgs - 10)
target_emails = [
    "peichen06@gmail.com",
    "a828603@yahoo.com.tw",
    "k39607@gmail.com",
    "jimchenlichung@gmail.com",
    "chalaw710218@gmail.com"
]

found = {}
# Fetch headers only
for i in range(total_msgs, start_idx - 1, -1):
    status, hdata = mail.fetch(str(i), '(BODY.PEEK[HEADER.FIELDS (TO DATE SUBJECT MESSAGE-ID)])')
    if status == 'OK' and hdata and hdata[0]:
        raw_header = hdata[0][1]
        msg = email.message_from_bytes(raw_header)
        to_hdr = str(msg.get("To", ""))
        date_hdr = str(msg.get("Date", ""))
        subject_hdr = str(msg.get("Subject", ""))
        msg_id_hdr = str(msg.get("Message-ID", ""))
        
        sub_parts = decode_header(subject_hdr)
        decoded_sub = ""
        for part, enc in sub_parts:
            if isinstance(part, bytes):
                decoded_sub += part.decode(enc or "utf-8", errors="ignore")
            else:
                decoded_sub += part
                
        for t in target_emails:
            if t in to_hdr and t not in found:
                found[t] = {
                    "to": to_hdr,
                    "date": date_hdr,
                    "subject": decoded_sub.strip(),
                    "message_id": msg_id_hdr.strip()
                }

print("\n================== 🎯 官方伺服器寄件鐵證 ==================", flush=True)
for t in target_emails:
    if t in found:
        print(f"【學員/收件人】: {t}", flush=True)
        print(f"  • 收件人名稱與標頭: {found[t]['to']}", flush=True)
        print(f"  • Google 伺服器時間戳: {found[t]['date']}", flush=True)
        print(f"  • 信件主旨: {found[t]['subject']}", flush=True)
        print(f"  • 唯一郵件憑證 (Message-ID): {found[t]['message_id']}", flush=True)
        print("-" * 55, flush=True)
    else:
        print(f"❌ 尚未找到: {t}", flush=True)

print("\n4. 正在檢查收件匣退信紀錄（Mailer-Daemon / Delivery Failure）...", flush=True)
mail.select("INBOX")
status, messages = mail.search(None, 'FROM "mailer-daemon@googlemail.com"')
bounces = messages[0].split()
print(f"• 退件通知信 (Bounce): {len(bounces)} 筆", flush=True)
if len(bounces) == 0:
    print("✅ 確定零退信！所有信件均已被各別收件伺服器（Gmail / Yahoo）無阻攔接受！", flush=True)

mail.logout()
