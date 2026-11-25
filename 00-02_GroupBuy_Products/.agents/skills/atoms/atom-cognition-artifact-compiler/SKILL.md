---
name: atom-cognition-artifact-compiler
description: 🧬 極星認知真值結構化產物編譯原子 (Polaris Cognition Artifact Compiler Atom v1.0)。由 CTO 林納斯 (Linus) 確定性架構主政、首席品質長戴明 (Dr. Deming) 安燈監製。專門接收經過 PRM 與 SPIN 去 AI 腔清洗之客觀事實與實戰信念，一鍵編譯輸出為：1. 現場不可做錯的《戴明神級防呆 SOP 檢核表》(compile-sop)、2. 扣緊在地痛點的《Threads/FB 爆款選題庫》(compile-topics)、3. 算盤 D1~D5 商業《5D 定價矩陣參數檔》(compile-pricing)。
---

# 🧬 極星認知真值結構化產物編譯原子 (atom-cognition-artifact-compiler)

由 CTO 林納斯 (Linus) 業務主政、首席品質長戴明 (Dr. Deming) 防呆監製、行銷長泰勒絲 (Taylor) 選題協同。

## 核心定位與職責
專門將非結構化的 Markdown 筆記與真值信念，轉化為現場真正可執行、具備物理約束力的四大標準產物：
1. **`compile-sop`**：自動編譯為 Markdown 表格式的《戴明神級防呆 SOP 現場檢核表》，包含檢查工項、合格判據與出發前安燈。
2. **`compile-topics`**：自動編譯為《Threads/FB 雙軌爆款選題靈感庫》，包含常民痛點切角、大師靈魂金句、以及第一則留言掛載建議。
3. **`compile-pricing`**：自動編譯為《5D 商業價值精算矩陣參數 JSON》，供報價引擎直接調用。

## 輸入參數規範
- `--mode`: 編譯目標產物模式 (`compile-sop`, `compile-topics`, `compile-pricing`，預設 `compile-sop`)
- `--source-belief`: 來源真值條目或經驗事實（可直接輸入或帶預設範例）
- `--output-file`: 產出檔案路徑（預設依模式自動命名）
- `--dry-run`: 物理演練模式，不寫入磁碟僅輸出編譯結構預覽

## 執行腳本
```bash
python scripts/artifact_compiler.py --mode compile-sop --dry-run
python scripts/artifact_compiler.py --mode compile-topics --dry-run
```
