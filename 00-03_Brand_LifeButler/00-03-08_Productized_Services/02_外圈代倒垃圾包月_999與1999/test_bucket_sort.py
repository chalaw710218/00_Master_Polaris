# -*- coding: utf-8 -*-
cands = [
    {'plate': 'KEM-8815', 'stop': '大道路(豐樂工業區)', 'total_task': 10, 'dist': 5105},
    {'plate': 'KEH-5109', 'stop': '中興路3段20號', 'total_task': 11, 'dist': 3315},
    {'plate': 'KEF-5181', 'stop': '新站路98巷', 'total_task': 40, 'dist': 200}
]

cands.sort(key=lambda x: (x['total_task'] // 3, x['dist']))
for c in cands:
    print(c['plate'], c['stop'], f"Bucket: {c['total_task']//3}", f"Dist: {c['dist']}")

assert cands[0]['plate'] == 'KEH-5109'
print("Math Logic Verified: KEH-5109 is #1!")
