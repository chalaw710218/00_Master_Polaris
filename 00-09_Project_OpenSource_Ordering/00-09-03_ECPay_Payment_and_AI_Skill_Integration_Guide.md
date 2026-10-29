# 💳 綠界科技金流申請與 ECPay AI Skill 整合手冊 (ECPay Payment & AI Integration Guide)

> **歸檔日期**：2026-10-29  
> **歸檔核定**：創辦人（品碩）指令封存備查  
> **主管首長**：工程長兼技術架構師 · 林納斯 (Linus Torvalds)  
> **歸檔定位**：作為「生活管家」線上自動收款、「AI 家教實戰班」學費金流、以及 `00-09` 開源點餐系統 B2B 金流模組之核心技術與商業存檔。

---

## 📌 一、 外部資源與申請通道清冊 (External Endpoints)

| 項目 | 資源名稱 | 原始來源 / 網址 | 用途說明 |
| :--- | :--- | :--- | :--- |
| **01** | **綠界特約商戶快速申請通道** | [ECPay AI 市集 - 快速申請](https://marketplace.ecpaydata.com.tw/products/admin_d0f97ed0afc64b5f82b6ffca40022533)<br>直連進件：[綠界特約商店申請 (SalesCode=1240)](https://member.ecpay.com.tw/FS/RegisterSpecialStore?SalesCode=1240) | 商業營運端。供生活管家或特定業務開通線上刷卡、超商代碼、ATM 虛擬帳號、Apple Pay 及電子發票特約商戶。 |
| **02** | **綠界.Developers (AI 市集)** | [ECPay AI 市集 - Developers](https://marketplace.ecpaydata.com.tw/products/admin_75f2c5c975c84ae2951f9b2e74399677) | 綠界官方提供之 AI 整合產品說明頁。 |
| **03** | **ECPay API Skill 官方倉庫** | [GitHub - ECPay/ecpay-api-skill](https://github.com/ECPay/ecpay-api-skill) (當前版本：V3.4) | 綠界官方專為 AI 編程助手（Claude Code、VS Code Copilot、Cursor 等）打造的開源知識套件。 |

---

## 🛠️ 二、 技術核心：綠界 ECPay API AI Skill (林納斯架構摘要)

### 1. 什麼是 ECPay API Skill？
傳統金流串接必須由工程師手動研讀數百頁 PDF 文件、手寫雜湊加密演算法與除錯。  
綠界官方發布之 `ecpay-api-skill` 將全套金流、物流、電子發票與電子收據的 API 規格、加密簽名規則（`CheckMacValue`、`AES-CBC/GCM`）與 134 個經過驗證的程式碼範例結構化，AI 開發助手讀取後即可直接依自然語言生成正確串接代碼。

### 2. 核心技術參數與防呆機制
* **MerchantID**：商店特店編號（金流、物流、發票各自獨立）。
* **HashKey / HashIV**：加解密專用密鑰對，嚴格禁止寫入前端或公開倉庫。
* **CheckMacValue**：檢查碼簽名防竄改機制（先排序參數 -> 串接 HashKey/HashIV -> URL Encode -> 轉小寫 -> SHA256 加密 -> 轉大寫）。
* **ReturnURL (Callback)**：Server-to-Server 背景即時回傳機制，確保消費者關閉瀏覽器亦不丟單。
* **SimulatePaid**：設為 `1` 即可在測試沙盒中模擬付款成功，無需真實刷卡。

### 3. 官方測試沙盒環境參數速查 (Sandbox Test Credentials)
未來進行串接實驗或交由新加入夥伴（LINE Bot / 工程團隊）測試時，直接使用以下官方公開測試資料：

* **測試 MerchantID**：`3002607`
* **測試 HashKey**：`pwFHCqoQZGm3CC6v`
* **測試 HashIV**：`EkRm7iFT261apevs`
* **金流測試端點 (AIO CheckOut)**：
  `https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5`

---

## 🚀 三、 極星生態三大應用場景備忘

1. **生活管家 (LifeButler) LINE 官方帳號點餐 / 生鮮團購自動化**：
   * 串接 LINE Bot 點餐後自動生成綠界結帳連結，消費者完成刷卡或超商代碼付款後，透過 Webhook 背景入帳並通知備貨。
2. **秋季 AI 家教實戰班 (AI Education)**：
   * 提供學員線上刷卡或 ATM 虛擬帳號付費通道，自動產出繳款確認與開立電子收據。
3. **`00-09` 開源點餐系統 (TastyIgniter) B2B 本地化模組**：
   * 作為協助在地餐飲店家架設獨立點餐網站時，內建或選配之台灣在地金流方案。

---

## 📂 四、 關聯檔案與索引
* [🔗 總樞紐資源與網址索引 (00-00_External_Resource_Index.md)](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_External_Resource_Index.md)
* [💻 工程長技術戰術筆記本 (00_Linus_Notebook.md)](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CTO_Linus/00_Linus_Notebook.md)
* [📄 開源點餐系統專案總覽 (00-09-00_Project_Overview.md)](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-09_Project_OpenSource_Ordering/00-09-00_Project_Overview.md)
