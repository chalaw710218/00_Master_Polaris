# -*- coding: utf-8 -*-
"""
極星生活管家 · 台東市公所官方全量清運路線與停靠站自動編譯器
由 CTO 林納斯 (Linus) 監製，依據 00-11-11 中華電信官方資料庫編譯
"""
import urllib.request
import ssl
import xml.etree.ElementTree as ET
import json
import os
import sys
import io
import time

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SCRIPT_DIR, "00-11_stops_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

ROUTES_XML = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-11_Reverse_Engineering_Lab\00-11-11_Qingyun_ePoint_GarbageTruck_APK_Reverse\analysis_notes\taitung_routes.xml"
OUTPUT_SEED_JSON = os.path.join(SCRIPT_DIR, "05_Trash_Radar_Engine", "taitung_trash_routes_seed.json")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {"User-Agent": "Mozilla/5.0 (Android)"}

# 讀取 38 條官方路線清單
root = ET.parse(ROUTES_XML).getroot()
print(f"Total official routes in XML: {len(root)}")

# 挑選出主力清運車輛 (過濾純'回'字頭重複支援車，主力車已自帶 recycle_day)
main_routes = []
for r in root:
    name = r.attrib.get('name', '').strip()
    run_id = r.attrib.get('run_id', '').strip()
    if name.startswith('回'):
        continue # 略過純獨立回收車，主車已有回收日屬性
    main_routes.append(r.attrib)

print(f"Selected {len(main_routes)} main truck routes for compilation.")

compiled_routes = []
total_stops_count = 0

for idx, r in enumerate(main_routes):
    run_id = r['run_id']
    plate = r['group_id'] if r.get('group_id') else r['name'].split('(')[0]
    name = r['name']
    trash_day = r.get('trash_day', '')
    recycle_day = r.get('recycle_day', '')
    has_recycling = (recycle_day != '無' and recycle_day != '')

    cache_file = os.path.join(CACHE_DIR, f"route_{run_id}.xml")
    raw_xml = None

    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            raw_xml = f.read()
    else:
        url = f"https://www.bstruck.hinet.net/MIS/subsystem/xml/scheduletime.ashx?key=1&status_id=0&run_id={run_id}"
        print(f"[{idx+1}/{len(main_routes)}] Fetching {name} (run_id: {run_id})...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                raw_xml = resp.read()
            with open(cache_file, "wb") as f:
                f.write(raw_xml)
            time.sleep(0.3)
        except Exception as e:
            print(f"  ❌ Error fetching {run_id}: {e}")
            continue

    if not raw_xml:
        continue

    try:
        s_root = ET.fromstring(raw_xml.decode('utf-8'))
    except Exception as e:
        print(f"  ❌ XML parse error for {run_id}: {e}")
        continue

    stops = []
    for item in list(s_root):
        s_name = item.attrib.get('name', '').strip()
        stime_raw = item.attrib.get('stime', '').strip() # e.g. "16:20~16:20"
        s_time = stime_raw.split('~')[0].strip() if '~' in stime_raw else stime_raw
        if not s_time or ':' not in s_time:
            continue
        try:
            lat = round(float(item.attrib.get('lat', 0)), 5)
            lon = round(float(item.attrib.get('lon', 0)), 5)
        except ValueError:
            continue
        
        if lat == 0 or lon == 0:
            continue

        stops.append({
            "stop_id": item.attrib.get('stop_id', ''),
            "name": s_name,
            "lat": lat,
            "lon": lon,
            "scheduled_time": s_time,
            "stay_range": item.attrib.get('stay_range', '沿途清運')
        })

    if not stops:
        continue

    total_stops_count += len(stops)
    print(f"  ✔ {plate} ({name}) -> {len(stops)} stops (首站: {stops[0]['name']} {stops[0]['scheduled_time']}, 末站: {stops[-1]['name']} {stops[-1]['scheduled_time']})")

    compiled_routes.append({
        "route_id": f"TT_OFFICIAL_{run_id}",
        "route_name": name,
        "truck_plate": plate,
        "run_id": run_id,
        "trash_day": trash_day,
        "recycle_day": recycle_day,
        "has_recycling": has_recycling,
        "stops": stops
    })

master_dataset = {
    "city": "台東縣",
    "township": "台東市",
    "meta": {
        "version": "2.0_OFFICIAL",
        "compiled_at": "2026-11-12",
        "provider": "生活管家工程部 ✕ CTO 林納斯 (00-11-11 逆向工程官方資料庫)",
        "source": "中華電信智慧車機清運系統 (www.bstruck.hinet.net) · 臺東縣臺東市公所 (ID: 22)",
        "total_routes": len(compiled_routes),
        "total_stops": total_stops_count
    },
    "routes": compiled_routes
}

with open(OUTPUT_SEED_JSON, "w", encoding="utf-8") as f:
    json.dump(master_dataset, f, ensure_ascii=False, indent=2)

print("==================================================")
print(f"🎉 官方全量數據編譯竣工！共收錄 {len(compiled_routes)} 條主力路線、{total_stops_count} 個正式停靠站點！")
print(f"📁 儲存路徑: {OUTPUT_SEED_JSON}")
print("==================================================")
