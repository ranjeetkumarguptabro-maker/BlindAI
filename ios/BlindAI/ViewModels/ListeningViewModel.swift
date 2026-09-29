import SwiftUI
import Combine

@MainActor
public final class ListeningViewModel: ObservableObject, SpeechServiceDelegate {
    @Published public var suggestedCommands: [String] = [
        "\"Take me to CIF\"",
        "\"What's in front of me?\"",
        "\"Where am I?\""
    ]
    @Published public var transcript: String = ""
    @Published public var audioLevel: Float = 0.0
    @Published public var statusMessage: String = "Listening..."
    
    public var onNavigateToRoute: ((AppRoute) -> Void)?
    
    private let speechService = SpeechService.shared
    private let navService = NavigationService.shared
    private let envService = EnvironmentService.shared
    private let hapticsService = HapticsService.shared
    
    public init(onNavigateToRoute: ((AppRoute) -> Void)? = nil) {
        self.onNavigateToRoute = onNavigateToRoute
        self.speechService.delegate = self
    }
    
    public func onAppear() {
        speechService.delegate = self
        transcript = ""
        statusMessage = "Listening..."
        hapticsService.impact(style: .medium)
        speechService.startListening()
    }
    
    public func onDisappear() {
        speechService.stopListening()
    }
    
    public func handleCommandSelected(_ command: String) {
        hapticsService.selection()
        let intent = speechService.parseIntent(from: command)
        executeIntent(intent)
    }
    
    public func handleStopTapped() {
        hapticsService.impact(style: .heavy)
        speechService.stopListening()
        onNavigateToRoute?(.home)
    }
    
    // MARK: - SpeechServiceDelegate
    nonisolated public func speechService(_ service: SpeechServiceProtocol, didUpdateTranscription text: String) {
        Task { @MainActor in
            self.transcript = text
        }
    }
    
    nonisolated public func speechService(_ service: SpeechServiceProtocol, didUpdateAudioLevel level: Float) {
        Task { @MainActor in
            self.audioLevel = level
        }
    }
    
    nonisolated public func speechService(_ service: SpeechServiceProtocol, didDetectIntent intent: VoiceIntent) {
        Task { @MainActor in
            self.executeIntent(intent)
        }
    }
    
    private func executeIntent(_ intent: VoiceIntent) {
        speechService.stopListening()
        
        switch intent {
        case .startNavigation(let destination):
            statusMessage = "Starting route to \(destination)..."
            navService.startRoute()
            onNavigateToRoute?(.activeNavigation)
            
        case .describeEnvironment:
            envService.describeEnvironment { [weak self] desc in
                self?.speechService.speak(desc)
                self?.onNavigateToRoute?(.home)
            }
            
        case .whereAmI:
            envService.queryWhereAmI { [weak self] loc in
                self?.speechService.speak(loc)
                self?.onNavigateToRoute?(.home)
            }
            
        case .stop:
            onNavigateToRoute?(.home)
            
        case .repeatInstruction:
            navService.repeatInstruction()
            
        case .unknown(let query):
            speechService.speak("Understood: \(query). Processing command.")
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.2) {
                self.onNavigateToRoute?(.home)
            }
        }
    }
}
