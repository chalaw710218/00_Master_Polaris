# 🌐 極星全域外部資源與系統端點總索引 (External Resource & System Index SSOT)

> **主政監督**：執行長 雪 (Yuki, CEO) ✕ CTO 林納斯 (Linus)  
> **更新維護**：每日收工閉環 (Daily Closing SOP) 與重大模組落地時即時同步校準。  
> **單一真理定位**：全域外部資源、API 端點、金鑰設定檔、實體領地與戰略物資的唯一中央索引庫。

---

## 🔑 一、 關鍵外部系統 API 與金鑰端點

| 系統名稱 | 外部系統 / 服務商 | 專案 ID / 標籤 | 設定檔 / 金鑰路徑 | 狀態與通訊健康度 |
| :--- | :--- | :--- | :--- | :--- |
| **Google Cloud Platform** | GCP 服務帳號 (Service Account) | `polaris-lifebutler` (`6237735105`) | `google_service_account.json` | ✅ 正常（讀寫日曆、試算表 100% 暢通） |
| **寶桑物流生活商行帳務** | Google 試算表 (SSOT 真值底座) | `生活管家_系統化管理_V2` | `1srOVCLlOIgS1QIOudMB7AmIiRCLXVREz-08jGiv7udA` | ✅ 正常（10張工作表，現役唯一真實帳務中樞） |
| **Google Business Profile** | GBP 商家檔案 API | `polaris-lifebutler` | 官方申訴立案 `Case ID: 8-2264000041757` | ⏳ 審核中（預估 7~10 個工作天解鎖配額） |
| **Google Calendar** | 私人 Google 日曆雙向管理 | 個人日曆 iCal 密鑰 | `00-00_Gamification_Engine/calendar_manager.py` | ✅ 正常（雙向同步，零帳密外洩） |
| **Meta Facebook API** | 「生活的一部分，就醬點！」粉專 | 粉專 ID `110505444816362` | `00-02_GroupBuy_Products/.agents/skills/facebook-publisher/` | ✅ 正常（支援自動圖文與排程發布） |
| **Facebook 個人託管登入** | 洪一華社團（美食1館、美食2館） | Playwright 持久化 Profile | `~\.gemini\polaris_fb_browser_data` | ✅ 正常（無頭模式反偵測，底價收割就緒） |
| **Meta Threads API** | 生活管家官方 Threads 帳號 | `@chalaw710218` | `00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/` | ✅ 正常（官方發布 + 留言秒回巡邏就緒） |
| **TastyIgniter SaaS** | 開源餐飲點餐主機 (V4) | GCP e2-micro 永久免費執行個體 | `00-09_Project_OpenSource_Ordering/` | ✅ 部署完成（3,980 買斷安裝費） |

---

## 🏛️ 二、 各天王實體主權領地與辦公室索引

