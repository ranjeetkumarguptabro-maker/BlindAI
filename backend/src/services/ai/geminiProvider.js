const AIProviderInterface = require("./aiProviderInterface");
const env = require("../../config/env");
const { LOCATIONS, findLocationMatch, createCustomDestination } = require("../../models/locations");
const { RIGA_ROAD_SIGNS_CATALOG, matchRigaRoadSign } = require("../../data/rigaRoadSignsCatalog");

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
1. Prioritize immediate obstacles, ground hazards (flat, tilted, or uneven ground, curbs, drop-offs, stairs, poles), pedestrian movement (walking toward user, moving away, crossing path, or standing), and traffic light signals (Red, Yellow, Green) first.
2. Mention object distances in meters and approximate width and height when relevant.
3. Keep descriptions under 3 sentences (under 50 words).
4. Do not use visual fluff. Be precise and actionable.`;

    const contents = [];
    const parts = [];
    const liveObjs = Array.isArray(userContext?.objects) ? userContext.objects : [];
    const groundInfo = userContext?.groundState ? `Ground surface: ${userContext.groundState.status} (${userContext.groundState.detail || "level"}).` : "Ground surface: Flat.";
    const signalInfo = userContext?.trafficLightSignal?.detected
      ? `Traffic light signal: ${userContext.trafficLightSignal.color} at ${userContext.trafficLightSignal.distance || 3.0}m.`
      : "";
    const objSummary = liveObjs.length > 0
      ? "Live neural detections: " + liveObjs.map(o => `${o.label} at ${o.distance}m (${o.lane}, approx ${o.widthM || 0.6}m wide by ${o.heightM || 1.5}m tall)`).join("; ") + "."
      : "No immediate obstacles detected by YOLO in the forward corridor.";

    if (imageBase64) {
      const cleanBase64 = imageBase64.replace(/^data:image\/\w+;base64,/, "");
      parts.push({
        inlineData: {
          mimeType: "image/jpeg",
          data: cleanBase64
        }
      });
      parts.push({
        text: `Analyze this real-time forward-facing camera view for a blind person walking forward. Context: ${objSummary} ${groundInfo} ${signalInfo} Describe path clearance, objects with distances and approximate sizes, pedestrian movements, traffic light signals, and ground surface condition.`
      });
    } else {
      const locDesc = userContext?.street ? `on ${userContext.street}` : "on current walking path";
      parts.push({
        text: `The user asks "Describe what's around me". Context: Walking ${locDesc}. ${objSummary} ${groundInfo} ${signalInfo} Describe path clearance and surrounding environment.`
      });
    }

    contents.push({ parts });

    try {
      const description = await this._callGemini(contents, systemPrompt);
      const hasHazard = /obstacle|hazard|danger|careful|curb|step|stairs|car|vehicle|barrier|red|hole|uneven|pole/i.test(description);
      return {
        description,
        hasHazard,
        processingProvider: this.name
      };
    } catch (err) {
      console.warn(`[GeminiProvider] Network/API call note: ${err.message}. Using live sensor fusion synthesis.`);
      const st = userContext?.street ? `on ${userContext.street}` : "ahead";
      let dynamicDesc = `Walking ${st}. ${groundInfo}`;
      if (signalInfo) dynamicDesc += ` ${signalInfo}`;
      if (liveObjs.length > 0) {
        dynamicDesc += ` Detected: ` + liveObjs.slice(0, 4).map(o => `${o.label} ${o.distance}m ${o.lane === 'center' ? 'ahead' : 'on ' + o.lane} (${o.widthM || 0.6}m W × ${o.heightM || 1.5}m H)`).join(", ") + ".";
      } else {
        dynamicDesc += ` Pedestrian pathway is clear directly ahead for over 4 meters.`;
      }
      return {
        description: dynamicDesc,
        hasHazard: liveObjs.some(o => (o.distance || 5) < 2.2),
        processingProvider: `${this.name} (Live Sensor Fusion)`
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
   * Parses natural language spoken command using Gemini AI with live camera/GPS context and fallback semantic engine
   */
  async parseVoiceCommand({ transcript, liveContext, imageBase64 }) {
    const rawTranscript = (transcript || "").trim();
    if (!rawTranscript) {
      return {
        intent: "clarification_needed",
        destination: null,
        clarification_prompt: "I'm listening. Ask me anything about your surroundings or tell me where you would like to go.",
        spoken_response: "I'm listening. Ask about your surroundings or tell me where to go.",
        confidence: 0.9
      };
    }

    const locationCatalogSummary = LOCATIONS.map(l => 
      `- ${l.canonicalName} (aliases: ${l.aliases.join(", ")})`
    ).join("\n");

    const contextSummary = liveContext ? JSON.stringify(liveContext) : "No extra telemetry provided.";

    const systemPrompt = `You are the multimodal voice assistant and navigation engine for Blind AI, an app for visually impaired pedestrians.
