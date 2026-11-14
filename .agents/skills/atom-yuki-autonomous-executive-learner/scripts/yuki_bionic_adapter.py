"""雪 (Yuki) 專屬仿生特化轉接器 (Role-Specific Adapter)
職責：檢查幕僚長派工帳本 (dispatch.py) 雜湊鏈完整性，並根據各類別任務派工紀錄提名 route 候選規則，輸出標準 JSON 供萬用母版 bionic_core 驗算。
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
    event_count = 0
    if ledger_file.exists():
        lines = [json.loads(x) for x in ledger_file.read_text(encoding="utf-8").splitlines() if x.strip()]
        event_count = len(lines)
        cats = {e.get("category") for e in lines if e.get("type") == "dispatch" and e.get("category")}
        for cat in sorted(cats):
            counts: dict[str, int] = {}
            for e in lines:
                if e.get("type") == "dispatch" and e.get("category") == cat:
                    for a in e.get("assigned", []):
                        counts[a] = counts.get(a, 0) + 1
            if counts:
                top_agent, cnt = max(counts.items(), key=lambda kv: kv[1])
                if cnt >= 3:
                    proposals.append({
                        "kind": "route",
                        "pattern": f"{cat}->{top_agent}",
                        "scope": "any",
                        "risk": "high",
                        "source_url": str(ledger_file),
                        "tier": "A",
                        "evidence": f"幕僚長派工帳本實測：『{cat}』類任務指派 {top_agent} 共 {cnt} 筆，提請驗證一次通過率",
                        "confidence": min(0.90, round(0.40 + cnt * 0.05, 2)),
                    })

    out = {
        "office": "yuki",
        "meta": {"dispatch_ledger": str(ledger_file), "events": event_count, "status_output": res.stdout.strip()},
        "proposals": proposals,
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
