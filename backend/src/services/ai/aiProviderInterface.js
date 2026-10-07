/**
 * AI Provider Abstract Interface
 * Enables modular swapping between Google Gemini, Anthropic Claude, OpenAI, or on-device models.
 */
class AIProviderInterface {
  /**
   * Describes the environment / camera frame for a visually impaired user.
   * @param {Object} params
   * @param {string} [params.imageBase64] Optional base64-encoded camera frame
   * @param {Object} [params.userContext] User heading, speed, location
   * @returns {Promise<{ description: string, hasHazard: boolean, hazardDetail?: string }>}
   */
  async describeEnvironment(params) {
    throw new Error("Method describeEnvironment() must be implemented by provider");
  }

  /**
   * Formulates clear, landmark-based orientation instructions.
   * @param {Object} params
   * @param {number} params.latitude
   * @param {number} params.longitude
   * @param {string} [params.street]
   * @param {string} [params.landmark]
   * @param {string} [params.heading]
   * @returns {Promise<{ headline: string, orientationDetails: string }>}
   */
  async explainLocation(params) {
    throw new Error("Method explainLocation() must be implemented by provider");
  }

  /**
   * Parses natural language spoken commands into structured intents.
   * @param {Object} params
   * @param {string} params.transcript User spoken text
   * @returns {Promise<{ intent: string, destination?: string, confidence: number }>}
   */
  async parseVoiceCommand(params) {
    throw new Error("Method parseVoiceCommand() must be implemented by provider");
  }

  /**
   * Detects and reads signboards, street names, entrance signs, transit stops, and placards from camera frames.
   * @param {Object} params
   * @param {string} [params.imageBase64]
   * @param {Object} [params.userContext]
   * @returns {Promise<{ signs: Array<Object>, summary: string, processingProvider: string }>}
   */
  async detectSignboards(params) {
    throw new Error("Method detectSignboards() must be implemented by provider");
  }
}

module.exports = AIProviderInterface;
