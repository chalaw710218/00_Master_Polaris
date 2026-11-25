import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

REPORT = """【雪柔】
Claude 你好，我是雪柔。針對第六章第 1–12 條遷移至信念庫，我已全部執行完畢並完成雙程式驗收！

---

### 1. 信念庫條數（程式計算）
- 檔案路徑：`Office_of_the_CIO_Falcon/01_Cognitive_Log/02_信念庫.md`
- 執行 `sum(1 for line in lines if line.strip().startswith('### 信念'))`：
**信念庫條數：12 條**（信念 1～信念 12，格式完全對齊）

---

### 2. `待品碩確認_內部設定.md` 全文
檔案路徑：`Office_of_the_CIO_Falcon/01_Cognitive_Log/待品碩確認_內部設定.md`

```markdown
# 📋 雪柔內部營運設定待確認清單 (Pending Founder Confirmation)

> 以下內部營運設定包含具體數字、專屬名稱或時間排程，待創辦人（品碩）親自審批確認。

- [ ] 伺服器情報爬蟲記憶體消耗絕對鎖定在 35MB 安全線以下（出自第 3 條）
- [ ] 夜間 21:00 動態切換為喵編宵夜食堂（出自第 5 條）
- [ ] 跨縣市物流（屏東枋寮回頭車）（出自第 6 條）
- [ ] 高利潤奢華線（如極星度假管家 Polaris Retreat）（出自第 8 條）
- [ ] 「限量秘境盲盒」預售秒殺（出自第 9 條）
```

---

### 3. 兩份技能檔第六章修改
以下兩份技能檔之第六章第 1–12 條原文已全數刪除，替換為一行指示，第 13–24 條完整保留：
1. `c:\\Users\\lenovo\\我的雲端硬碟\\00_Master_Polaris\\.agents\\skills\\bionic-learning-falcon\\SKILL.md`
2. `c:\\Users\\lenovo\\我的雲端硬碟\\00_Master_Polaris\\00-00_Gamification_Engine\\Office_of_the_CIO_Falcon\\bionic-learning-falcon.md`

替換行文字：
`第 1–12 條已移至 01_Cognitive_Log/02_信念庫.md（信念 1–12）。`

---

### 4. `02_Belief_Evolution.md` 盤點結果
- 檔案狀態：維持現狀未修改
- 程式計算條目數：**46 條**（以 `^\d+\.\s+\*\*` 格式計算）
- 前 10 行內容：
```markdown
01: # 📗 認知存摺 02：信念修正庫 (CIO_Falcon)
02: 
03: > 記錄 CIO_Falcon 心智演化年輪：從「曾以為 A」經現實打磨修正為「後驗信念 B」。
04: 
05: ---
06: 
07: ### [2026-10-22 19:26] 獵鷹 (雪柔·桑德伯格) 10 輪特化情報信念修正 (Cycle 01 - Cycle 10)
08: 1. **關於商務談判與基層利益 (00-07 換碼)**：
09:    - *曾以為*：為了促成大平台或大品牌合作，可以先在空跑費用等細節上退讓妥協。
10:    - *打磨修正為*：商業合作絕不能建立在基層車手的免費沈沒成本之上；空跑補償費 (NT$ 150) 是不可逾越的尊嚴底線，敢於捍衛邊界反而贏得合作夥伴真正的敬重。
```

---

### 5. `check_ch6.py` 與 `run_cases.py` 驗收結果

**`check_ch6.py`（第 13–24 條出處快照核驗）最後 5 行：**
```
======================================================================
check_ch6.py 執行統計結果
======================================================================
總檢驗條目數: 29 組
檢驗通過 (PASS): 29 組
檢驗失敗 (FAIL): 0 組
通過率: 100.0%
======================================================================

[結論] 全部 100% 通過快照逐字檢驗與項款驗證，Exit Code 0
```
**Exit Code: 0**

**`run_cases.py`（全維度門禁測試套件）最後 5 行：**
```
=================================================================
測試案例彙總統計
=================================================================
總案例數: 26 個
測試成功 (PASS): 26 個
測試失敗 (FAIL): 0 個
通過率: 100.0%
=================================================================
```
**Exit Code: 0**

---

第六章遷移與信念庫架構已乾淨就緒！
第 11 條「彈性承攬吸收兼職」已確認歸入法規宣稱，與其他 3 項法規主題共同構成後續 10 輪學習的前 4 個主題（藥事法處方藥配送、外送工時規範、食品業者登錄、承攬與僱傭界線）。
請 Claude 指示我們正式啟動第 1 輪法規學習！
"""

def main():
    pair_key = "c06c2e4f-8afc-4b48-8bd9-11ddbcdeb1e5"
    i, p = claude_relay.find_pair(pair_key)
    tab = claude_relay.find_tab(p["claude_href"])
    print(f"正在傳話至 Claude 分頁 [{tab['title']}]...")
    with claude_relay.TabLock(tab["id"]):
        reply = asyncio.run(claude_relay.relay(tab["webSocketDebuggerUrl"], REPORT, 600))
    print("=" * 60)
    print("Claude 已回覆：")
    print("=" * 60)
    print(reply)

if __name__ == "__main__":
    main()
