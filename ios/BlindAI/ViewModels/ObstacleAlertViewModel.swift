import SwiftUI
import Combine

@MainActor
public final class ObstacleAlertViewModel: ObservableObject {
    @Published public var hazard: ObstacleAlertItem = ObstacleAlertItem.defaultHazard
    @Published public var isAcknowledged: Bool = false
    
    public var onNavigateToRoute: ((AppRoute) -> Void)?
    public var onObstacleAcknowledged: (() -> Void)?
    
    private let speechService = SpeechService.shared
    private let hapticsService = HapticsService.shared
    
    public init(
        hazard: ObstacleAlertItem = ObstacleAlertItem.defaultHazard,
        onNavigateToRoute: ((AppRoute) -> Void)? = nil
    ) {
        self.hazard = hazard
        self.onNavigateToRoute = onNavigateToRoute
    }
    
    public func handleOnAppear() {
        // Announce obstacle distance first, then object and side as specified in requirements
        hapticsService.warning()
        speechService.speak("Obstacle ahead. Two meters ahead, construction barrier on right.")
    }
    
    public func repeatAlert() {
        hapticsService.impact(style: .medium)
        speechService.speak("Two meters ahead, construction barrier on right. Stay on the left.")
    }
    
    public func acknowledgeObstacle() {
        hapticsService.success()
        isAcknowledged = true
        speechService.speak("Obstacle acknowledged. Resuming path.")
        onObstacleAcknowledged?()
        
        // Log event to backend
        Task {
            _ = try? await BlindAIBackendClient.shared.logObstacleEvent(
                type: self.hazard.type,
                lane: "right",
                distanceMeters: self.hazard.distanceMeters,
                severity: "warning"
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
        onNavigateToRoute?(.activeNavigation)
    }
    
    public func handleSettingsTapped() {
        hapticsService.selection()
        speechService.speak("Obstacle detection sensitivity: High. Voice alerts: Enabled.")
    }
}
