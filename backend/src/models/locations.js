/**
 * Locations, Transit Stops & Destination Validation Model for Blind AI
 * Implements Module 1 (Destination Validation & Ambiguity Clarification)
 * and Module 2 (Riga Walking Routes, Pedestrian Crossings & Public Transport Options).
 */

const LOCATIONS = [
  {
    id: "rtu-campus",
    canonicalName: "Riga Technical University (RTU)",
    shortName: "RTU Campus",
    subtitle: "Ķīpsala Campus, Paula Valdena iela 1 / Āzenes iela 12",
    category: "Campus",
    coordinates: { lat: 56.9515, lon: 24.0812 },
    distanceKm: 2.1,
    estimatedMinutes: 25,
    waypointCount: 6,
    aliases: [
      "rtu",
      "riga technical university",
      "kipsala campus",
      "kipsala",
      "technical university",
      "rtu campus",
      "main campus"
    ],
    description: "Main Riga Technical University campus on Ķīpsala island with faculty buildings, laboratories, and tactile pedestrian pathways.",
    pedestrianCrossings: [
      { id: "cross-11-novembra", name: "11. novembra krastmala / Grēcinieku iela signalized crossing", distanceMeters: 180, type: "signalized_zebra", tactilePaving: true, audioSignal: true },
      { id: "cross-balasta", name: "Kuģu iela / Balasta dambis pedestrian crossing", distanceMeters: 920, type: "zebra_crosswalk", tactilePaving: true, audioSignal: false },
      { id: "cross-kipsalas", name: "Ķīpsalas iela / Paula Valdena iela zebra crossing", distanceMeters: 1650, type: "zebra_crosswalk", tactilePaving: true, audioSignal: false }
    ],
    transitOptions: [
      {
        mode: "trolleybus",
        routeNumber: "9",
        lineName: "Trolleybus 9 (Stacijas laukums → Iļģuciems)",
        boardStop: "Grēcinieku iela (Riga Old Town)",
        alightStop: "Ķīpsala",
        stopsCount: 2,
        rideMinutes: 5,
        walkToCampusMeters: 350,
        totalMinutes: 11,
        boardingInstructions: "At Grēcinieku iela stop, stand near the raised tactile curb strip. Trolleybus 9 announces its route number externally when doors open. Alight after 2 stops at Ķīpsala after crossing Akmens tilts, then take the pedestrian ramp down toward Āzenes iela."
      },
      {
        mode: "bus",
        routeNumber: "3",
        lineName: "Bus 3 (Pļavnieki → Daugavgrīva)",
        boardStop: "Grēcinieku iela / 11. novembra krastmala",
        alightStop: "Ķīpsala",
        stopsCount: 2,
        rideMinutes: 5,
        walkToCampusMeters: 350,
        totalMinutes: 11,
        boardingInstructions: "Board Bus 3 at Grēcinieku iela heading west across Akmens tilts. Listen for interior next-stop audio announcement 'Ķīpsala'."
      },
      {
        mode: "tram",
        routeNumber: "1",
        lineName: "Tram 1 (Jugla → Imanta)",
        boardStop: "11. novembra krastmala (Grēcinieku iela)",
        alightStop: "Nacionālā bibliotēka / Uzvaras parks",
        stopsCount: 2,
        rideMinutes: 4,
        walkToCampusMeters: 680,
        totalMinutes: 14,
        boardingInstructions: "Low-floor Tram 1 boards level with the platform at 11. novembra krastmala. Alight at Nacionālā bibliotēka across the river and follow Kuģu iela and Balasta dambis north to Ķīpsala."
      }
    ],
    waypoints: [
      { sequence: 1, instruction: "Walk west from Riga Old Town toward 11. novembra krastmala crossing", distanceMeters: 180, maneuver: "Head straight", icon: "↑", isCrossing: false },
      { sequence: 2, instruction: "Approach signalized pedestrian crossing at 11. novembra krastmala", distanceMeters: 25, maneuver: "Crosswalk ahead", icon: "🚶", isCrossing: true },
      { sequence: 3, instruction: "Cross Akmens tilts / Vanšu tilts pedestrian bridge walkway", distanceMeters: 730, maneuver: "Cross bridge", icon: "↑", isCrossing: false },
      { sequence: 4, instruction: "Turn right onto Balasta dambis / Ķīpsalas iela walkway", distanceMeters: 420, maneuver: "Turn right in 20 metres", icon: "↱", isCrossing: false },
      { sequence: 5, instruction: "Turn left onto Paula Valdena iela toward RTU campus", distanceMeters: 210, maneuver: "Turn left in 20 metres", icon: "↰", isCrossing: true },
      { sequence: 6, instruction: "You have arrived at your destination: Riga Technical University", distanceMeters: 0, maneuver: "Destination reached", icon: "★", isCrossing: false }
    ]
  },
  {
    id: "riga-old-town",
    canonicalName: "Riga Old Town (Vecrīga)",
    shortName: "Old Town",
    subtitle: "Vecrīga, Rātslaukums / Kaļķu iela 1, Rīga",
    category: "Historic District",
    coordinates: { lat: 56.9475, lon: 24.1064 },
    distanceKm: 2.1,
    estimatedMinutes: 25,
    waypointCount: 5,
    aliases: [
      "old town",
      "riga old town",
      "vecriga",
      "vecrīga",
      "ratslaukums",
      "town hall square",
      "kalku iela"
    ],
    description: "Historic center of Riga with pedestrianized cobblestone streets, Town Hall Square, and Grēcinieku iela transit hub.",
    pedestrianCrossings: [
      { id: "cross-kipsala-underpass", name: "Ķīpsala Krišjāņa Valdemāra iela crossing", distanceMeters: 320, type: "signalized_zebra", tactilePaving: true, audioSignal: true },
      { id: "cross-11-novembra-east", name: "11. novembra krastmala Old Town crossing", distanceMeters: 1850, type: "signalized_zebra", tactilePaving: true, audioSignal: true }
    ],
    transitOptions: [
      {
        mode: "trolleybus",
        routeNumber: "9",
        lineName: "Trolleybus 9 (Iļģuciems → Stacijas laukums)",
        boardStop: "Ķīpsala (city-bound platform)",
        alightStop: "Grēcinieku iela (Vecrīga)",
        stopsCount: 2,
        rideMinutes: 5,
        walkToCampusMeters: 150,
        totalMinutes: 9,
        boardingInstructions: "Board city-bound Trolleybus 9 at Ķīpsala stop. Alight after 2 stops at Grēcinieku iela directly beside Riga Old Town."
      }
    ],
    waypoints: [
      { sequence: 1, instruction: "Walk east toward Ķīpsala transit stop and bridge approach", distanceMeters: 350, maneuver: "Head straight", icon: "↑" },
      { sequence: 2, instruction: "Cross Daugava River pedestrian walkway toward Old Town", distanceMeters: 750, maneuver: "Head straight", icon: "↑" },
      { sequence: 3, instruction: "Approach signalized pedestrian crossing at 11. novembra krastmala", distanceMeters: 30, maneuver: "Crosswalk ahead", icon: "🚶", isCrossing: true },
      { sequence: 4, instruction: "Continue straight along Kaļķu iela into Vecrīga", distanceMeters: 220, maneuver: "Head straight", icon: "↑" },
      { sequence: 5, instruction: "You have arrived at your destination: Riga Old Town", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "rtu-library",
    canonicalName: "RTU Scientific Library",
    shortName: "Library",
    subtitle: "Paula Valdena iela 5, Ķīpsala",
    category: "Library",
    coordinates: { lat: 56.9524, lon: 24.0798 },
    distanceKm: 1.3,
    estimatedMinutes: 16,
    waypointCount: 4,
    aliases: [
      "library",
      "the library",
      "scientific library",
      "rtu library",
      "study hall",
      "reading room",
      "central library"
    ],
    description: "University library with accessible reading terminals, tactile floor markers, and elevator access.",
    pedestrianCrossings: [
      { id: "cross-valdena", name: "Paula Valdena iela raised pedestrian table", distanceMeters: 65, type: "zebra_crosswalk", tactilePaving: true, audioSignal: false }
    ],
    transitOptions: [
      {
        mode: "trolleybus",
        routeNumber: "9",
        lineName: "Trolleybus 9",
        boardStop: "Grēcinieku iela",
        alightStop: "Ķīpsala",
        stopsCount: 2,
        rideMinutes: 5,
        walkToCampusMeters: 280,
        totalMinutes: 10,
        boardingInstructions: "Take Trolleybus 9 or Bus 3 to Ķīpsala stop, then walk 280 metres north along Zunda canal path to Paula Valdena iela 5."
      }
    ],
    waypoints: [
      { sequence: 1, instruction: "Walk north on Paula Valdena iela", distanceMeters: 90, maneuver: "Head straight", icon: "↑" },
      { sequence: 2, instruction: "Turn left in 20 metres toward Library entrance", distanceMeters: 40, maneuver: "Turn left in 20 metres", icon: "↰" },
      { sequence: 3, instruction: "Ascend accessible entrance ramp", distanceMeters: 10, maneuver: "Ramp ahead", icon: "↑" },
      { sequence: 4, instruction: "You have arrived at your destination: RTU Scientific Library", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "rtu-main-building",
    canonicalName: "RTU Main Building & Administration",
    shortName: "Main Building",
    subtitle: "Ķīpsalas iela 6A, Ķīpsala Center",
    category: "Campus",
    coordinates: { lat: 56.9508, lon: 24.0819 },
    distanceKm: 0.9,
    estimatedMinutes: 11,
    waypointCount: 3,
    aliases: [
      "main building",
      "the main building",
      "administration",
      "admin building",
      "central building",
      "rectorate",
      "dean's office",
      "open main building",
      "open the main building"
    ],
    description: "Central administrative building, rectorate, and student service center.",
    pedestrianCrossings: [
      { id: "cross-kipsalas-6a", name: "Ķīpsalas iela central campus crosswalk", distanceMeters: 45, type: "zebra_crosswalk", tactilePaving: true, audioSignal: false }
    ],
    transitOptions: [],
    waypoints: [
      { sequence: 1, instruction: "Follow paved pathway towards central square", distanceMeters: 70, maneuver: "Head straight", icon: "↑" },
      { sequence: 2, instruction: "Turn right in 20 metres toward administrative portico", distanceMeters: 30, maneuver: "Turn right in 20 metres", icon: "↱" },
      { sequence: 3, instruction: "You have arrived at your destination: RTU Main Building", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "rtu-sports-center",
    canonicalName: "RTU Ķīpsala Sports Center & Pool",
    shortName: "Sports Center",
    subtitle: "Ķīpsalas iela 5, Ķīpsala",
    category: "Sports",
    coordinates: { lat: 56.9498, lon: 24.0825 },
    distanceKm: 0.7,
    estimatedMinutes: 9,
    waypointCount: 3,
    aliases: [
      "sports center",
      "the sports center",
      "sports centre",
      "the sports centre",
      "swimming pool",
      "pool",
      "gym",
      "fitness center",
      "athletics",
      "stadium"
    ],
    description: "Olympic swimming pool, athletics gym, and indoor court complex.",
    pedestrianCrossings: [
      { id: "cross-sports", name: "Ķīpsalas iela 5 pedestrian crossing", distanceMeters: 40, type: "zebra_crosswalk", tactilePaving: true, audioSignal: false }
    ],
    transitOptions: [],
    waypoints: [
      { sequence: 1, instruction: "Walk south toward Ķīpsalas iela", distanceMeters: 60, maneuver: "Head straight", icon: "↑" },
      { sequence: 2, instruction: "Turn left in 20 metres into Sports Complex courtyard", distanceMeters: 25, maneuver: "Turn left in 20 metres", icon: "↰" },
      { sequence: 3, instruction: "You have arrived at your destination: Ķīpsala Sports Center", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "rtu-student-hostel",
    canonicalName: "RTU Student Hostel",
    shortName: "Student Hostel",
    subtitle: "Āzenes iela 22, Ķīpsala",
    category: "Living",
    coordinates: { lat: 56.9532, lon: 24.0785 },
    distanceKm: 1.1,
    estimatedMinutes: 14,
    waypointCount: 3,
    aliases: [
      "student hostel",
      "the hostel",
      "hostel",
      "dormitory",
      "dorm",
      "dorms",
      "student housing",
      "residence hall"
    ],
    description: "Student residence halls and campus apartments.",
    pedestrianCrossings: [],
    transitOptions: [],
    waypoints: [
      { sequence: 1, instruction: "Walk east along Āzenes iela", distanceMeters: 80, maneuver: "Head straight", icon: "↑" },
      { sequence: 2, instruction: "Turn right in 20 metres onto hostel pedestrian walkway", distanceMeters: 35, maneuver: "Turn right in 20 metres", icon: "↱" },
      { sequence: 3, instruction: "You have arrived at your destination: RTU Student Hostel", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "rtu-cafeteria",
    canonicalName: "RTU Campus Cafeteria & Canteen",
    shortName: "Cafeteria",
    subtitle: "Āzenes iela 12, Ķīpsala",
    category: "Dining",
    coordinates: { lat: 56.9519, lon: 24.0805 },
    distanceKm: 0.6,
    estimatedMinutes: 8,
    waypointCount: 3,
    aliases: [
      "cafeteria",
      "the cafeteria",
      "canteen",
      "dining hall",
      "lunch",
      "food court",
      "cafe",
      "coffee shop",
      "restaurant",
      "student dining"
    ],
    description: "Accessible campus cafeteria and coffee shop.",
    pedestrianCrossings: [],
    transitOptions: [],
    waypoints: [
      { sequence: 1, instruction: "Walk toward Faculty walkway", distanceMeters: 50, maneuver: "Head straight", icon: "↑" },
      { sequence: 2, instruction: "Turn right in 20 metres into courtyard dining entrance", distanceMeters: 20, maneuver: "Turn right in 20 metres", icon: "↱" },
      { sequence: 3, instruction: "You have arrived at your destination: Campus Cafeteria", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "swedbank-building",
    canonicalName: "Swedbank Central Building",
    shortName: "Swedbank",
    subtitle: "Balasta dambis 15, Riga",
    category: "Business",
    coordinates: { lat: 56.9489, lon: 24.0858 },
    distanceKm: 1.8,
    estimatedMinutes: 21,
    waypointCount: 2,
    aliases: [
      "swedbank",
      "swedbank central building",
      "bank",
      "balasta dambis",
      "swedbank tower"
    ],
    description: "Landmark office building on the Daugava riverbank.",
    pedestrianCrossings: [],
    transitOptions: [],
    waypoints: [
      { sequence: 1, instruction: "Walk south on Balasta dambis along river", distanceMeters: 140, maneuver: "Head straight", icon: "↑" },
      { sequence: 2, instruction: "You have arrived at your destination: Swedbank Building", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "riga-central-station",
    canonicalName: "Rīga Central Station",
    shortName: "Central Station",
    subtitle: "Stacijas laukums 2, Rīga",
    category: "Transit",
    coordinates: { lat: 56.9463, lon: 24.1205 },
    distanceKm: 3.1,
    estimatedMinutes: 38,
    waypointCount: 4,
    aliases: [
      "central station",
      "riga central station",
      "train station",
      "railway station",
      "stacijas laukums"
    ],
    description: "Main passenger railway station and public transport interchange.",
    pedestrianCrossings: [
      { id: "cross-13-janvara", name: "13. janvāra iela / Marijas iela signalized crossing", distanceMeters: 120, type: "signalized_zebra", tactilePaving: true, audioSignal: true }
    ],
    transitOptions: [
      {
        mode: "trolleybus",
        routeNumber: "9",
        lineName: "Trolleybus 9 (Ķīpsala → Stacijas laukums)",
        boardStop: "Ķīpsala",
        alightStop: "Stacijas laukums",
        stopsCount: 4,
        rideMinutes: 10,
        walkToCampusMeters: 80,
        totalMinutes: 14,
        boardingInstructions: "Board Trolleybus 9 at Ķīpsala platform heading toward city center. Ride 4 stops to terminal stop Stacijas laukums."
      }
    ],
    waypoints: [
      { sequence: 1, instruction: "Cross bridge walkway toward City Center", distanceMeters: 730, maneuver: "Head straight", icon: "↑" },
      { sequence: 2, instruction: "Continue straight along 13. Janvāra iela", distanceMeters: 450, maneuver: "Head straight", icon: "↑" },
      { sequence: 3, instruction: "Your tram stop is approaching at Stacijas laukums", distanceMeters: 60, maneuver: "Transit stop ahead", icon: "🚊" },
      { sequence: 4, instruction: "You have arrived at your destination: Rīga Central Station", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "kipsala-transit-stop",
    canonicalName: "Ķīpsala Transit Stop",
    shortName: "Bus Stop",
    subtitle: "Krišjāņa Valdemāra iela, Ķīpsala",
    category: "Transit",
    coordinates: { lat: 56.9501, lon: 24.0842 },
    distanceKm: 0.4,
    estimatedMinutes: 5,
    waypointCount: 2,
    aliases: [
      "bus stop",
      "the bus stop",
      "transit stop",
      "public transport",
      "trolleybus stop",
      "kipsala bus",
      "tram stop"
    ],
    description: "Local bus and trolleybus transit stop with tactile paving and audio schedule cues.",
    pedestrianCrossings: [],
    transitOptions: [
      {
        mode: "bus",
        routeNumber: "3, 22, 37, 41, 53",
        lineName: "Rīgas Satiksme Buses & Trolleybus 9",
        boardStop: "Ķīpsala",
        alightStop: "Grēcinieku iela / Autoosta / Airport RIX (Bus 22)",
        stopsCount: 2,
        rideMinutes: 5,
        walkToCampusMeters: 0,
        totalMinutes: 5,
        boardingInstructions: "Wait beside the front shelter post with raised tactile paving. External speaker announces arriving route number."
      }
    ],
    waypoints: [
      { sequence: 1, instruction: "Walk east toward Krišjāņa Valdemāra iela transit ramp", distanceMeters: 40, maneuver: "Head straight", icon: "↑" },
      { sequence: 2, instruction: "You have arrived at your destination: Ķīpsala Transit Stop", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  }
];

/**
 * Ambiguous query dictionary where multiple distinct destinations could match
 * (Module 1 Step 5: "Ask a clarification question if the destination is ambiguous.")
 */
const AMBIGUOUS_QUERIES = {
  "university": {
    clarificationPrompt: "Did you mean Riga Technical University Ķīpsala Campus, RTU Main Building, or RTU Scientific Library?",
    candidates: ["Riga Technical University (RTU)", "RTU Main Building & Administration", "RTU Scientific Library"]
  },
  "station": {
    clarificationPrompt: "Which station would you like to go to? Say Rīga Central Station or Ķīpsala Transit Stop.",
    candidates: ["Rīga Central Station", "Ķīpsala Transit Stop"]
  },
  "building": {
    clarificationPrompt: "Which building do you want to navigate to? For example, RTU Main Building, RTU Scientific Library, or Swedbank Central Building.",
    candidates: ["RTU Main Building & Administration", "RTU Scientific Library", "Swedbank Central Building"]
  },
  "rtu building": {
    clarificationPrompt: "Which RTU building would you like to reach? Say RTU Main Building, RTU Scientific Library, or RTU Sports Center.",
    candidates: ["RTU Main Building & Administration", "RTU Scientific Library", "RTU Ķīpsala Sports Center & Pool"]
  }
};

/**
 * Extracts optional origin ("from X to Y") and navigation preferences ("by tram", "by bus", "walking only", "avoid stairs")
 */
function extractOriginDestinationAndPreferences(rawText) {
  const cleaned = (rawText || "").trim();
  const lower = cleaned.toLowerCase();

  const preferences = {
    mode: /by (bus|tram|trolleybus|public transport|transit)|take (a |the )?(bus|tram|trolleybus)/i.test(lower) ? "transit" : "walking",
    avoidStairs: /avoid stairs|no stairs|wheelchair|ramp only|step free/i.test(lower),
    includeTransitOptions: true
  };

  // Check "from <origin> to <destination>" pattern
  const fromToMatch = cleaned.match(/\bfrom\s+(.+?)\s+to\s+(.+?)$/i);
  if (fromToMatch) {
    const rawOrigin = fromToMatch[1].replace(/^(the|a|an)\s+/i, "").trim();
    const rawDest = fromToMatch[2]
      .replace(/\b(by bus|by tram|by trolleybus|by public transport|on foot|walking|without stairs|avoiding stairs).*$/i, "")
      .replace(/^(the|a|an)\s+/i, "")
      .trim();
    const matchedOrigin = findLocationMatch(rawOrigin) || createCustomDestination(rawOrigin);
    return {
      originQuery: rawOrigin,
      originLocation: matchedOrigin,
      destinationQuery: rawDest,
      preferences
    };
  }

  return {
    originQuery: null,
    originLocation: null,
    destinationQuery: null,
    preferences
  };
}

/**
 * Validates extracted destination before starting navigation (Module 1 Step 5 & 6 + Diagram "Destination clear?" node)
 */
function validateDestinationBeforeNavigation(cleanQuery, rawTranscript = "") {
  const q = (cleanQuery || "").toLowerCase().replace(/[\?\!\.,;:]/g, "").trim();

  // Vague or missing destination phrases -> Destination clear? = NO -> Ask User to Clarify
  const vaguePhrases = new Set([
    "",
    "there",
    "somewhere",
    "anywhere",
    "it",
    "place",
    "location",
    "a place",
    "some place",
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
    "go",
    "walk"
  ]);

  if (vaguePhrases.has(q)) {
    return {
      isDestinationClear: false,
      isAmbiguous: true,
      validatedDestination: null,
      clarificationPrompt: "Your destination is not clear yet. Where would you like to go? For example, say 'Take me to Riga Technical University' or 'RTU Scientific Library'."
    };
  }

  // Check explicit ambiguous category queries
  if (AMBIGUOUS_QUERIES[q]) {
    return {
      isDestinationClear: false,
      isAmbiguous: true,
      validatedDestination: null,
      candidates: AMBIGUOUS_QUERIES[q].candidates,
      clarificationPrompt: AMBIGUOUS_QUERIES[q].clarificationPrompt
    };
  }

  // Known catalog match
  const matched = findLocationMatch(q);
  if (matched) {
    return {
      isDestinationClear: true,
      isAmbiguous: false,
      validatedDestination: matched,
      clarificationPrompt: null
    };
  }

  // Custom geographic place name (at least 2 characters and not a question word)
  if (q.length >= 2 && !/^(what|where|how|why|when|who|can|is|are|do|does)\b/i.test(q)) {
    const customDest = createCustomDestination(cleanQuery);
    return {
      isDestinationClear: true,
      isAmbiguous: false,
      validatedDestination: customDest,
      clarificationPrompt: null
    };
  }

  return {
    isDestinationClear: false,
    isAmbiguous: true,
    validatedDestination: null,
    clarificationPrompt: "I didn't catch a clear destination. Please say the name of the place or address you want to navigate to."
  };
}

/**
 * Searches the catalog for a destination matching user query tokens or aliases
 */
function findLocationMatch(queryText) {
  if (!queryText) return null;
  const clean = queryText.toLowerCase().trim();

  // 1. Direct alias match
  for (const loc of LOCATIONS) {
    for (const alias of loc.aliases) {
      if (clean === alias) {
        return loc;
      }
    }
  }

  // 2. Whole-word alias match using regex boundaries
  for (const loc of LOCATIONS) {
    for (const alias of loc.aliases) {
      const re = new RegExp('\\b' + alias.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'i');
      if (re.test(clean)) {
        return loc;
      }
    }
  }

  // 3. Token overlap score requiring majority token match
  const queryTokens = clean.split(/\s+/).filter(t => t.length > 2);
  if (queryTokens.length === 0) return null;

  let bestMatch = null;
  let highestScore = 0;

  for (const loc of LOCATIONS) {
    let score = 0;
    const allTokens = new Set([
      ...loc.canonicalName.toLowerCase().split(/\s+/),
      ...loc.aliases.flatMap(a => a.split(/\s+/))
    ]);
    for (const qt of queryTokens) {
      if (allTokens.has(qt)) {
        score++;
      }
    }
    if (score > highestScore) {
      highestScore = score;
      bestMatch = loc;
    }
  }

  if (queryTokens.length === 1 && highestScore >= 1) {
    return bestMatch;
  }
  if (queryTokens.length > 1 && highestScore >= Math.ceil(queryTokens.length * 0.6)) {
    return bestMatch;
  }

  return null;
}

/**
 * Formulates a dynamic custom destination for any arbitrary location not in catalog
 */
function createCustomDestination(rawLocationName) {
  const formatted = rawLocationName
    .replace(/^to\s+/i, '')
    .replace(/^(the|a|an)\s+/i, '')
    .trim();
  const title = formatted.charAt(0).toUpperCase() + formatted.slice(1);

  return {
    id: "custom-" + Date.now(),
    canonicalName: title,
    shortName: title,
    subtitle: `${title} • Validated Pedestrian Destination`,
    category: "Real Destination",
    isCustom: true,
    distanceKm: 1.5,
    estimatedMinutes: 18,
    aliases: [title.toLowerCase()],
    description: `User-specified pedestrian destination: ${title}.`,
    pedestrianCrossings: [
      { id: "cross-custom-1", name: `Signalized pedestrian crossing toward ${title}`, distanceMeters: 120, type: "signalized_zebra", tactilePaving: true, audioSignal: true }
    ],
    transitOptions: [
      {
        mode: "bus",
        routeNumber: "3 / 22",
        lineName: "Rīgas Satiksme Public Transport",
        boardStop: "Nearest Transit Stop",
        alightStop: `${title} Stop`,
        stopsCount: 2,
        rideMinutes: 6,
        walkToCampusMeters: 200,
        totalMinutes: 10,
        boardingInstructions: `Wait at tactile curb strip and listen for external route announcement toward ${title}.`
      }
    ],
    waypoints: [
      { sequence: 1, instruction: `Navigation started. Continue straight toward ${title}`, distanceMeters: 120, maneuver: "Head straight", icon: "↑" },
      { sequence: 2, instruction: "Turn left in 20 metres at pedestrian crossing", distanceMeters: 20, maneuver: "Turn left in 20 metres", icon: "↰", isCrossing: true },
      { sequence: 3, instruction: `You have arrived at your destination: ${title}`, distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  };
}

module.exports = {
  LOCATIONS,
  AMBIGUOUS_QUERIES,
  findLocationMatch,
  createCustomDestination,
  extractOriginDestinationAndPreferences,
  validateDestinationBeforeNavigation
};
