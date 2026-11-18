/**
 * 生活管家・台東垃圾車即時車聯網 Cloudflare Worker 反向代理 (v2.0)
 * 部署於 Cloudflare Workers (免費版每日 100,000 次請求)
 * 作用：
 * 1. 為中華電信清運 API (Appcarlocation.ashx) 提供安全 HTTPS 轉發與 CORS 支援
 * 2. 自動並行聚合台東市清潔隊全量 20 條清運路線 (run_id) 之即時車機座標
 */

const TAITUNG_RUN_IDS = [
  "1399", "1519", "1503", "1509", "1560",
  "1468", "1449", "1593", "1447", "1551",
  "1520", "1454", "1451", "1470", "2558",
  "1444", "1466", "1445", "1446", "1404"
];

const DEFAULT_DEVICE = "00000000-0000-0000-0000-000000000000";

export default {
  async fetch(request, env, ctx) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, max-age=15"
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    const reqUrl = new URL(request.url);
    const runParam = reqUrl.searchParams.get("run");
    const runIdParam = reqUrl.searchParams.get("run_id");
    const targetParam = reqUrl.searchParams.get("url");

    // 🔒 安全防護 1：嚴格白名單域名檢查 (只允許 www.bstruck.hinet.net，其餘一律 403)
    if (targetParam) {
      try {
        const parsedTarget = new URL(targetParam);
        if (parsedTarget.hostname !== "www.bstruck.hinet.net") {
          return new Response("Forbidden: Domain not allowed", { status: 403, headers: corsHeaders });
        }
      } catch (_) {
        return new Response("Forbidden: Invalid URL", { status: 403, headers: corsHeaders });
      }
    }

    // 路由 1: 官方動態清運班表與預估時間 (/schedule?run_id=XXXX)
    if (reqUrl.pathname === "/schedule" || runIdParam || (targetParam && targetParam.includes("scheduletime.ashx"))) {
      let targetRunId = runIdParam;
      if (!targetRunId && targetParam) {
        try {
          const tUrl = new URL(targetParam);
          targetRunId = tUrl.searchParams.get("run_id");
        } catch (_) {}
      }
      if (!targetRunId && runParam) targetRunId = runParam;

      if (!targetRunId) {
        return new Response(`<Error>Missing run_id parameter</Error>`, { status: 400, headers: corsHeaders });
      }

      // 🔒 安全防護 2：run_id 只接受純數字，非數字一律 400
      if (!/^\d+$/.test(targetRunId)) {
        return new Response(`<Error>Invalid run_id: must be numeric digits only</Error>`, { status: 400, headers: corsHeaders });
      }

      const formatParam = reqUrl.searchParams.get("format");
      const noCacheTimestamp = Date.now();
      const scheduleApiUrl = `https://www.bstruck.hinet.net/MIS/subsystem/xml/scheduletime.ashx?key=1&status_id=0&run_id=${targetRunId}&_nocache=${noCacheTimestamp}`;
      try {
        const resp = await fetch(scheduleApiUrl, {
          headers: { 
            "User-Agent": "Mozilla/5.0 (Android)",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
          },
          cf: { cacheTtl: 0, cacheEverything: false }
        });
        const text = await resp.text();

        // 🌟 林納斯：支援 format=text 純文字格式（供手機瀏覽器一秒看懂結論）
        if (formatParam === "text") {
          const cfCountry = request.cf ? (request.cf.country || "未知") : (request.headers.get("CF-IPCountry") || "未知");
          const cfColo = request.cf ? (request.cf.colo || "未知") : "未知";

          const stopRegex = /<ScheduleTime\s+([^>]*?)>(.*?)<\/ScheduleTime>/g;
          const stops = [];
          let match;
          let cleanedCount = 0;
          let arrivedCount = 0;
          let arrivingCount = 0;
          let hasCarNoCount = 0;

          while ((match = stopRegex.exec(text)) !== null) {
            const attrStr = match[1];
            const getAttr = (name) => {
              const m = attrStr.match(new RegExp(`${name}="([^"]*)"`));
              return m ? m[1] : "";
            };
            const sName = getAttr("name");
            const sStime = getAttr("stime");
            const sEstimate = getAttr("estimate");
            const sCarNo = getAttr("car_no");

            if (sEstimate.includes("已清運")) cleanedCount++;
            if (sEstimate.includes("已抵達")) arrivedCount++;
            if (sEstimate.includes("約")) arrivingCount++;
            if (sCarNo.trim()) hasCarNoCount++;

            stops.push({ name: sName, stime: sStime, estimate: sEstimate, carNo: sCarNo });
          }

          const hasLive = (cleanedCount > 0 || arrivedCount > 0 || arrivingCount > 0 || hasCarNoCount > 0);
          let line1 = "";
          if (hasLive) {
            const parts = [];
            if (cleanedCount > 0) parts.push(`${cleanedCount} 站已清運`);
            if (arrivingCount > 0) parts.push(`${arrivingCount} 站約X分到`);
            if (arrivedCount > 0) parts.push(`${arrivedCount} 站已抵達`);
            if (hasCarNoCount > 0 && parts.length === 0) parts.push(`${hasCarNoCount} 站有車號`);
            line1 = `✅ 拿得到即時狀態（${parts.join("、")}）`;
          } else {
            line1 = `❌ 沒有即時狀態（全部只顯示表定時間）`;
          }

          const twTime = new Date().toLocaleString("zh-TW", {
            timeZone: "Asia/Taipei",
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false
          });
          const line2 = `連線地區與節點：${cfCountry} (${cfColo}) ｜ 抓取時間：${twTime} (台灣時間)`;

          const stopLines = stops.map(s => {
            return `${s.name} ｜ 表定: ${s.stime} ｜ estimate: ${s.estimate || "無"} ｜ car_no: ${s.carNo || "無"}`;
          });

          const plainText = [line1, line2, ...stopLines].join("\n");
          return new Response(plainText, {
            status: resp.status,
            headers: {
              "Access-Control-Allow-Origin": "*",
              "Content-Type": "text/plain; charset=utf-8",
              "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
              "Pragma": "no-cache"
            }
          });
        }

        // 預設維持 XML 回傳，雷達繼續使用
        return new Response(text, {
          status: resp.status,
          headers: {
            ...corsHeaders,
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache"
          }
        });
      } catch (err) {
        return new Response(`<Error>${err.message}</Error>`, { status: 502, headers: corsHeaders });
      }
    }

    // 若指定單一合法的 bstruck URL，代理轉發
    if (targetParam && !targetParam.includes("Appcarlocation.ashx")) {
      try {
        const resp = await fetch(targetParam, {
          headers: { "User-Agent": "Mozilla/5.0 (Android)" }
        });
        const text = await resp.text();
        return new Response(text, { status: resp.status, headers: corsHeaders });
      } catch (err) {
        return new Response(`<Error>${err.message}</Error>`, { status: 502, headers: corsHeaders });
      }
    }

    // 解析要查詢的 run_id 清單
    let runIds = TAITUNG_RUN_IDS;
    if (runParam) {
      const parsed = runParam.split(/[^0-9]+/).filter(Boolean);
      if (parsed.length > 0) runIds = parsed;
    } else if (targetParam && targetParam.includes("run=")) {
      try {
        const tUrl = new URL(targetParam);
        const r = tUrl.searchParams.get("run");
        if (r) {
          const parsed = r.split(/[^0-9]+/).filter(Boolean);
          if (parsed.length > 0) runIds = parsed;
        }
      } catch (_) {}
    }

    try {
      // 並行抓取台東各清運路線即時車機位置
      const fetchPromises = runIds.map(async (rid) => {
        const apiUrl = `https://www.bstruck.hinet.net/MIS/subsystem/XML/Appcarlocation.ashx?run=${rid}&device=${DEFAULT_DEVICE}&customer_id=22&key=1`;
        try {
          const res = await fetch(apiUrl, {
            headers: { "User-Agent": "Mozilla/5.0 (Android)" },
            cf: { cacheTtl: 15, cacheEverything: true }
          });
          if (!res.ok) return "";
          return await res.text();
        } catch (_) {
          return "";
        }
      });

      const results = await Promise.all(fetchPromises);
      const carTags = [];

      for (const xml of results) {
        if (!xml || !xml.includes("<Car ")) continue;
        const matches = xml.match(/<Car\s[^>]*>[\s\S]*?<\/Car>|<Car\s[^>]*\/>/g);
        if (matches) {
          for (const tag of matches) {
            carTags.push("  " + tag.trim());
          }
        }
      }

      const combinedXml = `<?xml version="1.0" encoding="utf-8"?>\n<Items>\n${carTags.join("\n")}\n</Items>`;
      return new Response(combinedXml, { status: 200, headers: corsHeaders });
    } catch (err) {
      return new Response(`<Error>${err.message}</Error>`, { status: 502, headers: corsHeaders });
    }
  }
};
