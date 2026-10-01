/**
 * Serverless catch-all if deployed from backend/ directory
 */
const requestHandler = require("../src/server");

module.exports = async (req, res) => {
  return requestHandler(req, res);
};
