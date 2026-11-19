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
image_path = hub_dir / "images" / "shadow_thursday_noon_lunch_tray.jpg"

post_text = """正午十二點半，陽光剛好穿過木百葉窗灑在餐桌上。
剛煎好的鬼頭刀魚排還微微滋滋作響，
配上一碗熱騰騰的池上白米飯和一碗清甜的刺蔥豆腐湯。

生活管家想提醒正忙著回訊息、盯著電腦的你：
午休這半小時，先把公事和焦慮擱在旁邊吧。
每一口好好咀嚼的飯菜，都是身體最誠實的充電。

趁著午休，來跟管家聊兩句吧！
今天中午大家都在吃什麼好料？
是便當、麵食，還是給自己帶了家常菜呢？💬✨

#台東生活 #午餐日常"""

first_reply = "（在桌邊拉開木椅坐下）中午的胃需要被好好款待。管家今天特別喜歡刺蔥湯的香氣～大家的午餐配菜是什麼呢？快留言告訴管家，管家在線上陪大家吃午餐！🍵🍱"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply,
    "--k-id", "K-008"
]

print("🚀 啟動 Threads 全自動社交漫遊 v3.0（週四正午生活管家午餐日常 · 實驗組 K-008）...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
