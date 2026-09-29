import SwiftUI
import Combine

@MainActor
public final class HomeViewModel: ObservableObject {
    @Published public var actionItems: [ActionCardType] = [
        .startNavigation,
        .describeAround,
        .whereAmI
    ]
    @Published public var statusToast: String? = nil
    @Published public var isShowingSettings: Bool = false
    
    public var onNavigateToRoute: ((AppRoute) -> Void)?
    
    private let speechService = SpeechService.shared
    private let envService = EnvironmentService.shared
    private let hapticsService = HapticsService.shared
    
    public init(onNavigateToRoute: ((AppRoute) -> Void)? = nil) {
        self.onNavigateToRoute = onNavigateToRoute
    }
    
    public func handleCardSelection(_ item: ActionCardType) {
        switch item {
        case .startNavigation:
            hapticsService.impact(style: .medium)
            speechService.speak("Where would you like to go?")
            onNavigateToRoute?(.destinationSearch)
            
        case .describeAround:
            hapticsService.impact(style: .medium)
            speechService.speak("Analyzing what is around you.")
            onNavigateToRoute?(.describeAround)
            
        case .whereAmI:
            hapticsService.impact(style: .medium)
            speechService.speak("Opening current location details.")
            onNavigateToRoute?(.whereAmI)
        }
    }
    
    public func handleMicrophoneTapped() {
        hapticsService.impact(style: .heavy)
        onNavigateToRoute?(.listening)
    }
    
    public func handleSettingsTapped() {
        hapticsService.selection()
        isShowingSettings = true
        speechService.speak("Settings opened. Voice guidance standard mode.")
    }
    
    public func dismissToast() {
        statusToast = nil
    }
}
