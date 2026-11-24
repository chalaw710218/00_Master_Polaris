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

print("=== CHECKING EACH K ITEM ===")

for s in sections:
    lines = [l.strip() for l in s.splitlines() if l.strip()]
    header = lines[0]
    kid = re.search(r'K-\d+', header).group(0)
    title = header.replace('###', '').strip()
    
    m_url = re.search(r'https?://[^\s\)]+', s)
    url = m_url.group(0) if m_url else ''
    
    cache_file = cache_dir / f"{kid}.txt"
    content = cache_file.read_text(encoding='utf-8', errors='ignore') if cache_file.exists() else "NO_FILE"
    
    if content.startswith("ERROR:") or content == "EMPTY_OR_BLOCKED" or content == "NO_FILE":
        print(f"{kid}: FETCH_FAILED ({content[:30]})")
    elif len(content.strip()) < 500:
        print(f"{kid}: SUSPICIOUSLY_SHORT ({len(content)} chars): {content[:100]}...")
    else:
        print(f"{kid}: SUCCESS ({len(content)} chars)")
