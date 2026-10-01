import Foundation
import Combine
import CoreVideo
#if canImport(ARKit)
import ARKit
#endif
#if canImport(Vision)
import Vision
#endif

/// Represents an obstacle detected by the LiDAR + Camera vision sensor fusion pipeline.
public struct DetectedObstacle: Identifiable, Equatable, Sendable {
    public let id: UUID
    public let label: String
    public let distanceMeters: Float
    public let confidence: Float
    public let boundingBox: CGRect
    public let lane: LaneMath.HorizontalLane
    public let verticalLevel: LaneMath.VerticalHeight
    public let dangerLevel: DangerLevel
    public let timestamp: Date
    
    public enum DangerLevel: String, Sendable, Comparable {
        case safe = "Safe"
        case notice = "Notice"
        case caution = "Caution"
        case danger = "Danger"
        case critical = "Critical Stop"
        
        public var priorityScore: Int {
            switch self {
            case .safe: return 1
            case .notice: return 2
            case .caution: return 3
            case .danger: return 4
            case .critical: return 5
            }
        }
        
        public static func < (lhs: DangerLevel, rhs: DangerLevel) -> Bool {
            lhs.priorityScore < rhs.priorityScore
        }
    }
    
    public init(
        id: UUID = UUID(),
        label: String,
        distanceMeters: Float,
        confidence: Float = 0.9,
        boundingBox: CGRect = CGRect(x: 0.3, y: 0.3, width: 0.4, height: 0.4),
        lane: LaneMath.HorizontalLane = .center,
        verticalLevel: LaneMath.VerticalHeight = .torso,
        dangerLevel: DangerLevel = .caution,
        timestamp: Date = Date()
    ) {
        self.id = id
        self.label = label
        self.distanceMeters = distanceMeters
        self.confidence = confidence
        self.boundingBox = boundingBox
        self.lane = lane
        self.verticalLevel = verticalLevel
        self.dangerLevel = dangerLevel
        self.timestamp = timestamp
    }
}

/// Service managing the ARKit ARSession with sceneDepth and smoothedSceneDepth LiDAR semantics,
/// pixel-buffer depth sampling, and Vision-based object detection.
public final class ARKitLiDARScannerService: NSObject, ObservableObject {
    public static let shared = ARKitLiDARScannerService()
    
    // Hardware & Scanner Status
    @Published public private(set) var isSupported: Bool = false
    @Published public private(set) var isScanning: Bool = false
    @Published public private(set) var currentDistanceMeters: Float = 5.0
    @Published public private(set) var nearestObstacle: DetectedObstacle?
    @Published public private(set) var detectedObstacles: [DetectedObstacle] = []
    @Published public private(set) var activeDangerLevel: DetectedObstacle.DangerLevel = .safe
    @Published public private(set) var confidenceScore: Float = 1.0
    
    // Configurable Corridors and Thresholds
    public var criticalDistanceThreshold: Float = 0.7   // < 0.7m: Immediate STOP
    public var dangerDistanceThreshold: Float = 1.5     // < 1.5m: Danger warning
    public var cautionDistanceThreshold: Float = 2.5    // < 2.5m: Obstacle ahead
    public var noticeDistanceThreshold: Float = 3.5     // < 3.5m: Notice
    
    // Callbacks for Safety Engine
    public var onObstacleDetected: ((DetectedObstacle) -> Void)?
    public var onCriticalHazard: ((DetectedObstacle) -> Void)?
    
    #if canImport(ARKit)
    private var arSession: ARSession?
    #endif
    
    private var simulationTimer: Timer?
    private var isSimulating: Bool = false
    
    public override init() {
        super.init()
        checkHardwareSupport()
    }
    
