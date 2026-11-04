import re

with open(r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_CMO_Taylor\00_Taylor_Notebook.md', encoding='utf-8') as f:
    lines = f.readlines()

cycle_lines = []
for i, line in enumerate(lines):
    if 'Cycle' in line and ('**' in line or '##' in line):
        cycle_lines.append((i+1, line.strip()))

print(f"Total lines mentioning Cycle: {len(cycle_lines)}")
for ln, l in cycle_lines[:30]:
    print(f"L{ln}: {l[:80]}")
