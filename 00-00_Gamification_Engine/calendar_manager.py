import sys
import urllib.request
import json
import re
import os
from pathlib import Path
from datetime import datetime, timedelta

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

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

# 系統密鑰配置 (由環境變數讀取)
ICAL_READ_URL = os.environ.get('GOOGLE_CALENDAR_ICAL_URL', '')
GAS_WRITE_URL = os.environ.get('GOOGLE_CALENDAR_GAS_URL', '')

def get_upcoming_events(days_ahead=30):
    """讀取未來指定天數內的行事曆行程"""
    req = urllib.request.Request(ICAL_READ_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"讀取日曆失敗: {e}")
        return []

    events = []
    raw_events = content.split('BEGIN:VEVENT')

    for raw in raw_events[1:]:
        event_data = {}
        lines = raw.splitlines()
        for line in lines:
            if line.startswith('SUMMARY:'):
                event_data['summary'] = line.replace('SUMMARY:', '').strip()
            elif line.startswith('DTSTART'):
                val = line.split(':')[-1].strip()
                event_data['dtstart_raw'] = val
            elif line.startswith('DTEND'):
                val = line.split(':')[-1].strip()
                event_data['dtend_raw'] = val
            elif line.startswith('LOCATION:'):
                event_data['location'] = line.replace('LOCATION:', '').strip()
            elif line.startswith('DESCRIPTION:'):
                event_data['description'] = line.replace('DESCRIPTION:', '').strip()

        if 'summary' in event_data and 'dtstart_raw' in event_data:
            raw_time = event_data['dtstart_raw']
            try:
                if 'T' in raw_time:
                    dt = datetime.strptime(raw_time[:15], '%Y%m%dT%H%M%S')
                else:
                    dt = datetime.strptime(raw_time[:8], '%Y%m%d')
                event_data['start_dt'] = dt
                events.append(event_data)
            except Exception:
                pass

    events.sort(key=lambda x: x['start_dt'])
    return events

def add_calendar_event(title, start_iso, end_iso, description="", location=""):
    """
    透過 Google Apps Script 寫入新行程至 Google 日曆
    時間格式範例：2026-10-15T14:00:00+08:00
    """
    payload = {
        'title': title,
        'startTime': start_iso,
        'endTime': end_iso,
        'description': description,
        'location': location
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        GAS_WRITE_URL,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get('status') == 'success':
                print(f"✅ 行程寫入成功！Event ID: {res_data.get('id')}")
                return True
            else:
                print(f"❌ 寫入失敗: {res_data}")
                return False
    except Exception as e:
        print(f"❌ 網路連線錯誤: {e}")
        return False

if __name__ == '__main__':
    print("【曉】日曆雙向管理器初始化完成。")
