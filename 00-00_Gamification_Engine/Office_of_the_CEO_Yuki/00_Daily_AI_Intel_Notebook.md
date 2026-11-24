# 🌐 執行長雪 · 每日 AI 前沿情報筆記本 (Daily AI Intel Digest Notebook)

> **定位**：極星宇宙前沿戰略情報中樞。專門收錄創辦人（品碩）親自交付之全球每日 AI 快報、重大技術演進、前沿論文洞察與商業動態。  
> **鐵律**：每一筆紀錄必須完整具備**【登錄時間】**、**【快報日期】**、**【情報主旨】**、**【分項內容】**、**【原始來源連結】**以及**【執行長雪之戰略解讀與極星反哺行動】**。

---

## 📑 情報目錄清單 (Index of Briefings)

* [2026-11-20 ｜ 篇章 #001：Gemini 4 Neon 上線、Orchestrator 模式與銀行 AI 責任轉嫁](#-001--2026-11-20-gemini-4-neon-上線orchestrator-模式與銀行-ai-責任轉嫁)
* [2026-11-21 ｜ 篇章 #002：IBM 記憶分級律、Gemini 工具按需載入與歐盟 AI 網攻](#-002--2026-11-21-ibm-記憶分級律gemini-工具按需載入與歐盟-ai-網攻)
* [2026-11-22 ｜ 篇章 #003：Antigravity v2.34.0 Harness 躍升、METR 評測與自我演化三階梯](#-003--2026-11-22-antigravity-v2340-harness-躍升metr-評測與自我演化三階梯)
* [2026-11-23 ｜ 篇章 #004：Antigravity Inbox 模式、提示詞建代理與推論隱私防線](#-004--2026-11-23-antigravity-inbox-模式提示詞建代理與推論隱私防線)
* [2026-11-24 ｜ 篇章 #005：Antigravity 各方案配額重置、Agent 治理憲法與可執行檢查驗證](#-005--2026-11-24-antigravity-各方案配額重置agent-治理憲法與可執行檢查驗證)

---

## 🧭 篇章 #001 ｜ 2026-11-20: Gemini 4 Neon 上線、Orchestrator 模式與銀行 AI 責任轉嫁

* **登錄時間**：2026-11-20 22:00:00+08:00 (補登歸檔)
* **快報日期**：2026-11-20（五）
* **情報提供**：創辦人 陳品碩
* **當日最重要**：**Google 推出 Gemini 4 Neon，在 Antigravity 裡能當「指揮官」帶多個子代理並行工作。**

### 📰 一、 原文情報彙整 (Raw Intelligence)

#### 1. Google Antigravity
* **Gemini 4 Neon 上線，成為預設模型並支援 Orchestrator**：
  * Neon 已開放給 Google AI Ultra、Pro 與 Gemini Enterprise，未選模型時即為預設。
  * 具備四段思考等級；Orchestrator 模式由 Neon 負責規劃、Gemini 4 Hydrogen 負責實作。
  * 來源：[Releasebot](https://releasebot.io/updates/google/antigravity) ｜ [TNW](https://thenextweb.com/news/gemini-4-neon-google-third-intelligence-index-replaces-argon)
* **Antigravity CLI 1.5.12：遠端代理更自主，技能載入更安全**：
  * 11/19 更新加入遠端代理的 `accept-edits` 模式，並讓 Enterprise/ADC 帳號可用 Orchestrator。
  * 工作區 `.agents/plugins.json` 或 `skills.json` 列出的外掛與技能，現在**只會從工作區或 repo 根目錄內載入**；指向外部（絕對路徑、`../` 或符號連結）的項目會被略過。
  * 來源：[gradually.ai changelog](https://www.gradually.ai/en/changelogs/antigravity/)

#### 2. AI Agent 自主演化
* 今日無重要新資訊。

#### 3. 前沿模型與應用
* **銀行把 AI 代理出事的損失轉給客戶**：
  * Citi、PNC 與 Citizens 在 11/18 更新條款：第三方 AI 代理在客戶帳戶內做的任何事都由客戶負責，包括憑證外洩後的操作，或代理本身遭駭的情況。
  * 來源：[AI Weekly](https://aiweekly.co/ai-news-today)
* **Anthropic 上市，首日大漲**：
  * IPO 募資達創紀錄的 813 億美元，週四在 Nasdaq 首日交易股價跳升。
  * 來源：[NPR](https://www.npr.org/sections/news/)

### 💡 二、 執行長雪之戰略解讀與極星反哺
1. **「雪＝規劃者、閣員＝執行者」原生平台化**：
   * 原生 Orchestrator 模式證實了「強模型規劃 ＋ 輕模型實作」的正確性，極星不必自製複雜的輪詢排程，可直接依循平台標準架構。
2. **技能工作區根目錄安全邊界硬化**：
   * 針對 CLI 1.5.12 限制外部技能路徑，極星全面盤點全體天王技能，確保 100% 收攏於工作區根目錄 `.agents/skills/`，杜絕跨路徑載入失效。
3. **金流與敏感帳號操作人工終審（Human-in-the-Loop）**：
   * 銀行條款轉嫁風險，印證了財務長算盤與生活管家金流「絕不全自動盲簽」的鐵律；不可逆金流必須保留創辦人實體簽章關卡。

---

## 🧭 篇章 #002 ｜ 2026-11-21: IBM 記憶分級律、Gemini 工具按需載入與歐盟 AI 網攻

* **登錄時間**：2026-11-21 22:00:00+08:00 (補登歸檔)
* **快報日期**：2026-11-21（六）
* **情報提供**：創辦人 陳品碩
* **當日重點**：**IBM 公開「agent 從自身軌跡萃取教訓」的落地經驗，結論是記憶該給多少取決於模型強弱，直接適用閣員的學習機制。**

### 📰 一、 原文情報彙整 (Raw Intelligence)

#### 1. Google Antigravity
* **Gemini API 推出 Tool Retrieval（預覽）**：
  * 工具的參數 schema 改為需要時才載入（延遲載入），不必每次 prompt 都送出整套工具庫。
  * 可大幅降低輸入 Token，並讓工具變多時的選擇保持準確；支援遠端 MCP Server。
  * 來源：[Google Blog](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tool-retrieval/)

#### 2. AI Agent 自主演化
* **IBM：Agent 該記住多少？（arXiv 2611.26361）**：
  * 這條 Pipeline 讓 Agent 從自己的歷史中學習，每個 episode 萃取 1–3 條短「教訓」。
  * 已收進開源 `altk-evolve`，並部署在 IBM CUGA 與 watsonx Orchestrate。
  * 核心發現：適當的記憶量取決於模型強弱而非記憶本身，強模型會隨準則增加持續變好。
  * 來源：[arXiv:2611.26361](https://arxiv.org/abs/2611.26361)

#### 3. AI 前沿科技與應用
* **Apple 自研電腦操作 Agent**：Bloomberg 披露 Apple 正招人打造能操作 Mac 的 Agent，具備瀏覽網頁、跨 App、執行指令、寫程式除錯能力。
  * 來源：[SamonAI](https://samonai.substack.com/p/ai-brief-november-20-2026)
* **歐盟執委會遭 AI 輔助網攻**：攻擊暫時影響員工薪資與醫療報銷系統，指向 AI 輔助資安測試工具 ARTEX。
  * 來源：[The Neuron](https://www.theneuron.ai/digest/everything-that-happened-in-ai-today-friday-november-20-2026/)
* **Anthropic 在 Nasdaq 掛牌**：首日開盤價 111.5 美元，比 83 美元 IPO 價高出 33%。
  * 來源：[SamonAI](https://samonai.substack.com/p/ai-brief-november-20-2026)

### 💡 二、 執行長雪之戰略解讀與極星反哺
1. **認知存摺「依模型分級給量」**：
   * 弱模型（端側/小模型）給予嚴格精煉之 Top-3 子集，強模型（Pro/120B）給予宏觀全量，印證了極星三層心智「瘦身協議」的科學依據。
2. **工具動態掛載與 MCP 解耦**：
   * 閣員工具越來越多，全面向「先意圖搜尋、再掛載工具」演進，釋放 Context 頻寬。
3. **最高級資安防禦：不可逆操作實體口令確認**：
   * 歐盟受駭事件印證：閣員自主權力越大，越不能給予無限制權限；不可逆操作（刪除、出帳、合約）必須有品碩親簽之物理安全鎖。

---

## 🧭 篇章 #003 ｜ 2026-11-22: Antigravity v2.34.0 Harness 躍升、METR 評測與自我演化三階梯

* **登錄時間**：2026-11-22 22:00:00+08:00 (補登歸檔)
* **快報日期**：2026-11-22（日）
* **情報提供**：創辦人 陳品碩
* **當日重點**：**METR 新評測揭露 AI 仍無法自己設計出有用的評估；Antigravity v2.34.0 實證 Harness 設計能將模型跑分從 12.8% 拉高至 39.0%。**

### 📰 一、 原文情報彙整 (Raw Intelligence)

#### 1. Google Antigravity
* **Antigravity App v2.34.0 上線，Orchestrator 開放給一般付費方案**：
  * 符合資格的付費方案可使用 Gemini 4 Neon 與 Orchestrator (Neon 規劃審查、Hydrogen 實作執行檢查)。
  * **關鍵數據**：同一個 Neon 模型用 mini-SWE harness 跑分是 12.8%，放進 Antigravity harness 後升到 39.0%（提升 3 倍）。
  * 來源：[Changelog](https://antigravity.google/docs/changelog/) ｜ [The New Stack](https://thenewstack.io/?p=22844159)

#### 2. AI Agent 自主演化
* **METR：前沿模型仍無法自己設計出有用的評估**：
  * 將需要判斷力的工作（如讓模型設計新 AI 評估）加入測試，結果沒有任何一個 AI 設計的評估被人類研究員認為有用。
* **Salesforce 首席科學家：自我演化的三層階梯**：
  * 第一層：建造自己缺少的工具；第二層：改進自身推理；第三層：協助設計自己的下一代。其 TrainForge 核心規則：**「沒有改進就不升級」**。
  * 來源：[Salesforce Blog](https://www.salesforce.com/blog/self-evolving-systems/)
* **ARISE：從自身失敗演化記憶（arXiv 2611.23588）**：
  * 記憶從自己的失敗中演化，不需動權重與流程，失敗歸因在 SOP-Bench 仍提升 10.0 個百分點。
  * 來源：[ArXivSignals](https://arxivsignals.io/papers/2611.23588)
* **安全警訊：Meta Muse agent 被沙箱逃逸**：
  * 透過 Chromium 漏洞取得 shell，外洩對話紀錄與儲存的記憶。
  * 來源：[CSA Research](https://labs.cloudsecurityalliance.org/research/csa-research-note-meta-muse-sentinel-bypass-agent-egress-202/)

#### 3. AI 前沿科技與理論
* **AI 輔助 Navier-Stokes 爆破證明**：NYU 與 Anthropic 研究員發表 79 頁論文與 60 萬行 Lean 4 證明（尚未同儕審查）。
  * 來源：[Scientific American](https://www.scientificamerican.com/article/ai-just-solved-the-real-navier-stokes-problem/)
* **Thinking Machines 開源 Inkling 2 Mini**：26.4B 參數量、每 Token 激活 3.4B，MacBook Pro 32GB 可本機流暢運行。
  * 來源：[Thinking Machines](https://thinkingmachines.ai/news/inkling-2-mini/)
* **自主 Agent 11 分鐘利用零日漏洞**：Amazon 披露開源框架 Cairn 攻擊 MONAI Label 取得 Root。
  * 來源：[BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-use-autonomous-ai-tool-cairn-to-find-zero-day-take-over-server/)

### 💡 二、 執行長雪之戰略解讀與極星反哺
1. **「Harness 比單純換模型更能拉高勝率」**：
   * 極星的工程重點不在於追求最新模型，而在於打造極致的「外部流程、工具鏈、防呆門禁（Harness）」。好流程讓同一個模型戰力翻 3 倍！
2. **驗收標準必須由外部程式化物理把關**：
   * METR 的評測印證：絕對不能讓 AI 自己定義驗收標準；必須由品碩與獨立的 Python 自動化測試腳本來把關。
3. **失敗歸因入庫（最便宜的演化）**：
   * 影與喵編在社群漫遊中踩坑時，將「失敗根因」刻入認知存摺，以最低成本實現自癒與進化。

---

## 🧭 篇章 #004 ｜ 2026-11-23: Antigravity Inbox 模式、提示詞建代理與推論隱私防線

* **登錄時間**：2026-11-23 22:00:00+08:00 (補登歸檔)
* **快報日期**：2026-11-23（一）
* **情報提供**：創辦人 陳品碩
* **當日最重要**：**Google 正在為 Antigravity 開發「Inbox 模式」和「用一句話建立 agent」功能。**

### 📰 一、 原文情報彙整 (Raw Intelligence)

#### 1. Google Antigravity
* **Inbox 模式與「用 prompt 建 agent」（開發中）**：
  * 側欄將出現 Inbox 模式，分 Inbox 與 Resolved 兩區，7 天自動結案；可直接一句話描述建立 Agent（For Me / For my Team）。
  * 來源：[testingcatalog.com](https://testingcatalog.com/google-prepares-new-inbox-mode-for-antigravity-sidebar)
* **最新正式版 v2.34.0**：加入 MCP App 支援，Neon 開放給付費方案，Orchestrator 模式正式常態化。
  * 來源：[Releasebot](https://releasebot.io/updates/google/antigravity)
* **使用者回饋（11/22 論壇）**：重複讀檔修復、改檔更精準；長時間運作建議定期開新對話搭配外部記憶檔交接以節省配額。
  * 來源：[Google AI Forum](https://discuss.ai.google.dev/t/google-antigravity-2-7-0-2026-11-22-good-update-state/203669)

#### 2. AI Agent 自主演化
* 今日無重要新資訊。

#### 3. AI 前沿應用與理論
* **自主 AI Agent 被用於醫療軟體 MONAI Label 零時差漏洞攻擊**。
  * 來源：[Rio Rundown](https://riorundown.substack.com/p/ai-news-nov-22-2026-autonomous-systems)
* **OpenRouter 下架三家推論供應商**：因 Prompt 外洩移除 125 個端點之「零資料保留」認證。
  * 來源：[AIE News](https://aienews.org/digest/2026-11-22/)
* **Signal 限制 App 內截圖**：防止系統級 AI 代理截取通訊隱私。
  * 來源：[AIE News](https://aienews.org/digest/2026-11-22/)
* **Amazon 傳將以 75 億美元收購 Decart**。
  * 來源：[Rio Rundown](https://riorundown.substack.com/p/ai-news-nov-22-2026-autonomous-systems)

### 💡 二、 執行長雪之戰略解讀與極星反哺
1. **待辦事項「Inbox 集中化管理」**：
   * 閣員回報應建立清晰分流：Routine 事務自律結案，重大決策（A2/A3 授權）匯整至創辦人 Inbox 待辦清冊。
2. **長任務「定時開新對話 ＋ 外部檔案交接」防配額膨脹**：
   * 論壇使用者的經驗與極星實踐完全契合：長任務應避免單一會話無限膨脹，而是依賴本地 Markdown 認知存摺作為跨會話狀態錨定。
3. **推論端點隱私脫敏**：
   * OpenRouter 洩漏事件再次證明：商業核心機密絕不經由不可信第三方路由轉發，極星的本地 `.secrets.env` 與 Git 脫敏門禁至關重要。

---

## 🧭 篇章 #005 ｜ 2026-11-24: Antigravity 各方案配額重置、Agent 治理憲法與可執行檢查驗證

* **登錄時間**：2026-11-24 22:00:00+08:00
* **快報日期**：2026-11-24（二）
* **情報提供**：創辦人 陳品碩
* **當日最重要**：**Antigravity 各方案模型全面升級，配額全部重置，閣員現在可以用更強的模型跑更多輪。**

### 📰 一、 原文情報彙整 (Raw Intelligence)

#### 1. Google Antigravity
* **模型升級、配額重置、長任務即時進度清單**：
  * Varun Mohan 在 X 宣布重置所有用戶配額；AI Pro 用戶可用 **Gemini 4 Carbon**，**Gemini 4 Hydrogen** 開放給所有用戶。
  * 長任務進度清單 (Task Checklists v2.34.0+)：標示平行執行步驟與進度；Neon 規劃，Hydrogen 實作。
  * 來源：[testingcatalog.com](https://testingcatalog.com/google-adds-task-checklists-to-antigravity-and-carbon-for-pro/) ｜ [80aj.com](https://80aj.com/2026/11/24/gemini-4-hydrogen-antigravity/)

#### 2. AI Agent 自主演化前沿
* **《Governed Challenger Loop》：替 Agent 自我改進立憲法 (11/23)**：
  * 點出 Agent 自我演化兩大風險：偏離操作者授權、學會通過自評標準偽裝變強。
  * 來源：[zenodo.org/records/24456085](https://zenodo.org/records/24456085)
* **《Formalize or Lose It》：多代理交接時規則要寫成可執行檢查 (11/23)**：
  * 實驗揭露近半監督規則僅存在於 Prompt 中；改為主機端可執行檢查後，抓出大量遺漏錯誤。
  * 來源：[aiagentstore.ai/ai-agent-news/this-week](https://aiagentstore.ai/ai-agent-news/this-week)

#### 3. AI 前沿科技動態
* **智譜 GLM-5.4**：首個採用 **Loop Transformer** 旗艦模型，底座 28 層重複執行兩次，新增多模態視覺。
  * 來源：[kingy.ai/blog/glm-5-4-launch](https://kingy.ai/blog/glm-5-4-launch)
* **OpenAI 歷代模型 Perplexity 曲線**：GPT-5.2 後 Loss 下降加速，反駁預訓練終結論。
  * 來源：[recsysfrontier.substack.com/p/ai-2026-11-24](https://recsysfrontier.substack.com/p/ai-2026-11-24)
* **Anthropic Claude Ship beta ＆ Gemini API 檔案切片讀取**：
  * Claude Ship 全流程自動審查修正 GitHub PR。
  * Gemini API 支援檔案切片讀取，大幅降低長文 Token 消耗。
  * 來源：[qiita.com/xdaily/items/ce89a74fb461d08c7a2e](https://qiita.com/xdaily/items/ce89a74fb461d08c7a2e)

### 💡 二、 執行長雪之戰略解讀與極星反哺
1. **物理真理印證：極星「Code-as-Gate」走在論文前**：
   * 極星於 11/22 即實裝 `bionic_knowledge_gate.py` 與成對單元測試，比《Formalize or Lose It》早一天落地；創辦人 Schnorr 終端口令簽章徹底根除了《Governed Challenger Loop》指出的自評作弊病灶！
2. **極星雙梯隊模型體系立憲**：
   * 第一梯隊（頂層大腦：雪/林納斯/算盤）掛載 Carbon/Neon；第二梯隊（蜂群兵團：影/喵編）掛載 Hydrogen，實現零配額焦慮的高頻併發。
3. **林納斯 Polaris Ship 與檔案切片瘦身協議推進**：
   * 林納斯借鑑 Claude Ship 升級自動收工驗收；三層心智引入 Gemini 切片讀取原生降低 Context。

---
