import json
import os
import requests
from google.oauth2.credentials import Credentials

mgr_dir = r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager"
token_path = os.path.join(mgr_dir, "token.json")

with open(token_path, "r", encoding="utf-8") as f:
    token_data = json.load(f)

creds = Credentials.from_authorized_user_info(token_data)
headers = {
    "Authorization": f"Bearer {creds.token}",
    "Content-Type": "application/json"
}

account_id = "112884798662846885062"
location_id = "1774177451467087781"
menu_url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/foodMenus"

# 構建全新真實結構化菜單
new_food_menus = {
    "menus": [
        {
            "labels": [
                {
                    "displayName": "職人食堂 內用外帶菜單",
                    "description": "每日新鮮手工備料，現蒸現煮職人料理",
                    "languageCode": "zh-TW"
                }
            ],
            "sections": [
                {
                    "labels": [
                        {
                            "displayName": "招牌現蒸點心・湯包系列",
                            "description": "現點現蒸，堅持手工製作薄皮爆汁",
                            "languageCode": "zh-TW"
                        }
                    ],
                    "items": [
                        {
                            "labels": [
                                {
                                    "displayName": "手工爆汁小籠湯包",
                                    "description": "現點現蒸爆汁薄皮小籠湯包，鮮甜肉汁一咬迸發",
                                    "languageCode": "zh-TW"
                                }
                            ],
                            "attributes": {
                                "price": {
                                    "currencyCode": "TWD",
                                    "units": "80"
                                }
                            }
                        },
                        {
                            "labels": [
                                {
                                    "displayName": "打拋豬小籠湯包",
                                    "description": "泰式香料九層塔風味，微辣濃郁多汁開胃",
                                    "languageCode": "zh-TW"
                                }
                            ],
                            "attributes": {
                                "price": {
                                    "currencyCode": "TWD",
                                    "units": "90"
                                }
                            }
                        },
                        {
                            "labels": [
                                {
                                    "displayName": "鮮蝦河粉",
                                    "description": "晶瑩剔透Q彈河粉，包裹爽脆鮮甜大蝦仁",
                                    "languageCode": "zh-TW"
                                }
                            ],
                            "attributes": {
                                "price": {
                                    "currencyCode": "TWD",
                                    "units": "70"
                                }
                            }
                        },
                        {
                            "labels": [
                                {
                                    "displayName": "手工鮮肉蒸餃",
                                    "description": "外皮Q勁，內餡扎實鮮美飽滿",
                                    "languageCode": "zh-TW"
                                }
                            ],
                            "attributes": {
                                "price": {
                                    "currencyCode": "TWD",
                                    "units": "70"
                                }
                            }
                        },
                        {
                            "labels": [
                                {
                                    "displayName": "招牌酸辣湯",
                                    "description": "木耳豆腐蛋花料多味濃，酸香微辣恰到好處",
                                    "languageCode": "zh-TW"
                                }
                            ],
                            "attributes": {
                                "price": {
                                    "currencyCode": "TWD",
                                    "units": "40"
                                }
                            }
                        },
                        {
                            "labels": [
                                {
                                    "displayName": "海苔蛋花湯",
                                    "description": "清爽高湯搭配細緻蛋花與海苔，暖胃解膩",
                                    "languageCode": "zh-TW"
                                }
                            ],
                            "attributes": {
                                "price": {
                                    "currencyCode": "TWD",
                                    "units": "35"
                                }
                            }
                        }
                    ]
                },
                {
                    "labels": [
                        {
                            "displayName": "招牌丼飯・特色定食",
                            "description": "均附溫泉半熟蛋、特製泡菜、胡麻綠花椰",
                            "languageCode": "zh-TW"
                        }
                    ],
                    "items": [
                        {
                            "labels": [
                                {
                                    "displayName": "炙燒牛五花燒肉丼飯",
                                    "description": "高溫炙燒焦香油花牛五花，鹹甜醬汁拌飯必點",
                                    "languageCode": "zh-TW"
                                }
                            ],
                            "attributes": {
                                "price": {
                                    "currencyCode": "TWD",
                                    "units": "170"
                                }
                            }
                        },
                        {
                            "labels": [
                                {
                                    "displayName": "泰式酸辣雞腿飯",
                                    "description": "外皮金黃酥脆大雞腿，附特製雞汁飯與泰式酸辣醬",
                                    "languageCode": "zh-TW"
                                }
                            ],
                            "attributes": {
                                "price": {
                                    "currencyCode": "TWD",
                                    "units": "160"
                                }
                            }
                        },
                        {
                            "labels": [
                                {
                                    "displayName": "酥脆厚切炸豬排飯",
                                    "description": "嚴選厚切豬排裹上酥脆麵衣，金黃厚實鮮嫩多汁",
                                    "languageCode": "zh-TW"
                                }
                            ],
                            "attributes": {
                                "price": {
                                    "currencyCode": "TWD",
                                    "units": "150"
                                }
                            }
                        },
                        {
                            "labels": [
                                {
                                    "displayName": "經典蒲燒鰻魚飯",
                                    "description": "醇厚蒲燒醬汁細火烘烤，肉質細緻香醇下飯",
                                    "languageCode": "zh-TW"
                                }
                            ],
                            "attributes": {
                                "price": {
                                    "currencyCode": "TWD",
                                    "units": "200"
                                }
                            }
                        }
                    ]
                },
                {
                    "labels": [
                        {
                            "displayName": "手作麵食・讚岐烏龍系列",
                            "description": "每日熬煮清爽高湯，可選讚岐烏龍麵或手工拉麵",
                            "languageCode": "zh-TW"
                        }
                    ],
                    "items": [
                        {
                            "labels": [
                                {
                                    "displayName": "招牌麻辣烏龍麵",
                                    "description": "大紅袍花椒秘製麻辣高湯，辛香濃郁後勁十足",
                                    "languageCode": "zh-TW"
                                }
                            ],
                            "attributes": {
                                "price": {
                                    "currencyCode": "TWD",
                                    "units": "110"
                                }
                            }
                        },
                        {
                            "labels": [
                                {
                                    "displayName": "柴魚昆布烏龍麵",
                                    "description": "北海道昆布佐特級日式柴魚慢熬清冽高湯，甘甜暖心",
                                    "languageCode": "zh-TW"
                                }
                            ],
                            "attributes": {
                                "price": {
                                    "currencyCode": "TWD",
                                    "units": "90"
                                }
                            }
                        }
                    ]
                }
            ]
        }
    ]
}

# 嘗試 PATCH 或 PUT 更新 foodMenus
print("Sending foodMenus update...")
res = requests.patch(menu_url, headers=headers, json=new_food_menus)
print("PATCH status:", res.status_code)
if res.status_code not in [200, 201]:
    print("PATCH error:", res.text[:300])
    # 嘗試 PUT
    res_put = requests.put(menu_url, headers=headers, json=new_food_menus)
    print("PUT status:", res_put.status_code)
    if res_put.status_code in [200, 201]:
        print("PUT succeeded!")
    else:
        print("PUT error:", res_put.text[:300])
else:
    print("PATCH succeeded!")
