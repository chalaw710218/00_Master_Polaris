import re
with open(r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_CMO_Taylor\00_Taylor_Notebook.md', encoding='utf-8') as f:
    text = f.read()

# Let's find all lines starting with * **Cycle
cycle_lines = re.findall(r'(\*\s+\*\*Cycle\s+\d+[^:\n]+[:：][^\n]+)', text)
print(f"Total cycle lines with content: {len(cycle_lines)}")

# Let's see some samples that might have different patterns
ranges = re.findall(r'(\*\s+\*\*Cycle\s+\d+[~～-]\d+[^:\n]+[:：][^\n]+)', text)
print(f"Total cycle ranges (e.g. Cycle 71~73): {len(ranges)}")
for r in ranges[:10]:
    print(r[:80])
