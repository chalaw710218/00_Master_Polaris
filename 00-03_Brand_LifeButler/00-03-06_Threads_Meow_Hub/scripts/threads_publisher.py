import os
import sys
import time
import requests
from pathlib import Path

# 確保 Windows 終端機支援 Emoji 輸出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 定位極星根目錄下的 .secrets.env
ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = ROOT_DIR / ".secrets.env"

def load_env(env_path):
    """簡易讀取 .env 檔案並載入環境變數"""
    if not env_path.exists():
        print(f"⚠️ 找不到金鑰設定檔: {env_path}")
        return {}
    env_vars = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                env_vars[key.strip()] = val.strip()
    return env_vars

ENV = load_env(ENV_PATH)
THREADS_USER_ID = ENV.get("THREADS_USER_ID")
THREADS_ACCESS_TOKEN = ENV.get("THREADS_ACCESS_TOKEN")
FB_PAGE_ACCESS_TOKEN = ENV.get("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = "110505444816362"

API_BASE = "https://graph.threads.net/v1.0"

def upload_local_image_to_meta_cdn(image_path):
    """
    Meta Threads API 嚴格規定 image_url 必須為公開 HTTP/HTTPS 網址，無法直接傳送本地檔案 bytes。
    【極星黑科技】：若為本地檔案路徑，自動利用既有粉專 Token 上傳為未發布相片，
    藉此取得 Meta 官方的高速 scontent CDN 永久公開連結，無縫供給 Threads 下載！
    """
    if not image_path:
        return None

    if str(image_path).startswith("http://") or str(image_path).startswith("https://"):
        return str(image_path)

    path = Path(image_path)
    if not path.exists():
        print(f"⚠️ 找不到本地圖片檔案: {path}")
        return None

    if not FB_PAGE_ACCESS_TOKEN:
        print("⚠️ 未設定 FB_PAGE_ACCESS_TOKEN，無法自動上傳至 Meta CDN！")
        return None

    print(f"📤 正在將本地圖片託管至 Meta 官方 CDN: {path.name}...")
    try:
        url_upload = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/photos"
        with open(path, "rb") as f:
            r = requests.post(url_upload, files={"source": f}, data={
                "access_token": FB_PAGE_ACCESS_TOKEN,
                "published": "false"
            })
        res = r.json()
        photo_id = res.get("id")
        if not photo_id:
            print(f"❌ 上傳 Meta CDN 失敗: {res}")
            return None

        # 抓取最高畫質的 CDN 網址
        url_query = f"https://graph.facebook.com/v20.0/{photo_id}?fields=images&access_token={FB_PAGE_ACCESS_TOKEN}"
        r2 = requests.get(url_query).json()
        images = r2.get("images", [])
        if images:
            cdn_url = images[0].get("source")
            print("✅ 本地圖片已成功託管至 Meta CDN！")
            return cdn_url
    except Exception as e:
        print(f"❌ 上傳 CDN 過程發生異常: {e}")
        return None

    return None

def create_media_container(text, image_url=None, reply_to_id=None):
    """
    第一階段：建立 Threads 媒體容器
    :param text: 發文文字內容 (最多 500 字)
    :param image_url: 圖片公開 URL (若有圖片，必須為可公開存取的網址)
    :param reply_to_id: 若是回覆某則串文或留言，填入該 post/comment ID
    """
    if not THREADS_USER_ID or not THREADS_ACCESS_TOKEN:
        print("❌ 錯誤：尚未在 .secrets.env 中設定 THREADS_USER_ID 或 THREADS_ACCESS_TOKEN！")
        return None

    url = f"{API_BASE}/{THREADS_USER_ID}/threads"
    payload = {
        "access_token": THREADS_ACCESS_TOKEN,
        "text": text
    }

    if image_url:
        payload["media_type"] = "IMAGE"
        payload["image_url"] = image_url
    else:
        payload["media_type"] = "TEXT"

    if reply_to_id:
        payload["reply_to_id"] = reply_to_id

    response = requests.post(url, data=payload)
    res_data = response.json()

    if "id" in res_data:
        creation_id = res_data["id"]
        print(f"✅ 媒體容器建立成功！Creation ID: {creation_id}")
        return creation_id
    else:
        print(f"❌ 建立容器失敗: {res_data}")
        return None

def publish_container(creation_id):
    """
    第二階段：正式發布容器至 Threads
    """
    url = f"{API_BASE}/{THREADS_USER_ID}/threads_publish"
    payload = {
        "access_token": THREADS_ACCESS_TOKEN,
        "creation_id": creation_id
    }

    response = requests.post(url, data=payload)
    res_data = response.json()

    if "id" in res_data:
        post_id = res_data["id"]
        print(f"🎉 脆文發布成功！Threads Post ID: {post_id}")
        print(f"🔗 前台連結: https://www.threads.net/@hellotaitung/post/{post_id}")
        return post_id
    else:
        print(f"❌ 發布失敗: {res_data}")
        return None

def publish_thread(text, image=None, reply_to_id=None):
    """
    完整發文流程封裝
    :param text: 貼文內容
    :param image: 可以是公開 HTTP 網址，也可以是電腦本機的圖片路徑 (如 C:/photo.jpg)
    :param reply_to_id: 可選，若為回覆特定串文填入 ID
    """
    print("🚀 [喵編發射台] 準備推送貼文至 Threads...")
    
    image_url = None
    if image:
        image_url = upload_local_image_to_meta_cdn(image)
        if not image_url:
            print("⚠️ 圖片轉載失敗，將改為純文字發布！")

    creation_id = create_media_container(text=text, image_url=image_url, reply_to_id=reply_to_id)
    if not creation_id:
        return None

    # Meta 建議在建立容器後稍微等待 2~4 秒確保容器就緒
    time.sleep(3)
    return publish_container(creation_id)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        content = " ".join(sys.argv[1:])
        publish_thread(text=content)
    else:
        test_text = "好，我宣佈這家店被一隻貓接管了喵！🐱（這是一則來自極星自動化系統的測試脆文）"
        print("未帶參數，執行預設測試文字...")
        publish_thread(text=test_text)
