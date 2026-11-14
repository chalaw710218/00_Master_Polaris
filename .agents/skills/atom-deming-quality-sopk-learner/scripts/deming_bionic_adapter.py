"""戴明 (Deming) 專屬仿生特化轉接器 (Role-Specific Adapter · v6.4)
職責：
  1. 執行戴明的品質防呆盤點。
  2. 將戴明專屬欄位 (`total`, `passed`, `defects`) 正規化為母版通用標準樣本列 (`deming_standard_samples.jsonl`: `{n, compliant, metrics}`)，確保母版零角色私貨。
  3. 讀取並消費 `perceived_deming.jsonl` 外部感知文獻摘要。
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
ROOT_DIR = SKILL_DIR.parent.parent.parent
PERCEIVED_FILE = ROOT_DIR / ".agents" / "skills" / "bionic-learning-system" / "bionic_core" / "vaults" / "perceived_deming.jsonl"
HIST_FILE = SKILL_DIR / "vaults" / "deming_quality_history.jsonl"
STANDARD_SAMPLES = SKILL_DIR / "vaults" / "deming_standard_samples.jsonl"


def consume_perceived() -> dict:
    if not PERCEIVED_FILE.exists():
        return {"count": 0, "latest_titles": []}
    rows = [json.loads(x) for x in PERCEIVED_FILE.read_text(encoding="utf-8").splitlines() if x.strip()]
    ab_rows = [r for r in rows if r.get("tier") in ("A", "B")]
    return {"count": len(rows), "ab_tier_count": len(ab_rows), "latest_titles": [r.get("title", "")[:60] for r in ab_rows[-3:]]}


def normalize_samples() -> int:
    if not HIST_FILE.exists():
        return 0
    raw_rows = [json.loads(x) for x in HIST_FILE.read_text(encoding="utf-8").splitlines() if x.strip()]
    STANDARD_SAMPLES.parent.mkdir(parents=True, exist_ok=True)
    with open(STANDARD_SAMPLES, "w", encoding="utf-8") as f:
        for idx, r in enumerate(raw_rows):
            n = int(r.get("total", r.get("n", 0)))
            comp = int(r.get("passed", r.get("compliant", 0)))
            defects = float(r.get("defects", max(0, n - comp)))
            std_row = {
                "id": f"deming-{idx + 1}",
                "n": n,
                "compliant": comp,
                "metrics": {"defects": defects},
                "ts": str(r.get("audited_at", f"{idx:06d}")),
            }
            f.write(json.dumps(std_row, ensure_ascii=False) + "\n")
    return len(raw_rows)


def main() -> None:
    learn_script = SCRIPT_DIR / "deming_real_learning.py"
    if not HIST_FILE.exists() and learn_script.exists():
        res = subprocess.run([sys.executable, str(learn_script), "--audit"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
        if res.returncode != 0:
            sys.stderr.write(res.stderr or res.stdout)
            sys.exit(1)
    if not HIST_FILE.exists():
        sys.stderr.write(f"找不到戴明品質存摺：{HIST_FILE}\n")
        sys.exit(1)

    cnt = normalize_samples()
    proposals = [{
        "kind": "baseline_standard",
        "pattern": "defects<=0",
        "scope": "any",
        "risk": "low",
        "source_url": str(STANDARD_SAMPLES),
        "tier": "A",
        "evidence": "全域原子腳本語法編譯與 --help 測試缺陷數上限為 0（合規基準標準）",
        "confidence": 0.95,
    }]
    out = {
        "office": "deming",
        "meta": {
            "state_file": str(HIST_FILE),
            "standard_samples_file": str(STANDARD_SAMPLES),
            "normalized_rows": cnt,
            "perceived_consumed": consume_perceived(),
        },
        "proposals": proposals,
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
