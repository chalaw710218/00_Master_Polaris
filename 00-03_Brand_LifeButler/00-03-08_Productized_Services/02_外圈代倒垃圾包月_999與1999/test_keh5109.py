# -*- coding: utf-8 -*-
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c * 1.25)

user_lat, user_lon = 22.7932, 121.1218 # 興航街80號
target_min = 16 * 60 + 10 # 16:10 出發

# KEH-5109 站點
stop_lat, stop_lon = 22.7718, 121.1215
stop_min = 16 * 60 + 20 # 16:20 車到

dist = haversine(user_lat, user_lon, stop_lat, stop_lon)
print(f"Distance: {dist} meters")

# 機車 (500m/min)
travel_min_scooter = max(1, round(dist / 500))
user_arrival_min = target_min + travel_min_scooter
can_catch = (user_arrival_min <= stop_min + 1)
total_task = max(travel_min_scooter, stop_min - target_min)
wait_min = max(0, stop_min - user_arrival_min)

print(f"機車行車時間: {travel_min_scooter} 分鐘")
print(f"抵達時刻: 16:{user_arrival_min - 16*60}")
print(f"現場等待: {wait_min} 分鐘")
print(f"垃圾車到場: 16:20")
print(f"任務總耗時: {total_task} 分鐘")
print(f"是否趕得上: {can_catch}")
