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
image_path = hub_dir / "images" / "meow_tuesday_dusk_breeze.jpg"

post_text = """天色暗得比昨天早了一點點。
台東街角的路燈，剛才一盞一盞亮起來了。

下班下課的機車聲，慢慢多了一點。
有人提著熱騰騰的便當，
有人牽著腳踏車慢慢踩過路口。

滑了一整天的手機，
眼睛應該也有點酸了吧？

先把螢幕放下來。
轉一轉脖子，喝口溫水，
吹一下傍晚這陣剛剛好的涼風。

晚餐記得好好吃。
今天大家辛苦了，下班快樂。🐾

#台東生活"""

first_reply = "（趴在木凳上甩甩尾巴）天黑之後風變涼了，出門買晚餐要順手抓件薄外套喔！今晚大家都打算吃什麼呢？🐾"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply,
    "--k-id", "K-004"
]

print("🚀 啟動 Threads 全自動社交漫遊 v3.0（週二黃昏店貓吹風漫遊 · K-004 人因排版工學）...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
