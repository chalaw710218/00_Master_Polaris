"""影 (Kage) 專屬仿生特化轉接器 (Role-Specific Adapter · v6.4)
職責：
  1. 將 Threads 原始快照 (`insights_history.jsonl`) 正規化為母版通用標準樣本列 (`kage_standard_samples.jsonl`: `{id, text, metric, ts}`)。
  2. 嚴格執行前後半切分（Discovery Split）：**僅使用前半段（前 50%）樣本**計算開頭鉤子成效並提名候選規則，嚴禁偷看後半段留出集（Holdout Split）！
  3. 讀取並消費 `perceived_kage.jsonl` 外部感知文獻摘要。
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
PERCEIVED_FILE = ROOT_DIR / ".agents" / "skills" / "bionic-learning-system" / "bionic_core" / "vaults" / "perceived_kage.jsonl"
RAW_HISTORY = ROOT_DIR / ".agents" / "skills" / "threads-growth-auditor" / "data" / "insights_history.jsonl"
STANDARD_SAMPLES = SKILL_DIR / "vaults" / "kage_standard_samples.jsonl"
MIN_N = 3
HOOK_LEN = 3


def consume_perceived() -> dict:
    if not PERCEIVED_FILE.exists():
        return {"count": 0, "latest_titles": []}
    rows = [json.loads(x) for x in PERCEIVED_FILE.read_text(encoding="utf-8").splitlines() if x.strip()]
    ab_rows = [r for r in rows if r.get("tier") in ("A", "B")]
    return {
        "count": len(rows),
        "ab_tier_count": len(ab_rows),
        "latest_titles": [r.get("title", "")[:60] for r in ab_rows[-3:]],
    }


def normalize_and_split() -> tuple[list[dict], list[dict]]:
    if not RAW_HISTORY.exists():
        return [], []
    posts_map: dict[str, dict] = {}
    for line in RAW_HISTORY.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        snap = json.loads(line)
        cap_ts = str(snap.get("captured_at", ""))
        for p in snap.get("posts", []):
            pid = str(p.get("id", ""))
            if not pid:
                continue
            prev = posts_map.get(pid)
            if prev is None or cap_ts >= prev["ts"]:
                posts_map[pid] = {
                    "id": pid,
                    "text": str(p.get("title", p.get("text", ""))),
                    "metric": float(p.get("er", 0.0)),
                    "ts": cap_ts,
                }
    all_samples = sorted(posts_map.values(), key=lambda x: (x["ts"], x["id"]))
    STANDARD_SAMPLES.parent.mkdir(parents=True, exist_ok=True)
    with open(STANDARD_SAMPLES, "w", encoding="utf-8") as f:
        for s in all_samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    mid = len(all_samples) // 2 if len(all_samples) >= 6 else len(all_samples)
    return all_samples, all_samples[:mid]


def main() -> None:
    learn_script = SCRIPT_DIR / "kage_real_learning.py"
    state_file = SKILL_DIR / "vaults" / "kage_synaptic_state.json"
    if learn_script.exists():
        res = subprocess.run([sys.executable, str(learn_script), "--learn"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        if res.returncode != 0:
            sys.stderr.write(res.stderr or res.stdout)
            sys.exit(1)

    all_samples, discovery_samples = normalize_and_split()
    proposals = []
    median_er = statistics.median([s["metric"] for s in discovery_samples]) if discovery_samples else 2.0

    # 僅在前半段 (Discovery Split) 統計鉤子並提名，絕不偷看後半段 Holdout
    hook_groups: dict[str, list[float]] = {}
    for s in discovery_samples:
        hook = s["text"][:HOOK_LEN]
        hook_groups.setdefault(hook, []).append(s["metric"])

    for hook, vals in sorted(hook_groups.items()):
        n = len(vals)
        if n < MIN_N:
            continue
        avg_er = round(statistics.mean(vals), 2)
        dyn_conf = min(0.95, round(0.50 + n * 0.05, 2))
        if avg_er < median_er * 0.7:
            proposals.append({
                "kind": "forbid_phrase",
                "pattern": hook,
                "scope": "prefix",
                "risk": "low",
                "source_url": str(STANDARD_SAMPLES),
                "tier": "A",
                "evidence": f"Discovery 前半集 (N={n}/{len(discovery_samples)})：開頭『{hook}』平均 ER={avg_er}% < 中位數 {median_er:.2f}%*0.7",
                "confidence": dyn_conf,
            })
        elif avg_er >= median_er * 1.3:
            proposals.append({
                "kind": "prefer_phrase",
                "pattern": hook,
                "scope": "prefix",
                "risk": "low",
                "source_url": str(STANDARD_SAMPLES),
                "tier": "A",
                "evidence": f"Discovery 前半集 (N={n}/{len(discovery_samples)})：開頭『{hook}』平均 ER={avg_er}% >= 中位數 {median_er:.2f}%*1.3",
                "confidence": dyn_conf,
            })

    out = {
        "office": "kage",
        "meta": {
            "state_file": str(state_file),
            "standard_samples_file": str(STANDARD_SAMPLES),
            "total_samples": len(all_samples),
            "discovery_samples_used": len(discovery_samples),
            "holdout_samples_reserved": len(all_samples) - len(discovery_samples),
            "perceived_consumed": consume_perceived(),
        },
        "proposals": proposals,
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
