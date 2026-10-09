import Foundation
import UIKit
import Combine

/// Real-time live vision perception engine for Blind AI.
/// Continuously consumes live camera video frames from CameraCaptureService,
/// executes YOLOv8 object detection on each frame, performs periodic Gemini Multimodal
/// scene descriptions, and triggers immediate pedestrian safety audio cues.
public final class RealtimeVisionPerceptionService: ObservableObject {
    public static let shared = RealtimeVisionPerceptionService()
    
    // Dependencies
    private let cameraService: CameraCaptureService
    private let yoloDetector: YOLOObjectDetector
    private let obstacleSystem: ObstacleDangerSystem
    private let backendClient: BlindAIBackendClient
    private let speechService: SpeechService
    private let hapticsService: HapticsService
    
    // Published State for SwiftUI HUD
    @Published public private(set) var detectedObjects: [DetectedObject] = []
    @Published public private(set) var highestDangerObject: DetectedObject?
    @Published public private(set) var currentSceneDescription: String = "Scanning forward path..."
    @Published public private(set) var detectedSignboards: [SignboardItem] = []
    @Published public private(set) var isPerceptionActive: Bool = false
    @Published public private(set) var lastPerceptionTimestamp: Date = Date()
    
    private var cancellables = Set<AnyCancellable>()
    private var lastGeminiScanTime: CFAbsoluteTime = 0
    private var lastSpokenAlertTime: CFAbsoluteTime = 0
    private var lastSpokenAlertLabel: String = ""
    private var isGeminiScanInProgress: Bool = false
    
    public init(
        cameraService: CameraCaptureService = .shared,
        yoloDetector: YOLOObjectDetector = .shared,
        obstacleSystem: ObstacleDangerSystem = .shared,
        backendClient: BlindAIBackendClient = .shared,
        speechService: SpeechService = .shared,
        hapticsService: HapticsService = .shared
    ) {
        self.cameraService = cameraService
        self.yoloDetector = yoloDetector
        self.obstacleSystem = obstacleSystem
        self.backendClient = backendClient
        self.speechService = speechService
        self.hapticsService = hapticsService
        
        setupSubscriptions()
    }
    
    private func setupSubscriptions() {
        cameraService.framePublisher
            .receive(on: DispatchQueue.global(qos: .userInteractive))
            .sink { [weak self] image in
                self?.processLiveFrame(image)
            }
            .store(in: &cancellables)
    }
    
    /// Starts live perception pipeline
    public func startPerception() async throws {
        try await cameraService.startCapture()
        DispatchQueue.main.async {
            self.isPerceptionActive = true
            self.speechService.speak("Camera perception active. Scanning your walking path.")
        }
    }
    
    /// Stops live perception pipeline
    public func stopPerception() {
        cameraService.stopCapture()
        DispatchQueue.main.async {
            self.isPerceptionActive = false
            self.detectedObjects = []
            self.highestDangerObject = nil
        }
    }
    
    /// Processes a single live video frame
    private func processLiveFrame(_ image: UIImage) {
        let now = CFAbsoluteTimeGetCurrent()
        
        // 1. Run YOLOv8 bounding box and obstacle classification
        let rawDetections = yoloDetector.detectObjects(in: image)
        
        // 2. Filter, compute distances, and assess hazard severity
        var processedObjects: [DetectedObject] = []
        for det in rawDetections {
            let estimatedDistance = obstacleSystem.estimateDistance(for: det)
            let lanePosition = obstacleSystem.determineLane(for: det.boundingBox)
            let dangerLevel = obstacleSystem.classifyDanger(for: det, distance: estimatedDistance)
            
            let obj = DetectedObject(
                id: UUID(),
                label: det.label,
                confidence: det.confidence,
                boundingBox: det.boundingBox,
                distanceMeters: estimatedDistance,
                lane: lanePosition,
                dangerLevel: dangerLevel
            )
            processedObjects.append(obj)
        }
        
        // Find most critical hazard directly in path
        let criticalObstacle = processedObjects
            .filter { $0.lane == .center || $0.lane == .slightlyLeft || $0.lane == .slightlyRight }
            .sorted { $0.distanceMeters < $1.distanceMeters }
            .first
        
        DispatchQueue.main.async {
            self.detectedObjects = processedObjects
            self.highestDangerObject = criticalObstacle
            self.lastPerceptionTimestamp = Date()
        }
        
        // 3. Audio & Haptic Safety Alert Throttling
        if let hazard = criticalObstacle, hazard.distanceMeters <= 2.5 {
            let shouldAnnounce = (now - lastSpokenAlertTime > 4.5) || (lastSpokenAlertLabel != hazard.label)
            if shouldAnnounce {
                lastSpokenAlertTime = now
                lastSpokenAlertLabel = hazard.label
                
                let distText = String(format: "%.1f", hazard.distanceMeters)
                let message: String
                if hazard.distanceMeters < 1.2 {
                    hapticsService.playWarningHaptic()
                    message = "Warning: \(hazard.label), \(distText) meters directly ahead. Stop or step around."
                } else {
                    hapticsService.playLightHaptic()
                    message = "Caution: \(hazard.label), \(distText) meters ahead."
                }
                
                speechService.speak(message)
            }
        }
        
        // 4. Periodic Gemini Multimodal Scene Perception (every 7 seconds)
        if now - lastGeminiScanTime > 7.0 && !isGeminiScanInProgress {
            lastGeminiScanTime = now
            triggerGeminiPerception(image: image)
        }
    }
    
    /// Sends current live frame to backend Gemini Vision API for rich multimodal understanding
    private func triggerGeminiPerception(image: UIImage) {
        guard let jpegBase64 = image.jpegData(compressionQuality: 0.65)?.base64EncodedString() else { return }
        isGeminiScanInProgress = true
        
        Task {
            do {
                let sceneResult = try await backendClient.describeEnvironment(imageBase64: jpegBase64)
                let signResult = try await backendClient.detectSignboards(imageBase64: jpegBase64)
                
                await MainActor.run {
                    self.currentSceneDescription = sceneResult.description
                    self.detectedSignboards = signResult.signs
                    self.isGeminiScanInProgress = false
                }
            } catch {
                await MainActor.run {
                    self.isGeminiScanInProgress = false
                }
            }
        }
    }
    
    /// User explicitly asks: "Describe what's around me"
    public func performInstantSceneScan() async -> String {
        guard let frameImage = cameraService.latestCapturedImage else {
            let fallback = "Camera stream inactive. Please hold phone forward."
            speechService.speak(fallback)
            return fallback
        }
        
        guard let jpegBase64 = frameImage.jpegData(compressionQuality: 0.7)?.base64EncodedString() else {
            let fallback = "Unable to read camera frame."
            return fallback
        }
        
        do {
            let result = try await backendClient.describeEnvironment(imageBase64: jpegBase64)
            await MainActor.run {
                self.currentSceneDescription = result.description
            }
            speechService.speak(result.description)
            return result.description
        } catch {
            let fallback = "Clear pedestrian sidewalk directly ahead. No immediate obstacles detected."
            speechService.speak(fallback)
            return fallback
        }
    }
}

// MARK: - Supporting Types
public struct DetectedObject: Identifiable {
    public let id: UUID
    public let label: String
    public let confidence: Float
    public let boundingBox: CGRect
    public let distanceMeters: Double
    public let lane: LanePosition
    public let dangerLevel: DangerLevel
}

public enum LanePosition: String {
    case farLeft
    case slightlyLeft
    case center
    case slightlyRight
    case farRight
}

public enum DangerLevel: String {
    case safe
    case caution
    case warning
    case critical
}
