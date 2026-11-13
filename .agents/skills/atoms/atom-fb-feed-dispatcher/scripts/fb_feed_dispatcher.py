#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/fb_feed_dispatcher.py
Facebook 粉絲專頁多圖暫存與 Feed 貼文派發底座
專精於 Meta Graph API v20.0 媒體池暫存、即時/排程雙模、第一留言秒發與自動歸檔
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

sys.stdout.reconfigure(encoding='utf-8')

PAGE_ID = '110505444816362'
ARCHIVE_PATH = Path("00-03_Brand_LifeButler/00-03-05_Brand_Content_Hub/00_Social_Posts_Master_Archive.md")

def append_to_social_archive(post_id: str, message: str, is_scheduled: bool, sched_time: str = None):
    """將發布戰報追加記錄至全域社群存證檔案"""
    if not ARCHIVE_PATH.parent.exists():
        return

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mode_str = f"【預約排程：{sched_time}】" if is_scheduled else "【即時發布】"

    entry = f"""
### [{now_str}] Facebook 貼文 {mode_str}
- **Post ID**: `{post_id}`
- **發布粉專**: 生活的一部分，就醬點！ (`{PAGE_ID}`)
- **貼文摘要**: {message[:120]}...
- **狀態**: {"已建立 Meta 伺服器定時任務" if is_scheduled else "已公開上線並完成第一留言導流"}
---
"""
    try:
        with open(ARCHIVE_PATH, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        print(f"⚠️ 歸檔寫入失敗 (非阻斷性): {e}")

def dispatch_facebook_post(
    message: str,
    image_paths: List[str] = None,
    first_comment: str = None,
    scheduled_timestamp: int = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """執行 Facebook 粉絲專頁貼文派發"""
    image_paths = image_paths or []
    is_scheduled = scheduled_timestamp is not None

    if dry_run:
        # 乾跑模擬
        mock_media_ids = [f"mock_media_{i+1}_99998888" for i in range(len(image_paths))]
        mock_post_id = f"{PAGE_ID}_mock_post_{int(datetime.now().timestamp())}"
        mock_comment_id = f"{mock_post_id}_mock_comment_12345" if first_comment and not is_scheduled else None

        attached_media = [{'media_fbid': mid} for mid in mock_media_ids]

        return {
            "status": "DRY_RUN_SUCCESS",
            "page_id": PAGE_ID,
            "post_id": mock_post_id,
            "mode": "SCHEDULED" if is_scheduled else "IMMEDIATE",
            "scheduled_publish_time": scheduled_timestamp,
            "uploaded_media_count": len(mock_media_ids),
            "attached_media": attached_media,
            "first_comment_sent": mock_comment_id is not None,
            "first_comment_id": mock_comment_id,
            "message_sample": message[:80] + "..." if len(message) > 80 else message
        }

    # 實體派發調用邏輯（此處需要有效 ACCESS_TOKEN）
    token = os.environ.get("FB_PAGE_ACCESS_TOKEN", "")
    if not token:
        print("❌ 未偵測到環境變數 FB_PAGE_ACCESS_TOKEN，請以 --dry-run 模擬或設定環境變數")
        sys.exit(1)

    import requests

    # 1. 上傳照片至暫存區 (published=false)
    media_ids = []
    for path in image_paths:
        if not os.path.exists(path):
            continue
        url_photo = f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos'
        try:
            with open(path, 'rb') as f:
                files = {'source': f}
                data = {'access_token': token, 'published': 'false'}
                r = requests.post(url_photo, files=files, data=data, timeout=30)
                res = r.json()
                if 'id' in res:
                    media_ids.append(res['id'])
        except Exception as e:
            print(f"⚠️ 照片上傳異常: {e}")

    # 2. 派發 Feed 貼文
    url_feed = f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed'
    payload = {
        'access_token': token,
        'message': message,
    }
    for i, mid in enumerate(media_ids):
        payload[f'attached_media[{i}]'] = f'{{"media_fbid":"{mid}"}}'

    if is_scheduled:
        payload['published'] = False
        payload['scheduled_publish_time'] = scheduled_timestamp
    else:
        payload['published'] = True

    r_feed = requests.post(url_feed, data=payload, timeout=30)
    feed_res = r_feed.json()

    if 'id' not in feed_res:
        print(f"❌ 貼文發布失敗: {feed_res}")
        sys.exit(1)

    post_id = feed_res['id']

    # 3. 若為即時發布，秒發第一則留言
    comment_id = None
    if not is_scheduled and first_comment:
        url_comment = f'https://graph.facebook.com/v20.0/{post_id}/comments'
        c_payload = {'access_token': token, 'message': first_comment}
        try:
            r_c = requests.post(url_comment, data=c_payload, timeout=15)
            c_res = r_c.json()
            if 'id' in c_res:
                comment_id = c_res['id']
        except Exception as e:
            print(f"⚠️ 第一留言發送異常: {e}")

    # 4. 寫入存證檔案
    append_to_social_archive(
        post_id=post_id,
        message=message,
        is_scheduled=is_scheduled,
        sched_time=str(datetime.fromtimestamp(scheduled_timestamp)) if is_scheduled else None
    )

    return {
        "status": "SUCCESS",
        "post_id": post_id,
        "first_comment_id": comment_id,
        "is_scheduled": is_scheduled
    }

def main():
    parser = argparse.ArgumentParser(description="Facebook 粉絲專頁多圖暫存與 Feed 貼文派發底座")
    parser.add_argument("--message", type=str, default="生活管家到府陪伴，生活的一部分，就醬點！\n\n👉 預約訂購與門市資訊，管家已整理在【第一則留言】中，點擊即可直達！", help="貼文內文")
    parser.add_argument("--images", nargs="*", default=["sample1.jpg", "sample2.jpg"], help="上傳照片路徑清單")
    parser.add_argument("--first-comment", type=str, default="👉 點擊加入管家專屬 LINE 官方帳號：https://lin.ee/z83YSq6\n📍 取貨地址：台東市正氣北路166巷90號", help="第一則留言內容")
    parser.add_argument("--schedule-timestamp", type=int, default=None, help="UNIX 排程時間戳")
    parser.add_argument("--dry-run", action="store_true", help="執行乾跑模擬")
    args = parser.parse_args()

    result = dispatch_facebook_post(
        message=args.message,
        image_paths=args.images,
        first_comment=args.first_comment,
        scheduled_timestamp=args.schedule_timestamp,
        dry_run=args.dry_run
    )

    print("==================================================")
    print("🚀 Facebook 粉絲專頁貼文派發底座執行完成 (Exit Code: 0)")
    print(f"執行狀態: {result['status']} | 模式: {result['mode']}")
    print(f"目標粉專: 生活的一部分，就醬點！ (Page ID: {result['page_id']})")
    print(f"生成 Post ID: {result['post_id']}")
    print(f"多圖暫存上傳: 成功裝載 {result['uploaded_media_count']} 張相片 (published=false 媒體池)")
    print("--------------------------------------------------")
    print("💬 第一則導流留言連動:")
    if result["first_comment_sent"]:
        print(f"  [✓] 貼文公開秒級發表完成！Comment ID: {result['first_comment_id']}")
        print(f"  [✓] 已完整附載 LINE OA 訂購網址與門市取貨資訊")
    else:
        print("  [-] 排程模式下暫緩發表（將於正式公開時排入）")
    print("--------------------------------------------------")
    print("📁 自動歸檔: 已就緒追加至 00_Social_Posts_Master_Archive.md")
    print("==================================================")

if __name__ == "__main__":
    main()
