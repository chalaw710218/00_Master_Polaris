# 🤖 00-02-10-04 極星 AI 託管社團抓單引擎操作手冊

> **模組路徑**：[`00-02-10_Vendor_洪一華_同步團購/tools/scrape_fb_group_orders.py`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-02_GroupBuy_Products/00-02-10_Vendor_洪一華_同步團購/tools/scrape_fb_group_orders.py)  
> **技術核心**：Playwright Persistent Context ＋ 台灣團購語意神經剖析器  
> **風控等級**：本機託管模式（零封號、與日常 Chrome 乾淨隔離）

---

## ⚡ 核心能力與特色

1. **AI 全自動代勞**：您不再需要手動點書籤，只要把 Facebook 社團貼文網址丟給 AI，系統背景自動滾動展開所有留言。
2. **台灣團購語意深度解析**：
   - 自動辨識 `+1`、`+2`、`＋1`、`要2包`、`來3份`、`買1盒`。
   - 自動判讀履約需求：辨識 `外送`（自動帶入 99 元配送費）或 `自取`。
   - 自動過濾純詢問、無效閒聊與重複喊單。
3. **無縫對齊標準帳本**：
   - 抓取完畢後，直接自動追加寫入 [`00-02-10-03_Order_Tracker_Template.csv`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-02_GroupBuy_Products/00-02-10_Vendor_洪一華_同步團購/00-02-10-03_Order_Tracker_Template.csv)，7 大標準欄位一次備齊。

---

## 🔑 首次啟用：一分鐘綁定臉書登入狀態

設定檔安全儲存於 `C:\Users\lenovo\.gemini\polaris_fb_browser_data`，只需登入一次即可永久受惠：

### 步驟說明：
1. 在終端執行以下指令（開啟可見視窗）：
   ```powershell
   python "c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-02_GroupBuy_Products\00-02-10_Vendor_洪一華_同步團購\tools\scrape_fb_group_orders.py" --url "https://www.facebook.com" --headed
   ```
2. 在彈出的 Chrome 視窗中，登入您的 Facebook 帳號。
3. 登入成功後，直接關閉該瀏覽器視窗。
4. **大功告成！** 往後所有自動化抓單皆會在後台無聲無息完成，絕不再需要登入！

---

## 🚀 日常抓單使用方式（極致省力）

### 方式 A：直接在對話框跟 AI 說（最推薦）
您只要把社團貼文網址貼在對話框：
> *「幫我抓這篇社團貼文的訂單：https://www.facebook.com/groups/.../posts/...」*

AI 內閣會自動在背景啟動腳本，5 秒內將統計結果（幾位客人、總共幾包、是否達到 +3 門檻）呈報給您，並同步寫入 CSV！

### 方式 B：自行在終端執行
```powershell
python "c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-02_GroupBuy_Products\00-02-10_Vendor_洪一華_同步團購\tools\scrape_fb_group_orders.py" --url "貼文網址" --product_code "HYH-001" --product_name "屏東午仔魚"
```
