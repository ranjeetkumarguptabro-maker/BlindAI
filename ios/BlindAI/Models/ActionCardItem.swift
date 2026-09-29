import SwiftUI

public enum ActionCardType: String, Identifiable, CaseIterable {
    case startNavigation = "start_navigation"
    case describeAround = "describe_around"
    case whereAmI = "where_am_i"
    
    public var id: String { rawValue }
    
    public var title: String {
        switch self {
        case .startNavigation: return "Start navigation"
        case .describeAround: return "Describe what's around me"
        case .whereAmI: return "Where am I?"
        }
    }
    
    public var subtitle: String {
        switch self {
        case .startNavigation: return "Get directions to a place"
        case .describeAround: return "Identify objects, signs, and more"
        case .whereAmI: return "Tell me my current location"
        }
    }
    
    public var iconName: String {
        switch self {
        case .startNavigation: return "figure.walk"
        case .describeAround: return "camera.fill"
        case .whereAmI: return "map.fill"
        }
    }
    
    public var iconColor: Color {
        switch self {
        case .startNavigation: return .blindAIOrange
        case .describeAround: return .blindAIPurple
        case .whereAmI: return .blindAIGreen
        }
    }
    
    public var iconBackground: Color {
        switch self {
        case .startNavigation: return .blindAIOrangeBg
        case .describeAround: return .blindAIPurpleBg
        case .whereAmI: return .blindAIGreenBg
        }
    }
    
    public var accessibilityHint: String {
        switch self {
        case .startNavigation: return "Double tap to enter active navigation route"
        case .describeAround: return "Double tap to start camera environment analysis"
        case .whereAmI: return "Double tap to announce current location"
        }
    }
}
