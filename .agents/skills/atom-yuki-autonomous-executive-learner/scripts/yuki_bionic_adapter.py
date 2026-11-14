"""雪 (Yuki) 專屬仿生特化轉接器 (Role-Specific Adapter · v6.4)
職責：
  1. 呼叫 `dispatch.py status` 檢查雜湊鏈完整性（鏈壞即 Exit Code 1 阻斷）。
  2. 讀取並消費 `perceived_yuki.jsonl` 外部感知文獻摘要。
  3. 根據创辦人已驗簽匯出之標準路由樣本 (`yuki_verified_route_samples.jsonl`)，檢查各類別是否同時具備主組（>=3 筆已簽收結案）與對照組（>=3 筆已簽收結案）且主組一次通過率優於對照組，才提名 `route` 候選規則！絕不盲目只看派工次數提名。
"""
from __future__ import annotations

import json
import statistics
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
PERCEIVED_FILE = ROOT_DIR / ".agents" / "skills" / "bionic-learning-system" / "bionic_core" / "vaults" / "perceived_yuki.jsonl"
VERIFIED_SAMPLES = SKILL_DIR / "vaults" / "yuki_verified_route_samples.jsonl"
MIN_GROUP_N = 3


def consume_perceived() -> dict:
    if not PERCEIVED_FILE.exists():
        return {"count": 0, "latest_titles": []}
    rows = [json.loads(x) for x in PERCEIVED_FILE.read_text(encoding="utf-8").splitlines() if x.strip()]
    ab_rows = [r for r in rows if r.get("tier") in ("A", "B")]
    return {"count": len(rows), "ab_tier_count": len(ab_rows), "latest_titles": [r.get("title", "")[:60] for r in ab_rows[-3:]]}


def main() -> None:
    disp_script = SCRIPT_DIR / "dispatch.py"
    ledger_file = SKILL_DIR / "vaults" / "yuki_dispatch.jsonl"
    if not disp_script.exists():
        sys.stderr.write(f"找不到派工帳本腳本：{disp_script}\n")
        sys.exit(1)

    res = subprocess.run([sys.executable, str(disp_script), "status"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    if res.returncode != 0:
        sys.stderr.write(res.stderr or res.stdout)
        sys.exit(1)

    proposals = []
    readiness_notes: list[str] = []

    if VERIFIED_SAMPLES.exists():
        lines = [json.loads(x) for x in VERIFIED_SAMPLES.read_text(encoding="utf-8").splitlines() if x.strip()]
        if lines and lines[-1].get("kind") == "verified_route_samples":
            all_samples = lines[-1].get("samples", [])
            # 僅使用前半段 (Discovery Split) 提名路由規則
            mid = len(all_samples) // 2 if len(all_samples) >= 6 else len(all_samples)
            disc_samples = all_samples[:mid]
            cats = sorted({s.get("category") for s in disc_samples if s.get("category")})
            for cat in cats:
                cat_rows = [s for s in disc_samples if s.get("category") == cat]
                agents = sorted({a for s in cat_rows for a in s.get("assigned", [])})
                if len(agents) < 2:
                    readiness_notes.append(f"類別『{cat}』僅派給單一閣員 {agents}，尚缺對照派工組")
                    continue
                best_agent = None
                best_diff = 0.0
                best_stats = (0, 0, 0.0, 0.0)
                for a in agents:
                    w = [float(s["metric"]) for s in cat_rows if a in s.get("assigned", [])]
                    wo = [float(s["metric"]) for s in cat_rows if a not in s.get("assigned", [])]
                    if len(w) >= MIN_GROUP_N and len(wo) >= MIN_GROUP_N:
                        mw, mwo = statistics.mean(w), statistics.mean(wo)
                        if mw - mwo > best_diff:
                            best_diff = mw - mwo
                            best_agent = a
                            best_stats = (len(w), len(wo), round(mw, 1), round(mwo, 1))
                if best_agent:
                    nw, nwo, mw, mwo = best_stats
                    proposals.append({
                        "kind": "route",
                        "pattern": f"{cat}->{best_agent}",
                        "scope": "any",
                        "risk": "high",
                        "source_url": str(VERIFIED_SAMPLES),
                        "tier": "A",
                        "evidence": f"已驗簽結案樣本：『{cat}』指派 {best_agent} 一次通過率 {mw}% (N={nw}) > 對照組 {mwo}% (N={nwo})",
                        "confidence": min(0.90, round(0.50 + nw * 0.05, 2)),
                    })
                else:
                    readiness_notes.append(f"類別『{cat}』主組或對照組已簽收結案樣本未達 {MIN_GROUP_N} 筆")
    else:
        readiness_notes.append("尚未由創辦人執行 dispatch.py export-verified 匯出已驗簽結案樣本")

    out = {
        "office": "yuki",
        "meta": {
            "dispatch_ledger": str(ledger_file),
            "verified_samples_file": str(VERIFIED_SAMPLES),
            "status_output": res.stdout.strip(),
            "route_readiness": readiness_notes,
            "perceived_consumed": consume_perceived(),
        },
        "proposals": proposals,
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
