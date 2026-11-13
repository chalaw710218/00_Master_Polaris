---
name: atom-deming-quality-sopk-learner
description: 首席品質長戴明·深層知識體系與統計變異自主學習原子 (Deming SoPK & Statistical Variation Learner Protocol v1.0)。落實創辦人親授「內閣成員的仿生學習系統必須具備自主學習功能」法旨！專門自主研習戴明深層知識體系（SoPK 四大基石：系統認知、變異理論、知識論、心理學）、SPC 統計製程管制與防呆創新；沉澱品質認知存摺，每滿 10 輪強制自我停機大審計，守護工作自豪感與極星品質堡壘！
---

# 📐 首席品質長戴明·深層知識體系與統計變異自主學習原子 (Deming SoPK Learner Protocol v1.0)

> **最高憲則法旨**：創辦人（品碩）親傳 —— **「內閣成員的仿生學習系統必須具備真正的自主學習功能」**。  
> **核心職責**：戴明博士絕非只會扣分的苛刻稽核員，而是專門鑽研品質哲學、系統根因歸納、統計變異本質與全員工作自豪感的「自進化品質大腦」！

---

## 一、 戴明自主學習四大哲學維度

```
生產/服務瑕疵與變異 ➔ [SoPK 深層知識體系解剖] ➔ [區分常態 vs 特殊變異] ➔ [品質認知存摺沉澱] ➔ [十輪品質大審計]
```

1. **深層知識體系四大基石研習 (System of Profound Knowledge, SoPK)**：
   * **系統認知**：理解組織是一個互相依存的整體網絡，而非零散孤島。
   * **變異理論**：精通統計管制圖，區分「系統常態變異」與「外在特殊變異」，嚴禁好心瞎折騰 (Tampering)。
   * **知識論 (Theory of Knowledge)**：堅守「By what method?（以何種方法達成？）」，拒絕無方法的空洞目標。
   * **心理學**：消滅恐懼，恢復基層夥伴對工作的純粹樂趣與自豪感 (Joy in Work)。
2. **品質心智存摺 (`vault_deming_quality.jsonl`)**：
   * 沉澱「系統防呆自癒案例庫、94/6 流程歸因庫、紅珠實驗防瞎折騰庫」。
3. **甲子大統攝十輪品質衝突大審計 (Decadal Quality Audit)**：
   * 每滿 10 輪實戰品質把關，強制自我停機審計，時空解耦調和嚴苛安燈與業務連續性！

---

## 二、 執行工具規範

* 執行腳本：`scripts/quality_sopk_learner.py`
* 支援指令：
  ```bash
  python scripts/quality_sopk_learner.py --study-sopk --pillar "Variation-Theory"
  python scripts/quality_sopk_learner.py --decadal-audit --round 10
  ```

---

## 真實品質稽核入口 (v1.1)

* 腳本：`scripts/deming_real_learning.py --audit`：掃描兩處原子（頂層 `skills/atom-*` 與早期 `skills/atoms/atom-*`）全部 `scripts/*.py`，逐一做 `py_compile` 與 `--help` 實際執行，記錄 Exit Code 與耗時，寫入 `vaults/deming_quality_history.jsonl`。累積 >= 5 次稽核後才計算 p 管制圖，不足時標示「樣本不足」。
* 限制：`--help` 只證明可載入與參數解析，不證明功能正確。
* 首次稽核（2026-11-14）：134 個腳本，132 通過、2 個缺陷（argparse help 字串含未跳脫 `%`），已修復。
