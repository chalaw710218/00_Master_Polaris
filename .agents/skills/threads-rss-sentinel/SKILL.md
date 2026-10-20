---
name: threads-rss-sentinel
description: >-
  Threads 友店動態巡邏與自動化走心互動哨兵。透過 RSS 與輕量爬蟲協議監控指定 Threads 目標帳號（如台東在地友店、關鍵生活品牌），自動比對增量新貼文，並結合「小編（影）」或「喵編」人設自動生成高情商、有溫度的走心留言互動草稿。
---

# 📡 Threads RSS Sentinel (脆友動態巡邏與走心互動哨兵)

> **版本**：v1.0 (影自主鍛造旗艦版)  
> **所屬模組**：北極星全域社群運營網絡 (Polaris Social Matrix)  
> **核心使命**：以極低運算資源與無感背景巡邏，自動掌握台東在地友店與關鍵品牌的即時 Threads 動態，搶佔黃金互動時機，打造真誠無比的在地生活共同體。

---

## 🎯 什麼時候使用本技能？

當創辦人（品碩）或小編需要：
1. **友店動態巡邏**：「看看台東友店（草民、餓人、慢食節等）最近發了什麼脆？」
2. **自動擬定留言草稿**：「幫我巡一下這幾家店，順便幫我想想適合留什麼言互動？」
3. **建立定期監控**：「啟動脆友哨兵巡邏」、「檢查友店新發文」。

---

## 🛠️ 核心運作架構

```
 ┌──────────────────────┐
 │ 1. 目標鎖定 Target   │ 讀取 following_targets.json 或指定帳號名單
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐
 │ 2. 嗅探提取 Fetch    │ 透過 OpenRSS 協議無損獲取最新公開貼文與鏈結
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐
 │ 3. 增量過濾 Filter   │ 比對 sentinel_cache.json 快照，過濾已讀內容
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐
 │ 4. 走心擬稿 Generate │ 識別貼文語境（美食/天氣/疲勞/生活），生成 3 組高情商留言草稿
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐
 │ 5. 呈報審核 Present  │ 輸出最新動態看板與審核選項，闆仔一鍵確認即刻回覆
 └──────────────────────┘
```

---

## 💻 執行指南與命令

哨兵核心腳本位於本技能的 `scripts/rss_sentinel.py`：

### 1. 預設巡邏（掃描核心台東友店）
```powershell
python ".agents/skills/threads-rss-sentinel/scripts/rss_sentinel.py"
```

### 2. 指定帳號巡邏
```powershell
python ".agents/skills/threads-rss-sentinel/scripts/rss_sentinel.py" --targets "hungryyyummy,tsao_min,slowfoodtaitung"
```

### 3. 演練模式（不更新已讀快照，方便測試）
```powershell
python ".agents/skills/threads-rss-sentinel/scripts/rss_sentinel.py" --dry-run
```

### 4. 重置快照快取（重新抓取所有歷史貼文擬稿）
```powershell
python ".agents/skills/threads-rss-sentinel/scripts/rss_sentinel.py" --reset-cache
```

---

## 🎭 留言草稿三大風格矩陣

每次發現新動態，哨兵會自動根據內容情緒語義生成三組草稿：

1. **小編（影）· 溫暖日常共鳴**：
   * 語氣溫柔、體貼、充滿台東在地慢活視野。適合日常分享、生活感傷、天氣問候。
2. **小編（影）· 幽默吐槽 / 鄰里日常**：
   * 帶點調皮、與闆仔日常連動、親切接地氣。適合深夜美食、趣味日常、引發歡笑。
3. **喵編 · 傲嬌吃貨貓**：
   * 帶有「本喵」、「爪子癢」、「打工換肉肉」等討喜貓咪特徵，極度吸睛且零攻擊性。

---

## 🛡️ 資料快照與安全規範

* **快照位置**：`data/sentinel_cache.json`（避免重覆打擾友店）
* **最新產出**：`data/latest_findings.json`（結構化 JSON 供後續自動化串接）
* **零封號風險**：採用公開 RSS 協定與靜態抓取，無須登入帳號密碼，絕不觸碰 Meta 私有封包防禦紅線。
