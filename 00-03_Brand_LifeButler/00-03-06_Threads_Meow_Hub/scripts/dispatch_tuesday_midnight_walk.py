import sys
import subprocess
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

hub_dir = Path(__file__).resolve().parent.parent
script_path = hub_dir / "scripts" / "execute_autonomous_walk_v3.py"
image_path = hub_dir / "images" / "meow_tuesday_midnight_box_sleep.jpg"

post_text = """外面的路燈光線靜靜照在老木地板上。
街道上的車聲慢慢停了，
只剩下客廳角落均勻微小的呼嚕聲。

不管今天忙得怎麼樣、事情有沒有全部做完，
到了這個時間，都可以先安心放下了。

給自己蓋好被子，把手機調成靜音。
明天的事，明天醒來再說吧。

晚安台東，大家做個溫暖的好夢。🐾

#台東生活 #耍廢日常"""

first_reply = "（把小鼻子埋進白爪子裡蹭蹭）夜深了，店裡的燈都關好囉！大家快去睡覺，明天見喵🐾"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply,
    "--k-id", "control"
]

print("🚀 啟動 Threads 全自動社交漫遊 v3.0（週二深夜店貓紙箱安睡 · 原生對照組 []）...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
