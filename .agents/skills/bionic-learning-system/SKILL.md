---
name: bionic-learning-system
description: 北極星萬用仿生自進化系統母版 (Bionic Learning System v6.5 殿堂級零信任全覆蓋母版)。100% 角色無關（Role-Agnostic）之底層自進化引擎，由各閣員 Adapter 轉為通用標準樣本列，母版執行純數學驗算、快照存證強制重算 (snapshots/<sha>.jsonl)、狀態機防舊簽重放、反盲簽展示與創辦人 PBKDF2+Schnorr 公鑰驗簽。採用 Core + references/ 按需載入架構，核心規範精簡至 6KB 以內。
is_master: true
lock_status: IMMUTABLE_GOLDEN_MASTER (董事長親定不可覆寫萬用母版；2026-11-15 升級至 v6.5 殿堂級零信任全覆蓋版，舊版完整保留於 _master_history/)
authorized_by: 陳品碩 (陳先生 / 品碩 / 董事長)
version: v6.5-MASTER
---

# 🧬 北極星萬用仿生自進化系統母版 (Universal Bionic Learning Master v6.5)

> ⚡ **【第一章｜憲法級總綱 · 萬用純數學底座與特化分離】**
> 1. **文字不等於進化，宣稱必須有物理憑證**：任何「學習／驗證／審計／轉正」，若無 `bionic_core/` 對應之可執行腳本 Exit Code 0 與雜湊鏈帳本紀錄，一律視為**未發生**。
> 2. **自進化的唯一判準是「先讀後寫」**：下一次產出行為是否被已轉正（`active`）的規則約束改變；只寫日記、不進閘門者，不得自稱自進化。
> 3. **自進化對象為「規則、技能、設定、程式」，非模型權重**：嚴禁誇大為模型重新訓練。
> 4. **母版純數學寫死 ✕ 子版正規化特化（Pure Math Kernel, Role-Specific Adapters）**：
>    - **母版 (`bionic-learning-system` + `bionic_core/`)**：100% 角色無關，**零業務欄位名、零角色私貨**；僅讀取通用標準樣本列（Standard Sample Rows），將**規則狀態機、不可篡改快照重算、反盲簽展示、折疊防偽重算、創辦人公鑰驗簽與十輪審計寫死**。
>    - **子版 (`bionic-learning-{role}` + 子版 Adapter)**：負責消費 `perceived_{role}.jsonl`、將角色專屬資料正規化為標準樣本列（以 `post_ts` 精確回推發布時戳）、並僅以**前半段資料（Discovery Split）**提名候選規則。

---

## 🔄 第二章｜七段萬用自進化閉環協定 (7-Stage Universal Closed-Loop)

```
① 觸發 (Trigger) ➔ ② 感知 (Perceive) ➔ ③ 提名 (Propose) ➔ ④ 驗算 (Evaluate)
                                                              │
⑦ 審計/淘汰 (Audit & Sweep) ◀── ⑥ 強制 (Enforce Gate) ◀── ⑤ 轉正 (Promote)
```

