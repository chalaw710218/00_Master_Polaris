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

# All Mail is "[Gmail]/所有郵件" -> &UWiQ6JD1TvY-
status, data = mail.select('"[Gmail]/&UWiQ6JD1TvY-"')
total = int(data[0])
print(f"All Mail Total: {total}")

for i in range(total, max(1, total - 12), -1):
    status, hdata = mail.fetch(str(i), '(BODY.PEEK[HEADER.FIELDS (TO DATE SUBJECT)])')
    if status == 'OK' and hdata and hdata[0]:
        raw_header = hdata[0][1]
        msg = email.message_from_bytes(raw_header)
        to_hdr = str(msg.get("To", ""))
        date_hdr = str(msg.get("Date", ""))
        subject_hdr = str(msg.get("Subject", ""))
        sub_parts = decode_header(subject_hdr)
        decoded_sub = ""
        for part, enc in sub_parts:
            if isinstance(part, bytes):
                decoded_sub += part.decode(enc or "utf-8", errors="ignore")
            else:
                decoded_sub += part
        print(f"[{i}] Date: {date_hdr} | To: {to_hdr} | Subject: {decoded_sub.strip()[:40]}")
