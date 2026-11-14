"""約瑟夫 (Josef) 專屬仿生特化轉接器 (Role-Specific Adapter)
職責：執行約瑟夫的視覺光學對比度盤點腳本，依高齡視力友善標準提名合規基準，輸出標準 JSON 供萬用母版 bionic_core 驗算。
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
    learn_script = SCRIPT_DIR / "josef_real_learning.py"
    hist_file = SKILL_DIR / "vaults" / "josef_contrast_history.jsonl"
    if learn_script.exists():
        res = subprocess.run([sys.executable, str(learn_script), "--audit-palette"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        if res.returncode != 0:
            sys.stderr.write(res.stderr or res.stdout)
            sys.exit(1)
    if not hist_file.exists():
        sys.stderr.write(f"找不到對比度存摺：{hist_file}\n")
        sys.exit(1)

    proposals = [{
        "kind": "baseline_standard",
        "pattern": "contrast_ratio:7.0",
        "scope": "any",
        "risk": "low",
        "source_url": str(hist_file),
        "tier": "A",
        "evidence": "WCAG 2.1 AAA 高齡視力友善內文相對亮度對比度強制 >= 7.0:1（合規基準標準）",
        "confidence": 0.95,
    }]
    out = {
        "office": "josef",
        "meta": {"state_file": str(hist_file)},
        "proposals": proposals,
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
