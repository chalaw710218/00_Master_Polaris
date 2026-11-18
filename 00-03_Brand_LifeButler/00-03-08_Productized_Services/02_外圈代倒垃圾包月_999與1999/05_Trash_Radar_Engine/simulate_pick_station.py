import json
import math

# haversine
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

userLat = 22.7594
userLng = 121.1400
currentDayName = "星期二"
nowMin = 16 * 60 + 50 # 16:50 -> 1010

with open('05_Trash_Radar_Engine/data/garbage_routes.json', 'r', encoding='utf-8') as f:
    routes = json.load(f)

candidateStops = []

for route in routes:
    trashDay = route.get("trash_day", "")
    if currentDayName not in trashDay and "每天" not in trashDay and "每日" not in trashDay:
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

        canReachByBike = arrivalMin >= (nowMin + bikeMin)
        canReachByWalk = arrivalMin >= (nowMin + walkMin)

        bikeMargin = arrivalMin - (nowMin + bikeMin)
        walkMargin = arrivalMin - (nowMin + walkMin)

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
            "bikeMargin": bikeMargin,
            "walkMargin": walkMargin
        }
        candidateStops.append(item)
        if "460號" in st.get("name", ""):
            print(">>> 460號 candidate info:", item)

reachableStops = [s for s in candidateStops if s["canReachByBike"]]
print(f"Total candidate stops: {len(candidateStops)}, reachable: {len(reachableStops)}")

# 查看 460 號是否在 reachableStops
st_460 = [s for s in reachableStops if "460號" in s["name"]]
print("460 in reachable?:", len(st_460))

# 執行 index.html 現有的排序
def sort_key_cmp(a, b):
    # 優先度 1: 走路近站
    aWalkable = a["canReachByWalk"] and a["dist"] <= 600
    bWalkable = b["canReachByWalk"] and b["dist"] <= 600
    if aWalkable and not bWalkable:
        return -1
    if not aWalkable and bWalkable:
        return 1

    # 優先度 2: 車即將抵達且不勉強 (bikeMargin > 3) 優先
    aTight = a["bikeMargin"] <= 3
    bTight = b["bikeMargin"] <= 3
    if not aTight and bTight:
        return -1
    if aTight and not bTight:
        return 1

    # 優先度 3: 總等候時間由近到遠
    if a["arrivalMin"] != b["arrivalMin"]:
        return a["arrivalMin"] - b["arrivalMin"]
    return a["dist"] - b["dist"]

import functools
sorted_stops = sorted(reachableStops, key=functools.cmp_to_key(sort_key_cmp))

print("\n--- TOP 10 STOPS IN CURRENT LOGIC ---")
for i, s in enumerate(sorted_stops[:10]):
    print(f"{i+1}. {s['name']} | dist={s['dist']}m | time={s['time']} | bikeMargin={s['bikeMargin']} | walkMargin={s['walkMargin']} | canWalk={s['canReachByWalk']}")
