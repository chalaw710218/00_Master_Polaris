# 門禁修正（Claude 11/25 盲測後）：只改 6 處，每處都必須剛好找到一次，否則什麼都不寫
import os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bionic_knowledge_gate.py")
s = open(P, encoding="utf-8").read()
E = [
("def get_vault_urls(", '''def nums_missing(fact: str, quote: str) -> list:
    """核心事實裡的數字，必須以完整數字出現在摘句裡（1 不能靠 11B 蒙混）"""
    q = quote.replace(',', '')
    return [x for x in re.findall(r'\\d+(?:\\.\\d+)?', fact.replace(',', ''))
            if not re.search(r'(?<!\\d)(?<!\\d\\.)' + re.escape(x) + r'(?!\\d|\\.\\d)', q)]


def get_vault_urls('''),
('''        for x in fact_nums:
            if x not in clean_quote_for_num:
                raise SourceValidationError(f"【入庫拒絕】核心事實數字 {x} 不在摘句中")''',
'''        miss = nums_missing(fact, q)
        if miss:
            raise SourceValidationError(f"【入庫拒絕】核心事實數字 {miss[0]} 不在摘句中")'''),
('''    content = vault_path.read_text(encoding="utf-8")
    urls = set()
    for m in re.finditer(r'-\\s+\\*\\*(?:證據網址|網址|出處)\\*\\*[：:]\\s*(https?://[^\\s\\)]+)', content):
        u = m.group(1).strip().rstrip("/")
        urls.add(u)
    return urls''',
'''    return {(e.get("url") or "").strip().rstrip("/") + "||" + (e.get("quote") or "").strip()
            for e in parse_experiences_markdown(vault_path)}'''),
('''            if u_clean in target_existing:
                raise SourceValidationError(
                    f"【入庫拒絕】網址已出現在事實庫中（重複網址：{u}）！一網址只能對應一筆知識！"
                )''','''            if u_clean + "||" + q in target_existing:
                raise SourceValidationError(
                    f"【入庫拒絕】同一網址＋同一摘句已在事實庫中（{u}）！"
                )'''),
('''            # if item.get("url"): vault_urls.add(...)''','''            vault_urls.add(item["url"].strip().rstrip("/") + "||" + item["quote"].strip())'''),
('''    items = parse_pending_markdown(pending_path)''','''    items = parse_pending_markdown(pending_path)
    n_sec = len(re.findall(r'^##\\s', pending_path.read_text(encoding="utf-8"), re.MULTILINE))
    bad_titles = [i["title"] for i in items if not re.match(r'^第\\s*\\d+\\s*輪｜', i["title"])]
    if n_sec == 0 or n_sec != len(items) or bad_titles:
        print(f"❌ 待入庫檔有 {n_sec} 段，合格解析 {len(items) - len(bad_titles)} 條：有段落格式不完整（標題要「## 第 N 輪｜」，網址／逐字摘句／核心事實都要有）。Exit Code 1")
        sys.exit(1)
    titles = [i["title"] for i in items] + [e["title"] for e in parse_experiences_markdown(vault_path)]
    dup = sorted({t for t in titles if titles.count(t) > 1})
    if dup:
        print(f"❌ 標題重複：{dup}。Exit Code 1")
        sys.exit(1)'''),
('''        for title, reason in rejected:
            print(f"  👉 「{title}」: {reason}")
''','''        for title, reason in rejected:
            print(f"  👉 「{title}」: {reason}")
        print("\\n❌ 有條目被退回，整批不寫入。Exit Code 1")
        sys.exit(1)
'''),
('''                    failed_checks.append((title, f"逐字驗證未通過：{why}"))
                    continue
                print("✅ 逐字驗證 PASS")''','''                    failed_checks.append((title, f"逐字驗證未通過：{why}"))
                    continue
                miss = nums_missing(entry.get("fact", ""), quote)
                if miss:
                    print("❌ 數字不符")
                    failed_checks.append((title, f"核心事實數字 {miss[0]} 不在摘句中"))
                    continue
                print("✅ 逐字驗證 PASS")'''),
]
for old, new in E:
    if s.count(old) != 1:
        print("❌ 找不到（或找到不只一處）：", old[:50].replace("\n", " ")); sys.exit(1)
    s = s.replace(old, new)
open(P + ".bak", "w", encoding="utf-8").write(open(P, encoding="utf-8").read())
open(P, "w", encoding="utf-8").write(s)
print("✅ 8 處修改完成，舊版備份為 bionic_knowledge_gate.py.bak")
