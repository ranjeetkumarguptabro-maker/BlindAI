/**
 * rigaRoadSignsCatalog.js
 *
 * Complete Official Catalog of Road Signs in Riga (Latvia)
 * Following Latvian (LVS 77 / European Vienna Convention) Road Sign Standards.
 *
 * Categories:
 * 1. Warning Signs (Brīdinošas zīmes) - 19 signs
 * 2. Prohibition Signs (Aizlieguma zīmes) - 19 signs
 * 3. Mandatory Signs (Norādījuma zīmes) - 17 signs
 * 4. Information Signs (Informācijas zīmes) - 19 signs
 * 5. Direction Signs (Ceļa zīmes – norādes) - 11 signs
 * 6. Temporary Signs (Pagaidu ceļa zīmes) - 9 signs
 * 7. Additional Plates (Papildzīmes) - 7 signs
 * Total: 101 entries (all signs from the Riga Road Signs reference board + Tree / Nature hazards)
 */

const RIGA_ROAD_SIGNS_CATALOG = [
  // ==================== 1. WARNING SIGNS (Brīdinošas zīmes) ====================
  {
    id: 'warn_general_danger',
    name: 'General danger',
    latvianName: 'Citas briesmas',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '⚠️',
    pedestrianGuidance: 'Warning sign ahead: General danger. Proceed with heightened caution.',
    keywords: ['general danger', 'danger', 'citas briesmas', '!']
  },
  {
    id: 'warn_bend_left',
    name: 'Dangerous bend left',
    latvianName: 'Bīstams pagrieziens pa kreisi',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '⚠️',
    pedestrianGuidance: 'Warning sign: Dangerous road bend to the left ahead. Listen carefully for curving traffic.',
    keywords: ['dangerous bend left', 'bend left', 'curve left']
  },
  {
    id: 'warn_bend_right',
    name: 'Dangerous bend right',
    latvianName: 'Bīstams pagrieziens pa labi',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '⚠️',
    pedestrianGuidance: 'Warning sign: Dangerous road bend to the right ahead. Listen for approaching vehicles.',
    keywords: ['dangerous bend right', 'bend right', 'curve right']
  },
  {
    id: 'warn_double_bend',
    name: 'Double bend',
    latvianName: 'Bīstami pagriezieni',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '⚠️',
    pedestrianGuidance: 'Warning sign: Double road bend ahead. Stay well inside the sidewalk.',
    keywords: ['double bend', 'winding road']
  },
  {
    id: 'warn_steep_descent',
    name: 'Steep descent',
    latvianName: 'Stāvs lejupceļš',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '📐',
    pedestrianGuidance: 'Warning sign: Steep downward slope ahead. Watch your footing on the descent.',
    keywords: ['steep descent', 'downhill', 'slope down']
  },
  {
    id: 'warn_steep_ascent',
    name: 'Steep ascent',
    latvianName: 'Stāvs augšupceļš',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '📐',
    pedestrianGuidance: 'Warning sign: Steep upward incline ahead.',
    keywords: ['steep ascent', 'uphill', 'incline']
  },
  {
    id: 'warn_narrow_road',
    name: 'Narrow road',
    latvianName: 'Ceļa sašaurinājums',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '⚠️',
    pedestrianGuidance: 'Warning sign: Road narrows ahead. Sidewalk clearance may be reduced.',
    keywords: ['narrow road', 'road narrows']
  },
  {
    id: 'warn_road_narrows_both',
    name: 'Road narrows (both sides)',
    latvianName: 'Ceļa sašaurinājums abās pusēs',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '⚠️',
    pedestrianGuidance: 'Warning sign: Road narrows on both sides. Keep to the inner edge of the walkway.',
    keywords: ['road narrows both sides', 'narrows both sides']
  },
  {
    id: 'warn_uneven_road',
    name: 'Uneven road',
    latvianName: 'Nelīdzens ceļš',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '⚠️',
    pedestrianGuidance: 'Warning sign: Uneven ground surface ahead. Watch your step for bumps or potholes.',
    keywords: ['uneven road', 'bumpy road', 'nelidzens cels']
  },
  {
    id: 'warn_slippery_road',
    name: 'Slippery road',
    latvianName: 'Slidens ceļš',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '⚠️',
    pedestrianGuidance: 'Warning sign: Slippery surface ahead. Shorten your stride for traction.',
    keywords: ['slippery road', 'slidens cels', 'slippery']
  },
  {
    id: 'warn_falling_rocks',
    name: 'Falling rocks',
    latvianName: 'Akmeņu nogruvums',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '⚠️',
    pedestrianGuidance: 'Warning sign: Falling rocks or debris zone ahead.',
    keywords: ['falling rocks', 'debris']
  },
  {
    id: 'warn_pedestrians',
    name: 'Pedestrians',
    latvianName: 'Gājēji',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '🚸',
    pedestrianGuidance: 'Warning sign: Pedestrian crossing zone ahead. Prepare to align with crosswalk.',
    keywords: ['pedestrians', 'gajeji', 'pedestrian warning']
  },
  {
    id: 'warn_children',
    name: 'Children',
    latvianName: 'Bērni',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '🚸',
    pedestrianGuidance: 'Warning sign: Children and school zone ahead. Expect active foot traffic.',
    keywords: ['children', 'berni', 'school zone']
  },
  {
    id: 'warn_cyclists',
    name: 'Cyclists',
    latvianName: 'Velosipēdisti',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '🚲',
    pedestrianGuidance: 'Warning sign: Cyclist crossing ahead. Listen for approaching bicycles and scooters.',
    keywords: ['cyclists', 'velosipedisti', 'bicycle warning']
  },
  {
    id: 'warn_crossroads',
    name: 'Crossroads',
    latvianName: 'Krustojums',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '➕',
    pedestrianGuidance: 'Warning sign: Uncontrolled crossroads intersection ahead. Stop at curb and listen all ways.',
    keywords: ['crossroads', 'krustojums', 'intersection']
  },
  {
    id: 'warn_roundabout',
    name: 'Roundabout',
    latvianName: 'Lokveida krustojums',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '🔄',
    pedestrianGuidance: 'Warning sign: Roundabout intersection ahead. Use designated perimeter crosswalks.',
    keywords: ['roundabout warning', 'lokveida krustojums']
  },
  {
    id: 'warn_tramway',
    name: 'Tramway',
    latvianName: 'Tramvajs',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '🚊',
    pedestrianGuidance: 'Warning sign: Riga Tramway tracks ahead! Watch for rail grooves in pavement and approaching trams.',
    keywords: ['tramway', 'tramvajs', 'tram crossing', 'tram tracks']
  },
  {
    id: 'warn_level_crossing_barrier',
    name: 'Level crossing with barrier',
    latvianName: 'Dzelzceļa pārbrauktuve ar barjeru',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '🚧',
    pedestrianGuidance: 'Warning sign: Railway level crossing with gate barrier ahead. Listen for warning bells.',
    keywords: ['level crossing with barrier', 'railway barrier', 'train crossing']
  },
  {
    id: 'warn_level_crossing_no_barrier',
    name: 'Level crossing without barrier',
    latvianName: 'Dzelzceļa pārbrauktuve bez barjeras',
    category: 'Warning Signs',
    categoryLatvian: 'Brīdinošas zīmes',
    shape: 'triangle_red',
    icon: '🚂',
    pedestrianGuidance: 'Danger: Unprotected railway level crossing without barrier ahead! Stop and listen carefully.',
    keywords: ['level crossing without barrier', 'unguarded railway']
  },

  // ==================== 2. PROHIBITION SIGNS (Aizlieguma zīmes) ====================
  {
    id: 'prohib_no_entry',
    name: 'No entry',
    latvianName: 'Iebraukt aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red_solid',
    icon: '⛔',
    pedestrianGuidance: 'Prohibition sign: No entry for vehicles (One-way exit). Vehicles may exit toward you.',
    keywords: ['no entry', 'iebraukt aizliegts', 'do not enter']
  },
  {
    id: 'prohib_no_vehicles',
    name: 'No vehicles',
    latvianName: 'Braukt aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '⭕',
    pedestrianGuidance: 'Prohibition sign: All vehicles prohibited. Street ahead is calm for pedestrians.',
    keywords: ['no vehicles', 'braukt aizliegts']
  },
  {
    id: 'prohib_no_motor_vehicles',
    name: 'No motor vehicles',
    latvianName: 'Mehāniskajiem transportlīdzekļiem braukt aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '🚫',
    pedestrianGuidance: 'Prohibition sign: No motor vehicles allowed beyond this point.',
    keywords: ['no motor vehicles', 'no cars']
  },
  {
    id: 'prohib_no_motorcycles',
    name: 'No motorcycles',
    latvianName: 'Motocikliem braukt aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '🚫',
    pedestrianGuidance: 'Prohibition sign: No motorcycles allowed.',
    keywords: ['no motorcycles']
  },
  {
    id: 'prohib_no_lorries',
    name: 'No lorries',
    latvianName: 'Kravas automobiļiem braukt aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '🚫',
    pedestrianGuidance: 'Prohibition sign: Heavy trucks prohibited.',
    keywords: ['no lorries', 'no trucks']
  },
  {
    id: 'prohib_no_buses',
    name: 'No buses',
    latvianName: 'Autobusiem braukt aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '🚫',
    pedestrianGuidance: 'Prohibition sign: Buses prohibited.',
    keywords: ['no buses']
  },
  {
    id: 'prohib_no_bicycles',
    name: 'No bicycles',
    latvianName: 'Velosipēdiem braukt aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '🚳',
    pedestrianGuidance: 'Prohibition sign: Bicycles prohibited on this walkway.',
    keywords: ['no bicycles', 'no bikes']
  },
  {
    id: 'prohib_no_pedestrians',
    name: 'No pedestrians',
    latvianName: 'Gājējiem iet aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '🚷',
    pedestrianGuidance: 'CRITICAL ALERT: No pedestrians sign detected! Walking is prohibited here. Use alternate sidewalk.',
    keywords: ['no pedestrians', 'gajejiem iet aizliegts', 'pedestrians prohibited']
  },
  {
    id: 'prohib_no_right_turn',
    name: 'No right turn',
    latvianName: 'Nogriezties pa labi aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '🚫',
    pedestrianGuidance: 'Traffic sign: No right turn for vehicles.',
    keywords: ['no right turn']
  },
  {
    id: 'prohib_no_left_turn',
    name: 'No left turn',
    latvianName: 'Nogriezties pa kreisi aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '🚫',
    pedestrianGuidance: 'Traffic sign: No left turn for vehicles.',
    keywords: ['no left turn']
  },
  {
    id: 'prohib_no_u_turn',
    name: 'No U-turn',
    latvianName: 'Apgriezties pretējā virzienā aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '🚫',
    pedestrianGuidance: 'Traffic sign: No U-turn for vehicles.',
    keywords: ['no u-turn', 'no u turn']
  },
  {
    id: 'prohib_no_overtaking',
    name: 'No overtaking',
    latvianName: 'Apdzīt aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '🚫',
    pedestrianGuidance: 'Traffic sign: No overtaking zone.',
    keywords: ['no overtaking']
  },
  {
    id: 'prohib_no_overtaking_lorries',
    name: 'No overtaking (lorries)',
    latvianName: 'Kravas automobiļiem apdzīt aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '🚫',
    pedestrianGuidance: 'Traffic sign: No overtaking for trucks.',
    keywords: ['no overtaking lorries']
  },
  {
    id: 'prohib_max_speed_50',
    name: 'Maximum speed (50 km/h)',
    latvianName: 'Maksimālā ātruma ierobežojums 50',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '5️⃣0️⃣',
    pedestrianGuidance: 'Speed limit sign: 50 kilometers per hour urban traffic zone.',
    keywords: ['maximum speed', 'speed limit 50', '50']
  },
  {
    id: 'prohib_max_height',
    name: 'Maximum height (4.0m)',
    latvianName: 'Augstuma ierobežojums 4,0m',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '↕️',
    pedestrianGuidance: 'Clearance sign: Maximum overhead height 4.0 meters (bridge or archway ahead).',
    keywords: ['maximum height', '4.0m', '4,0m']
  },
  {
    id: 'prohib_max_width',
    name: 'Maximum width (2.5m)',
    latvianName: 'Platuma ierobežojums 2,5m',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '↔️',
    pedestrianGuidance: 'Clearance sign: Maximum road width 2.5 meters (narrow passage).',
    keywords: ['maximum width', '2.5m', '2,5m']
  },
  {
    id: 'prohib_max_axle_load',
    name: 'Maximum axle load (6t)',
    latvianName: 'Ass slodzes ierobežojums 6t',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_red',
    icon: '⚖️',
    pedestrianGuidance: 'Traffic sign: Maximum axle load 6 tonnes.',
    keywords: ['maximum axle load', '6t']
  },
  {
    id: 'prohib_no_stopping',
    name: 'No stopping',
    latvianName: 'Apstāties un stāvēt aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_blue_red_x',
    icon: '🚫',
    pedestrianGuidance: 'Sign: No stopping or standing along curb.',
    keywords: ['no stopping', 'apstaties aizliegts']
  },
  {
    id: 'prohib_no_parking',
    name: 'No parking',
    latvianName: 'Stāvēt aizliegts',
    category: 'Prohibition Signs',
    categoryLatvian: 'Aizlieguma zīmes',
    shape: 'circle_blue_red_slash',
    icon: '🚫',
    pedestrianGuidance: 'Sign: No parking along curb.',
    keywords: ['no parking', 'stavet aizliegts']
  },

  // ==================== 3. MANDATORY SIGNS (Norādījuma zīmes) ====================
  {
    id: 'mand_proceed_straight',
    name: 'Proceed straight',
    latvianName: 'Braukt taisni',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '⬆️',
    pedestrianGuidance: 'Mandatory sign: Traffic proceeds straight ahead.',
    keywords: ['proceed straight', 'braukt taisni', 'straight only']
  },
  {
    id: 'mand_turn_right',
    name: 'Turn right',
    latvianName: 'Braukt pa labi',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '➡️',
    pedestrianGuidance: 'Mandatory sign: Turn right ahead.',
    keywords: ['turn right sign', 'braukt pa labi']
  },
  {
    id: 'mand_turn_left',
    name: 'Turn left',
    latvianName: 'Braukt pa kreisi',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '⬅️',
    pedestrianGuidance: 'Mandatory sign: Turn left ahead.',
    keywords: ['turn left sign', 'braukt pa kreisi']
  },
  {
    id: 'mand_straight_or_right',
    name: 'Proceed straight or right',
    latvianName: 'Braukt taisni vai pa labi',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '↗️',
    pedestrianGuidance: 'Mandatory sign: Traffic proceeds straight or turns right.',
    keywords: ['proceed straight or right']
  },
  {
    id: 'mand_straight_or_left',
    name: 'Proceed straight or left',
    latvianName: 'Braukt taisni vai pa kreisi',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '↖️',
    pedestrianGuidance: 'Mandatory sign: Traffic proceeds straight or turns left.',
    keywords: ['proceed straight or left']
  },
  {
    id: 'mand_keep_right',
    name: 'Keep right',
    latvianName: 'Apbraukt šķērsli pa labi',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '↘️',
    pedestrianGuidance: 'Mandatory sign: Keep right around island or obstacle.',
    keywords: ['keep right sign', 'pass on right']
  },
  {
    id: 'mand_keep_left',
    name: 'Keep left',
    latvianName: 'Apbraukt šķērsli pa kreisi',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '↙️',
    pedestrianGuidance: 'Mandatory sign: Keep left around island or obstacle.',
    keywords: ['keep left sign', 'pass on left']
  },
  {
    id: 'mand_roundabout',
    name: 'Roundabout (Mandatory)',
    latvianName: 'Lokveida krustojums',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '🔄',
    pedestrianGuidance: 'Mandatory sign: Roundabout traffic circle directly ahead.',
    keywords: ['roundabout mandatory', 'traffic circle']
  },
  {
    id: 'mand_min_speed',
    name: 'Minimum speed (50)',
    latvianName: 'Minimālā ātruma ierobežojums',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '🔵',
    pedestrianGuidance: 'Mandatory sign: Minimum vehicle speed 50 km/h.',
    keywords: ['minimum speed']
  },
  {
    id: 'mand_pedestrian_path',
    name: 'Pedestrian path',
    latvianName: 'Gājēju ceļš',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '🚶',
    pedestrianGuidance: 'Dedicated Pedestrian Path sign detected! Safe vehicle-free walkway ahead.',
    keywords: ['pedestrian path', 'gajeju cels', 'footpath', 'walkway sign']
  },
  {
    id: 'mand_cycle_path',
    name: 'Cycle path',
    latvianName: 'Velosipēdu ceļš',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '🚲',
    pedestrianGuidance: 'Caution: Dedicated Cycle Path sign! Step to the pedestrian side to avoid bicycles.',
    keywords: ['cycle path', 'velosipedu cels', 'bike lane']
  },
  {
    id: 'mand_shared_ped_cycle',
    name: 'Shared pedestrian and cycle path',
    latvianName: 'Kopīgs gājēju un velosipēdu ceļš',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '🚶🚲',
    pedestrianGuidance: 'Shared Pedestrian and Cycle Path sign! Walk safely and stay alert for passing cyclists.',
    keywords: ['shared pedestrian and cycle path', 'kopigs gajeju un velosipedu cels', 'shared path']
  },
  {
    id: 'mand_snow_chains',
    name: 'Snow chains compulsory',
    latvianName: 'Obligāti jālieto pretslīdes ķēdes',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '❄️',
    pedestrianGuidance: 'Winter road sign: Icy conditions, snow chains compulsory.',
    keywords: ['snow chains']
  },
  {
    id: 'mand_sound_horn',
    name: 'Sound horn',
    latvianName: 'Skaņas signāla lietošana',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_blue',
    icon: '📯',
    pedestrianGuidance: 'Mandatory sign: Sound horn zone.',
    keywords: ['sound horn']
  },
  {
    id: 'mand_end_min_speed',
    name: 'End of mandatory speed',
    latvianName: 'Minimālā ātruma ierobežojuma beigas',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_grey_slash',
    icon: '⚪',
    pedestrianGuidance: 'Sign: End of minimum speed zone.',
    keywords: ['end of mandatory speed']
  },
  {
    id: 'mand_end_no_overtaking',
    name: 'End of no overtaking',
    latvianName: 'Apdzīšanas aizlieguma beigas',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_grey_slash',
    icon: '⚪',
    pedestrianGuidance: 'Sign: End of no overtaking restriction.',
    keywords: ['end of no overtaking']
  },
  {
    id: 'mand_end_no_overtaking_lorries',
    name: 'End of no overtaking (lorries)',
    latvianName: 'Kravas automobiļu apdzīšanas aizlieguma beigas',
    category: 'Mandatory Signs',
    categoryLatvian: 'Norādījuma zīmes',
    shape: 'circle_grey_slash',
    icon: '⚪',
    pedestrianGuidance: 'Sign: End of truck overtaking restriction.',
    keywords: ['end of no overtaking lorries']
  },

  // ==================== 4. INFORMATION SIGNS (Informācijas zīmes) ====================
  {
    id: 'info_priority_road',
    name: 'Priority road',
    latvianName: 'Galvenais ceļš',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'diamond_yellow',
    icon: '🔶',
    pedestrianGuidance: 'Information sign: Priority main road. Vehicles have right of way unless at a zebra crosswalk.',
    keywords: ['priority road', 'galvenais cels']
  },
  {
    id: 'info_end_priority_road',
    name: 'End of priority road',
    latvianName: 'Galvenā ceļa beigas',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'diamond_yellow_slash',
    icon: '🔶',
    pedestrianGuidance: 'Information sign: End of priority road.',
    keywords: ['end of priority road']
  },
  {
    id: 'info_give_way',
    name: 'Give way',
    latvianName: 'Dodiet ceļu',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'triangle_inverted_red',
    icon: '🔻',
    pedestrianGuidance: 'Yield / Give Way sign detected at intersection ahead.',
    keywords: ['give way', 'dodiet celu', 'yield']
  },
  {
    id: 'info_stop',
    name: 'Stop Sign',
    latvianName: 'Neapstājoties tālāk braukt aizliegts (STOP)',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'octagon_red',
    icon: '🛑',
    pedestrianGuidance: 'STOP sign detected at intersection! Vehicles must halt here. Check before crossing.',
    keywords: ['stop', 'stop sign']
  },
  {
    id: 'info_pedestrian_crossing',
    name: 'Pedestrian crossing Sign',
    latvianName: 'Gājēju pāreja',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '🚸',
    pedestrianGuidance: 'Pedestrian Crossing (Gājēju pāreja) sign detected! Zebra crossing path is right here.',
    keywords: ['pedestrian crossing', 'gajeju pareja', 'crosswalk sign', 'zebra sign']
  },
  {
    id: 'info_underpass',
    name: 'Underpass',
    latvianName: 'Apakšzemes gājēju pāreja',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '↘️🪜',
    pedestrianGuidance: 'Pedestrian Underpass sign detected! Stairs leading down to underground crossing ahead.',
    keywords: ['underpass', 'apakszemes gajeju pareja', 'subway crossing']
  },
  {
    id: 'info_overpass',
    name: 'Overpass',
    latvianName: 'Virszemes gājēju pāreja',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '↗️🪜',
    pedestrianGuidance: 'Pedestrian Overpass bridge sign detected! Stairs leading up ahead.',
    keywords: ['overpass', 'virszemes gajeju pareja', 'pedestrian bridge']
  },
  {
    id: 'info_dead_end',
    name: 'Dead end',
    latvianName: 'Strupceļš',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '🛑',
    pedestrianGuidance: 'Dead end (Strupceļš) street sign detected ahead. No through road for vehicles.',
    keywords: ['dead end', 'strupcels', 'cul de sac']
  },
  {
    id: 'info_one_way',
    name: 'One-way street',
    latvianName: 'Vienvirziena ceļš',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '⬆️',
    pedestrianGuidance: 'One-way street (Vienvirziena ceļš) sign detected.',
    keywords: ['one-way street', 'one way', 'vienvirziena cels']
  },
  {
    id: 'info_parking',
    name: 'Parking (P)',
    latvianName: 'Stāvvieta (P)',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '🅿️',
    pedestrianGuidance: 'Parking area (P) sign detected. Watch for cars maneuvering or reversing.',
    keywords: ['parking', 'stavvieta', 'p']
  },
  {
    id: 'info_parking_zone',
    name: 'Parking zone (ZONA P)',
    latvianName: 'Stāvvietu zona (ZONA P)',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'rect_white_blue',
    icon: '🅿️',
    pedestrianGuidance: 'Parking Zone (ZONA P) sign detected. Watch for parked and moving cars.',
    keywords: ['parking zone', 'zona p', 'stavvietu zona']
  },
  {
    id: 'info_bus_stop',
    name: 'Bus stop',
    latvianName: 'Autobusa pietura',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '🚏',
    pedestrianGuidance: 'Riga Bus Stop (Autobusa pietura) sign detected! Boarding area is right here.',
    keywords: ['bus stop', 'autobusa pietura', 'autobuss', 'pietura']
  },
  {
    id: 'info_tram_stop',
    name: 'Tram stop',
    latvianName: 'Tramvaja pietura',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '🚊',
    pedestrianGuidance: 'Riga Tram Stop (Tramvaja pietura) sign detected! Watch for boarding platform and tracks.',
    keywords: ['tram stop', 'tramvaja pietura', 'tramvajs']
  },
  {
    id: 'info_taxi_rank',
    name: 'Taxi rank (TAXI)',
    latvianName: 'Taksometru stāvvieta (TAXI)',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '🚕',
    pedestrianGuidance: 'Taxi Rank (TAXI) stand sign detected ahead.',
    keywords: ['taxi', 'taxi rank', 'taksometru stavvieta']
  },
  {
    id: 'info_hospital',
    name: 'Hospital',
    latvianName: 'Slimnīca',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '🏥',
    pedestrianGuidance: 'Hospital (Slimnīca) sign detected nearby.',
    keywords: ['hospital', 'slimnica']
  },
  {
    id: 'info_first_aid',
    name: 'First aid post',
    latvianName: 'Pirmās palīdzības punkts',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '➕',
    pedestrianGuidance: 'Medical First Aid Post sign detected nearby.',
    keywords: ['first aid', 'first aid post', 'pirmas palidzibas']
  },
  {
    id: 'info_police',
    name: 'Police (POLICIJA)',
    latvianName: 'Policija (POLICIJA)',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'rect_blue_white',
    icon: '🚓',
    pedestrianGuidance: 'Latvian Police Station (POLICIJA) sign detected ahead.',
    keywords: ['police', 'policija']
  },
  {
    id: 'info_service_station',
    name: 'Service station',
    latvianName: 'Degvielas uzpildes stacija',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '⛽',
    pedestrianGuidance: 'Fuel Service Station sign detected. Watch for vehicles crossing the sidewalk driveway.',
    keywords: ['service station', 'gas station', 'degvielas']
  },
  {
    id: 'info_ev_charging',
    name: 'Electric vehicle charging',
    latvianName: 'Elektromobiļu uzlādes stacija',
    category: 'Information Signs',
    categoryLatvian: 'Informācijas zīmes',
    shape: 'square_blue',
    icon: '🔌',
    pedestrianGuidance: 'Electric Vehicle Charging Station sign detected. Watch for charging cables near curb.',
    keywords: ['electric vehicle charging', 'ev charging', 'elektromobilu']
  },

  // ==================== 5. DIRECTION SIGNS (Ceļa zīmes – norādes) ====================
  {
    id: 'dir_to_riga',
    name: 'Direction: ↑ RĪGA (To Riga)',
    latvianName: 'Virziena rādītājs: ↑ RĪGA',
    category: 'Direction Signs',
    categoryLatvian: 'Ceļa zīmes – norādes',
    shape: 'rect_blue',
    icon: '🪧',
    pedestrianGuidance: 'Direction sign board: Straight ahead to RĪGA.',
    keywords: ['riga', 'rīga', 'to riga']
  },
  {
    id: 'dir_to_jurmala',
    name: 'Direction: ← JŪRMALA (To Jūrmala)',
    latvianName: 'Virziena rādītājs: ← JŪRMALA',
    category: 'Direction Signs',
    categoryLatvian: 'Ceļa zīmes – norādes',
    shape: 'rect_blue',
    icon: '🪧',
    pedestrianGuidance: 'Direction sign board: Turn left toward JŪRMALA.',
    keywords: ['jurmala', 'jūrmala', 'to jurmala']
  },
  {
    id: 'dir_to_daugavpils',
    name: 'Direction: DAUGAVPILS → (To Daugavpils)',
    latvianName: 'Virziena rādītājs: DAUGAVPILS →',
    category: 'Direction Signs',
    categoryLatvian: 'Ceļa zīmes – norādes',
    shape: 'rect_blue',
    icon: '🪧',
    pedestrianGuidance: 'Direction sign board: Turn right toward DAUGAVPILS.',
    keywords: ['daugavpils', 'to daugavpils']
  },
  {
    id: 'dir_route_e22',
    name: 'European route E22',
    latvianName: 'Eiropas maģistrāle E22',
    category: 'Direction Signs',
    categoryLatvian: 'Ceļa zīmes – norādes',
    shape: 'rect_green',
    icon: '🛣️',
    pedestrianGuidance: 'Route sign: European Highway E22.',
    keywords: ['e22', 'european route']
  },
  {
    id: 'dir_route_a2',
    name: 'National route A2',
    latvianName: 'Galvenais valsts autoceļš A2',
    category: 'Direction Signs',
    categoryLatvian: 'Ceļa zīmes – norādes',
    shape: 'rect_red',
    icon: '🛣️',
    pedestrianGuidance: 'Route sign: Latvian National Highway A2.',
    keywords: ['a2', 'national route']
  },
  {
    id: 'dir_route_p4',
    name: 'Regional route P4',
    latvianName: 'Reģionālais autoceļš P4',
    category: 'Direction Signs',
    categoryLatvian: 'Ceļa zīmes – norādes',
    shape: 'rect_blue',
    icon: '🛣️',
    pedestrianGuidance: 'Route sign: Latvian Regional Road P4.',
    keywords: ['p4', 'regional route']
  },
  {
    id: 'dir_city_centre',
    name: 'Direction: Centrs → (City centre)',
    latvianName: 'Virziena rādītājs: Centrs →',
    category: 'Direction Signs',
    categoryLatvian: 'Ceļa zīmes – norādes',
    shape: 'rect_white',
    icon: '🏙️',
    pedestrianGuidance: 'Riga Direction Sign: Riga City Centre (Centrs) to the right.',
    keywords: ['centrs', 'city centre', 'city center']
  },
  {
    id: 'dir_airport',
    name: 'Direction: ← Lidosta (Airport)',
    latvianName: 'Virziena rādītājs: ← Lidosta',
    category: 'Direction Signs',
    categoryLatvian: 'Ceļa zīmes – norādes',
    shape: 'rect_white',
    icon: '✈️',
    pedestrianGuidance: 'Riga Direction Sign: Riga Airport (Lidosta) to the left.',
    keywords: ['lidosta', 'airport']
  },
  {
    id: 'dir_port',
    name: 'Direction: Osta (Port)',
    latvianName: 'Virziena rādītājs: Osta',
    category: 'Direction Signs',
    categoryLatvian: 'Ceļa zīmes – norādes',
    shape: 'rect_white',
    icon: '⛴️',
    pedestrianGuidance: 'Riga Direction Sign: Riga Passenger Port (Osta).',
    keywords: ['osta', 'port', 'ferry']
  },
  {
    id: 'dir_old_town',
    name: 'Tourist Sign: Vecrīga → (Old Town)',
    latvianName: 'Tūrisma virziena rādītājs: Vecrīga →',
    category: 'Direction Signs',
    categoryLatvian: 'Ceļa zīmes – norādes',
    shape: 'rect_brown',
    icon: '🏛️',
    pedestrianGuidance: 'Tourist Landmark Sign: Riga Old Town (Vecrīga) to the right.',
    keywords: ['vecriga', 'vecrīga', 'old town']
  },
  {
    id: 'dir_museum',
    name: 'Tourist Sign: Muzejs → (Museum)',
    latvianName: 'Tūrisma virziena rādītājs: Muzejs →',
    category: 'Direction Signs',
    categoryLatvian: 'Ceļa zīmes – norādes',
    shape: 'rect_brown',
    icon: '🏛️',
    pedestrianGuidance: 'Tourist Landmark Sign: Museum (Muzejs) to the right.',
    keywords: ['muzejs', 'museum']
  },

  // ==================== 6. TEMPORARY SIGNS (Pagaidu ceļa zīmes) ====================
  {
    id: 'temp_road_works',
    name: 'Road works (Temporary)',
    latvianName: 'Ceļa darbi (Pagaidu)',
    category: 'Temporary Signs',
    categoryLatvian: 'Pagaidu ceļa zīmes',
    shape: 'triangle_yellow',
    icon: '🚧',
    pedestrianGuidance: 'WARNING: Temporary Road Works sign ahead! Watch for trenches, barriers, or uneven walkway.',
    keywords: ['road works', 'cela darbi', 'construction sign', 'men at work']
  },
  {
    id: 'temp_traffic_lights',
    name: 'Temporary traffic lights',
    latvianName: 'Gaismas luksofors (Pagaidu)',
    category: 'Temporary Signs',
    categoryLatvian: 'Pagaidu ceļa zīmes',
    shape: 'triangle_yellow',
    icon: '🚦',
    pedestrianGuidance: 'Temporary traffic signal ahead due to road works.',
    keywords: ['temporary traffic lights', 'luksofors']
  },
  {
    id: 'temp_uneven_road',
    name: 'Uneven road (Temporary)',
    latvianName: 'Nelīdzens ceļš (Pagaidu)',
    category: 'Temporary Signs',
    categoryLatvian: 'Pagaidu ceļa zīmes',
    shape: 'triangle_yellow',
    icon: '⚠️',
    pedestrianGuidance: 'Caution: Temporary uneven pavement surface ahead due to construction.',
    keywords: ['uneven road temporary', 'construction bumps']
  },
  {
    id: 'temp_speed_limit_30',
    name: 'Temporary speed limit (30 km/h)',
    latvianName: 'Pagaidu ātruma ierobežojums 30',
    category: 'Temporary Signs',
    categoryLatvian: 'Pagaidu ceļa zīmes',
    shape: 'circle_red_yellow',
    icon: '3️⃣0️⃣',
    pedestrianGuidance: 'Temporary 30 km/h slow zone sign.',
    keywords: ['temporary speed limit', 'speed limit 30', '30']
  },
  {
    id: 'temp_end_speed_limit',
    name: 'End of temporary speed limit (30)',
    latvianName: 'Pagaidu ātruma ierobežojuma beigas',
    category: 'Temporary Signs',
    categoryLatvian: 'Pagaidu ceļa zīmes',
    shape: 'circle_grey_slash',
    icon: '⚪',
    pedestrianGuidance: 'End of temporary 30 km/h speed limit.',
    keywords: ['end of temporary speed limit']
  },
  {
    id: 'temp_lane_closure_right',
    name: 'Lane closure (right)',
    latvianName: 'Brauktuves sašaurinājums pa labi',
    category: 'Temporary Signs',
    categoryLatvian: 'Pagaidu ceļa zīmes',
    shape: 'rect_yellow',
    icon: '🚧',
    pedestrianGuidance: 'Temporary sign: Right lane closed ahead.',
    keywords: ['lane closure right']
  },
  {
    id: 'temp_lane_closure_left',
    name: 'Lane closure (left)',
    latvianName: 'Brauktuves sašaurinājums pa kreisi',
    category: 'Temporary Signs',
    categoryLatvian: 'Pagaidu ceļa zīmes',
    shape: 'rect_yellow',
    icon: '🚧',
    pedestrianGuidance: 'Temporary sign: Left lane closed ahead.',
    keywords: ['lane closure left']
  },
  {
    id: 'temp_detour_right',
    name: 'Detour (right)',
    latvianName: 'Apbraukšanas virziens pa labi',
    category: 'Temporary Signs',
    categoryLatvian: 'Pagaidu ceļa zīmes',
    shape: 'rect_yellow',
    icon: '➡️',
    pedestrianGuidance: 'Temporary Detour sign: Path diverted to the right.',
    keywords: ['detour right', 'apbrauksanas']
  },
  {
    id: 'temp_detour_left',
    name: 'Detour (left)',
    latvianName: 'Apbraukšanas virziens pa kreisi',
    category: 'Temporary Signs',
    categoryLatvian: 'Pagaidu ceļa zīmes',
    shape: 'rect_yellow',
    icon: '⬅️',
    pedestrianGuidance: 'Temporary Detour sign: Path diverted to the left.',
    keywords: ['detour left']
  },

  // ==================== 7. ADDITIONAL PLATES (Papildzīmes) ====================
  {
    id: 'plate_distance_100m',
    name: 'Distance plate (100 m)',
    latvianName: 'Attālums līdz objektam (100 m)',
    category: 'Additional Plates',
    categoryLatvian: 'Papildzīmes',
    shape: 'plate_white',
    icon: '📏',
    pedestrianGuidance: 'Additional plate: Feature is 100 meters ahead.',
    keywords: ['100 m', '100m', 'distance plate']
  },
  {
    id: 'plate_extent_300m',
    name: 'Extent of restriction (↑ 300 m ↑)',
    latvianName: 'Darbības zona (300 m)',
    category: 'Additional Plates',
    categoryLatvian: 'Papildzīmes',
    shape: 'plate_white',
    icon: '📏',
    pedestrianGuidance: 'Additional plate: Zone extends for 300 meters.',
    keywords: ['300 m', '300m', 'extent of restriction']
  },
  {
    id: 'plate_winter_period',
    name: 'During winter period',
    latvianName: 'Ziemas periodā',
    category: 'Additional Plates',
    categoryLatvian: 'Papildzīmes',
    shape: 'plate_white',
    icon: '❄️',
    pedestrianGuidance: 'Additional plate: Applies during winter snow/ice period.',
    keywords: ['during winter period', 'winter', 'ziemas']
  },
  {
    id: 'plate_road_works',
    name: 'Applies to road works',
    latvianName: 'Remontdarbi',
    category: 'Additional Plates',
    categoryLatvian: 'Papildzīmes',
    shape: 'plate_white',
    icon: '⚒️',
    pedestrianGuidance: 'Additional plate: Active surface maintenance works.',
    keywords: ['applies to road works', 'remontdarbi']
  },
  {
    id: 'plate_motor_vehicles',
    name: 'Applies to motor vehicles',
    latvianName: 'Transportlīdzekļa veids (Automobiļi)',
    category: 'Additional Plates',
    categoryLatvian: 'Papildzīmes',
    shape: 'plate_white',
    icon: '🚗',
    pedestrianGuidance: 'Additional plate: Applies to passenger cars.',
    keywords: ['applies to motor vehicles']
  },
  {
    id: 'plate_bicycles',
    name: 'Applies to bicycles',
    latvianName: 'Transportlīdzekļa veids (Velosipēdi)',
    category: 'Additional Plates',
    categoryLatvian: 'Papildzīmes',
    shape: 'plate_white',
    icon: '🚲',
    pedestrianGuidance: 'Additional plate: Applies to bicycles and scooters.',
    keywords: ['applies to bicycles']
  },
  {
    id: 'plate_disabled_persons',
    name: 'Applies to disabled persons',
    latvianName: 'Invalīdi (Accessible Zone)',
    category: 'Additional Plates',
    categoryLatvian: 'Papildzīmes',
    shape: 'plate_white',
    icon: '♿',
    pedestrianGuidance: 'Accessibility plate: Designated accessible zone for persons with disabilities.',
    keywords: ['applies to disabled persons', 'disabled', 'invalidi', 'accessible']
  },

  // ==================== 8. URBAN NATURE & SIDEWALK OBSTACLES (Tree / Foliage) ====================
  {
    id: 'urban_tree',
    name: 'Tree',
    latvianName: 'Koks (Sidewalk Tree / Trunk & Canopy)',
    category: 'Sidewalk Environment',
    categoryLatvian: 'Vides objekti',
    shape: 'natural_tree',
    icon: '🌳',
    pedestrianGuidance: 'Tree detected ahead along walkway. Keep clear of tree trunk and overhanging branches.',
    keywords: ['tree', 'trees', 'koks', 'koki', 'branch', 'foliage', 'trunk']
  }
];

function matchRigaRoadSign(queryText) {
  if (!queryText) return null;
  const cleaned = String(queryText).trim().toLowerCase();
  for (const sign of RIGA_ROAD_SIGNS_CATALOG) {
    if (
      sign.name.toLowerCase() === cleaned ||
      sign.latvianName.toLowerCase() === cleaned ||
      sign.keywords.some(k => cleaned.includes(k.toLowerCase()))
    ) {
      return sign;
    }
  }
  return null;
}

module.exports = {
  RIGA_ROAD_SIGNS_CATALOG,
  matchRigaRoadSign
};
