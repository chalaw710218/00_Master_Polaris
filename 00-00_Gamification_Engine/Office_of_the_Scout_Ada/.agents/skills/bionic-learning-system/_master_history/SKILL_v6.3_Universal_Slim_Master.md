---
name: bionic-learning-system
description: 北極星萬用仿生自進化系統母版 (Bionic Learning System v6.3 萬用解耦與模組化精簡旗艦母版)。100% 角色無關（Role-Agnostic）之底層自進化引擎，將規則狀態機、零信任真值驗算、先讀後寫強制閘門、去時間戳輪次帳本與程式化十輪衝突審計寫死於 bionic_core/；個性化與進化方向統一由各閣員特化子版與 Adapter 獨立定義。採用 Core + references/ 按需載入架構，核心規範精簡至 4KB 以內，確保最高遵守度。
is_master: true
lock_status: IMMUTABLE_GOLDEN_MASTER (董事長親定不可覆寫萬用母版；2026-11-15 升級至 v6.3 萬用解耦精簡版，舊版完整保留於 _master_history/)
authorized_by: 陳品碩 (陳先生 / 品碩 / 董事長)
version: v6.3-MASTER
---

# 🧬 北極星萬用仿生自進化系統母版 (Universal Bionic Learning Master v6.3)

> ⚡ **【第一章｜憲法級總綱 · 萬用底座與特化分離】**
> 1. **文字不等於進化，宣稱必須有物理憑證**：任何「學習／驗證／審計／轉正」，若無 `bionic_core/` 對應之可執行腳本 Exit Code 0 與雜湊鏈帳本紀錄，一律視為**未發生**。
> 2. **自進化的唯一判準是「先讀後寫」**：下一次產出行為是否被已轉正（`active`）的規則約束改變；只寫日記、不進閘門者，不得自稱自進化。
> 3. **自進化對象為「規則、技能、設定、程式」，非模型權重**：嚴禁誇大為模型重新訓練。
> 4. **母版萬用寫死 ✕ 子版專長特化（Role-Agnostic Kernel, Role-Specific Adapters）**：
>    - **母版 (`bionic-learning-system` + `bionic_core/`)**：100% 角色無關，僅將**通用規則狀態機、數學驗算模型、安全閘門、熔斷器與十輪審計程式寫死**，嚴禁在母版程式碼寫死任何單一閣員代號或特定業務邏輯。
>    - **子版 (`bionic-learning-{role}` + 子版 Adapter)**：負責定義該閣員的人格屬性、專業方向、真值資料集與候選規則提名邏輯，並於 `bionic_core/verifier_registry.json` 註冊掛載。

---

## 🔄 第二章｜七段萬用自進化閉環協定 (7-Stage Universal Closed-Loop)

所有閣員子版執行自進化，強制經由 `bionic_core/` 以下七段確定性管線運作：

```
① 觸發 (Trigger) ➔ ② 感知 (Perceive) ➔ ③ 提名 (Propose) ➔ ④ 驗算 (Evaluate)
                                                              │
⑦ 審計/淘汰 (Audit & Sweep) ◀── ⑥ 強制 (Enforce Gate) ◀── ⑤ 轉正 (Promote)
```

| 階段 | 核心腳本 (`bionic_core/`) | 萬用強制規範（寫死不可繞過） |
| :--- | :--- | :--- |
| **① 觸發** | `run_evolution_cycle.py --office <role>` | 由董事長指令或核准排程觸發；自動根據 `verifier_registry.json` 載入該角色之 `adapter_script`。 |
| **② 感知** | `perceive_web.py` | 嚴格網域邊界分級（A/B/C/D，轉址後二次校驗）；遵守 `robots.txt`；磁碟持久化三態熔斷；剝離提示注入行；D 級來源禁入規則。 |
| **③ 提名** | `rule_store.py propose` | 學習結論必須蒸餾為結構化 `candidate` 規則（8 大萬用型態：`forbid_phrase`, `prefer_phrase`, `max_count`, `regex_forbid`, `metric_min`, `metric_max`, `baseline_standard`, `route`）。 |
| **④ 驗算** | `rule_store.py evaluate` | **嚴禁人工手填指標**！由程式直接讀取 `verifier_registry.json` 登記之真實資料集並簽章 `dataset_sha256`：<br>• **文字成效規則**：強制執行時序留出驗證（Holdout Split）＋高成效樣本誤傷率掃描（誤傷 `>35%` 立即攔截）。<br>• **數值門檻規則**：真實達標率或缺陷數嚴格比對（廢除 `wo_mean=0.0` 假通過）。<br>• **合規基準 (`baseline_standard`)**：綁定憲法級固定標準，不偽裝為 A/B 實驗。<br>• **派工路由 (`route`)**：讀取 `dispatch.py` 帳本統計經董事長簽收之一次通過率。 |
| **⑤ 轉正** | `rule_store.py promote` | 須通過 `trial_ok`（`N >= 3` 且優於對照、Holdout 通過、誤傷率達標）；**高風險 (`risk="high"`) 規則強制要求 `--founder-approved`**。`fold()` 於折疊時強制二次重驗，手動塞入假 `promote` 直接打入 `tampered_rejected`。 |
| **⑥ 強制** | `enforce.py gate` | **先讀後寫（Fail-Closed）**：各子版產出前必須載入 `active` 規則（`enforce.py constraints`），產出後通過 `enforce.py gate`（違規或停機鎖未解即 `Exit Code 1`）。 |
| **⑦ 輪次與十輪審計** | `cycle_ledger.py` + `rule_store.py sweep` | `tick` 自動剝離微秒時間戳計算實質內容 SHA-256（資料未變拒絕刷輪次）；每滿 10 輪強制鎖定 `.AUDIT_REQUIRED.lock`；解鎖須通過 `audit_scan` 程式化矛盾與互斥掃描（字數 `>= 100` 且無 `forbid/prefer` 衝突）。 |

