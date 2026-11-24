# -*- coding: utf-8 -*-
import requests

secrets_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.secrets.env"
env = {}
with open(secrets_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()

fb_tok = env.get("FB_PAGE_ACCESS_TOKEN")

# 刪除重複的第 2 次發布貼文，保留第 1 次守護神發布的貼文 (1172927288749506)
dup_fb_id = "110505444816362_1172927865416115"
r = requests.delete(f"https://graph.facebook.com/v21.0/{dup_fb_id}?access_token={fb_tok}").json()
print("FB 刪除重複貼文結果:", r)
