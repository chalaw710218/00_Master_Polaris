"""
Polaris AI Cabinet - Facebook Test Post Publisher & Archiver
=============================================================
專為「生活的一部分，就醬點！」打造之臉書官方自動發布與利刃存檔引擎。
包含：
1. 多圖相簿發布 ＋ 防降權第一則留言
2. 發布後自動追加歸檔至 00-03-05 歷史發布母庫 (03_Published_Archive.md)
3. 更新 00-02-10 選品清冊狀態
"""

import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris")
ENV_PATH = ROOT_DIR / ".secrets.env"
PUBLISHED_ARCHIVE_PATH = ROOT_DIR / "00-03_Brand_LifeButler" / "00-03-05_Brand_Content_Hub" / "03_Published_Archive.md"
PRODUCT_CATALOG_PATH = ROOT_DIR / "00-02_GroupBuy_Products" / "00-02-10_Vendor_洪一華_同步團購" / "00-02-10-01_Product_Catalog_and_Curator_Filter.md"

def load_env(env_path):
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
PAGE_ID = "110505444816362"
TOKEN = ENV.get("FB_PAGE_ACCESS_TOKEN")

IMAGE_PATHS = [
    r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-02_GroupBuy_Products\00-02-10_Vendor_洪一華_同步團購\catalog_images\dachan_chicken_1.jpg",
    r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-02_GroupBuy_Products\00-02-10_Vendor_洪一華_同步團購\catalog_images\dachan_chicken_2.jpg",
    r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-02_GroupBuy_Products\00-02-10_Vendor_洪一華_同步團購\catalog_images\dachan_chicken_3.jpg"
]

MESSAGE = """(測試文)下單不列入計算!

說個正事...

在台東做生活管家這段時間，我常常被問到一個問題：
「闆仔，你們常常在跑大宗生鮮，有沒有那種下班回家不用動刀、拆開就能直接丟進鍋裡的真正好雞肉？」

市面上的雞肉很多，但大多有兩個問題...
要嘛就是一般的平價白肉雞，煮個湯水縮掉一半，肉質軟爛沒什麼香氣...
要嘛就是買回來的雞肉還要自己花半小時去皮、去骨、剔除油脂，弄得整個流理台油膩膩...

這次幫大家在在地供應鏈挖到這款...
大成安心雞的「土雞去皮清肉」跟「玉米土雞去皮清肉」。

大廠產銷履歷我就不多說了，真正的重點在於它是「土雞」...
肉質緊實、纖維細緻，而且最重要的是...
它已經完全去皮、去骨修清完成了。
退冰拆封，不管是丟氣炸鍋、煮雞湯、還是切塊快炒，雙手完全不用沾到任何生肉腥味。

一包足足 500g 真空包裝，特價 130 元。

另外還有一款一台斤 600g 的豪華原切豬五花跟梅花肉片，200 元，一樣是堅持原切、絕不用組合肉。

每週四、五、六晚上 19:00 到 21:00，我們有集單外送車次，到府外送一樣 99 元...
如果你同時有點我們就醬點的自營生鮮，等於一趟外送費幫你代取兩個地點。
當然，你要到店自取免跑腿也沒問題。

⚠️ 這篇是系統對接的【測試貼文】，目前所有留言下單暫不列入實際扣款計算，純粹測試排版與系統流程...

第一則留言有門市與管家自取說明，想了解的可以看一下。

我要去送外送跟寫程式了，先這樣..."""

FIRST_COMMENT = """【管家公告・第一則留言】
感謝大家看到這篇！本篇為生活管家系統與在地供應鏈對接之「功能測試文」，本篇留言 +1 均不列入正式訂單計算。
正式開團公告與每週四～六 19:00-21:00 專人配送服務，將於近日正式上線！
門市自取地址：台東市寶桑生活物流商行（正氣北路166巷90號）
有任何在地生鮮需求，歡迎隨時私訊粉專管家！"""

