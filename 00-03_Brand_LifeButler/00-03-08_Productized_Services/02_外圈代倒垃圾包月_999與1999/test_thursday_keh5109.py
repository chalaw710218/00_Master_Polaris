# -*- coding: utf-8 -*-
import json
import math
import sys
import io

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c * 1.25)

with open('05_Trash_Radar_Engine/taitung_trash_routes_seed.json', 'r', encoding='utf-8') as f:
    routes = json.load(f)['routes']

# 創辦人題目：
# 地點：台東市興航街80號 (lat: 22.7932, lon: 121.1218)
# 時間：星期四下午 16:10
# 預設生活首選：騎機車 (500m/min)
user_lat, user_lon = 22.7932, 121.1218
t_str = "16:10"
th, tm = map(int, t_str.split(':'))
target_min = th * 60 + tm
speed_mpm = 500 # 騎機車

all_stops = []
for r in routes:
    for s in r['stops']:
        dist = haversine(user_lat, user_lon, s['lat'], s['lon'])
        time_str = s.get('scheduled_time') or s.get('time')
        sh, sm = map(int, time_str.split(':'))
        stop_min = sh * 60 + sm
        travel_min = max(1, round(dist / speed_mpm))
        arrival_min = target_min + travel_min
        can_catch = (arrival_min <= stop_min + 1)
        total_task = max(travel_min, stop_min - target_min)
        all_stops.append({
            'route': r['route_name'],
            'plate': r['truck_plate'],
            'stop': s['name'],
            'dist': dist,
            'time': time_str,
            'stop_min': stop_min,
            'travel_min': travel_min,
            'can_catch': can_catch,
            'total_task': total_task
        })

# 1. 最快完成
catchable = [s for s in all_stops if s['can_catch'] and s['total_task'] <= 60]
catchable_sorted = sorted(catchable, key=lambda x: (x['total_task'], x['dist']))
top_fastest = catchable_sorted[0]

print("==================================================")
print("【創辦人實戰情境驗證】星期四 16:10 興航街80號 ✕ 騎機車出發")
print("==================================================")
print(f"🥇 首選最快攔截站點: {top_fastest['stop']}")
print(f"車次表定時間: {top_fastest['time']}")
print(f"出勤車號: {top_fastest['plate']}")
print(f"作戰距離: {top_fastest['dist']} 公尺 (機車約 {top_fastest['travel_min']} 分鐘)")
print(f"出門到倒完總耗時: {top_fastest['total_task']} 分鐘")
print("==================================================")

assert top_fastest['plate'] == "KEH-5109", f"Expected KEH-5109, got {top_fastest['plate']}"
assert "中興路三段20號" in top_fastest['stop'], f"Expected 中興路三段20號, got {top_fastest['stop']}"
assert top_fastest['time'] == "16:20", f"Expected 16:20, got {top_fastest['time']}"
assert top_fastest['total_task'] <= 15, f"Expected <= 15 mins, got {top_fastest['total_task']}"

print("🎉 驗證完全命中！KEH-5109 (16:20 中興路三段20號) 100% 成為最快首選！")