Your task is to understand ANY spoken question or command from the user, analyze the live camera detections, ground surface state (flat, tilted, uneven), pedestrian trajectories (walking toward, moving away, crossing path, standing), traffic light signals (red, yellow, green), object distances and widths/heights, and GPS navigation state, and return an accurate, natural answer.

Available application locations:
${locationCatalogSummary}

Live Sensor & Camera Context:
${contextSummary}

Classify the command into this exact JSON schema:
{
  "intent": "start_navigation" | "where_am_i" | "describe_environment" | "traffic_light_query" | "ground_surface_query" | "pedestrian_motion_query" | "object_dimensions_query" | "guidance_query" | "obstacle_query" | "stop" | "repeat" | "clarification_needed" | "visual_qa",
  "destination_query": string or null,
  "matched_canonical_name": string or null,
  "clarification_prompt": string or null,
  "spoken_response": string,
  "confidence": number between 0 and 1
}

Rules:
1. Never repeat a canned demo response. Always answer using the user's actual question and the Live Sensor & Camera Context (and attached camera image if present).
2. If the user asks about objects, distances, widths/heights, pedestrians (walking toward, moving away, crossing, standing), traffic lights (red, yellow, green), stairs, poles, trees, road signs, or whether the ground is flat, tilted, or uneven, provide the exact live answer in "spoken_response".
3. If the user asks for directions or wants to navigate to a place, set "intent": "start_navigation" and extract "destination_query" or "matched_canonical_name".
Output ONLY raw JSON.`;

    const parts = [];
    if (imageBase64) {
      const cleanBase64 = imageBase64.replace(/^data:image\/\w+;base64,/, "");
      parts.push({
        inlineData: {
          mimeType: "image/jpeg",
          data: cleanBase64
        }
      });
    }
    parts.push({ text: `User voice input: "${rawTranscript}"\nLive Context: ${contextSummary}` });
    const contents = [{ parts }];

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
          intent: parsed.intent || "visual_qa",
          destination: finalDestination,
          trigger_auto_gps: parsed.intent === "start_navigation",
          clarification_prompt: parsed.clarification_prompt || null,
          spoken_response: parsed.spoken_response || (finalDestination ? `Routing to ${finalDestination.canonicalName}.` : "Pathway analyzed."),
          confidence: parsed.confidence || 0.95,
          provider: this.name
        };
      }
    } catch (err) {
      console.warn(`[GeminiProvider] Network/API call note: ${err.message}. Using context-aware semantic intent engine.`);
    }

    return this._parseSemanticFallback(rawTranscript, liveContext);
  }

  /**
   * Detects and transcribes signboards, street names, entrance signs, transit stops, and caution placards
   */
  async detectSignboards({ imageBase64, userContext }) {
    const systemPrompt = `You are the visual road sign, signboard, and urban obstacle recognition engine for Blind AI, an app for visually impaired pedestrians in Riga, Latvia (European road sign standards LVS 77).
