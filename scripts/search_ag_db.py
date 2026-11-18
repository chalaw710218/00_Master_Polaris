import os

target = "快速找垃圾車程式開發".encode("utf-8")
candidates = []

for base in [os.path.expandvars(r"%APPDATA%"), os.path.expandvars(r"%LOCALAPPDATA%")]:
    if not os.path.exists(base):
        continue
    for item in os.listdir(base):
        if "antigravity" in item.lower() or "gemini" in item.lower():
            candidates.append(os.path.join(base, item))

print("Candidates:", candidates)

found = []
for c in candidates:
    for root, dirs, files in os.walk(c):
        for f in files:
            fp = os.path.join(root, f)
            try:
                if os.path.getsize(fp) < 30 * 1024 * 1024:
                    with open(fp, "rb") as fh:
                        if target in fh.read():
                            found.append(fp)
                            print("FOUND IN:", fp)
            except Exception:
                pass

print("Done. Total found:", len(found))
