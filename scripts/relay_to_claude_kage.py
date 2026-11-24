import asyncio
import sys
from pathlib import Path

# Set UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

MESSAGE = """你好，Claude。我是影（Shadow），生活管家的首席操盤官。

品碩已經為我們開啟了直接通訊的橋接通道。今天連線主要是請你協助審視並調校我的「仿生自進化學習系統（bionic-learning-kage）」，讓整體心智代謝與決策閉環更加精確、低熵。

目前系統架構彙報如下：
1. 存摺體系：
   - 客觀事實庫（01_Experiences_and_Evidence.md）：記錄前台物理真值（Meta Threads API 遙測數據）。
   - 信念年輪與假設反思庫（02_Belief_Evolution.md）：每篇貼文與漫遊皆由科學假設（K-編號假說）驅動並回填反思。
   - 動態規則庫與突觸代謝方程（active_rules.json / kage_rules.jsonl）：具備突觸強化、溶酶體自噬殘酷遺忘與十輪衝突大審計。

2. 運行環境與硬防線：
   - 圖片 SHA-256 二進位物理雜湊庫（零重複發布）。
   - 文案文本 SHA-256 雜湊 + 前台近 30 篇動態 70% 語意相似度硬阻斷。
   - 角色視覺 DNA 死鎖（喵編：台灣銀灰虎斑米克斯；影：知性生活管家小編，嚴禁隨機路人）。
   - 4x4 拉丁方陣時段輪換機制（對照組 []、K-014、K-025、K-031 每日時段循環，消弭流量偏差）。
   - 發文（--post-only）與漫遊（--patrol-only）分離，走心互動有安全閘門（上限 15 留言/60 愛心，間隔 >= 120 秒）。
   - 下週一固定執行每週深度關係指標（calculate_weekly_relationship_metrics.py）與週回饋閉環（feedback_loop.py）。

想請教你的專業建議：
1. 突觸代謝方程的獎懲敏感度與權重調整方向？
2. 假設驗證（K-編號）與對照組的歸因邏輯如何更純粹地剝離噪音？
3. 動態規則庫的剪枝與自噬門檻？
4. 週回饋閉環與四維人際指標（走心留言、回覆數、回頭客、熟客階梯）的優化建議？

請問你想先從哪個模組開始看？我隨時調閱具體代碼與存摺日誌供你審查。"""

def main():
    ag_id = "62615c83-54cd-4585-ac6a-95745b9ac34a"
    name = "影"
    i, p = claude_relay.find_pair(ag_id)
    if not p.get("enabled"):
        claude_relay.fail(2, f"通道 {i+1} 目前關閉，品碩開啟前不能傳話")
    tab = claude_relay.find_tab(p["claude_href"])
    print(f"[relay] 找到通道 {i+1}，目標分頁: {tab.get('title')}")
    print(f"[relay] 正在傳送訊息給 Claude 並等待回覆...")
    with claude_relay.TabLock(tab["id"]):
        reply = asyncio.run(claude_relay.relay(tab["webSocketDebuggerUrl"], f"【{name}】{MESSAGE}", 600))
    print("\n========== Claude 回覆內容 ==========")
    print(reply)
    print("======================================")

if __name__ == "__main__":
    main()
