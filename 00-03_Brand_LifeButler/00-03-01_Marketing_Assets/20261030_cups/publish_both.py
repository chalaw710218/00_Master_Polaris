import os
import sys
import time
import requests
from pathlib import Path

# Fix Windows console UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris")
ENV_PATH = ROOT_DIR / ".secrets.env"

def load_env(env_path):
    env_vars = {}
    if not env_path.exists():
        print(f"⚠️ 找不到金鑰設定檔: {env_path}")
        return env_vars
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()
    return env_vars

ENV = load_env(ENV_PATH)
FB_PAGE_ACCESS_TOKEN = ENV.get("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = "110505444816362"
THREADS_USER_ID = ENV.get("THREADS_USER_ID")
THREADS_ACCESS_TOKEN = ENV.get("THREADS_ACCESS_TOKEN")

IMAGE_DIR = ROOT_DIR / "00-03_Brand_LifeButler" / "00-03-01_Marketing_Assets" / "20261030_cups"
IMAGES = [
    IMAGE_DIR / "cup_1.jpg",
    IMAGE_DIR / "cup_2.jpg",
    IMAGE_DIR / "cup_3.jpg",
    IMAGE_DIR / "cup_4.jpg"
]

print("=" * 60)
print("🚀 【極星雙平台發射台】開始執行發布任務...")
print("=" * 60)

# ==========================================
# 1. 發布 Facebook (泰勒絲版)
# ==========================================
print("\n📘 [1/2] 正在處理 Facebook 粉絲專頁發布（泰勒絲操刀）...")

fb_text = """【讓器物開啟第二人生｜家宅 1 樓快閃尋寶，二手良品杯具均一價 10 元】

生活裡總有一些物件，曾經陪伴過某段時光。
可能是某個清晨滾燙的黑咖啡、或是某個午後慢火沖開的茶湯。
整理家宅一樓時，我們把這批依然完好、乾淨的二手杯具細細排開：
不鏽鋼保溫瓶、法式濾壓壺、透光的玻璃茶器、還有帶著歲月痕跡的青花瓷蓋杯。

丟棄太過可惜，不如用最輕鬆的銅板價，讓它們去到真正懂得珍惜的家。

💰 惜物結緣價：通通 10 元 / 個
⏰ 開放時間：明天下午 15:00 - 18:00（僅此 3 小時）
📍 相遇地點：台東市正氣北路 166 巷 90 號（家宅 1 樓）

📌 【現場約定，請彼此體諒與配合】：
1. 線上不做任何回覆：團隊現場忙於備料出貨，恕不回覆留言與私訊確認款式。
2. 先到先得，恕不保留：緣分屬於親自到場的人，挑完為止。
3. 環保自律：現場零錢有限，請大家自備 10 元硬幣與環保提袋。

期待明天下午，在正氣北路與大家溫暖相遇。"""

fb_media_ids = []
fb_cdn_urls = []

for img_path in IMAGES:
    url_photo = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/photos"
    try:
        with open(img_path, "rb") as f:
            r = requests.post(url_photo, files={"source": f}, data={
                "access_token": FB_PAGE_ACCESS_TOKEN,
                "published": "false"
            })
            p_data = r.json()
            if "id" in p_data:
                photo_id = p_data["id"]
                fb_media_ids.append(photo_id)
                print(f"   ↳ 成功上傳 FB 圖片 ID: {photo_id}")
                
                # 同步取得 CDN URL (供 Threads 使用)
                url_query = f"https://graph.facebook.com/v20.0/{photo_id}?fields=images&access_token={FB_PAGE_ACCESS_TOKEN}"
                r2 = requests.get(url_query).json()
                imgs = r2.get("images", [])
                if imgs:
                    fb_cdn_urls.append(imgs[0].get("source"))
            else:
                print(f"   ↳ 圖片上傳失敗: {p_data}")
    except Exception as e:
        print(f"   ↳ 圖片讀取失敗 {img_path}: {e}")

if fb_media_ids:
    url_feed = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/feed"
    payload = {
        "access_token": FB_PAGE_ACCESS_TOKEN,
        "message": fb_text,
        "published": "true"
    }
    for i, mid in enumerate(fb_media_ids):
        payload[f"attached_media[{i}]"] = f'{{"media_fbid":"{mid}"}}'

    r_feed = requests.post(url_feed, data=payload)
    res_feed = r_feed.json()
    if "id" in res_feed:
        fb_post_id = res_feed["id"]
        print(f"🎉 Facebook 發布成功！Post ID: {fb_post_id}")
        print(f"🔗 FB 前台連結: https://www.facebook.com/{fb_post_id}")
    else:
        print(f"❌ Facebook 發布失敗: {res_feed}")
else:
    print("❌ 無法上傳任何圖片至 Facebook，略過貼文建立。")

# ==========================================
# 2. 發布 Threads (影版)
# ==========================================
print("\n🧵 [2/2] 正在處理 Threads 發布（影操刀）...")

threads_text = """家宅一樓大掃除挖到寶……
這整桌二手杯子居然連不鏽鋼保溫瓶跟法式濾壓壺都有 😱

創辦人說通通 10 塊錢出清，誰先來誰帶走。

📍 台東市正氣北路166巷90號（家宅1樓）
⏰ 明天下午 3:00 - 6:00（就這三小時，逾時不候）

⚠️ 脆友注意，看完再出門：
1. 線上我一概不回（問我還有沒有、叫我幫留的，我真的會裝沒看到 🙈）
2. 先到先挑、恕不保留，被挑走就沒了
3. 請自備 10 塊零錢跟購物袋，現場沒零錢找你！

明天下午見，不要太晚來搶光了才哭 🏃💨"""

# Threads 多圖 Carousel
threads_post_id = None
if fb_cdn_urls and THREADS_USER_ID and THREADS_ACCESS_TOKEN:
    api_base = "https://graph.threads.net/v1.0"
    
    # 建立多圖容器
    carousel_item_ids = []
    print("   ↳ 正在建立 Threads Carousel 子相片容器...")
    for idx, cdn_url in enumerate(fb_cdn_urls[:4]):
        r_item = requests.post(f"{api_base}/{THREADS_USER_ID}/threads", data={
            "access_token": THREADS_ACCESS_TOKEN,
            "media_type": "IMAGE",
            "image_url": cdn_url,
            "is_carousel_item": "true"
        }).json()
        item_id = r_item.get("id")
        if item_id:
            carousel_item_ids.append(item_id)
            print(f"      • 子項目 {idx+1} 成功: {item_id}")
        else:
            print(f"      • 子項目 {idx+1} 失敗: {r_item}")
        time.sleep(1)

    if len(carousel_item_ids) >= 2:
        print("   ↳ 正在建立 Threads 輪播主容器...")
        children_str = ",".join(carousel_item_ids)
        r_car = requests.post(f"{api_base}/{THREADS_USER_ID}/threads", data={
            "access_token": THREADS_ACCESS_TOKEN,
            "media_type": "CAROUSEL",
            "children": children_str,
            "text": threads_text,
            "topic_tag": "台東生活"
        }).json()
        creation_id = r_car.get("id")
    elif len(carousel_item_ids) == 1 or fb_cdn_urls:
        print("   ↳ 正在建立 Threads 單圖主容器...")
        r_single = requests.post(f"{api_base}/{THREADS_USER_ID}/threads", data={
            "access_token": THREADS_ACCESS_TOKEN,
            "media_type": "IMAGE",
            "image_url": fb_cdn_urls[0],
            "text": threads_text,
            "topic_tag": "台東生活"
        }).json()
        creation_id = r_single.get("id")
    else:
        creation_id = None

    if creation_id:
        print(f"   ↳ 主容器建立成功: {creation_id}，等待 5 秒轉碼緩衝...")
        time.sleep(5)
        r_pub = requests.post(f"{api_base}/{THREADS_USER_ID}/threads_publish", data={
            "access_token": THREADS_ACCESS_TOKEN,
            "creation_id": creation_id
        }).json()
        
        threads_post_id = r_pub.get("id")
        if threads_post_id:
            print(f"🎉 Threads 發布成功！Post ID: {threads_post_id}")
            print(f"🔗 Threads 前台連結: https://www.threads.net/@hellotaitung/post/{threads_post_id}")
        else:
            print(f"❌ Threads 發布失敗: {r_pub}")
    else:
        print("❌ Threads 容器建立失敗！")

print("\n" + "=" * 60)
print("🏁 雙平台發布任務執行完畢！")
print("=" * 60)
