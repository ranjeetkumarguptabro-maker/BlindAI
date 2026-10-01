import Foundation
import CoreGraphics
import CoreVideo
#if canImport(Vision)
import Vision
#endif

/// Candidate object detected by Apple's Vision framework
public struct DetectedObjectCandidate: Identifiable, Equatable, Sendable {
    public let id: UUID
    public let label: String
    public let confidence: Float
    public let boundingBox: CGRect // Normalized UIKit coordinate system (origin top-left)
    public let lane: LaneMath.HorizontalLane
    public let verticalHeight: LaneMath.VerticalHeight
    
    public init(
        id: UUID = UUID(),
        label: String,
        confidence: Float,
        boundingBox: CGRect,
        lane: LaneMath.HorizontalLane,
        verticalHeight: LaneMath.VerticalHeight
    ) {
        self.id = id
        self.label = label
        self.confidence = confidence
        self.boundingBox = boundingBox
        self.lane = lane
        self.verticalHeight = verticalHeight
    }
}

/// Service running Vision framework object detection on camera frames
public final class VisionObjectDetector {
    public static let shared = VisionObjectDetector()
    
    // Supported obstacle taxonomy
    public static let recognizedCategories: Set<String> = [
        "person", "car", "bicycle", "motorcycle", "chair", "table",
        "wall", "pole", "tree", "door", "stairs", "construction barrier",
        "trash bin", "bench", "traffic cone", "barrier", "scooter"
    ]
    
    public init() {}
    
    /// Detects objects within a camera frame pixel buffer
    public func detectObjects(in pixelBuffer: CVPixelBuffer) async -> [DetectedObjectCandidate] {
        #if canImport(Vision)
        return await withCheckedContinuation { continuation in
            var candidates: [DetectedObjectCandidate] = []
            
            // Vision Detect Rectangles Request for physical obstacles & barriers
            let rectRequest = VNDetectRectanglesRequest { request, error in
                guard error == nil, let results = request.results as? [VNRectangleObservation] else {
                    return
                }
                
                for rect in results where rect.confidence > 0.65 {
                    // Vision normalized coordinates have origin at bottom-left; convert to top-left
                    let uiRect = CGRect(
                        x: rect.boundingBox.origin.x,
                        y: 1.0 - rect.boundingBox.origin.y - rect.boundingBox.size.height,
                        width: rect.boundingBox.size.width,
                        height: rect.boundingBox.size.height
                    )
                    
                    let lane = self.determineLane(for: uiRect)
                    let height = self.determineVerticalHeight(for: uiRect)
                    
                    candidates.append(DetectedObjectCandidate(
                        label: "Obstacle",
                        confidence: rect.confidence,
                        boundingBox: uiRect,
                        lane: lane,
                        verticalHeight: height
                    ))
                }
            }
            rectRequest.minimumAspectRatio = 0.2
            rectRequest.maximumAspectRatio = 5.0
            rectRequest.minimumConfidence = 0.6
            
            let handler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer, options: [:])
            do {
                try handler.perform([rectRequest])
                continuation.resume(returning: candidates)
            } catch {
                continuation.resume(returning: [])
            }
        }
        #else
        return []
        #endif
    }
    
    /// Maps horizontal position of bounding box into lane
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
    
    /// Maps vertical position of bounding box into torso vs head height
    public func determineVerticalHeight(for rect: CGRect) -> LaneMath.VerticalHeight {
        // If the top of the box is in upper 25% of camera view
        if rect.minY < 0.25 {
            return .head
        } else {
            return .torso
        }
    }
    
    /// Classifies an arbitrary text query or model tag into standardized canonical name
    public func canonicalize(label: String) -> String {
        let lower = label.lowercased().trimmingCharacters(in: .whitespacesAndNewlines)
        if lower.contains("person") || lower.contains("pedestrian") || lower.contains("human") {
            return "Person"
        }
        if lower.contains("chair") || lower.contains("seat") || lower.contains("stool") {
            return "Chair"
        }
        if lower.contains("bench") {
            return "Bench"
        }
        if lower.contains("table") || lower.contains("desk") {
            return "Table"
        }
        if lower.contains("car") || lower.contains("vehicle") || lower.contains("automobile") {
            return "Car"
        }
        if lower.contains("bike") || lower.contains("bicycle") {
            return "Bicycle"
        }
        if lower.contains("barrier") || lower.contains("cone") || lower.contains("construction") {
            return "Construction barrier"
        }
        if lower.contains("tree") || lower.contains("bush") {
            return "Tree"
        }
        if lower.contains("pole") || lower.contains("post") || lower.contains("lamppost") {
            return "Pole"
        }
        if lower.contains("stair") || lower.contains("step") {
            return "Stairs"
        }
        if lower.contains("door") {
            return "Door"
        }
        if lower.contains("trash") || lower.contains("bin") || lower.contains("garbage") {
            return "Trash bin"
        }
        return "Obstacle"
    }
}
