/**
 * UnifiedSafetyEngine.js
 *
 * Implements:
 * - Module 4: Sensor Fusion and Central Navigation Controller
 *   Combines GPS/heading, planned route, YOLO object detections, LiDAR/camera depth estimation,
 *   multi-frame motion tracking, and selective OCR/Gemini scene understanding.
 *   Prioritizes nearby hazards over ordinary route instructions and resumes route guidance once clear.
 *   Enforces Critical Safety Limitation: never tells a user to cross a road merely because a camera
 *   model detects a green light, and communicates uncertainty when detection confidence is low.
 * - Module 5: Concise Voice and Haptic Feedback
 *   Implements canonical concise messages and speech preemption (safety warnings cancel routine speech).
 * - Module 6: Continuous 8-Step Navigation Loop, Route Deviation Rerouting & Honest Sensor Limitations.
 */

const CANONICAL_FEEDBACK = {
  navigation_begins: "Navigation started. Continue straight.",
  upcoming_turn: (dir = "left", meters = 20) => `Turn ${dir} in ${meters} metres.`,
  nearby_obstacle: "Obstacle ahead. Slow down.",
  person_obstacle: (position = "slightly to your right") => `Person ahead, ${position}. Slow down.`,
  route_deviation: "You may have left the planned route. Recalculating.",
  public_transport: (stopType = "tram") => `Your ${stopType} stop is approaching.`,
  uncertain_detection: "I can't confidently identify the sign. Please proceed cautiously.",
  destination_reached: "You have arrived at your destination.",
  green_light_caution:
    "Green signal detected ahead, but camera detection cannot guarantee road safety. Listen for traffic and verify before crossing.",
  gps_inaccurate: "GPS signal is currently inaccurate. Rely on your white cane or guide dog and proceed with caution.",
  camera_unavailable: "Rear camera is currently unavailable. Obstacle detection is inactive.",
  connectivity_lost: "Network connectivity lost. Using local on-device perception and cached route."
};

const HAPTIC_PATTERNS = {
  critical_stop: [200, 100, 200, 100, 400],
  nearby_obstacle: [150, 80, 150],
  caution: [80, 60],
  turn_left: [60, 40, 120],
  turn_right: [120, 40, 60],
  route_deviation: [100, 60, 100, 60, 100],
  arrival: [80, 50, 80],
  clear_resume: [60]
};

class UnifiedSafetyEngine {
  constructor() {
    this.hazardSeverity = "SAFE"; // 'SAFE' | 'NOTICE' | 'CAUTION' | 'DANGER' | 'CRITICAL_STOP'
    this.navState = "IDLE"; // 'IDLE' | 'LISTENING' | 'ROUTING' | 'ACTIVE_WALKING' | 'APPROACHING_CROSSWALK' | 'HAZARD_STOPPED' | 'REROUTING' | 'ARRIVED' | 'EMERGENCY_SOS'

    this.sensorFreshness = {
      camera: { timestamp: 0, isStale: true, maxAgeMs: 1500, available: true },
      gps: { timestamp: 0, isStale: true, maxAgeMs: 12000, accuracyMeters: 5.0, available: true },
      imu: { timestamp: 0, isStale: true, maxAgeMs: 1200, available: true },
      lidar: { timestamp: 0, isStale: true, maxAgeMs: 800, hardwareSupported: false },
      network: { timestamp: Date.now(), isStale: false, maxAgeMs: 30000, online: true }
    };

    this.activePriority = 4;
    this.lastSpeechText = "";
    this.lastSpeechTime = 0;
    this.speechHistory = [];
    this.hapticHistory = [];
    this.listeners = [];

    // Multi-frame object tracking memory (Module 4: reduce repeated warnings & distinguish stationary vs moving toward user)
    this.trackedObjects = new Map();
    this.suppressedRepeatCount = 0;
    this.pendingRouteInstruction = null;
    this.disclaimer =
      "Blind AI is an assistive navigation prototype and is not a replacement for a white cane, guide dog, or standard orientation and mobility (O&M) techniques.";
  }

