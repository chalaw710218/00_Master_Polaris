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

SPEED_WALK_MPM = 67   # 4 km/h
SPEED_BIKE_MPM = 416  # 25 km/h

userLat = 22.7594
userLng = 121.1400
currentDay = 2 # 週二
currentDayName = "星期二"
nowMin = 16 * 60 + 50 # 16:50 -> 1010

with open('05_Trash_Radar_Engine/data/garbage_routes.json', 'r', encoding='utf-8') as f:
    routes = json.load(f)

# 正確的星期比對函數
def match_day(trash_day_str, day_num):
    # day_num: 0(日), 1(一), 2(二), 3(三), 4(四), 5(五), 6(六)
    if not trash_day_str:
        return False
    if "每天" in trash_day_str or "每日" in trash_day_str:
        return True
    day_map = {
        0: ["日", "天", "星期日", "週日", "禮拜天"],
        1: ["一", "星期一", "週一"],
        2: ["二", "星期二", "週二"],
        3: ["三", "星期三", "週三"],
        4: ["四", "星期四", "週四"],
        5: ["五", "星期五", "週五"],
        6: ["六", "星期六", "週六"],
    }
    targets = day_map.get(day_num, [])
    for t in targets:
        if t in trash_day_str:
            return True
    return False

candidateStops = []

for route in routes:
    trashDay = route.get("trash_day", "")
    if not match_day(trashDay, currentDay):
        continue
    
    for st in route.get("stops", []):
        t = st.get("time")
        lat = st.get("lat")
        lon = st.get("lon")
        if not t or not lat or not lon:
            continue
        h, m = map(int, t.split(':'))
        stopMin = h * 60 + m
        dist = haversine(userLat, userLng, lat, lon)

        walkMin = max(1, round(dist / SPEED_WALK_MPM))
        bikeMin = max(1, round(dist / SPEED_BIKE_MPM))

        arrivalMin = stopMin
        hasLiveGps = False

        # 只要車抵達時間 >= 現在時間 + 騎車時間，就代表趕得上 (騎車趕得上即視為可達)
        # 若走路也趕得上 (arrivalMin >= nowMin + walkMin)，亦記錄
        canReachByBike = arrivalMin >= (nowMin + bikeMin)
        canReachByWalk = arrivalMin >= (nowMin + walkMin)

        # 決定此站的最佳交通工具 (若走路趕得上且 <= 600m，用 walk；否則用 bike)
        bestMode = "walk" if (canReachByWalk and dist <= 600) else "bike"
        travelMin = walkMin if bestMode == "walk" else bikeMin
        margin = arrivalMin - (nowMin + travelMin)

        item = {
            "name": st.get("name"),
            "dist": dist,
            "time": t,
            "stopMin": stopMin,
            "arrivalMin": arrivalMin,
            "walkMin": walkMin,
            "bikeMin": bikeMin,
            "canReachByBike": canReachByBike,
            "canReachByWalk": canReachByWalk,
            "canReach": canReachByBike,
            "bestMode": bestMode,
            "travelMin": travelMin,
            "margin": margin,
            "plate": route.get("truck_plate")
        }
        candidateStops.append(item)

# 篩選趕得上的站點
reachableStops = [s for s in candidateStops if s["canReach"]]

# 依品碩親定鐵律排序：
# 主答案 = 使用者趕得上的班次中，最早能倒完垃圾的那一站 (arrivalMin 最小)
# 若抵達時間相同，以距離近者優先 (dist 最小)
reachableStops.sort(key=lambda x: (x["arrivalMin"], x["dist"]))

print(f"Total candidates: {len(candidateStops)}, reachable: {len(reachableStops)}")
print("\n--- TOP 10 EARLIEST REACHABLE STOPS ---")
for i, s in enumerate(reachableStops[:10]):
    print(f"{i+1}. {s['name']} | plate={s['plate']} | time={s['time']} | dist={s['dist']}m | mode={s['bestMode']}({s['travelMin']}m) | margin={s['margin']}m")
