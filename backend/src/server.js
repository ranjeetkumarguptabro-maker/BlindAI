const http = require("http");
const env = require("./config/env");
const aiService = require("./services/ai/aiService");
const environmentController = require("./controllers/environmentController");
const voiceController = require("./controllers/voiceController");
const routesController = require("./controllers/routesController");

/**
 * Dependency-free, lightweight HTTP API server for Blind AI Backend
 */
const server = http.createServer(async (req, res) => {
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
  const pathname = parsedUrl.pathname;

  // JSON helper
  const sendJson = (statusCode, data) => {
    res.writeHead(statusCode, { "Content-Type": "application/json" });
    res.end(JSON.stringify(data));
  };

  // Helper to read JSON request body
  const readBody = () => new Promise((resolve) => {
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
    // Health Check
    if (pathname === "/health" || pathname === "/api/v1/health") {
      return sendJson(200, {
        status: "ok",
        service: "Blind AI Backend",
        aiProvider: aiService.activeProviderName,
        geminiConfigured: !!env.geminiApiKey,
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
});

server.listen(env.port, () => {
  console.log(`\n=================================================`);
  console.log(`🚀 Blind AI Backend listening on port ${env.port}`);
  console.log(`🤖 Active AI Provider: ${aiService.activeProviderName}`);
  console.log(`🔑 Gemini API Key configured: ${env.geminiApiKey ? "YES (from GEMINI_API_KEY environment variable)" : "NO"}`);
  console.log(`📱 Base URL: http://localhost:${env.port}/api/v1`);
  console.log(`=================================================\n`);
});

module.exports = server;