| 階段 | 核心腳本 (`bionic_core/`) | v6.5 殿堂級零信任強制規範（寫死不可繞過） |
| :--- | :--- | :--- |
| **① 觸發** | `run_evolution_cycle.py --office <role>` | 先以 `preview_evaluation` 試算指標並組裝預覽快照；於記憶體比對無重複且無停機鎖後，才正式寫入帳本與快照。無實質變更被阻斷時**規則帳本零污染**（0 廢 trial、0 廢檔案）。 |
| **② 感知** | `perceive_web.py` | 嚴格網域邊界分級；遵守 `robots.txt`；磁碟持久化三態熔斷；輸出由各子版 Adapter 實質消費並轉譯為理論論述。 |
| **③ 提名** | `rule_store.py propose` | 子版 Adapter **僅准使用前半段（Discovery 50%）樣本**提名候選規則；貼文時戳以 `captured_at - age_h` 精確回推發布時間，徹底消除時序切分退化。 |
| **④ 驗算** | `rule_store.py evaluate` | 驗算時強制複製至不可篡改快照 `snapshots/{sha}.jsonl`：<br>• **文字規則**：`holdout_passed` 預設 `False`，**後半段留出集雙組皆須 `>= 3` 筆且優於對照**＋好文誤傷率 `<=35%`。<br>• **數值規則**：支援 `>=`、`<=`、`:` 算子，統一以達標率 (%) 比對，完美支援 `metric_max`（如 `fcp_ms:500`）。<br>• **路由規則 (`route`)**：僅採計創辦人驗簽匯出之標準結案樣本（主組與對照組皆須 `N >= 3`）。 |
| **⑤ 轉正** | `rule_store.py promote` | **反盲簽展示 (Anti-Blind-Signing)**：終端機完整展示待轉正規則全量指標與論述。<br>**狀態機防舊簽重放**：只有 `candidate` 可轉正，已退場規則貼舊簽直接判定 `tampered_rejected`。<br>**Schnorr 公鑰驗簽**：`fold()` 逐行驗雜湊鏈、現場重算快照指標、公鑰免口令驗簽。 |
| **⑥ 強制** | `enforce.py gate` | **先讀後寫（Fail-Closed）**：若存在 active 數值規則但未傳入指標，直接判定違規阻斷！守門員強制核驗 `--task-id` 之雜湊鏈、角色匹配與未結案狀態。未轉正狀態僅作軟性扣分，硬阻斷 100% 委託母版規則。 |
| **⑦ 輪次與十輪審計** | `cycle_ledger.py` + `rule_store.py sweep` | 輪次帳本 Append-Only 帶 `prev`/`hash` 雜湊鏈；**全關卡逐段狀態機 (`is_locked`)**：掃描所有滿 10 倍數關卡確認具備合格 audit_done。高風險審計解鎖簽章強綁定 `(office, cycle, last_tick_hash)`；手動刪 `.lock` 檔或補假 tick 絕對無法解鎖！ |

---

## 🧭 第三章｜幕僚長派工與創辦人中性主權簽收 (`dispatch.py` & `founder_auth.py`)

1. **信任錨中性化**：公鑰與 KCV 統一儲存於 `bionic_core/vaults/founder_vault.meta.json`，標籤為 `polaris-founder-kcv-v65`；簽名時終端機印出 16 碼公鑰指紋備查。
2. **唯一結果真值**：僅採計董事長於真實終端機輸入口令簽章之 `收 / 退 / 改派:<閣員>`，並透過 `dispatch.py export-verified` 匯出附帶 `founder_sig` 之標準路由樣本。

---

## 🚫 第四章｜絕對禁止事項 (Zero-Trust Red Lines)

1. **禁止自簽與偽造事件**：嚴禁手寫 JSONL 偽造 `trial`、`promote` 或 `audit_done`（`fold()` 均現場重算快照與公鑰驗簽）。
2. **禁止空轉刷輪次**：無規則或驗算結果變化時，嚴禁入帳新輪次。
3. **禁止母版混入角色私貨**：`bionic_core/*.py` 嚴禁出現任何特定角色欄位名。
4. **禁止偷看留出集提名**：Adapter 嚴禁用後半段留出集資料提名規則。
5. **禁止繞過外部存取控制**：遇存取限制一律如實回報。

---

## 📚 第五章｜按需載入附屬參考檔索引 (`references/` On-Demand Library)

| 觸發情境 | 按需讀取之參考檔路徑 | 內容摘要 |
| :--- | :--- | :--- |
| 設計學習假說、理解 FEP/自檢/代謝公式時 | `references/01_cognitive_theories_fep_prm_spin.md` | FEP 主動推論、過程級自檢、自對弈去 AI 腔、突觸代謝與溶酶體自噬 |
| 執行十輪審計、排查熔斷器或密碼學驗簽時 | `references/02_rfc_and_circuit_breaker_spec.md` | 持久化三態熔斷器、雜湊鏈 JSONL、`founder_auth` 公鑰驗簽與審計解鎖 |
| 新增/修改閣員特化子版或撰寫 Adapter 時 | `references/03_child_variant_interface_spec.md` | 萬用母版與特化子版解耦邊界、通用標準樣本列規格、`verifier_registry.json` |
| 查閱母版 v0.0 ~ v6.5 歷代版本演進與備份時 | `references/04_master_version_genealogy.md` | `_master_history/` 歷代完整快照與 `bionic_core` 歷史備份索引 |

---
*（極星萬用仿生自進化系統母版 v6.5-MASTER 規範全文完 · 雜湊與公鑰驗簽閉環生效中）*
