---
name: bionic-learning-system
description: 北極星萬用仿生自進化系統母版 (Bionic Learning System v6.4 密碼學零信任與純數學萬用核心母版)。100% 角色無關（Role-Agnostic）之底層自進化引擎，由各閣員 Adapter 轉為通用標準樣本列，母版僅執行純數學驗算、折疊防偽重算與創辦人 PBKDF2+Schnorr 公鑰驗簽。採用 Core + references/ 按需載入架構，核心規範精簡至 6KB 以內。
is_master: true
lock_status: IMMUTABLE_GOLDEN_MASTER (董事長親定不可覆寫萬用母版；2026-11-15 升級至 v6.4 密碼學零信任與純數學核心版，舊版完整保留於 _master_history/)
authorized_by: 陳品碩 (陳先生 / 品碩 / 董事長)
version: v6.4-MASTER
---

# 🧬 北極星萬用仿生自進化系統母版 (Universal Bionic Learning Master v6.4)

> ⚡ **【第一章｜憲法級總綱 · 萬用純數學底座與特化分離】**
> 1. **文字不等於進化，宣稱必須有物理憑證**：任何「學習／驗證／審計／轉正」，若無 `bionic_core/` 對應之可執行腳本 Exit Code 0 與雜湊鏈帳本紀錄，一律視為**未發生**。
> 2. **自進化的唯一判準是「先讀後寫」**：下一次產出行為是否被已轉正（`active`）的規則約束改變；只寫日記、不進閘門者，不得自稱自進化。
> 3. **自進化對象為「規則、技能、設定、程式」，非模型權重**：嚴禁誇大為模型重新訓練。
> 4. **母版純數學寫死 ✕ 子版正規化特化（Pure Math Kernel, Role-Specific Adapters）**：
>    - **母版 (`bionic-learning-system` + `bionic_core/`)**：100% 角色無關，**零業務欄位名、零角色私貨**；僅讀取通用標準樣本列（Standard Sample Rows），將**規則狀態機、純數學驗算、折疊防偽重算、創辦人公鑰驗簽與十輪審計寫死**。
>    - **子版 (`bionic-learning-{role}` + 子版 Adapter)**：負責消費 `perceived_{role}.jsonl`、將角色專屬資料正規化為標準樣本列、並僅以**前半段資料（Discovery Split）**提名候選規則。

---

## 🔄 第二章｜七段萬用自進化閉環協定 (7-Stage Universal Closed-Loop)

```
① 觸發 (Trigger) ➔ ② 感知 (Perceive) ➔ ③ 提名 (Propose) ➔ ④ 驗算 (Evaluate)
                                                              │
⑦ 審計/淘汰 (Audit & Sweep) ◀── ⑥ 強制 (Enforce Gate) ◀── ⑤ 轉正 (Promote)
```

| 階段 | 核心腳本 (`bionic_core/`) | v6.4 萬用零信任規範（寫死不可繞過） |
| :--- | :--- | :--- |
| **① 觸發** | `run_evolution_cycle.py --office <role>` | 依 `verifier_registry.json` 載入子版 `adapter_script`。先於記憶體核對規則與驗算 SHA-256，無實質變化當場拒絕且不寫廢檔；`--all-ready` 具備單點容錯隔離。 |
| **② 感知** | `perceive_web.py` | 嚴格網域邊界分級（轉址後二次校驗）；遵守 `robots.txt`；磁碟持久化三態熔斷；剝離提示注入；輸出由各子版 Adapter 實質消費。 |
| **③ 提名** | `rule_store.py propose` | 子版 Adapter **僅准使用前半段（Discovery 50%）樣本**提名候選規則（8 大型態：`forbid_phrase`, `prefer_phrase`, `max_count`, `regex_forbid`, `metric_min`, `metric_max`, `baseline_standard`, `route`）。 |
| **④ 驗算** | `rule_store.py evaluate` | 僅讀取通用標準樣本列並簽章 `dataset_sha256`：<br>• **文字規則**：`holdout_passed` **初值預設 `False`**（後半段留出集缺組或樣本 `<6` 一律不得轉正）＋好文誤傷率 `<=35%`。<br>• **數值規則**：支援 `>=`、`<=`、`:` 算子，統一以達標率 (%) 比對，完美支援 `metric_max`（如 `fcp_ms:500`）。<br>• **路由規則 (`route`)**：拒絕未驗簽原始帳本！僅採計經董事長口令執行 `dispatch.py export-verified` 驗簽匯出之標準結案樣本（主組與對照組皆須 `N >= 3`）。 |
| **⑤ 轉正** | `rule_store.py promote` | 廢除無密碼布林旗標！高風險 (`risk="high"`) 轉正強制於真實終端機 (TTY) 輸入創辦人口令，產生 `PBKDF2 + Schnorr` 雙重簽章 (`founder_sig`)。`fold()` 逐行驗雜湊鏈、重算資料集指標防偽、並以公鑰 `pub_y` 免口令驗簽，任何手寫假 `trial` 或假 `promote` 直接打入 `tampered_rejected`。 |
| **⑥ 強制** | `enforce.py gate` | **先讀後寫（Fail-Closed）**：若存在 active 數值規則但呼叫端未傳入對應指標（指標缺席），直接判定違規阻斷！守門員強制核驗 `--task-id` 之雜湊鏈、指派角色匹配與未結案狀態。 |
| **⑦ 輪次與十輪審計** | `cycle_ledger.py` + `rule_store.py sweep` | 輪次雜湊剝離時間戳、`discover` 與 `meta`（僅算規則與驗算結果）；滿 10 輪強制停機；高風險辦公室 `audit-done` 強制要求 TTY 創辦人口令簽章，且手動刪 `.lock` 檔無法繞過帳本驗簽鎖定。 |

