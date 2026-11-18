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
image_path = hub_dir / "images" / "meow_wednesday_noon_third_place.jpg"

post_text = """（把兩隻小前爪收在白胸脯底下，折手手趴在木凳上）

正午十二點半，巷子裡的陽光正好。
隔壁阿姨提著剛買好的雞腿便當走進來，
坐在門口長凳上吹電風扇喘口氣，順手摸了摸本喵的頭。

不用刻意找話題，也不用談什麼大道理。
在這裡，大家只是暫時把工作與忙碌放下，
喝一口溫溫的茶，聊一句「今天的青菜很甜喔」。

在生活裡，除了家和上班的地方，
好像真的需要一個這樣隨時能走進來歇歇腳的角落。

中午太陽大，大家吃飽記得多喝水。
本喵在木凳上繼續幫大家看店放空喔。🐾

#台東生活 #第三空間"""

first_reply = "（呼嚕嚕瞇瞇眼）走累了隨時推門進來坐坐！大家今天中午吃了什麼好料呢？🐾"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply,
    "--k-id", "K-005"
]

print("🚀 啟動 Threads 全自動社交漫遊 v3.0（週三正午店貓母雞蹲 · K-005 第三空間與社區弱連結信任）...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
