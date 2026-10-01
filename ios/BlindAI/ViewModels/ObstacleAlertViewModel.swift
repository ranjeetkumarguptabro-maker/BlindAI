import SwiftUI
import Combine

@MainActor
public final class ObstacleAlertViewModel: ObservableObject {
    @Published public var hazard: ObstacleAlertItem = ObstacleAlertItem.defaultHazard
    @Published public var isAcknowledged: Bool = false
    @Published public var dangerLevel: DetectedObstacle.DangerLevel = .danger
    
    public var onNavigateToRoute: ((AppRoute) -> Void)?
    public var onObstacleAcknowledged: (() -> Void)?
    
    private let speechService = SpeechService.shared
    private let hapticsService = HapticsService.shared
    private let dangerSystem = ObstacleDangerSystem.shared
    private var cancellables = Set<AnyCancellable>()
    
    public init(
        hazard: ObstacleAlertItem = ObstacleAlertItem.defaultHazard,
        onNavigateToRoute: ((AppRoute) -> Void)? = nil
    ) {
        self.hazard = hazard
        self.onNavigateToRoute = onNavigateToRoute
        bindDangerSystem()
    }
    
    private func bindDangerSystem() {
        dangerSystem.$activeHazard
            .receive(on: DispatchQueue.main)
            .compactMap { $0 }
            .sink { [weak self] newHazard in
                self?.hazard = newHazard
                self?.isAcknowledged = false
            }
            .store(in: &cancellables)
            
        dangerSystem.$dangerLevel
            .receive(on: DispatchQueue.main)
            .sink { [weak self] level in
                self?.dangerLevel = level
            }
            .store(in: &cancellables)
    }
    
    public func handleOnAppear() {
        // Announce obstacle distance, object, and guidance
        if dangerLevel == .critical {
            hapticsService.notification(type: .error)
            hapticsService.impact(style: .heavy)
            speechService.speak("Stop. Obstacle directly ahead.")
        } else {
            hapticsService.warning()
            let announcement = "\(hazard.title). \(hazard.subtitle) \(hazard.guidance)"
            speechService.speak(announcement)
        }
    }
    
    public func repeatAlert() {
        hapticsService.impact(style: .medium)
        let alertText = "\(hazard.subtitle). \(hazard.guidance)"
        speechService.speak(alertText)
    }
    
    public func acknowledgeObstacle() {
        hapticsService.success()
        isAcknowledged = true
        dangerSystem.clearActiveAlert()
        speechService.speak("Obstacle acknowledged. Resuming path.")
        onObstacleAcknowledged?()
        
        // Log event to backend
        Task {
            _ = try? await BlindAIBackendClient.shared.logObstacleEvent(
                type: self.hazard.type,
                lane: self.hazard.sideText,
                distanceMeters: self.hazard.distanceMeters,
                severity: self.dangerLevel.rawValue
            )
        }
        
        // Return to active navigation
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) { [weak self] in
            self?.onNavigateToRoute?(.activeNavigation)
        }
    }
    
    public func handleBackTapped() {
        hapticsService.impact(style: .light)
        speechService.stop()
        dangerSystem.clearActiveAlert()
        onNavigateToRoute?(.activeNavigation)
    }
    
    public func handleSettingsTapped() {
        hapticsService.selection()
        speechService.speak("Obstacle detection sensitivity: High. LiDAR frame semantics: sceneDepth active. Voice alerts: Enabled.")
    }
}
