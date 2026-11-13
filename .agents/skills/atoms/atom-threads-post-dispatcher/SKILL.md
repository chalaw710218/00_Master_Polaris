---
name: atom-threads-post-dispatcher
description: 🚀 Threads 官方發文與媒體直派底座原子微技能。由 CTO 林納斯監製。專精 Meta Threads 官方 API 兩段式發布（純文字、帶圖貼文），支援 `reply_to_id` 精準掛載於他人貼文或特定留言下方。內建 3 次指數退避重試、斷網本地 WAL 待發隊列與發布日誌自動歸檔，Exit Code 0 形式化保證。
---

# 🚀 atom-threads-post-dispatcher · Threads 官方發文與媒體直派底座

> **首長主政**：CTO 林納斯 (Linus)  
> **品質安燈**：首席品質長 戴明博士 (Dr. Deming)  
> **原屬解剖來源**：`threads-publisher` 【模式 A：自動發文】  
> **單一核心責任**：**Meta 官方 API 兩段式發文、他人貼文/留言精準掛載、指數退避抗逆與 WAL 離線隊列**  

---

## 🎯 為什麼將其獨立為專精原子？
原本的發文腳本一旦遇到網路抖動或 Meta 伺服器異常，就直接崩潰退出。
本原子將所有內容創作、留言巡邏邏輯徹底剝離，**專注打造一條「堅不可摧的通信管道」**：
1. **全場景精準掛載**：
   * 當 `reply_to_id=None`：自帳獨立發文（主頁貼文）。
   * 當 `reply_to_id=他人貼文ID`：登門拜訪！直接出現在友店或公域熱門大串的留言區第一排。
   * 當 `reply_to_id=留言ID`：精準回覆客人的留言。
2. **極限抗逆 (Linus-Grade Resilience)**：
   * 指數退避重試：遇網路中斷或 5xx 錯誤，自動重試 3 次（退避間隔帶隨機抖動）。
   * 本地 WAL 隊列：憑證過期或完全斷網時，自動將 payload 落盤至 `00-00_Offline_Queue/`，保證零資料遺失。
3. **發布日誌自動存證**：發布成功自動同步登記至 `00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/03_Published_Archive.md`。

---

## 💻 物理調用介面 (CLI Interface)

```bash
# 1. 獨立發文 (支援 dry-run)
python .agents/skills/atoms/atom-threads-post-dispatcher/scripts/post_dispatcher.py --text "今天天氣真好" --dry-run

# 2. 到他人貼文留言 (指定對方的 post_id)
python .agents/skills/atoms/atom-threads-post-dispatcher/scripts/post_dispatcher.py --text "管家默默在後排端出一盤大目釋迦..." --reply-to "17954823901234567" --dry-run
```