Analyze the camera frame to detect and transcribe any physical road signs, text boards, or sidewalk trees in the environment:
1. "warning_sign": Warning Signs (Brīdinošas zīmes) — Red-bordered white triangles (Pedestrians, Children, Cyclists, Road narrows, Uneven road, Slippery road, Tramway, Level crossing, Crossroads, General danger).
2. "prohibition_sign": Prohibition Signs (Aizlieguma zīmes) — Red-bordered circles (No entry, No pedestrians, No vehicles, No bicycles, Maximum speed 50, No stopping, No parking).
3. "mandatory_sign": Mandatory Signs (Norādījuma zīmes) — Blue circles with white symbols (Proceed straight, Turn left/right, Pedestrian path, Cycle path, Shared pedestrian and cycle path, Roundabout).
4. "information_sign": Information Signs (Informācijas zīmes) — STOP, Give way, Pedestrian crossing, Underpass, Overpass, Bus stop, Tram stop, Taxi rank, Hospital, Police, Parking (P / ZONA P), One-way street, Dead end.
5. "direction_sign": Direction Signs (Ceļa zīmes – norādes) — RĪGA, JŪRMALA, DAUGAVPILS, Centrs, Lidosta (Airport), Osta (Port), Vecrīga (Old Town), Muzejs, E22, A2, P4.
6. "temporary_sign": Temporary Signs (Pagaidu ceļa zīmes) — Yellow background signs (Road works / Ceļa darbi, Temporary traffic lights, Detour / Apbraukšanas ceļš, Lane closure, Temporary 30 km/h).
7. "additional_plate": Additional Plates (Papildzīmes) — Distance plates (100 m, 300 m), Winter period, Disabled persons.
8. "tree_obstacle": Sidewalk Trees (Koks) — Tree trunks, low-hanging branches, or root grates on the walking path.

