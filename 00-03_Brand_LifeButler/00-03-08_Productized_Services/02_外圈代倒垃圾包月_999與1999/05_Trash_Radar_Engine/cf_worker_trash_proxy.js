/**
 * 生活管家・台東垃圾車即時車聯網 Cloudflare Worker 反向代理
 * 部署於 Cloudflare Workers (免費版每日 100,000 次請求)
 * 作用：為中華電信清運 API 提供安全 HTTPS 轉發與 CORS Access-Control-Allow-Origin 支援
 */

export default {
  async fetch(request, env, ctx) {
    // 跨域 CORS Header
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, max-age=15" // 緩存 15 秒保護公所車機
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);
    // 預設抓取台東市公所 (customer_id=22) 即時車輛位置
    const targetUrl = "https://www.bstruck.hinet.net/MIS/subsystem/XML/Appcarlocation.ashx?customer_id=22&key=1";

    try {
      const response = await fetch(targetUrl, {
        headers: {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
      });

      const xmlText = await response.text();
      return new Response(xmlText, {
        status: response.status,
        headers: corsHeaders
      });
    } catch (err) {
      return new Response(`<Error>${err.message}</Error>`, {
        status: 502,
        headers: corsHeaders
      });
    }
  }
};
