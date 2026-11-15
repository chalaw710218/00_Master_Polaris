import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
HUB_DIR = SCRIPT_DIR.parent

text_file = HUB_DIR / "data" / "draft_monday_midnight_meow_v2.txt"
reply_file = HUB_DIR / "data" / "reply_monday_midnight_meow_v2.txt"

text = text_file.read_text(encoding="utf-8")
reply = reply_file.read_text(encoding="utf-8")

def run_walk(img_path=None):
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "execute_autonomous_walk_v3.py"),
        "--text", text,
        "--reply", reply,
        "--topic", "台東生活"
    ]
    if img_path and Path(img_path).exists():
        cmd.extend(["--image", str(img_path)])

    res = subprocess.run(cmd)
    return res.returncode

if __name__ == "__main__":
    img = sys.argv[1] if len(sys.argv) > 1 else None
    sys.exit(run_walk(img))
