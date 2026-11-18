# -*- coding: utf-8 -*-
"""
test_founder_cases_round4.py
驗證品碩親傳兩大實戰規則：
1. 最快卡片：先抓離客人定位最近的實際 GPS 車輛，再判定其前方未過站點
2. 絕對不提供已過站（已清運/已駛離）的站點給客人
"""

import json
import re

print("Starting verification of Founder's Round 4 rules...")
