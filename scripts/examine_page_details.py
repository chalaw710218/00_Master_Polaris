import re
from pathlib import Path

cache_dir = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\k_page_cache")

def examine(kid):
    txt = (cache_dir / f"{kid}.txt").read_text(encoding='utf-8', errors='ignore')
    print(f"\n============================== {kid} ==============================")
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    print("Page Title/Start:", " // ".join(lines[:6]))
    return txt

txt_k5 = examine("K-005")
# Look for Oldenburg, third place
for l in txt_k5.splitlines():
    if any(k in l.lower() for k in ["oldenburg", "third place", "neutral", "home"]):
        if len(l.strip()) > 30:
            print("  [K-005 hit]:", l.strip()[:140])

txt_k6 = examine("K-006")
# Look for prompt engineering verbs / ai
for l in txt_k6.splitlines():
    if any(k in l.lower() for k in ["verb", "clear", "direct", "fluff", "action", "prompt"]):
        if len(l.strip()) > 20:
            print("  [K-006 hit]:", l.strip()[:140])

txt_k7 = examine("K-007")
for l in txt_k7.splitlines():
    if any(k in l.lower() for k in ["good, clean", "fair", "philosophy"]):
        if len(l.strip()) > 20:
            print("  [K-007 hit]:", l.strip()[:140])

txt_k8 = examine("K-008")
for l in txt_k8.splitlines():
    if any(k in l.lower() for k in ["velocity", "window", "30", "60", "speed", "reply"]):
        if len(l.strip()) > 30:
            print("  [K-008 hit]:", l.strip()[:140])

txt_k9 = examine("K-009")
for l in txt_k9.splitlines():
    if any(k in l.lower() for k in ["eight", "domains", "framework", "barrier", "aging in place"]):
        if len(l.strip()) > 30:
            print("  [K-009 hit]:", l.strip()[:140])

txt_k12 = examine("K-012")
for l in txt_k12.splitlines():
    if any(k in l.lower() for k in ["reply", "replies", "two-way", "ranking", "active", "passive"]):
        if len(l.strip()) > 30:
            print("  [K-012 hit]:", l.strip()[:140])

txt_k17 = examine("K-017")
for l in txt_k17.splitlines():
    if any(k in l.lower() for k in ["wabi-sabi", "imperfection", "photo", "truth"]):
        if len(l.strip()) > 30:
            print("  [K-017 hit]:", l.strip()[:140])

txt_k21 = examine("K-021")
print("K-021 sample text:", txt_k21[:300])

txt_k23 = examine("K-023")
print("K-023 sample text:", txt_k23[:300])

txt_k25 = examine("K-025")
print("K-025 sample text:", txt_k25[:300])

txt_k31 = examine("K-031")
print("K-031 sample text:", txt_k31[:300])
