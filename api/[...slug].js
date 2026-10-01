/**
 * Vercel Serverless catch-all for /api/* routes
 */
const requestHandler = require("../backend/src/server");

module.exports = async (req, res) => {
  return requestHandler(req, res);
};
