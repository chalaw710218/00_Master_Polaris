import difflib
from pathlib import Path

src_p = Path(r"C:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_Gamification_Engine/Office_of_the_CEO_Yuki/scripts/bionic_knowledge_gate.py")
dst_p = Path(r"c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/bionic_knowledge_gate.py")

src_lines = src_p.read_text(encoding="utf-8").splitlines(keepends=True)
dst_lines = []
for line in src_lines:
    l = line
    l = l.replace("執行長雪", "生活管家影")
    l = l.replace('"office": "yuki"', '"office": "kage"')
    l = l.replace('data.get("office", "yuki")', 'data.get("office", "kage")')
    dst_lines.append(l)

dst_p.write_text("".join(dst_lines), encoding="utf-8")
print("Written successfully. Diff:")
diff = difflib.unified_diff(src_lines, dst_lines, fromfile="yuki/bionic_knowledge_gate.py", tofile="kage/bionic_knowledge_gate.py", lineterm="")
for d in diff:
    print(d)
