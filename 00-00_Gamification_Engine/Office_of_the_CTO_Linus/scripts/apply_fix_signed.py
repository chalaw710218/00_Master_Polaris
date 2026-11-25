# 門禁修正（簽章版：雪、林納斯）Claude 2026-11-25
# 必要修改每處都必須剛好找到一次，否則什麼都不寫；自動備份 .bak
import os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bionic_knowledge_gate.py")
s = open(P, encoding="utf-8").read()
orig = s
def rep(old, new, required=True):
    global s
    n = s.count(old)
    if n == 1:
        s = s.replace(old, new); return True
    if required:
        print("❌ 找不到（或找到不只一處）：", old.strip().splitlines()[0][:60]); sys.exit(1)
    return False

# 1. 數字要完整比對（1 不能靠 11B 蒙混）
rep("def validate_entry(", '''def nums_missing(fact: str, quote: str) -> list:
    """核心事實裡的數字，必須以完整數字出現在摘句裡（1 不能靠 11B 蒙混）"""
    q = quote.replace(',', '')
    return [x for x in re.findall(r'\\d+(?:\\.\\d+)?', fact.replace(',', ''))
            if not re.search(r'(?<!\\d)(?<!\\d\\.)' + re.escape(x) + r'(?!\\d|\\.\\d)', q)]


def validate_entry(''')
rep("unmatched_nums = [n for n in fact_nums if n not in quote_nums and n not in clean_quote_for_num]",
    "unmatched_nums = nums_missing(fact, quote)")

# 2. 去重改成「同網址＋同摘句」（只有雪版有舊的網址去重）
yuki_style = rep('''    content = vault_path.read_text(encoding="utf-8")
    urls = set()
    for m in re.finditer(r'-\\s+\\*\\*(?:證據網址|網址|出處)\\*\\*[：:]\\s*(https?://[^\\s\\)]+)', content):
        u = m.group(1).strip().rstrip("/")
        urls.add(u)
    return urls''', '''    return {(e.get("url") or "").strip().rstrip("/") + "||" + (e.get("quote") or "").strip()
            for e in parse_experiences_markdown(vault_path)}''', required=False)
if yuki_style:
    rep('''            if u_clean in target_existing:
                raise SourceValidationError(
                    f"【入庫拒絕】網址已出現在事實庫中（重複網址：{u}）！一網址只能對應一筆知識！"
                )''', '''            if u_clean + "||" + q in target_existing:
                raise SourceValidationError(
                    f"【入庫拒絕】同一網址＋同一摘句已在事實庫中（{u}）！"
                )''')
    rep('''            if item.get("url"):
                vault_urls.add(item["url"].strip().rstrip("/"))''',
        '''            vault_urls.add(item["url"].strip().rstrip("/") + "||" + item["quote"].strip())''')

# 3. 格式不完整、標題重複、同網址＋同摘句重複 → 整批退回
rep('''    items = parse_pending_markdown(pending_path)''', '''    items = parse_pending_markdown(pending_path)
    n_sec = len(re.findall(r'^##\\s', pending_path.read_text(encoding="utf-8"), re.MULTILINE))
    bad_titles = [i["title"] for i in items if not re.match(r'^第\\s*\\d+\\s*輪｜', i["title"])]
    if n_sec == 0 or n_sec != len(items) or bad_titles:
        print(f"❌ 待入庫檔有 {n_sec} 段，合格解析 {len(items) - len(bad_titles)} 條：有段落格式不完整（標題要「## 第 N 輪｜」，網址／逐字摘句／核心事實都要有）。Exit Code 1")
        sys.exit(1)
    # 只檢查新條目：新條目和事實庫重複、或新條目彼此重複（事實庫裡原有的重複不影響）
    _old = parse_experiences_markdown(vault_path)
    old_titles = {e["title"] for e in _old}
    new_titles = [i["title"] for i in items]
    dup = sorted({t for t in new_titles if t in old_titles or new_titles.count(t) > 1})
    if dup:
        print(f"❌ 標題重複：{dup}。Exit Code 1")
        sys.exit(1)
    old_keys = {((e.get("url") or "").strip().rstrip("/"), (e.get("quote") or "").strip()) for e in _old}
    new_keys = [(i["url"].strip().rstrip("/"), i["quote"].strip()) for i in items]
    dupk = [k for k in new_keys if k in old_keys or new_keys.count(k) > 1]
    if dupk:
        print(f"❌ 同一網址＋同一摘句重複：{dupk[0][0]}。Exit Code 1")
        sys.exit(1)''')

# 4. 有條目被退回 → 整批不產生待簽檔，Exit 1
rep('''        for title, reason in rejected:
            print(f"  👉 「{title}」: {reason}")
''', '''        for title, reason in rejected:
            print(f"  👉 「{title}」: {reason}")
        print("\\n❌ 有條目被退回，整批不產生待簽檔。Exit Code 1")
        sys.exit(1)
''')

open(P + ".bak", "w", encoding="utf-8").write(orig)
open(P, "w", encoding="utf-8").write(s)
print("✅ 修改完成（網址去重改寫：%s），舊版備份為 bionic_knowledge_gate.py.bak" % ("是" if yuki_style else "原本沒有，改由第 3 項處理"))
