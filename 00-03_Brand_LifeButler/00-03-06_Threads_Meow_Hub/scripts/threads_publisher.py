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

def prepare_web_safe_video(video_path):
    """
    確保 MP4 包含 Meta Threads 要求之標準音軌 (Silent AAC)、yuv420p 色彩與 faststart header
    """
    import subprocess
    path = Path(video_path)
    if not path.exists():
        return None

    ffmpeg_bin = Path(r"C:\Python312\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe")
    if not ffmpeg_bin.exists():
        return path

    safe_path = path.parent / f"{path.stem}_safe.mp4"
    cmd = [
        str(ffmpeg_bin), "-y",
        "-i", str(path),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest",
        "-movflags", "+faststart",
        str(safe_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and safe_path.exists():
        return safe_path
    return path

def upload_local_video_to_public_cdn(video_path):
    """
    將本地 MP4 短影音上傳至支援 Meta Threads 串流轉碼抓取之公開 CDN (Catbox)
    """
    if not video_path:
        return None
    if str(video_path).startswith("http://") or str(video_path).startswith("https://"):
        return str(video_path)

    safe_video = prepare_web_safe_video(video_path)
    print(f"📤 正在將短影音託管至公開串流 CDN: {safe_video.name}...")
    try:
        with open(safe_video, "rb") as f:
            r = requests.post("https://catbox.moe/user/api.php", data={"reqtype": "fileupload"}, files={"fileToUpload": f}, timeout=30)
        if r.status_code == 200 and r.text.startswith("https://"):
            cdn_url = r.text.strip()
            print(f"✅ 短影音已成功託管至公開串流 CDN: {cdn_url}")
            return cdn_url
    except Exception as e:
        print(f"❌ 影音託管異常: {e}")
    return None

def create_media_container(text, image_url=None, video_url=None, reply_to_id=None, topic_tag=None):
    """
    第一階段：建立 Threads 媒體容器
    :param text: 發文文字內容 (最多 500 字)
    :param image_url: 圖片公開 URL
    :param video_url: 影片公開 URL (MP4 / MOV)
    :param reply_to_id: 若是回覆某則串文或留言，填入該 post/comment ID
    :param topic_tag: Threads 官方主題標籤
    """
    if not THREADS_USER_ID or not THREADS_ACCESS_TOKEN:
        print("❌ 錯誤：尚未在 .secrets.env 中設定 THREADS_USER_ID 或 THREADS_ACCESS_TOKEN！")
        return None

    url = f"{API_BASE}/{THREADS_USER_ID}/threads"
    payload = {
        "access_token": THREADS_ACCESS_TOKEN,
        "text": text
    }

    if video_url:
        payload["media_type"] = "VIDEO"
        payload["video_url"] = video_url
    elif image_url:
        payload["media_type"] = "IMAGE"
        payload["image_url"] = image_url
    else:
        payload["media_type"] = "TEXT"

    if reply_to_id:
        payload["reply_to_id"] = reply_to_id

    if topic_tag:
        payload["topic_tag"] = topic_tag

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

def publish_thread(text, image=None, video=None, reply_to_id=None, topic_tag=None):
    """
    完整發文流程封裝（支援純文字、高清圖片與 MP4 微動態短影音）
    :param text: 貼文內容
    :param image: 可以是公開 HTTP 網址，也可以是電腦本機的圖片路徑 (如 C:/photo.jpg)
    :param video: 可以是公開 HTTP 網址，也可以是電腦本機的 MP4 影片路徑 (如 C:/video.mp4)
    :param reply_to_id: 可選，若為回覆特定串文填入 ID
    :param topic_tag: 可選，Threads 官方主題分類 (例如：台東生活、生活服務、美食外送、耍廢日常、在地服務、好店推薦)
    """
    print("🚀 [喵編發射台] 準備推送貼文至 Threads...")
    
    # 創辦人親定鐵律：發文圖片絕對不可重複使用檢查
    used_registry_file = ROOT_DIR / "00-03_Brand_LifeButler" / "00-03-06_Threads_Meow_Hub" / "data" / "published_image_registry.json"
    if image and not str(image).startswith("http"):
        img_name = Path(image).name
        if used_registry_file.exists():
            try:
                import json
                with open(used_registry_file, "r", encoding="utf-8") as rf:
                    reg = json.load(rf)
                used_names = [item.get("filename") for item in reg.get("published_images", [])]
                if img_name in used_names:
                    print(f"\n🛑【創辦人親定鐵律攔截】：圖片 '{img_name}' 已經在先前的貼文中使用過！發文圖片嚴禁重複！")
                    print("👉 請生成或選用全新未上線過的照片，保障每篇貼文的獨特性與新鮮感。")
                    return None
            except Exception as e:
                print(f"⚠️ 圖片去重檢查警告: {e}")

    # 若未指定 topic_tag 且非回覆留言，啟動智慧主題判定
    if not topic_tag and not reply_to_id:
        text_lower = text.lower()
        if any(k in text_lower for k in ["午仔魚", "生鮮", "外送", "煮飯", "便當", "菜單", "好吃的"]):
            topic_tag = "美食外送"
        elif any(k in text_lower for k in ["跑腿", "代買", "倒垃圾", "服務", "生活管家", "免跑腿"]):
            topic_tag = "生活服務"
        elif any(k in text_lower for k in ["貓", "闆仔", "耍廢", "日常", "偷懶"]):
            topic_tag = "耍廢日常"
        elif any(k in text_lower for k in ["台東", "太平洋", "正氣路", "在地", "山海"]):
            topic_tag = "台東生活"
        else:
            topic_tag = "生活服務" # 預設生活服務同溫層

    if topic_tag and not reply_to_id:
        print(f"🏷️ 掛載主題標籤 (Topic Tag): > {topic_tag}")

    video_url = None
    image_url = None

    if video:
        video_url = upload_local_video_to_public_cdn(video)
        if not video_url:
            print("⚠️ 影片轉載失敗，將嘗試降級為圖片或純文字！")

    if not video_url and image:
        image_url = upload_local_image_to_meta_cdn(image)
        if not image_url:
            print("⚠️ 圖片轉載失敗，將改為純文字發布！")

    creation_id = create_media_container(text=text, image_url=image_url, video_url=video_url, reply_to_id=reply_to_id, topic_tag=topic_tag)
    if not creation_id:
        return None

    # 若為影片容器，必須輪詢轉碼進度 (Polling status until FINISHED)
    if video_url:
        print(f"⏳ 正在等待 Meta 伺服器對短影音進行轉碼 (Creation ID: {creation_id})...")
        for i in range(25):
            time.sleep(5)
            check_url = f"{API_BASE}/{creation_id}?fields=status,error_message&access_token={THREADS_ACCESS_TOKEN}"
            check_res = requests.get(check_url).json()
            status = check_res.get("status")
            print(f"   ↳ 轉碼進度 [{i+1}/25]: {status}")
            if status == "FINISHED":
                print("✨ 影音轉碼就緒！")
                break
            elif status == "ERROR":
                print(f"❌ 影音轉碼失敗: {check_res}")
                return None
        else:
            print("⚠️ 影音轉碼超時！")
            return None
    else:
        # 圖片或純文字容器稍等 3 秒
        time.sleep(3)

    result_post_id = publish_container(creation_id)
    if result_post_id and image and not str(image).startswith("http"):
        try:
            import json
            from datetime import datetime
            img_name = Path(image).name
            if used_registry_file.exists():
                with open(used_registry_file, "r", encoding="utf-8") as rf:
                    reg = json.load(rf)
                reg.setdefault("published_images", []).append({
                    "filename": img_name,
                    "published_at": datetime.now().isoformat(),
                    "post_id": result_post_id,
                    "topic": topic_tag or "生活動態"
                })
                with open(used_registry_file, "w", encoding="utf-8") as wf:
                    json.dump(reg, wf, ensure_ascii=False, indent=2)
                print(f"🔒 已將圖片 '{img_name}' 登記至去重庫，永不重複使用！")
        except Exception as e:
            print(f"⚠️ 登記圖片去重庫提示: {e}")

    return result_post_id

if __name__ == "__main__":
    if len(sys.argv) > 1:
        content = " ".join(sys.argv[1:])
        publish_thread(text=content)
    else:
        test_text = "好，我宣佈這家店被一隻貓接管了喵！🐱（這是一則來自極星自動化系統的測試脆文）"
        print("未帶參數，執行預設測試文字...")
        publish_thread(text=test_text)
