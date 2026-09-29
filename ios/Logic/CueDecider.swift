import Foundation

/// CueDecider prioritizes audio and haptic cues based on distance, obstacle urgency, and turn instructions.
public struct CueDecider {
    public enum CuePriority: Int, Comparable {
        case low = 1
        case navigation = 2
        case turnImminent = 3
        case obstacle = 4
        case headHazard = 5
        case emergency = 6
        
        public static func < (lhs: CuePriority, rhs: CuePriority) -> Bool {
            lhs.rawValue < rhs.rawValue
        }
    }
    
    public struct Cue: Equatable {
        public let priority: CuePriority
        public let spokenMessage: String
        public let hapticPattern: String
        
        public init(priority: CuePriority, spokenMessage: String, hapticPattern: String) {
            self.priority = priority
            self.spokenMessage = spokenMessage
            self.hapticPattern = hapticPattern
        }
    }
    
    public init() {}
    
    /// Decides whether a new cue should preempt an active lower-priority cue
    public func shouldPreempt(activeCue: Cue?, newCue: Cue) -> Bool {
        guard let active = activeCue else { return true }
        return newCue.priority > active.priority
    }
}
