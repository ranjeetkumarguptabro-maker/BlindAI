import Foundation
import Combine
import SwiftUI

/// ObstacleDangerSystem evaluates distance, direction, walking corridor intersection, and movement
/// to decide safety risk levels and trigger voice/haptic alerts without overwhelming the user.
public final class ObstacleDangerSystem: ObservableObject {
    public static let shared = ObstacleDangerSystem()
    
    @Published public private(set) var activeHazard: ObstacleAlertItem?
    @Published public private(set) var dangerLevel: DetectedObstacle.DangerLevel = .safe
    @Published public private(set) var lastSpokenAlert: String = ""
    @Published public private(set) var isAlertActive: Bool = false
    
    // Services
    private let speechService = SpeechService.shared
    private let hapticsService = HapticsService.shared
    
    // Rate-limiting / Cooldown to prevent auditory overload
    private var lastAnnouncementTime: Date = Date.distantPast
    private let alertCooldownSeconds: TimeInterval = 3.2
    private var lastAnnouncedDistance: Float = 999.0
    private var lastAnnouncedLabel: String = ""
    
    // Configurable Distance Thresholds (meters)
    public var criticalStopDistance: Float = 0.75  // < 0.75m: Immediate STOP
    public var dangerDistance: Float = 1.4         // ~1.0m: Obstacle ahead, 1 meter
    public var cautionDistance: Float = 2.4        // ~2.0m: [Object] ahead, 2 meters
    public var noticeDistance: Float = 3.4         // ~3.0m: Object ahead
    
    public init() {
        setupSubscriptions()
    }
    
    private func setupSubscriptions() {
        ARKitLiDARScannerService.shared.onObstacleDetected = { [weak self] obstacle in
            self?.processDetectedObstacle(obstacle)
        }
        
        ARKitLiDARScannerService.shared.onCriticalHazard = { [weak self] obstacle in
            self?.triggerCriticalEmergencyAlert(for: obstacle)
        }
    }
    
    /// Processes a detected obstacle through the safety rule pipeline
    public func processDetectedObstacle(_ obstacle: DetectedObstacle) {
        let now = Date()
        let distance = obstacle.distanceMeters
        let lane = obstacle.lane
        let label = obstacle.label
        
        // 1. Evaluate Danger Level
        let evaluatedLevel: DetectedObstacle.DangerLevel
        if lane == .center {
            if distance < criticalStopDistance {
                evaluatedLevel = .critical
            } else if distance < dangerDistance {
                evaluatedLevel = .danger
            } else if distance < cautionDistance {
                evaluatedLevel = .caution
            } else if distance < noticeDistance {
                evaluatedLevel = .notice
            } else {
                evaluatedLevel = .safe
            }
        } else {
            // Beside path (left or right)
            if distance < 1.0 {
                evaluatedLevel = .caution
            } else if distance < 2.0 {
                evaluatedLevel = .notice
            } else {
                // 4m beside path: silent
                evaluatedLevel = .safe
            }
        }
        
        DispatchQueue.main.async {
            self.dangerLevel = evaluatedLevel
        }
        
        // 2. Critical Alert (< 0.7m) immediately bypasses cooldown
        if evaluatedLevel == .critical {
            triggerCriticalEmergencyAlert(for: obstacle)
            return
        }
        
        // 3. Check cooldown & deduplication
        let timeSinceLastAlert = now.timeIntervalSince(lastAnnouncementTime)
        let distanceDelta = abs(distance - lastAnnouncedDistance)
        let isEscalating = distance < lastAnnouncedDistance && distanceDelta > 0.6
        
        // Only announce if cooldown expired or hazard is rapidly approaching
        guard timeSinceLastAlert > alertCooldownSeconds || isEscalating else {
            return
        }
        
        // 4. Formulate Spoken & Haptic Alert according to specification
        switch evaluatedLevel {
        case .danger:
            // ~1 meter ahead
            let spoken = "Obstacle ahead, 1 meter."
            emitAlert(
                message: spoken,
                haptic: .warning,
                obstacle: obstacle,
                title: "Obstacle ahead",
                subtitle: "1 meter ahead in walking path",
                guidance: lane == .left ? "Keep right." : "Keep left."
            )
            
        case .caution:
            // ~2 meters ahead
            let side = lane == .center ? "ahead" : (lane == .left ? "ahead on your left" : "ahead on your right")
            let roundedDist = Int(round(distance))
            let distWord = roundedDist <= 1 ? "1 meter" : "\(roundedDist) meters"
            let guidance = lane == .left ? "Keep right." : (lane == .right ? "Keep left." : "Slow down or veer slightly right.")
            let spoken = "\(label) \(side), \(distWord). \(guidance)"
            
            emitAlert(
                message: spoken,
                haptic: .medium,
                obstacle: obstacle,
                title: "\(label) ahead",
                subtitle: "\(distWord) ahead, \(side)",
                guidance: guidance
            )
            
        case .notice:
            // ~3 meters ahead
            let spoken = "\(label) ahead, 3 meters."
            emitAlert(
                message: spoken,
                haptic: .light,
                obstacle: obstacle,
                title: "Object ahead",
                subtitle: "\(label) 3 meters ahead",
                guidance: "Corridor clear for 2 meters."
            )
            
        case .safe:
            // Beside path / 4m away: silent
            break
        case .critical:
            break
        }
    }
    
