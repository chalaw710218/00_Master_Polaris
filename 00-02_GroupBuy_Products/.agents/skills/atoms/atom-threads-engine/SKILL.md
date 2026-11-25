---
name: atom-threads-engine
description: ⚡ 確定性 Meta Threads API 傳輸與長效通訊底座 (Deterministic Meta Threads Transmission Engine)。由 CTO 林納斯 (Linus) 監製，具備 Container 兩段式發布、指數退避重試 (Exponential Backoff)、WAL 離線待發隊列與故障安燈機制。
---

# ⚡ atom-threads-engine · 確定性 Meta Threads 傳輸底座

> **首長主政**：CTO 林納斯 (Linus)  
> **品質安燈**：首席品質長 戴明博士 (Dr. Deming)  
> **核心定位**：**高抗逆確定性通信原子微技能 (Deterministic Pipe Atom)**  

---

## 🎯 為什麼是「萬用管道原子」？
本技能將原本散落在各個技能裡的「發文與發留言 HTTP 請求」徹底抽離並做深做透：
1. **單一職責**：專注且僅專注於「將標準文字或圖片 payload，100% 確定性地送達 Meta Threads 伺服器並取回發布成果」。
2. **零業務邏輯干擾**：它不關心發文內容是店貓、管家還是促銷，只負責通信可靠性。
3. **極限抗逆 (Extreme Resilience)**：
   * 遇網路超時或 5xx 錯誤：自動觸發 3 次指數退避重試（2s, 4s, 8s + 隨機抖動）。
   * 遇 Access Token 失效或斷網：自動落盤至本機 `00-00_Offline_Queue/`，記錄 WAL 日誌，通知生活管家待命，保證零資料遺失（Exit Code 0 形式化保證）。

---

## 💻 物理調用介面 (CLI Interface)

```bash
# 模擬發文或正式發布
python scripts/threads_engine_deep.py --mode text --text "今天天氣真好" --dry-run
```
