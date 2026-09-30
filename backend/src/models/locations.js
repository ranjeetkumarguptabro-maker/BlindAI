/**
 * Locations & Destinations Catalog for Blind AI
 * Used by Gemini AI voice intent parser, navigation route planner, and frontend search.
 */

const LOCATIONS = [
  {
    id: "rtu-campus",
    canonicalName: "Riga Technical University (RTU)",
    shortName: "RTU Campus",
    subtitle: "Ķīpsala Campus, Paula Valdena iela 1",
    category: "Campus",
    distanceKm: 2.4,
    estimatedMinutes: 28,
    waypointCount: 8,
    aliases: [
      "rtu",
      "riga technical university",
      "campus",
      "kipsala campus",
      "kipsala",
      "university",
      "cif",
      "technical university",
      "faculty",
      "main campus"
    ],
    description: "Main university campus with faculty centers, lecture halls, and laboratories.",
    waypoints: [
      { sequence: 1, instruction: "Walk towards Vanšu tilts", distanceMeters: 160, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 2, instruction: "Cross Vanšu tilts (bridge)", distanceMeters: 730, maneuver: "Cross bridge", icon: "arrow.turn.up.left" },
      { sequence: 3, instruction: "Turn right on Ķīpsalas iela", distanceMeters: 120, maneuver: "Turn right", icon: "↱" },
      { sequence: 4, instruction: "Continue straight along Paula Valdena iela", distanceMeters: 80, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 5, instruction: "Approaching pedestrian crossing at Zunda quay", distanceMeters: 30, maneuver: "Crosswalk ahead", icon: "🚶" },
      { sequence: 6, instruction: "Arrived at RTU Main Entrance", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "rtu-library",
    canonicalName: "RTU Scientific Library",
    shortName: "Library",
    subtitle: "Paula Valdena iela 5, Ķīpsala",
    category: "Library",
    distanceKm: 1.3,
    estimatedMinutes: 16,
    waypointCount: 5,
    aliases: [
      "library",
      "the library",
      "scientific library",
      "rtu library",
      "study hall",
      "reading room",
      "central library",
      "book store",
      "books"
    ],
    description: "University library with accessible reading terminals and quiet study floors.",
    waypoints: [
      { sequence: 1, instruction: "Walk north on Paula Valdena iela", distanceMeters: 90, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 2, instruction: "Turn left towards Library entrance", distanceMeters: 40, maneuver: "Turn left", icon: "↰" },
      { sequence: 3, instruction: "Ascend accessible entrance ramp", distanceMeters: 10, maneuver: "Ramp ahead", icon: "arrow.up" },
      { sequence: 4, instruction: "Arrived at RTU Scientific Library", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "rtu-main-building",
    canonicalName: "RTU Main Building & Administration",
    shortName: "Main Building",
    subtitle: "Kaļķu iela 1 / Ķīpsala Center",
    category: "Campus",
    distanceKm: 0.9,
    estimatedMinutes: 11,
    waypointCount: 4,
    aliases: [
      "main building",
      "the main building",
      "administration",
      "admin building",
      "central building",
      "rectorate",
      "dean's office",
      "headquarters",
      "open main building",
      "open the main building"
    ],
    description: "Central administrative building, rectorate, and academic service center.",
    waypoints: [
      { sequence: 1, instruction: "Follow paved pathway towards central square", distanceMeters: 70, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 2, instruction: "Turn right toward administrative portico", distanceMeters: 30, maneuver: "Turn right", icon: "↱" },
      { sequence: 3, instruction: "Arrived at Main Building Entrance", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "rtu-sports-center",
    canonicalName: "RTU Ķīpsala Sports Center & Pool",
    shortName: "Sports Center",
    subtitle: "Ķīpsalas iela 5, Ķīpsala",
    category: "Sports",
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
      "stadium",
      "workout center"
    ],
    description: "Olympic swimming pool, athletics gym, and indoor court complex.",
    waypoints: [
      { sequence: 1, instruction: "Walk south toward Ķīpsalas iela", distanceMeters: 60, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 2, instruction: "Turn left into Sports Complex courtyard", distanceMeters: 25, maneuver: "Turn left", icon: "↰" },
      { sequence: 3, instruction: "Arrived at Ķīpsala Sports Center", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "rtu-student-hostel",
    canonicalName: "RTU Student Hostel",
    shortName: "Student Hostel",
    subtitle: "Āzenes iela 22, Ķīpsala",
    category: "Living",
    distanceKm: 1.1,
    estimatedMinutes: 14,
    waypointCount: 4,
    aliases: [
      "student hostel",
      "the hostel",
      "hostel",
      "dormitory",
      "dorm",
      "dorms",
      "student housing",
      "residence hall",
      "living quarters"
    ],
    description: "Student residence halls and campus apartments.",
    waypoints: [
      { sequence: 1, instruction: "Walk east along Āzenes iela", distanceMeters: 80, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 2, instruction: "Turn right onto hostel pedestrian walkway", distanceMeters: 35, maneuver: "Turn right", icon: "↱" },
      { sequence: 3, instruction: "Arrived at RTU Student Hostel Entrance", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "rtu-cafeteria",
    canonicalName: "RTU Campus Cafeteria & Canteen",
    shortName: "Cafeteria",
    subtitle: "Āzenes iela 12, Ķīpsala",
    category: "Dining",
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
    waypoints: [
      { sequence: 1, instruction: "Walk toward Faculty walkway", distanceMeters: 50, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 2, instruction: "Enter courtyard dining entrance", distanceMeters: 20, maneuver: "Turn right", icon: "↱" },
      { sequence: 3, instruction: "Arrived at Campus Cafeteria", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "swedbank-building",
    canonicalName: "Swedbank Central Building",
    shortName: "Swedbank",
    subtitle: "Balasta dambis 15, Riga",
    category: "Business",
    distanceKm: 1.8,
    estimatedMinutes: 21,
    waypointCount: 6,
    aliases: [
      "swedbank",
      "swedbank central building",
      "bank",
      "balasta dambis",
      "swedbank tower"
    ],
    description: "Landmark office building and financial branch on the Daugava riverbank.",
    waypoints: [
      { sequence: 1, instruction: "Walk north on Balasta dambis along river", distanceMeters: 140, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 2, instruction: "Arrived at Swedbank Building Main Lobby", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "riga-central-station",
    canonicalName: "Rīga Central Station",
    shortName: "Central Station",
    subtitle: "Stacijas laukums, Rīga",
    category: "Transit",
    distanceKm: 3.1,
    estimatedMinutes: 38,
    waypointCount: 10,
    aliases: [
      "central station",
      "riga central station",
      "train station",
      "railway station",
      "trains",
      "railway",
      "station"
    ],
    description: "Main passenger railway station and transit interchange.",
    waypoints: [
      { sequence: 1, instruction: "Cross Vanšu tilts toward City Center", distanceMeters: 200, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 2, instruction: "Continue along 13. Janvāra iela", distanceMeters: 150, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 3, instruction: "Arrived at Rīga Central Station Main Concourse", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  },
  {
    id: "kipsala-transit-stop",
    canonicalName: "Ķīpsala Transit Stop",
    shortName: "Bus Stop",
    subtitle: "Krišjāņa Valdemāra iela, Ķīpsala",
    category: "Transit",
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
      "bus"
    ],
    description: "Local bus and trolleybus transit stop with tactile paving and audio schedule cues.",
    waypoints: [
      { sequence: 1, instruction: "Walk west toward Krišjāņa Valdemāra iela", distanceMeters: 40, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 2, instruction: "Arrived at Ķīpsala Transit Shelter", distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  }
];

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
    subtitle: `${title} • 2.6 km • 32 min • 7 waypoints`,
    category: "Custom Place",
    distanceKm: 2.6,
    estimatedMinutes: 32,
    waypointCount: 7,
    isCustom: true,
    aliases: [title.toLowerCase()],
    description: `User-specified destination: ${title}.`,
    waypoints: [
      { sequence: 1, instruction: `Head toward ${title}`, distanceMeters: 100, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 2, instruction: `Continue along pedestrian pathway to ${title}`, distanceMeters: 120, maneuver: "Head straight", icon: "arrow.up" },
      { sequence: 3, instruction: `Arriving at ${title}`, distanceMeters: 0, maneuver: "Destination reached", icon: "★" }
    ]
  };
}

module.exports = {
  LOCATIONS,
  findLocationMatch,
  createCustomDestination
};
