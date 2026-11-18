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
image_path = hub_dir / "images" / "meow_wednesday_morning_stretch.jpg"

post_text = """（在老木地板的晨光光斑裡慢慢伸個長長的大懶腰）

早晨的風吹進木窗，帶著一點點涼意。
太陽剛爬過屋頂，把木地板曬得暖暖的。

管家剛剛把店門拉開，
廚房裡傳來電鍋跳起的一聲「啵」。

新的一天又開始了。
今天不用太著急，先深呼吸一口氣，
把肩膀放鬆，像本喵一樣先把腰伸開再說。

大家早安！今天出門記得帶件外套喔。🐾

#台東生活 #耍廢日常"""

first_reply = "（把小腦袋湊到罐頭旁邊嗅了嗅）早晨最重要的事：早餐一定要吃飽飽！大家今天早餐都吃什麼呢？🐾"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply,
    "--k-id", "control"
]

print("🚀 啟動 Threads 全自動社交漫遊 v3.0（週三晨間店貓伸懶腰 · 規則3每日原生對照組 control）...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
