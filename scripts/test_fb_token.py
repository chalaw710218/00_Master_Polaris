# -*- coding: utf-8 -*-
from pathlib import Path
import os
import requests

env_path = Path('.secrets.env')
if not env_path.exists():
    print('❌ .secrets.env 不存在！')
    exit(1)

token = None
for line in env_path.read_text(encoding='utf-8').splitlines():
    line = line.strip()
    if line.startswith('FB_PAGE_ACCESS_TOKEN='):
        token = line.split('=', 1)[1].strip().strip('"').strip("'")

if not token:
    print('❌ 找不到 FB_PAGE_ACCESS_TOKEN！')
    exit(1)

print(f'Token 前 15 碼: {token[:15]}... 總長度: {len(token)}')

# 只讀測試：查詢粉專基本資料 (不發布任何貼文)
page_id = '110505444816362'
url = f'https://graph.facebook.com/v20.0/{page_id}?fields=id,name,category,link&access_token={token}'
try:
    resp = requests.get(url, timeout=10)
    print(f'HTTP Status: {resp.status_code}')
    data = resp.json()
    if resp.status_code == 200:
        print('✅ 金鑰驗證有效！粉專基本資料如下：')
        print(f"  粉專 ID: {data.get('id')}")
        print(f"  粉專名稱: {data.get('name')}")
        print(f"  粉專類別: {data.get('category')}")
        print(f"  粉專連結: {data.get('link')}")
    else:
        print('❌ 金鑰無效或查詢失敗：')
        print(f"  回應內容: {data}")
except Exception as e:
    print(f'❌ 連線異常: {str(e)}')
