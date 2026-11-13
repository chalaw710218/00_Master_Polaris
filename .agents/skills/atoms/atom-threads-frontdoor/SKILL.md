---
name: atom-threads-frontdoor
description: 🏠 Threads 客廳門禁與自帳新留言 100% 秒回原子微技能。由生活管家影 (Kage) 與店貓喵編掌舵。專精監控自帳最新貼文留言區，識別訪客意圖（讚美、提問、閒聊、辛勞），以極具溫度的雙主角人設秒回並贈送紅心，內建防重複回覆資料庫與戴明安燈質檢。
---

# 🏠 atom-threads-frontdoor · Threads 客廳門禁與自帳秒回原子

> **首長主政**：生活管家 影 (Kage) ✕ 店貓 喵編 (Meow Editor)  
> **技術監製**：CTO 林納斯 (Linus)  
> **品質安燈**：首席品質長 戴明博士 (Dr. Deming)  
> **原屬解剖來源**：`threads-autonomous-walker` 【第一步：看家門】  
> **單一核心責任**：**自帳貼文留言區 100% 監控、情緒識別與高情商走心秒回**  

---

## 🎯 為什麼將其獨立為專精原子？
自帳留言區是極星在 Threads 的「客廳防禦陣地」。
任何主動留言的讀者都是最寶貴的關係人口。
本原子剝離了發文、生圖與公域爬蟲等無關雜質，**專精且僅專注於「守護客廳」**：
1. **意圖深層識別**：將留言分為「辛勞傾訴」、「日常閒話」、「對產品好奇」、「純粹讚美」四大類。
2. **防重複回覆機制**：維護本地回覆庫 (`data/replied_comments_vault.json`)，絕不重複回覆同一個 comment_id。
3. **客廳溫度保障**：100% 去 AI 塑料感，絕不用「謝謝支持～」等罐頭字串，視來客情況由影遞茶或喵編傲嬌打招呼。

---

## 💻 物理調用介面 (CLI Interface)

```bash
# 巡邏並回覆自帳最新留言 (支援模擬 dry-run 與正式環境)
python .agents/skills/atoms/atom-threads-frontdoor/scripts/frontdoor_sentinel.py --dry-run
```
