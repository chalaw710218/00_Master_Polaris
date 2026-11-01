# 🚀 Make.com 敏捷通道直連 Google 商家 5 分鐘配置指南

> **專案主理**：情報長 雪柔 (Sheryl Sandberg / 獵鷹)  
> **適用場景**：在 Google 官方配額審核期（7~10天）期間，透過 Make.com 官方認證白名單跳板，讓 Python 腳本今晚立刻能一鍵直發「職人食堂」動態至 Google 地圖！

---

## 🎯 一、 運作原理（為什麼 Make 免審核？）

* **Google 官方白名單**：Make.com 已經通過 Google 企業級最高審核，擁有龐大的 GBP API 呼叫配額。
* **您的角色**：您是「職人食堂」的管理員。當您在 Make 裡登入 Google 帳號授權時，Make 會拿到代表您管理該門市的合法 Token。
* **極星自動化接軌**：Make 提供一個 Webhook 網址給我們，極星的 Python 腳本只要一行 `requests.post()` 把動態文字與圖片傳過去，Google 地圖**秒級發布**！

---

## 🛠️ 二、 今晚 5 分鐘圖解配置步驟

### 步驟 1：免費註冊 / 登入 Make.com
* 開啟瀏覽器進入 👉 **[https://www.make.com](https://www.make.com)**
* 免費註冊或直接使用 Google 帳號登入（免費方案每月有 1,000 次操作額度，對發貼文綽綽有餘！）。

---

### 步驟 2：建立一個新情境 (Create a new scenario)
1. 進入後台首頁，點擊右上角的紫色按鈕 **【Create a new scenario】**。
2. 畫面中間會出現一個大大的紫色加號 **`+`**。

---

### 步驟 3：配置第一個節點【Custom Webhook】（接收 Python 發出的動態）
1. 點擊加號，在搜尋框輸入：`Webhooks`。
2. 選擇 **Webhooks** ➔ 點擊 **Custom webhook**。
3. 點擊 **Add**，將 Webhook 名稱命名為：`Polaris_GBP_Post`。
4. 點擊 **Save**。
5. **重要**：畫面上會出現一串網址（例如：`https://hook.eu2.make.com/abcdef123456...`）。
   * 點擊 **【Copy address to clipboard】**（複製下來，今晚貼給我即可！）。

---

### 步驟 4：配置第二個節點【Google Business Profile】（官方直連發布）
1. 在 Webhook 圓圈右側，點擊 **【Add another module】**（小加號）。
2. 在搜尋框輸入：`Google Business Profile`。
3. 選擇 **Google Business Profile** ➔ 點擊 **Create a Post**（建立動態）。
4. **帳號授權 (Connection)**：
   * 點擊 **Add** ➔ 點擊 **Sign in with Google**。
   * **選取您身為「職人食堂管理員」的 Google 帳號**，跳出授權視窗點擊「允許」。
5. **選定門市 (Location)**：
   * 授權成功後，在 **Account** 下拉選單選取您的帳號名稱。
   * 在 **Location** 下拉選單中，會直接看見 👉 **【職人食堂】**！點選它！
6. **欄位對應 (Mapping)**：
   * **Topic Type**：選取 `STANDARD` (一般最新動態)
   * **Summary (內文)**：點擊輸入框，選取左邊 Webhook 傳來的 `summary`
   * **Call To Action (按鈕)**：
     * Action Type：選取 `CALL` (致電)
     * URL / Phone：選取 Webhook 傳來的 `phone` 或直接填 `089342900`
   * **Media (圖片)**：若要帶圖，將 Image URL 對應 Webhook 的 `image_url`
7. 點擊右下角 **Save**，並將左下角的排程開關切換為 **【ON】** (Immediately as data arrives)。

---

## 💻 三、 極星端的 Python 一鍵直發腳本

當您晚上把複製到的 Webhook 網址給我後，我們資料夾裡的 [`send_post_via_webhook.py`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-05_AI_Education/Tutorial_08_Google_Business_AI_Manager/send_post_via_webhook.py) 只要執行：

```bash
python send_post_via_webhook.py
```

* **系統就會自動把安慶街 60 號的「爆汁小籠湯包現蒸堅持」動態直接推送至 Google Maps！**
* 整個過程零延遲、不報錯、完全繞開 Google 7 天配額等待期！