---

## 🧭 第三章｜幕僚長派工與創辦人主權簽收 (Chief-of-Staff Dispatch & $\Pi_{\text{global}}$)

1. **無單號不派工**：幕僚長（雪）分派任務予任何閣員，必須經 `dispatch.py dispatch` 寫入雜湊鏈帳本並取得 `task_id`（`T-YYYYMMDD-xxxxxx`）；無單號之口頭分派視為未發生。
2. **唯一結果真值**：派工結果唯一採信董事長於真實互動終端機（TTY）以個人口令（PBKDF2 + HMAC-SHA256）簽章之固定簽收詞：**`收` / `退` / `改派:<閣員代號>`**。

---

## 🚫 第四章｜絕對禁止事項 (Zero-Trust Red Lines)

1. **禁止模型自評轉正**：嚴禁直接編輯 `*_rules.jsonl` 將狀態改為 `active` 或偽造 `promote` 事件。
2. **禁止空轉刷輪次**：無新資料或規則狀態實質改變時，嚴禁藉由修改時間戳重複呼叫 `tick`。
3. **禁止母版混入角色私貨**：嚴禁在 `bionic_core/*.py` 寫死特定閣員名稱或專屬業務正則；一切角色特化邏輯必須放置於該角色專屬目錄之 Adapter。
4. **禁止 Fail-Open 放行**：任何產出守門員載入 `enforce.py` 失敗時，必須立即 `sys.exit(1)` 阻斷。
5. **禁止繞過外部存取控制**：遇 `robots.txt` 禁止、登入牆、Cloudflare 403 或授權限制（如司法院 API），一律如實回報並標記「待董事長授權」。

---

## 📚 第五章｜按需載入附屬參考檔索引 (`references/` On-Demand Library)

> 💡 **Antigravity 原生按需載入機制**：本母版已將深度理論、安全協議與子版開發介面拆分至 `references/` 目錄。平時對話**無須載入**，僅在執行以下特定任務時以 `read_file` 按需讀取對應檔案：

| 觸發情境 | 按需讀取之參考檔路徑 | 內容摘要 |
| :--- | :--- | :--- |
| 設計新學習假說、理解 FEP/自檢/代謝公式時 | [`references/01_cognitive_theories_fep_prm_spin.md`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/.agents/skills/bionic-learning-system/references/01_cognitive_theories_fep_prm_spin.md) | FEP 主動推論雙路徑、過程級自檢、內部自對弈去 AI 腔、突觸代謝與溶酶體自噬方程 |
| 執行十輪衝突大審計、排查熔斷器或提交 RFC 時 | [`references/02_rfc_and_circuit_breaker_spec.md`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/.agents/skills/bionic-learning-system/references/02_rfc_and_circuit_breaker_spec.md) | 磁碟持久化三態熔斷器、無鎖雜湊鏈 JSONL、`audit_scan` 程式化審計解鎖與 Master RFC 流程 |
| **新增/修改閣員特化子版或撰寫 Adapter 時** | [`references/03_child_variant_interface_spec.md`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/.agents/skills/bionic-learning-system/references/03_child_variant_interface_spec.md) | 萬用母版與特化子版解耦邊界、`verifier_registry.json` 註冊格式、四大萬用驗算模型介面 |
| 查閱母版 v0.0 ~ v6.3 歷代版本演進與備份時 | [`references/04_master_version_genealogy.md`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/.agents/skills/bionic-learning-system/references/04_master_version_genealogy.md) | `_master_history/` 歷代完整快照與 `bionic_core` 歷史備份索引 |
