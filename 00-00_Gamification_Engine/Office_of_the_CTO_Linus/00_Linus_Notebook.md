# 💻 工程長 (林納斯 / Linus) 專屬技術戰術筆記本 (CTO Master Notebook)

> **手冊持有者**：工程長兼技術架構師 (CTO) · 林納斯 (Linus)  
> **核心使命**：死守系統穩定性、直擊底層效能瓶頸、極致防呆、掌握開源技術主權。  
> **生效日期**：2026-10-19 ｜ **版本**：v1.0 (The Pragmatic Mastermind)

---

## 🧭 一、 核心系統架構與技術參數速查

### 1. `00-09` TastyIgniter V4 (GCP e2-micro 1GB 終端部署)
* **主機規格**：GCP Free Tier (e2-micro, 2 vCPU, 1GB RAM, 30GB Standard Disk)
* **底層堆疊**：Ubuntu 22.04 LTS + CloudPanel + PHP 8.1 + MySQL 8.0 + Nginx
* **核心記憶體防崩潰機制**：
  * **Swap 分割區**：強制配置 2GB Swap (`/swapfile`)，防止突發高峰觸發 Linux OOM Killer。
  * **Laravel 優化快取**：
    ```bash
    php artisan optimize
    php artisan view:cache
    php artisan config:cache
    php artisan route:cache
    ```
  * **郵件異步/日誌化**：`MAIL_MAILER=log`（徹底消除下單結帳時 SMTP 連線逾時引起的 3 秒轉跳卡頓）。
* **在地化設定**：
  * 幣別：新台幣 (TWD, `NT$`)，小數點位數設定為 `0`。
  * 時區：`Asia/Taipei` (UTC+8)。

### 2. ESC/POS 雲端出單機硬體驅動通訊協議
* **通訊標準**：ESC/POS (Standard Thermal Printer Command Set)
* **網段架構**：雲端 TastyIgniter 後端 -> Webhook / 輪詢代理 -> 本地區域網 (LAN) 出單機 (9100 Port)
* **容錯防呆機制**：
  * **離線緩存隊列**：出單失敗不丟單，寫入 SQLite 本地暫存，等待網路重連自動重試（上限 5 次）。
  * **字型編碼**：強制 UTF-8 轉 Big5 / CP950，避免中文字元亂碼。

### 3. 極星自動化 RPA 腳本庫技術清冊
| 腳本名稱 | 實體路徑 | 驅動方式 | 容錯與資安防線 |
| :--- | :--- | :--- | :--- |
| `calendar_manager.py` | `00-00_Gamification_Engine/` | CLI / Python 3 | 私人 iCal 讀取 + GAS Webhook 寫入，零密碼洩漏 |
| `fb_publisher.py` | `00-02_.../facebook-publisher/` | Graph API v19.0 | 多圖發布原子性，任一圖失敗立即 rollback，自動搶第一留言 |
| `comment_harvester.py` | `00-02_.../facebook-publisher/` | Graph API 輪詢 | 正則匹配 `+1` / 數量，自動去重避免重複記帳 |

---

## 🔬 二、 00-11 逆向工程實驗室本機防線 (Air-Gapped Sandbox)

* **物理環境限制**：嚴格本機離線隔離，禁止上傳任何反編譯代碼或通訊封包至遠端 GitHub。
* **拆解標準作業程序**：
  1. **封包擷取**：Charles / Wireshark 監聽目標協議，導出 HAR 或 pcapng。
  2. **靜態反編譯**：Electron asar 解包、.NET ILSpy 逆向或 APK decompile。
  3. **資料結構還原**：剝離表層 UI，提煉 API Request/Response JSON Schema。
  4. **技術反哺評估**：確認是否可作為極星架構的標準化組件（如開源點餐、車隊派單）。

---

## 🚨 三、 緊急事故排除 SOP (Troubleshooting Protocols)

### 1. 伺服器 OOM (Out of Memory) 假死應急
* **症狀**：網頁載入出現 502 Bad Gateway 或 504 Gateway Timeout，SSH 難以連線。
* **快速重啟命令**：
  ```bash
  sudo systemctl restart php8.1-fpm
  sudo systemctl restart nginx
  sudo systemctl restart mysql
  ```
* **排查根因**：檢視 `/var/log/nginx/error.log` 與 `/var/log/syslog` 是否有 `oom-killer` 殺死進程紀錄。

### 2. 出單機斷線或缺紙異常
* **處置動作**：系統立即將訂單標記為 `UNPRINTED_ALERT`，並發送 LINE Notify 提醒店內人員檢查紙捲。

### 3. Meta Graph API Token 失效
* **處置動作**：檢查 `.secrets.env` 中的 Token 是否過期（正常為 60 天長效 Token），調用 Token Refresh 工具更新。

---

## 📌 四、 林納斯的核心口訣

1. **「不要給我看花俏的投影片，給我看你的資料表欄位定義 (Schema)。」**
2. **「如果這個功能需要使用者讀超過三行說明書，那這個設計就是垃圾。」**
3. **「優化必須基於 Profiling 數據，猜測瓶頸是新手的專利。」**
