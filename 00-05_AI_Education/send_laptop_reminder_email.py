import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris")
ENV_PATH = ROOT_DIR / ".secrets.env"

def load_env(path):
    env = {}
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

ENV = load_env(ENV_PATH)
GMAIL_USER = ENV.get("GMAIL_USER")
GMAIL_PWD = ENV.get("GMAIL_APP_PASSWORD")
FOUNDER_EMAIL = ENV.get("FOUNDER_EMAIL", "chalaw710218@gmail.com")

def build_reminder_email(recipient_name, recipient_email):
    subject = "【重要上課提醒】明天下午 14:00 家宅開練！請務必攜帶「筆記型電腦與原廠充電線」🎓"
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; color: #333333; background-color: #f7f9fa; margin: 0; padding: 20px; }}
  .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #e1e8ed; overflow: hidden; }}
  .header {{ background: #0a0f1d; color: #ffffff; padding: 24px; text-align: center; border-bottom: 3px solid #f5b738; }}
  .header h1 {{ margin: 0; font-size: 20px; letter-spacing: 1px; color: #e1eeff; }}
  .header p {{ margin: 6px 0 0; font-size: 14px; color: #8cb9eb; }}
  .content {{ padding: 28px 24px; }}
  .highlight-box {{ background: #fff8e6; border-left: 4px solid #f5b738; padding: 16px; margin: 20px 0; border-radius: 0 4px 4px 0; }}
  .highlight-box h3 {{ margin: 0 0 8px; color: #b7791f; font-size: 16px; }}
  .item-list {{ margin: 12px 0; padding-left: 20px; }}
  .item-list li {{ margin-bottom: 8px; }}
  .footer {{ background: #f1f5f9; padding: 18px 24px; font-size: 13px; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; }}
  .badge {{ display: inline-block; background: #2563eb; color: #ffffff; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-bottom: 12px; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="badge">生活管家 ｜ 2026 秋季實體家教系列班</div>
    <h1>明天下午 14:00 正氣北路家宅開練！</h1>
    <p>第 2 講：Antigravity 操作 ✕ Meta 官方自動發文串接 (FB / Threads API)</p>
  </div>
  <div class="content">
    <p>親愛的 <strong>{recipient_name}</strong> 您好：</p>
    <p>期待明天下午與您見面！明天（11/18 週三）即將迎來技術含金量最高、也是徹底消滅每天手動發文折磨的關鍵實戰：<strong>【第 2 講：把社群發射台交給 AI ✕ Meta 官方自動化串接】</strong>。</p>
    
    <div class="highlight-box">
      <h3>⚠️【明晚上課最關鍵準備：請務必自備筆電！】</h3>
      <p style="margin: 0; font-weight: bold; color: #b7791f;">堅持 100% 純實體現場個別巡桌指導，現場沒備公用電腦，請務必攜帶：</p>
      <ul class="item-list" style="margin-top: 8px;">
        <li>💻 <strong>筆記型電腦（Windows 或 Mac 筆電皆可）</strong>：現場我們將坐在您身邊，親手幫您在自己的電腦跑通自動發射台！</li>
        <li>🔌 <strong>原廠充電器 / 電源線</strong>：連續實作兩小時，耗電量極高，務必攜帶電源線。</li>
        <li>🌐 <strong>Google 帳號 ＆ Facebook / Threads 帳密確認</strong>：確保記得帳密，現場串接官方合法 API。</li>
      </ul>
    </div>

    <h3 style="color: #0f172a; margin-top: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;">📍 課程詳細資訊</h3>
    <ul class="item-list">
      <li><strong>⏰ 上課時間</strong>：2026-11-18 (週三) 下午 14:00 - 16:00（<strong>13:50 開放入席報到</strong>）</li>
      <li><strong>📍 上課地點</strong>：生活管家·家宅總部（<strong>台東市正氣北路166巷90號</strong>）</li>
      <li><strong>🎯 現場紀律</strong>：全場嚴格限額 6 席深度陪伴，API 沒跑通、沒發出專屬第一篇不准走！</li>
      <li><strong>💰 學費政策</strong>：老學員（含第 1 講夥伴）0 元免單回娘家！</li>
    </ul>

    <p style="margin-top: 24px;">若您明天下車或找路需要指引，請隨時私訊我們的官方 LINE 或撥打電話聯繫管家團隊。<br>明天下午，我們一起把時間買回來！</p>
    
    <p style="margin-top: 20px; font-weight: bold;">生活管家 創辦人 陳品碩（闆仔）＆ 教學團隊 敬上</p>
  </div>
  <div class="footer">
    📍 生活管家·家宅總部 ｜ 台東市正氣北路166巷90號<br>
    💬 官方 LINE 諮詢：<a href="https://lin.ee/z83YSq6" style="color: #2563eb; text-decoration: none;">https://lin.ee/z83YSq6</a>
  </div>
</div>
</body>
</html>
"""
    return subject, html_content

def send_email(recipient_name, recipient_email):
    if not GMAIL_USER or not GMAIL_PWD:
        print("❌ 未設定 GMAIL_USER 或 GMAIL_APP_PASSWORD！")
        return False
        
    subject, html_body = build_reminder_email(recipient_name, recipient_email)
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = f"生活管家 闆仔 <{GMAIL_USER}>"
    msg["To"] = f"{recipient_name} <{recipient_email}>"
    
    part_html = MIMEText(html_body, "html", "utf-8")
    msg.attach(part_html)
    
    try:
        print(f"📧 正在發送攜帶筆電提醒信至: {recipient_name} ({recipient_email})...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PWD)
            server.sendmail(GMAIL_USER, recipient_email, msg.as_string())
        print(f"✅ 成功發送提醒信至: {recipient_email}！")
        return True
    except Exception as e:
        print(f"❌ 發送郵件失敗: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 2:
        name = sys.argv[1]
        email = sys.argv[2]
        send_email(name, email)
    else:
        print("Usage: python send_laptop_reminder_email.py <name> <email>")
