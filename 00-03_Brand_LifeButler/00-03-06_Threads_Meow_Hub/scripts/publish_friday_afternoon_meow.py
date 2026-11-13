import os
import sys
import json
import time
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = ROOT_DIR / ".secrets.env"
HUB_DIR = Path(__file__).resolve().parent.parent
SESSION_PATH = Path(__file__).resolve().parent / "threads_session.json"
PROOF_DIR = Path(__file__).resolve().parent / "screenshots"
PROOF_DIR.mkdir(parents=True, exist_ok=True)

def load_env(env_path):
    if not env_path.exists():
        return {}
    env_vars = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()
    return env_vars

ENV = load_env(ENV_PATH)
TOKEN = ENV.get("THREADS_ACCESS_TOKEN")
USER_ID = ENV.get("THREADS_USER_ID")
API_BASE = "https://graph.threads.net/v1.0"

def upload_to_imgbb(image_path):
    """上傳至公開 CDN 取得 Threads 官方要求之公網圖片 URL"""
    key = ENV.get("IMGBB_API_KEY", "b3a88cbdb6b7852c9ff506ecf58bc1fc")
    with open(image_path, "rb") as f:
        res = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": key},
            files={"image": f},
            timeout=30
        )
    data = res.json()
    if data.get("success"):
        return data["data"]["url"]
    raise Exception(f"ImgBB 上傳失敗: {data}")

def publish_friday_afternoon(image_path):
    print("==================================================")
    print("🚀 [週五下午茶專場 · 喵編隨筆記發布啟動]")
    print("==================================================")
    
    post_text = """剛剛看著小編盯著手機看盤，
整張臉隨著數字一下綠一下紅。

本喵在老木桌底下伸個大懶腰，
用肉墊拍了拍他的拖鞋。

其實不管今天 2330 還是大盤漲跌多少，
螢幕上的數字要是沒換成剛出爐的炸物，
那就只是伺服器裡的電子跳動喵！

台股都收盤了，
今天可是星期五下午耶！
肚子是自己的，
放假前必須好好犒賞自己一頓。

管家已經把熱湯備在玄關，
如果今晚只能選一樣當下班犒賞，
你打算買香酥多汁的現炸大雞腿，
還是點一份加辣的無骨鹽酥雞？🍗

#週五快樂"""

    print("📤 正在上傳真實 35mm 暖光照片至 CDN...")
    image_url = upload_to_imgbb(image_path)
    print(f"✅ 圖片 CDN URL 取得: {image_url}")

    # 1. 建立 Media Container
    print("📦 正在建立 Threads 媒體容器...")
    create_url = f"{API_BASE}/{USER_ID}/threads"
    create_payload = {
        "media_type": "IMAGE",
        "image_url": image_url,
        "text": post_text,
        "topic_tag": "週五快樂",
        "access_token": TOKEN
    }
    r = requests.post(create_url, data=create_payload, timeout=30).json()
    container_id = r.get("id")
    if not container_id:
        raise Exception(f"建立媒體容器失敗: {r}")
    print(f"✅ 媒體容器已就緒: {container_id}")

    # 等待媒體容器處理
    time.sleep(5)

    # 2. 正式發布貼文
    print("📢 正在發布至 Threads 公域...")
    pub_url = f"{API_BASE}/{USER_ID}/threads_publish"
    r2 = requests.post(pub_url, data={"creation_id": container_id, "access_token": TOKEN}, timeout=30).json()
    post_id = r2.get("id")
    if not post_id:
        raise Exception(f"發布貼文失敗: {r2}")
    print(f"🎉 貼文發布成功！Post ID: {post_id}")

    # 取得 Permalink
    permalink = ""
    try:
        info_url = f"{API_BASE}/{post_id}?fields=permalink&access_token={TOKEN}"
        p_res = requests.get(info_url, timeout=15).json()
        permalink = p_res.get("permalink", "")
        print(f"🔗 貼文永久連結: {permalink}")
    except Exception:
        pass

    # 3. 立即發布作者公開首回覆（點火推薦池）
    print("\n💬 正在發布作者公開首回覆（管家影款待點火）...")
    first_reply_text = "（默默端上一盤現切芭樂跟熱麥茶）今天不管戰況如何，走出公司推開門，就好好把生活接回自己手裡。想吃熱騰騰炸物又不想排隊吹風的話，生活管家任意門在主頁，隨時替你跑腿送到門口。今晚好好放鬆～🍵✨"
    
    rep_container_url = f"{API_BASE}/{USER_ID}/threads"
    rep_payload = {
        "media_type": "TEXT",
        "text": first_reply_text,
        "reply_to_id": post_id,
        "access_token": TOKEN
    }
    rc = requests.post(rep_container_url, data=rep_payload, timeout=20).json()
    rep_cid = rc.get("id")
    reply_id = ""
    if rep_cid:
        time.sleep(3)
        rp = requests.post(pub_url, data={"creation_id": rep_cid, "access_token": TOKEN}, timeout=20).json()
        reply_id = rp.get("id", "")
        print(f"✅ 作者公開首回覆發布成功！Reply ID: {reply_id}")

    # 4. 前台 Playwright 截圖存證
    proof_path = PROOF_DIR / f"walk_v3_{post_id}_meow_friday_afternoon_verified.png"
    if permalink and SESSION_PATH.exists():
        print("\n📸 前往前台進行實景存證截圖...")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    storage_state=str(SESSION_PATH),
                    viewport={"width": 1280, "height": 900},
                    locale="zh-TW"
                )
                page = context.new_page()
                page.goto(permalink, wait_until="domcontentloaded", timeout=25000)
                page.wait_for_timeout(4000)
                page.screenshot(path=str(proof_path))
                browser.close()
                print(f"✅ 實景截圖存證完成: {proof_path}")
        except Exception as e:
            print(f"⚠️ 截圖異常 (貼文仍已成功發布): {e}")

    # 5. 存檔營運日誌
    out_result = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "persona": "Meow Editor (店貓喵編) ✕ Shadow (生活管家 影)",
        "theme": "週五收盤下午茶 ✕ 股市代碼三不三轉降維轉譯 ✕ 犒賞雞腿",
        "post_id": post_id,
        "permalink": permalink,
        "reply_id": reply_id,
        "image_url": image_url,
        "proof_screenshot": str(proof_path) if proof_path.exists() else ""
    }
    with open(HUB_DIR / "scripts" / "latest_friday_snack_result.json", "w", encoding="utf-8") as f:
        json.dump(out_result, f, ensure_ascii=False, indent=2)

    return out_result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        img_p = Path(sys.argv[1])
        publish_friday_afternoon(img_p)
    else:
        print("請提供照片絕對路徑！")
