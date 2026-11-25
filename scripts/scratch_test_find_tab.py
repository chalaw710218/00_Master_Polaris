import sys
from pathlib import Path
HERE = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\scripts")
sys.path.insert(0, str(HERE))
import claude_relay

pair_key = "c06c2e4f-8afc-4b48-8bd9-11ddbcdeb1e5"
i, p = claude_relay.find_pair(pair_key)
print("p is:", p)
try:
    tab = claude_relay.find_tab(p["claude_href"])
    print("Found tab:", tab)
except Exception as e:
    print("Error:", e)
