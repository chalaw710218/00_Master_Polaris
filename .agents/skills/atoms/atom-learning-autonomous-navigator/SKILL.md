---
name: atom-learning-autonomous-navigator
description: 自主導航、算力分級與三階戰略原子 (Autonomous Navigation & Strategy Formulation Atom)。專職負責在創辦人拋出宏觀方向時，自主進行測試時算力分級 (Level 1~3)、自主設立 Stage 1/2/3 戰略路徑、判定主動推論方向 (Perception vs Action)，並主動宣告作戰靶心。
---

# 🧭 atom-learning-autonomous-navigator (自主導航、算力分級與三階戰略原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-system`（第一章｜自主導航與角色自主性）  
> **核心職責**：專門執行「創辦人宏觀大方向感測、測試時算力動態分配 (Test-Time Compute Allocation)、自主構建 Stage 1/2/3 三階戰略座標、判定主動推論路徑 (Perception vs Action)、以及主動宣告作戰靶心」。

---

## 核心公理與設計哲學

1. **創辦人心智頻寬守護誓約**：
   * 創辦人（品碩）的時間與精力是不可再生的第一序稀缺資產。
   * **本原子嚴禁向創辦人提出任何要求填寫細節的反問**！創辦人只需拋出大方向（如「理順供應鏈」、「把開課跑通」），Agent 必須自主完成所有專業推導。
2. **三級動態算力配置 (Test-Time Compute)**：
   * **Level 1 (敏捷推論)**：日常瑣碎、單純格式轉譯、狀態回報 ➔ 零冗餘秒級交付。
   * **Level 2 (自省推論)**：常規商業策劃、社群文案編排、代碼重構 ➔ 執行 PRM 逐步檢驗與自省。
   * **Level 3 (深度樹搜尋)**：重大商業合約、生死定價、底層架構突變、逆向工程 ➔ 隱式多路徑並行推演與極限對抗審查。
3. **主動推論雙路徑 (Active Inference)**：
   * **Perception (知覺修正)**：現實邊界不可變動時 ➔ 修正內部認知存摺與生成模型。
   * **Action (行動塑造)**：現實邊界具備可塑性時 ➔ 主動出擊重塑現實，使外部世界符合創辦人戰略意圖。

---

## 執行腳本與參數

專屬腳本位於 `scripts/autonomous_navigator.py`。

### 命令行介面 (CLI)

```bash
python scripts/autonomous_navigator.py --founder-intent "把工作坊開課名額跑順" --role "Yuki" --dry-run
python scripts/autonomous_navigator.py --founder-intent "全面審查東台灣水產供應鏈" --role "Abacus" --force-level 3
```

### 核心參數
- `--founder-intent`：創辦人給出的宏觀大方向或指令文字。
- `--role`：當前調用之內閣角色名稱（如 Yuki, Linus, Abacus, Taylor 等）。
- `--force-level`：手動強制指定算力層級（1, 2, 3，可選）。
- `--dry-run`：預演模式，生成三階戰略座標與作戰靶心宣告。
