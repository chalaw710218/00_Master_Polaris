---
name: atom-cognition-vault-auditor
description: 🧬 極星認知存摺全息健康掃描與去 AI 腔質檢原子 (Polaris Cognition Vault Auditor & Slop Filter Atom v1.0)。由首席品質長戴明 (Dr. Deming) 安燈主政、執行長雪 (Yuki) 認知監製。專門遞歸巡邏全域內閣辦公室之認知存摺，盤點客觀事實 (Facts)、深層信念 (Beliefs) 與前瞻好奇心 (Curiosities) 累積量，並透過 PRM 置信度打分與 SPIN 自對弈機制，徹底濾除「在當今瞬息萬變的世界中」、「總之」等空洞 AI 腔浮誇廢話，確保知識純度。
---

# 🧬 極星認知存摺全息健康掃描與去 AI 腔質檢原子 (atom-cognition-vault-auditor)

由首席品質長戴明 (Dr. Deming) 業務主政、執行長雪 (Yuki) 心智監製、CTO 林納斯 (Linus) 確定性代碼驗收。

## 核心定位與職責
專門解決內閣在長期仿生自進化中，認知存摺膨脹、未經證實的空中樓閣假說混入、以及 LLM 容易生成的空洞 AI 腔套話污染知識庫之痛點。
本原子作為認知純度守門人，提供：
1. **全息存摺資產盤點**：自動統計各首長辦公室累積的客觀硬事實、演化深層信念與前瞻商業好奇心數量。
2. **PRM 過程級置信度打分**：僅放行置信度 $\ge 90\%$ 且具備實證驗證的條目。
3. **SPIN 自對弈去 AI 腔濾網**：硬核檢驗並剔除浮誇開場白、空洞套話與雞湯式發言，保留創辦人最重視的實幹商人底色。

## 輸入參數規範
- `--vault-dir`: 指定掃描之辦公室存摺根目錄（預設 `.` 工作區）
- `--filter-slop`: 是否開啟嚴格去 AI 腔過濾器（預設開啟）
- `--min-confidence`: PRM 置信度門檻（預設 `90`%）
- `--dry-run`: 物理演練模式，模擬掃描並輸出健康質檢報告

## 執行腳本
```bash
python scripts/vault_auditor.py --dry-run
```
