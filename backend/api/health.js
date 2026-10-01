/**
 * Native Vercel Serverless Function for /api/health
 */
const requestHandler = require("../src/server");

module.exports = async (req, res) => {
  req.url = "/health";
  return requestHandler(req, res);
};
