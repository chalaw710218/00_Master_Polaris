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

IMAGE_DIR = ROOT_DIR / "00-03_Brand_LifeButler" / "00-03-01_Marketing_Assets" / "20261106_cups"
IMAGES = [
    IMAGE_DIR / "cups_table_1.jpg",
    IMAGE_DIR / "cups_table_2.jpg"
]

print("=" * 60)
print("🚀 【極星發射台】二手生活器物出清快閃・雙平台發布準備中...")
print("=" * 60)

# ==========================================
# 1. Facebook (泰勒絲版)
# ==========================================
fb_text = """【惜物快閃尋寶｜二手生活器皿與杯具，每件通通 10 元！】

家宅一樓再次整理出一批狀況良好、乾淨實用的生活器具。
看照片就知道——復古印花玻璃杯、不鏽鋼保溫隨行杯、沖咖啡必備的壺具、細緻的陶瓷小碗、茶杯與馬克杯，整整齊齊排滿一桌。

這些器物曾經承載過日常的溫度，丟棄太過可惜。
我們用一個銅板價，讓它們去到真正需要的地方，開啟下一段生活旅程。

💰 惜物價：每件均一價 10 元
⏰ 開放時間：明天（星期六）下午 15:00 - 18:00（僅此 3 小時）
📍 相遇地點：台東市正氣北路 166 巷 90 號（家宅 1 樓）

📌 【現場重要約定，請大家共同配合】：
1. 線上不做任何回應：現場夥伴全力忙於備料與出貨，恕不回覆私訊、留言問庫存。
2. 先到先挑、恕不保留：緣分屬於親自到場的人，挑完為止。
3. 自律環保：現場零錢有限，請大家自備 10 元硬幣與環保提袋。

明天下午，歡迎順路來家宅 1 樓尋寶！"""

# ==========================================
# 2. Threads (影版)
# ==========================================
threads_text = """這桌又被清出來了……😱
復古印花玻璃杯、不鏽鋼隨行保溫瓶、咖啡壺、陶瓷小碗，整整齊齊排滿桌。

老闆說：通通一個銅板 10 塊錢帶走！

📍 台東市正氣北路166巷90號（家宅1樓）
⏰ 明天星期六下午 3:00 - 6:00（就這三小時，逾時不候）

⚠️ 影的防呆提醒，看完再出門：
1. 線上我一概不回覆（問還有沒有、叫我幫留的，我真的會裝沒看到 🙈）
2. 先到先挑、恕不保留，挑完就沒了
3. 請自備 10 元硬幣跟購物袋，現場沒零錢找你！

明天下午三點，家宅見，手慢無 🏃💨"""

def launch_facebook():
    print("\n📘 [1/2] 正在推送至 Facebook 粉絲專頁（泰勒絲操刀）...")
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
                    print(f"   ↳ 成功上傳 FB 相片 ID: {photo_id}")
                    
                    url_query = f"https://graph.facebook.com/v20.0/{photo_id}?fields=images&access_token={FB_PAGE_ACCESS_TOKEN}"
                    r2 = requests.get(url_query).json()
                    imgs = r2.get("images", [])
                    if imgs:
                        fb_cdn_urls.append(imgs[0].get("source"))
                else:
                    print(f"   ↳ 相片上傳失敗: {p_data}")
        except Exception as e:
            print(f"   ↳ 讀取失敗: {e}")

    if fb_media_ids:
        url_feed = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/feed"
        payload = {
            "access_token": FB_PAGE_ACCESS_TOKEN,
            "message": fb_text,
            "published": "true"
        }
        for i, mid in enumerate(fb_media_ids):
            payload[f"attached_media[{i}]"] = f'{{"media_fbid":"{mid}"}}'

        res_feed = requests.post(url_feed, data=payload).json()
        if "id" in res_feed:
            fb_post_id = res_feed["id"]
            print(f"🎉 Facebook 發布成功！Post ID: {fb_post_id}")
            print(f"🔗 FB 前台連結: https://www.facebook.com/{fb_post_id}")
            return fb_post_id, fb_cdn_urls
        else:
            print(f"❌ Facebook 發布失敗: {res_feed}")
    return None, fb_cdn_urls

def launch_threads(fb_cdn_urls):
    print("\n🧵 [2/2] 正在推送至 Threads（影操刀）...")
    if not (fb_cdn_urls and THREADS_USER_ID and THREADS_ACCESS_TOKEN):
        print("❌ 缺少 Threads 憑證或圖片 CDN 網址！")
        return None

    api_base = "https://graph.threads.net/v1.0"
    carousel_item_ids = []
    for idx, cdn_url in enumerate(fb_cdn_urls[:2]):
        r_item = requests.post(f"{api_base}/{THREADS_USER_ID}/threads", data={
            "access_token": THREADS_ACCESS_TOKEN,
            "media_type": "IMAGE",
            "image_url": cdn_url,
            "is_carousel_item": "true"
        }).json()
        item_id = r_item.get("id")
        if item_id:
            carousel_item_ids.append(item_id)
            print(f"   ↳ 建立輪播子項目 {idx+1}: {item_id}")
        time.sleep(1)

    if len(carousel_item_ids) >= 2:
        children_str = ",".join(carousel_item_ids)
        r_car = requests.post(f"{api_base}/{THREADS_USER_ID}/threads", data={
            "access_token": THREADS_ACCESS_TOKEN,
            "media_type": "CAROUSEL",
            "children": children_str,
            "text": threads_text,
            "topic_tag": "台東生活"
        }).json()
        creation_id = r_car.get("id")
    else:
        r_single = requests.post(f"{api_base}/{THREADS_USER_ID}/threads", data={
            "access_token": THREADS_ACCESS_TOKEN,
            "media_type": "IMAGE",
            "image_url": fb_cdn_urls[0],
            "text": threads_text,
            "topic_tag": "台東生活"
        }).json()
        creation_id = r_single.get("id")

    if creation_id:
        print(f"   ↳ 容器建立成功: {creation_id}，等待 5 秒轉碼緩衝...")
        time.sleep(5)
        r_pub = requests.post(f"{api_base}/{THREADS_USER_ID}/threads_publish", data={
            "access_token": THREADS_ACCESS_TOKEN,
            "creation_id": creation_id
        }).json()
        threads_post_id = r_pub.get("id")
        if threads_post_id:
            print(f"🎉 Threads 發布成功！Post ID: {threads_post_id}")
            print(f"🔗 Threads 前台連結: https://www.threads.net/@hellotaitung/post/{threads_post_id}")
            return threads_post_id
        else:
            print(f"❌ Threads 發布失敗: {r_pub}")
    return None

if __name__ == "__main__":
    fb_id, cdn_urls = launch_facebook()
    threads_id = launch_threads(cdn_urls)
    print("\n" + "=" * 60)
    print("🏁 雙平台發布作業完成！")
    print("=" * 60)
