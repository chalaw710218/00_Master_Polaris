<?php
/**
 * TastyIgniter Ultimate Fixer
 */

$baseDir = __DIR__;

echo "<h1>【曉】專案 - 系統終極修復工具</h1>";
echo "<pre>";

// 1. Fix .env file
$envPath = $baseDir . '/.env';
if (file_exists($envPath)) {
    $envContent = file_get_contents($envPath);
    
    // Replace APP_URL
    $envContent = preg_replace('/^APP_URL=.*$/m', 'APP_URL=https://34.9.115.248.nip.io', $envContent);
    
    // Add ASSET_URL if not exists
    if (strpos($envContent, 'ASSET_URL=') === false) {
        $envContent .= "\nASSET_URL=https://34.9.115.248.nip.io\n";
    }
    
    // Add FORCE_HTTPS if not exists
    if (strpos($envContent, 'FORCE_HTTPS=') === false) {
        $envContent .= "FORCE_HTTPS=true\n";
    }

    file_put_contents($envPath, $envContent);
    echo "✅ [.env] 檔案已強制更新為 HTTPS！\n";
} else {
    echo "❌ 找不到 .env 檔案！\n";
}

// 2. Load Laravel Environment to clear cache and create admin
require $baseDir . '/vendor/autoload.php';
$app = require_once $baseDir . '/bootstrap/app.php';

$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

// 3. Clear Caches
try {
    Illuminate\Support\Facades\Artisan::call('config:clear');
    Illuminate\Support\Facades\Artisan::call('cache:clear');
    Illuminate\Support\Facades\Artisan::call('view:clear');
    echo "✅ [Cache] 系統快取已徹底清除！\n";
} catch (\Exception $e) {
    echo "⚠️ [Cache] 清除快取失敗: " . $e->getMessage() . "\n";
}

// 4. Create Super Admin
try {
    $user = \Igniter\User\Models\User::where('email', 'chalaw710218@gmail.com')->first();
    
    if (!$user) {
        $user = new \Igniter\User\Models\User();
        $user->name = '陳品碩';
        $user->email = 'chalaw710218@gmail.com';
        $user->username = 'admin';
        $user->password = 'Cola0218';
        $user->super_user = true;
        $user->status = true;
        $user->save();
        echo "✅ [Admin] 超級管理員帳號 (chalaw710218@gmail.com) 已成功建立！\n";
    } else {
        $user->password = 'Cola0218'; // Reset password just in case
        $user->super_user = true;
        $user->save();
        echo "✅ [Admin] 超級管理員帳號已存在，已將密碼重置為 Cola0218！\n";
    }
} catch (\Exception $e) {
    echo "⚠️ [Admin] 建立管理員失敗: " . $e->getMessage() . "\n";
}

echo "</pre>";
echo "<h2>修復完成！請點擊下方按鈕前往登入頁面：</h2>";
echo "<a href='https://34.9.115.248.nip.io/admin' style='padding: 10px 20px; background: #ff6600; color: white; text-decoration: none; border-radius: 5px; font-size: 18px;'>前往登入後台</a>";
?>
