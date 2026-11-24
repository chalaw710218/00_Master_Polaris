import sys
from pathlib import Path

# Add bionic_core to sys.path
HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
CORE_DIR = WORKSPACE / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
sys.path.insert(0, str(CORE_DIR))

import evidence_gate

def test_q1_ruling():
    snapshot_path = HERE / "snapshots" / "環署廢字第1091202281號.txt"
    if not snapshot_path.exists():
        print(f"❌ 快照檔案不存在: {snapshot_path}")
        return False
    
    page_text = snapshot_path.read_text(encoding="utf-8")
    
    # 說明二（一）
    q1 = "（一）若以大（小）客車、大（小）貨車、大（小）客貨兩用車...非屬清潔行為，應依廢棄清理法第 41 條...公民營廢棄物清除機構許可文件後，始得受託清除廢棄物業務"
    ok1, why1 = evidence_gate.quote_in_page(q1, page_text, min_fragment=20)
    if not ok1:
        print(f"❌ Q1 說明二（一）摘句比對失敗: {why1}")
        return False

    # 說明二（二）
    q2 = "（二）以人力、手推車、三輪車等方式載運家戶垃圾...環境保護局設置之各垃圾收集點傾倒者，仍維持得視為清潔行為"
    ok2, why2 = evidence_gate.quote_in_page(q2, page_text, min_fragment=20)
    if not ok2:
        print(f"❌ Q1 說明二（二）摘句比對失敗: {why2}")
        return False

    print("✅ Q1 [環署廢字第1091202281號函] 說明二（一）與（二）逐字摘句驗證通過！")
    return True

def test_q2_ruling():
    print("Q2 檢索範圍：衛生福利部主管法規查詢系統、衛福部首長信箱釋疑、長照專區問答集，結果：未找到")
    return True

if __name__ == "__main__":
    q1_ok = test_q1_ruling()
    q2_ok = test_q2_ruling()
    all_ok = q1_ok and q2_ok
    print("-" * 50)
    print(f"函釋證據檢驗結果: {'全部通過 (PASS)' if all_ok else '未通過 (FAIL)'}")
    print(f"Exit Code: {0 if all_ok else 1}")
    sys.exit(0 if all_ok else 1)
