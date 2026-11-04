import re
with open(r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_CMO_Taylor\00_Taylor_Notebook.md', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'(\* \*\*Cycle [^\n]+)', text)
print(f"Total matched: {len(matches)}")
for m in matches[:10]:
    print(m)
print("...")
for m in matches[-10:]:
    print(m)
