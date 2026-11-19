import json, math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlam = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

with open('05_Trash_Radar_Engine/data/garbage_routes.json', 'r', encoding='utf-8') as f:
    routes = json.load(f)

def test_user(lat, lng, dayNum, h, m):
    nowMin = h * 60 + m
    dayChars = ['日', '一', '二', '三', '四', '五', '六']
    targetChar = dayChars[dayNum]
    
    candidates = []
    for r in routes:
        tday = r.get('trash_day', '')
        if targetChar not in tday and '每天' not in tday and '每日' not in tday: continue
        for st in r.get('stops', []):
            if not st.get('time') or not st.get('lat') or not st.get('lon'): continue
            sh, sm = map(int, st.get('time').split(':'))
            smin = sh * 60 + sm
            dist = haversine(lat, lng, st.get('lat'), st.get('lon'))
            walkMin = max(1, round(dist / 67))
            bikeMin = max(1, round(dist / 416))
            canReachByBike = smin >= (nowMin + bikeMin)
            candidates.append({
                'name': st.get('name'),
                'time': st.get('time'),
                'smin': smin,
                'dist': dist,
                'canReachByBike': canReachByBike,
                'bikeMin': bikeMin
            })
    
    # 物理最近日常站
    nearest = min(candidates, key=lambda x: x['dist'])
    
    # 可達站中最快能倒完
    reachable = [c for c in candidates if c['canReachByBike']]
    reachable.sort(key=lambda x: (x['smin'], x['dist']))
    best = reachable[0] if reachable else None
    
    print(f"\n=== 時間 {h:02d}:{m:02d} ===")
    print(f"原本離您最近的站: {nearest['name']} (距 {nearest['dist']}m, 表定 {nearest['time']})")
    if nearest['smin'] < nowMin:
        print("  -> 狀態: 車已開走 (已錯過)")
    elif best and nearest['name'] == best['name']:
        print("  -> 狀態: 即為本站主答案")
    else:
        print(f"  -> 狀態: 車將於 {nearest['time']} 抵達 (還有 {nearest['smin'] - nowMin} 分鐘)")
    
    if best:
        print(f"主答案 (立即行動): 去 {best['name']} (表定 {best['time']}, 倒數 {best['smin']-nowMin} 分, 騎車 {best['bikeMin']} 分)")
    else:
        print("主答案: 今日已無可趕上班次")

test_user(22.7594, 121.1400, 2, 16, 50)
test_user(22.7594, 121.1400, 2, 16, 58)
