import re

with open(r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_CMO_Taylor\00_Taylor_Notebook.md', encoding='utf-8') as f:
    text = f.read()

# Pattern matching * **Cycle <num><any title>**：<content>
pattern = re.compile(r'\*\s+\*\*Cycle\s+(\d+)\s*([^:\n*]+)\*\*[:：]\s*([^\n]+)')
matches = pattern.findall(text)
print(f"Matched with general pattern: {len(matches)}")

cycle_nums = [int(m[0]) for m in matches]
print(f"Min cycle: {min(cycle_nums)}, Max cycle: {max(cycle_nums)}")
print(f"Total unique cycles: {len(set(cycle_nums))}")

# Check missing cycles between 61 and 260
missing = [i for i in range(61, 261) if i not in cycle_nums]
print(f"Missing cycles between 61 and 260: {missing}")
