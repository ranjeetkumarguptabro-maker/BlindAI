/**
 * UnifiedSafetyEngine.js
 * 
 * Pillar 3: One Unified Safety Engine
 * Single source of truth for hazard severity, sensor freshness, navigation state,
 * and prioritized audio/haptic output dispatch.
 */

class UnifiedSafetyEngine {
  constructor() {
    this.hazardSeverity = 'SAFE'; // 'SAFE' | 'NOTICE' | 'CAUTION' | 'DANGER' | 'CRITICAL_STOP'
    this.navState = 'IDLE'; // 'IDLE' | 'LISTENING' | 'ROUTING' | 'ACTIVE_WALKING' | 'APPROACHING_CROSSWALK' | 'HAZARD_STOPPED' | 'EMERGENCY_SOS'
    
    this.sensorFreshness = {
      camera: { timestamp: 0, isStale: true, maxAgeMs: 1500 },
      gps: { timestamp: 0, isStale: true, maxAgeMs: 12000 },
      imu: { timestamp: 0, isStale: true, maxAgeMs: 1200 },
      lidar: { timestamp: 0, isStale: true, maxAgeMs: 800 }
    };
    
    this.activePriority = 4;
    this.lastSpeechText = '';
    this.lastSpeechTime = 0;
    this.speechHistory = [];
    this.hapticHistory = [];
    this.listeners = [];
  }

  addListener(listener) {
    if (typeof listener === 'function') {
      this.listeners.push(listener);
    }
  }

  notifyListeners(event, data) {
    this.listeners.forEach(fn => {
      try {
        fn(event, data);
      } catch (err) {
        console.warn('[SafetyEngine] Listener error:', err);
      }
    });
  }

  updateSensor(sensorName, timestamp = Date.now()) {
    if (this.sensorFreshness[sensorName]) {
      this.sensorFreshness[sensorName].timestamp = timestamp;
      this.sensorFreshness[sensorName].isStale = false;
      this.notifyListeners('sensor_updated', { sensor: sensorName, timestamp });
    }
  }

  checkFreshness(currentTime = Date.now()) {
    for (const [name, info] of Object.entries(this.sensorFreshness)) {
      if (info.timestamp === 0 || (currentTime - info.timestamp > info.maxAgeMs)) {
        info.isStale = true;
      }
    }
    return { ...this.sensorFreshness };
  }

  setHazardSeverity(severity, details = {}) {
    const prev = this.hazardSeverity;
    this.hazardSeverity = severity;

    if (severity === 'CRITICAL_STOP') {
      if (this.navState === 'ACTIVE_WALKING') {
        this.navState = 'HAZARD_STOPPED';
      }
      this.dispatchSpeech(
        details.message || "STOP! Immediate obstacle ahead. Do not proceed.",
        1,
        [200, 100, 200, 100, 400]
      );
    } else if (severity === 'DANGER') {
      this.dispatchSpeech(
        details.message || "Caution! Hazard detected in path.",
        2,
        [150, 80, 150]
      );
    } else if (severity === 'CAUTION') {
      this.dispatchSpeech(
        details.message || "Obstacle nearby. Keep center path.",
        2,
        [80, 60]
      );
    } else if (prev === 'CRITICAL_STOP' && severity === 'SAFE') {
      if (this.navState === 'HAZARD_STOPPED') {
        this.navState = 'ACTIVE_WALKING';
        this.dispatchSpeech(
          "Obstacle cleared. Path is safe ahead. Resuming walking route.",
          2,
          [100]
        );
      }
    }

    this.notifyListeners('hazard_changed', { previous: prev, current: severity, details });
    return this.hazardSeverity;
  }

  setNavState(newState) {
    const prev = this.navState;
    this.navState = newState;
    this.notifyListeners('nav_state_changed', { previous: prev, current: newState });
    return this.navState;
  }

  dispatchSpeech(text, priority = 3, hapticPattern = null) {
    if (!text) return false;

    if (hapticPattern && Array.isArray(hapticPattern)) {
      this.hapticHistory.push({ pattern: hapticPattern, timestamp: Date.now() });
    }

    // Suppress lower-priority speech when in CRITICAL_STOP
    if (this.hazardSeverity === 'CRITICAL_STOP' && priority > 2) {
      this.notifyListeners('speech_suppressed', { text, priority, reason: 'CRITICAL_STOP' });
      return false;
    }

    const now = Date.now();
    // Rate limit duplicate exact speech within 2.8s
    if (this.lastSpeechText === text && (now - this.lastSpeechTime < 2800)) {
      return false;
    }

    this.lastSpeechText = text;
    this.lastSpeechTime = now;
    this.activePriority = priority;
    this.speechHistory.push({ text, priority, timestamp: now });

    this.notifyListeners('speech_dispatched', { text, priority });
    return true;
  }

  reset() {
    this.hazardSeverity = 'SAFE';
    this.navState = 'IDLE';
    this.activePriority = 4;
    this.lastSpeechText = '';
    this.lastSpeechTime = 0;
    this.speechHistory = [];
    this.hapticHistory = [];
    for (const info of Object.values(this.sensorFreshness)) {
      info.timestamp = 0;
      info.isStale = true;
    }
  }
}

// Singleton and Class exports
const safetyEngineInstance = new UnifiedSafetyEngine();

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    UnifiedSafetyEngine,
    safetyEngine: safetyEngineInstance
  };
}
