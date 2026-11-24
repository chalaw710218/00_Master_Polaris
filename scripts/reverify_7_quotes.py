import sys
import re
from pathlib import Path

p_core = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
sys.path.insert(0, str(p_core))
import evidence_gate

cache_dir = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\k_page_cache")

items = [
    ("K-002", "We find that use of model-generated content in training causes irreversible defects in the resulting models, where tails of the original content distribution disappear. We refer to this effect as Model Collapse and show that it can occur in Variational Autoencoders, Gaussian Mixture Models and LLMs."),
    ("K-005", "Third places is a term coined by sociologist  Ray Oldenburg  and refers to places where people spend time between home (‘first’ place) and work (‘second’ place)."),
    ("K-007", "Slow Food is a global movement of local groups and activists united by the common goal of ensuring everyone has access to good, clean and fair food."),
    ("K-008", "Social media algorithms act as primary distribution filters. They heavily amplify content that captures early, high-velocity engagement like saves and shares, while actively burying passive, low-effort content beneath more competitive signals."),
    ("K-009", "The city of Oldenburg has pursued a systematic strategy to promote age-friendliness since 2012, guided by the eight domains of the WHO “Age-Friendly Cities” framework."),
    ("K-012", "The Threads algorithm prioritizes signals that show genuine interest, such as replies, profile visits, time spent engaging with a post, and repeat interactions with an author."),
    ("K-017", "The underlying idea became that things are more beautiful for bearing imperfections.")
]

for kid, q in items:
    f = cache_dir / f"{kid}.txt"
    txt = f.read_text(encoding='utf-8')
    print(f"\n==================== {kid} ====================")
    print(f"網頁正文長度: {len(txt)} 字元")
    
    ok, why = evidence_gate.quote_in_page(q, txt)
    print(f"evidence_gate.quote_in_page 判定: ok={ok}, why={why}")
    
    # Locate exact substring in raw text
    # Let's clean multiple spaces in q and search in normalized text
    # Or search for key fragment
    frag = " ".join(q.split()[:4]).lower()
    
    # Find position in raw txt
    # Let's search case-insensitively
    pattern = re.escape(q[:40])
    m = re.search(pattern, txt, re.IGNORECASE)
    if not m:
        # Search by simpler fragment
        pattern = re.escape(q.split()[0] + " " + q.split()[1] + " " + q.split()[2])
        m = re.search(pattern, txt, re.IGNORECASE)
        
    if m:
        pos = m.start()
        start = max(0, pos - 80)
        end = min(len(txt), pos + len(q) + 80)
        snippet = txt[start:end].replace('\n', ' ')
        snippet = re.sub(r'\s+', ' ', snippet).strip()
        print(f"摘句在網頁中位置: 第 {pos} 字元")
        print(f"前後 80 字元完整原文:\n  \"{snippet}\"")
    else:
        print(f"未找到位置，搜尋字詞: {frag}")
