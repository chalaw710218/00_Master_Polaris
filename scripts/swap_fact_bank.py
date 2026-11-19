import hashlib
import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
COG_LOG_DIR = PROJECT_ROOT / "00-00_Gamification_Engine" / "Office_of_the_CEO_Yuki" / "01_Cognitive_Log"

ORIG_FILE = COG_LOG_DIR / "01_Experiences_and_Evidence.md"
BACKUP_FILE = COG_LOG_DIR / "_未驗證封存" / "01_Experiences_and_Evidence_原檔_20261120.md"
V2_FILE = COG_LOG_DIR / "01_Experiences_and_Evidence_v2.md"


def get_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not ORIG_FILE.is_file():
        print(f"錯誤：找不到原檔 {ORIG_FILE}", file=sys.stderr)
        sys.exit(1)
    if not BACKUP_FILE.is_file():
        print(f"錯誤：找不到備份檔 {BACKUP_FILE}", file=sys.stderr)
        sys.exit(1)
    if not V2_FILE.is_file():
        print(f"錯誤：找不到 v2 檔 {V2_FILE}", file=sys.stderr)
        sys.exit(1)

    # 步驟 a: 比對備份檔與現在原檔的 sha256
    backup_sha = get_sha256(BACKUP_FILE)
    orig_sha_before = get_sha256(ORIG_FILE)

    if backup_sha != orig_sha_before:
        print("備份對不上，停止")
        sys.exit(1)

    step_a_result = "相同（備份與原檔完全一致）"

    # 步驟 b: 將 v2 內容複製成 01_Experiences_and_Evidence.md（覆蓋）
    v2_bytes = V2_FILE.read_bytes()
    ORIG_FILE.write_bytes(v2_bytes)

    # 步驟 c: 重新計算新的 01_Experiences_and_Evidence.md 和 v2 的 sha256 是否相同
    orig_sha_after = get_sha256(ORIG_FILE)
    v2_sha = get_sha256(V2_FILE)
    step_c_result = "是" if (orig_sha_after == v2_sha) else "否"

    # 步驟 d: 再算一次備份檔 sha256，確認備份沒被動到
    backup_sha_after = get_sha256(BACKUP_FILE)
    if backup_sha != backup_sha_after:
        print("錯誤：備份檔在替換過程中被改動！", file=sys.stderr)
        sys.exit(1)
    step_d_sha16 = backup_sha_after[:16]

    # 計算新事實庫的條目數（用 ### [序號 數一次）
    new_text = ORIG_FILE.read_text(encoding="utf-8")
    entry_count = len(re.findall(r"^### \[序號", new_text, re.MULTILINE))

    # 印出結果
    print("=" * 40)
    print(f"步驟 a 比對結果: {step_a_result}")
    print(f"步驟 c 結果: {step_c_result}")
    print(f"步驟 d 備份 sha256 前 16 碼: {step_d_sha16}")
    print(f"新事實庫的條目數: {entry_count}")
    print("=" * 40)
    print(f"已成功由 v2 覆蓋: {ORIG_FILE}")
    print(f"v2 檔保留: {V2_FILE}")
    print(f"備份檔完好: {BACKUP_FILE}")


if __name__ == "__main__":
    main()
