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
image_path = hub_dir / "images" / "auction_items_20261116" / "auction_item_3_17912415738586244.jpg"

post_text = """誰能想到幫忙整理生活空間時，
最讓人挪不開眼睛的，居然是這幾只印著復古小花的陶瓷碗盤？✨

早上用軟布一只一只輕輕擦拭乾淨，
放在窗邊木桌上，被台東十一月的陽光照得微溫。
有裝熱湯的大深碗、裝家常菜的平盤，還有帶點年代感的小湯匙。
盛上一碗剛煮好的白飯或熱麵，光看著心裡就很踏實。

與其讓它們鎖在櫃子裡落灰，
不如讓它們重新走進某個家庭的廚房餐桌上。

今天下午兩點開門，人在市區的朋友，
吃完午餐散步經過正氣北路家宅一樓，進來替餐桌帶只漂亮的碗回家吧。

（碗盤均一價 20 元、湯匙 10 元，現場不留物、挑完為止喔💬）

大家平時吃飯，是不是也偏愛這種厚實又有手感的老瓷器呢？"""

first_reply = "（輕輕擦亮一組復古小花湯匙）現場就在台東市正氣北路 166 巷 90 號（生活管家，就醬點！）。下午兩點到五點，散步經過隨時進來坐坐、翻翻老件。自備環保袋跟零錢，挑完為止喔！🍵✨"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply
]

print("🚀 啟動 Threads 全自動社交漫遊與第一波惜物尋寶發布...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
