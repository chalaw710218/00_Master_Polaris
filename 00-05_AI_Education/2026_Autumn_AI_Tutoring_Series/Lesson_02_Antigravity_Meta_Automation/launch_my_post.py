# -*- coding: utf-8 -*-
"""
🎓 生活管家 2026 秋季實戰家教班 · 第 2 講實戰發射台腳本
功能：自動讀取本機照片與文案，透過 Meta 官方 Graph API 發布至 FB 粉絲專頁，並自動留下第一則引流留言。
"""

import os
import sys
import time
import requests
from pathlib import Path

# 強制設定標準輸出編碼為 UTF-8，防止 Windows 終端機中文亂碼
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 1. 讀取密碼保險箱 (.secrets.env 或 .env)
def load_env(env_path):
    env = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

CURRENT_DIR = Path(__file__).resolve().parent
ENV_PATH = CURRENT_DIR / ".secrets.env"
if not ENV_PATH.exists():
    ENV_PATH = CURRENT_DIR / ".env"

config = load_env(ENV_PATH)
PAGE_ID = config.get("FB_PAGE_ID", "").strip()
ACCESS_TOKEN = config.get("FB_PAGE_ACCESS_TOKEN", "").strip()

print("=" * 60)
print("🚀 生活管家 · 社群全自動發射台啟動中...")
print("=" * 60)

# 2. 防呆檢查金鑰與檔案
if not PAGE_ID or not ACCESS_TOKEN or "你的" in PAGE_ID or "你的" in ACCESS_TOKEN:
    print("\n❌ 錯誤：請先在 .secrets.env 填入正確的 FB_PAGE_ID 與 FB_PAGE_ACCESS_TOKEN！")
    print("👉 請參考講義第 5 步，將取得的 60 天長效金鑰貼上存檔。\n")
    sys.exit(1)

# 檢查圖片
image_file = None
for candidate in ["photo.jpg", "photo.png", "image.jpg", "image.png", "海報.jpg", "海報.png"]:
    p = CURRENT_DIR / candidate
    if p.exists():
        image_file = p
        break

if not image_file:
    print("\n❌ 錯誤：找不到貼文圖片！")
    print("👉 請將一張照片或海報命名為 photo.jpg，放入本腳本相同的資料夾中。\n")
    sys.exit(1)

# 檢查文案
text_file = None
for candidate in ["draft.txt", "content.txt", "文案.txt"]:
    p = CURRENT_DIR / candidate
    if p.exists():
        text_file = p
        break

if not text_file:
    print("\n❌ 錯誤：找不到文案草稿！")
    print("👉 請將一段文案存為 draft.txt，放入本腳本相同的資料夾中。\n")
    sys.exit(1)

with open(text_file, "r", encoding="utf-8") as f:
    post_message = f.read().strip()

print(f"📦 偵測到發射素材：")
print(f"  • 照片檔案：{image_file.name}")
print(f"  • 文案字數：{len(post_message)} 字")
print(f"  • 目標粉專 ID：{PAGE_ID}")
print("-" * 60)

API_BASE = f"https://graph.facebook.com/v20.0/{PAGE_ID}"

try:
    # -------------------------------------------------------------
    # 步驟 1：上傳圖片取得行李吊牌 (Media ID)
    # -------------------------------------------------------------
    print("📡【步驟 1/3】正在上傳照片至 Meta 伺服器取得通行號碼牌 (Media ID)...")
    url_photo = f"{API_BASE}/photos"
    
    with open(image_file, "rb") as f:
        files = {"source": f}
        data = {
            "access_token": ACCESS_TOKEN,
            "published": "false"  # 關鍵：先不上傳公開，只取得 Media ID
        }
        res_photo = requests.post(url_photo, files=files, data=data, timeout=30)
    
    photo_json = res_photo.json()
    if "error" in photo_json:
        print(f"\n❌ 上傳照片失敗！Meta 回傳錯誤：")
        print(f"   代碼：{photo_json['error'].get('code')} - {photo_json['error'].get('message')}")
        if photo_json['error'].get('code') in [190, 102]:
            print("   👉 提示：您的 Token 可能已過期或複製不完整，請重新取得 60 天長效權杖！")
        elif photo_json['error'].get('code') == 200:
            print("   👉 提示：權限不足！請確認您拿的是『Page Token (粉專權杖)』，而不是個人 User Token！")
        sys.exit(1)
        
    media_id = photo_json.get("id")
    print(f"  ✅ 成功取得照片行李吊牌！Media ID: {media_id}")

    # -------------------------------------------------------------
    # 步驟 2：文案與號碼牌合體推播至時間軸 (Feed Publish)
    # -------------------------------------------------------------
    print("\n🚀【步驟 2/3】正在將文案與照片推播至 Facebook 粉絲專頁時間軸...")
    url_feed = f"{API_BASE}/feed"
    payload_feed = {
        "access_token": ACCESS_TOKEN,
        "message": post_message,
        "attached_media": f'[{{"media_fbid":"{media_id}"}}]'
    }
    
    res_feed = requests.post(url_feed, data=payload_feed, timeout=30)
    feed_json = res_feed.json()
    
    if "error" in feed_json:
        print(f"\n❌ 發布貼文失敗！Meta 回傳錯誤：")
        print(f"   代碼：{feed_json['error'].get('code')} - {feed_json['error'].get('message')}")
        sys.exit(1)
        
    post_id = feed_json.get("id")
    print(f"  ✅ 貼文秒級上線！專屬 Post ID: {post_id}")

    # -------------------------------------------------------------
    # 步驟 3：自動暗樁！第一則留言防降權引流
    # -------------------------------------------------------------
    print("\n💬【步驟 3/3】正在啟動自動暗樁，於貼文第一則留言附上引流連結...")
    time.sleep(1.5)  # 稍微緩衝 1.5 秒，確保貼文已被 Meta 索引
    
    url_comment = f"https://graph.facebook.com/v20.0/{post_id}/comments"
    comment_text = "💡【生活管家 貼心提醒】\n歡迎點擊下方官方 LINE 諮詢或了解更多詳情：\n👉 https://lin.ee/z83YSq6\n（私訊生活管家，為您安排專屬諮詢！）"
    
    payload_comment = {
        "access_token": ACCESS_TOKEN,
        "message": comment_text
    }
    
    res_comment = requests.post(url_comment, data=payload_comment, timeout=30)
    comment_json = res_comment.json()
    
    if "id" in comment_json:
        print(f"  ✅ 第一則留言自動掛載成功！Comment ID: {comment_json.get('id')}")
    else:
        print(f"  ⚠️ 留言掛載跳過或略過：{comment_json}")

    # -------------------------------------------------------------
    # 驗收完成
    # -------------------------------------------------------------
    print("\n" + "=" * 60)
    print("🎉 恭喜！全流程發射成功（Exit Code: 0）！")
    print("📱 請現在拿出您的手機，打開 Facebook 粉絲專頁查看最新貼文！")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ 執行過程發生未預期錯誤: {e}")
    sys.exit(1)