    /// Evaluates if the current physical device supports LiDAR scene depth
    public func checkHardwareSupport() {
        #if canImport(ARKit)
        if #available(iOS 14.0, *) {
            self.isSupported = ARWorldTrackingConfiguration.supportsFrameSemantics(.sceneDepth)
        } else {
            self.isSupported = false
        }
        #else
        self.isSupported = false
        #endif
    }
    
    /// Starts the real ARSession with LiDAR sceneDepth or simulation if unsupported
    public func startScanning() {
        guard !isScanning else { return }
        isScanning = true
        
        #if canImport(ARKit)
        if #available(iOS 14.0, *), ARWorldTrackingConfiguration.supportsFrameSemantics(.sceneDepth) {
            startARSession()
            return
        }
        #endif
        
        // Non-LiDAR device or simulator fallback
        startSimulation()
    }
    
    /// Stops scanning and releases camera and depth resources
    public func stopScanning() {
        isScanning = false
        simulationTimer?.invalidate()
        simulationTimer = nil
        
        #if canImport(ARKit)
        arSession?.pause()
        arSession = nil
        #endif
    }
    
    #if canImport(ARKit)
    @available(iOS 14.0, *)
    private func startARSession() {
        let configuration = ARWorldTrackingConfiguration()
        
        // Request LiDAR Scene Depth and Smoothed Scene Depth
        var semantics: ARConfiguration.FrameSemantics = []
        if ARWorldTrackingConfiguration.supportsFrameSemantics(.sceneDepth) {
            semantics.insert(.sceneDepth)
        }
        if ARWorldTrackingConfiguration.supportsFrameSemantics(.smoothedSceneDepth) {
            semantics.insert(.smoothedSceneDepth)
        }
        configuration.frameSemantics = semantics
        
        let session = ARSession()
        session.delegate = self
        session.run(configuration, options: [.resetTracking, .removeExistingAnchors])
        self.arSession = session
    }
    #endif
    
    // MARK: - Depth Buffer Pixel Sampling
    
    /// Samples depth map at given normalized coordinates (0.0 ... 1.0)
    /// Reads depth in meters from CVPixelBuffer (kCVPixelFormatType_DepthFloat32).
    public func sampleDepth(
        from depthBuffer: CVPixelBuffer,
        confidenceBuffer: CVPixelBuffer?,
        at normalizedRect: CGRect
    ) -> (distance: Float, confidence: Float)? {
        CVPixelBufferLockBaseAddress(depthBuffer, .readOnly)
        if let conf = confidenceBuffer {
            CVPixelBufferLockBaseAddress(conf, .readOnly)
        }
        
        defer {
            CVPixelBufferUnlockBaseAddress(depthBuffer, .readOnly)
            if let conf = confidenceBuffer {
                CVPixelBufferUnlockBaseAddress(conf, .readOnly)
            }
        }
        
        let width = CVPixelBufferGetWidth(depthBuffer)
        let height = CVPixelBufferGetHeight(depthBuffer)
        guard width > 0, height > 0 else { return nil }
        
        guard let baseAddress = CVPixelBufferGetBaseAddress(depthBuffer) else { return nil }
        let bytesPerRow = CVPixelBufferGetBytesPerRow(depthBuffer)
        
        var confBaseAddress: UnsafeMutableRawPointer? = nil
        var confBytesPerRow = 0
        if let conf = confidenceBuffer {
            confBaseAddress = CVPixelBufferGetBaseAddress(conf)
            confBytesPerRow = CVPixelBufferGetBytesPerRow(conf)
        }
        
        // Sample points across region of interest (5x5 grid)
        let startX = max(0, min(width - 1, Int(normalizedRect.minX * CGFloat(width))))
        let endX = max(startX + 1, min(width, Int(normalizedRect.maxX * CGFloat(width))))
        let startY = max(0, min(height - 1, Int(normalizedRect.minY * CGFloat(height))))
        let endY = max(startY + 1, min(height, Int(normalizedRect.maxY * CGFloat(height))))
        
        var validDepths: [Float] = []
        var confidenceSum: Float = 0
        var sampledPoints = 0
        
        let stepX = max(1, (endX - startX) / 5)
        let stepY = max(1, (endY - startY) / 5)
        
        for y in stride(from: startY, to: endY, by: stepY) {
            let rowPtr = baseAddress.advanced(by: y * bytesPerRow).assumingMemoryBound(to: Float32.self)
            let confRowPtr = confBaseAddress?.advanced(by: y * confBytesPerRow).assumingMemoryBound(to: UInt8.self)
            
            for x in stride(from: startX, to: endX, by: stepX) {
                let depth = rowPtr[x]
                
                // Confidence: 0 = low, 1 = medium, 2 = high
                var confVal: Float = 1.0
                if let confRow = confRowPtr {
                    let rawConf = confRow[x]
                    if rawConf == 0 {
                        continue // Skip unreliable low-confidence measurements
                    }
                    confVal = rawConf == 2 ? 1.0 : 0.6
                }
                
                // Valid LiDAR depth range typically 0.2m to 5.0m
                if depth > 0.1 && depth < 6.0 && !depth.isNaN {
                    validDepths.append(depth)
                    confidenceSum += confVal
                    sampledPoints += 1
                }
            }
        }
        
        guard !validDepths.isEmpty else { return nil }
        
        validDepths.sort()
        // Use 25th percentile for closest surface of the object facing the user
        let index = max(0, min(validDepths.count - 1, validDepths.count / 4))
        let distance = validDepths[index]
        let avgConfidence = sampledPoints > 0 ? (confidenceSum / Float(sampledPoints)) : 0.8
        
        return (distance, avgConfidence)
    }
    
    // MARK: - Danger Assessment
    
    public func evaluateDangerLevel(distance: Float, lane: LaneMath.HorizontalLane) -> DetectedObstacle.DangerLevel {
        if lane == .center {
            if distance < criticalDistanceThreshold {
                return .critical
            } else if distance < dangerDistanceThreshold {
                return .danger
            } else if distance < cautionDistanceThreshold {
                return .caution
            } else if distance < noticeDistanceThreshold {
                return .notice
            }
            return .safe
        } else {
            // Beside walking path (left or right)
            if distance < 1.0 {
                return .caution
            } else if distance < 2.0 {
                return .notice
            }
            return .safe
        }
    }
    
    // MARK: - Simulation Mode (Fallback for non-LiDAR / Simulator)
    
    public func startSimulation() {
        isSimulating = true
        simulationTimer?.invalidate()
        
        var step = 0
        let scenarios: [(label: String, distance: Float, lane: LaneMath.HorizontalLane, box: CGRect)] = [
            ("Clear Path", 4.5, .center, CGRect(x: 0.35, y: 0.35, width: 0.3, height: 0.3)),
            ("Bench", 3.2, .right, CGRect(x: 0.68, y: 0.40, width: 0.25, height: 0.25)),
            ("Chair", 2.1, .center, CGRect(x: 0.38, y: 0.35, width: 0.25, height: 0.30)),
            ("Person", 1.4, .center, CGRect(x: 0.32, y: 0.20, width: 0.36, height: 0.60)),
            ("Construction barrier", 0.65, .center, CGRect(x: 0.20, y: 0.30, width: 0.60, height: 0.45)),
            ("Clear Path", 4.0, .center, CGRect(x: 0.35, y: 0.35, width: 0.3, height: 0.3))
        ]
        
        simulationTimer = Timer.scheduledTimer(withTimeInterval: 2.5, repeats: true) { [weak self] _ in
            guard let self = self, self.isScanning else { return }
            
            let scenario = scenarios[step % scenarios.count]
            step += 1
            
            let danger = self.evaluateDangerLevel(distance: scenario.distance, lane: scenario.lane)
            let obstacle = DetectedObstacle(
                label: scenario.label,
                distanceMeters: scenario.distance,
                confidence: 0.94,
                boundingBox: scenario.box,
                lane: scenario.lane,
                verticalLevel: .torso,
                dangerLevel: danger
            )
            
            DispatchQueue.main.async {
                self.currentDistanceMeters = scenario.distance
                self.confidenceScore = 0.94
                self.activeDangerLevel = danger
                if scenario.label != "Clear Path" {
                    self.nearestObstacle = obstacle
                    self.detectedObstacles = [obstacle]
                    self.onObstacleDetected?(obstacle)
                    if danger == .critical {
                        self.onCriticalHazard?(obstacle)
                    }
                } else {
                    self.nearestObstacle = nil
                    self.detectedObstacles = []
                }
            }
        }
    }
    
    /// Injects an obstacle for interactive UI testing and simulator previews
    public func injectObstacle(label: String, distanceMeters: Float, lane: LaneMath.HorizontalLane) {
        let danger = evaluateDangerLevel(distance: distanceMeters, lane: lane)
        let obstacle = DetectedObstacle(
            label: label,
            distanceMeters: distanceMeters,
            confidence: 0.98,
            boundingBox: CGRect(x: 0.35, y: 0.35, width: 0.3, height: 0.3),
            lane: lane,
            verticalLevel: .torso,
            dangerLevel: danger
        )
        
        DispatchQueue.main.async {
            self.currentDistanceMeters = distanceMeters
            self.activeDangerLevel = danger
            self.nearestObstacle = obstacle
            self.detectedObstacles = [obstacle]
            self.onObstacleDetected?(obstacle)
            if danger == .critical {
                self.onCriticalHazard?(obstacle)
            }
        }
    }
}

