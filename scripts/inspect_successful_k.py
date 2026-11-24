import sys
import re
from pathlib import Path

p_core = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
sys.path.insert(0, str(p_core))
import evidence_gate

cache_dir = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\k_page_cache")
p_kb = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\pending_knowledge_base.md")
txt = p_kb.read_text(encoding='utf-8')
sections = [s for s in re.split(r'\n(?=###\s*【K-\d+)', txt) if s.strip().startswith('### 【K-')]

success_kids = ["K-001", "K-002", "K-005", "K-006", "K-007", "K-008", "K-009", "K-012", "K-016", "K-017", "K-021", "K-023", "K-025", "K-031"]

for s in sections:
    header = s.splitlines()[0]
    kid = re.search(r'K-\d+', header).group(0)
    if kid not in success_kids:
        continue
        
    print(f"\n==================== {kid} ====================")
    print(header)
    
    # Existing quote
    lines = [l.strip() for l in s.splitlines() if l.strip()]
    quotes = [l.lstrip('>').strip() for l in lines if l.startswith('>')]
    quote_text = ' '.join(quotes).strip()
    print(f"Existing quote in KB: {quote_text}")
    
    cache_file = cache_dir / f"{kid}.txt"
    page_text = cache_file.read_text(encoding='utf-8', errors='ignore')
    
    # Check if existing quote matches
    if quote_text and not quote_text.startswith("搜尋摘要確認"):
        clean_q = quote_text.strip(' "“‘”’')
        ok, why = evidence_gate.quote_in_page(clean_q, page_text)
        print(f"Direct quote check: ok={ok}, why={why}")
    else:
        print("Existing quote is a summary. Needs finding actual verbatim quote in page.")
