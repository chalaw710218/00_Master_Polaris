"""
run_learn_cycle.py — 生活管家影正規學習入庫推進器 (Learning Cycle Runner)
遵循母版 v6.5 與生活管家免簽門禁規範：
1. 讀取 data/_待入庫.md 中的學習條目。
2. 呼叫 bionic_knowledge_gate.py prepare 執行線上逐字比對與防呆檢驗。
3. 通過後自動追加寫入 data/fact_bank.md。
4. 記錄真實學習輪次入 kage_cycles.jsonl。
5. 觸發 run_gate_tests.py 確保全域回歸測試持續 PASS！
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

HERE = Path(__file__).resolve().parent
HUB_DIR = HERE.parent
DATA_DIR = HUB_DIR / "data"
PENDING_FILE = DATA_DIR / "_待入庫.md"
FACT_BANK_FILE = DATA_DIR / "fact_bank.md"
LOGS_DIR = HUB_DIR / "logs"
CYCLES_LOG = HUB_DIR.parents[1] / ".agents" / "skills" / "bionic-learning-system" / "bionic_core" / "vaults" / "kage_cycles.jsonl"

from bionic_knowledge_gate import prepare_cmd

def run_learning_cycle():
    print("=== 生活管家影正規仿生學習閉環開始 ===")
    if not PENDING_FILE.exists():
        print(f"❌ 找不到待入庫檔案：{PENDING_FILE}")
        return False

    content = PENDING_FILE.read_text(encoding="utf-8").strip()
    if not content:
        print(f"ℹ️ 待入庫檔案為空，無新學習條目需要處理。")
        return True

    print(f"正在對 {PENDING_FILE} 執行門禁線上檢驗與直接入庫...")
    passed_cnt, rejected_cnt, rejected_list = prepare_cmd(
        pending_path=PENDING_FILE,
        vault_path=FACT_BANK_FILE,
        is_baseline=False
    )

    if rejected_cnt > 0:
        print(f"\n❌ [安燈阻斷] 存在未通過門禁之條目（退回 {rejected_cnt} 條），學習暫停！")
        for title, reason in rejected_list:
            print(f"  👉 「{title}」: {reason}")
        return False

    if passed_cnt == 0:
        print("❌ 未入庫任何新條目。")
        return False

    print(f"\n🎉 學習入庫成功！共 {passed_cnt} 條真實事實寫入正式事實庫。")

    # 記錄入學習輪次帳本 (kage_cycles.jsonl)
    CYCLES_LOG.parent.mkdir(parents=True, exist_ok=True)
    cycle_record = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "type": "learning_cycle",
        "role": "kage",
        "passed_count": passed_cnt,
        "vault": str(FACT_BANK_FILE),
        "summary": f"完成正規知識學習入庫，通過 {passed_cnt} 條客觀事實"
    }
    with open(CYCLES_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(cycle_record, ensure_ascii=False) + "\n")
    print(f"✅ 學習輪次已刻印至：{CYCLES_LOG}")

    # 清空 _待入庫.md
    PENDING_FILE.write_text("", encoding="utf-8")
    print(f"✅ 已清空 {PENDING_FILE}")

    # 自動跑回歸測試
    print("\n🔍 正在執行全域回歸測試以確保門禁無損...")
    from tests.run_gate_tests import main as run_tests
    try:
        run_tests()
    except SystemExit as e:
        if e.code != 0:
            print("❌ 回歸測試失敗！")
            return False

    return True

if __name__ == "__main__":
    success = run_learning_cycle()
    sys.exit(0 if success else 1)
