import json
from pathlib import Path

hub_dir = Path(__file__).resolve().parent.parent
root_dir = hub_dir.parents[1]
p = root_dir / ".agents" / "skills" / "bionic-learning-system" / "bionic_core" / "vaults" / "kage_cycles.jsonl"

if p.exists():
    lines = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    print("Total events in kage_cycles.jsonl:", len(lines))
    for i, ev in enumerate(lines):
        t = ev.get("type")
        c = ev.get("cycle")
        s = ev.get("summary", "")[:40]
        h = ev.get("hash", "")[:12]
        print(f"[{i+1}] Type={t} | Cycle={c} | Hash={h} | Summary={s}")
