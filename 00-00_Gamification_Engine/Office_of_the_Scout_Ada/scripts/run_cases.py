# 回歸測試：逐一執行 scripts/tests/case_*.md，比對門禁的 Exit Code 是否符合標記
# 案例第 1 行必須是【應退回】或【應通過】；第 2 行若是「模式：check」則跑 check，否則跑 prepare
# 每個案例都在暫存資料夾、用目前事實庫的副本執行，不會動到真正的事實庫
import glob, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "bionic_knowledge_gate.py")
VAULT = os.path.join(HERE, "..", "01_Cognitive_Log", "01_事實庫.md")
bad = 0
cases = sorted(glob.glob(os.path.join(HERE, "tests", "case_*.md")))
for c in cases:
    lines = open(c, encoding="utf-8").read().split("\n")
    label = lines[0].strip()
    if label not in ("【應退回】", "【應通過】"):
        bad += 1; print("FAIL", os.path.basename(c), "第 1 行沒有標記"); continue
    mode = "check" if lines[1].strip() == "模式：check" else "prepare"
    body = "\n".join(lines[2:] if mode == "check" else lines[1:])
    d = tempfile.mkdtemp()
    f = os.path.join(d, "case.md"); open(f, "w", encoding="utf-8").write(body)
    if mode == "check":
        cmd = [sys.executable, GATE, "check", "--file", f]
    else:
        v = os.path.join(d, "vault.md"); shutil.copy(VAULT, v)
        cmd = [sys.executable, GATE, "prepare", "--file", f, "--vault", v, "--output", os.path.join(d, "s.json")]
    code = subprocess.run(cmd, capture_output=True).returncode
    ok = (code == 0) == (label == "【應通過】")
    if not ok: bad += 1
    print("PASS" if ok else "FAIL", os.path.basename(c), label, "exit", code)
    shutil.rmtree(d, ignore_errors=True)
print(f"案例 {len(cases)} 個，FAIL {bad} 個")
sys.exit(1 if bad or not cases else 0)
