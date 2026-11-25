import glob,re,sys
bad=0
for f in sorted(glob.glob('01_Cognitive_Log/反查/*.md')):
    for n,l in enumerate(open(f,encoding='utf-8'),1):
        c=[x.strip() for x in l.strip().strip('|').split('|')]
        if len(c)<6 or c[2]!='【已驗證】': continue
        if not c[3].startswith('http') or len(c[4])<15:
            bad+=1; print('FAIL',f,n,c[0],'缺網址或摘句太短'); continue
        nums=re.findall(r'\d+(?:\.\d+)?',c[1].replace(',',''))
        miss=[x for x in nums if x not in c[4].replace(',','')]
        if miss: bad+=1; print('FAIL',f,n,c[0],'摘句缺少原句數字',miss)
print('FAIL 行數:',bad); sys.exit(1 if bad else 0)
