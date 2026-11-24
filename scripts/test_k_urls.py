import sys
import re
import urllib.request
from pathlib import Path

# Add bionic_core to sys.path
p_core = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
sys.path.insert(0, str(p_core))
import evidence_gate

p_kb = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\pending_knowledge_base.md")
txt = p_kb.read_text(encoding='utf-8')
sections = [s for s in re.split(r'\n(?=###\s*【K-\d+)', txt) if s.strip().startswith('### 【K-')]

print(f"Total sections: {len(sections)}")

for s in sections:
    lines = [l.strip() for l in s.splitlines() if l.strip()]
    header = lines[0]
    m_id = re.search(r'K-\d+', header)
    kid = m_id.group(0) if m_id else 'UNKNOWN'
    
    m_url = re.search(r'https?://[^\s\)]+', s)
    url = m_url.group(0) if m_url else ''
    
    # Extract title
    title = header.replace('###', '').strip()
    
    # Extract quote if any
    quotes = [l.lstrip('>').strip() for l in lines if l.startswith('>')]
    quote_text = ' '.join(quotes).strip()
    
    print(f"{kid}: {url}")
