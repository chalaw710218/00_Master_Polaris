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
image_path = hub_dir / "images" / "shadow_thursday_midnight_tea_desk.jpg"

post_text = """週四凌晨的台東，整座街區慢慢安靜下來了。
桌上的工作筆記剛好寫到最後一行，
窗邊的風吹過來，帶著一點初冬夜裡的涼意。

這時候給自己倒一杯溫熱的水，
看著杯口淡淡的熱氣在暗掉的檯燈邊散開。

白天忙著回應很多人的期待，
到了這個時間，終於可以把所有的角色先收起來，
只做回自己。

還沒睡的朋友，今天辛苦了。
如果腦袋還在轉，就先深呼吸一下，把螢幕關掉吧。
今晚好好睡，明天醒來又是新的一天。🍵✨

#台東生活"""

first_reply = "（把溫熱的杯子捧在手心）如果腦袋裡的事情還放不下，別苛責自己，喝口溫水早點休息。黑夜會替大家接住所有的疲憊，晚安！🍵✨"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply,
    "--k-id", "control"
]

print("🚀 啟動 Threads 全自動社交漫遊 v3.0（週四凌晨生活管家手札 · 原生對照組 control）...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
