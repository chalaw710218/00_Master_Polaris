#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-linus-compute-architecture: ACI 命令行契約與 Tarjan 避鎖排程原子腳本
專職負責工程長林納斯 (Linus) 算力與架構極限防線（Tarjan算法死鎖檢測、ACI契約）。
"""

import sys
import os
import argparse
import json
from datetime import datetime

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def find_scc_tarjan(graph: dict) -> list:
    """使用 Tarjan 演算法檢測有向圖的強連通分量 (SCC)"""
    index = 0
    indices = {}
    lowlink = {}
    on_stack = set()
    stack = []
    sccs = []

    def strongconnect(node):
        nonlocal index
        indices[node] = index
        lowlink[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in indices:
                strongconnect(neighbor)
                lowlink[node] = min(lowlink[node], lowlink[neighbor])
            elif neighbor in on_stack:
                lowlink[node] = min(lowlink[node], indices[neighbor])

        if lowlink[node] == indices[node]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == node:
                    break
            sccs.append(scc)

    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)

    for node in all_nodes:
        if node not in indices:
            strongconnect(node)

    return sccs

def audit_dag_deadlock(graph: dict) -> dict:
    """Tarjan DAG 避鎖律 (Law 20)：排查多 Agent 依賴圖是否存在死鎖環路"""
    sccs = find_scc_tarjan(graph)
    
    # 環路死鎖定義：SCC 大小 > 1，或自環節點
    cycles = []
    for scc in sccs:
        if len(scc) > 1:
            cycles.append(scc)
        elif len(scc) == 1:
            node = scc[0]
            if node in graph.get(node, []):
                cycles.append([node, node])

    is_deadlock_free = (len(cycles) == 0)

    return {
        "is_deadlock_free": is_deadlock_free,
        "total_nodes": len(graph),
        "detected_cycles_count": len(cycles),
        "cycles": cycles,
        "verdict": "✅ Tarjan 演算法證實：任務有向圖無任何循環死鎖環路！" if is_deadlock_free else "❌ 警告：檢測到循環死鎖環路，任務依賴死鎖！"
    }

def main():
    parser = argparse.ArgumentParser(description="ACI 命令行契約與 Tarjan 避鎖排程原子")
    parser.add_argument("--check-dag", type=str, help="任務依賴圖 JSON 字串 (如 '{\"A\":[\"B\"], \"B\":[\"C\"]}')")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")

    args = parser.parse_args()

    # 1. 解析依賴圖
    if args.check_dag:
        try:
            graph = json.loads(args.check_dag)
        except Exception as e:
            print(f"[-] JSON 解析失敗：{e}", file=sys.stderr)
            sys.exit(1)
    else:
        # 內建模擬合規無死鎖多天王 DAG 樣品
        graph = {
            "Task_Linus_Code": ["Task_Deming_Audit"],
            "Task_Abacus_Price": ["Task_Deming_Audit"],
            "Task_Deming_Audit": ["Task_Yuki_Approve"],
            "Task_Yuki_Approve": []
        }

    res = audit_dag_deadlock(graph)

    # 2. 嚴格遵守 ACI 命令行契約 (Law 16)：STDOUT 輸出純淨結構化 JSON
    output_payload = {
        "status": "SUCCESS" if res["is_deadlock_free"] else "DEADLOCK_DETECTED",
        "exit_code_semantic": 0 if res["is_deadlock_free"] else 1,
        "tarjan_audit": res,
        "timestamp": datetime.now().isoformat()
    }

    print(json.dumps(output_payload, ensure_ascii=False, indent=2))

    if res["is_deadlock_free"]:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
