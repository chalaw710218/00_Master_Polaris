import urllib.request
import re
import os
from pathlib import Path
from datetime import datetime

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

ICAL_URL = os.environ.get('GOOGLE_CALENDAR_ICAL_URL', '')

def fetch_and_parse_calendar():
    req = urllib.request.Request(ICAL_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"連線失敗: {e}")
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
                event_data['dt'] = dt
                events.append(event_data)
            except Exception:
                pass

    events.sort(key=lambda x: x['dt'])
    return events

if __name__ == '__main__':
    events = fetch_and_parse_calendar()
    print(f"總共抓取到 {len(events)} 筆行程記錄：\n")
    now = datetime(2026, 10, 12) # 系統基準時間
    
    print("--- 過去與即將到來的關鍵行程清單 ---")
    for ev in events:
        time_str = ev['dt'].strftime('%Y-%m-%d %H:%M')
        loc = f" (地點: {ev['location']})" if 'location' in ev and ev['location'] else ""
        print(f"• [{time_str}] {ev['summary']}{loc}")
