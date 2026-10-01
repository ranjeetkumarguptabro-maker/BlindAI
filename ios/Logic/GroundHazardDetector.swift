import Foundation

/// GroundHazardDetector analyzes LiDAR ground plane continuity for drops, curbs, steps, and depressions.
public final class GroundHazardDetector {
    public enum GroundHazardType: String, Sendable {
        case curbDown = "Curb down"
        case curbUp = "Curb up"
        case stairsDown = "Stairs descending"
        case stairsUp = "Stairs ascending"
        case depression = "Pothole or depression"
        case none = "Even ground"
    }
    
    public struct GroundHazardAssessment: Equatable, Sendable {
        public let hasHazard: Bool
        public let hazardType: GroundHazardType
        public let distanceMeters: Float
        public let heightDeltaMeters: Float
        public let spokenWarning: String?
        
        public init(
            hasHazard: Bool,
            hazardType: GroundHazardType,
            distanceMeters: Float,
            heightDeltaMeters: Float,
            spokenWarning: String? = nil
        ) {
            self.hasHazard = hasHazard
            self.hazardType = hazardType
            self.distanceMeters = distanceMeters
            self.heightDeltaMeters = heightDeltaMeters
            self.spokenWarning = spokenWarning
        }
    }
    
    public init() {}
    
    /// Analyzes sequential ground depth measurements along the forward walking axis
    /// to detect drop-offs or elevation changes.
    public func analyzeGroundProfile(
        nearGroundDepth: Float,    // ~1.2m ahead on ground
        farGroundDepth: Float,     // ~2.5m ahead on ground
        expectedGroundSlope: Float = 0.0
    ) -> GroundHazardAssessment {
        let expectedFarDepth = nearGroundDepth * 1.8 // Geometric expected depth based on camera pitch
        let depthDelta = farGroundDepth - expectedFarDepth
        
        // Sudden drop (e.g. curb, drop-off, or subway platform edge)
        if depthDelta > 0.45 {
            return GroundHazardAssessment(
                hasHazard: true,
                hazardType: .curbDown,
                distanceMeters: nearGroundDepth,
                heightDeltaMeters: depthDelta * 0.5,
                spokenWarning: "Caution: Step down or curb ahead in 1 meter."
            )
        }
        
        // Sudden rise (e.g. raised curb or ascending step)
        if depthDelta < -0.40 {
            return GroundHazardAssessment(
                hasHazard: true,
                hazardType: .curbUp,
                distanceMeters: nearGroundDepth,
                heightDeltaMeters: abs(depthDelta) * 0.5,
                spokenWarning: "Caution: Step up or curb ahead."
            )
        }
        
        return GroundHazardAssessment(
            hasHazard: false,
            hazardType: .none,
            distanceMeters: nearGroundDepth,
            heightDeltaMeters: 0.0,
            spokenWarning: nil
        )
    }
}
