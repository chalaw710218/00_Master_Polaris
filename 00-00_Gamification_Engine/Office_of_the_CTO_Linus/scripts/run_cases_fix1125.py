# 回歸測試（簽章版，只測 prepare）：逐一執行 scripts/tests_fix1125/case_*.md，比對 Exit Code
# 每個案例都在暫存資料夾、用事實庫副本執行；只產生暫存待簽檔，不會動到真正的事實庫或待簽檔
import glob, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "bionic_knowledge_gate.py")
VAULT = os.path.join(HERE, "..", "01_Cognitive_Log", "01_Experiences_and_Evidence.md")
bad = 0
cases = sorted(glob.glob(os.path.join(HERE, "tests_fix1125", "case_*.md")))
for c in cases:
    lines = open(c, encoding="utf-8").read().split("\n")
    label = lines[0].strip()
    if label not in ("【應退回】", "【應通過】"):
        bad += 1; print("FAIL", os.path.basename(c), "第 1 行沒有標記"); continue
    d = tempfile.mkdtemp()
    f = os.path.join(d, "case.md"); open(f, "w", encoding="utf-8").write("\n".join(lines[1:]))
    v = os.path.join(d, "vault.md"); shutil.copy(VAULT, v)
    cmd = [sys.executable, GATE, "prepare", "--file", f, "--vault", v, "--output", os.path.join(d, "s.json")]
    code = subprocess.run(cmd, capture_output=True).returncode
    ok = (code == 0) == (label == "【應通過】")
    if not ok: bad += 1
    print("PASS" if ok else "FAIL", os.path.basename(c), label, "exit", code)
    shutil.rmtree(d, ignore_errors=True)
print(f"案例 {len(cases)} 個，FAIL {bad} 個")
sys.exit(1 if bad or not cases else 0)
