import imaplib
import email
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
_, data = mail.fetch('208', '(RFC822)')
raw_email = data[0][1]
msg = email.message_from_bytes(raw_email)

print("=== 檢驗 208 退信詳情 ===")
print("From:", msg.get("From"))
print("To:", msg.get("To"))
print("Date:", msg.get("Date"))
print("Subject:", msg.get("Subject"))

for part in msg.walk():
    if part.get_content_type() == 'text/plain':
        print("--- Body ---")
        print(part.get_payload(decode=True).decode('utf-8', errors='ignore'))
        break

mail.logout()
