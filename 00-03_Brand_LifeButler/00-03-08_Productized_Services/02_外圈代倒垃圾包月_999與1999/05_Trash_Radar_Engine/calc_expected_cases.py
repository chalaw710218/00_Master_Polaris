import json
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c)

SPEED_WALK_MPM = 67
SPEED_BIKE_MPM = 416

with open('05_Trash_Radar_Engine/data/garbage_routes.json', 'r', encoding='utf-8') as f:
    routes = json.load(f)

def match_day(trash_day_str, day_num):
    if not trash_day_str: return False
    if "每天" in trash_day_str or "每日" in trash_day_str: return True
    day_chars = {0: ["日", "天"], 1: ["一"], 2: ["二"], 3: ["三"], 4: ["四"], 5: ["五"], 6: ["六"]}
    for c in day_chars.get(day_num, []):
        if c in trash_day_str: return True
    return False

def find_best_stop(userLat, userLng, dayNum, nowHour, nowMinute):
    nowMin = nowHour * 60 + nowMinute
    candidateStops = []
    for route in routes:
        if not match_day(route.get("trash_day", ""), dayNum):
            continue
        for st in route.get("stops", []):
            t = st.get("time")
            lat = st.get("lat")
            lon = st.get("lon")
            if not t or not lat or not lon: continue
            h, m = map(int, t.split(':'))
            stopMin = h * 60 + m
            dist = haversine(userLat, userLng, lat, lon)
            walkMin = max(1, round(dist / SPEED_WALK_MPM))
            bikeMin = max(1, round(dist / SPEED_BIKE_MPM))
            arrivalMin = stopMin
            canReachByBike = arrivalMin >= (nowMin + bikeMin)
            canReachByWalk = arrivalMin >= (nowMin + walkMin)
            bestMode = "walk" if (canReachByWalk and dist <= 600) else "bike"
            travelMin = walkMin if bestMode == "walk" else bikeMin
            margin = arrivalMin - (nowMin + travelMin)

            if canReachByBike:
                candidateStops.append({
                    "name": st.get("name"),
                    "dist": dist,
                    "time": t,
                    "arrivalMin": arrivalMin,
                    "bestMode": bestMode,
                    "travelMin": travelMin,
                    "margin": margin,
                    "plate": route.get("truck_plate")
                })
    # 排序：最早能倒完垃圾 (arrivalMin 最小)，若相同則 dist 最小
    candidateStops.sort(key=lambda x: (x["arrivalMin"], x["dist"]))
    return candidateStops

print("=== 情境一：新生路460號 (22.7594, 121.1400)，週二 16:50 ===")
res1 = find_best_stop(22.7594, 121.1400, 2, 16, 50)
for i, s in enumerate(res1[:3]):
    print(f"Top {i+1}: {s['name']} | plate={s['plate']} | time={s['time']} | dist={s['dist']}m | margin={s['margin']}m")

print("\n=== 情境二：正氣路水果街 (22.7540, 121.1510)，週四 17:15 ===")
res2 = find_best_stop(22.7540, 121.1510, 4, 17, 15)
for i, s in enumerate(res2[:3]):
    print(f"Top {i+1}: {s['name']} | plate={s['plate']} | time={s['time']} | dist={s['dist']}m | margin={s['margin']}m")

print("\n=== 情境三：體育場 (22.7523, 121.1465)，週一 18:00 ===")
res3 = find_best_stop(22.7523, 121.1465, 1, 18, 0)
for i, s in enumerate(res3[:3]):
    print(f"Top {i+1}: {s['name']} | plate={s['plate']} | time={s['time']} | dist={s['dist']}m | margin={s['margin']}m")
