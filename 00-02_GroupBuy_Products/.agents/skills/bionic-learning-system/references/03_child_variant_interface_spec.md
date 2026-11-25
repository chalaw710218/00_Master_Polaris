# 🔌 參考卷三｜萬用母版與特化子版解耦對接規格書 (Universal Master-Child Adapter Interface v6.4)

> **定位**：本文件為 `bionic-learning-system` 母版之子版開發與特化指南（`references/03_child_variant_interface_spec.md`）。  
> **核心鐵律（董事長親定）**：**「母版負責將通用規則框架、狀態機與純數學驗算寫死；個性化與資料正規化一律由各子版 Agent 的 Adapter 進行特化！」**

---

## 1. 母版與子版的職責邊界（零角色私貨）

| 層級 | 負責內容（寫死 vs 特化） | 絕對禁止事項 |
| :--- | :--- | :--- |
| **萬用母版層 (`bionic-learning-system` + `bionic_core/`)** | **100% 角色無關（Pure Math Kernel）**：<br>1. 規則狀態機 (`candidate` ➔ `active` ➔ `retired` / `tampered_rejected`)<br>2. 通用標準樣本列驗算器（留出驗證預設 `False`、誤傷率計算、達標率比對、驗簽路由統計）<br>3. 折疊防偽重算與創辦人 PBKDF2+Schnorr 公鑰驗簽 (`founder_auth.py`)<br>4. 先讀後寫強制閘門與指標缺席阻斷 (`enforce.py`)<br>5. 純規則雜湊輪次帳本與程式化衝突掃描 (`cycle_ledger.py`) | ❌ **母版程式碼內嚴禁寫死任何單一閣員代號、業務欄位名（如 `pass_body_text_7`, `defects`, `fcp_ms`, `posts`, `er`）或派工詞（`收`/`退`）！** |
| **特化子版層 (`bionic-learning-{role}` + 子版 Adapter)** | **100% 領域特化（Domain-Specific）**：<br>1. 消費 `perceived_{role}.jsonl` 外部感知摘要<br>2. 將角色原始資料轉為母版通用標準樣本列 (`*_standard_samples.jsonl`)<br>3. **僅使用前半段（Discovery 50%）樣本**計算特徵並提名候選規則 | ❌ **子版嚴禁偷看後半段留出集提名規則，亦嚴禁繞過母版自行宣布轉正！** |

---

## 2. 三種通用標準樣本列格式 (Universal Standard Sample Rows)

所有子版 Adapter 必須將專屬資料轉換為以下三種標準 JSONL 格式之一，供 `rule_store.py` 執行純數學驗算：

1. **標準文字成效樣本列 (`{id, text, metric, ts}`)**：
   - 格式：`{"id": "01", "text": "貼文或標題內容", "metric": 4.5, "ts": "2026-11-15T00:00:00"}`
   - 適用規則：`forbid_phrase`, `prefer_phrase`, `max_count`, `regex_forbid`。
   - 驗算標準：`holdout_passed` 初值預設 `False`，須樣本 `>= 6` 且後半段留出集同時具備遵守組與對照組並優於對照、總樣本 `N >= 3`、好文誤傷率 `<= 35%`。
2. **標準數值門檻樣本列 (`{n, compliant, metrics}` 或 `{samples: [...]}`)**：
   - 格式：`{"id": "run-1", "n": 100, "compliant": 100, "metrics": {"fcp_ms": 380.0}, "ts": "..."}`
   - 適用規則：`metric_min` (`>=`), `metric_max` (`<=`), `baseline_standard` (`>=` / `<=`)。
   - 驗算標準：統一以達標率 (%) vs 未達標率 (%) 比對，完美支援 `metric_max`（如 `fcp_ms:500`）。
3. **創辦人驗簽路由樣本信封 (`verified_route_samples`)**：
   - 由創辦人於真實終端機執行 `dispatch.py export-verified` 驗鏈並驗證每筆 `signoff` 之 HMAC 後匯出，附帶 `founder_sig` 簽章。
   - 適用規則：`route`（格式 `任務類別->閣員代號`），主組與對照組皆須 `N >= 3` 且留出集通過。
