/**
 * Vercel Serverless catch-all for /api/* routes
 */
const requestHandler = require("../backend/src/server");

module.exports = async (req, res) => {
  if (req.query && Array.isArray(req.query.slug)) {
    req.url = "/api/" + req.query.slug.join("/");
  } else if (req.query && typeof req.query.slug === "string") {
    req.url = "/api/" + req.query.slug;
  }
  return requestHandler(req, res);
};
