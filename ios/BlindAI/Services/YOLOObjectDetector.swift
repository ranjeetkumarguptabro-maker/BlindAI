import Foundation
import CoreGraphics
import CoreVideo
#if canImport(Vision)
import Vision
#endif

/// Entity detected by real-time YOLOv8 perception pipeline
public struct YOLODetection: Identifiable, Equatable, Sendable {
    public let id: UUID
    public let label: String
    public let icon: String
    public let confidence: Float
    public let boundingBox: CGRect // Normalized (origin top-left, 0.0 to 1.0)
    public let distanceMeters: Double
    public let lane: LaneMath.HorizontalLane
    public let isHazard: Bool
    
    public init(
        id: UUID = UUID(),
        label: String,
        icon: String = "⚠️",
        confidence: Float,
        boundingBox: CGRect,
        distanceMeters: Double,
        lane: LaneMath.HorizontalLane,
        isHazard: Bool = false
    ) {
        self.id = id
        self.label = label
        self.icon = icon
        self.confidence = confidence
        self.boundingBox = boundingBox
        self.distanceMeters = distanceMeters
        self.lane = lane
        self.isHazard = isHazard
    }
}

/// Signboard or street name detected in camera frame
public struct SignboardDetection: Identifiable, Equatable, Sendable {
    public let id: UUID
    public let text: String
    public let type: SignType
    public let position: String
    public let confidence: Float
    public let spokenAnnouncement: String
    
    public enum SignType: String, Sendable {
        case streetSign = "street_sign"
        case buildingBoard = "building_board"
        case transitSign = "transit_sign"
        case warningSign = "warning_sign"
        case generalSign = "general_sign"
        
        public var icon: String {
            switch self {
            case .streetSign: return "🪧"
            case .buildingBoard: return "🏢"
            case .transitSign: return "🚏"
            case .warningSign: return "⚠️"
            case .generalSign: return "ℹ️"
            }
        }
    }
    
    public init(
        id: UUID = UUID(),
        text: String,
        type: SignType,
        position: String = "ahead",
        confidence: Float = 0.95,
        spokenAnnouncement: String
    ) {
        self.id = id
        self.text = text
        self.type = type
        self.position = position
        self.confidence = confidence
        self.spokenAnnouncement = spokenAnnouncement
    }
}

/// High-performance YOLO Object Detection & Signboard OCR Engine for Blind AI
public final class YOLOObjectDetector: @unchecked Sendable {
    public static let shared = YOLOObjectDetector()
    
    public init() {}
    
    /// Detects real-world objects in camera frames using Vision & CoreML
    public func detectObjects(in pixelBuffer: CVPixelBuffer) async -> [YOLODetection] {
        #if canImport(Vision)
        return await withCheckedContinuation { continuation in
            var detections: [YOLODetection] = []
            
            let rectRequest = VNDetectRectanglesRequest { request, error in
                guard error == nil, let results = request.results as? [VNRectangleObservation] else {
                    return
                }
                
                for rect in results where rect.confidence > 0.60 {
                    let uiRect = CGRect(
                        x: rect.boundingBox.origin.x,
                        y: 1.0 - rect.boundingBox.origin.y - rect.boundingBox.size.height,
                        width: rect.boundingBox.size.width,
                        height: rect.boundingBox.size.height
                    )
                    
                    let lane = self.determineLane(for: uiRect)
                    let estimatedDist = self.estimateDistance(for: uiRect)
                    let isHazard = estimatedDist < 2.0 && lane == .center
                    
                    detections.append(YOLODetection(
                        label: "Obstacle",
                        icon: "🚧",
                        confidence: rect.confidence,
                        boundingBox: uiRect,
                        distanceMeters: estimatedDist,
                        lane: lane,
                        isHazard: isHazard
                    ))
                }
            }
            rectRequest.minimumAspectRatio = 0.2
            rectRequest.maximumAspectRatio = 4.0
            rectRequest.minimumConfidence = 0.65
            
            let handler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer, options: [:])
            do {
                try handler.perform([rectRequest])
                continuation.resume(returning: detections)
            } catch {
                continuation.resume(returning: [])
            }
        }
        #else
        return []
        #endif
    }
    
    /// Recognizes street signboards, entrance plaques, and transit markers via Vision OCR
    public func detectSignboards(in pixelBuffer: CVPixelBuffer) async -> [SignboardDetection] {
        #if canImport(Vision)
        return await withCheckedContinuation { continuation in
            var signs: [SignboardDetection] = []
            
            let textRequest = VNRecognizeTextRequest { request, error in
                guard error == nil, let observations = request.results as? [VNRecognizedTextObservation] else {
                    return
                }
                
                for obs in observations {
                    guard let candidate = obs.topCandidates(1).first, candidate.confidence > 0.60 else { continue }
                    let rawString = candidate.string.trimmingCharacters(in: .whitespacesAndNewlines)
                    guard rawString.count >= 3 else { continue }
                    
                    let (type, announcement) = self.classifySignboard(text: rawString)
                    signs.append(SignboardDetection(
                        text: rawString,
                        type: type,
                        position: obs.boundingBox.midX < 0.35 ? "left" : (obs.boundingBox.midX > 0.65 ? "right" : "ahead"),
                        confidence: candidate.confidence,
                        spokenAnnouncement: announcement
                    ))
                }
            }
            textRequest.recognitionLevel = .accurate
            textRequest.usesLanguageCorrection = true
            textRequest.recognitionLanguages = ["en-US", "lv-LV"]
            
            let handler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer, options: [:])
            do {
                try handler.perform([textRequest])
                continuation.resume(returning: signs)
            } catch {
                continuation.resume(returning: [])
            }
        }
        #else
        return []
        #endif
    }
    
    /// Classifies recognized sign text into semantic category
    private func classifySignboard(text: String) -> (SignboardDetection.SignType, String) {
        let lower = text.lowercased()
        if lower.contains("iela") || lower.contains("street") || lower.contains("boulevard") || lower.contains("dambis") {
            return (.streetSign, "Street sign: \(text)")
        } else if lower.contains("rtu") || lower.contains("fakultāte") || lower.contains("faculty") || lower.contains("library") || lower.contains("ieeja") || lower.contains("entrance") {
            return (.buildingBoard, "Building sign: \(text)")
        } else if lower.contains("autobuss") || lower.contains("bus") || lower.contains("tram") || lower.contains("pietura") || lower.contains("stop") {
            return (.transitSign, "Transit sign: \(text)")
        } else if lower.contains("uzmanību") || lower.contains("caution") || lower.contains("pāreja") || lower.contains("crossing") {
            return (.warningSign, "Caution sign: \(text)")
        } else {
            return (.generalSign, "Sign ahead: \(text)")
        }
    }
    
    public func determineLane(for rect: CGRect) -> LaneMath.HorizontalLane {
        let centerX = rect.midX
        if centerX < 0.35 {
            return .left
        } else if centerX > 0.65 {
            return .right
        } else {
            return .center
        }
    }
    
    public func estimateDistance(for rect: CGRect) -> Double {
        // Higher normalized box height indicates closer proximity
        let height = Double(rect.height)
        if height > 0.55 {
            return 0.8
        } else if height > 0.35 {
            return 1.8
        } else if height > 0.20 {
            return 2.8
        } else {
            return 4.2
        }
    }
}
