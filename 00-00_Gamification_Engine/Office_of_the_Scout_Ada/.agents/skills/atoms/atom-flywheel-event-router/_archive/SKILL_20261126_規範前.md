---
name: atom-flywheel-event-router
description: "全域業務事件意圖解析與流水線智慧路由原子技能。由執行長雪業務主政，專門將創辦人、社群或客戶傳入的未修飾文字與圖片資訊，於毫秒級內進行意圖解析，精準路由至四大作戰動脈：『groupbuy (管家選品)』、『life_service (生活服務)』、『ai_education (AI教育開課)』與『forensics (商業徵信)』，並附載信心評分 (Confidence Score) 與推薦下游調用之專精原子技能清單。"
---

# 🧭 全域業務事件意圖解析與流水線智慧路由原子技能 (Flywheel Event Router Atom)

> **所屬技能組**：飛輪總控 / 執行長戰略調度  
> **核心職責**：專精於「原始業務事件意圖解析、四大作戰動脈精準路由 (groupbuy/life_service/ai_education/forensics)、信心度量化、下游專精原子鏈路裝配」。  
> **原技能母體**：`polaris-flywheel-orchestrator`

---

## 核心功能與深度特性
1. **四大業務作戰動脈智能分流 (4 Pipeline Classification)**：
   - 🛒 `groupbuy`（管家選品）：生鮮商品照、廠商樣品、大宗肉品、海鮮、堅果、農產報價。
   - 🧹 `life_service`（生活服務）：外地孝親、陪診、浴室防滑、水電跑腿、長輩修容理髮、到府代買。
   - 🎓 `ai_education`（AI 教育開課）：實體工作坊、新技術教學、教案投影片、Google 報名表單。
   - 🦅 `forensics`（商業徵信）：廠商背景調查、裁判書穿透、負責人關係網絡、防欺詐資產審計。
2. **多維語意關鍵特徵與信心評分 (Confidence Scoring)**：
   - 自動提取事件文本之核心關鍵字群，計算歸類置信度（0.0 ~ 1.0）。若低於 0.65 自動列入待澄清輔助隊列。
3. **下游專精原子鏈路自動推薦 (Downstream Atomic Dispatch)**：
   - 輸出標準化 JSON Payload，明確標記下一步應調用的專精原子：
     - 若為選品：推薦 `atom-groupbuy-cost-auditor` ➔ `atom-groupbuy-four-prism-copy` ➔ `atom-poster-grid-architect`。
     - 若為生活服務：推薦 `atom-pricing-5d-calculator` ➔ `atom-care-order-dispatcher` ➔ `atom-pricing-bulletproof-clause`。
4. **乾跑防呆 (Dry-Run Support)**：
   - 支援 `--dry-run` 模擬全類型事件分流，提供結構化 JSON 輸出與 Exit Code 0 擔保。

---

## 執行腳本
```bash
python scripts/flywheel_event_router.py --input "這款智利冷凍鮭魚廠商報價每公斤 450 元，幫我分析看看" --dry-run
```
