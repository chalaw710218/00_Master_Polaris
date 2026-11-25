---
name: atom-pricing-5d-calculator
description: "創辦人原創 5D 商業價值矩陣多型精算底座原子技能。專精於 D1(摩擦力)、D2(風險承擔)、D3(認知門檻)、D4(時效槓桿)、D5(情緒信任) 五維係數校準，支援 5D-Labor (勞務工時)、5D-Impact (成果價值捕獲)、5D-Asset (數位資產研發攤提) 三大模態純淨數值計算，並內建查理·蒙格代墊款三色燈風控線。"
---

# 🧮 創辦人原創 5D 商業價值矩陣多型精算底座原子技能 (5D Pricing Matrix Calculator Atom)

> **所屬技能組**：5D定價 / 算盤財務工匠  
> **核心職責**：專精於「D1~D5 五維係數校準、三大模態 (Labor/Impact/Asset) 數學連乘、查理·蒙格代墊款三色燈風控線、最低起步價保底精算」。  
> **原技能母體**：`polaris-5d-pricing-engine`

---

## 核心功能與深度特性
1. **五維價值係數精確校準 (D1~D5 Calibration)**：
   - `D1` 摩擦力 (1.0~2.5)：路程距離、氣候路況、等待時間與多點採買不確定性。
   - `D2` 風險承擔 (1.0~3.0)：物品貨值賠償風險、低溫生鮮保鮮責任、易碎品防護。
   - `D3` 認知技術門檻 (1.0~3.5)：特殊採購辨識力、專業水電配管、藥局代領醫學常識轉譯。
   - `D4` 時效槓桿力 (1.0~3.0)：急件即刻出勤、深夜暴雨救援、常規預約排程。
   - `D5` 情緒信任安心度 (1.0~2.5)：陪伴高齡長者、親切耐心、重大事項託付。
2. **三大模態純淨精算 (Base Polymorphism Engine)**：
   - **5D-Labor 勞務型**：$\text{Price} = \max(\text{NT\$ 200}, \text{RoundUp}(\text{Base Hours} \times D1 \times D2 \times D3 \times D4 \times D5 \times \text{時薪基準}))$.
   - **5D-Impact 成果型**：按客戶挽救損失或創造利潤之比例捕獲價值，$\text{Price} = \max(\text{NT\$ 6,000}, \text{Value Impact} \times \text{提成} \times \text{Multiplier})$.
   - **5D-Asset 資產型**：固定研發成本規模攤提加上邊際履約成本與資產溢價乘數。
3. **查理·蒙格代墊款三色燈風控線 (Cashflow Fortress Gate)**：
   - 🟢 **綠燈 (<= NT$ 1,000)**：常規代墊，憑發票/收據現場結清。
   - 🟡 **黃燈 (NT$ 1,001 ~ 2,000)**：需委託人提供即時轉帳證明或信用擔保。
   - 🔴 **紅燈 (> NT$ 2,000)**：**強制啟動預付防線**！必須全額預付方可出勤代買，杜絕無息墊資與壞帳。

---

## 執行腳本
```bash
python scripts/pricing_5d_calculator.py --mode labor --minutes 45 --d1 1.2 --d2 1.5 --item-value 2500 --dry-run
```
