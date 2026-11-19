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
image_path = hub_dir / "images" / "shadow_thursday_dusk_errand_bag.jpg"

post_text = """傍晚六點多，天色從金黃慢慢沈入深藍。
騎車到巷口幫阿公把剛採的地瓜葉和常備菜提進屋裡，
阿公笑著說：「下班啦？今天風涼，騎車慢一點。」

在台東做生活管家這些日子，最深的體會是：
所謂安心的生活，
不是家裡多了多少科技設備，
而是知道門外隨時有人照看、有熟悉的鄰里能搭上一把手。

不管是幫忙提一袋重物、順路丟包垃圾，或是下班時的一句問候。
天色暗下來的時候，願每個人的家門口都有一盞溫暖的燈。

今晚下班的你，回到家了嗎？
吃上一頓熱騰騰的晚餐，卸下一整天的疲憊吧。🍲✨

#台東生活"""

first_reply = "（在玄關幫大家把鞋子擺齊）下班後的時光是屬於自己的。不管今天過得順不順利，回到家先喝口溫水、把外套掛好。生活管家在後排替大家守著這份平靜～大家今晚吃什麼家常菜呢？🍵✨"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply,
    "--k-id", "K-009"
]

print("🚀 啟動 Threads 全自動社交漫遊 v3.0（週四黃昏生活管家下班守候 · 實驗組 K-009）...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
