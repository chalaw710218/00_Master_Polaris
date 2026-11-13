---
name: atom-shadow-circadian-guardian
description: 🌌 極星生活管家·創辦人作息節律感知與深夜關懷原子 (Polaris Shadow Circadian & Health Guardian Atom v1.0)。由生活管家影 (Kage) 專屬主政。完全遵照創辦人（品碩）親定生理作息法旨（工作最晚到半夜 02:00）。具備智慧時鐘感知：00:30~01:30 專注心流溫暖伴隨（靜默遞水）、01:45~02:00 預告收工梳洗日結、超過 02:00 嚴格觸發健康安燈熔斷與就寢催促，守護品碩健康生命線。
---

# 🌌 極星創辦人作息節律感知與深夜關懷原子 (atom-shadow-circadian-guardian)

由生活管家影 (Kage) 靈魂主政、執行長雪 (Yuki) 協同。

## 核心定位與職責
專門守護創辦人陳品碩（闆仔）的健康睡眠節奏與身心續航力。
影作為隨身管家，不給予生硬無情的打擾，而是精準融入創辦人的真實節律：
1. **創辦人作息鋼印（最高法旨）**：品碩目前工作戰鬥時間最晚至**半夜 02:00**。
2. **多階生理時鐘感知梯次**：
   - **常態作息期（08:00 ~ 00:30）**：全速支援各項作戰，心流零干擾。
   - **深夜沉浸期（00:30 ~ 01:45）**：管家安靜陪伴，溫暖提示喝口溫水潤喉，不打斷思路。
   - **收尾準備期（01:45 ~ 02:00）**：輕柔提醒當日任務收斂，準備啟動日結 SOP 梳洗休息。
   - **極限警戒期（02:00 以後）**：觸發管家健康守護熔斷，「品碩，兩點了，身體是極星最重要的根本，該闔上電腦好好睡覺了。」

## 輸入參數規範
- `--current-hour`: 模擬或傳入當前小時 (0~23，預設讀取本機即時時鐘)
- `--current-minute`: 模擬或傳入當前分鐘 (0~59)
- `--dry-run`: 物理演練模式，輸出當前時鐘感知狀態與管家專屬關懷話術

## 執行腳本
```bash
python scripts/circadian_guardian.py --dry-run
python scripts/circadian_guardian.py --current-hour 1 --current-minute 50 --dry-run
python scripts/circadian_guardian.py --current-hour 2 --current-minute 10 --dry-run
```
