# -*- coding: utf-8 -*-
# 驗證常民生活學排序規則
def sort_candidates(candidates):
    def cmp_func(a, b):
        time_diff = a['total_task'] - b['total_task']
        if abs(time_diff) <= 2:
            return a['dist'] - b['dist']
        return time_diff
    
    import functools
    return sorted(candidates, key=functools.cmp_to_key(cmp_func))

# 測試
cands = [
    {'plate': 'KEM-8815', 'stop': '大道路(豐樂工業區)', 'total_task': 10, 'dist': 4100},
    {'plate': 'KEH-5109', 'stop': '中興路3段20號', 'total_task': 11, 'dist': 2600}
]

sorted_cands = sort_candidates(cands)
print("Top 1:", sorted_cands[0]['plate'], sorted_cands[0]['stop'])
assert sorted_cands[0]['plate'] == 'KEH-5109'
print("Assertion Passed!")
