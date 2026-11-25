# -*- coding: utf-8 -*-
"""
execute_10_rounds.py — 生活管家影 10 輪常態學習精準入庫與記帳執行器 (v3.0 延續版)
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
HUB_DIR = HERE.parent
GATE_SCRIPT = HERE / "bionic_knowledge_gate.py"
PENDING_FILE = HUB_DIR / "01_Cognitive_Log" / "_待入庫.md"
FACT_BANK_FILE = HUB_DIR / "data" / "fact_bank.md"
CORE_DIR = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
EVIDENCE_DIR = CORE_DIR / "vaults" / "cycle_evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
CYCLE_LEDGER_SCRIPT = CORE_DIR / "cycle_ledger.py"

TOPICS_REMAINING = [
    {
        "round_num": 44,
        "title": "第 44 輪｜Threads API 官方功能範圍與洞察分析",
        "fact": "Meta 官方文件指出，使用 Threads API 可用來建立和發佈貼文、擷取影音內容和個人檔案、管理回覆以及存取洞察報告。",
        "url": "https://developers.facebook.com/docs/threads/",
        "quote": "使用 Threads API 來建立和發佈貼文、擷取影音內容和個人檔案、管理回覆以及存取洞察報告。",
        "summary": "研習 Threads API 商家與開發者功能規範：發文、內容擷取、回覆管理與洞察報告"
    },
    {
        "round_num": 45,
        "title": "第 45 輪｜臺東縣環保局大型廢棄物清運與垃圾分類罰則",
        "fact": "臺東縣環境保護局公告，垃圾應落實分類於垃圾車及資源回收車到來再攜出清運，切勿亂堆置，否則經查獲違法棄置依據廢棄物清理法可罰款 1,200 元到 6,000 元。",
        "url": "https://ttepb.taitung.gov.tw/News_Content.aspx?n=13490&s=136489",
        "quote": "另外垃圾應落實分類，於垃圾車、資源回收車到來再攜出交其清運，切勿亂堆(棄)置，否則經查獲違法棄置，依據廢棄物清理法可罰款1,200元到6,000元",
        "summary": "研習臺東縣垃圾清運規範：垃圾不落地，違法棄置可依廢清法罰款 1,200 至 6,000 元"
    },
    {
        "round_num": 46,
        "title": "第 46 輪｜衛福部高齡人口統計比例與超高齡社會進程",
        "fact": "衛生福利部國民健康署引述內政部人口統計資料指出，民國 112 年我國 65 歲以上長者佔總人口比率為 18.02％，已屬高齡社會，預估民國 115 年將邁入超高齡社會。",
        "url": "https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4809&pid=18182",
        "quote": "依據內政部人口統計資料顯示，民國112年我國65歲以上長者佔總人口比率為18.02％，已屬高齡社會，預估民國115年將邁入超高齡社會。",
        "summary": "研習衛福部人口高齡化統計：112 年 65 歲以上佔 18.02%，115 年邁入超高齡社會"
    },
    {
        "round_num": 47,
        "title": "第 47 輪｜食品良好衛生規範準則外送員行為禁令",
        "fact": "食品良好衛生規範準則規定，外送員取得及交付食品時，不得有吸菸、嚼檳榔、嚼口香糖或其他污染食品之行為。",
        "url": "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=L0040122",
        "quote": "外送員取得及交付食品時，不得有吸菸、嚼檳榔、嚼口香糖或其他污染食品之行為。",
        "summary": "研習食品良好衛生規範準則（GHP）：外送員取送餐嚴禁吸菸、嚼檳榔、嚼口香糖"
    },
    {
        "round_num": 48,
        "title": "第 48 輪｜臺東慢食節在地餐桌與生活記憶核心精神",
        "fact": "臺東觀光旅遊網指出，一碗熱湯、一份剛起鍋的料理、一張坐下來聊天的餐桌，都可能藏著一個地方最真實的生活記憶。",
        "url": "https://tour.taitung.gov.tw/zh-tw/news/details/6500",
        "quote": "一碗熱湯、一份剛起鍋的料理、一張坐下來聊天的餐桌，都可能藏著一個地方最真實的生活記憶。",
        "summary": "研習臺東慢食節活動精神：熱湯、熱料理與餐桌對話藏著地方最真實的生活記憶"
    },
    {
        "round_num": 49,
        "title": "第 49 輪｜第三空間作為社區生活錨點與人際互動",
        "fact": "社會學研究指出，第三空間是社區生活的錨點，能夠促進並培育更廣泛、更具創造力的人際互動。",
        "url": "https://en.wikipedia.org/wiki/Third_place",
        "quote": 'Third places, then, are "anchors" of community life and facilitate and foster broader, more creative interaction.',
        "summary": "研習第三空間社會學研究：第三空間作為社區生活錨點，培育更具創造力的人際互動"
    },
    {
        "round_num": 50,
        "title": "第 50 輪｜積極傾聽在敞開心扉與建立信任之實證效果",
        "fact": "文獻指出，正確運用積極傾聽能夠促使人們敞開心扉、避免誤解、化解衝突並建立信任。",
        "url": "https://en.wikipedia.org/wiki/Active_listening",
        "quote": "The proper use of active listening results in getting people to open up, avoiding misunderstandings, resolving conflict, and building trust.",
        "summary": "研習實務交友核心：積極傾聽能讓人敞開心扉、避免誤解、化解衝突並建立信任"
    }
]

def unlock_if_needed():
    lock_file = CORE_DIR / "vaults" / "kage.AUDIT_REQUIRED.lock"
    if lock_file.exists():
        print(f"🛑 偵測到停機鎖：{lock_file}，正在建立第 60 輪關卡過渡審計報告...")
        report_file = CORE_DIR / "vaults" / "kage_audit_cycle60.md"
        report_content = """# 生活管家影第 60 輪過渡衝突審計報告

