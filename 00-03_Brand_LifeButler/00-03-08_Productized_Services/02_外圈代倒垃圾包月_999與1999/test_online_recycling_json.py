import urllib.request
import json

url = 'https://chalaw710218.github.io/taitung-trash-radar/data/recycling_routes.json?v=20261117_v2'
req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print(f'Total routes online: {len(data)}')
    verified = [r for r in data if r.get('is_plate_verified')]
    unverified = [r for r in data if not r.get('is_plate_verified')]
    print(f'Verified: {len(verified)} ({verified[0].get("run_id")} -> {verified[0].get("truck_plate")})')
    print(f'Unverified: {len(unverified)}')
