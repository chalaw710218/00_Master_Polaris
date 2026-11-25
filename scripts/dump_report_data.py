from pathlib import Path
from build_all_proposals import GROUPS_CONFIG

print("=== 母體行數變化統計 ===")
for g in GROUPS_CONFIG:
    if g['parent_orig'] and g['parent_orig'].exists():
        orig_lines = len(g['parent_orig'].read_text(encoding='utf-8').splitlines())
        prop_file = Path(f"_proposed/{g['group_name']}/{g['parent_name']}/SKILL.md")
        prop_lines = len(prop_file.read_text(encoding='utf-8').splitlines())
        print(f"{g['group_name']}: {orig_lines} → {prop_lines}")
    else:
        print(f"{g['group_name']}: 不存在（無母體）")

print("\n=== 所有「待品碩核准」的 allowlist 條目清單 ===")
al = Path("scripts/rule_diff_allowlist.txt").read_text(encoding="utf-8").splitlines()
pending = [l for l in al if "待品碩核准" in l]
print(f"總計待核准條目數：{len(pending)} 條\n")
for idx, p in enumerate(pending, 1):
    print(f"{idx:2d}. {p}")
