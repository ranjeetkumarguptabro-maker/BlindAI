/**
 * Vercel Serverless Function entry point for Blind AI API
 */
const requestHandler = require("../backend/src/server");

module.exports = async (req, res) => {
  return requestHandler(req, res);
};
