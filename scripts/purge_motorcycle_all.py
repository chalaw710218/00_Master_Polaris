import os

base_dir = r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-08_Productized_Services\02_外圈代倒垃圾包月_999與1999'

# 1. Update 02_產品規格與定價手冊.md
spec_path = os.path.join(base_dir, '02_產品規格與定價手冊.md')
with open(spec_path, 'r', encoding='utf-8') as f:
    spec_text = f.read()

# Replace motorcycle carriage references in 02
spec_text = spec_text.replace('機車載重平衡與人身安全', '專員步行平衡與人體工學安全')
spec_text = spec_text.replace('機車騎乘平衡與道路安全', '專員提攜平衡與人身安全')
spec_text = spec_text.replace('機車踏板', '手推車/提攜')

# Check other terms in 02
with open(spec_path, 'w', encoding='utf-8') as f:
    f.write(spec_text)

# 2. Update 06_生活管家專屬客服大腦與全場景回應話術手冊.md
chat_path = os.path.join(base_dir, '06_生活管家專屬客服大腦與全場景回應話術手冊.md')
with open(chat_path, 'r', encoding='utf-8') as f:
    chat_text = f.read()

chat_text = chat_text.replace('保護外勤載重平衡與人身安全', '保護外勤步行提攜與人身安全')
chat_text = chat_text.replace('為保護外勤夥伴機車騎乘平衡', '為保護外勤夥伴步行提攜負重安全')
chat_text = chat_text.replace('機車踏板空間', '步行提攜與手推車空間')
chat_text = chat_text.replace('機車後座大置物箱', '人力步行提攜')
chat_text = chat_text.replace('機車置物箱平整放得下', '雙手提攜便利且無滲漏')

# Clarify the no-motorcycle policy in chat manual
no_moto_rule = """
> [!CAUTION]
> **【客服大腦最高法定邊界・嚴禁機車載運垃圾】**：
> 凡客戶詢問「專員是騎機車載垃圾嗎？」「可以幫我載很大包嗎？」，客服一律明確告知：
> 「我們的專員騎機車僅作為抵達您家門前的代步工具！**現場一律以人力雙手步行代提至巷口定點等待垃圾車投入**，全程不使用機車載運垃圾，以符合環境部非廢棄物清除業之法規規範，並確保乾淨衛生！」
"""

if '【客服大腦最高法定邊界・嚴禁機車載運垃圾】' not in chat_text:
    chat_text = chat_text.replace('## 🧠 一、 生活管家客服核心價值與人設定位', '## 🧠 一、 生活管家客服核心價值與人設定位\n' + no_moto_rule)

with open(chat_path, 'w', encoding='utf-8') as f:
    f.write(chat_text)

print('02 and 06 successfully updated and aligned with NO MOTORCYCLE rule!')
