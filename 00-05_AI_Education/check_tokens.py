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

fb_id = env.get("FB_PAGE_ID")
fb_tok = env.get("FB_PAGE_ACCESS_TOKEN")
th_uid = env.get("THREADS_USER_ID")
th_tok = env.get("THREADS_ACCESS_TOKEN")

r_fb = requests.get(f"https://graph.facebook.com/v21.0/{fb_id}?fields=name&access_token={fb_tok}").json()
print("FB Check:", r_fb)

r_th = requests.get(f"https://graph.threads.net/v1.0/me?fields=id,username&access_token={th_tok}").json()
print("Threads Check:", r_th)
