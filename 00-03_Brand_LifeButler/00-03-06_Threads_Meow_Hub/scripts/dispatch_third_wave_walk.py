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
image_path = hub_dir / "images" / "auction_items_20261116" / "auction_item_2_18155298982556609.jpg"

post_text = """誰能想到傍晚五點半的台東天色暗得這麼溫柔，
正氣北路家宅一樓的鐵捲門剛緩緩拉下一半，空氣裡全是滿足的安靜。✨

真的很謝謝今天下午特地散步繞過來、進門翻翻老件的脆友跟鄰居。
看著那些印著復古小花的陶瓷碗盤一只只被雙手小心捧走、
合腳的黑鞋與樂福鞋找到願意珍惜它們的新主人，
這大概就是整理生活空間最讓人暖心的事情了。

今天沒趕上的朋友別扼腕——
明天（週二）跟後天（週三）下午兩點到六點，
家宅一樓直接換上第二波「童趣 ✕ 居家生活收納」惜物快閃！🧸📦

TOMICA 消防車背包、小象磁性畫板、小朋友洗澡玩具通通 10 元起；
整排全新袋裝的水槽瀝水架跟廚房防溢蓋直接均一價 10 元帶走。
丟掉太可惜，讓它們在需要的家裡繼續發光。

明天下午散步經過，記得再進來看看生活管家跟喵編喔！

大家家裡是不是也有一樣「雖然用不到、但看到別人好好用著就會很開心」的小物件呢？💬"""

first_reply = "（泡好一壺熱熱的鹿野紅烏龍）今天大家都辛苦了！明天第二波快閃時間一樣在正氣北路 166 巷 90 號家宅一樓（14:00 - 18:00）。自備零錢跟環保袋，我們明天午後見囉！🍵✨"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply
]

print("🚀 啟動 Threads 全自動社交漫遊與第三波【今日現場惜物沉澱 ✕ 明日第二波快閃無縫預告】發布...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
