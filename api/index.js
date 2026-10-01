/**
 * Vercel Serverless Function entry point for Blind AI API
 */
const requestHandler = require("../backend/src/server");

module.exports = async (req, res) => {
  const parsed = new URL(req.url, "http://localhost");
  const originalUrl = req.headers["x-matched-path"] || parsed.searchParams.get("url") || parsed.searchParams.get("path");
  if (originalUrl) {
    req.url = originalUrl;
  }
  return requestHandler(req, res);
};
