const aiService = require("../services/ai/aiService");

exports.parseVoiceIntent = async (req, res) => {
  try {
    const { transcript, liveContext, imageBase64 } = req.body || {};
    if (!transcript) {
      return res.status(400).json({
        status: "error",
        message: "Missing 'transcript' in request body."
      });
    }

    const intentResult = await aiService.parseVoiceCommand({ transcript, liveContext, imageBase64 });
    return res.json({
      status: "success",
      data: intentResult
    });
  } catch (err) {
    console.error("[VoiceController] Error parsing voice intent:", err);
    return res.status(500).json({
      status: "error",
      message: err.message
    });
  }
};
