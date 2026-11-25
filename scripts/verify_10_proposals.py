import subprocess
from pathlib import Path
from build_all_proposals import GROUPS_CONFIG

for g in GROUPS_CONFIG:
    orig_files = []
    if g['parent_orig'] and g['parent_orig'].exists():
        orig_files.append(str(g['parent_orig']))
    for a in g['atoms']:
        orig_files.append(str(a['orig']))
    
    prop_files = []
    prop_dir = Path(f"_proposed/{g['group_name']}")
    for sub in prop_dir.iterdir():
        if sub.is_dir() and (sub / "SKILL.md").exists():
            prop_files.append(str(sub / "SKILL.md"))
    
    cmd = ["python", "scripts/rule_diff_check.py", "--orig"] + orig_files + ["--prop"] + prop_files
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    has_token_missing = "🚨【第一階段未通過" in res.stdout
    pending_count = res.stdout.count("[⏳ 待品碩核准]")
    unauthorized_count = res.stdout.count("[❌ 違規遺失]")
    print(f"{g['group_name']:<12}: Tokens Missing: {str(has_token_missing):<5} | Pending Allow: {pending_count:2d} | Unauthorized Missing: {unauthorized_count:2d}")
