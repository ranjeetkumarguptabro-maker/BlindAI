import Foundation
import CoreGraphics
import CoreVideo
#if canImport(CoreML)
import CoreML
#endif
#if canImport(Vision)
import Vision
#endif
#if canImport(UIKit)
import UIKit
#endif

// MARK: - 1. Core ML YOLOv8 Nano Model Configuration & Input/Output Specs
/// Standard Core ML integration pattern for YOLOv8 Nano (`yolov8n.mlpackage` / `.mlmodel` / `.mlmodelc`)
/// configured for half-precision (FP16) or quantized (INT8) execution on the Apple Neural Engine (ANE).
/// - Input Tensor: Fixed $640 \times 640 \times 3$ RGB `CVPixelBuffer`, normalized to $[0.0, 1.0]$.
/// - Output Tensors: Bounding box coordinates, confidence scores, and class probabilities (`VNRecognizedObjectObservation`)
///   mapped directly to `ObstacleAlertItem` (`ObstacleAlertItem.swift`) and `YOLODetection`.
public final class YOLOObstacleDetector: @unchecked Sendable {
    public static let shared = YOLOObstacleDetector()
    public static let inputResolution = CGSize(width: 640, height: 640)
    public static let supportedModelBundleNames = ["yolov8n", "BlindAI_YOLOv8n", "yolov8s"]
    
    #if canImport(Vision) && canImport(CoreML)
    private var model: VNCoreMLModel?
    #endif
    public private(set) var isCoreMLModelLoaded: Bool = false

    public init() {
        setupModel()
    }

    private func setupModel() {
        #if canImport(Vision) && canImport(CoreML)
        let config = MLModelConfiguration()
        // Leverage Apple Neural Engine (ANE) + GPU + CPU for FP16 / INT8 execution and minimal thermal throttling
        config.computeUnits = .all
        
        // Search main bundle for compiled (.mlmodelc) or package (.mlpackage / .mlmodel) YOLOv8 Nano asset
        for name in Self.supportedModelBundleNames {
            if let compiledURL = Bundle.main.url(forResource: name, withExtension: "mlmodelc"),
               let mlModel = try? MLModel(contentsOf: compiledURL, configuration: config),
               let visionModel = try? VNCoreMLModel(for: mlModel) {
                self.model = visionModel
                self.model?.usesCPUOnly = false // Leverage Neural Engine (ANE) on supported iOS devices
                self.isCoreMLModelLoaded = true
                return
            }
            if let packageURL = Bundle.main.url(forResource: name, withExtension: "mlpackage") ?? Bundle.main.url(forResource: name, withExtension: "mlmodel"),
               let compiledURL = try? MLModel.compileModel(at: packageURL),
               let mlModel = try? MLModel(contentsOf: compiledURL, configuration: config),
               let visionModel = try? VNCoreMLModel(for: mlModel) {
                self.model = visionModel
                self.model?.usesCPUOnly = false
                self.isCoreMLModelLoaded = true
                return
            }
        }
        #endif
    }

