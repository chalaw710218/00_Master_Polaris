# -*- coding: utf-8 -*-
"""
生活管家 · 一鍵倒垃圾雷達 v2.0 官方 948 站實戰矩陣驗證
驗收創辦人真實情境：
1. 興航街80號 ✕ 16:10 機車先鋒 -> 命中中興路三段 (BXT-2067 16:18 / KEH-5109 16:21)
2. 興航街80號 ✕ 16:10 機車先鋒 (含資源回收) -> 100% 鎖定 KEH-5109 (16:21 中興路3段20號，雙收)
3. 興航街80號 ✕ 18:40 步行夜間 -> 命中 KEF-5181 (新站路 18:51 / 19:04)
4. 週四資源回收雙收車次過濾
"""
import json
import math
import sys
import io

if sys.platform.startswith("win"):
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
    data = json.load(f)

routes = data['routes']
print(f"Loaded {len(routes)} routes, {sum(len(r['stops']) for r in routes)} stops.")

u_lat, u_lon = 22.7932, 121.1218
t_str = "16:10"
th, tm = map(int, t_str.split(':'))
target_min = th * 60 + tm
day_char = "四" # 星期四

def query_radar(want_recycle=False, mode_speed=500, user_time_min=target_min):
    all_stops = []
    for r in routes:
        if day_char not in r.get('trash_day', ''):
            continue
        if want_recycle:
            if not r.get('has_recycling') or day_char not in r.get('recycle_day', ''):
                continue
        for s in r['stops']:
            dist = haversine(u_lat, u_lon, s['lat'], s['lon'])
            sh, sm = map(int, s['scheduled_time'].split(':'))
            stop_min = sh * 60 + sm
            travel_min = max(1, round(dist / mode_speed))
            arrival_min = user_time_min + travel_min
            can_catch = (arrival_min <= stop_min + 1)
            total_task = max(travel_min, stop_min - user_time_min)
            all_stops.append({
                'route': r['route_name'],
                'plate': r['truck_plate'],
                'stop': s['name'],
                'dist': dist,
                'time': s['scheduled_time'],
                'stop_min': stop_min,
                'travel_min': travel_min,
                'can_catch': can_catch,
                'total_task': total_task
            })
    catchable = [s for s in all_stops if s['can_catch'] and s['total_task'] <= 60]
    catchable.sort(key=lambda x: (x['total_task'] // 3, x['dist']))
    all_stops.sort(key=lambda x: x['dist'])
    return catchable[0] if catchable else None, all_stops[0] if all_stops else None

# 1. 測試情境 1：純一般垃圾 16:10 機車出發
top_fast1, _ = query_radar(want_recycle=False)
print("==================================================")
print("【情境 1】週四 16:10 興航街80號 ✕ 騎機車先鋒搶快 (純垃圾)")
print("==================================================")
print(f"首選攔截站點: {top_fast1['stop']}")
print(f"出勤車號: {top_fast1['plate']}")
print(f"表定時間: {top_fast1['time']}")
print(f"作戰距離: {top_fast1['dist']} 公尺 (機車約 {top_fast1['travel_min']} 分鐘)")
print(f"任務總耗時: {top_fast1['total_task']} 分鐘")
assert "中興路3段" in top_fast1['stop'], f"Expected 中興路3段, got {top_fast1['stop']}"
assert top_fast1['total_task'] <= 12, "Should be finished in 12 mins"
print("✅ 情境 1 命中中興路三段先鋒車次！")

# 2. 測試情境 2：勾選【資源回收雙收】16:10 機車出發
top_fast2, _ = query_radar(want_recycle=True)
print("\n==================================================")
print("【情境 2】週四 16:10 興航街80號 ✕ 騎機車雙收先鋒 (垃圾+回收)")
print("==================================================")
print(f"首選雙收攔截站點: {top_fast2['stop']}")
print(f"出勤車號: {top_fast2['plate']}")
print(f"表定時間: {top_fast2['time']}")
print(f"作戰距離: {top_fast2['dist']} 公尺 (機車約 {top_fast2['travel_min']} 分鐘)")
print(f"任務總耗時: {top_fast2['total_task']} 分鐘")
assert top_fast2['plate'] == "KEH-5109", f"Expected KEH-5109, got {top_fast2['plate']}"
assert "中興路3段20號" in top_fast2['stop'], f"Expected 中興路3段20號, got {top_fast2['stop']}"
assert top_fast2['time'] == "16:21", f"Expected 16:21, got {top_fast2['time']}"
print("✅ 情境 2 資源回收雙收 100% 鎖定創辦人實證車號 KEH-5109 (中興路3段20號 16:21)！")

# 3. 測試情境 3：興航街80號 ✕ 18:40 步行夜間倒垃圾
t_night_min = 18 * 60 + 40
top_fast3, top_near3 = query_radar(want_recycle=False, mode_speed=75, user_time_min=t_night_min)
print("\n==================================================")
print("【情境 3】週四 18:40 興航街80號 ✕ 步行夜間清運")
print("==================================================")
print(f"離家最近站點: {top_near3['stop']}")
print(f"出勤車號: {top_near3['plate']}")
print(f"表定時間: {top_near3['time']}")
print(f"離家距離: {top_near3['dist']} 公尺 (步行約 {top_near3['travel_min']} 分鐘)")
assert top_near3['plate'] == "KEF-5181", f"Expected KEF-5181, got {top_near3['plate']}"
assert "新站" in top_near3['stop'] or "興安" in top_near3['stop'], f"Expected 新站/興安, got {top_near3['stop']}"
assert top_near3['dist'] <= 400, f"Distance too far: {top_near3['dist']}m"
print(f"最快完成站點: {top_fast3['stop']} (車次 {top_fast3['time']} {top_fast3['plate']}，出門 {top_fast3['total_task']} 分鐘搞定)")
print("✅ 情境 3 官方 KEF-5181 新站特區站點 100% 命中！")

print("\n==================================================")
print("🎉 生活管家 v2.0 官方 948 站實戰矩陣 100% 綠燈 PASS (Exit Code: 0)！")
print("==================================================")
