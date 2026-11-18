import sys
import json
from pathlib import Path

hub_dir = Path(__file__).resolve().parent.parent
root_dir = hub_dir.parents[1]
bionic_dir = root_dir / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
sys.path.append(str(bionic_dir))

import enforce
import rule_store

rules = rule_store.fold("kage")
print("=== KAGE ACTIVE RULES ===")
active_rules = enforce.load_active_rules("kage")
for r in active_rules:
    print(f"[{r.get('rule_id')}] Kind: {r.get('kind')} | Pattern: {r.get('pattern')} | Status: {r.get('status')} | Source: Tier {r.get('source_tier')}")

print("\n=== KAGE ALL RULES STATUS ===")
for rid, r in rules.items():
    st = r.get("status")
    kind = r.get("kind")
    pat = r.get("pattern")
    ret_reason = r.get("retired_reason", "")
    print(f"- {rid}: {kind} '{pat}' -> {st} (Retired Reason: {ret_reason})")

p = rule_store._path("kage")
if p.exists():
    lines = [x for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    print(f"\nLedger Total Events: {len(lines)}")
    last_ev = json.loads(lines[-1])
    print(f"Latest Event: Type={last_ev.get('type')}, Rule={last_ev.get('rule_id')}, Hash={last_ev.get('hash')[:20]}...")

# Check round ledger
round_file = root_dir / ".agents" / "skills" / "bionic-learning-system" / "bionic_core" / "vaults" / "round_ledger.jsonl"
if round_file.exists():
    r_lines = [x for x in round_file.read_text(encoding="utf-8").splitlines() if x.strip()]
    kage_rounds = [json.loads(x) for x in r_lines if json.loads(x).get("office") == "kage"]
    print(f"\nTotal Kage Bionic Learning Rounds Logged: {len(kage_rounds)}")
    if kage_rounds:
        last_r = kage_rounds[-1]
        print(f"Latest Round: #{last_r.get('round_num')}, Cycle: {last_r.get('cycle_id')}, Hash: {last_r.get('hash', '')[:20]}...")
