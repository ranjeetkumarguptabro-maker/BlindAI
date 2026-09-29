const GeminiProvider = require("./geminiProvider");
const env = require("../../config/env");

class AIService {
  constructor() {
    this.providers = new Map();
    
    // Register default providers
    this.registerProvider("gemini", new GeminiProvider());
    
    // Set active provider from environment variable
    this.activeProviderName = env.defaultProvider || "gemini";
  }

  /**
   * Registers an AI provider implementation
   * @param {string} name 
   * @param {AIProviderInterface} provider 
   */
  registerProvider(name, provider) {
    this.providers.set(name.toLowerCase(), provider);
  }

  /**
   * Switches the active AI provider dynamically
   * @param {string} name 
   */
  setActiveProvider(name) {
    const key = name.toLowerCase();
    if (!this.providers.has(key)) {
      throw new Error(`AI Provider "${name}" is not registered.`);
    }
    this.activeProviderName = key;
    console.log(`[AIService] Switched active AI provider to: ${name}`);
  }

  get activeProvider() {
    const provider = this.providers.get(this.activeProviderName);
    if (!provider) {
      throw new Error(`Active provider "${this.activeProviderName}" not found.`);
    }
    return provider;
  }

  // Delegated AI capabilities
  async describeEnvironment(params) {
    return this.activeProvider.describeEnvironment(params);
  }

  async explainLocation(params) {
    return this.activeProvider.explainLocation(params);
  }

  async parseVoiceCommand(params) {
    return this.activeProvider.parseVoiceCommand(params);
  }
}

// Export singleton instance
module.exports = new AIService();
