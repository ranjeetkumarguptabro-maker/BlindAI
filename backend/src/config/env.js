// Environment configuration validator

const env = {
  port: parseInt(process.env.PORT || "3000", 10),
  environment: process.env.ENVIRONMENT || "development",
  geminiApiKey: process.env.GEMINI_API_KEY || "",
  defaultProvider: process.env.DEFAULT_AI_PROVIDER || "gemini",
  geminiModel: process.env.GEMINI_MODEL || "gemini-1.5-flash",
  maxTokens: parseInt(process.env.MAX_TOKENS || "300", 10),
  temperature: parseFloat(process.env.TEMPERATURE || "0.3")
};

if (!env.geminiApiKey) {
  console.warn("⚠️  [Blind AI Backend] Warning: GEMINI_API_KEY is not defined in environment variables. Real Gemini calls will fall back to local mock reasoning.");
}

module.exports = env;
