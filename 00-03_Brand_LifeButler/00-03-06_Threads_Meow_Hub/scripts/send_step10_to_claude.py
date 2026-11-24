import subprocess
import sys
from pathlib import Path

RELAY_SCRIPT = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\scripts\claude_relay.py")
MSG_FILE = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts\step10_message.txt")

msg = MSG_FILE.read_text(encoding="utf-8")

cmd = [
    sys.executable,
    str(RELAY_SCRIPT),
    "--ag", "62615c83-54cd-4585-ac6a-95745b9ac34a",
    "--name", "影",
    msg
]

print("正在傳送回覆給 Claude (靠的) ...")
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
print("Return code:", res.returncode)
print("Stdout:")
print(res.stdout)
if res.stderr:
    print("Stderr:")
    print(res.stderr)
