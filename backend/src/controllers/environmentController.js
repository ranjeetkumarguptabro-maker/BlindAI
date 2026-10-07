const aiService = require("../services/ai/aiService");

exports.describeEnvironment = async (req, res) => {
  try {
    const { imageBase64, userContext } = req.body || {};
    const result = await aiService.describeEnvironment({ imageBase64, userContext });
    return res.json({
      status: "success",
      data: result
    });
  } catch (err) {
    console.error("[EnvironmentController] Error describing environment:", err);
    return res.status(500).json({
      status: "error",
      message: err.message
    });
  }
};

exports.whereAmI = async (req, res) => {
  try {
    const { latitude, longitude, street, landmark, heading } = req.body || {};
    const result = await aiService.explainLocation({ latitude, longitude, street, landmark, heading });
    return res.json({
      status: "success",
      data: result
    });
  } catch (err) {
    console.error("[EnvironmentController] Error explaining location:", err);
    return res.status(500).json({
      status: "error",
      message: err.message
    });
  }
};

exports.detectSignboards = async (req, res) => {
  try {
    const { imageBase64, userContext } = req.body || {};
    const result = await aiService.detectSignboards({ imageBase64, userContext });
    return res.json({
      status: "success",
      data: result
    });
  } catch (err) {
    console.error("[EnvironmentController] Error detecting signboards:", err);
    return res.status(500).json({
      status: "error",
      message: err.message
    });
  }
};
