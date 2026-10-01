const http = require("http");
const fs = require("fs");
const path = require("path");
const env = require("./config/env");
const aiService = require("./services/ai/aiService");
const supabaseClient = require("./services/db/supabaseClient");
const environmentController = require("./controllers/environmentController");
const voiceController = require("./controllers/voiceController");
const routesController = require("./controllers/routesController");

// Valid frontend application routes (SPA serving)
const VALID_FRONTEND_ROUTES = new Set([
  "/",
  "/preview",
  "/index.html",
  "/home",
  "/listening",
  "/destinationSearch",
  "/destination-search",
  "/routePreview",
  "/route-preview",
  "/activeNavigation",
  "/active-navigation",
  "/whereAmI",
  "/where-am-i",
  "/describeAround",
  "/describe-around",
  "/obstacleAlert",
  "/obstacle-alert",
  "/crosswalkSafety",
  "/crosswalk-safety"
]);

/**
 * Dependency-free, lightweight HTTP API server for Blind AI Backend
 */
const requestHandler = async (req, res) => {
  // CORS Headers
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

  if (req.method === "OPTIONS") {
    res.writeHead(204);
    res.end();
    return;
  }

  // Parse URL & Query
  const parsedUrl = new URL(req.url, `http://${req.headers.host || "localhost"}`);
  let pathname = parsedUrl.pathname;

  // Resolve true route if forwarded via Vercel serverless rewrites
  const forwardedPath = req.headers["x-matched-path"]
    || req.headers["x-vercel-matched-path"]
    || parsedUrl.searchParams.get("url")
    || parsedUrl.searchParams.get("path");

  if (forwardedPath && (pathname === "/api/index.js" || pathname === "/api" || pathname === "/src/server.js" || pathname === "/api/")) {
    pathname = forwardedPath.split("?")[0];
  }

  // JSON helper
  const sendJson = (statusCode, data) => {
    res.writeHead(statusCode, { "Content-Type": "application/json" });
    if (req.method === "HEAD") {
      res.end();
    } else {
      res.end(JSON.stringify(data));
    }
  };

  // Helper to read JSON request body
  const readBody = () => new Promise((resolve) => {
    if (req.method === "HEAD" || req.method === "GET") {
      resolve({});
      return;
    }
    let body = "";
    req.on("data", chunk => { body += chunk; });
    req.on("end", () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (e) {
        resolve({});
      }
    });
  });

  try {
    // 0. Interactive Web Simulator & Valid Frontend Application Routes (SPA)
    if (VALID_FRONTEND_ROUTES.has(pathname) && (req.method === "GET" || req.method === "HEAD")) {
      const candidatePaths = [
        path.resolve(__dirname, "../../index.html"),
        path.resolve(__dirname, "../../preview.html"),
        path.resolve(__dirname, "../preview.html"),
        path.resolve(__dirname, "../public/index.html"),
        path.resolve(process.cwd(), "index.html"),
        path.resolve(process.cwd(), "preview.html"),
        path.resolve(process.cwd(), "public/index.html")
      ];
      for (const p of candidatePaths) {
        if (fs.existsSync(p) && fs.statSync(p).isFile()) {
          const html = fs.readFileSync(p, "utf8");
          res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
          if (req.method === "HEAD") {
            res.end();
          } else {
            res.end(html);
          }
          return;
        }
      }
    }

    // Static assets in /docs/
    if (pathname.startsWith("/docs/") && req.method === "GET") {
      const subPath = pathname.replace(/^\//, "");
      const docCandidates = [
        path.resolve(__dirname, "../../", subPath),
        path.resolve(__dirname, "../", subPath),
        path.resolve(process.cwd(), subPath),
        path.resolve(process.cwd(), "public", subPath)
      ];
      for (const docFilePath of docCandidates) {
        if (fs.existsSync(docFilePath) && fs.statSync(docFilePath).isFile()) {
          const ext = path.extname(docFilePath).toLowerCase();
          const mimeTypes = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml"
          };
          res.writeHead(200, { "Content-Type": mimeTypes[ext] || "application/octet-stream" });
          fs.createReadStream(docFilePath).pipe(res);
          return;
        }
      }
    }

    // Health Check
    if (pathname === "/health" || pathname === "/api/v1/health") {
      return sendJson(200, {
        status: "ok",
        service: "Blind AI Backend",
        aiProvider: aiService.activeProviderName,
        geminiConfigured: !!env.geminiApiKey,
        supabaseConfigured: !!env.supabaseKey,
        timestamp: new Date().toISOString()
      });
    }

    // 1. Environment / Scene Description
    if (pathname === "/api/v1/environment/describe" && req.method === "POST") {
      req.body = await readBody();
      return environmentController.describeEnvironment(req, {
        json: data => sendJson(200, data),
        status: code => ({ json: data => sendJson(code, data) })
      });
    }

    // 2. Where Am I? Location Context
    if (pathname === "/api/v1/environment/where-am-i" && req.method === "POST") {
      req.body = await readBody();
      return environmentController.whereAmI(req, {
        json: data => sendJson(200, data),
        status: code => ({ json: data => sendJson(code, data) })
      });
    }

    // 3. Voice Intent Parsing
    if (pathname === "/api/v1/voice/intent" && req.method === "POST") {
      req.body = await readBody();
      return voiceController.parseVoiceIntent(req, {
        json: data => sendJson(200, data),
        status: code => ({ json: data => sendJson(code, data) })
      });
    }

    // 4. Routes List & Route Planning
    if (pathname === "/api/v1/routes" && req.method === "GET") {
      return routesController.getRoutes(req, {
        json: data => sendJson(200, data)
      });
    }

    if (pathname === "/api/v1/routes/plan" && req.method === "POST") {
      req.body = await readBody();
      return routesController.planRoute(req, {
        json: data => sendJson(200, data)
      });
    }

    // 5. Navigation Session Events (Obstacle logging & tracking)
    if (pathname.startsWith("/api/v1/navigation/sessions/") && pathname.endsWith("/events") && req.method === "POST") {
      const eventData = await readBody();
      console.log("[Backend] Recorded obstacle/navigation event:", eventData);
      
      // Persist to Supabase if configured
      try {
        await supabaseClient.recordObstacleEvent(eventData);
      } catch (dbErr) {
        console.warn("[Backend] Supabase log warning:", dbErr.message);
      }

      return sendJson(201, {
        status: "success",
        message: "Obstacle event recorded",
        eventId: "obs-" + Date.now(),
        data: eventData
      });
    }

    // 404 Fallback
    return sendJson(404, {
      status: "error",
      message: `Endpoint ${req.method} ${pathname} not found.`
    });

  } catch (err) {
    console.error("[Server Error]", err);
    return sendJson(500, {
      status: "error",
      message: err.message || "Internal server error"
    });
  }
};

const server = http.createServer(requestHandler);

if (require.main === module) {
  server.listen(env.port, () => {
    console.log(`\n=================================================`);
    console.log(`🚀 Blind AI Backend listening on port ${env.port}`);
    console.log(`🤖 Active AI Provider: ${aiService.activeProviderName}`);
    console.log(`🔑 Gemini API Key configured: ${env.geminiApiKey ? "YES (from GEMINI_API_KEY environment variable)" : "NO"}`);
    console.log(`🗄️  Supabase Key configured: ${env.supabaseKey ? "YES (from SUPABASE_KEY environment variable)" : "NO"}`);
    console.log(`📱 Base URL: http://localhost:${env.port}/api/v1`);
    console.log(`=================================================\n`);
  });
}

requestHandler.server = server;
module.exports = requestHandler;
