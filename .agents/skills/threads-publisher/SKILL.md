---
name: threads-publisher
description: 萬用 Threads 官方自動發文與留言巡邏秒回技能。支援純文字爆款貼文、圖片貼文發布，以及自動化巡邏留言區並以指定人設（如喵編）進行高情商接梗回覆。
---
# 脆友全自動發文與秒回機 (Threads Universal Publisher & Replier)

## 技能說明
這是一個極星通用的 Threads 官方自動化技能。
支援**「即時發布脆文」**、**「帶圖脆文發布」**以及**「留言區全自動巡邏與高情商秒回」**三大能力。
透過 Meta Threads 官方 API，直連 `.secrets.env` 中的 60 天長效金鑰，實現零人工手動的社群經營閉環。

## 觸發時機
當使用者表示：
* 「幫我發到 Threads」、「把這篇發脆」、「發送這篇 Threads 貼文」（👉 **即時發文模式**）
* 「幫我檢查 Threads 留言」、「巡邏留言並回覆」、「啟動回覆機器人」（👉 **自動回覆模式**）
* 「一鍵發布草稿池第 X 篇」（👉 **草稿池調用發文**）

---

## 執行流程

### 模式 A：Threads 自動發文 (Publish Mode)

#### Step 1: 確認發布內容
* 取得欲發布的文字內容（500 字以內，符合 Threads 呼吸感排版）。
* **支援本地圖片上傳**：若有附帶圖片，無論是本機檔案路徑（如 `C:/photo.jpg`）或網路 URL，腳本都會自動上傳至 Meta 官方 CDN，無縫完成帶圖發布！

#### Step 2: 執行發布腳本模板
調用以下封裝腳本（自動由極星根目錄 `.secrets.env` 取得金鑰）：

```python
import os
import sys
import time
import requests
from pathlib import Path

# 確保 Windows 支援 UTF-8 Emoji
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def load_env():
    # 往上回溯尋找 .secrets.env
    cur = Path.cwd()
    for parent in [cur] + list(cur.parents):
        env_file = parent / ".secrets.env"
        if env_file.exists():
            env_vars = {}
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env_vars[k.strip()] = v.strip()
            return env_vars
    return {}

env = load_env()
USER_ID = env.get("THREADS_USER_ID")
TOKEN = env.get("THREADS_ACCESS_TOKEN")
API_BASE = "https://graph.threads.net/v1.0"

def publish_thread(text, image_url=None):
    if not USER_ID or not TOKEN:
        print("❌ 錯誤：尚未設定 THREADS_USER_ID 或 THREADS_ACCESS_TOKEN")
        return None

    # 1. 建立容器
    payload = {
        "access_token": TOKEN,
        "text": text,
        "media_type": "IMAGE" if image_url else "TEXT"
    }
    if image_url:
        payload["image_url"] = image_url

    r1 = requests.post(f"{API_BASE}/{USER_ID}/threads", data=payload).json()
    creation_id = r1.get("id")
    if not creation_id:
        print(f"❌ 建立容器失敗: {r1}")
        return None

    time.sleep(2)

    # 2. 正式發布
    r2 = requests.post(f"{API_BASE}/{USER_ID}/threads_publish", data={
        "access_token": TOKEN,
        "creation_id": creation_id
    }).json()

    post_id = r2.get("id")
    if post_id:
        print(f"🎉 發布成功！Post ID: {post_id}")
        print(f"🔗 貼文網址: https://www.threads.net/@/post/{post_id}")
        return post_id
    else:
        print(f"❌ 發布失敗: {r2}")
        return None
```

#### Step 3: 自動記錄與回報
發布成功後，自動於 `03_Published_Archive.md` 記錄發布時間、標題、Post ID 與前台連結，並回報使用者。

---

### 模式 B：Threads 留言自動巡邏與秒回 (Replier Mode)

#### Step 1: 抓取最新貼文與留言樹
調用官方端點：
* `GET /{user-id}/threads?limit=3` 取得最新 3 篇貼文。
* `GET /{media-id}/conversation` 取得所有階層之脆友留言。

#### Step 2: 執行安全過濾機制
1. **防止自己回覆自己**：檢查留言者 `username`，若為自身官方帳號（如 `hellotaitung`），立即略過。
2. **去重記憶庫**：比對本地 `replied_ids.json`，若該則留言 ID 已回覆過，立即跳過，絕不重複騷擾網友。

#### Step 3: 依人設生成神回覆與推播
* 採用**「三秒共情 ＋ 接梗幽默 ＋ 拋出新反問」**公式。
* 呼叫 `POST /{user-id}/threads`，夾帶 `reply_to_id=留言ID` 與 `text=回覆文字` 建立回覆容器並發布。
* 將處理完成之留言 ID 寫入 `replied_ids.json` 歸檔。

---

## 規範與鐵律
1. **金鑰安全**：金鑰必須存放在 `.secrets.env`，嚴禁任何 Token 出現在公開檔案或提交至 GitHub。
2. **文字排版**：每段文字換行留白，維持「短句、有呼吸感」的道地脆味。
3. **無硬廣**：內文零購買連結，引流一律以俏皮口吻引導至個人簡介 (Bio) 傳送門。