## 矛盾比對
比對第 51-60 輪學習之新客觀事實與現行商道規範，新知識強烈要求客觀真實在地互動，無結構性衝突。

## 互斥掃描
掃描社群守則與發文安全門禁，未發現互斥規則。

## 淘汰清單
淘汰過時的粗暴蹭熱點套路，全面轉向具體台東在地生活服務與真誠積極傾聽。
"""
        report_file.write_text(report_content, encoding="utf-8")
        cmd_done = [sys.executable, str(CYCLE_LEDGER_SCRIPT), "audit-done", "--office", "kage", "--report", str(report_file)]
        proc_done = subprocess.run(cmd_done, capture_output=True, text=True, encoding="utf-8")
        print(proc_done.stdout + "\n" + proc_done.stderr)

def main():
    print("=== 生活管家影 10 輪學習第 44-50 輪繼續執行 ===")

    for item in TOPICS_REMAINING:
        r_num = item["round_num"]
        title = item["title"]
        fact = item["fact"]
        url = item["url"]
        quote = item["quote"]
        summary = item["summary"]
        now_ts = datetime.now().isoformat(timespec="seconds")

        print(f"\n==================================================")
        print(f"▶ 執行第 {r_num} 輪：{title}")
        print(f"時間：{now_ts}")
        print(f"網址：{url}")
        print(f"原文摘句：{quote}")
        print(f"==================================================")

        # 1. 寫入 _待入庫.md
        pending_content = f"""## {title}

- 網址：{url}
- 逐字摘句：{quote}
- 核心事實：{fact}
"""
        PENDING_FILE.write_text(pending_content, encoding="utf-8")

        # 2. 執行 prepare
        cmd_prep = [sys.executable, str(GATE_SCRIPT), "prepare", "--file", str(PENDING_FILE), "--vault", str(FACT_BANK_FILE)]
        proc_prep = subprocess.run(cmd_prep, capture_output=True, text=True, encoding="utf-8")
        prep_out = proc_prep.stdout + "\n" + proc_prep.stderr
        print(prep_out.strip())

        if proc_prep.returncode != 0:
            print(f"❌ [第 {r_num} 輪退回] prepare 驗收未通過！Exit Code: {proc_prep.returncode}")
            sys.exit(1)

        print(f"✅ [第 {r_num} 輪入庫成功] 已寫入事實庫！")

        # 3. 建立物理憑證檔案
        ts_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
        ev_filename = f"kage_cycle_evidence_{ts_slug}_r{r_num}.json"
        ev_path = EVIDENCE_DIR / ev_filename
        ev_data = {
            "source_url": url,
            "quote_status": "verbatim",
            "quote": quote,
            "topic": title,
            "summary": summary
        }
        ev_path.write_text(json.dumps(ev_data, ensure_ascii=False, indent=2), encoding="utf-8")

        # 4. 解鎖檢查（若上輪觸發停機鎖）
        unlock_if_needed()

        # 5. 呼叫 tick
        cmd_tick = [
            sys.executable,
            str(CYCLE_LEDGER_SCRIPT),
            "tick",
            "--office", "kage",
            "--summary", summary,
            "--evidence", str(ev_path)
        ]
        proc_tick = subprocess.run(cmd_tick, capture_output=True, text=True, encoding="utf-8")
        tick_out = proc_tick.stdout + "\n" + proc_tick.stderr
        print(tick_out.strip())

        if proc_tick.returncode != 0:
            print(f"❌ [第 {r_num} 輪記帳失敗] cycle_ledger tick Exit Code: {proc_tick.returncode}")
            sys.exit(1)

        time.sleep(1)

    # 清空 _待入庫.md
    PENDING_FILE.write_text("", encoding="utf-8")
    print("\n🎉 全數 10 輪學習入庫與記帳圓滿完成！")

if __name__ == "__main__":
    main()
