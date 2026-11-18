import urllib.request
import xml.etree.ElementTree as ET
import json

# 抓取台東全部 38 條路線
routes_url = "https://www.bstruck.hinet.net/MIS/subsystem/xml/Approute.ashx?customer_id=22&key=1"
req = urllib.request.Request(routes_url, headers={'User-Agent': 'Mozilla/5.0 (Android)'})
with urllib.request.urlopen(req, timeout=10) as resp:
    root = ET.fromstring(resp.read().decode('utf-8'))

recycling_routes = []
for item in root.findall('Item'):
    name = item.attrib.get('name', '')
    run_id = item.attrib.get('run_id', '')
    route_no = item.attrib.get('route_no', '')
    trash_day = item.attrib.get('trash_day', '')
    recycle_day = item.attrib.get('recycle_day', '')

    # 凡是名稱帶 "回" 或專門回收車
    if name.startswith('回') or '回收' in name or '(資)' in name:
        s_url = f"https://www.bstruck.hinet.net/MIS/subsystem/xml/scheduletime.ashx?key=1&status_id=0&run_id={run_id}"
        try:
            s_req = urllib.request.Request(s_url, headers={'User-Agent': 'Mozilla/5.0 (Android)'})
            with urllib.request.urlopen(s_req, timeout=5) as s_resp:
                s_root = ET.fromstring(s_resp.read().decode('utf-8'))
                stops = []
                for st in s_root.findall('ScheduleTime'):
                    s_name = st.attrib.get('name', '').strip()
                    s_lat = float(st.attrib.get('lat', '0'))
                    s_lon = float(st.attrib.get('lon', '0'))
                    s_stime = st.attrib.get('stime', '').split('~')[0].strip()
                    stops.append({
                        "name": s_name,
                        "lat": s_lat,
                        "lon": s_lon,
                        "time": s_stime,
                        "recycle_day": trash_day
                    })
                
                clean_plate = name.replace('回', '').split('(')[0].strip()
                recycling_routes.append({
                    "route_id": f"TT_RECYCLE_{run_id}",
                    "run_id": run_id,
                    "route_name": name,
                    "truck_plate": clean_plate,
                    "trash_day": trash_day,
                    "recycle_day": trash_day,
                    "has_recycling": True,
                    "is_recycling_truck": True,
                    "stops": stops
                })
                print(f"Loaded recycle route {name} (run_id={run_id}, stops={len(stops)})")
        except Exception as e:
            print(f"Error loading {name}: {e}")

with open("05_Trash_Radar_Engine/evidence/recycling_routes.json", "w", encoding="utf-8") as f:
    json.dump(recycling_routes, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(recycling_routes)} recycling routes!")