| 部門代號 | 主掌幹部 | 領地名稱 | 實體目錄路徑 | 專屬辦公室與戰略筆記本 |
| :--- | :--- | :--- | :--- | :--- |
| **00-00** | **雪 (Yuki)** | 總中樞與遊戲化引擎 | [`00-00_Gamification_Engine/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/) | [`Office_of_the_CEO_Yuki`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CEO_Yuki/) ｜ [`00_CEO_Notebook.md`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CEO_Yuki/00_CEO_Notebook.md) |
| **00-01** | **車隊隊長** | 物流與車隊交付 | [`00-01_Logistics_System/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-01_Logistics_System/) | 寶桑物流商行、外送專法戰略解耦 3PL 車隊 |
| **00-02** | **算盤 (Abacus)** | 團購與供應鏈選品 | [`00-02_GroupBuy_Products/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-02_GroupBuy_Products/) | [`Office_of_the_CFO_Abacus`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CFO_Abacus/) ｜ [`00_Abacus_Notebook.md`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CFO_Abacus/00_Abacus_Notebook.md) |
| **00-03** | **泰勒絲 / 影** | 品牌與生活管家 | [`00-03_Brand_LifeButler/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-03_Brand_LifeButler/) | [`Office_of_the_CMO_Taylor`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CMO_Taylor/) ｜ [`00_Taylor_Notebook.md`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CMO_Taylor/00_Taylor_Notebook.md) |
| **00-04** | **品碩 (Boss)** | 個人成長與經理人 | [`00-04_Personal_Growth/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-04_Personal_Growth/) | 社區專業經理人認證、越式美食顧問復盤案 |
| **00-05** | **雪 / 林納斯** | AI 教育與架構輸出 | [`00-05_AI_Education/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-05_AI_Education/) | 極星 AI 課後實戰班講義庫（01至08篇） |
| **00-07** | **獵鷹 (Falcon)** | TWQR 金流推廣 | [`00-07_TWQR_Promotion/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-07_TWQR_Promotion/) | [`Office_of_the_CIO_Falcon`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CIO_Falcon/) ｜ [`00_Falcon_Notebook.md`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CIO_Falcon/00_Falcon_Notebook.md) |
| **00-08** | **社區幹事** | 社區據點與公積金 | [`00-08_Community_Management/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-08_Community_Management/) | 家宅社區據點運作、公積金帳本 |
| **00-09** | **林納斯 (Linus)** | 開源點餐系統 SaaS | [`00-09_Project_OpenSource_Ordering/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-09_Project_OpenSource_Ordering/) | [`Office_of_the_CTO_Linus`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CTO_Linus/) ｜ [`00_Linus_Notebook.md`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CTO_Linus/00_Linus_Notebook.md) |
| **00-10** | **娟娟 / 雪** | 新住民培力與多元共融 | [`00-10_New_Immigrant_Empowerment/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-10_New_Immigrant_Empowerment/) | 文化教室、舒肥與清潔 SOP、時間銀行 |
| **00-11** | **林納斯 (Linus)** | 逆向工程實驗室 | [`00-11_Reverse_Engineering_Lab/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-11_Reverse_Engineering_Lab/) | 本機離線隔離研發、專案拆解台 |
| **00-13** | **渡鴉 (Raven)** | 網路穿透與商業徵信處 | [`00-13_Cyber_Forensics_and_Investigation/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-13_Cyber_Forensics_and_Investigation/) | [`Office_of_the_Forensic_Raven`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_Forensic_Raven/) ｜ [`00_Raven_Notebook.md`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_Forensic_Raven/00_Raven_Notebook.md) |
| **00-14** | **約瑟夫 (Josef)** | 視覺設計與海報工坊處 | [`00-14_Visual_Design_and_Poster_Craft/`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-14_Visual_Design_and_Poster_Craft/) | [`Office_of_the_CVO_Josef`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CVO_Josef/) ｜ [`00_Josef_Notebook.md`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CVO_Josef/00_Josef_Notebook.md) |

---

## 🛠️ 三、 核心操作型武器庫與實體腳本索引

| 技能代碼 | 幹部 | 功能與武器描述 | 實體執行代碼路徑 |
| :--- | :--- | :--- | :--- |
| **`bionic-cognition-compiler`** | 雪 / 林納斯 / 戴明 | 認知存摺自動編譯器 (全息掃描/防呆SOP編譯/社群選題編譯) | `.agents/skills/bionic-cognition-compiler/scripts/cognition_compiler_cli.py` |
| **`lifebutler-care-artisan`** | 雪 / 算盤 / 戴明 / 約瑟夫 | 孝親安居與高齡溫暖服務封裝器 (防滑熱像/陪診圖卡/尊嚴修容/回憶錄) | `.agents/skills/lifebutler-care-artisan/scripts/care_artisan_cli.py` |
| **`polaris-poster-artisan`** | 約瑟夫 | 萬用實體與社群海報即時造物機 (300 DPI / 戴明安燈 100分) | `00-14_Visual_Design_and_Poster_Craft/scripts/poster_artisan_cli.py` |
| **`polaris-forensic-investigator`**| 渡鴉 | 黑色商業調查與反欺詐穿透 CLI (裁判書全文/身分證校驗) | `00-13_Cyber_Forensics_and_Investigation/scripts/polaris_forensic_cli.py` |
| **`polaris-5d-pricing-engine`** | 算盤 | 5D 價值精算時間矩陣引擎 (D1~D5 轉化 TP 點數) | `00-00_Gamification_Engine/polaris_5d_pricing_engine.py` |
| **`threads-autonomous-walker`** | 影 | Threads 社交自律漫遊六部曲 (看家門/訪鄰居/散步/筆記/首回/戰報) | `00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/execute_autonomous_walk_v3.py` |
| **`facebook-publisher`** | 泰勒絲 | 官方 Facebook 粉專圖文排程自動發射台 | `00-02_GroupBuy_Products/.agents/skills/facebook-publisher/fb_publisher.py` |
| **`polaris-motion-reels`** | 林納斯 | 9:16 Ken Burns 緩動短影音微動態合成管線 | Python + FFmpeg 自動化轉譯 |
| **`daily-closing-sop`** | 雪 | 每日營運收工閉環標準作業程序 (資安脫敏/RPG結算/Git推送) | `.agents/skills/daily-closing-sop/SKILL.md` |
| **`polaris-flywheel-orchestrator`** | 雪 | 全域飛輪總控調度引擎 (九天王路由/品牌防火牆/一鍵審批) | `00-00_Gamification_Engine/polaris_flywheel_orchestrator.py` |
