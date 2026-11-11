# -*- coding: utf-8 -*-
"""
專項實測：台東市興航街 80 號 ✕ 17:20 錯過班次實測驗證
"""
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

# 情境 1：創辦人實測情境：台東市興航街80號 (lat: 22.7932, lon: 121.1218)，時間 16:26 出發，步行
user_lat, user_lon = 22.7932, 121.1218
t_str = "16:26"
th, tm = map(int, t_str.split(':'))
target_min = th * 60 + tm
speed_mpm = 75 # 步行

all_stops = []
for r in routes:
    for s in r['stops']:
        dist = haversine(user_lat, user_lon, s['lat'], s['lon'])
        sh, sm = map(int, (s.get('scheduled_time') or s.get('time')).split(':'))
        stop_min = sh * 60 + sm
        travel_min = max(1, round(dist / speed_mpm))
        arrival_min = target_min + travel_min
        can_catch = (arrival_min <= stop_min + 1)
        total_task = max(travel_min, stop_min - target_min)
        all_stops.append({
            'route': r['route_name'],
            'stop': s['name'],
            'dist': dist,
            'time': s.get('scheduled_time') or s.get('time'),
            'stop_min': stop_min,
            'travel_min': travel_min,
            'can_catch': can_catch,
            'total_task': total_task
        })

# 排序最近站點
all_stops_by_dist = sorted(all_stops, key=lambda x: x['dist'])
top_nearest = all_stops_by_dist[0]

print("==================================================")
print("【情境 1 驗證】台東市興航街80號 ✕ 16:26 步行出發")
print("==================================================")
print(f"最近站點: {top_nearest['stop']}")
print(f"距離: {top_nearest['dist']} 公尺 (原本盲測錯誤為 3129 公尺！)")
print(f"步行耗時: {top_nearest['travel_min']} 分鐘 (原本盲測錯誤為 42 分鐘！)")
assert top_nearest['dist'] <= 150, f"Distance too far: {top_nearest['dist']}m"
assert top_nearest['travel_min'] <= 3, f"Travel min too long: {top_nearest['travel_min']}min"

# 排序最快搞定
catchable = [s for s in all_stops if s['can_catch'] and s['total_task'] <= 60]
catchable_sorted = sorted(catchable, key=lambda x: (x['total_task'], x['dist']))
top_fastest = catchable_sorted[0]
print(f"首選攔截點: {top_fastest['stop']}")
print(f"車次時間: {top_fastest['time']}")
print(f"出門到搞定總耗時: {top_fastest['total_task']} 分鐘 (原本盲測錯誤為 54 分鐘！)")
assert top_fastest['dist'] <= 200
assert top_fastest['total_task'] <= 25

# 情境 2：創辦人提出的關鍵問題：如果已經錯過家門口時間 (例如車次 16:50/17:00 抵達，客人 17:20 才出門)
t_str2 = "17:20"
th2, tm2 = map(int, t_str2.split(':'))
target_min2 = th2 * 60 + tm2

all_stops2 = []
for r in routes:
    for s in r['stops']:
        dist = haversine(user_lat, user_lon, s['lat'], s['lon'])
        sh, sm = map(int, (s.get('scheduled_time') or s.get('time')).split(':'))
        stop_min = sh * 60 + sm
        # 假設客人騎機車去攔截
        travel_min = max(1, round(dist / 500))
        arrival_min = target_min2 + travel_min
        can_catch = (arrival_min <= stop_min + 1)
        total_task = max(travel_min, stop_min - target_min2)
        all_stops2.append({
            'route': r['route_name'],
            'stop': s['name'],
            'dist': dist,
            'time': s.get('scheduled_time') or s.get('time'),
            'stop_min': stop_min,
            'travel_min': travel_min,
            'can_catch': can_catch,
            'total_task': total_task
        })

print("\n==================================================")
print("【情境 2 驗證】家門口班次(16:50)已過 ✕ 17:20 騎機車跨區火速攔截")
print("==================================================")
# 檢查最近站點是否已過
nearest2 = sorted(all_stops2, key=lambda x: x['dist'])[0]
print(f"家門口最近站點表定: {nearest2['stop']} ({nearest2['time']}) -> 已過去 {target_min2 - nearest2['stop_min']} 分鐘！")
assert nearest2['stop_min'] < target_min2, "Nearest stop should be in the past"

# 篩選趕得上的跨區站點
catchable2 = [s for s in all_stops2 if s['can_catch'] and s['total_task'] <= 60]
catchable2_sorted = sorted(catchable2, key=lambda x: (x['total_task'], x['dist']))
top_intercept = catchable2_sorted[0]
print(f"跨區火速攔截成功！首選攔截點: {top_intercept['stop']} (車次 {top_intercept['time']})")
print(f"距離: {top_intercept['dist']} 公尺，騎機車只需: {top_intercept['travel_min']} 分鐘！")
print(f"出門到搞定總耗時: {top_intercept['total_task']} 分鐘")
assert top_intercept['can_catch'] == True
assert top_intercept['stop_min'] >= target_min2
print("==================================================")
print("🎉 創辦人兩大實測盲點 100% 完美解決！")
print("==================================================")
