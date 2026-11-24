import sys
import re
from pathlib import Path

p_core = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
sys.path.insert(0, str(p_core))
import evidence_gate

cache_dir = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\k_page_cache")

targets = [
    ("K-005", ["third place", "oldenburg", "community", "social"]),
    ("K-006", ["ai", "prompt", "verb", "style", "direct"]),
    ("K-007", ["good", "clean", "fair", "philosophy"]),
    ("K-008", ["algorithm", "speed", "velocity", "reply", "minute"]),
    ("K-009", ["age-friendly", "community", "environment", "who"]),
    ("K-012", ["threads", "algorithm", "reply", "ranking", "conversation"]),
    ("K-016", ["intergenerational", "trust", "digital", "older", "younger"]),
    ("K-017", ["wabi-sabi", "photography", "imperfection", "light", "natural"]),
    ("K-021", ["topic", "tag", "threads", "hashtag", "search"]),
    ("K-023", ["protagonist", "dual", "cadence", "narrative"]),
    ("K-025", ["operational transparency", "buell", "effort", "trust"]),
    ("K-031", ["customer development", "blank", "pre-announcement", "need"])
]

for kid, kws in targets:
    f = cache_dir / f"{kid}.txt"
    if not f.exists():
        print(f"[{kid}] No file")
        continue
    txt = f.read_text(encoding='utf-8', errors='ignore')
    print(f"\n==================== {kid} (length: {len(txt)}) ====================")
    
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+|\n+', txt)
    matched_sents = []
    for s in sentences:
        s_clean = s.strip()
        if len(s_clean) > 30 and any(k.lower() in s_clean.lower() for k in kws):
            matched_sents.append(s_clean)
            
    print(f"Found {len(matched_sents)} candidate sentences. Showing top 3:")
    for ms in matched_sents[:3]:
        print(f"  * {ms[:150]}")
