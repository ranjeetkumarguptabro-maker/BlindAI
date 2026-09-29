import Foundation

/// LaneMath calculates corridor lateral clearance and obstacle position relative to user heading.
/// Uses a 3x2 grid: left, center, right horizontally; ground/torso, head vertically.
public struct LaneMath {
    public struct GridCell: Equatable, Sendable {
        public let horizontal: HorizontalLane
        public let vertical: VerticalHeight
        public var distanceMeters: Float
        public var confidence: Float
        public var isObstacle: Bool
        
        public init(
            horizontal: HorizontalLane,
            vertical: VerticalHeight,
            distanceMeters: Float = 5.0,
            confidence: Float = 1.0,
            isObstacle: Bool = false
        ) {
            self.horizontal = horizontal
            self.vertical = vertical
            self.distanceMeters = distanceMeters
            self.confidence = confidence
            self.isObstacle = isObstacle
        }
    }
    
    public enum HorizontalLane: String, Sendable, CaseIterable {
        case left, center, right
    }
    
    public enum VerticalHeight: String, Sendable, CaseIterable {
        case torso, head
    }
    
    public var grid: [GridCell]
    
    public init() {
        var initialGrid: [GridCell] = []
        for lane in HorizontalLane.allCases {
            for height in VerticalHeight.allCases {
                initialGrid.append(GridCell(horizontal: lane, vertical: height))
            }
        }
        self.grid = initialGrid
    }
    
    /// Returns the nearest obstacle in the corridor, if any
    public func nearestObstacle() -> GridCell? {
        return grid
            .filter { $0.isObstacle }
            .min { $0.distanceMeters < $1.distanceMeters }
    }
    
    /// Evaluates if user path is clear
    public var isCenterClear: Bool {
        let centerObstacles = grid.filter { $0.horizontal == .center && $0.isObstacle }
        return centerObstacles.isEmpty
    }
}
