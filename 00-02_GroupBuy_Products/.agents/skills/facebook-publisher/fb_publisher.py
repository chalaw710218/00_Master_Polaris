import requests
import json
import sys
import os
from pathlib import Path

# ==========================================
# 👑 【生活管家，就醬點！】全自動臉書發布引擎 V2.0
# 功能：多圖發布貼文 + 自動第一留言 (First Comment 導流)
# ==========================================

# 自動載入 .secrets.env
def _load_env():
    p = Path(__file__).resolve()
    for parent in [p] + list(p.parents):
        env_file = parent / '.secrets.env'
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        os.environ.setdefault(k.strip(), v.strip())
            break
_load_env()

PAGE_ID = os.environ.get('FB_PAGE_ID', '110505444816362')
TOKEN = os.environ.get('FB_PAGE_ACCESS_TOKEN', '')

DEFAULT_FIRST_COMMENT = """👉 點擊加入管家專屬 LINE 官方帳號（內有完整系統可直接點選訂購）：
https://lin.ee/z83YSq6

📍【門市取貨資訊】
• 取貨地址：台東市正氣北路166巷90號
• 服務區域：台東市區、知本、南王、都蘭、東河專人配送"""

def publish_post_with_first_comment(message, image_paths=None, first_comment=None):
    """
    發布貼文並自動於下方留下第一則留言
    :param message: 貼文主內文
    :param image_paths: 圖片絕對路徑清單 (list)
    :param first_comment: 第一則留言文字，若為 None 則使用預設值
    """
    media_ids = []
    
    # 1. 上傳圖片 (若有指定圖片)
    if image_paths and len(image_paths) > 0:
        print(f"📸 準備上傳 {len(image_paths)} 張圖片至 Meta 草稿區...")
        for path in image_paths:
            if not os.path.exists(path):
                print(f"⚠️ 找不到檔案: {path}，跳過。")
                continue
            url_photo = f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos'
            try:
                with open(path, 'rb') as f:
                    files = {'source': f}
                    data = {'access_token': TOKEN, 'published': 'false'}
                    r = requests.post(url_photo, files=files, data=data)
                    res = r.json()
                    if 'id' in res:
                        media_ids.append(res['id'])
                        print(f"✅ 圖片上傳成功: {os.path.basename(path)} (ID: {res['id']})")
                    else:
                        print(f"❌ 圖片上傳失敗: {res}")
            except Exception as e:
                print(f"❌ 上傳例外錯誤 {path}: {e}")
    
    # 2. 發布主貼文
    print("🚀 正在發布粉專主貼文...")
    url_feed = f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed'
    payload = {
        'access_token': TOKEN,
        'message': message,
    }
    
    if media_ids:
        for i, mid in enumerate(media_ids):
            payload[f'attached_media[{i}]'] = f'{{"media_fbid":"{mid}"}}'
            
    r_post = requests.post(url_feed, data=payload)
    post_res = r_post.json()
    
    if 'id' not in post_res:
        print(f"❌ 主貼文發布失敗: {post_res}")
        return False, None
        
    post_id = post_res['id']
    print(f"🎉 主貼文發布成功！Post ID: {post_id}")
    
    # 3. 自動發布第一留言 (First Comment 模組)
    comment_text = first_comment if first_comment is not None else DEFAULT_FIRST_COMMENT
    comment_id = None
    if comment_text.strip():
        print("💬 正在自動搶佔第一留言 (First Comment)...")
        url_comment = f'https://graph.facebook.com/v20.0/{post_id}/comments'
        comment_payload = {
            'access_token': TOKEN,
            'message': comment_text
        }
        r_comment = requests.post(url_comment, data=comment_payload)
        comment_res = r_comment.json()
        if 'id' in comment_res:
            comment_id = comment_res['id']
            print(f"✅ 第一留言發布成功！Comment ID: {comment_res['id']}")
        else:
            print(f"⚠️ 第一留言發布未成功: {comment_res}")
            
    # 4. 全自動不漏接歸檔 Hook (寫入 00-03-05 歷史總庫)
    _auto_archive_post(post_id, message, image_paths, comment_text, comment_id)
            
    return True, post_id

def _auto_archive_post(post_id, message, image_paths=None, comment_text=None, comment_id=None):
    """發布成功後，全自動追加寫入 00-03-05 社群全集總庫，確保 100% 零漏接"""
    try:
        from datetime import datetime
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p = Path(__file__).resolve()
        archive_path = None
        for parent in [p] + list(p.parents):
            target = parent / "00-03_Brand_LifeButler" / "00-03-05_Brand_Content_Hub" / "00_Social_Posts_Master_Archive.md"
            if target.exists():
                archive_path = target
                break
        if not archive_path:
            return
            
        first_line = message.strip().split('\n')[0][:50]
        entry = f"""

---

### 📝 【自動補登】Facebook 貼文 ({now_str})
* **發布日期**：{now_str} ｜ **平台**：Facebook 粉專「生活的一部分，就醬點！」
* **貼文 ID**：`{post_id}`{f" ｜ **第一留言 ID**：`{comment_id}`" if comment_id else ""}
* **主題摘要**：{first_line}...
* **搭配素材**：{image_paths if image_paths else "純文字貼文"}
* **【發布全文】**：
```text
{message}
```
"""
        if comment_text:
            entry += f"""* **【第一則留言 (First Comment)】**：
```text
{comment_text}
```
"""
        with open(archive_path, 'a', encoding='utf-8') as f:
            f.write(entry)
        print(f"🗄️ [自動歸檔] 已無縫同步寫入 00-03-05 社群發布歷史總庫！")
    except Exception as e:
        print(f"⚠️ 自動歸檔略過 (不影響主發布流程): {e}")

if __name__ == '__main__':
    print("臉書自動發文機 V2.0 (含第一留言模組) 測試載入完成。")
