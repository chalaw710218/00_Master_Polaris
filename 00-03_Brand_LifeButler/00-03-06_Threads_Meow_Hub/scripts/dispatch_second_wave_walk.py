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
image_path = hub_dir / "images" / "auction_items_20261116" / "auction_item_1_18016272158985943.jpg"

post_text = """誰能想到才剛過下午兩點，
正氣北路家宅一樓的鐵捲門才剛拉開，陽光正好灑在門口這排鞋子上？✨

今天現場除了早上的復古花卉碗盤，
這排保存超好的優雅低跟涼鞋，闆仔特別交待「直接免費結緣帶走」，延續它的美麗；
旁邊經典百搭黑鞋跟樂福鞋也只要 30 元一雙（尺寸是 77、78 號）。

本喵早就蹲在門口長凳上負責迎賓監工了喵！🐾
下午在台東市區散步經過的朋友，
進來吹吹電風扇、挑雙合腳的鞋子或帶只漂亮的碗回家吧。

（老規矩：現場不留貨、自備零錢與環保提袋，挑完為止喔！）

大家平時買鞋最在意的也是好走跟百搭嗎？💬"""

first_reply = "🐾 喵編現場帶路：尋寶地址在台東市正氣北路 166 巷 90 號（生活管家，就醬點！）。下午兩點到五點現場都有人，剛吃飽午餐散步過來尋寶剛剛好喵～挑完為止！"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply
]

print("🚀 啟動 Threads 全自動社交漫遊與第二波【現場開門 ✕ 鞋款即時動態】發布...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
