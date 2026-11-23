import os

registry_path = r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\clients\00_MERCHANT_MASTER_REGISTRY.md"

if os.path.exists(registry_path):
    with open(registry_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 檢查是否有 facebook 欄位，若無則補充
    if "https://www.facebook.com/p/職人食堂-61561543646858/" not in content:
        content = content.replace(
            "- **官方網站**：[https://chalaw710218.github.io/shokunin-taitung/](https://chalaw710218.github.io/shokunin-taitung/)",
            "- **官方網站**：[https://chalaw710218.github.io/shokunin-taitung/](https://chalaw710218.github.io/shokunin-taitung/)\n- **Facebook 官方專頁**：[https://www.facebook.com/p/職人食堂-61561543646858/](https://www.facebook.com/p/職人食堂-61561543646858/)"
        )
        with open(registry_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated registry with Facebook URL!")
    else:
        print("Registry already has Facebook URL.")
