// Environment configuration validator
const fs = require("fs");
const path = require("path");

// Fallback loader if not run with node --env-file
const loadEnvFile = () => {
  const possiblePaths = [
    path.resolve(process.cwd(), ".env"),
    path.resolve(__dirname, "../../.env")
  ];
  for (const envPath of possiblePaths) {
    if (fs.existsSync(envPath)) {
      try {
        const content = fs.readFileSync(envPath, "utf8");
        const lines = content.split("\n");
        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || trimmed.startsWith("#")) continue;
          const eqIdx = trimmed.indexOf("=");
          if (eqIdx !== -1) {
            const key = trimmed.slice(0, eqIdx).trim();
            const val = trimmed.slice(eqIdx + 1).trim();
            if (!process.env[key]) {
              process.env[key] = val;
            }
          }
        }
      } catch (e) {
        // Ignore fallback load error
      }
    }
  }
};

loadEnvFile();

const env = {
  port: parseInt(process.env.PORT || "3000", 10),
  environment: process.env.ENVIRONMENT || "development",
  geminiApiKey: process.env.GEMINI_API_KEY || "",
  supabaseKey: process.env.SUPABASE_KEY || process.env.SUPABASE_ANON_KEY || "",
  supabaseUrl: process.env.SUPABASE_URL || "",
  defaultProvider: process.env.DEFAULT_AI_PROVIDER || "gemini",
  geminiModel: process.env.GEMINI_MODEL || "gemini-1.5-flash",
  maxTokens: parseInt(process.env.MAX_TOKENS || "300", 10),
  temperature: parseFloat(process.env.TEMPERATURE || "0.3")
};

if (!env.geminiApiKey) {
  console.warn("⚠️  [Blind AI Backend] Warning: GEMINI_API_KEY is not defined in environment variables. Real Gemini calls will fall back to local mock reasoning.");
}

if (!env.supabaseKey) {
  console.warn("ℹ️  [Blind AI Backend] Supabase Key is not set in environment variables. Database operations will run in local in-memory mode.");
}

module.exports = env;
