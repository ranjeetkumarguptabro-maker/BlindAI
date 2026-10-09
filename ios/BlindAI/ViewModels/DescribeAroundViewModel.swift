import SwiftUI
import Combine

@MainActor
public final class DescribeAroundViewModel: ObservableObject {
    @Published public var items: [EnvironmentSceneItem] = []
    @Published public var liveSceneDescription: String = "Analyzing real-time camera view..."
    @Published public var isSpeaking: Bool = false
    @Published public var isLoading: Bool = false
    
    public var onNavigateToRoute: ((AppRoute) -> Void)?
    
    private let speechService = SpeechService.shared
    private let hapticsService = HapticsService.shared
    private let backendClient = BlindAIBackendClient.shared
    private let cameraService = CameraCaptureService.shared
    private let perceptionService = RealtimeVisionPerceptionService.shared
    
    public init(onNavigateToRoute: ((AppRoute) -> Void)? = nil) {
        self.onNavigateToRoute = onNavigateToRoute
    }
    
    public func handleOnAppear() {
        scanLiveEnvironment()
    }
    
    public func scanLiveEnvironment() {
        hapticsService.impact(style: .medium)
        isLoading = true
        speechService.speak("Scanning camera view to describe your surroundings...")
        
        Task {
            let desc = await perceptionService.performInstantSceneScan()
            self.liveSceneDescription = desc
            self.buildDynamicSceneItems(from: desc)
            self.isLoading = false
            self.isSpeaking = true
            
            DispatchQueue.main.asyncAfter(deadline: .now() + 4.0) { [weak self] in
                self?.isSpeaking = false
            }
        }
    }
    
    private func buildDynamicSceneItems(from text: String) {
        var newItems: [EnvironmentSceneItem] = []
        
        // 1. Path clearance item
        let hasHazard = /obstacle|hazard|danger|careful|curb|step|stairs|car|barrier/i
        if text.contains(hasHazard) {
            newItems.append(EnvironmentSceneItem(
                id: "item-hazard",
                title: "Obstacle / Hazard detected ahead",
                subtitle: "Proceed with caution",
                iconName: "exclamationmark.triangle.fill",
                iconColor: .red,
                iconBackground: Color.red.opacity(0.15)
            ))
        } else {
            newItems.append(EnvironmentSceneItem(
                id: "item-clear",
                title: "Sidewalk ahead is clear",
                subtitle: "Safe to continue forward",
                iconName: "checkmark.circle.fill",
                iconColor: .green,
                iconBackground: Color.green.opacity(0.15)
            ))
        }
        
        // 2. Main scene description item
        newItems.append(EnvironmentSceneItem(
            id: "item-scene",
            title: "Scene Summary",
            subtitle: text,
            iconName: "eye.fill",
            iconColor: Color(red: 70/255, green: 135/255, blue: 245/255),
            iconBackground: Color(red: 235/255, green: 244/255, blue: 255/255)
        ))
        
        // 3. Real detected objects from YOLO
        for (idx, obj) in perceptionService.detectedObjects.prefix(3).enumerated() {
            newItems.append(EnvironmentSceneItem(
                id: "obj-\(idx)",
                title: "\(obj.label) (\(String(format: "%.1f", obj.distanceMeters))m ahead)",
                subtitle: "Position: \(obj.lane.rawValue)",
                iconName: "cube.fill",
                iconColor: .orange,
                iconBackground: Color.orange.opacity(0.15)
            ))
        }
        
        self.items = newItems
    }
    
    public func repeatSpokenSummary() {
        hapticsService.impact(style: .medium)
        speechService.speak(liveSceneDescription)
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
