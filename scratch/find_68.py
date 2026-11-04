with open(r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_CMO_Taylor\00_Taylor_Notebook.md', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'Cycle 6[789][^\n]+', text)
if m:
    pos = m.start()
    print(text[pos-100:pos+300])
