---
name: atom-deming-joy-flow-allocator
description: 首席品質長戴明·80/20鋼鐵底線與工作自豪感心流調配原子 (Deming 80/20 Elastic Flow & Joy in Work Allocator v1.0)。專門落實戴明第16律「80/20彈性心流律」、第17律「時空分級放行律」與第18律「障礙清除領導律」。在80%安全合規與財務底線鎖死的前提下，主動授權20%前線人性自主裁量權（長輩溫暖陪伴、突發天候關懷），視為極星最高品質溢價；並以「基層障礙清除率」作為領導治理唯一指標，徹底驅逐恐懼，守護全員工作自豪感。
role_key: deming
type: atomic_skill
parent_skill: bionic-learning-deming
version: v1.0
exit_code_verified: true
---

# 👑 戴明 80/20 彈性心流與工作自豪感調配原子 (Deming 80/20 Joy Flow Allocator)

> 📐 **原子使命**：貫徹戴明哲學最溫暖深邃的精髓——「工作自豪感 (Joy in Work)」與「80/20 彈性心流律」。如果一個品質系統只剩下冰冷的懲處與死板的打卡，那不是戴明品質，而是官僚暴政！本原子將 SOP 鎖死於 80% 的鋼鐵安全底線，同時將 20% 的空間授權給前線生活管家的人性善意與溫暖心流；並將主管的唯一 KPI 錨定於「基層工作障礙清除率」！

---

## 🏛️ 80/20 彈性心流架構 (The 80/20 Elastic Flow Architecture)

```mermaid
flowchart TD
    Task["前線管家服務 / 研發作業"] --> DualCheck{"80% 鋼鐵安全底線核驗"}
    
    subgraph Ironclad80 ["🛡️ 80% 鋼鐵安全底線 (不可妥協)"]
        S1["• 零負毛利與財務代墊風控"]
        S2["• 零品牌代號洩漏 (極星防火牆)"]
        S3["• 零資安洩漏與本機 Exit Code 0"]
        S4["• 客戶知情與人身安全保證"]
    end
    
    DualCheck -->|觸犯任何一項| Veto["🚨 安燈硬阻斷 (Andon Hard Stop)\n• 立即叫停，禁止出廠"]
    
    DualCheck -->|80% 底線完全滿足| Flow20{"20% 人性心流與溫度評估"}
    
    subgraph FlowZone20 ["🌸 20% 人性自主心流 (品質溢價)"]
        F1["• 為獨居長輩多停留 10 分鐘傾聽日常"]
        F2["• 遭遇驟雨自發性加套雙層防雨包裝"]
        F3["• 主動記錄長者用藥與步態微小變化"]
    end
    
    Flow20 -->|展現人性關懷| JoyPass["👑 戴明至樂品質榮譽放行 (PASSED_WITH_JOY_HONOR)\n• 認定為最高品質溢價，享有免責保護"]
    Flow20 -->|常規標準作業| StandardPass["✅ 標準合規放行 (STANDARD_COMPLIANT)"]
```

---

## 🧭 管理者唯一 KPI：障礙清除治理 (Impediment Clearance Governance)

* **傳統錯誤管理**：監工、挑刺、統計違規次數、考勤打卡 $\rightarrow$ 誘發恐懼與隱匿。
* **戴明領導治理**：唯一職責為「為一線夥伴清除工作障礙」！
  - 阻礙公式：$$\text{障礙清除率 (ICR)} = \frac{\text{已排除之工具/流程卡頓數}}{\text{夥伴回報之摩擦痛點總數}} \ge 90\%$$

---

## 🛠️ 命令列工具 (CLI Usage)

```powershell
# 評估前線作業：核驗 80% 底線 + 計算 20% 溫暖心流
python scripts/joy_flow_allocator.py --eval-task '{"safety_checks": {"no_negative_margin": true, "no_brand_leak": true, "no_security_breach": true}, "human_warmth_actions": ["為獨居阿嬤多倒一杯溫水並檢查鞋帶安全", "代客留意門鎖生鏽問題"]}'

# 評估管理者「障礙清除率」KPI
python scripts/joy_flow_allocator.py --eval-manager '{"impediments_reported": 10, "impediments_cleared": 9}'
```
