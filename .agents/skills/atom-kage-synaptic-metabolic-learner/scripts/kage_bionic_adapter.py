"""影 (Kage) 專屬仿生特化轉接器 (Role-Specific Adapter)
職責：執行影的突觸學習腳本，根據影的專長（Threads 開頭鉤子停留率與互動率）提名候選規則，輸出標準 JSON 供萬用母版 bionic_core 驗算。
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent


def main() -> None:
    learn_script = SCRIPT_DIR / "kage_real_learning.py"
    state_file = SKILL_DIR / "vaults" / "kage_synaptic_state.json"
    if learn_script.exists():
        res = subprocess.run([sys.executable, str(learn_script), "--learn"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        if res.returncode != 0:
            sys.stderr.write(res.stderr or res.stdout)
            sys.exit(1)
    if not state_file.exists():
        sys.stderr.write(f"找不到狀態檔：{state_file}\n")
        sys.exit(1)

    data = json.loads(state_file.read_text(encoding="utf-8"))
    median_er = float(data.get("account_median_er", 2.0))
    proposals = []
    for hook, stat in data.get("hook_weights", {}).items():
        if stat.get("confidence") != "OK":
            continue
        avg_er = float(stat.get("avg_er", 0.0))
        n = int(stat.get("n", 0))
        dyn_conf = min(0.95, round(0.50 + n * 0.05, 2))
        if avg_er < median_er * 0.7:
            proposals.append({
                "kind": "forbid_phrase",
                "pattern": hook,
                "scope": "prefix",
                "risk": "low",
                "source_url": str(data.get("source", "insights_history.jsonl")),
                "tier": "A",
                "evidence": f"真實 Threads 快照 N={n}，開頭『{hook}』平均 ER={avg_er}% < 帳號中位數 {median_er}%*0.7",
                "confidence": dyn_conf,
            })
        elif avg_er >= median_er * 1.3:
            proposals.append({
                "kind": "prefer_phrase",
                "pattern": hook,
                "scope": "prefix",
                "risk": "low",
                "source_url": str(data.get("source", "insights_history.jsonl")),
                "tier": "A",
                "evidence": f"真實 Threads 快照 N={n}，開頭『{hook}』平均 ER={avg_er}% >= 帳號中位數 {median_er}%*1.3",
                "confidence": dyn_conf,
            })

    out = {
        "office": "kage",
        "meta": {"state_file": str(state_file), "learned_at": data.get("learned_at"), "median_er": median_er},
        "proposals": proposals,
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
