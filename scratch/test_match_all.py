import sys, re
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open(r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_CMO_Taylor\00_Taylor_Notebook.md', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r'\*\s+\*\*Cycle\s+(\d+)\s*(.*?)\*\*[:：]\s*([^\n]+)')
matches = pattern.findall(text)
print(f"Total matched: {len(matches)}")
cycle_nums = [int(m[0]) for m in matches]
print(f"Min: {min(cycle_nums)}, Max: {max(cycle_nums)}, Unique: {len(set(cycle_nums))}")
missing = [i for i in range(61, 261) if i not in cycle_nums]
print(f"Missing in 61..260: {missing}")