    /// Triggers immediate high-priority STOP alert for critical proximity
    public func triggerCriticalEmergencyAlert(for obstacle: DetectedObstacle) {
        lastAnnouncementTime = Date()
        lastAnnouncedDistance = obstacle.distanceMeters
        lastAnnouncedLabel = obstacle.label
        
        let emergencyMessage = "Stop. Obstacle directly ahead."
        
        DispatchQueue.main.async {
            self.dangerLevel = .critical
            self.isAlertActive = true
            self.lastSpokenAlert = emergencyMessage
            
            self.activeHazard = ObstacleAlertItem(
                type: obstacle.label,
                distanceMeters: Double(obstacle.distanceMeters),
                distanceText: "Critical proximity",
                sideText: "directly ahead",
                title: "Stop. Obstacle directly ahead",
                subtitle: "\(obstacle.label) less than 0.7 meters ahead.",
                guidance: "Halt immediately. Clear path before proceeding.",
                cardTitle: obstacle.label,
                cardSubtitle: "Direct collision path (<0.7m)"
            )
        }
        
        // Immediate emergency haptics and speech preemption
        hapticsService.notification(type: .error)
        hapticsService.impact(style: .heavy)
        speechService.stop()
        speechService.speak(emergencyMessage)
    }
    
    private func emitAlert(
        message: String,
        haptic: HapticStyle,
        obstacle: DetectedObstacle,
        title: String,
        subtitle: String,
        guidance: String
    ) {
        lastAnnouncementTime = Date()
        lastAnnouncedDistance = obstacle.distanceMeters
        lastAnnouncedLabel = obstacle.label
        
        DispatchQueue.main.async {
            self.isAlertActive = true
            self.lastSpokenAlert = message
            
            self.activeHazard = ObstacleAlertItem(
                type: obstacle.label,
                distanceMeters: Double(obstacle.distanceMeters),
                distanceText: "\(Int(round(obstacle.distanceMeters))) meters ahead",
                sideText: obstacle.lane == .left ? "on left" : (obstacle.lane == .right ? "on right" : "ahead"),
                title: title,
                subtitle: subtitle,
                guidance: guidance,
                cardTitle: obstacle.label,
                cardSubtitle: "\(Int(round(obstacle.distanceMeters)))m ahead (\(obstacle.lane.rawValue))"
            )
        }
        
        switch haptic {
        case .heavy:
            hapticsService.impact(style: .heavy)
        case .warning:
            hapticsService.warning()
        case .medium:
            hapticsService.impact(style: .medium)
        case .light:
            hapticsService.impact(style: .light)
        }
        
        speechService.speak(message)
    }
    
    public enum HapticStyle {
        case light, medium, heavy, warning
    }
    
    /// Resets active alert state when user acknowledges or obstacle clears
    public func clearActiveAlert() {
        DispatchQueue.main.async {
            self.isAlertActive = false
            self.activeHazard = nil
            self.dangerLevel = .safe
        }
    }
}
