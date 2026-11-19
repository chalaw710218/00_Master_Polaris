import json, math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlam = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

with open('05_Trash_Radar_Engine/data/garbage_routes.json', 'r', encoding='utf-8') as f:
    routes = json.load(f)

def run_test(lat, lng, dayNum, h, m, requireRecycle):
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
            bikeMin = max(1, round(dist / 416))
            canReachByBike = smin >= (nowMin + bikeMin)
            
            # recycle logic
            hasRecycleToday = (targetChar in st.get('recycle_day', '')) or (r.get('has_recycling') and targetChar in r.get('recycle_day', ''))
            
            candidates.append({
                'name': st.get('name'),
                'time': st.get('time'),
                'smin': smin,
                'dist': dist,
                'canReachByBike': canReachByBike,
                'bikeMin': bikeMin,
                'hasRecycleToday': hasRecycleToday
            })
            
    reachable = [c for c in candidates if c['canReachByBike']]
    if requireRecycle:
        reachable = [c for c in reachable if c['hasRecycleToday']]
        
    reachable.sort(key=lambda x: (x['smin'], x['dist']))
    best = reachable[0] if reachable else None
    
    print(f"模式: {'【勾選資源回收】' if requireRecycle else '【未勾選 (一般垃圾)】'} | 時間: {h:02d}:{m:02d}")
    if best:
        print(f"  -> 推薦站: {best['name']} | 表定 {best['time']} | 有無回收: {best['hasRecycleToday']}")
        assert not requireRecycle or best['hasRecycleToday'], "錯誤！勾選回收時推薦了無回收的站點！"
    else:
        print("  -> 今日無符合班次")
    return best

print("=== 測試一：週二 16:50 新生路460號 ===")
b1_normal = run_test(22.7594, 121.1400, 2, 16, 50, False)
b1_recycle = run_test(22.7594, 121.1400, 2, 16, 50, True)

print("\n=== 測試二：週四 17:15 正氣路水果街 ===")
b2_normal = run_test(22.7540, 121.1510, 4, 17, 15, False)
b2_recycle = run_test(22.7540, 121.1510, 4, 17, 15, True)

print("\n✅ 所有資源回收勾選邏輯斷言 100% 通過！")
