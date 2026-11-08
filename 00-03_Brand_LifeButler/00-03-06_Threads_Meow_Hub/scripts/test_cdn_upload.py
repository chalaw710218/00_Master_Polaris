import sys
from pathlib import Path
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

p = Path("images/shadow_sunday_midnight_tea_desk.jpg")
print(f"測試圖片存在: {p.exists()}，大小: {p.stat().st_size} bytes")

# 1. 測試 Catbox
try:
    with open(p, "rb") as f:
        r = requests.post("https://catbox.moe/user/api.php", data={"reqtype": "fileupload"}, files={"fileToUpload": f}, timeout=25)
    print("Catbox 狀態碼:", r.status_code, "URL:", r.text)
except Exception as e:
    print("Catbox 失敗:", e)

# 2. 測試 Meta Graph API
sys.path.append("scripts")
from threads_publisher import upload_local_image_to_meta_cdn
try:
    meta_url = upload_local_image_to_meta_cdn(p)
    print("Meta CDN URL:", meta_url)
except Exception as e:
    print("Meta CDN 失敗:", e)
