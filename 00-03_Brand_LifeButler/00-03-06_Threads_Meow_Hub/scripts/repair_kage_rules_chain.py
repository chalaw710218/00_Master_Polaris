import sys
import json
from pathlib import Path

p = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
sys.path.insert(0, str(p))
import rule_store

rules_file = p / "vaults" / "kage_rules.jsonl"
lines = [l.strip() for l in rules_file.read_text(encoding="utf-8").splitlines() if l.strip()]

new_lines = []
prev = rule_store.ZERO_HASH

for l in lines:
    ev = json.loads(l)
    body = {k: v for k, v in ev.items() if k != "hash"}
    body["prev"] = prev
    h = rule_store._hash_body(body)
    body["hash"] = h
    prev = h
    new_lines.append(json.dumps(body, ensure_ascii=False))

# 測試在記憶體中折疊
backup_file = p / "vaults" / "kage_rules.jsonl.bak"
backup_file.write_text(rules_file.read_text(encoding="utf-8"), encoding="utf-8")
rules_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

# 驗證 fold
rules = rule_store.fold("kage")
print("Folded rules count:", len(rules))
for rid, r in rules.items():
    print(f"Rule {rid}: status={r.get('status')}, pattern={r.get('pattern')}, tampered_reason={r.get('tampered_reason')}")

# 測試 enforce constraints
active = [r for r in rules.values() if r.get("status") == "active"]
print("\nActive rules count:", len(active))
import enforce
print("\nCompiled constraints output:")
print(enforce.compile_constraints(active))
