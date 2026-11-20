import subprocess
import sys

# Ensure UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    # Use git grep to get all files containing 'bionic-learning-yuki.md'
    cmd = ["git", "grep", "-l", "bionic-learning-yuki.md"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    
    lines = [l.strip() for l in res.stdout.splitlines() if l.strip()]
    
    # Filter: 不含 _archive 和 _未驗證封存 資料夾，且不含自身
    filtered = []
    for f in lines:
        if "_archive" in f or "_未驗證封存" in f:
            continue
        if f.endswith("bionic-learning-yuki.md"):
            continue
        filtered.append(f)
        
    print(f"搜尋到的數量: {len(filtered)}")
    print("檔案清單:")
    for f in filtered:
        print(f"  - {f}")
        
    if len(filtered) == 0:
        print("數量是 0，可以執行移動。")
    else:
        print("數量不是 0，依指令『不要移，把檔名列出來回報』。")

if __name__ == "__main__":
    main()
