import SwiftUI
import Combine

@MainActor
public final class WhereAmIViewModel: ObservableObject {
    @Published public var locationHeadline: String = "You are at Riga Technical University (RTU), Ķīpsala Campus in Riga, Latvia."
    @Published public var locationDetails: String = "You are facing east, near the main entrance of the RTU Ķīpsala campus. The Daugava river is on your right and Vanšu tilts (bridge) is behind you."
    @Published public var isUpdating: Bool = false
    
    public var onNavigateToRoute: ((AppRoute) -> Void)?
    
    private let speechService = SpeechService.shared
    private let hapticsService = HapticsService.shared
    
    public init(onNavigateToRoute: ((AppRoute) -> Void)? = nil) {
        self.onNavigateToRoute = onNavigateToRoute
    }
    
    public var spokenAnnouncement: String {
        "\(locationHeadline) \(locationDetails)"
    }
    
    public func handleUpdateLocation() {
        hapticsService.impact(style: .medium)
        isUpdating = true
        speechService.speak("Updating your current location...")
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.2) { [weak self] in
            guard let self = self else { return }
            self.isUpdating = false
            self.hapticsService.notification(type: .success)
            self.speechService.speak("Location confirmed. You are at Riga Technical University, Ķīpsala Campus, facing east.")
        }
    }
    
    public func handleShowOnMap() {
        hapticsService.impact(style: .medium)
        onNavigateToRoute?(.routePreview)
    }
    
    public func handleBack() {
        hapticsService.selection()
        onNavigateToRoute?(.home)
    }
}
