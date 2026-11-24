import sys
import re
import time
from pathlib import Path

p_core = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
sys.path.insert(0, str(p_core))
import evidence_gate

cache_dir = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\k_page_cache")
cache_dir.mkdir(parents=True, exist_ok=True)

p_kb = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\pending_knowledge_base.md")
txt = p_kb.read_text(encoding='utf-8')
sections = [s for s in re.split(r'\n(?=###\s*【K-\d+)', txt) if s.strip().startswith('### 【K-')]

print(f"Total sections: {len(sections)}")

for s in sections:
    lines = [l.strip() for l in s.splitlines() if l.strip()]
    header = lines[0]
    kid = re.search(r'K-\d+', header).group(0)
    
    m_url = re.search(r'https?://[^\s\)]+', s)
    url = m_url.group(0) if m_url else ''
    
    cache_file = cache_dir / f"{kid}.txt"
    if cache_file.exists() and cache_file.stat().st_size > 100:
        print(f"[{kid}] Cached ({cache_file.stat().st_size} bytes)")
        continue
        
    print(f"[{kid}] Fetching: {url} ...")
    try:
        page_text = evidence_gate.fetch_page_text(url, timeout=15)
        if len(page_text.strip()) > 50:
            cache_file.write_text(page_text, encoding='utf-8')
            print(f"   -> Success ({len(page_text)} chars)")
        else:
            cache_file.write_text("EMPTY_OR_BLOCKED", encoding='utf-8')
            print(f"   -> Empty/Blocked")
    except Exception as e:
        cache_file.write_text(f"ERROR: {e}", encoding='utf-8')
        print(f"   -> Failed: {e}")
    time.sleep(1)

print("\nAll done fetching!")