  getPrototypeDisclaimer() {
    return this.disclaimer;
  }

  addListener(listener) {
    if (typeof listener === "function") {
      this.listeners.push(listener);
    }
  }

  notifyListeners(event, data) {
    this.listeners.forEach(fn => {
      try {
        fn(event, data);
      } catch (err) {
        console.warn("[SafetyEngine] Listener error:", err);
      }
    });
  }

  updateSensor(sensorName, timestamp = Date.now(), meta = {}) {
    if (this.sensorFreshness[sensorName]) {
      this.sensorFreshness[sensorName].timestamp = timestamp;
      this.sensorFreshness[sensorName].isStale = false;
      Object.assign(this.sensorFreshness[sensorName], meta);
      this.notifyListeners("sensor_updated", { sensor: sensorName, timestamp, ...meta });
    }
  }

  checkFreshness(currentTime = Date.now()) {
    for (const [name, info] of Object.entries(this.sensorFreshness)) {
      if (info.timestamp === 0 || currentTime - info.timestamp > info.maxAgeMs) {
        info.isStale = true;
      }
    }
    return { ...this.sensorFreshness };
  }

  /**
   * Module 6: Honest communication of sensor or service limitations
   */
  reportSensorLimitation(limitationType) {
    if (limitationType === "gps_inaccurate") {
      this.sensorFreshness.gps.available = false;
      this.dispatchSpeech(CANONICAL_FEEDBACK.gps_inaccurate, 2, HAPTIC_PATTERNS.caution);
      return CANONICAL_FEEDBACK.gps_inaccurate;
    }
    if (limitationType === "camera_unavailable") {
      this.sensorFreshness.camera.available = false;
      this.dispatchSpeech(CANONICAL_FEEDBACK.camera_unavailable, 2, HAPTIC_PATTERNS.caution);
      return CANONICAL_FEEDBACK.camera_unavailable;
    }
    if (limitationType === "connectivity_lost") {
      this.sensorFreshness.network.online = false;
      this.dispatchSpeech(CANONICAL_FEEDBACK.connectivity_lost, 3, HAPTIC_PATTERNS.caution);
      return CANONICAL_FEEDBACK.connectivity_lost;
    }
    return null;
  }

  /**
   * Module 4: Multi-Frame Object Tracking & Motion Classification
   * Distinguishes stationary obstacles from objects moving toward the user, and suppresses duplicate warnings.
   */
  trackObjectAcrossFrames(obj, now = Date.now()) {
    const key = `${obj.class || obj.label || "obstacle"}_${obj.lane || "center"}`;
    const prev = this.trackedObjects.get(key);
    const dist = typeof obj.distance === "number" ? obj.distance : 3.0;

    let motionState = "stationary";
    let shouldSuppressRepeat = false;

    if (prev && now - prev.timestamp < 4000) {
      const distDelta = dist - prev.distance; // negative means getting closer
      if (distDelta <= -0.25) {
        motionState = "moving_toward_user";
      } else if (distDelta >= 0.25) {
        motionState = "moving_away";
      } else {
        motionState = "stationary";
      }

      // Suppress repeated identical warning if stationary or not significantly closer within 3.5s
      if (motionState !== "moving_toward_user" && Math.abs(distDelta) < 0.35 && now - prev.lastAnnouncedAt < 3500) {
        shouldSuppressRepeat = true;
        this.suppressedRepeatCount++;
      }
    }

    const updatedTrack = {
      key,
      class: obj.class || obj.label || "obstacle",
      distance: dist,
      lane: obj.lane || "center",
      motionState,
      timestamp: now,
      lastAnnouncedAt: shouldSuppressRepeat && prev ? prev.lastAnnouncedAt : now
    };
    this.trackedObjects.set(key, updatedTrack);

    return {
      ...updatedTrack,
      shouldSuppressRepeat
    };
  }

