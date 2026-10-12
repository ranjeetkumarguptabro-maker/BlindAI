import SwiftUI
#if canImport(Vision)
import Vision
#endif

public struct ObstacleAlertItem: Identifiable, Equatable {
    public let id: UUID
    public let type: String
    public let distanceMeters: Double
    public let distanceText: String
    public let sideText: String
    public let title: String
    public let subtitle: String
    public let guidance: String
    public let cardTitle: String
    public let cardSubtitle: String
    public let confidence: Float
    public let boundingBox: CGRect
    public let trackId: String?
    public let velocityMps: Double?
    
    public init(
        id: UUID = UUID(),
        type: String = "Construction barrier",
        distanceMeters: Double = 2.0,
        distanceText: String = "Two meters ahead",
        sideText: String = "on right",
        title: String = "Obstacle ahead",
        subtitle: String = "Two meters ahead,\nconstruction barrier on right.",
        guidance: String = "Stay on the left pathway. Clear clearance ahead.",
        cardTitle: String = "Construction barrier",
        cardSubtitle: String = "On the right, 2 meters ahead.",
        confidence: Float = 0.95,
        boundingBox: CGRect = .zero,
        trackId: String? = nil,
        velocityMps: Double? = nil
    ) {
        self.id = id
        self.type = type
        self.distanceMeters = distanceMeters
        self.distanceText = distanceText
        self.sideText = sideText
        self.title = title
        self.subtitle = subtitle
        self.guidance = guidance
        self.cardTitle = cardTitle
        self.cardSubtitle = cardSubtitle
        self.confidence = confidence
        self.boundingBox = boundingBox
        self.trackId = trackId
        self.velocityMps = velocityMps
    }
    
    #if canImport(Vision)
    /// Maps a Core ML YOLOv8 `VNRecognizedObjectObservation` output tensor directly into `ObstacleAlertItem`
    public init(
        observation: VNRecognizedObjectObservation,
        distanceMeters: Double,
        trackId: String? = nil,
        velocityMps: Double? = nil
    ) {
        let topLabel = observation.labels.first?.identifier.capitalized ?? "Obstacle"
        let conf = observation.labels.first?.confidence ?? observation.confidence
        // Convert Vision bottom-left normalized coordinates [0.0, 1.0] to UIKit top-left normalized coordinates
        let uiBox = CGRect(
            x: observation.boundingBox.origin.x,
            y: 1.0 - observation.boundingBox.origin.y - observation.boundingBox.size.height,
            width: observation.boundingBox.size.width,
            height: observation.boundingBox.size.height
        )
        let side: String
        let steerGuidance: String
        if uiBox.midX < 0.35 {
            side = "on left"
            steerGuidance = "Keep right. Clear clearance ahead."
        } else if uiBox.midX > 0.65 {
            side = "on right"
            steerGuidance = "Keep left. Clear clearance ahead."
        } else {
            side = "directly ahead"
            steerGuidance = distanceMeters < 1.0
                ? "Stop immediately. Obstacle directly in your walking path."
                : "Slow down and step slightly left or right."
        }
        let distFormatted = String(format: "%.1f meters ahead", distanceMeters)
        
        self.init(
            id: observation.uuid,
            type: topLabel,
            distanceMeters: distanceMeters,
            distanceText: distFormatted,
            sideText: side,
            title: distanceMeters < 1.0 ? "Stop. \(topLabel) ahead" : "\(topLabel) ahead",
            subtitle: "\(distFormatted),\n\(topLabel.lowercased()) \(side).",
            guidance: steerGuidance,
            cardTitle: trackId != nil ? "\(topLabel) (\(trackId!))" : topLabel,
            cardSubtitle: "\(SideFormatter.capitalize(side)), \(String(format: "%.1fm", distanceMeters)) ahead.",
            confidence: conf,
            boundingBox: uiBox,
            trackId: trackId,
            velocityMps: velocityMps
        )
    }
    #endif
    
    private enum SideFormatter {
        static func capitalize(_ s: String) -> String {
            guard let first = s.first else { return s }
            return String(first).uppercased() + s.dropFirst()
        }
    }
    
    public static let defaultHazard = ObstacleAlertItem()
}
