import SwiftUI
import Combine

@MainActor
public final class CrosswalkSafetyViewModel: ObservableObject {
    @Published public var crossing: CrosswalkStatusItem = CrosswalkStatusItem.defaultCrossing
    @Published public var isWaveformPulsing: Bool = true
    @Published public var isCrossingComplete: Bool = false
    
    public var onNavigateToRoute: ((AppRoute) -> Void)?
    public var onCrosswalkFinished: (() -> Void)?
    
    private let speechService = SpeechService.shared
    private let hapticsService = HapticsService.shared
    
    public init(
        crossing: CrosswalkStatusItem = CrosswalkStatusItem.defaultCrossing,
        onNavigateToRoute: ((AppRoute) -> Void)? = nil
    ) {
        self.crossing = crossing
        self.onNavigateToRoute = onNavigateToRoute
    }
    
    public func handleOnAppear() {
        // As per spec Section 8:
        // Crosswalk detected -> "Approaching crosswalk. Listen for traffic." -> AUTOMATIC SILENCE
        hapticsService.impact(style: .heavy)
        speechService.speak("Approaching crosswalk. Listen for traffic.")
    }
    
    public func repeatNotice() {
        hapticsService.impact(style: .medium)
        speechService.speak("Approaching crosswalk. Pedestrian signal is green. I will be quiet while you cross.")
    }
    
    public func confirmCrossed() {
        hapticsService.success()
        isCrossingComplete = true
        speechService.speak("Crosswalk completed. Resuming route.")
        onCrosswalkFinished?()
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) { [weak self] in
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
        speechService.speak("Crosswalk safety mode: Automatic quiet enabled.")
    }
}
