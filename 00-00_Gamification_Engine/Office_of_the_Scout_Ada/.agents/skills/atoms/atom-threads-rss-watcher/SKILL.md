---
name: atom-threads-rss-watcher
description: 📡 Threads 友店公開增量巡邏哨兵原子微技能。專精以零封號風險之公開協定，無感巡邏台東在地友店或指定 Threads 帳號。比對本地 `sentinel_cache.json` 快取，精準過濾舊貼文，只萃取當前新鮮增量貼文交付下游使用。
---

# 📡 atom-threads-rss-watcher · Threads 友店公開增量巡邏哨兵

> **首長主政**：生活管家 影 (Kage) ✕ CTO 林納斯 (Linus)  
> **品質安燈**：首席品質長 戴明博士 (Dr. Deming)  
> **原屬解剖來源**：`threads-rss-sentinel` 【步驟 1~3：目標鎖定、嗅探提取、增量過濾】  
> **單一核心責任**：**台東在地友店/關鍵品牌公開貼文嗅探、快取比對與增量動態純淨萃取**  

---

## 🎯 為什麼將其獨立為專精原子？
社群巡邏最忌諱「每天人工重複點開每一家店」。
本原子剝離了文案創作與互動邏輯，**專精做好「最安靜、最省資源的街角哨兵」**：
1. **零封號風險**：採用公開端點與輕量讀取，不觸碰 Meta 私有封包防禦紅線。
2. **增量精確過濾**：維護本地快取 `data/sentinel_cache.json`，只要這篇貼文上次已經看過，立即跳過，絕不重複打擾。
3. **支援多名單切換**：可巡邏核心台東名單（草民、餓人、慢食等），亦可動態傳入指定帳號清單。

---

## 💻 物理調用介面 (CLI Interface)

```bash
# 預設巡邏核心友店 (支援 dry-run 與自訂帳號)
python .agents/skills/atoms/atom-threads-rss-watcher/scripts/rss_watcher.py --dry-run
```
