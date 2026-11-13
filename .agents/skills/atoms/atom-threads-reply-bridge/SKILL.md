---
name: atom-threads-reply-bridge
description: 🚀 Threads 首回覆點火與主頁導流原子微技能。專精在貼文發布後 1 分鐘內，由作者身分發表第一則公開款待留言。解決 Threads API 無法自動私訊的痛點，搶佔前 60 分鐘對話室熱度，建立低跳出率的主頁引流橋樑並掛載特務秒回警戒。
---

# 🚀 atom-threads-reply-bridge · 首回覆點火與主頁導流原子

> **首長主政**：生活管家 影 (Kage) ✕ 店貓 喵編 (Meow Editor)  
> **技術監製**：CTO 林納斯 (Linus)  
> **品質安燈**：首席品質長 戴明博士 (Dr. Deming)  
> **原屬解剖來源**：`threads-autonomous-walker` 【第四步點五：首回覆橋接】  
> **單一核心責任**：**貼文發布後 1 分鐘內自動發表公開首回覆，點火推薦演算法並建立個人檔案導流橋樑**  

---

## 🎯 為什麼將其獨立為專精原子？
貼文發布後的「前 60 分鐘」是演算法決定是否擴散推薦的黃金窗口。
本原子剝離了排版、爬蟲等前期作業，**專精且僅專注於「發布後的點火與導流」**：
1. **款待式首回覆**：以作者身分在留言區端出第二道私房細節（如完整散步地圖或貓咪花絮），自然引導讀者點進主頁查看。
2. **對話室熱度點火**：確保每篇貼文發出 60 秒內至少有 1 則留言互動，避免零回應冷場。
3. **特務警戒掛載**：生成警戒時間標籤（`alert_window_until`），通知系統在發布後一小時內維持極高敏銳度。

---

## 💻 物理調用介面 (CLI Interface)

```bash
# 針對剛發布的 post_id 生成並送出首回覆 (支援 dry-run)
python .agents/skills/atoms/atom-threads-reply-bridge/scripts/reply_bridge.py --post-id "th_12345" --role shadow --dry-run
```
