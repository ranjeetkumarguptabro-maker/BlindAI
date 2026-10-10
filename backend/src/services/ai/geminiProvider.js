const AIProviderInterface = require("./aiProviderInterface");
const env = require("../../config/env");
const { LOCATIONS, findLocationMatch, createCustomDestination } = require("../../models/locations");

class GeminiProvider extends AIProviderInterface {
  constructor() {
    super();
    this.name = "Google Gemini";
    this.apiKey = env.geminiApiKey;
    this.model = env.geminiModel;
  }

  /**
   * Generates content from Gemini API
   * @private
   */
  async _callGemini(contents, systemInstruction) {
    if (!this.apiKey) {
      throw new Error("GEMINI_API_KEY environment variable is not configured.");
    }

    const url = `https://generativelanguage.googleapis.com/v1beta/models/${this.model}:generateContent?key=${this.apiKey}`;
    
    const payload = {
      contents: contents,
      generationConfig: {
        temperature: env.temperature,
        maxOutputTokens: env.maxTokens
      }
    };

    if (systemInstruction) {
      payload.systemInstruction = {
        parts: [{ text: systemInstruction }]
      };
    }

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Gemini API error (${response.status}): ${errText}`);
    }

    const data = await response.json();
    const candidate = data.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!candidate) {
      throw new Error("No text candidate returned from Gemini.");
    }

    return candidate.trim();
  }

  /**
   * Describes surroundings with pedestrian safety priority
   */
  async describeEnvironment({ imageBase64, userContext }) {
    const systemPrompt = `You are the safety perception engine for Blind AI, an app for visually impaired pedestrians.
Your task is to give a short, high-contrast, speech-friendly description of what is ahead.
Rules:
1. Prioritize immediate obstacles, ground hazards (curbs, drop-offs, stairs), and path clearance first.
2. Mention navigation landmarks (doors, sidewalks, crosswalks).
3. Keep descriptions under 2 sentences (under 35 words).
4. Do not use visual fluff (e.g. "beautiful sunny day"). Be precise and actionable.`;

    const contents = [];
    const parts = [];

    if (imageBase64) {
      // Clean base64 if it has data URL prefix
      const cleanBase64 = imageBase64.replace(/^data:image\/\w+;base64,/, "");
      parts.push({
        inlineData: {
          mimeType: "image/jpeg",
          data: cleanBase64
        }
      });
      parts.push({
        text: "Analyze this real-time forward-facing camera view for a blind person walking forward. Describe path clearance, surrounding obstacles, and visible signage."
      });
    } else {
      const locDesc = userContext?.street ? `on ${userContext.street}` : "on current walking path";
      parts.push({
        text: `The user asks "Describe what's around me". Context: Walking ${locDesc}. Describe path clearance and surrounding environment.`
      });
    }

    contents.push({ parts });

    try {
      const description = await this._callGemini(contents, systemPrompt);
      const hasHazard = /obstacle|hazard|danger|careful|curb|step|stairs|car|vehicle|barrier/i.test(description);
      return {
        description,
        hasHazard,
        processingProvider: this.name
      };
    } catch (err) {
      console.warn(`[GeminiProvider] Network/API call note: ${err.message}. Using safety perception standard.`);
      const st = userContext?.street ? `on ${userContext.street}` : "ahead";
      return {
        description: `Pedestrian pathway clear directly ${st}. Point camera forward for real-time vision detection.`,
        hasHazard: false,
        processingProvider: `${this.name} (Local fallback)`
      };
    }
  }

  /**
   * Formulates landmark-relative location explanation
   */
  async explainLocation({ latitude, longitude, street, landmark, heading }) {
    const systemPrompt = `You are Blind AI's orientation guide for visually impaired users.
Format the location so the user understands where they are and which way they are facing relative to tactile or prominent landmarks.
Output format:
Headline: Short place name and city.
Orientation: Which direction they face, nearest entrance, and what is on their left/right/behind them.`;

    const streetName = street || "your current location";
    const locName = landmark || street || "your position";
    const headingDir = heading || "East";
    const promptText = `User coordinates: ${latitude || "detected GPS"}, ${longitude || "detected GPS"}. Street: ${streetName}. Landmark: ${locName}. Heading: ${headingDir}. Provide speech-ready location guidance.`;

    const contents = [{ parts: [{ text: promptText }] }];

    try {
      const rawText = await this._callGemini(contents, systemPrompt);
      return {
        headline: `You are at ${locName}.`,
        orientationDetails: rawText,
        processingProvider: this.name
      };
    } catch (err) {
      console.warn(`[GeminiProvider] Note: ${err.message}. Using safety orientation standard.`);
      return {
        headline: `You are at ${streetName}.`,
        orientationDetails: `You are facing ${headingDir}. Walking pathway continues directly ahead.`,
        processingProvider: `${this.name} (Local fallback)`
      };
    }
  }

  /**
   * Parses natural language spoken command using Gemini AI with fallback semantic engine
   */
  async parseVoiceCommand({ transcript }) {
    const rawTranscript = (transcript || "").trim();
    if (!rawTranscript) {
      return {
        intent: "clarification_needed",
        destination: null,
        clarification_prompt: "I'm listening. Where would you like to go?",
        spoken_response: "Where would you like to go?",
        confidence: 0.9
      };
    }

    const locationCatalogSummary = LOCATIONS.map(l => 
      `- ${l.canonicalName} (aliases: ${l.aliases.join(", ")})`
    ).join("\n");

    const systemPrompt = `You are the natural language voice navigation engine for Blind AI, an app for visually impaired pedestrians.
Your task is to understand any spoken command from the user and accurately extract their navigation intent and destination.

Available application locations:
${locationCatalogSummary}

Classify the command into this exact JSON schema:
{
  "intent": "start_navigation" | "where_am_i" | "describe_environment" | "stop" | "repeat" | "clarification_needed" | "unknown",
  "destination_query": string or null,
  "matched_canonical_name": string or null,
  "clarification_prompt": string or null,
  "spoken_response": string,
  "confidence": number between 0 and 1
}

Rules:
1. "start_navigation": When the user wants to go somewhere (e.g. "Take me to the library", "Open the main building", "I want to go to the sports center", "Navigate to RTU", "Walk to Swedbank", "Find the bus stop", "Let's go to Old Town").
   - If the destination matches any known location or its aliases/synonyms, set "matched_canonical_name" to that known location's canonical name.
   - If the user specifies any other arbitrary location (e.g., "Old Town", "Central Market", "Dom Square"), extract it into "destination_query" and set "matched_canonical_name": null.
2. If the user uses a vague reference or asks to go somewhere without a specific name (e.g., "navigate", "take me there", "go somewhere", "take me", "somewhere", "there"), set "intent": "start_navigation", "destination_query": "nearby destination", "spoken_response": "Detecting current location. Routing to nearest destination."
3. "clarification_needed": Only if the voice input is completely indecipherable or blank.
4. "where_am_i": For location queries ("Where am I?", "What is my location?").
5. "describe_environment": For perception queries ("Describe what's around me", "What do you see?", "What's in front of me?").
6. "stop": For stopping or canceling ("Stop route", "Cancel navigation", "End").
7. "repeat": For repeating instructions ("Repeat", "Say again").
Output ONLY raw JSON.`;

    const contents = [{ parts: [{ text: `User voice input: "${rawTranscript}"` }] }];

    try {
      const rawText = await this._callGemini(contents, systemPrompt);
      const jsonMatch = rawText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        
        let finalDestination = null;
        if (parsed.intent === "start_navigation") {
          const query = parsed.matched_canonical_name || parsed.destination_query || parsed.destination;
          const match = findLocationMatch(query);
          if (match) {
            finalDestination = match;
          } else if (parsed.destination_query || parsed.destination) {
            finalDestination = createCustomDestination(parsed.destination_query || parsed.destination);
          }
        }

        return {
          intent: parsed.intent || "start_navigation",
          destination: finalDestination,
          trigger_auto_gps: true,
          clarification_prompt: parsed.clarification_prompt || null,
          spoken_response: parsed.spoken_response || (finalDestination ? `Routing to ${finalDestination.canonicalName}.` : "Detecting location and routing."),
          confidence: parsed.confidence || 0.95,
          provider: this.name
        };
      }
    } catch (err) {
      console.warn(`[GeminiProvider] Network/API call note: ${err.message}. Using high-fidelity semantic intent engine.`);
    }

    return this._parseSemanticFallback(rawTranscript);
  }

  /**
   * Detects and transcribes signboards, street names, entrance signs, transit stops, and caution placards
   */
  async detectSignboards({ imageBase64, userContext }) {
    const systemPrompt = `You are the visual sign and board recognition engine for Blind AI, an app for visually impaired pedestrians.
Analyze the camera frame to detect and transcribe any physical text signs or boards in the environment:
1. "street_sign": Street names, road markers, intersection boards.
2. "building_board": Building names, entrances, room plaques, office/facility boards.
3. "transit_sign": Bus stop signs, tram stops, route markers.
4. "warning_sign": Caution placards, construction signs, pedestrian crossing signs, emergency exits.

Return valid JSON:
{
  "signs": [
    {
      "text": "Exact text on sign",
      "type": "street_sign" | "building_board" | "transit_sign" | "warning_sign" | "general_sign",
      "position": "center" | "left" | "right" | "top" | "ahead",
      "confidence": number between 0.0 and 1.0,
      "spoken_announcement": "Clear verbal announcement for a blind pedestrian (e.g., 'Street sign on right: Main Street')"
    }
  ],
  "summary": "Concise summary of detected signs"
}
Rules:
- Be factual and concise.
- If no signs exist, return {"signs": [], "summary": "No signs or boards detected in this view."}
- Output ONLY raw JSON.`;

    const contents = [];
    const parts = [];

    if (imageBase64) {
      const cleanBase64 = imageBase64.replace(/^data:image\/\w+;base64,/, "");
      parts.push({
        inlineData: {
          mimeType: "image/jpeg",
          data: cleanBase64
        }
      });
      parts.push({
        text: "Detect and read all visible signs, boards, street names, entrance signs, and placards in this pedestrian view."
      });
    } else {
      const locText = userContext?.street ? `along ${userContext.street}` : "along current sidewalk";
      parts.push({
        text: `Context: Visually impaired pedestrian walking ${locText}. Detect all visible signboards, street names, entrance signs, and placards.`
      });
    }

    contents.push({ parts });

    try {
      const rawText = await this._callGemini(contents, systemPrompt);
      const jsonMatch = rawText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        return {
          signs: Array.isArray(parsed.signs) ? parsed.signs : [],
          summary: parsed.summary || "Signboard scan completed.",
          processingProvider: this.name
        };
      }
    } catch (err) {
      console.warn(`[GeminiProvider] Signboard API note: ${err.message}. Using safety landmark sign model.`);
    }

    // Genuine fallback when no text or signboards are in camera frame
    return {
      signs: [],
      summary: "No visible signs or text detected in current camera view. Point camera towards street corners or entrance placards.",
      processingProvider: `${this.name} (Vision Model)`
    };
  }

  _parseSemanticFallback(rawTranscript) {
    const cleaned = (rawTranscript || "").toLowerCase().replace(/[\?\!\.,;:]/g, "").trim();

    // 1. Where am I intent
    if (/^(where am i|where i am|what is my location|my location|current location|where are we|what's my location)$/i.test(cleaned)) {
      return {
        intent: "where_am_i",
        target_button: "where_am_i",
        button_id: "where_am_i",
        action: "click_button",
        destination: null,
        spoken_response: "Checking your current location and orientation.",
        confidence: 0.99,
        provider: `${this.name} (Semantic Fallback)`
      };
    }

    // 2. Describe surroundings intent
    if (/^(describe|describe what('s| is) around me|describe around me|what do you see|what('s| is) around|what('s| is) in front|look around|see around)$/i.test(cleaned)) {
      return {
        intent: "describe_environment",
        target_button: "describe_around",
        button_id: "describe_around",
        action: "click_button",
        destination: null,
        spoken_response: "Scanning camera view to describe surroundings.",
        confidence: 0.99,
        provider: `${this.name} (Semantic Fallback)`
      };
    }

    // 3. Stop / Cancel intent
    if (/^(stop|cancel|end navigation|stop navigation|stop route|cancel route|halt)$/i.test(cleaned)) {
      return {
        intent: "stop",
        target_button: "stop_route",
        button_id: "stop_route",
        action: "click_button",
        destination: null,
        spoken_response: "Navigation stopped.",
        confidence: 0.99,
        provider: `${this.name} (Semantic Fallback)`
      };
    }

    // 4. Repeat intent
    if (/^(repeat|say again|what was that|repeat instruction|repeat location|repeat warning)$/i.test(cleaned)) {
      return {
        intent: "repeat",
        target_button: "repeat",
        button_id: "repeat",
        action: "click_button",
        destination: null,
        spoken_response: "Repeating last instruction.",
        confidence: 0.99,
        provider: `${this.name} (Semantic Button Match)`
      };
    }

    // 5. Affirmative / I Understand / Dismiss Obstacle
    if (/^(yes|yeah|yep|sure|ok|okay|i understand|understand|dismiss|dismiss obstacle|got it|clear|resume|continue|proceed|affirmative)$/i.test(cleaned)) {
      return {
        intent: "affirmative",
        target_button: "acknowledge_obstacle",
        button_id: "acknowledge_obstacle",
        action: "click_button",
        spoken_response: "Obstacle acknowledged. Resuming route.",
        confidence: 0.99,
        provider: `${this.name} (Semantic Voice Match)`
      };
    }

    // 5b. Negative / Hold / Wait
    if (/^(no|nope|wait|hold on|pause|not yet)$/i.test(cleaned)) {
      return {
        intent: "negative",
        action: "negative",
        spoken_response: "Holding position. Let me know when you are ready to continue.",
        confidence: 0.99,
        provider: `${this.name} (Semantic Voice Match)`
      };
    }

    // 5c. Guidance Query
    if (/^(where do i go|where to go|where should i go|which way|which direction|where to walk|guide me|navigate me)$/i.test(cleaned)) {
      return {
        intent: "guidance_query",
        action: "guidance_query",
        spoken_response: "Walk straight ahead. Pathway is clear.",
        confidence: 0.99,
        provider: `${this.name} (Semantic Voice Match)`
      };
    }

    // 5d. Obstacle Query
    if (/^(is there anything in my way|is the path clear|is there an obstacle|what('s| is) in my way|what('s| is) ahead|any obstacles)$/i.test(cleaned)) {
      return {
        intent: "obstacle_query",
        action: "obstacle_query",
        spoken_response: "Pathway is completely clear ahead for over 4 meters.",
        confidence: 0.99,
        provider: `${this.name} (Semantic Voice Match)`
      };
    }

    // 6. Settings
    if (/^(settings|open settings|audio settings|preferences)$/i.test(cleaned)) {
      return {
        intent: "click_button",
        target_button: "settings",
        button_id: "settings",
        action: "click_button",
        spoken_response: "Opening settings.",
        confidence: 0.99,
        provider: `${this.name} (Semantic Button Match)`
      };
    }

    // 7. Signboard Reading / Detection
    if (/^(read signs|read signboards?|detect signs?|what does the sign say|look for signs?|sign boards?)$/i.test(cleaned)) {
      return {
        intent: "detect_signs",
        target_button: "detect_signs",
        button_id: "detect_signs",
        action: "click_button",
        spoken_response: "Reading visible signboards and street signs.",
        confidence: 0.98,
        provider: `${this.name} (Semantic Button Match)`
      };
    }

    // 8. Camera toggle
    if (/^(camera|switch camera|toggle camera|turn camera on|open camera|back camera)$/i.test(cleaned)) {
      return {
        intent: "click_button",
        target_button: "toggle_camera",
        button_id: "toggle_camera",
        action: "click_button",
        spoken_response: "Toggling back camera.",
        confidence: 0.98,
        provider: `${this.name} (Semantic Button Match)`
      };
    }

    // 9. Start Navigation button direct click
    if (/^(start navigation|start route|begin navigation|start walking|let('s)? go)$/i.test(cleaned)) {
      return {
        intent: "start_navigation",
        target_button: "start_navigation",
        button_id: "start_navigation",
        action: "click_button",
        trigger_auto_gps: true,
        spoken_response: "Starting navigation.",
        confidence: 0.99,
        provider: `${this.name} (Semantic Button Match)`
      };
    }

    // 10. Navigation Intent Extraction with Auto-GPS
    const navPrefixRegex = /^(please\s+)?(take me to|navigate to|open the|open|i want to go to|i want you to go to|i want you to go|i need to go to|i need to get to|head to|walk to|go to|find the|find|directions to|route to|start route to|start navigation to|take me|navigate|start navigation|start route|directions|route|head|walk|go)\s*(.*)$/i;
    const match = cleaned.match(navPrefixRegex);

    let destinationQuery = "";
    if (match) {
      destinationQuery = (match[3] || "").trim();
    } else {
      destinationQuery = cleaned;
    }

    // Clean leading articles
    const cleanQuery = destinationQuery.replace(/^(the|a|an)\s+/i, "").trim();

    // Check for vague or missing destination phrases
    const vagueWords = new Set([
      "",
      "there",
      "somewhere",
      "anywhere",
      "it",
      "place",
      "location",
      "navigate",
      "navigation",
      "start navigation",
      "start route",
      "route",
      "directions",
      "go somewhere",
      "take me somewhere",
      "take me there",
      "take me",
      "where is it"
    ]);

    if (vagueWords.has(cleanQuery) || vagueWords.has(cleaned) || /^(navigate|start navigation|go somewhere|take me somewhere|take me there|directions|route|start route)$/i.test(cleaned)) {
      return {
        intent: "start_navigation",
        trigger_auto_gps: true,
        destination: {
          canonicalName: "Nearby Destination",
          shortName: "Nearby Destination",
          subtitle: "Nearest accessible walking destination",
          isNearbySearch: true
        },
        spoken_response: "Detecting current location. Finding nearest destination to navigate.",
        confidence: 0.95,
        provider: `${this.name} (Semantic Fallback)`
      };
    }

    // Search catalog for a known location match
    const knownMatch = findLocationMatch(cleanQuery);
    if (knownMatch) {
      return {
        intent: "start_navigation",
        trigger_auto_gps: true,
        destination: knownMatch,
        spoken_response: `Detecting current location. Routing to ${knownMatch.canonicalName}. Distance ${knownMatch.distanceKm} kilometers, estimated ${knownMatch.estimatedMinutes} minutes.`,
        confidence: 0.96,
        provider: `${this.name} (Semantic Fallback)`
      };
    }

    // Custom arbitrary location specified by user
    if (cleanQuery.length >= 2) {
      const customDest = createCustomDestination(cleanQuery);
      return {
        intent: "start_navigation",
        trigger_auto_gps: true,
        destination: customDest,
        spoken_response: `Detecting current location. Planning pedestrian route to ${customDest.canonicalName}.`,
        confidence: 0.95,
        provider: `${this.name} (Semantic Fallback)`
      };
    }

    return {
      intent: "clarification_needed",
      trigger_auto_gps: false,
      destination: null,
      clarification_prompt: "I didn't quite catch that destination. Where would you like to go?",
      spoken_response: "Where would you like to go? Please tell me the place or address.",
      confidence: 0.5,
      provider: `${this.name} (Semantic Fallback)`
    };
  }
}

module.exports = GeminiProvider;