---

## 🧭 第三章｜幕僚長派工與創辦人主權簽收 (`dispatch.py` & `founder_auth.py`)

1. **無單號不派工**：雪分派任務必須經 `dispatch.py dispatch` 取得 `task_id`；`dispatch.py status` 若偵測斷鏈立即回傳 `Exit Code 1`。
2. **唯一結果真值**：僅採計董事長於真實終端機 (TTY) 輸入個人口令簽章之 `收 / 退 / 改派:<閣員>`，並透過 `dispatch.py export-verified` 匯出附帶 `founder_sig` 之標準路由樣本。

---

## 🚫 第四章｜絕對禁止事項 (Zero-Trust Red Lines)

1. **禁止自簽與偽造事件**：嚴禁手寫 JSONL 偽造 `trial`、`promote` 或 `audit_done`（`fold()` 與 `is_locked()` 均內建重算與公鑰驗簽）。
2. **禁止空轉刷輪次**：無規則或驗算結果變化時（即使抓了新網頁），嚴禁入帳新輪次。
3. **禁止母版混入角色私貨**：`bionic_core/*.py` 嚴禁出現任何特定角色欄位名；一切資料轉換由子版 Adapter 負責。
4. **禁止偷看留出集提名**：Adapter 嚴禁用後半段留出集資料提名規則。
5. **禁止繞過外部存取控制**：遇 `robots.txt` 或法規資料庫連線限制，一律如實回報。

---

## 📚 第五章｜按需載入附屬參考檔索引 (`references/` On-Demand Library)

平時對話無須載入，僅在執行特定任務時以 `read_file` 按需讀取：

| 觸發情境 | 按需讀取之參考檔路徑 | 內容摘要 |
| :--- | :--- | :--- |
| 設計學習假說、理解 FEP/自檢/代謝公式時 | `references/01_cognitive_theories_fep_prm_spin.md` | FEP 主動推論、過程級自檢、自對弈去 AI 腔、突觸代謝與溶酶體自噬 |
| 執行十輪審計、排查熔斷器或密碼學驗簽時 | `references/02_rfc_and_circuit_breaker_spec.md` | 持久化三態熔斷器、雜湊鏈 JSONL、`founder_auth` 公鑰驗簽與審計解鎖 |
| 新增/修改閣員特化子版或撰寫 Adapter 時 | `references/03_child_variant_interface_spec.md` | 萬用母版與特化子版解耦邊界、通用標準樣本列規格、`verifier_registry.json` |
| 查閱母版 v0.0 ~ v6.4 歷代版本演進與備份時 | `references/04_master_version_genealogy.md` | `_master_history/` 歷代完整快照與 `bionic_core` 歷史備份索引 |

---
*（極星萬用仿生自進化系統母版 v6.4-MASTER 規範全文完 · 雜湊與公鑰驗簽閉環生效中）*