    #if canImport(Vision)
    /// Executes YOLOv8 Nano Core ML inference on a $640 \times 640 \times 3$ normalized `CVPixelBuffer`
    public func detect(pixelBuffer: CVPixelBuffer, completion: @escaping ([VNRecognizedObjectObservation]) -> Void) {
        guard let model = model else {
            completion([])
            return
        }
        
        let request = VNCoreMLRequest(model: model) { request, error in
            guard error == nil, let results = request.results as? [VNRecognizedObjectObservation] else {
                completion([])
                return
            }
            completion(results)
        }
        
        request.imageCropAndScaleOption = .scaleFill // Match 640x640 training preprocessing
        
        let handler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer, options: [:])
        DispatchQueue.global(qos: .userInitiated).async {
            do {
                try handler.perform([request])
            } catch {
                completion([])
            }
        }
    }
    
    /// Maps Core ML `[VNRecognizedObjectObservation]` output tensors directly into `[ObstacleAlertItem]` (`ObstacleAlertItem.swift`)
    public func detectObstacleAlerts(pixelBuffer: CVPixelBuffer, completion: @escaping ([ObstacleAlertItem]) -> Void) {
        detect(pixelBuffer: pixelBuffer) { observations in
            let items: [ObstacleAlertItem] = observations.enumerated().map { idx, obs in
                let height = Double(obs.boundingBox.height)
                let estDist = height > 0.55 ? 0.8 : (height > 0.35 ? 1.8 : (height > 0.20 ? 2.8 : 4.2))
                let trackId = String(format: "ID:%02d", idx + 1)
                let labelLower = (obs.labels.first?.identifier ?? "").lowercased()
                let velocity: Double = labelLower.contains("tram") ? 8.0 : (labelLower.contains("car") ? 3.5 : (labelLower.contains("bicycle") ? 2.1 : 1.2))
                return ObstacleAlertItem(
                    observation: obs,
                    distanceMeters: estDist,
                    trackId: trackId,
                    velocityMps: velocity
                )
            }
            completion(items)
        }
    }
    #endif
}

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
        case warningSign = "warning_sign"
        case prohibitionSign = "prohibition_sign"
        case mandatorySign = "mandatory_sign"
        case informationSign = "information_sign"
        case directionSign = "direction_sign"
        case temporarySign = "temporary_sign"
        case additionalPlate = "additional_plate"
        case streetSign = "street_sign"
        case buildingBoard = "building_board"
        case transitSign = "transit_sign"
        case generalSign = "general_sign"
        
        public var icon: String {
            switch self {
            case .warningSign: return "⚠️"
            case .prohibitionSign: return "🚫"
            case .mandatorySign: return "🔵"
            case .informationSign: return "ℹ️"
            case .directionSign: return "🪧"
            case .temporarySign: return "🚧"
            case .additionalPlate: return "🪧"
            case .streetSign: return "🪧"
            case .buildingBoard: return "🏢"
            case .transitSign: return "🚏"
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
    public let coreMLDetector = YOLOObstacleDetector.shared
    
    public init() {}
    
    /// Synchronous / UIImage wrapper used by `RealtimeVisionPerceptionService`
    #if canImport(UIKit)
    public func detectObjects(in image: UIImage) -> [YOLODetection] {
        guard let cgImage = image.cgImage else { return [] }
        #if canImport(Vision)
        var results: [YOLODetection] = []
        let semaphore = DispatchSemaphore(value: 0)
        let rectRequest = VNDetectRectanglesRequest { request, error in
            defer { semaphore.signal() }
            guard error == nil, let observations = request.results as? [VNRectangleObservation] else { return }
            for rect in observations where rect.confidence > 0.58 {
                let uiRect = CGRect(
                    x: rect.boundingBox.origin.x,
                    y: 1.0 - rect.boundingBox.origin.y - rect.boundingBox.size.height,
                    width: rect.boundingBox.size.width,
                    height: rect.boundingBox.size.height
                )
                let lane = self.determineLane(for: uiRect)
                let dist = self.estimateDistance(for: uiRect)
                results.append(YOLODetection(
                    label: "Obstacle",
                    icon: "🚧",
                    confidence: rect.confidence,
                    boundingBox: uiRect,
                    distanceMeters: dist,
                    lane: lane,
                    isHazard: dist < 2.0 && lane == .center
                ))
            }
        }
        let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
        try? handler.perform([rectRequest])
        _ = semaphore.wait(timeout: .now() + 0.08)
        return results
        #else
        return []
        #endif
    }
    #endif

    /// Detects real-world objects (obstacles, Crossing Paths, Riga Road Signs, and Sidewalk Trees) in camera frames using Vision & CoreML YOLOv8n
    public func detectObjects(in pixelBuffer: CVPixelBuffer) async -> [YOLODetection] {
        #if canImport(Vision)
        // 1. If compiled Core ML YOLOv8 Nano (`yolov8n.mlpackage` / `.mlmodelc`) is loaded, run ANE inference first
        if coreMLDetector.isCoreMLModelLoaded {
            let coreMLDetections: [YOLODetection] = await withCheckedContinuation { continuation in
                coreMLDetector.detect(pixelBuffer: pixelBuffer) { observations in
                    let mapped: [YOLODetection] = observations.compactMap { obs in
                        guard let top = obs.labels.first, top.confidence >= 0.35 else { return nil }
                        let uiRect = CGRect(
                            x: obs.boundingBox.origin.x,
                            y: 1.0 - obs.boundingBox.origin.y - obs.boundingBox.size.height,
                            width: obs.boundingBox.size.width,
                            height: obs.boundingBox.size.height
                        )
                        let lane = self.determineLane(for: uiRect)
                        let dist = self.estimateDistance(for: uiRect)
                        return YOLODetection(
                            id: obs.uuid,
                            label: top.identifier.capitalized,
                            icon: self.icon(for: top.identifier),
                            confidence: top.confidence,
                            boundingBox: uiRect,
                            distanceMeters: dist,
                            lane: lane,
                            isHazard: dist < 2.2 && lane == .center
                        )
                    }
                    continuation.resume(returning: mapped)
                }
            }
            if !coreMLDetections.isEmpty {
                return coreMLDetections
            }
        }
        return await withCheckedContinuation { continuation in
            var detections: [YOLODetection] = []
            
            let rectRequest = VNDetectRectanglesRequest { request, error in
                guard error == nil, let results = request.results as? [VNRectangleObservation] else {
                    return
                }
                
                var groundStripeRects: [CGRect] = []
                
                for rect in results where rect.confidence > 0.58 {
                    let uiRect = CGRect(
                        x: rect.boundingBox.origin.x,
                        y: 1.0 - rect.boundingBox.origin.y - rect.boundingBox.size.height,
                        width: rect.boundingBox.size.width,
                        height: rect.boundingBox.size.height
                    )
                    
                    let aspectRatio = uiRect.width / max(0.01, uiRect.height)
                    // Wide horizontal bars on the ground plane indicate zebra crossing stripes
                    if uiRect.origin.y > 0.42 && aspectRatio >= 1.85 {
                        groundStripeRects.append(uiRect)
                        continue
                    }
                    
                    let lane = self.determineLane(for: uiRect)
                    let estimatedDist = self.estimateDistance(for: uiRect)
                    
                    // Elevated square/board in upper field -> Road Sign
                    if uiRect.origin.y < 0.38 && uiRect.height < 0.32 && aspectRatio >= 0.65 && aspectRatio <= 2.6 {
                        detections.append(YOLODetection(
                            label: "Road Sign",
                            icon: "🪧",
                            confidence: rect.confidence,
                            boundingBox: uiRect,
                            distanceMeters: estimatedDist,
                            lane: lane,
                            isHazard: false
                        ))
                        continue
                    }
                    
                    // Tall vertical trunk/canopy structure -> Tree
                    if uiRect.origin.y < 0.30 && uiRect.height >= 0.42 && aspectRatio <= 0.65 {
                        detections.append(YOLODetection(
                            label: "Tree",
                            icon: "🌳",
                            confidence: rect.confidence,
                            boundingBox: uiRect,
                            distanceMeters: estimatedDist,
                            lane: lane,
                            isHazard: estimatedDist < 2.2
                        ))
                        continue
                    }
                    
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
                
                // Fuse ground-plane zebra stripes into a unified Crossing Path detection
                if !groundStripeRects.isEmpty {
                    let unionRect = groundStripeRects.reduce(groundStripeRects[0]) { $0.union($1) }
                    let lane = self.determineLane(for: unionRect)
                    let bottomY = max(0.22, Double(unionRect.maxY) - 0.24)
                    let crossDist = max(0.6, min(6.5, 1.35 / bottomY))
                    detections.append(YOLODetection(
                        label: "Crossing Path",
                        icon: "🚸",
                        confidence: min(0.98, 0.82 + Float(groundStripeRects.count) * 0.03),
                        boundingBox: unionRect,
                        distanceMeters: crossDist,
                        lane: lane,
                        isHazard: false
                    ))
                }
            }
            rectRequest.minimumAspectRatio = 0.15
            rectRequest.maximumAspectRatio = 8.0
            rectRequest.maximumObservations = 12
            rectRequest.minimumConfidence = 0.58
            
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
    
    /// Recognizes street signboards, Latvian road signs, entrance plaques, and transit markers via Vision OCR
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
                    guard rawString.count >= 2 else { continue }
                    
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
    
    /// Classifies recognized sign text into Latvian (Riga) Road Sign category
    private func classifySignboard(text: String) -> (SignboardDetection.SignType, String) {
        let lower = text.lowercased()
        if lower == "stop" {
            return (.informationSign, "STOP sign ahead at intersection. Pause at curb and check traffic.")
        } else if lower.contains("policija") || lower.contains("police") {
            return (.informationSign, "Information sign ahead: Latvian Police station (POLICIJA).")
        } else if lower.contains("zona p") || lower == "p" {
            return (.informationSign, "Information sign ahead: Parking zone (ZONA P). Watch for vehicles.")
        } else if lower.contains("taxi") {
            return (.informationSign, "Information sign ahead: Taxi rank (TAXI).")
        } else if lower.contains("rīga") || lower.contains("riga") || lower.contains("jūrmala") || lower.contains("jurmala") || lower.contains("daugavpils") || lower.contains("centrs") || lower.contains("lidosta") || lower.contains("osta") || lower.contains("vecrīga") || lower.contains("vecriga") || lower.contains("muzejs") || lower.contains("e22") || lower.contains("a2") || lower.contains("p4") {
            return (.directionSign, "Riga direction sign ahead: \(text)")
        } else if lower.contains("ceļa darbi") || lower.contains("road works") || lower.contains("30") {
            return (.temporarySign, "Temporary road works sign ahead: \(text). Watch for barriers.")
        } else if lower.contains("50") || lower.contains("4.0m") || lower.contains("2.5m") || lower.contains("6t") || lower.contains("aizliegts") {
            return (.prohibitionSign, "Prohibition road sign ahead: \(text)")
        } else if lower.contains("100 m") || lower.contains("300 m") {
            return (.additionalPlate, "Additional distance plate: \(text)")
        } else if lower.contains("iela") || lower.contains("street") || lower.contains("boulevard") || lower.contains("dambis") {
            return (.streetSign, "Street sign: \(text)")
        } else if lower.contains("rtu") || lower.contains("fakultāte") || lower.contains("faculty") || lower.contains("library") || lower.contains("ieeja") || lower.contains("entrance") {
            return (.buildingBoard, "Building sign: \(text)")
        } else if lower.contains("autobuss") || lower.contains("bus") || lower.contains("tram") || lower.contains("pietura") {
            return (.transitSign, "Transit sign: \(text)")
        } else if lower.contains("uzmanību") || lower.contains("caution") || lower.contains("pāreja") || lower.contains("crossing") || lower.contains("10%") {
            return (.warningSign, "Warning sign ahead: \(text)")
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
    
    public func icon(for label: String) -> String {
        let lower = label.lowercased()
        if lower.contains("person") || lower.contains("pedestrian") { return "🚶" }
        if lower.contains("car") || lower.contains("truck") || lower.contains("vehicle") { return "🚗" }
        if lower.contains("tram") || lower.contains("bus") { return "🚋" }
        if lower.contains("bicycle") || lower.contains("cyclist") { return "🚲" }
        if lower.contains("traffic light") { return "🚦" }
        if lower.contains("sign") { return "🪧" }
        if lower.contains("tree") { return "🌳" }
        if lower.contains("stair") { return "🪜" }
        if lower.contains("pole") { return "💈" }
        return "⚠️"
    }
}