// MARK: - ARSessionDelegate

#if canImport(ARKit)
extension ARKitLiDARScannerService: ARSessionDelegate {
    @available(iOS 14.0, *)
    public func session(_ session: ARSession, didUpdate frame: ARFrame) {
        // Prefer smoothedSceneDepth for steadier distance estimation; fallback to raw sceneDepth
        guard let depthData = frame.smoothedSceneDepth ?? frame.sceneDepth else { return }
        
        let depthMap = depthData.depthMap
        let confidenceMap = depthData.confidenceMap
        
        // Center walking corridor sample (35% to 65% width, 30% to 70% height)
        let corridorRect = CGRect(x: 0.35, y: 0.30, width: 0.30, height: 0.40)
        
        if let sample = sampleDepth(from: depthMap, confidenceBuffer: confidenceMap, at: corridorRect) {
            let distance = sample.distance
            let confidence = sample.confidence
            let danger = evaluateDangerLevel(distance: distance, lane: .center)
            
            DispatchQueue.main.async {
                self.currentDistanceMeters = distance
                self.confidenceScore = confidence
                self.activeDangerLevel = danger
                
                if danger >= .caution {
                    let obstacle = DetectedObstacle(
                        label: "Obstacle",
                        distanceMeters: distance,
                        confidence: confidence,
                        boundingBox: corridorRect,
                        lane: .center,
                        verticalLevel: .torso,
                        dangerLevel: danger
                    )
                    self.nearestObstacle = obstacle
                    self.detectedObstacles = [obstacle]
                    self.onObstacleDetected?(obstacle)
                    
                    if danger == .critical {
                        self.onCriticalHazard?(obstacle)
                    }
                } else if danger == .safe && self.activeDangerLevel != .safe {
                    self.nearestObstacle = nil
                    self.detectedObstacles = []
                }
            }
        }
    }
    
    public func session(_ session: ARSession, didFailWithError error: Error) {
        print("[ARKitLiDAR] ARSession failed with error: \(error.localizedDescription)")
        startSimulation()
    }
    
    public func sessionWasInterrupted(_ session: ARSession) {
        print("[ARKitLiDAR] ARSession was interrupted.")
    }
    
    public func sessionInterruptionEnded(_ session: ARSession) {
        print("[ARKitLiDAR] ARSession interruption ended. Resuming scanning.")
    }
}
#endif
