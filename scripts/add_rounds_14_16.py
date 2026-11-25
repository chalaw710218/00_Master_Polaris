import sys
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
sys.path.insert(0, str(HERE))

import bionic_knowledge_gate as bkg

TZ = timezone(timedelta(hours=8))

ITEMS = [
    {
        "round": 14,
        "topic": "勞動部「勞動契約認定指導原則」與檢核表從屬性要素",
        "title": "勞動部 勞動契約認定指導原則 人格從屬性經濟從屬性與組織從屬性具體判斷要素",
        "source": "勞動部公告 勞動契約認定指導原則（108/11/19）",
        "url": "https://www.mol.gov.tw/1607/1632/1640/12431/",
        "quote": "其中， ( 一 ) 人格從屬性，是從勞工的「工作時間」、「給付勞務方法」及「勞務地點」受到事業單位指揮或管制約束，「不能拒絕雇主指派的工作」、「勞工必須接受事業單位對其考核」、「必須遵守服務紀律及懲處」、「須親自提供勞務」及「不能以自己名義提供勞務」等 8 項要素進行判斷； ( 二 ) 經濟從屬性，是從「勞工不論工作有無成果，事業單位都會計給報酬」、「勞工無須負擔營業風險」、「勞工不須自行備置勞務設備」、「勞工僅能依事業單位訂立或片面變更之標準獲取報酬」、「勞工僅得透過事業單位提供勞務，不得與第三人私下交易」等 5 項要素進行判斷； ( 三 ) 組織從屬性，是從勞工須透過與其他人分工才能完成工作等；其他還包含勞工保險、薪資扣繳及相同勞務的勞工契約性質等參考事項。"
    },
    {
        "round": 15,
        "topic": "到藥局代領已調劑之慢箋藥品法規依據",
        "title": "全民健康保險醫療辦法 第15條 保險對象持處方箋應在特約院所或特約藥局調劑",
        "source": "全民健康保險醫療辦法 第15條",
        "url": "https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=L0060009&flno=15",
        "quote": "保險對象持特約醫院、診所醫師交付之處方箋，應在該特約醫院、診所或至特約藥局調劑。"
    },
    {
        "round": 16,
        "topic": "交通部與郵政法對運送業者代為交寄信件之限制",
        "title": "郵政法 第6條 運送業者除附送與貨物有關之通知外不得為前項文件之遞送",
        "source": "郵政法 第6條",
        "url": "https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=K0050001&flno=6",
        "quote": "運送業者，除附送與貨物有關之通知外，不得為前項文件之遞送。"
    }
]

def main():
    ledger_path = WORKSPACE / "00-00_Gamification_Engine" / "Office_of_the_CIO_Falcon" / "01_Cognitive_Log" / "learning_ledger.jsonl"
    results = []

    for item in ITEMS:
        r = item["round"]
        started = datetime.now(TZ).isoformat()
        print(f"\n--- 執行第 {r} 輪 add: {item['title'][:30]}... ---")
        ok, msg = bkg.cmd_add(item["title"], item["url"], item["quote"], item["source"])
        ended = datetime.now(TZ).isoformat()
        print(f"結果: ok={ok}, msg={msg}")
        
        add_ok = 1 if ok else 0
        add_rejected = 0 if ok else 1
        
        # 寫入 ledger
        ledger_entry = {
            "round": r,
            "topic": item["topic"],
            "started": started,
            "ended": ended,
            "add_ok": add_ok,
            "add_rejected": add_rejected
        }
        with open(ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(ledger_entry, ensure_ascii=False) + "\n")
        print(f"Ledger 已更新第 {r} 輪")
        results.append((item, ok, msg))

    print("\n=== 全部 3 輪新增完畢 ===")

if __name__ == "__main__":
    main()
