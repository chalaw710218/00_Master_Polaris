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
image_path = hub_dir / "images" / "meow_tuesday_afternoon_ceramic_table.jpg"

post_text = """午後三點半的斜陽，剛好把桌上那只厚陶杯曬得溫溫的。
杯口有些洗了幾百次的歲月痕跡，摸起來特別順手。

本喵把小下巴靠在老木桌邊，聽著茶水倒進陶杯裡清脆的聲音。
比起那些亮晶晶的精緻瓷器，
天天拿在手裡盛熱水、泡茶的質樸老件，好像更能裝下生活裡的踏實。

下午稍微歇口氣吧！
泡杯茶，摸摸身邊那些陪伴你很久的生活小物，
日子就在這些微小的溫暖裡慢慢發亮。🐾 #台東生活"""

first_reply = "（用毛茸茸的臉頰輕輕蹭蹭陶杯）午後容易犯睏，起來喝口熱茶潤潤喉喵！本喵在店裡替大家守著陽光🐾"

cmd = [
    sys.executable,
    str(script_path),
    "--text", post_text,
    "--image", str(image_path),
    "--topic", "台東生活",
    "--reply", first_reply,
    "--k-id", "K-003"
]

print("🚀 啟動 Threads 全自動社交漫遊 v3.0（週二午後店貓陶杯漫遊）...")
res = subprocess.run(cmd, text=True, encoding="utf-8")
sys.exit(res.returncode)
