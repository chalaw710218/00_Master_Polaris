---
name: atom-product-redteam-audit
description: 執行四方黑臉交叉審查與戴明防呆安燈出廠驗收。在三合一交付套版完稿準備發布前審核時使用；初稿骨架裝配時不用。只由 polaris-productization-master 呼叫，不單獨使用。
metadata:
  group: 商品化
  parent: polaris-productization-master
  owner: 戴明
  status: draft
  version: "1.0"
---

# 🛑 商品化多 Agent 四方黑臉交叉審查與戴明防呆安燈原子技能 (Product Red-Team Audit & Deming Andon Atom)

> **核心職責**：專精於「四方黑臉多維挑刺審查、反 AI 塑料感真實性驗收、品牌法定名稱零洩漏防火牆、100 分制安燈拉繩門禁」。  

---

## 核心功能與深度特性
1. **多 Agent 四方黑臉獨立挑刺 (4-Way Red-Teaming)**：
   - **泰勒絲 (FB 檢核 · 25分)**：首句穿透率、是否像過載傳單、內文嚴格零外部超連結、第一則留言導流是否閉環。
   - **影 (Threads 檢核 · 25分)**：嚴禁代碼假手寫、嚴禁 AI 假人臉、是否具備自嘲與常民真實痛點。
   - **約瑟夫 (美學檢核 · 25分)**：視讀呼吸留白率、雙字體層級、版面秩序。
   - **戴明 (合規安燈 · 25分)**：服務邊界透明、明碼標價完整、查理蒙格代墊款風控、家宅門市座標齊備、**品牌法定名稱零洩漏防火牆 (嚴禁極星)**。
2. **戴明 100 分制出廠門禁 (Andon Quality Gate)**：
   - 總分 $\ge 85$ 分且無一票否決項目：准予呈報創辦人批准發射 (`PASS_ANDON`)。
   - 總分 $< 85$ 分或觸犯品牌紅線：**立即觸發安燈拉繩 (`PULL_ANDON_REJECT`)，Exit Code 1 阻斷出廠**，列出具體改善清單。

---

## 執行腳本
```bash
python scripts/product_redteam_audit.py --product-dir "00-02_Products/00-02-07_Vendor_越臺鹽焗腰果" --dry-run
```
