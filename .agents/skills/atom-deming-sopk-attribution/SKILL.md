---
name: atom-deming-sopk-attribution
description: 首席品質長戴明·深層知識體系與94/6系統歸因審計原子 (Deming SoPK & 94/6 Systemic Attribution Protocol v1.0)。負責落實戴明深層知識體系（系統認知、變異理論、知識論「By what method?」、心理學），以SPC與韋斯頓電氣四規則區分常態與特殊變異（避免瞎折騰），並嚴格執行「94/6責任律」將缺陷根因精準歸咎於系統流程與防呆缺失，驅逐恐懼，杜絕苛責基層夥伴。
role_key: deming
type: atomic_skill
parent_skill: bionic-learning-deming
version: v1.0
exit_code_verified: true
---

# 🔬 戴明深層知識體系與94/6系統歸因審計原子 (Deming SoPK & 94/6 Attribution)

> 📐 **原子使命**：貫徹戴明哲學最神聖核心——深層知識體系 (SoPK, System of Profound Knowledge) 與 94/6 責任律。任何品質事件開口必問操作型定義「By what method?」；以變異統計理論嚴格區分常態變異（系統固有）與特殊變異（外生異常），杜絕管理者的盲目微調瞎折騰（Tampering）；並將 94% 的品質問題溯源至制度、SOP 與工具缺陷，堅決捍衛基層夥伴的心理安全感！

---

## 🏛️ SoPK 四大核心支柱 (The Four Pillars of SoPK)

```mermaid
flowchart TD
    subgraph SoPK ["🔬 戴明深層知識體系 (System of Profound Knowledge)"]
        P1["1. 系統認知 (System Appreciation)\n• 極星全域最優解優先\n• 廢除部門 KPI 定額撕裂"]
        P2["2. 變異理論 (Knowledge of Variation)\n• 常態變異 vs 特殊變異\n• 韋斯頓電氣四規則流式預警\n• Cpk >= 1.33 製程能力管理"]
        P3["3. 知識論 (Theory of Knowledge)\n• 開口必問『By what method?』\n• 無操作型定義即非知識\n• PDSA (Study) 深究根因"]
        P4["4. 心理學 (Psychology & Joy)\n• 驅逐恐懼 (Drive out fear)\n• 94/6 責任律 (責任在系統不在人)\n• 捍衛工作自豪感 (Joy in Work)"]
    end
    
    P1 & P2 & P3 & P4 --> AuditEngine["⚖️ 戴明系統歸因審計引擎 (sopk_attribution_engine.py)"]
```

---

## ⚖️ 94 / 6 責任律審計守則 (The 94/6 System Attribution Law)

* **94% 系統責任 (Common System Cause)**：
  - 流程模糊、交接表單缺失、器具設計不良、培訓不足、缺乏防呆 (Poka-Yoke)、時間過度緊繃。
  - **處置方針**：100% 由管理層與架構師檢討，修改 SOP 並部署數位防呆機制。
* **6% 人員特殊失誤 (Special Human Cause)**：
  - 僅當存在故意蓄意破壞、或在已具備完善防呆與知情確認下仍刻意繞過者。
  - **處置方針**：嚴禁人身羞辱與公開處罰，進行一對一障礙清除對話與再培訓。

---

## 🛠️ 命令列工具 (CLI Usage)

```powershell
# 1. 執行數值序列變異分析與 Cpk / 韋斯頓電氣規則審計
python scripts/sopk_attribution_engine.py --mode spc --values "10.2, 10.5, 9.8, 10.1, 10.4, 9.9, 12.8" --usl 11.5 --lsl 8.5

# 2. 執行事故 94/6 系統歸因審計（自動糾正甩鍋基層的錯誤報告）
python scripts/sopk_attribution_engine.py --mode incident --report '{"incident": "外送員送錯地址", "claimed_blame": "外送員不細心", "system_context": {"address_format_ambiguous": true, "gps_drift_no_warning": true}}'
```
