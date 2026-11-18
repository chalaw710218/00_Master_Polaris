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
image_path = hub_dir / "images" / "meow_wednesday_afternoon_tea.jpg"

post_text = """（把兩隻白爪子輕輕搭在檜木桌沿，耳朵動了一下）

午後兩點多，管家拎起熱水壺，
熱水順著細細的壺嘴倒進厚陶杯裡。

茶葉在水裡慢慢旋開、沉到底部，
一小縷白色熱氣順著窗邊的陽光往上飄。

沒有華麗的大道理，
生活就是把水燒開、把茶泡好、把手邊的小事一件一件做整齊。

聞到茶香，腦袋好像跟著清醒了一點。
下午還有半天，慢慢做、不著急。🐾

#台東生活 #耍廢日常"""

first_reply = "（伸舌頭舔舔嘴唇）水很燙，本喵先幫大家吹吹涼！下午累了記得站起來伸個懶腰喔🐾"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply,
    "--k-id", "K-006"
]

print("🚀 啟動 Threads 全自動社交漫遊 v3.0（週三午後店貓聞茶香 · K-006 去AI腔具體感官動詞描摹）...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
