import SwiftUI
import Combine

@MainActor
public final class DescribeAroundViewModel: ObservableObject {
    @Published public var items: [EnvironmentSceneItem] = EnvironmentSceneItem.defaultRigaScene
    @Published public var isSpeaking: Bool = false
    @Published public var isLoading: Bool = false
    
    public var onNavigateToRoute: ((AppRoute) -> Void)?
    
    private let speechService = SpeechService.shared
    private let hapticsService = HapticsService.shared
    private let backendClient = BlindAIBackendClient.shared
    
    public init(onNavigateToRoute: ((AppRoute) -> Void)? = nil) {
        self.onNavigateToRoute = onNavigateToRoute
    }
    
    public func handleOnAppear() {
        speakSceneSummary()
    }
    
    public func speakSceneSummary() {
        hapticsService.impact(style: .medium)
        isSpeaking = true
        let summary = "Here's what I see: Sidewalk ahead is clear. Riga Technical University main entrance on the left. Bicycle rack 3 meters ahead on right. People walking nearby. It is sunny and bright."
        speechService.speak(summary)
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 4.0) { [weak self] in
            self?.isSpeaking = false
        }
    }
    
    public func repeatSpokenSummary() {
        speakSceneSummary()
    }
    
    public func handleBackTapped() {
        hapticsService.impact(style: .light)
        speechService.stop()
        onNavigateToRoute?(.home)
    }
    
    public func handleSettingsTapped() {
        hapticsService.selection()
        speechService.speak("Settings. Vision analysis detail level is set to High.")
    }
}
