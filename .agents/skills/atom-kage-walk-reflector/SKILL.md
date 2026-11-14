---
name: atom-kage-walk-reflector
description: 首席特務兼生活管家影·漫遊返航自省與閉環進化原子 (Kage Post-Walk Reflection & Closed-Loop Evolver Protocol v1.0)。落實創辦人親授「或是撰寫新的技能加進去呢」法旨！專門負責在 Threads 社交漫遊（去逛逛）結束後自動接管：直連 Meta 官方 API 遙測前台真實成效、啟動 PRM 突觸真值天平對比假設、自動回寫客觀事實庫與信念年輪雙存摺、並自動調用規則庫代謝與輪次帳本憑證入帳，實現「出門逛一次街、心智進化一代」的零摩擦閉環！
role_key: kage
type: atomic_skill
parent_skill: bionic-learning-kage
version: v1.0
exit_code_verified: true
authorized_by: 陳品碩 (Pinshuo)
---

# 🛸 影之漫遊返航自省與閉環進化原子 (Kage Post-Walk Reflector)

> 👤 **原子使命**：落實創辦人（品碩）親定心法——**「去逛逛結束後，必須進行實質反饋與修正！」**  
> 本技能作為前線社交漫遊與後腦認知存摺的「神經突觸連接器」。當漫遊腳本執行完畢（發布新貼文、秒回友店）後，本技能立即自動接管，執行真實成效遙測、真值天平計算、兩本認知存摺自動刻印、以及規則庫代謝入帳，徹底解決過去「只出勤打卡、不反省進化」的斷點問題。

---

## 🏛️ 五階自省與閉環架構 (Five-Stage Closed-Loop Pipeline)

```mermaid
flowchart TD
    WalkDone["1. 接收前線漫遊訊號\n(latest_walk_v3_result.json 或最新發布 Post ID)"] --> Telemetry["2. 直連 Meta Threads API 遙測聽診\n(抓取帳號即時指標與前一篇貼文 Views / Likes / Replies / 轉化率)"]
    
    Telemetry --> Verifier["3. 啟動 PRM 突觸真值天平\n• 比對發文預期 vs 實際數據 (計算真實誤差)\n• 檢驗是否踩中廢話句型 (反 AI 塑料檢驗)\n• 評估停留時間與對話深度"]
    
    Verifier --> VaultWrite["4. 實質回寫認知存摺雙重奏\n• 存摺 01 (客觀事實庫): 追加物理硬數據、Post ID 與截圖存證\n• 存摺 02 (信念演化庫): 若有認知突破，自動刻印貝氏信念年輪"]
    
    VaultWrite --> LedgerTick["5. 規則代謝與輪次帳本入帳 (v6.1 零信任)\n• 調用 rule_store.py: 勝出規則轉正、失效規則啟動溶酶體自噬\n• 調用 cycle_ledger.py tick: 生成去時間戳 SHA-256 憑證入帳！"]
```

---

## 🧭 五部曲執行標準程序 (Standard Operating Procedure)

1. **第一步：讀取漫遊戰報**
   * 自動解析 `00-03-06_Threads_Meow_Hub/scripts/latest_walk_v3_result.json`。
   * 取得本次漫遊之發布貼文 ID、首回覆 ID、配圖路徑、以及回訪友店清單。
2. **第二步：官方遙測聽診**
   * 透過 Meta Graph API (`https://graph.threads.net/v1.0/`) 查詢當前帳號最新總數據（關注數、歷史總互動數）以及近 24 小時貼文的精確指標。
3. **第三步：突觸真值天平對比**
   * 計算本輪互動率 $\text{ER} = \frac{\text{Likes} + \text{Replies} + \text{Reposts}}{\text{Views}}$。
   * 比對歷史基準線，評估本次題材（貓咪反差、風土私房、老屋共生）之槓桿成效。
4. **第四步：雙存摺無鎖追加 (Append-Only)**
   * 自動在 `Office_of_the_Operative_Kage/01_Cognitive_Log/01_Experiences_and_Evidence.md` 注入最新一筆物理驗證實績。
   * 若發現新的有效經驗，同步在 `02_Belief_Evolution.md` 銘刻年輪。
5. **第五步：輪次帳本物理入帳**
   * 自動生成符合 v6.1 規範的漫遊憑證檔案 `kage_walk_reflect_evidence.json`。
   * 呼叫 `cycle_ledger.py tick` 物理推進輪次帳本，確保自進化的每一步皆可被密碼學與時間戳查驗！

---

## 🛠️ 命令列工具與調用方式 (CLI Usage)

```powershell
# 1. 漫遊結束後自動呼叫（完全自動模式）
python scripts/post_walk_reflector.py --auto

# 2. 演練模式（僅輸出診斷與反思，不實際寫入存摺）
python scripts/post_walk_reflector.py --dry-run

# 3. 指定 Post ID 進行深度回溯自省
python scripts/post_walk_reflector.py --post-id <THREADS_POST_ID>
```