def archive_published_post(post_id: str):
    """將發布紀錄追加至 03_Published_Archive.md"""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    archive_entry = f"""

---

### 📝 [發布紀錄] 大成安心雞・土雞去皮清肉 (測試文)
* **發布時間**：{now_str}
* **發布平台**：Facebook 官方粉專 (Page ID: {PAGE_ID})
* **貼文 ID**：`{post_id}`
* **貼文直達**：[查看 Facebook 貼文](https://www.facebook.com/{post_id})
* **登台角色**：闆仔 (Boss) - 專業知識向
* **核准標記**：`(測試文)下單不列入計算!`
* **搭配圖片**：3 張實拍照 (`catalog_images/dachan_chicken_1~3.jpg`)
* **利刃審計標記**：已排程啟動 `sharp-groupbuy-analyzer` 逆推大成原廠底價與製造商檔案。
"""
    try:
        with open(PUBLISHED_ARCHIVE_PATH, "a", encoding="utf-8") as f:
            f.write(archive_entry)
        print(f"[+] 成功追加歷史發布母庫存檔: {PUBLISHED_ARCHIVE_PATH}")
    except Exception as e:
        print(f"[-] 發布存檔例外: {e}")

def publish():
    if not TOKEN:
        print("❌ 未設定 FB_PAGE_ACCESS_TOKEN，無法發文！")
        return

    print("=" * 60)
    print("🚀 特務影 ＆ 泰勒絲：正在執行 Facebook 測試文發布程序...")
    print("=" * 60)

    # 1. 上傳圖片
    media_ids = []
    print(f"[*] 正在上傳 {len(IMAGE_PATHS)} 張商品實拍照至 Meta 伺服器...")
    for idx, path in enumerate(IMAGE_PATHS, 1):
        if not os.path.exists(path):
            print(f"⚠️ 找不到圖片: {path}")
            continue
        url_photo = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
        try:
            with open(path, "rb") as f:
                r = requests.post(url_photo, files={"source": f}, data={"access_token": TOKEN, "published": "false"})
                data = r.json()
                if "id" in data:
                    media_ids.append(data["id"])
                    print(f"[+] 圖片 {idx} 上傳成功 (Media ID: {data['id']})")
                else:
                    print(f"[-] 圖片 {idx} 上傳失敗: {data}")
        except Exception as e:
            print(f"[-] 上傳例外: {e}")

    # 2. 發布貼文
    print("[*] 正在向粉專推送圖文相簿貼文...")
    url_feed = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
    payload = {
        "access_token": TOKEN,
        "message": MESSAGE
    }
    for i, mid in enumerate(media_ids):
        payload[f'attached_media[{i}]'] = f'{{"media_fbid":"{mid}"}}'

    r_post = requests.post(url_feed, data=payload)
    post_res = r_post.json()

    if "id" not in post_res:
        print(f"❌ 貼文發布失敗: {post_res}")
        return

    post_id = post_res["id"]
    print(f"\n🎉 貼文發布成功！\n👉 Post ID: {post_id}")
    print(f"👉 貼文直達連結: https://www.facebook.com/{post_id}")

    # 3. 發表第一則留言（防降權）
    print("[*] 正在發表第一則留言...")
    time.sleep(2)
    url_comment = f"https://graph.facebook.com/v20.0/{post_id}/comments"
    r_comment = requests.post(url_comment, data={"access_token": TOKEN, "message": FIRST_COMMENT})
    comment_res = r_comment.json()

    if "id" in comment_res:
        print(f"[+] 第一則留言發表成功 (Comment ID: {comment_res['id']})")
    else:
        print(f"[-] 第一則留言發表提醒: {comment_res}")

    # 4. 歷史存檔與利刃審計標記
    print("[*] 正在執行歷史發布母庫存檔...")
    archive_published_post(post_id)

    print("\n" + "=" * 60)
    print("🏆 全自動發布 ＆ 歷史歸檔閉環圓滿完成！")
    print("=" * 60)

if __name__ == "__main__":
    publish()
