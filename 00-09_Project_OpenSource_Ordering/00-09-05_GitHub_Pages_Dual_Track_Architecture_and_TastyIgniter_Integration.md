# 📘《GitHub 網址雙軌架構解析與 TastyIgniter 零成本前端整合白皮書》 (SSOT v1.0)
## GitHub Pages Dual-Track URL Architecture & TastyIgniter Integration Guide

> **文件編號**：`00-09-05`  
> **領地歸屬**：`00-09_Project_OpenSource_Ordering` (曉專案 · 開源點餐與供應鏈中樞)  
> **主政首長**：CTO 林納斯 (Linus) ✕ 執行長 雪 (Yuki) ✕ 首席前端架構師 尼奧 (Neo) ✕ 首席品質長 戴明 (Dr. Deming)  
> **發布日期**：2026 年 11 月 11 日 · 正式入庫

---

## 🏛️ 一、 戰略背景與核心提問

創辦人（品碩）於 2026-11-10 提出關鍵戰略思維：
> *「在 GitHub 上，一個人可以擁有幾個網址呢？我們是不是可以直接在 GitHub 上部署我們的官網，並結合 Google 雲端跑 TastyIgniter，做到免費又免煩惱網址？」*

本白皮書作為 `00-09` 推進 TastyIgniter 開源點餐系統時的**「前端拓撲與網址分流法定真理來源 (SSOT)」**，徹底解剖 GitHub 的網址資源架構，並設計出將「GitHub 免費靜態分發」與「GCP 免費後端算力」完美咬合的工業級落地方案。

---

## 🌐 二、 GitHub Pages 網址雙軌架構深層解析 (Dual-Track System)

在 GitHub 生態系中，**單一使用者帳號（例如：`chalaw710218`）實質上可以擁有「無限多個」獨立網站與合法 HTTPS 網址**。其運作邏輯由「1 個頂級主站」與「無限個專案分站」構成：

```
                        ┌──────────────────────────────────────────────┐
                        │   GitHub 帳號：chalaw710218 (創辦人個人空間)   │
                        └──────────────────────┬───────────────────────┘
                                               │
             ┌─────────────────────────────────┴─────────────────────────────────┐
             ▼                                                                   ▼
【軌道 A · 唯一的頂級主站 (User Site)】                            【軌道 B · 無限個專案分站 (Project Sites)】
 倉庫命名硬性限制：chalaw710218.github.io                          任何倉庫開啟 Pages，立即獲發一個獨立子網址！
             │                                                                   │
             ▼                                                                   ▼
 https://chalaw710218.github.io/                     https://chalaw710218.github.io/<倉庫名稱>/
 (全域唯一，純根目錄，品牌官方總門面)                               (數量無上限，各業務專案獨立沙盒)
```

