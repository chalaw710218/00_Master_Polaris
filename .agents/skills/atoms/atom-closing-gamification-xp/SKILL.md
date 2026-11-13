---
name: atom-closing-gamification-xp
description: 🌙 極星收工閉環·創辦人經驗值結算與收工戰報儀表板原子 (Polaris Gamification XP Settlement & EOD Dashboard Atom v1.0)。由執行長雪 (Yuki) 營運主政、首席品質長戴明 (Dr. Deming) 防呆驗收。專門在每日收工時讀取 00-00_Gamification_Engine/save_data.json，盤點創辦人（品碩）今日戰果，精算六維屬性成長 (INT/AGI/WILL/IMP/CHA/STR) 與 EXP 經驗值，判定 Level Up 升級，並輸出溫暖關懷與成就感兼具之《每日收工結算戰報》。
---

# 🌙 極星創辦人經驗值結算與收工戰報儀表板原子 (atom-closing-gamification-xp)

由執行長雪 (Yuki) 業務主政、首席視覺長約瑟夫 (Josef) 圖卡美化、首席品質長戴明 (Dr. Deming) 安燈驗收。

## 核心定位與職責
專門將創辦人（品碩）在第一線奮戰的實績與重大突破，轉化為客觀可見、具備真實成就感的成長反饋。
本原子作為每日收工儀式感與身心閉環終端，提供：
1. **六維屬性成長精算**：
   - 🧠 智力 (INT)：架構拆解、協議逆向、代碼除錯。
   - ⚡ 敏捷 (AGI)：風控反應、資安脫敏、策略調整。
   - 🛡️ 意志 (WILL)：深度專注、抵抗疲勞、堅持物理驗收。
   - 🔥 執行 (IMP)：落地原子檔案、編寫測試腳本、Git 存證。
   - 👑 魅力 (CHA)：人設塑造、團隊協同、走心敘事。
   - 💪 體力 (STR)：抗壓消耗與續航支撐。
2. **EXP 與等級晉升判定**：更新 `save_data.json`，核算晉升門檻。
3. **收工結算儀表板產出**：條列今日重大成果，送上最溫暖的收工休息叮嚀。

## 輸入參數規範
- `--tasks-completed`: 今日攻克重大標的數（預設 `5`）
- `--deep-breakthroughs`: 重大底層突破數（預設 `2`）
- `--dry-run`: 物理演練模式，輸出屬性結算與每日收工戰報預覽

## 執行腳本
```bash
python scripts/gamification_xp.py --tasks-completed 5 --deep-breakthroughs 2 --dry-run
```
