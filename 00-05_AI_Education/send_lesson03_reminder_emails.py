# -*- coding: utf-8 -*-
"""
生活管家 · 2026 秋季實戰家教班 · 第 3 講 學員上課提醒信發送腳本
上課時間：2026-11-25 (週三) 下午 14:00 - 16:00
地點：生活管家總部（台東市正氣北路166巷90號）
重點：必須攜帶筆記型電腦與充電線！
"""

import os
import sys
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from pathlib import Path

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

STUDENTS = [
    {"name": "蔡佩真", "email": "peichen06@gmail.com", "role": "晨間早點闆娘"},
    {"name": "李淑芬", "email": "a828603@yahoo.com.tw", "role": "生活夥伴"},
    {"name": "鍾秀美", "email": "k39607@gmail.com", "role": "在地頭家"},
    {"name": "陳豊鍾", "email": "jimchenlichung@gmail.com", "role": "在地頭家"},
    {"name": "陳品碩 (創辦人存證備查)", "email": "chalaw710218@gmail.com", "role": "主講導師"}
]

def build_reminder_email(recipient_name):
    subject = "【重要上課提醒】明天下午 14:00-16:00 正氣北路家宅總部開練！請務必攜帶「筆記型電腦與充電線」🎓"
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; color: #333333; background-color: #f7f9fa; margin: 0; padding: 20px; }}
  .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #e1e8ed; overflow: hidden; }}
  .header {{ background: #0d1117; color: #ffffff; padding: 24px; text-align: center; border-bottom: 3px solid #f59e0b; }}
  .header h1 {{ margin: 0; font-size: 20px; letter-spacing: 0.5px; color: #fbbf24; }}
  .header p {{ margin: 6px 0 0; font-size: 14px; color: #cbd5e1; }}
  .content {{ padding: 28px 24px; }}
  .highlight-box {{ background: #fff8e6; border-left: 4px solid #f59e0b; padding: 16px; margin: 20px 0; border-radius: 0 4px 4px 0; }}
  .highlight-box h3 {{ margin: 0 0 8px; color: #b45309; font-size: 16px; }}
  .item-list {{ margin: 12px 0; padding-left: 20px; }}
  .item-list li {{ margin-bottom: 8px; }}
  .footer {{ background: #f1f5f9; padding: 18px 24px; font-size: 13px; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; }}
  .badge {{ display: inline-block; background: #f59e0b; color: #000000; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-bottom: 12px; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="badge">生活管家 ｜ 2026 秋季實戰家教班</div>
    <h1>明天下午 14:00-16:00 家宅開練！</h1>
    <p>第 3 講大壓軸：《商業資料與價格架構 ✕ AI 擬人化工程：打造專屬 AI 數位店長》</p>
  </div>
  <div class="content">
    <p>親愛的 <strong>{recipient_name}</strong> 您好：</p>
    <p>期待明天下午與您見面！明天（11/25 週三）即將迎來秋季系列班的<strong>【第 3 講 · 終極壓軸】</strong>。過去兩週我們完成了 AI 的「大腦」與「手腳 API 自動化」，明天我們將親手為它<strong>「注入靈魂」</strong>，捏出一尊開口就像您親自顧店的專屬 AI 數位分身！</p>
    
    <div class="highlight-box">
      <h3>⚠️【明晚上課最重要叮嚀：請務必自備筆電！】</h3>
      <p style="margin: 0; font-weight: bold; color: #b45309;">我們堅持 100% 純實體現場逐桌手把手個別調教，現場沒有公用電腦，請務必攜帶：</p>
      <ul class="item-list" style="margin-top: 8px;">
        <li>💻 <strong>筆記型電腦（Windows 或 Mac 筆電皆可）</strong>：現場我們將坐在您身邊，親手帶您在電腦上建好商業資料庫與人設！</li>
        <li>🔌 <strong>原廠充電器 / 電源線</strong>：連續實機操作兩小時，耗電量大，務必帶線。</li>
        <li>📝 <strong>想好店裡 1~3 樣主力商品與價格</strong>：現場直接建立真實價格表，實測對話合格才准下課！</li>
      </ul>
    </div>

    <h3 style="color: #0f172a; margin-top: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;">📍 課程詳細資訊</h3>
    <ul class="item-list">
      <li><strong>⏰ 上課時間</strong>：2026-11-25 (週三) 下午 14:00 - 16:00（<strong>13:50 開放入席報到</strong>）</li>
      <li><strong>📍 上課地點</strong>：生活管家·家宅總部（<strong>台東市正氣北路166巷90號</strong>）</li>
      <li><strong>🎯 現場紀律</strong>：全場深度調教，現場沒捏出合格的專屬數位店長不准走！</li>
      <li><strong>💰 學費政策</strong>：老學員 0 元免單回娘家！</li>
    </ul>

    <p style="margin-top: 24px;">正氣北路家宅總部的熱茶已經泡好，黑板與投影幕已準備就緒。<br>明天下午，我們一起把有溫度的數位店長捏出來帶回家！</p>
    
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

def send_all():
    if not GMAIL_USER or not GMAIL_PWD:
        print("❌ 未設定 GMAIL_USER 或 GMAIL_APP_PASSWORD！")
        return False
        
    print(f"🚀 開始發送第 3 講攜帶筆電提醒信（發件人: {GMAIL_USER}）...\n")
    
    success_count = 0
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PWD)
        for s in STUDENTS:
            name = s["name"]
            email = s["email"]
            subject, html_body = build_reminder_email(name)
            
            msg = MIMEMultipart("alternative")
            msg["Subject"] = Header(subject, "utf-8")
            msg["From"] = f"生活管家 闆仔 <{GMAIL_USER}>"
            msg["To"] = f"{name} <{email}>"
            
            part_html = MIMEText(html_body, "html", "utf-8")
            msg.attach(part_html)
            
            try:
                server.sendmail(GMAIL_USER, email, msg.as_string())
                print(f"✅ 成功發送提醒信至: {name} ({email})")
                success_count += 1
            except Exception as e:
                print(f"❌ 發送失敗 {name} ({email}): {e}")
                
    print(f"\n==========================================")
    print(f"🎉 全部寄發完成！成功 {success_count} / {len(STUDENTS)} 封！")
    print(f"==========================================")
    return True

if __name__ == "__main__":
    send_all()
