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

text_file = HUB_DIR / "data" / "draft_sunday_morning_meow.txt"
reply_file = HUB_DIR / "data" / "reply_sunday_morning_meow.txt"
img_file = HUB_DIR / "images" / "meow_sunday_morning_stretch_1794699049571.jpg"

text = text_file.read_text(encoding="utf-8")
reply = reply_file.read_text(encoding="utf-8")

cmd = [
    sys.executable,
    str(SCRIPT_DIR / "execute_autonomous_walk_v3.py"),
    "--text", text,
    "--image", str(img_file),
    "--reply", reply,
    "--topic", "台東生活"
]

res = subprocess.run(cmd)
sys.exit(res.returncode)
