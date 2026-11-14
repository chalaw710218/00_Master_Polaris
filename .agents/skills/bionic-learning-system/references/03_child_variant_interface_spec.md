# 🔌 參考卷三｜萬用母版與特化子版解耦對接規格書 (Universal Master-Child Adapter Interface)

> **定位**：本文件為 `bionic-learning-system` 母版之子版開發與特化指南（`references/03_child_variant_interface_spec.md`）。  
> **核心鐵律（董事長親定）**：**「母版負責將通用規則框架、狀態機與安全程式寫死；個性化與進化方向一律由各子版 Agent 的屬性與專長進行特化！」**

---

## 1. 母版與子版的職責邊界（嚴格解耦）

| 層級 | 負責內容（寫死 vs 特化） | 絕對禁止事項 |
| :--- | :--- | :--- |
| **萬用母版層 (`bionic-learning-system` + `bionic_core/`)** | **100% 角色無關（Role-Agnostic）**：<br>1. 規則狀態機 (`candidate` ➔ `active` ➔ `retired` / `tampered_rejected`)<br>2. 通用真值驗算器（留出驗證、誤傷率計算、合規門檻比對、路由成功率統計）<br>3. 先讀後寫強制閘門 (`enforce.py`)<br>4. 去時間戳輪次帳本與程式化衝突掃描 (`cycle_ledger.py`)<br>5. 受控上網與持久化熔斷 (`perceive_web.py`) | ❌ **母版程式碼內嚴禁寫死任何單一閣員代號（如 `if office == 'kage'`）、專屬檔案路徑或特定業務正則（如天氣詞、特定色票）！** |
| **特化子版層 (`bionic-learning-{role}` + 子版 Adapter)** | **100% 領域特化（Domain-Specific）**：<br>1. 該閣員的人格、專業信念與進化方向<br>2. 該閣員專屬的真值資料集路徑與欄位映射（定義於 `verifier_registry.json`）<br>3. 該閣員專屬的特徵萃取與候選規則提名器（Adapter 腳本） | ❌ **子版嚴禁繞過母版 `rule_store.py` / `enforce.py` 自行宣布規則轉正或跳過十輪審計鎖！** |

---

## 2. 子版接入萬用母版的標準設定 (`verifier_registry.json`)

任何新增或現有閣員子版，只需在 `bionic_core/verifier_registry.json` 註冊標準設定（無須修改母版 `.py` 程式碼）：

```json
{
  "office_id": {
    "dataset_path": "相對專案根目錄之真實資料集路徑 (.jsonl)",
    "evaluator_type": "text_er | metric_summary | dispatch_ledger | custom",
    "adapter_script": "該子版專屬之特徵學習與規則提名腳本路徑 (.py)",
    "discover_feeds_key": "feeds_registry.json 內對應之探索源鍵名",
    "risk_default": "low | high",
    "enforce_hook": "實際產出流程呼叫 enforce.py gate 之位置說明"
  }
}
```

---

## 3. 母版支援之四大萬用驗算模型 (`evaluator_type`)

母版 `rule_store.py evaluate` 根據資料集結構與規則型態（`kind`），提供四種與角色無關的萬用數學驗算器：

1. **`text_metric`（文字特徵 ✕ 連續成效指標，支援 JSONL 內含 `posts` 或單行 `{"text": ..., "metric": ...}`）**：
   - 適用規則：`forbid_phrase`, `prefer_phrase`, `max_count`, `regex_forbid`（支援 `scope="prefix"` 或 `"any"`）。
   - 驗算標準：樣本數 `N >= 3`、遵守組平均值 `> 對照組`、時序留出集（Holdout 後半段）方向一致、且高於中位數樣本之誤傷率 `<= 35%`。
2. **`metric_threshold`（數值門檻對照，支援配對陣列或摘要統計）**：
   - 適用規則：`metric_min`, `metric_max`。
   - 驗算標準：真實達標率或數值必須嚴格滿足門檻（廢除 `wo_mean = 0.0` 假通過）。
3. **`baseline_standard`（憲法級固定合規基準）**：
   - 適用規則：`baseline_standard`（格式 `指標名:基準值`，如 `contrast_ratio:7.0`、`defects:0`）。
   - 驗算標準：綁定真實基線盤點檔案與 SHA-256 簽章，於 `enforce.py gate --metrics` 執行硬性合規攔截，不偽裝成 A/B 隨機實驗。
4. **`dispatch_route`（派工路由成功率，讀取 `dispatch.py` 格式帳本）**：
   - 適用規則：`route`（格式 `任務類別->閣員代號`）。
   - 驗算標準：統計經創辦人簽收結案之一次通過率（First-Pass Acceptance Rate），指派該閣員之一次通過率優於對照且 `N >= 3`。
