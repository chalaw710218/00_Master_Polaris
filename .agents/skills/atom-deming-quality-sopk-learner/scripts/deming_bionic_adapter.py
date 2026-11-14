"""戴明 (Deming) 專屬仿生特化轉接器 (Role-Specific Adapter)
職責：執行戴明的品質防呆盤點，依零缺陷基準提名合規標準，輸出標準 JSON 供萬用母版 bionic_core 驗算。
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
    learn_script = SCRIPT_DIR / "deming_real_learning.py"
    hist_file = SKILL_DIR / "vaults" / "deming_quality_history.jsonl"
    if not hist_file.exists() and learn_script.exists():
        res = subprocess.run([sys.executable, str(learn_script), "--audit"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
        if res.returncode != 0:
            sys.stderr.write(res.stderr or res.stdout)
            sys.exit(1)
    if not hist_file.exists():
        sys.stderr.write(f"找不到戴明品質存摺：{hist_file}\n")
        sys.exit(1)

    proposals = [{
        "kind": "baseline_standard",
        "pattern": "defects:0",
        "scope": "any",
        "risk": "low",
        "source_url": str(hist_file),
        "tier": "A",
        "evidence": "全域原子腳本語法編譯與 --help 測試缺陷數上限為 0（合規基準標準）",
        "confidence": 0.95,
    }]
    out = {
        "office": "deming",
        "meta": {"state_file": str(hist_file)},
        "proposals": proposals,
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
