# 【極星架構規範】Google Gemini Notebook (NotebookLM) 長效連線與免登入持久化 SOP

> **檔案代號**：`POLARIS-SOP-AI-NOTEBOOKLM-AUTH-v1.0`  
> **建立時間**：2026-10-29  
> **制定負責人**：❄️ 執行長 雪 (CEO Yuki) ✕ 🛠️ 工程長 林納斯 (CTO Linus)  
> **適用範圍**：北極星全體 AI 智能體內閣、創辦人（闆仔）終端設備、00-05 AI 教育工作坊實戰環境

---

## 📌 核心架構摘要 (Executive Summary)

針對 Google Gemini Notebook（原名 NotebookLM）之程式化整合，本規範確立**「本機憑證持久化（Persistent Profile State）」**標準。

透過 Playwright 隔離瀏覽器運行環境將 Google 授權憑證固化於本機沙盒中，**所有 Python 腳本、Antigravity 內閣智能體及 CLI 工具將永久自動繼承該連線狀態，往後開機與執行皆無需再次登入**。

```mermaid
flowchart TD
    User["創辦人 闆仔 (Pinshuo)"] -->|首次登入一次| LoginWindow["Playwright 獨立安全視窗 (login.bat)"]
    LoginWindow -->|導出 37 枚 Session Cookies & Storage| StateFile["本機永久憑證庫<br/>~/.notebooklm/profiles/default/storage_state.json"]
    StateFile -->|自動繼承授權| CLI["NotebookLM CLI 工具 (python -m notebooklm)"]
    StateFile -->|無感背景續期 (Headless Reauth)| ReauthEngine["後台無感刷新引擎<br/>NOTEBOOKLM_HEADLESS_REAUTH=1"]
    CLI -->|原生控制 API| GoogleCloud["Google Gemini Notebook 雲端大腦"]
    GoogleCloud -->|生成交付| Deliverables["20 頁電影級 PPTX / PDF 簡報<br/>JSON 心智圖 (Mind Map)<br/>零幻覺 Grounded 問答"]
```

---

## 🗄️ 1. 憑證實體存儲路徑 (Storage Paths)

所有認證資料皆嚴格存放在本機使用者設定檔目錄，不隨專案目錄移動或 Git 提交而外洩：

| 項目 | 實體絕對路徑 | 說明 |
| :--- | :--- | :--- |
| **持久化憑證總庫** | `C:\Users\lenovo\.notebooklm\profiles\default\storage_state.json` | 儲存 Google 帳號 37+ 枚可用 Cookies、localStorage 與身分標籤 |
| **Playwright 瀏覽器設定檔** | `C:\Users\lenovo\.notebooklm\profiles\default\` | 隔離式 Chromium 使用者環境，保留裝置指紋防止被 Google 判定異地登入 |
| **捷徑啟動批次檔** | `C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\login.bat` | 應急備用重新登入入口 |

---

## 🔄 2. 長效免登入與背景自動續期 (Headless Auto-Refresh)

本環境已內建「無頭後台自動續期（Headless Reauth）」機制。即使長期未使用導致 Session 接近過期，系統亦可在背景自動續約，無需跳出任何視窗打擾使用者。

### 2.1 環境變數配置（建議常駐）
在 Windows PowerShell 或系統環境變數中啟用：
```powershell
[System.Environment]::SetEnvironmentVariable('NOTEBOOKLM_HEADLESS_REAUTH', '1', 'User')
```

### 2.2 健康檢查指令（連線檢驗）
隨時可透過終端執行診斷指令，檢查憑證是否健康：
```powershell
python -m notebooklm doctor
```
*預期回傳：`Auth: ✓ pass | local auth cookies usable (37 cookies)` 與 `Headless Reauth: ✓ pass`。*

### 2.3 在線被動驗證（不消耗 Token、不刷新 Session）
```powershell
python -m notebooklm auth check --test --passive
```

---

## 🚨 3. 應急重連標準作業程序 (Emergency Fallback SOP)

若未來因 Google 全域更換密碼、雙層驗證失效或憑證被手動清除時，請依照下列 3 步極簡復原：

1. **執行登入批次檔**：  
   雙擊點擊 `00-05_AI_Education\login.bat`（或在終端機輸入 `python -m notebooklm login`）。
2. **在自動彈出的 Chromium 視窗登入 Google**：  
   輸入 Google 帳號與密碼完成登入。
3. **確認視窗自動關閉**：  
   登入成功進入 NotebookLM 首頁後，終端機會自動擷取新憑證寫入 `storage_state.json` 並關閉瀏覽器。

---

## 🛠️ 4. 核心指令操作手冊 (Command Reference Cheatsheet)

以下指令均已驗證可直接在任何目錄無縫呼叫：

### 4.1 筆記本管理 (Notebook Operations)
```powershell
# 列出帳號下所有筆記本
python -m notebooklm list

# 建立新筆記本並自動啟用
python -m notebooklm create "專案名稱" --use

# 切換工作筆記本 (支援部分 UUID 匹配)
python -m notebooklm use 347a5c6f

# 查詢當前使用中的筆記本狀態
python -m notebooklm status
```

### 4.2 資料來源管理 (Source Ingestion)
```powershell
# 將講義、PDF 或研究報告加入當前筆記本作為資料源
python -m notebooklm source add "檔案路徑.md"
python -m notebooklm source add "參考資料.pdf"

# 列出當前筆記本的所有資料來源
python -m notebooklm source list
```

### 4.3 零幻覺來源錨定提問 (Grounded Q&A)
```powershell
# 向筆記本提出漏斗式問題 (自動附加 Citation 標籤)
python -m notebooklm ask "請簡述本講義核心架構"
```

### 4.4 Studio 原生產物一鍵生成與下載 (Studio Artifacts)
```powershell
# 1. 生成演講者簡報投影片 (繁體中文)
python -m notebooklm generate slide-deck "課程大綱簡報" --format presenter --language zh_Hant

# 2. 下載最新投影片 (支援 PPTX 與 PDF 雙格式)
python -m notebooklm download slide-deck --format pptx "投影片.pptx" --force
python -m notebooklm download slide-deck --format pdf "投影片.pdf" --force

# 3. 生成結構化心智圖 (note-backed 同步模式)
python -m notebooklm generate mind-map --kind note-backed --language zh_Hant

# 4. 下載心智圖 JSON 節點樹
python -m notebooklm download mind-map "心智圖.json" --force
```

---

## 🏛️ 5. 內閣簽署與登錄 (Cabinet Ratification)

- **審定人**：❄️ 執行長 雪 (CEO Yuki)
- **架構查驗**：🛠️ 工程長 林納斯 (CTO Linus)
- **實測紀錄**：已於 2026-10-29 成功生成第 1 講 20 頁繁中電影級 PPTX/PDF 簡報與完整心智圖，確認 100% 穩定免登入。