  /**
   * Module 4 & Module 6: Central Navigation Controller 8-Step Continuous Loop Evaluation
   * Combines GPS/heading, planned route, YOLO objects, LiDAR/camera depth, and OCR/scene text.
   */
  evaluateNavigationCycle({
    gps = {},
    route = {},
    yoloObjects = [],
    depthReadings = {},
    ocrSign = null,
    trafficSignal = null,
    now = Date.now()
  } = {}) {
    // Step 1: Read latest location & check sensor reliability (Module 6)
    if (gps.unavailable || (typeof gps.accuracyMeters === "number" && gps.accuracyMeters > 35)) {
      const msg = this.reportSensorLimitation("gps_inaccurate");
      return { action: "sensor_limitation", spoken: msg, priority: 2 };
    }
    if (depthReadings.cameraUnavailable) {
      const msg = this.reportSensorLimitation("camera_unavailable");
      return { action: "sensor_limitation", spoken: msg, priority: 2 };
    }

    // Step 2: Check if destination is reached
    if (route.destinationReached || (typeof route.remainingMeters === "number" && route.remainingMeters <= 1.5 && route.isFinalStep)) {
      this.setNavState("ARRIVED");
      this.setHazardSeverity("SAFE");
      this.dispatchSpeech(CANONICAL_FEEDBACK.destination_reached, 2, HAPTIC_PATTERNS.arrival);
      return {
        action: "destination_reached",
        spoken: CANONICAL_FEEDBACK.destination_reached,
        haptic: HAPTIC_PATTERNS.arrival,
        priority: 2
      };
    }

    // Step 3 & 4: Fuse YOLO object detections with LiDAR / camera depth estimation
    const fusedObjects = (yoloObjects || [])
      .map(obj => {
        const bbox = obj.bbox || [0, 0, 100, 200];
        const centerRatio = bbox[0] !== undefined && bbox[2] !== undefined ? (bbox[0] + bbox[2] / 2) / 640 : 0.5;
        const lane =
          obj.lane ||
          (centerRatio < 0.38 ? "slightly to your left" : centerRatio > 0.62 ? "slightly to your right" : "directly ahead");
        const rawDist =
          typeof obj.distance === "number"
            ? obj.distance
            : typeof depthReadings[obj.class] === "number"
            ? depthReadings[obj.class]
            : typeof depthReadings.defaultDistance === "number"
            ? depthReadings.defaultDistance
            : null;
        // Filter unreliable depth measurements (< 0.25m noise or > 12.0m)
        const reliableDist = rawDist !== null && rawDist >= 0.25 && rawDist <= 12.0 ? rawDist : null;
        return {
          ...obj,
          class: (obj.class || obj.label || "obstacle").toLowerCase(),
          confidence: typeof obj.confidence === "number" ? obj.confidence : 0.9,
          distance: reliableDist,
          depthSource: depthReadings.lidarSupported ? "lidar" : "camera_depth",
          lane
        };
      })
      .filter(o => o.distance !== null)
      .sort((a, b) => a.distance - b.distance);

    // Step 5 & 6: Prioritize immediate nearby obstacles over ordinary route instructions (Module 4)
    const closestHazard = fusedObjects.find(o => o.distance <= 2.2);
    if (closestHazard) {
      // Save ordinary route instruction so we can resume once hazard is resolved
      if (route.nextInstruction) {
        this.pendingRouteInstruction = route.nextInstruction;
      }

      const track = this.trackObjectAcrossFrames(closestHazard, now);
      let warningText = CANONICAL_FEEDBACK.nearby_obstacle;
      if (closestHazard.class.includes("person")) {
        const posDesc =
          closestHazard.lane === "right" || closestHazard.lane === "slightly to your right"
            ? "slightly to your right"
            : closestHazard.lane === "left" || closestHazard.lane === "slightly to your left"
            ? "slightly to your left"
            : "ahead";
        warningText = CANONICAL_FEEDBACK.person_obstacle(posDesc);
      }

      const severity = closestHazard.distance < 0.85 ? "CRITICAL_STOP" : "DANGER";
      this.hazardSeverity = severity;
      if (severity === "CRITICAL_STOP") this.navState = "HAZARD_STOPPED";

      if (!track.shouldSuppressRepeat) {
        this.dispatchSpeech(warningText, 1, HAPTIC_PATTERNS.nearby_obstacle);
      }

      return {
        action: "hazard_priority_override",
        hazard: closestHazard,
        motionState: track.motionState,
        suppressedRepeat: track.shouldSuppressRepeat,
        spoken: warningText,
        haptic: HAPTIC_PATTERNS.nearby_obstacle,
        priority: 1
      };
    }

    // If previous state was hazard-stopped or danger and now path is clear, resume normal route guidance!
    if ((this.hazardSeverity === "DANGER" || this.hazardSeverity === "CRITICAL_STOP") && fusedObjects.length === 0) {
      this.hazardSeverity = "SAFE";
      this.navState = "ACTIVE_WALKING";
      const resumeInstruction = route.nextInstruction || this.pendingRouteInstruction || "Continue straight.";
      const resumeText = `Path clear. ${resumeInstruction}`;
      this.pendingRouteInstruction = null;
      this.dispatchSpeech(resumeText, 2, HAPTIC_PATTERNS.clear_resume);
      return {
        action: "resume_route_guidance",
        spoken: resumeText,
        haptic: HAPTIC_PATTERNS.clear_resume,
        priority: 2
      };
    }

    // Check Module 4 Critical Safety Limitation on traffic signals:
    // Never tell user to cross a road merely because a camera model detects a green light!
    if (trafficSignal && trafficSignal.color === "GREEN") {
      this.dispatchSpeech(CANONICAL_FEEDBACK.green_light_caution, 2, HAPTIC_PATTERNS.caution);
      return {
        action: "traffic_light_caution",
        spoken: CANONICAL_FEEDBACK.green_light_caution,
        haptic: HAPTIC_PATTERNS.caution,
        priority: 2
      };
    }

    // Check Route Deviation (Module 5 & 6)
    if (route.deviatedFromRoute || (typeof route.deviationMeters === "number" && route.deviationMeters > 18)) {
      this.setNavState("REROUTING");
      this.dispatchSpeech(CANONICAL_FEEDBACK.route_deviation, 2, HAPTIC_PATTERNS.route_deviation);
      return {
        action: "route_deviation",
        spoken: CANONICAL_FEEDBACK.route_deviation,
        haptic: HAPTIC_PATTERNS.route_deviation,
        priority: 2
      };
    }

    // Check Uncertain OCR / Sign Detection (Module 4 & 5)
    if (ocrSign && typeof ocrSign.confidence === "number" && ocrSign.confidence < 0.65) {
      this.dispatchSpeech(CANONICAL_FEEDBACK.uncertain_detection, 3, HAPTIC_PATTERNS.caution);
      return {
        action: "uncertain_detection",
        spoken: CANONICAL_FEEDBACK.uncertain_detection,
        haptic: HAPTIC_PATTERNS.caution,
        priority: 3
      };
    }

    // Check Approaching Public Transport Stop (Module 5)
    if (route.approachingTransitStop) {
      const msg = CANONICAL_FEEDBACK.public_transport(route.transitStopType || "tram");
      this.dispatchSpeech(msg, 3, HAPTIC_PATTERNS.caution);
      return {
        action: "public_transport_approaching",
        spoken: msg,
        haptic: HAPTIC_PATTERNS.caution,
        priority: 3
      };
    }

    // Check Upcoming Turn (Module 5)
    if (route.upcomingTurnDirection && typeof route.distanceToTurnMeters === "number" && route.distanceToTurnMeters <= 25) {
      const msg = CANONICAL_FEEDBACK.upcoming_turn(route.upcomingTurnDirection, Math.round(route.distanceToTurnMeters));
      const haptic = route.upcomingTurnDirection === "left" ? HAPTIC_PATTERNS.turn_left : HAPTIC_PATTERNS.turn_right;
      this.dispatchSpeech(msg, 3, haptic);
      return {
        action: "upcoming_turn",
        spoken: msg,
        haptic,
        priority: 3
      };
    }

    // Default routine navigation instruction
    const routineText = route.nextInstruction || CANONICAL_FEEDBACK.navigation_begins;
    return {
      action: "continue_route",
      spoken: routineText,
      haptic: null,
      priority: 4
    };
  }