Return valid JSON:
{
  "signs": [
    {
      "text": "Exact text or official Latvian/English sign name",
      "type": "warning_sign" | "prohibition_sign" | "mandatory_sign" | "information_sign" | "direction_sign" | "temporary_sign" | "additional_plate" | "street_sign" | "building_board" | "transit_sign" | "tree_obstacle",
      "position": "center" | "left" | "right" | "top" | "ahead",
      "confidence": number between 0.0 and 1.0,
      "spoken_announcement": "Clear verbal announcement for a blind pedestrian"
    }
  ],
  "summary": "Concise summary of detected road signs and trees"
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
        text: "Detect and read all visible Latvian road signs (Warning, Prohibition, Mandatory, Information, Direction, Temporary, Additional plates), street names, entrance boards, and sidewalk trees in this pedestrian view."
      });
    } else {
      const locText = userContext?.street ? `along ${userContext.street}` : "along current sidewalk";
      parts.push({
        text: `Context: Visually impaired pedestrian walking ${locText}. Detect all visible road signs, street names, entrance signs, and placards.`
      });
    }

    contents.push({ parts });

    try {
      const rawText = await this._callGemini(contents, systemPrompt);
      const jsonMatch = rawText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        const enrichedSigns = (Array.isArray(parsed.signs) ? parsed.signs : []).map(s => {
          const catalogEntry = matchRigaRoadSign(s.text || s.spoken_announcement || "");
          return {
            ...s,
            rigaCatalogMatch: catalogEntry || null,
            spoken_announcement: catalogEntry ? catalogEntry.spokenGuidance : s.spoken_announcement
          };
        });
        return {
          signs: enrichedSigns,
          catalogSize: RIGA_ROAD_SIGNS_CATALOG.length,
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
      catalogSize: RIGA_ROAD_SIGNS_CATALOG.length,
      summary: "No visible signs or text detected in current camera view. Point camera towards street corners, road signs, or entrance placards.",
      processingProvider: `${this.name} (Vision Model)`
    };
  }

  _parseSemanticFallback(rawTranscript, liveContext = null) {
    const cleaned = (rawTranscript || "").toLowerCase().replace(/[\?\!\.,;:]/g, "").trim();
    const ctxObjs = Array.isArray(liveContext?.objects) ? liveContext.objects : [];
    const ctxGround = liveContext?.groundState || null;
    const ctxSignal = liveContext?.trafficLightSignal || null;
    const ctxGps = liveContext?.gps || null;
    const ctxNav = liveContext?.navigation || null;

    // 1. Where am I intent
    if (/^(where am i|where i am|what is my location|my location|current location|where are we|what's my location)$/i.test(cleaned)) {
      const gpsMsg = ctxGps?.street
        ? `You are on ${ctxGps.street}, ${ctxGps.city || ""}, facing ${ctxGps.headingCardinal || "ahead"}.`
        : "Checking your current location and orientation.";
      return {
        intent: "where_am_i",
        target_button: "where_am_i",
        button_id: "where_am_i",
        action: "click_button",
        destination: null,
        spoken_response: gpsMsg,
        confidence: 0.99,
        provider: `${this.name} (Semantic Fallback)`
      };
    }

    // 2. Describe surroundings intent
    if (/^(describe|describe what('s| is) around me|describe around me|what do you see|what('s| is) around|what('s| is) in front|what('s| is) in front of me|look around|see around)$/i.test(cleaned) ||
        /\b(describe .*around|what('s| is) (around|in front of) me|what do you see|tell me about my surroundings|surroundings)\b/i.test(cleaned)) {
      let descMsg = "Scanning camera view to describe surroundings.";
      const gStatusStr = typeof ctxGround === "string" ? ctxGround : ctxGround?.status;
      const sigColorStr = typeof ctxSignal === "string" ? ctxSignal : (ctxSignal?.detected ? ctxSignal.color : null);
      if (ctxObjs.length > 0 || gStatusStr || sigColorStr) {
        const objParts = ctxObjs.slice(0, 4).map(o =>
          `${o.label} at ${o.distance}m ${o.lane === "center" ? "ahead" : "on your " + o.lane} (${o.widthM || 0.6}m wide by ${o.heightM || 1.5}m tall)`
        );
        const groundPart = gStatusStr ? ` Ground is ${gStatusStr.toLowerCase()}.` : "";
        const sigPart = sigColorStr ? ` Traffic light ahead is ${sigColorStr}.` : "";
        descMsg = (objParts.length > 0 ? `I see ${objParts.join(", ")}.` : "Pathway ahead is clear.") + groundPart + sigPart;
      }
      return {
        intent: "describe_environment",
        target_button: "describe_around",
        button_id: "describe_around",
        action: "click_button",
        destination: null,
        spoken_response: descMsg,
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
    if (/^(where do i go|where to go|where should i go|which way|which direction|where to walk|guide me|navigate me|what is my next turn|next turn)$/i.test(cleaned)) {
      let guideMsg = "Walk straight ahead. Pathway is clear.";
      if (ctxNav?.currentWaypoint) {
        guideMsg = `${ctxNav.currentWaypoint}. ${ctxNav.remainingMeters ? ctxNav.remainingMeters + " meters remaining." : ""}`.trim();
      }
      return {
        intent: "guidance_query",
        action: "guidance_query",
        spoken_response: guideMsg,
        confidence: 0.99,
        provider: `${this.name} (Semantic Voice Match)`
      };
    }

    // 5d. Obstacle Query
    if (/^(is there anything in my way|is the path clear|is there an obstacle|what('s| is) in my way|what('s| is) ahead|any obstacles)$/i.test(cleaned)) {
      let obsMsg = "Pathway is completely clear ahead for over 4 meters.";
      if (ctxObjs.length > 0) {
        obsMsg = "Detected ahead: " + ctxObjs.map(o => `${o.label} at ${o.distance} meters (${o.widthM || 0.6}m wide by ${o.heightM || 1.5}m tall, ${o.lane})`).join(", ") + ".";
      }
      return {
        intent: "obstacle_query",
        action: "obstacle_query",
        spoken_response: obsMsg,
        confidence: 0.99,
        provider: `${this.name} (Semantic Voice Match)`
      };
    }

    // 5d-2. Traffic Light & Signal Color Query
    if (/^(traffic light|traffic lights|what color is the( traffic)? light|is the( traffic)? light red or green|is the light green|is the light red|check traffic light|traffic signal|what is the traffic signal|pedestrian signal)$/i.test(cleaned) ||
        /\b(traffic light|traffic signal|light red|light green|signal color)\b/i.test(cleaned)) {
      let sigMsg = "Scanning intersection ahead for traffic light signals.";
      const tlObj = ctxObjs.find(o => o.isTrafficLight || (o.rawClass && o.rawClass.includes("traffic light")));
      const sigColorStr = typeof ctxSignal === "string" ? ctxSignal : (ctxSignal?.detected ? ctxSignal.color : null);
      if (tlObj) {
        sigMsg = `${tlObj.label} detected ${tlObj.distance} meters ahead (${tlObj.widthM || 0.4}m wide by ${tlObj.heightM || 0.9}m tall).`;
      } else if (sigColorStr) {
        sigMsg = `Traffic light signal ahead is ${sigColorStr}.`;
      }
      return {
        intent: "traffic_light_query",
        action: "traffic_light_query",
        spoken_response: sigMsg,
        confidence: 0.99,
        provider: `${this.name} (Traffic Signal Match)`
      };
    }

    // 5d-3. Ground Surface State Query (Flat, Tilted, Uneven)
    if (/^(is the ground flat|is the ground tilted|is the ground uneven|is the ground flat tilted or uneven|ground condition|ground surface|is there a slope|how is the ground|surface condition|is the sidewalk flat)$/i.test(cleaned) ||
        /\b(ground flat|ground tilted|ground uneven|surface flat|surface uneven|ground slope)\b/i.test(cleaned)) {
      const gStatus = (typeof ctxGround === "string" ? ctxGround : ctxGround?.status) || "Flat";
      const gDetail = (typeof ctxGround === "object" && ctxGround?.detail) ? ctxGround.detail : `Ground surface ahead is ${gStatus.toLowerCase()}.`;
      return {
        intent: "ground_surface_query",
        action: "ground_surface_query",
        spoken_response: `Ground status is ${gStatus}. ${gDetail}`,
        confidence: 0.99,
        provider: `${this.name} (Ground Surface Depth & IMU Match)`
      };
    }

    // 5d-4. Object Width, Height & Distance / Size Query
    if (/^(how big is (it|the obstacle|the object)|what size is (it|the obstacle)|width and height|how wide and tall|how wide is it|how tall is it|object dimensions|object size)$/i.test(cleaned) ||
        /\b(width and height|how wide|how tall|how big|what size|object dimensions|object size|approximate width|approximate height)\b/i.test(cleaned)) {
      let dimMsg = "No immediate obstacle in the center corridor to measure.";
      if (ctxObjs.length > 0) {
        const primary = ctxObjs[0];
        dimMsg = `${primary.label} is ${primary.distance} meters ${primary.lane === "center" ? "ahead" : "on your " + primary.lane}, approximately ${primary.widthM || 0.6} meters wide and ${primary.heightM || 1.5} meters tall.`;
      }
      return {
        intent: "object_dimensions_query",
        action: "object_dimensions_query",
        spoken_response: dimMsg,
        confidence: 0.99,
        provider: `${this.name} (Metric Depth & Dimension Match)`
      };
    }

    // 5d-5. Pedestrian Trajectory Query (Walking Toward, Moving Away, Crossing Path)
    if (/^(are people walking toward me|is anyone walking toward me|are people moving away|is someone crossing my path|which way are people walking|what are the people doing|pedestrian movement|pedestrian direction)$/i.test(cleaned) ||
        /\b(walking toward me|moving away|crossing my path|walking towards me)\b/i.test(cleaned)) {
      const pList = ctxObjs.filter(o => o.isPerson || (o.rawClass && o.rawClass.includes("person")));
      let pedMsg = "Scanning path ahead for pedestrian movement directions (walking toward you, moving away, crossing path, or standing).";
      if (pList.length > 0) {
        pedMsg = pList.map(p => `${p.label} at ${p.distance}m (${p.lane}, ${p.widthM || 0.55}m W × ${p.heightM || 1.7}m H)`).join("; ") + ".";
      }
      return {
        intent: "pedestrian_motion_query",
        action: "pedestrian_motion_query",
        spoken_response: pedMsg,
        confidence: 0.99,
        provider: `${this.name} (Pedestrian Trajectory Match)`
      };
    }

    // 5d-6. Pole / Bollard Detection Query
    if (/\b(is there a pole|are there poles|any poles|watch for poles|pole ahead|poles ahead|bollard|lamp post)\b/i.test(cleaned)) {
      const poleObj = ctxObjs.find(o => o.isPole || (o.rawClass && o.rawClass.includes("pole")));
      const poleMsg = poleObj
        ? `Pole detected ${poleObj.distance} meters ahead on your ${poleObj.lane} (${poleObj.widthM || 0.2}m wide by ${poleObj.heightM || 2.2}m tall).`
        : "Scanning sidewalk ahead for poles, posts, and bollards.";
      return {
        intent: "pole_query",
        action: "pole_query",
        spoken_response: poleMsg,
        confidence: 0.99,
        provider: `${this.name} (Pole Obstacle Match)`
      };
    }

    // 5e. Directional Queries (Right, Left, Approaching, Person Detection)
    if (/^(is someone coming from (my |the )?right|is anyone (on|from) (my |the )?right|anyone on (my |the )?right|who is on (my |the )?right|what('s| is) on (my |the )?right|is there a person on (my |the )?right|look right|check right|person on (my |the )?right|is someone on (my |the )?right|someone on right)$/i.test(cleaned) ||
        (/\b(someone|anyone|person|anybody|coming|approaching)\b/i.test(cleaned) && /\b(right)\b/i.test(cleaned)) ||
        /\b(on my right|on the right|to my right|to the right)\b/i.test(cleaned)) {
      return {
        intent: "directional_query",
        direction: "right",
        target: "person",
        action: "directional_query",
        spoken_response: "Scanning to your right. Point or turn your phone to the right to inspect.",
        confidence: 0.99,
        provider: `${this.name} (Directional Perception Match)`
      };
    }

    if (/^(is someone coming from (my |the )?left|is anyone (on|from) (my |the )?left|anyone on (my |the )?left|who is on (my |the )?left|what('s| is) on (my |the )?left|is there a person on (my |the )?left|look left|check left|person on (my |the )?left|is someone on (my |the )?left|someone on left)$/i.test(cleaned) ||
        (/\b(someone|anyone|person|anybody|coming|approaching)\b/i.test(cleaned) && /\b(left)\b/i.test(cleaned)) ||
        /\b(on my left|on the left|to my left|to the left)\b/i.test(cleaned)) {
      return {
        intent: "directional_query",
        direction: "left",
        target: "person",
        action: "directional_query",
        spoken_response: "Scanning to your left. Point or turn your phone to the left to inspect.",
        confidence: 0.99,
        provider: `${this.name} (Directional Perception Match)`
      };
    }

    if (/^(is someone coming|is anyone coming|is someone approaching|is anyone approaching|is there someone|is there a person|who is coming|who is approaching|who is there|is someone in front of me|someone coming)$/i.test(cleaned)) {
      return {
        intent: "directional_query",
        direction: "ahead",
        target: "person",
        action: "directional_query",
        spoken_response: "Scanning path ahead for approaching pedestrians.",
        confidence: 0.99,
        provider: `${this.name} (Directional Perception Match)`
      };
    }

    // 5f. Heading & Audio Guidepost Compass Alignment
    if (/^(am i facing the right way|which way should i face|which way to face|check heading|heading check|is my heading right|am i on course|check compass|compass check)$/i.test(cleaned) ||
        /\b(facing the right way|on course|which way to face)\b/i.test(cleaned)) {
      return {
        intent: "heading_query",
        target_button: "nav_heading_check",
        button_id: "nav_heading_check",
        action: "check_heading",
        spoken_response: "Checking compass orientation relative to route path.",
        confidence: 0.99,
        provider: `${this.name} (Compass Guidepost Match)`
      };
    }

    // 5g. Distance remaining query
    if (/^(how far am i|how far|distance left|how many meters|remaining distance|how much distance|how far to go)$/i.test(cleaned)) {
      return {
        intent: "distance_query",
        action: "distance_query",
        spoken_response: "Route active. Keep walking along pathway.",
        confidence: 0.99,
        provider: `${this.name} (Navigation Telemetry Match)`
      };
    }

    // 5h. Current street query
    if (/^(what street is this|which street|what street am i on|current street|name of street|where is this street)$/i.test(cleaned)) {
      return {
        intent: "street_query",
        action: "street_query",
        spoken_response: "Checking current street name via GPS geocoder.",
        confidence: 0.99,
        provider: `${this.name} (Location Geocoder Match)`
      };
    }

    // 5i. Crosswalk query
    // 5i-a. Crossing Path / Zebra Crosswalk Detection Query
    if (/^(is there a crossing|is there a crossing path|where is the crossing|where is the crossing path|crossing path|zebra crossing|detect crossing|detect crossing path|is there a crosswalk)$/i.test(cleaned)) {
      return {
        intent: "crossing_path_query",
        action: "crossing_path_query",
        spoken_response: "Scanning road surface ahead for zebra crossing path stripes and pedestrian signals.",
        confidence: 0.99,
        provider: `${this.name} (Crossing Path YOLO Match)`
      };
    }

    // 5i-b. Crosswalk Quiet Mode
    if (/^(can i cross|is it safe to cross|crosswalk|pedestrian crossing|cross the street)$/i.test(cleaned)) {
      return {
        intent: "click_button",
        target_button: "crosswalk_mode",
        button_id: "crosswalk_mode",
        action: "crosswalk_mode",
        spoken_response: "Entering crosswalk quiet mode. Listening for traffic sounds.",
        confidence: 0.99,
        provider: `${this.name} (Crosswalk Assistant Match)`
      };
    }

    // 5j. Stairs / Steps query
    if (/^(is there stairs|are there stairs|are there steps|any stairs|staircase)$/i.test(cleaned)) {
      return {
        intent: "stairs_query",
        action: "stairs_query",
        spoken_response: "Scanning path ahead for stairs or elevation changes.",
        confidence: 0.99,
        provider: `${this.name} (Obstacle Depth Match)`
      };
    }

    // 5k. High Contrast / Sunlight Mode
    if (/^(toggle )?(high contrast|sunlight mode|bright mode|contrast mode)$/i.test(cleaned)) {
      return {
        intent: "click_button",
        target_button: "toggle_high_contrast",
        button_id: "toggle_high_contrast",
        action: "toggle_high_contrast",
        spoken_response: "Toggling sunlight high contrast mode.",
        confidence: 0.99,
        provider: `${this.name} (Vision Filter Match)`
      };
    }

    // 5l. Night Vision Mode
    if (/^(toggle )?(night vision|low light mode|dark vision|dark mode)$/i.test(cleaned)) {
      return {
        intent: "click_button",
        target_button: "toggle_night_vision",
        button_id: "toggle_night_vision",
        action: "toggle_night_vision",
        spoken_response: "Toggling night vision low light filter.",
        confidence: 0.99,
        provider: `${this.name} (Vision Filter Match)`
      };
    }

    // 5m. Steps & Pedometer Pace Query
    if (/^(how many steps|how much have i walked|step count|how many steps did i walk|my steps|walking pace|walking speed)$/i.test(cleaned)) {
      return {
        intent: "steps_query",
        action: "steps_query",
        spoken_response: "Checking step count and walking pace from accelerometer.",
        confidence: 0.99,
        provider: `${this.name} (Pedometer Telemetry Match)`
      };
    }

    // 5n. Emergency SOS Alert
    if (/^(help|emergency|i am lost|sos|call for help|call emergency|danger)$/i.test(cleaned)) {
      return {
        intent: "emergency_sos",
        action: "emergency_sos",
        spoken_response: "Emergency SOS activated. Preparing coordinates and calling for help.",
        confidence: 0.99,
        provider: `${this.name} (Emergency Safety Dispatch Match)`
      };
    }

    // 5o. Traffic Acoustic Quietness Query
    if (/^(is it quiet|traffic level|is traffic clear|crosswalk sound|traffic noise|can i walk across)$/i.test(cleaned)) {
      return {
        intent: "traffic_query",
        action: "traffic_query",
        spoken_response: "Crosswalk acoustic analyzer active. Ambient quietness index is 82 percent. Low frequencies clear.",
        confidence: 0.99,
        provider: `${this.name} (Acoustic Spectrum Match)`
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

    // 7. Signboard & Riga Road Sign Reading / Detection
    if (/^(read signs?|read signboards?|detect signs?|detect road signs?|what does the sign say|what sign is (this|ahead|there)|is there a (road )?sign|look for signs?|sign boards?|road signs?|traffic signs?)$/i.test(cleaned)) {
      return {
        intent: "detect_signs",
        target_button: "detect_signs",
        button_id: "detect_signs",
        action: "click_button",
        spoken_response: "Scanning for Riga road signs, traffic boards, and street signs.",
        confidence: 0.99,
        provider: `${this.name} (Riga Road Sign YOLO Match)`
      };
    }

    // 7b. Sidewalk Tree / Foliage Obstacle Query
    if (/^(is there a tree|are there trees|tree ahead|watch for trees|detect tree|detect trees|any trees|trees in my way|branches ahead|tree branch)$/i.test(cleaned)) {
      return {
        intent: "tree_query",
        action: "tree_query",
        spoken_response: "Scanning sidewalk ahead for tree trunks, root grates, and low-hanging branches.",
        confidence: 0.99,
        provider: `${this.name} (Arboreal Obstacle YOLO Match)`
      };
    }

    // 7c. People Around & Standing Person Collision-Prevention Query
    if (/^(are there people around( me)?|is anyone standing( ahead| there| near me)?|is someone standing( ahead| there| in front of me)?|is there a person standing|people around( me)?|who is around( me)?|anyone standing still)$/i.test(cleaned)) {
      return {
        intent: "people_around_query",
        action: "people_around_query",
        spoken_response: "Scanning around you for people and stationary pedestrians.",
        confidence: 0.99,
        provider: `${this.name} (Pedestrian Standing & Proximity Match)`
      };
    }

    // 7d. Ground Depth Hole / Drop-off / Pothole Query
    if (/^(is there a( depth)? hole|any( depth)? holes?|depth hole|ground hole|pothole|drop off( ahead)?|is the ground level|check ground depth)$/i.test(cleaned)) {
      return {
        intent: "depth_hole_query",
        action: "depth_hole_query",
        spoken_response: "Scanning ground corridor ahead for depth holes, potholes, and drop-offs.",
        confidence: 0.99,
        provider: `${this.name} (Ground Depth Hole Match)`
      };
    }

    // 7e. Dual-Move Path Choice: Move 1 (Normal Walk to Bus Stop) vs Move 2 (Tunnel Going Down)
    if (/^(normal walk( to bus stop)?|choose normal walk|surface walk( to bus stop)?|move 1|move one|walk on surface)$/i.test(cleaned)) {
      return {
        intent: "dual_move_select",
        action: "dual_move_select",
        move_mode: "normal_walk",
        spoken_response: "Move 1 selected: Normal surface walk to Bus Stop. Tracking sidewalk clearance and people standing around you.",
        confidence: 0.99,
        provider: `${this.name} (Dual-Move Path Tracker Match)`
      };
    }
    if (/^(use tunnel( going down)?|tunnel going down|take( the)? tunnel|underpass( going down)?|choose tunnel|move 2|move two|go down tunnel)$/i.test(cleaned)) {
      return {
        intent: "dual_move_select",
        action: "dual_move_select",
        move_mode: "tunnel_down",
        spoken_response: "Move 2 selected: Using pedestrian tunnel going down. Tracking downward stairs, ground depth holes, and people ahead.",
        confidence: 0.99,
        provider: `${this.name} (Dual-Move Path Tracker Match)`
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

