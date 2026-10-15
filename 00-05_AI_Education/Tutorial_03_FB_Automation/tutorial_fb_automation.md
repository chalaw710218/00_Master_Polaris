# 零手動！打造專屬 AI 管家：從商品分析到臉書自動發文的全自動化實戰

在 AI 時代，如果你的工作流還停留在「請 ChatGPT 寫文案 ➡️ 手動複製 ➡️ 貼到臉書發布」，那其實只發揮了 AI 一半的潛力！真正的自動化，是讓 AI Agent 幫你完成從「分析、寫作」到「最終上架發布」的一條龍服務。

今天這篇文章，我們將揭開 **「Facebook Graph API 自動發文」** 的神秘面紗。並且獨家大公開：近期許多開發者在 Meta 後台卡關的「隱藏權限陷阱」該如何破解！

---

## 💡 為什麼要串接 Facebook API？
對於經營電商、團購或自媒體的商家來說，每天上架新品是一件耗時的苦差事。透過串接 Facebook API，你可以建置一個專屬的「AI 管家」。
以我們的實戰經驗為例：只要把廠商的「海鮮報價與照片」丟給 AI，AI 就會自動分析定價、生成情境圖、寫好社群文案，最後**自動排版並推播到粉絲專頁**，完全不需要人工按下滑鼠！

---

## 🛠️ 第一關：潛入 Meta 開發者後台
要讓 AI 擁有發文能力，我們必須取得一把「存取權杖 (Access Token)」。

1. 前往 [Meta for Developers](https://developers.facebook.com/) 註冊開發者帳號。
2. 點擊「建立應用程式 (Create App)」。
3. 應用程式類型選擇「其他 (Other)」 ➡️ 「企業商家 (Business)」。
4. 命名你的應用程式（例如：就醬點自動發文機）並建立。

---

## ⚠️ 第二關：破解 Meta 的「隱藏權限陷阱」（精華重點）
建立好應用程式後，我們需要進入「圖形 API 測試工具 (Graph API Explorer)」。發文必備的權限是 `pages_manage_posts`，但很多人在這裡卡關：**在新增權限的下拉選單中，根本找不到這個選項！**

**💡 獨家破解法：**
這是 Meta 近期改版「使用案例 (Use Cases)」架構後的陷阱。你不能直接在測試工具硬要權限，你必須先在應用程式的後台設定中，把相關的基礎權限（如 Facebook Login）打開，測試工具那邊才會解除封印，讓你在下拉選單中選取 `pages_manage_posts`。這是一個非常容易踩坑的細節！

---

## 🔑 第三關：取得「無敵長效權杖」
有了權限後，取權杖的「順序」非常重要：
1. **先拿 User Token**：在測試工具的「User or Page」選單中，先維持 `User Access Token`，並授權 `pages_manage_posts` 等權限，這時會跳出 FB 授權畫面，請務必勾選你的粉絲專頁。
2. **切換 Page Token**：授權完畢後，再次點擊下拉選單，這時你的「粉絲專頁名稱」就會神奇地出現了！**點選它，上方會產生一串全新的權杖，這才是真正能發文的 Page Token。**
3. **延長效期**：點擊權杖旁邊的藍色 `ⓘ` 圖示，進入「延長存取權杖」，把原本只有兩小時的權杖，轉換成 60 天以上的長效型權杖。

---

## 🤖 第四關：Python 自動發文腳本大公開
拿到長效權杖後，我們就可以讓 AI 執行發文腳本了。臉書發布帶有圖片的貼文屬於「兩段式打法」：
1. 先把圖片上傳到草稿區取得 `media_id`。
2. 再把文案與 `media_id` 一起發布。

以下是實戰可用的 Python 腳本範本：

```python
import requests
import urllib.parse

PAGE_ID = '你的粉絲專頁ID'
TOKEN = '你的長效型 Page Token'
IMAGE_PATH = 'C:/你的圖片路徑.jpg'
MESSAGE = '這是由 AI 管家自動分析並發布的貼文！'

# 1. 上傳圖片
print('上傳圖片中...')
url_photo = f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos'
with open(IMAGE_PATH, 'rb') as f:
    files = {'source': f}
    data = {'access_token': TOKEN, 'published': 'false'}
    r = requests.post(url_photo, files=files, data=data)
    media_id = r.json().get('id')

# 2. 發布貼文
if media_id:
    print('發布貼文中...')
    url_feed = f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed'
    payload = {
        'access_token': TOKEN,
        'message': MESSAGE,
        'attached_media[0]': f'{{"media_fbid":"{media_id}"}}'
    }
    requests.post(url_feed, data=payload)
    print('貼文發布成功！')
```

---

## 🎯 結語
當你成功跑通這個流程，你的 AI 就不再只是一個「聊天機器人」，而是一個真正能幫你推進業務的「數位分身」。快去試試看，解放你的雙手吧！
