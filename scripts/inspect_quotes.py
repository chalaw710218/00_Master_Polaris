import sys
import re
from pathlib import Path

p_core = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
sys.path.insert(0, str(p_core))
import evidence_gate

p_kb = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\pending_knowledge_base.md")
txt = p_kb.read_text(encoding='utf-8')
sections = [s for s in re.split(r'\n(?=###\s*【K-\d+)', txt) if s.strip().startswith('### 【K-')]

print(f"Total sections: {len(sections)}")

results = []
for s in sections:
    lines = [l.strip() for l in s.splitlines() if l.strip()]
    header = lines[0]
    kid = re.search(r'K-\d+', header).group(0)
    title = header.replace('###', '').strip()
    
    m_url = re.search(r'https?://[^\s\)]+', s)
    url = m_url.group(0) if m_url else ''
    
    # quote type
    is_verbatim = '【逐字原文摘句】' in s
    is_summary = '【僅有搜尋摘要】' in s
    
    # quote content
    quotes = [l.lstrip('>').strip() for l in lines if l.startswith('>')]
    quote_text = ' '.join(quotes).strip()
    
    results.append({
        'kid': kid,
        'title': title,
        'url': url,
        'is_verbatim': is_verbatim,
        'is_summary': is_summary,
        'quote': quote_text
    })

print("K items summary:")
for r in results:
    q_type = 'VERBATIM' if r['is_verbatim'] else ('SUMMARY' if r['is_summary'] else 'NONE')
    print(f"{r['kid']}: [{q_type}] {r['quote'][:50]}")
