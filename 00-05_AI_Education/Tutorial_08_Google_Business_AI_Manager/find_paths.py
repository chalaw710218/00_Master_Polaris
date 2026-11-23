import os

def find_repo():
    possible_paths = [
        r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\clients\01_Taitung_Shokunin_Diner\website",
        r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\website",
        r"C:\Users\lenovo\shokunin-taitung"
    ]
    for p in possible_paths:
        if os.path.exists(p):
            print("Found:", p, "contents:", os.listdir(p))

find_repo()
