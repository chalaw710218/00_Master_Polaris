# 🚀 曉專案：GCP 免費主機開通與 TastyIgniter (V4) 終極部署指南

這份指南將帶領您使用 Google 帳號，開通 Google Cloud Platform (GCP) 的「永久免費主機」，安裝 CloudPanel 伺服器管理面板，並**最終成功部署最新架構的 TastyIgniter v4 點餐系統**。

這是一份結合了基礎架設與高難度「雙層代理 (Nginx + Varnish) 除錯」的終極技術文件，為日後幫店家架設點餐系統的標準作業流程 (SOP)。

---

## ☁️ 第一階段：在 GCP 開通免費主機

1. **登入 GCP 控制台**
   * 打開瀏覽器，前往：[Google Cloud Console](https://console.cloud.google.com/)
   * 進入您既有的專案，點擊畫面中間的 **「➕ 建立 VM」** 或右下方的 **「Compute Engine」**。

2. **建立運算執行個體 (VM) 與關鍵設定**
   為了確保主機符合「永久免費」資格，請務必按照以下設定：
   * **區域 (Region)**：🚨 必須選擇美國機房 `us-central1`、`us-west1` 或 `us-east1`。
   * **機器類型**：選擇 **e2-micro** (2個 vCPU，1 GB 記憶體)。
   * **開機磁碟**：作業系統選 **Ubuntu 22.04 LTS**，磁碟選擇 **標準永久磁碟 (30 GB)**。
   * **防火牆**：勾選 **「允許 HTTP 流量」** 與 **「允許 HTTPS 流量」**。

   > 💡 **預估費用 $6.11？** 這是系統原價，符合免費資格者月底結帳會自動扣抵，帳單將為 **$0 元**。

---

## 🛠️ 第二階段：連線至主機與安裝 CloudPanel

1. **切換最高權限 (Root)**
   點擊機器的 **「SSH」** 按鈕開啟終端機，輸入以下指令切換身份（游標變為白色的 `root@...`）：
   ```bash
   sudo su -
   ```

2. **安裝 CloudPanel 面板**
   在 root 權限下，建立虛擬記憶體並執行安裝腳本（約需 30~45 分鐘）：
   ```bash
   fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
   curl -sS https://installer.cloudpanel.io/ce/v2/install.sh -o install.sh
   DB_ENGINE=MARIADB_10.11 bash install.sh
   ```

3. **解決 8443 Port 防火牆阻擋**
   如果 `https://外部IP:8443` 連線超時，請到 GCP 搜尋「防火牆 (VPC 網路)」 ➔ 「建立防火牆規則」。來源 IPv4 填 `0.0.0.0/0`，通訊埠勾選 TCP 並填寫 `8443`。

---

## ⚙️ 第三階段：建立網站與資料庫

1. **新增 PHP 網站 (使用 nip.io)**
   登入 CloudPanel (`https://外部IP:8443`)，進入右上角「+ 新增網站」 ➔ 「建立 PHP 網站」。
   *   **網域名稱**：輸入 `您機器的IP.nip.io` (例如 `34.9.115.248.nip.io`)
   *   **PHP 版本**：🚨 **TastyIgniter V4 需求較新，務必選擇 PHP 8.4**。

2. **建立專屬資料庫**
   在網站管理區 ➔ 「資料庫」 ➔ 「新增資料庫」：
   *   **名稱與使用者**: `tasty`
   *   **密碼**: `********` (基於安全考量已隱藏)

---

## 📦 第四階段：安裝 TastyIgniter V4 (最新架構)

回到 GCP SSH 終端機，執行以下指令將系統空投至網站：

1. **切換使用者並使用 Composer 安裝**
   ```bash
   sudo su - chalaw0218
   cd htdocs/34.9.115.248.nip.io
   rm index.php
   composer create-project tastyigniter/tastyigniter .
   ```

2. **修正「雙重目錄」與 Nginx 根目錄**
   Composer 解壓縮時可能會產生 `htdocs/htdocs` 雙層目錄。請將檔案搬移回上一層，並進入 CloudPanel 的 **Vhost 設定**，將 **Document Root** 精準指向 `public/` 資料夾。

3. **執行系統安裝指令**
   ```bash
   php artisan igniter:install
   ```

---

## ⚔️ 第五階段：終極除錯大戰 (四大魔王)

部署現代化的 Laravel 框架在 CloudPanel (Nginx + Varnish) 環境中，我們遭遇並破解了四個棘手的阻礙：

### 🚨 魔王一：HTTPS 混合內容阻擋 (網頁破圖)
**解法**：修改 Laravel 核心 `app/Providers/AppServiceProvider.php`，強行植入 `\Illuminate\Support\Facades\URL::forceScheme('https');`。並在 `.env` 中加入 `SESSION_SECURE_COOKIE=true` 與 `TRUSTED_PROXIES=*`。

### 🚨 魔王二：Varnish 快取吞噬 Cookie (無法登入)
**解法**：CloudPanel 預設的 Varnish 快取把安全憑證 (CSRF Token) 吃了。我們必須修改 Nginx 的 Vhost 設定，將所有流量直接繞過 Varnish，直通後端 PHP。

### 🚨 魔王三：Nginx 靜態檔案攔截 (CSS/JS 404)
**解法**：Nginx 預設直接從硬碟讀取 CSS/JS，但 TI 的資源是動態生成的。在 Nginx 設定檔加入回退規則：
```nginx
location ~* ^.+\.(css|js|...)$ {
    try_files $uri @backend;
}
```

### 🚨 魔王四：PHP-FPM 版本不對稱與資料庫鎖死
**解法**：
1. **資料庫鎖死**：重啟 MySQL (`systemctl restart mysql`)，清空資料庫 (`php artisan db:wipe`) 重新安裝。
2. **PHP 版本切換**：我們發現 PHP 8.4 的 FPM 跑在 Port `19001`，但 Nginx 還在連舊的 `20001`。我們直接修改 Nginx 的 `fastcgi_pass` 指向正確的 Port。

---

## 🎉 第六階段：成功登入！

經過底層搶修並透過腳本手動建立超級管理員後，系統完美運作：

*   **登入網址**: `https://34.9.115.248.nip.io/admin`
*   **管理員帳號**: `chalaw****@gmail.com` (基於安全考量部分隱藏)
*   **管理員密碼**: `********` (基於安全考量已隱藏)

**完美登入畫面：**
![TastyIgniter 登入頁面](file:///C:/Users/lenovo/.gemini/antigravity/brain/a9622cf8-bc97-45cf-9cc8-c38e44cf1d66/.user_uploaded/media_1790664648532.png)

**成功進入管理後台：**
![TastyIgniter 儀表板](file:///C:/Users/lenovo/.gemini/antigravity/brain/a9622cf8-bc97-45cf-9cc8-c38e44cf1d66/.user_uploaded/media_1790664985247.png)