  setHazardSeverity(severity, details = {}) {
    const prev = this.hazardSeverity;
    this.hazardSeverity = severity;

    if (severity === "CRITICAL_STOP") {
      if (this.navState === "ACTIVE_WALKING") {
        this.navState = "HAZARD_STOPPED";
      }
      this.dispatchSpeech(
        details.message || "STOP! Immediate obstacle ahead. Do not proceed.",
        1,
        HAPTIC_PATTERNS.critical_stop
      );
    } else if (severity === "DANGER") {
      this.dispatchSpeech(
        details.message || CANONICAL_FEEDBACK.nearby_obstacle,
        2,
        HAPTIC_PATTERNS.nearby_obstacle
      );
    } else if (severity === "CAUTION") {
      this.dispatchSpeech(
        details.message || "Obstacle nearby. Keep center path.",
        2,
        HAPTIC_PATTERNS.caution
      );
    } else if (prev === "CRITICAL_STOP" && severity === "SAFE") {
      if (this.navState === "HAZARD_STOPPED") {
        this.navState = "ACTIVE_WALKING";
        this.dispatchSpeech(
          "Obstacle cleared. Path is safe ahead. Resuming walking route.",
          2,
          HAPTIC_PATTERNS.clear_resume
        );
      }
    }

    this.notifyListeners("hazard_changed", { previous: prev, current: severity, details });
    return this.hazardSeverity;
  }

