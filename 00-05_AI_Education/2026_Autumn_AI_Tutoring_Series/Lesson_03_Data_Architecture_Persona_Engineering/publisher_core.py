# -*- coding: utf-8 -*-
"""
發布腳本模組：Post 02, Post 03, Post 04
"""
import os
import requests
import time

secrets_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.secrets.env"
env = {}
with open(secrets_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()

FB_PAGE_ID = env.get("FB_PAGE_ID", "110505444816362")
FB_PAGE_TOKEN = env.get("FB_PAGE_ACCESS_TOKEN", "")
TH_UID = env.get("THREADS_USER_ID", "29191709603824305")
TH_TOK = env.get("THREADS_ACCESS_TOKEN", "")

def publish_post(image_path, fb_caption, fb_comment, th_caption, th_comment, label=""):
    print(f"\n🚀 [發射台] 開始發布 {label} ...")
    
    # Facebook
    url_fb_photo = f"https://graph.facebook.com/v21.0/{FB_PAGE_ID}/photos"
    with open(image_path, "rb") as img_file:
        res_fb = requests.post(url_fb_photo, files={"source": img_file}, data={
            "caption": fb_caption,
            "access_token": FB_PAGE_TOKEN
        }).json()
    
    fb_post_id = res_fb.get("post_id") or res_fb.get("id")
    if not fb_post_id:
        print(f"❌ [FB] 發布失敗: {res_fb}")
        return False
    print(f"🎉 [FB] 主貼文成功: {fb_post_id}")
    
    # CDN URL
    photo_id = res_fb.get("id")
    r_pinfo = requests.get(f"https://graph.facebook.com/v21.0/{photo_id}?fields=images&access_token={FB_PAGE_TOKEN}").json()
    cdn_url = r_pinfo.get("images", [{}])[0].get("source", "")
    
    # FB Comment
    time.sleep(2)
    requests.post(f"https://graph.facebook.com/v21.0/{fb_post_id}/comments", data={
        "message": fb_comment,
        "access_token": FB_PAGE_TOKEN
    })
    print(f"💬 [FB] 第一則留言成功！")
    
    # Threads
    url_th = f"https://graph.threads.net/v1.0/{TH_UID}/threads"
    res_th = requests.post(url_th, data={
        "media_type": "IMAGE",
        "image_url": cdn_url,
        "text": th_caption,
        "access_token": TH_TOK
    }).json()
    
    th_cid = res_th.get("id")
    if th_cid:
        time.sleep(5)
        res_pub = requests.post(f"https://graph.threads.net/v1.0/{TH_UID}/threads_publish", data={
            "creation_id": th_cid,
            "access_token": TH_TOK
        }).json()
        th_pid = res_pub.get("id")
        print(f"🎉 [Threads] 推播成功: {th_pid}")
        
        # Threads Comment
        time.sleep(2)
        r_rep = requests.post(url_th, data={
            "media_type": "TEXT",
            "text": th_comment,
            "reply_to_id": th_pid,
            "access_token": TH_TOK
        }).json()
        if "id" in r_rep:
            time.sleep(2)
            requests.post(f"https://graph.threads.net/v1.0/{TH_UID}/threads_publish", data={
                "creation_id": r_rep["id"],
                "access_token": TH_TOK
            })
            print(f"💬 [Threads] 第一則留言成功！")
            
    print(f"🎯 {label} 雙平台發布大圓滿！")
    return True
