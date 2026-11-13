---
name: atom-threads-tree-watcher
description: 🌳 Threads 留言樹遍歷與會話監控原子微技能。由 CTO 林納斯監製。專精遞歸解析 Meta Threads 官方 `/{media-id}/conversation` 留言樹，自動排除官方自帳發言、比對本地已回覆庫，精準萃取未讀待回覆訪客清單，提供上游決策模組使用。
---

# 🌳 atom-threads-tree-watcher · Threads 留言樹遍歷與會話監控原子

> **首長主政**：CTO 林納斯 (Linus)  
> **品質安燈**：首席品質長 戴明博士 (Dr. Deming)  
> **原屬解剖來源**：`threads-publisher` 【模式 B：留言巡邏】  
> **單一核心責任**：**Meta 官方 API conversation 樹狀留言遞歸解析、自帳物理過濾與未讀清單萃取**  

---

## 🎯 為什麼將其獨立為專精原子？
Threads 的留言結構不是平面的，而是具有多層巢狀（Nested Reply Tree）。
原本的腳本往往只能抓第一層，或把自己的回覆也誤當成訪客新留言。
本原子剝離所有文案生成與發布邏輯，**專注做好「樹狀留言的清道夫與過濾器」**：
1. **多層遞歸解析**：遍歷最新貼文的所有子節點留言，確保無遺漏。
2. **自帳硬性防呆過濾**：設定自帳黑名單（如 `hellotaitung`, `official_butler`），只要留言者是自己，立即過濾，100% 杜絕機器人與自己聊天的死循環。
3. **未讀純淨萃取**：自動比對已回覆記憶庫，只將「真正尚未被照顧到的讀者留言」打包成結構化待辦隊列。

---

## 💻 物理調用介面 (CLI Interface)

```bash
# 掃描指定或最新貼文的留言樹 (支援 dry-run)
python .agents/skills/atoms/atom-threads-tree-watcher/scripts/tree_watcher.py --post-id "th_12345" --dry-run
```
