import difflib
from pathlib import Path

p = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts\bionic_knowledge_gate.py")
old_content = p.read_text(encoding="utf-8")

target = 'DEFAULT_EXPERIENCES_PATH = Path(__file__).resolve().parent.parent / "01_Cognitive_Log" / "01_Experiences_and_Evidence.md"'
repl = 'DEFAULT_EXPERIENCES_PATH = Path(__file__).resolve().parent.parent / "data" / "fact_bank.md"'

if target not in old_content:
    raise ValueError("Target not found")

new_content = old_content.replace(target, repl, 1)
p.write_text(new_content, encoding="utf-8")

diff = difflib.unified_diff(
    old_content.splitlines(keepends=True),
    new_content.splitlines(keepends=True),
    fromfile="kage/bionic_knowledge_gate.py",
    tofile="kage/bionic_knowledge_gate_default_factbank.py"
)
diff_txt = "".join(diff)
print("Updated DEFAULT_EXPERIENCES_PATH. Diff:")
print(diff_txt)
Path("scripts/gate_vault_diff.txt").write_text(diff_txt, encoding="utf-8")
