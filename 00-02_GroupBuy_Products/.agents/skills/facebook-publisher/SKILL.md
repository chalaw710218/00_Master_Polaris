---
name: facebook-publisher
description: 將指定商品資料夾內的文案與圖片，全自動發布或預約排程發布至「生活的一部分，就醬點！」Facebook 粉絲專頁。
---
# 臉書自動發文機 (Facebook Auto Publisher)

## 技能說明
這是一個獨立的發文技能。支援**「即時發布」**與**「預約排程發布」**雙模式。將「產出文案」與「實際發文」解耦拆開，讓決策者先確認過文案與圖片滿意後，再呼叫此技能進行最終的臉書推播或定時排程。

## 使用時機
當使用者表示：
* 「幫我發文」、「請將 XX 商品發到臉書」、「執行發文」（👉 **即時發布模式**）
* 「幫我排程在明天下午 3 點發布」、「預約 XX 日期發布」（👉 **預約排程模式**）

---

## 執行步驟

### Step 1: 確認欲發布的目標商品與模式
*   若使用者未明確指定商品，列出目前工作區內的商品資料夾 (如 `00-02-07_Vendor_越臺鹽焗腰果`)，詢問要發布哪一項商品。
*   確認發布模式：
    *   **即時發布**：立即送出公開貼文。
    *   **預約排程**：取得使用者指定的發布時間（支援自然語言如「明天中午12點」、「下週一晚上7點」）。
        *   *Meta 規範限制：排程時間必須在當前時間的 10 分鐘至 75 天之內。*
*   讀取該商品資料夾內的 `行銷企劃與管家文案.md`。

### Step 2: 萃取 FB 專屬文案
*   從 MD 檔案中，精準擷取「### 📌 Facebook 社群文案」下方直到下一個大標題之前的純文字內容。
*   保留所有 Emoji 與換行排版。
*   **【絕對鐵律・避免降權】：臉書貼文內文中絕對不可出現任何外部超連結（包含 http://、https:// 等網址）！**
    *   內文中的 CTA 只能寫：「👉 預約訂購與門市資訊，管家已整理在【第一則留言】中，點擊即可直達！」
    *   所有的外部導流網址（如 LINE 官方帳號、訂單系統網址），一律統一在貼文正式公開後發表於**【第一則留言 (First Comment)】**！

### Step 3: 挑選欲發布的圖片
*   掃描該商品資料夾內的官方實拍照。
*   自動挑選最清晰、最具說服力的 1~5 張官方照片，依序記錄絕對路徑。

### Step 4: 寫入並執行 Python 發文腳本 (支援排程與即時雙模)
套用以下 Python 腳本模板並執行：

```python
import requests
import json
import sys
import datetime

PAGE_ID = '110505444816362'
TOKEN = 'EAATKJBLZArMgBSompnyrNvMzTPUHB3eXZAyAeZASWPEGGdNtZAHrznrabA3lPcunk6XnVukoalmLyUubLxLdpJY0E0ZBE69QhcY0SSIFTnBb0EMOw0JRVYN60ZC1qBtm25ZAZAEYPYolyZBJG2ExPYh1XKD8F2CgZCNxLq5AELgY79G0dmvlFxz42Ap0pOeNZBjTNREuuKPgb2N56svPDlgn4oohngZD'

# 1. 圖片路徑清單
image_paths = [
    r"C:\絕對路徑\1.jpg"
]

# 2. 貼文文案
message = \"\"\"這裡放純文字文案（嚴禁外連網址）\"\"\"

# 3. 排程設定（若為即時發布，設為 None；若為排程發布，填入指定 datetime 物件）
SCHEDULED_TIME = None  # 例如: datetime.datetime(2026, 10, 16, 12, 0, 0)

print('開始上傳圖片至暫存區...')
media_ids = []
for path in image_paths:
    url_photo = f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos'
    try:
        with open(path, 'rb') as f:
            files = {'source': f}
            data = {'access_token': TOKEN, 'published': 'false'}
            r = requests.post(url_photo, files=files, data=data)
            photo_data = r.json()
            if 'id' in photo_data:
                media_ids.append(photo_data['id'])
                print(f'成功上傳圖片 ID: {photo_data["id"]}')
            else:
                print(f'圖片上傳失敗: {photo_data}')
    except Exception as e:
        print(f'讀取圖片失敗 {path}: {e}')

if not media_ids:
    print("沒有成功上傳任何圖片，中止發文。")
    sys.exit(1)

print('開始處理貼文發布/排程...')
url_feed = f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed'
payload = {
    'access_token': TOKEN,
    'message': message,
}

for i, media_id in enumerate(media_ids):
    payload[f'attached_media[{i}]'] = f'{{"media_fbid":"{media_id}"}}'

# 排程判斷邏輯
if SCHEDULED_TIME:
    timestamp = int(SCHEDULED_TIME.timestamp())
    payload['published'] = False
    payload['scheduled_publish_time'] = timestamp
    print(f'設定排程時間為: {SCHEDULED_TIME.strftime("%Y-%m-%d %H:%M:%S")} (Timestamp: {timestamp})')
else:
    payload['published'] = True

r2 = requests.post(url_feed, data=payload)
result = r2.json()

if 'id' in result:
    post_id = result["id"]
    if SCHEDULED_TIME:
        print(f'✅ 貼文排程成功！Post ID: {post_id}，預計於 {SCHEDULED_TIME} 自動公開發布。')
    else:
        print(f'✅ 貼文即時發布成功！Post ID: {post_id}')
        
        # 即時發布時秒級發表第一則留言
        first_comment_text = """👉 點擊加入管家專屬 LINE 官方帳號（內有完整系統可直接點選訂購）：
https://lin.ee/z83YSq6

📍【門市取貨資訊】
• 取貨地址：台東市正氣北路166巷90號
• 服務區域：台東市區、知本、南王、都蘭、東河專人配送"""

        url_comment = f'https://graph.facebook.com/v20.0/{post_id}/comments'
        comment_payload = {
            'access_token': TOKEN,
            'message': first_comment_text
        }
        r_comment = requests.post(url_comment, data=comment_payload)
        c_res = r_comment.json()
        if 'id' in c_res:
            print(f'✅ 第一留言發布成功！Comment ID: {c_res["id"]}')
        else:
            print(f'⚠️ 第一留言未成功: {c_res}')
else:
    print(f'❌ 貼文處理失敗: {result}')
    sys.exit(1)
```

### Step 5: 回報使用者與記錄歸檔
*   若為即時發布：回報成功並提醒前往前台粉專確認。
*   若為預約排程：回報預約成功與預計推播時間，並在 `02_Content_Matrix.md` 與 `03_Published_Archive.md` 標記為【已排程・待發布】。
