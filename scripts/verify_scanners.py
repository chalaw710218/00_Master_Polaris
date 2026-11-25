import subprocess
from pathlib import Path
from build_all_proposals import GROUPS_CONFIG

for g in GROUPS_CONFIG:
    target_dir = Path(f"_proposed/{g['group_name']}")
    cmd = ["python", "scripts/skill_scanner.py", str(target_dir)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    errs = 0
    warns = 0
    for line in res.stdout.splitlines():
        if "[E" in line and ":" in line:
            val = line.split(":")[-1].strip()
            if val.isdigit():
                errs += int(val)
        if "[W" in line and ":" in line:
            val = line.split(":")[-1].strip()
            if val.isdigit():
                warns += int(val)
    print(f"{g['group_name']:<12}: Errors = {errs} | Warnings = {warns}")
