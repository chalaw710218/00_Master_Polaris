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
image_path = hub_dir / "images" / "shadow_thursday_morning_slow_food.jpg"

post_text = """早晨八點多走過台東市區的早市，
阿伯剛把清晨從田裡拔下來的過溝菜蕨和紅藜饅頭擺上木箱。
葉片上還帶著露水，泥土的氣味很乾淨。

國際慢食常講 Good、Clean、Fair，
但在台東，這不是深奧的理論，
只是常民生活裡最樸素的默契：
順著季節吃當季的滋味，
善待土地，也給認真耕作的人一份踏實的尊嚴。

我們每一次選擇吃進肚子裡的東西，
其實都是在為我們想要的在地生活投下一票。

今天大家的早餐都吃了什麼呢？
如果可以，今天也給自己選一份好好對待身體的食物吧。🍵✨

#台東生活 #慢食日常"""

first_reply = "（端上一只溫熱的手作陶杯）在台東生活久了，越懂得好食材不需要太多修飾。早晨大家習慣吃中式蛋餅饅頭，還是西式咖啡麵包呢？留言跟管家分享吧！🍵✨"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply,
    "--k-id", "K-007"
]

print("🚀 啟動 Threads 全自動社交漫遊 v3.0（週四晨間生活管家慢食日常 · 實驗組 K-007）...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
