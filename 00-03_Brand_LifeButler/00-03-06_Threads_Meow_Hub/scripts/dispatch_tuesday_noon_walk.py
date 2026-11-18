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
image_path = hub_dir / "images" / "meow_tuesday_noon_loaf_bento.jpg"

post_text = """正午十二點多，巷口便當店排骨剛起鍋的香氣飄過來了。
本喵把小灰爪往胸口一折，在木窗台前瞇著眼曬太陽。

人類到了中午好像都在看時鐘、排隊等外帶，
但對店貓來說，世界的步調很簡單：
有陽光、有海風，還有廚房飄來的飯菜香。

今天中午大家都吃什麼好料呢？
吃飽了記得喘口氣，像本喵一樣原地折手手放空一下吧。🐾 #台東生活"""

first_reply = "（探出毛毛頭）中午太陽大，外出買便當記得戴帽子多喝水喵！下午繼續替大家隔空加油打氣🐾"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply,
    "--k-id", "K-002"
]

print("🚀 啟動 Threads 全自動社交漫遊 v3.0（週二正午店貓便當漫遊）...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
