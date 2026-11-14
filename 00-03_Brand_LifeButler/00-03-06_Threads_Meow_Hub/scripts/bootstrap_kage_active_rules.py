import sys
import os
import json
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

p = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
sys.path.insert(0, str(p))
import rule_store
import enforce

ds_path = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\kage_standard_samples.jsonl")

# 1. 提案第一條：forbid_phrase 我就問
rid1 = rule_store.propose(
    office="kage",
    kind="forbid_phrase",
    pattern="我就問",
    risk="low",
    source_url=str(ds_path),
    tier="A",
    evidence="真實 Threads 快照 N=4，開頭『我就問』平均 ER=0.85% < 帳號中位數 2.0%*0.7",
    scope="prefix",
    confidence=0.85,
    ttl_days=90
)
print(f"Proposed Rule 1: {rid1}")

# evaluate Rule 1
ok1, why1, ev1 = rule_store.evaluate_rule(office="kage", rule_id=rid1, dataset_path=ds_path)
print(f"Evaluate Rule 1: ok={ok1}, why={why1}")
if ok1:
    ok_p1, why_p1 = rule_store.promote(office="kage", rule_id=rid1)
    print(f"Promote Rule 1: ok={ok_p1}, why={why_p1}")

# 2. 提案第二條：prefer_phrase 誰能想
rid2 = rule_store.propose(
    office="kage",
    kind="prefer_phrase",
    pattern="誰能想",
    risk="low",
    source_url=str(ds_path),
    tier="A",
    evidence="真實 Threads 快照 N=3，開頭『誰能想』平均 ER=3.5% >= 帳號中位數 2.0%*1.3",
    scope="prefix",
    confidence=0.85,
    ttl_days=90
)
print(f"Proposed Rule 2: {rid2}")

# evaluate Rule 2
ok2, why2, ev2 = rule_store.evaluate_rule(office="kage", rule_id=rid2, dataset_path=ds_path)
print(f"Evaluate Rule 2: ok={ok2}, why={why2}")
if ok2:
    ok_p2, why_p2 = rule_store.promote(office="kage", rule_id=rid2)
    print(f"Promote Rule 2: ok={ok_p2}, why={why_p2}")

# 3. 驗證 enforce constraints
active = enforce.load_active_rules("kage")
print(f"\n驗證 active 規則總數: {len(active)}")
print("\n編譯後的約束輸出:")
print(enforce.compile_constraints(active))