  setNavState(newState) {
    const prev = this.navState;
    this.navState = newState;
    this.notifyListeners("nav_state_changed", { previous: prev, current: newState });
    return this.navState;
  }

  dispatchSpeech(text, priority = 3, hapticPattern = null) {
    if (!text) return false;

    if (hapticPattern && Array.isArray(hapticPattern)) {
      this.hapticHistory.push({ pattern: hapticPattern, timestamp: Date.now() });
    }

    // Module 5: Prioritize safety-critical warnings over routine navigation or long scene descriptions
    if (this.hazardSeverity === "CRITICAL_STOP" && priority > 2) {
      this.notifyListeners("speech_suppressed", { text, priority, reason: "CRITICAL_STOP" });
      return false;
    }

    const now = Date.now();
    // Preempt ongoing lower-priority routine speech when a higher-priority safety alert arrives
    if (priority <= 2 && this.activePriority > 2) {
      this.notifyListeners("speech_preempted", {
        preemptedText: this.lastSpeechText,
        newText: text,
        newPriority: priority
      });
    } else if (this.lastSpeechText === text && now - this.lastSpeechTime < 2800) {
      // Rate limit duplicate exact speech within 2.8s
      return false;
    }

    this.lastSpeechText = text;
    this.lastSpeechTime = now;
    this.activePriority = priority;
    this.speechHistory.push({ text, priority, timestamp: now });

    this.notifyListeners("speech_dispatched", { text, priority });
    return true;
  }

  reset() {
    this.hazardSeverity = "SAFE";
    this.navState = "IDLE";
    this.activePriority = 4;
    this.lastSpeechText = "";
    this.lastSpeechTime = 0;
    this.speechHistory = [];
    this.hapticHistory = [];
    this.trackedObjects.clear();
    this.suppressedRepeatCount = 0;
    this.pendingRouteInstruction = null;
    for (const info of Object.values(this.sensorFreshness)) {
      info.timestamp = 0;
      info.isStale = true;
    }
  }
}

// Singleton and Class exports
const safetyEngineInstance = new UnifiedSafetyEngine();

if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    UnifiedSafetyEngine,
    safetyEngine: safetyEngineInstance,
    CANONICAL_FEEDBACK,
    HAPTIC_PATTERNS
  };
}
