const aiService = require("../services/ai/aiService");
const { RIGA_ROAD_SIGNS_CATALOG, matchRigaRoadSign } = require("../data/rigaRoadSignsCatalog");

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

exports.getRoadSignsCatalog = async (req, res) => {
  try {
    const query = req.query?.q || "";
    const category = req.query?.category || "";
    let signs = RIGA_ROAD_SIGNS_CATALOG;
    if (category) {
      signs = signs.filter(s => s.category.toLowerCase() === category.toLowerCase());
    }
    const matched = query ? matchRigaRoadSign(query) : null;
    return res.json({
      status: "success",
      totalSigns: RIGA_ROAD_SIGNS_CATALOG.length,
      standard: "Latvian Road Sign Standard (LVS 77 / Vienna Convention) — Riga, Latvia + Urban Tree Obstacles",
      referenceImage: "/riga_road_signs.jpg",
      matchedSign: matched,
      data: signs
    });
  } catch (err) {
    console.error("[EnvironmentController] Error fetching road signs catalog:", err);
    return res.status(500).json({
      status: "error",
      message: err.message
    });
  }
};