### 2.1 軌道 A：頂級使用者主站 (User Site · 唯一門面)
* **硬性命名規則**：倉庫名稱必須 100% 精確命名為 `<username>.github.io`（創辦人即為 `chalaw710218.github.io`）。
* **配額限制**：**全帳號僅能擁有 1 個**。
* **網址外觀**：
  $$\text{https://chalaw710218.github.io/}$$
* **結構優勢**：網址後方**不帶任何斜槓路徑目錄**，具備最高級別的權威感、整潔感與可記憶性。
* **業務定位**：鎖定作為「生活的一部分，就醬點！」**品牌官方總首頁**，承載品牌精神（Bawsa 儀式）、三大核心服務總覽、生活管家理念與官方聯絡管道。

### 2.2 軌道 B：無限專案分站 (Project Sites · 彈性艦隊)
* **建立規則**：創辦人名下的任何現有或新建倉庫（無論公開或 GitHub Pro 私有），只要於 `Settings ➔ Pages` 中啟用發布，該倉庫即刻擁有專屬獨立網址。
* **配額限制**：**物理數量無上限（$\infty$）！** 只要開一個倉庫，就多一個免費網站。
* **網址外觀**：
  $$\text{https://chalaw710218.github.io/}[\text{專案名稱}]/$$
* **生活管家矩陣實戰配置**：
  | 業務專案 | 推薦倉庫名稱 | 完整訪問網址 | 業務職能 |
  | :--- | :--- | :--- | :--- |
  | **品牌官方總門面** | `chalaw710218.github.io` | `https://chalaw710218.github.io/` | 官網總首頁、品牌價值、生活管家介紹 |
  | **代倒垃圾預約系統** | `trash-radar` | `https://chalaw710218.github.io/trash-radar/` | 寶桑外圈包月 (999/1999) 預約與垃圾車即時雷達 |
  | **線上點餐與選單展示** | `tasty-menu` | `https://chalaw710218.github.io/tasty-menu/` | 友店生鮮與餐飲展示前端、對接 TastyIgniter 後端 |
  | **AI 家教班招生網站** | `ai-tutoring` | `https://chalaw710218.github.io/ai-tutoring/` | 4,650 元實戰家教班招生簡章、課綱與報名表單 |
  | **長輩居安照護指南** | `senior-care` | `https://chalaw710218.github.io/senior-care/` | 孝親陪伴、居安修繕說明與家屬諮詢入口 |

### 2.3 軌道 C：未來綁定獨立自訂網域 (Custom Domain Expansion)
若未來極星採購專屬頂級網域名稱（例如：`justclick.tw` 或 `lifebutler.tw`），GitHub Pages 支援全自動免費 SSL 綁定：
* **主根網域**：`www.justclick.tw` ➔ 映射至軌道 A（品牌總官網）。
* **二級子網域（Subdomains，無限切分）**：
  * `order.justclick.tw` ➔ 映射至點餐專案
  * `trash.justclick.tw` ➔ 映射至代倒垃圾專案
  * `ai.justclick.tw` ➔ 映射至 AI 家教班

---

## ⚙️ 三、 GitHub Pages 與 TastyIgniter 整合拓撲 (Architecture Blueprint)

### 3.1 技術本質解構：靜態分發 vs. 動態運算
* **GitHub Pages 的本質**：純靜態託管（Static Site Generation）。專精於 HTML5、CSS3、JavaScript、WebAssembly、向量 SVG 與靜態圖片，背靠微軟全球 Anycast CDN，**不能直接在 GitHub 內部運行 PHP 運算或 MySQL 資料庫**。
* **TastyIgniter 的本質**：基於 PHP 8.4 (Laravel 框架) ＋ MySQL/MariaDB 的全動態電子商務與餐廳排程引擎，需要伺服器環境（Nginx/Apache）處理結帳、排程、購物車 Session 與庫存交易。

### 3.2 創辦人「0 元免網址」終極整合三方案

```
                                ┌──────────────────────────────────────────────┐
                                │   訪客 / 消費者端 (LINE 點擊 / 瀏覽器掃碼)   │
                                └──────────────────────┬───────────────────────┘
                                                       │
                     ┌─────────────────────────────────┴─────────────────────────────────┐
                     ▼                                                                   ▼
       【前端：GitHub Pages 全球靜態 CDN】                                 【後端：Google Cloud 免費雲端算力】
        網址：chalaw710218.github.io/order/                                 網址：*.run.app 或 GCP e2-micro 靜態 IP
        職能：0.3秒秒開、展示菜單、無感交互                               職能：TastyIgniter PHP 8.4、購物車交易、訂單推播
                     │                                                                   │
                     └────────────────────────── JSON API / 訂單送出 ─────────────────────┘
```

#### 方案一：前後端解耦 (Headless / API 輕量化模式 · 最佳體驗)
* **前端 (GitHub Pages)**：
  * 採用尼奧（Neo）設計之純靜態前端（或 Vue/Alpine.js 極簡單頁），加載時間 $< 0.3\text{ 秒}$。
  * 畫面展示商品圖片、價格、分類與生活管家親切文案。
* **後端 (GCP Cloud Run / e2-micro)**：
  * 部署標準 TastyIgniter v4，僅在使用者點擊「確認下單」時，透過 HTTPS Fetch 將購物車 JSON 拋送至 TastyIgniter REST API。
* **優勢**：
  1. 訪客平時看菜單完全不消耗 Google 伺服器運算資源，極致抗高流量。
  2. 即使後端冷啟動，前台頁面依然秒開，使用者體驗評分（Lighthouse）直奔 100 分。

#### 方案二：門面導流與 WebApp 橋接 (Portal & Seamless Bridge · 最快落地)
* **前端 (GitHub Pages)**：
  * 作為品牌官方總入口，呈現特約友店故事、地圖分布與精選菜色。
* **點餐動作**：
  * 按下「開始線上點餐」，無縫深層連結（Deep Link）跳轉至 GCP 託管之 TastyIgniter 原生主題（或嵌入式 iframe/PWA 全螢幕模式）。
* **優勢**：無需額外重寫前端點餐 UI，100% 沿用 TastyIgniter 原生外掛、金流（綠界 ECPay）與出單機驅動。

---

## 🛡️ 四、 戴明安燈出廠與配額安全紅線 (Deming Andon Safeguards)

在啟用 GitHub Pages 部署官網與專案時，必須恪守以下四道安全閘門：

1. **空間防呆線**：
   * 單一倉庫容量建議維持在 **$1\text{ GB}$ 以內**。
   * 高清照片（如生鮮商品照、高解析海報）應先壓縮或託管於外部物件存儲，避免 Git 倉庫膨脹。
2. **流量防護線**：
   * GitHub Pages 每月免費流量軟上限為 **$100\text{ GB}$**。
   * 換算常民生活應用（以單次訪問消耗 2MB 計算），每月可承受約 **$50,000$ 人次** 之高頻造訪，對台東在地營運極度充裕。
3. **商業與個資零洩漏防火牆**：
   * GitHub Pages 發布之分支（如 `main` 或 `gh-pages`）**絕對禁止包含任何 `.env` 檔案、API 金鑰或內部機密代碼**。
   * 官網對外品牌法定全稱強制維持「生活的一部分，就醬點！」與「生活管家」，內部研發代號 100% 隔離。
4. **HTTPS 憑證自動保全**：
   * 啟用 Pages 時，勾選「Enforce HTTPS」，GitHub 將自動透過 Let's Encrypt 頒發並每 90 天自動續期安全憑證，免人工干預。

---

## 📋 五、 執行長雪與技術長林納斯之落地步驟 (Implementation SOP)

當創辦人下達「啟動官網部署」指令時，內閣將依序執行以下四步閉環：

1. **步驟 1：建立專屬主站倉庫**
   * 建立公開倉庫 `chalaw710218.github.io`。
2. **步驟 2：注入尼奧 Gentle UI 前端代碼**
   * 載入 `00-14` CIS 標準色票（`#FAF8F3` 常民生活米白、`#F5A623` 寶桑暖陽黃）與 1.65 倍長輩平權行距。
   * 配置一鍵加入官方 LINE OA 與撥打生活管家專線（0982-828-560）之行動懸浮膠囊。
3. **步驟 3：開啟 GitHub Pages 發布管線**
   * 設定 Source 為 `Deploy from a branch` ➔ 分支 `main` ➔ 目錄 `/ (root)`。
   * 系統將於 60 秒內完成全球 CDN 分發。
4. **步驟 4：對接 00-09 TastyIgniter 點餐後台**
   * 於首頁「點餐專區」配置雙向通道，無縫銜接 GCP 免費後端，實現 0 元營運閉環！

---

*文件存檔路徑：`00-09_Project_OpenSource_Ordering/00-09-05_GitHub_Pages_Dual_Track_Architecture_and_TastyIgniter_Integration.md`*  
*核定簽署：執行長 雪 (Yuki) ✕ CTO 林納斯 (Linus) · 2026-11-11*
