---
name: google-colab-commander
description: ⚡ 極星 Google Colab 雲端 GPU 算力指揮官協議 (Google Colab Pro GPU Commander Protocol v1.0)。由 CTO 林納斯 (Linus) 確定性代碼主政、首席科技偵察官艾達 (Ada) 算力調度、首席視覺長約瑟夫 (Josef) 圖像生圖協同。專門透過 Google 官方開源之 Colab MCP (Model Context Protocol) 伺服器，直接接管創辦人的 Google Colab Pro 雲端環境（T4 / A100 / L4 頂級 GPU）。讓代理人能夠在雲端全自動建立執行階段、安裝依賴（!pip install）、遠端執行 Python 運算、以及調用 ComfyUI / Flux 高清生圖，實現「本地 0 負擔、雲端免費頂級算力」之閉環。
---

# ⚡ 極星 Google Colab 雲端 GPU 算力指揮官協議 (Google Colab Commander)

> **領地歸屬**：`00-00_Gamification_Engine/Office_of_the_CTO_Linus` ✕ `Office_of_the_Scout_Ada`  
> **法定效力**：本協議為極星宇宙調用 Google 雲端 GPU 算力之標準作業程序 (SSOT)。  
> **核心使命**：**榨乾科技巨頭贈送的每一分 GPU 算力！本地 0 負擔，雲端跑大圖！**

---

## 🏛️ 一、 核心架構與連接機制 (MCP Bridge)

本協議透過 Google 官方 Model Context Protocol (`googlecolab/colab-mcp`) 與創辦人的 Google Colab Pro 建立直連：

```
                    ┌──────────────────────────────────────────────┐
                    │    創辦人自然語言指令（例：「幫我生一張喵編」）   │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │       極星內閣代理人 (Antigravity)            │
                    │       (Yuki / Linus / Josef / Ada)           │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           │ (MCP JSON-RPC / Stdio)
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │      Colab MCP 伺服器 (googlecolab/colab-mcp) │
                    │      路徑：~/.local/bin/uvx.exe              │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           │ (Google OAuth 2.0 / HTTPS)
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │    Google Colab Pro 雲端運算環境 (GPU Pod)    │
                    │    • 頂級顯卡：NVIDIA T4 / A100 / L4        │
                    │    • 任務執行：ComfyUI / Flux 生圖 / 深度運算 │
                    └──────────────────────────────────────────────┘
```

---

## ⚙️ 二、 全域配置設定 (SSOT Config)

### 2.1 全域 MCP 設定檔 (`~/.gemini/config/mcp_config.json`)
```json
{
  "mcpServers": {
    "colab": {
      "command": "C:\\Users\\lenovo\\.local\\bin\\uvx.exe",
      "args": [
        "git+https://github.com/googlecolab/colab-mcp"
      ],
      "timeout": 60000
    }
  }
}
```

### 2.2 首次認證標準授權流程 (First-Time Auth)
1. 當代理人首次調用 `colab` MCP 工具時，系統將呼叫預設瀏覽器開啟 Google 授權視窗。
2. 創辦人確認選取具備 **「Colab Pro」** 權限之 Google 帳號。
3. 點擊「允許 (Allow)」後，授權憑證將自動保存在本地 `~/.colab-mcp-auth-token.json`，後續所有會話皆享有永久免登入自動連線。

---

## 🛠️ 三、 核心作戰應用場景

### 場景 1：【ComfyUI ✕ Flux 慢工出細活高清生圖】
* **痛點**：創辦人本地電腦缺乏頂級獨立顯卡，生圖卡頓、幾何死板。
* **解法**：
  1. 艾達與林納斯透過 Colab MCP 於雲端啟動 GPU 執行個體。
  2. 遠端部署輕量 ComfyUI 核心與 Flux 模型權重。
  3. 約瑟夫注入專屬提示詞（「條紋虎斑喵編騎復古小綿羊、懷抱大鮮魚、35mm 街拍電影質感」）。
  4. Google 雲端 GPU 於 15 秒內渲染完成，成品自動下載至本地 `00-14` 或 `00-03` 目錄。

### 場景 2：【在地巨量數據與路線最佳化計算】
* **痛點**：垃圾雷達 300+ 站點與全台東市路線模擬計算耗費本地 CPU。
* **解法**：將 Python 模擬演算法直接拋給 Colab 雲端跑批次矩陣計算，計算完畢直接回傳結果 JSON。

---

## 🛡️ 四、 戴明安燈出廠與配額保護 (Deming Andon Gate)

1. **算力點數監測**：每次調用前確認 Colab Pro 運算單元（CU）狀態，禁止無意義空轉。
2. **自動斷線省點數**：任務執行完畢後，強制通知或釋放 GPU 核心，避免忘記關閉造成點數浪費。
3. **資安脫敏**：上傳至 Colab 執行的代碼與數據，嚴格禁止包含個人私密密碼與未授權 Token。
