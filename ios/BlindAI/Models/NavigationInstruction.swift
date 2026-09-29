import Foundation

public struct NavigationInstruction: Equatable {
    public let title: String
    public let mainInstruction: String
    public let distanceValue: String
    public let distanceUnit: String
    public let maneuverText: String
    public let maneuverIcon: String
    
    public init(
        title: String = "Navigation",
        mainInstruction: String = "Take a right onto the sidewalk.",
        distanceValue: String = "41",
        distanceUnit: String = "m",
        maneuverText: String = "Veer left 152°",
        maneuverIcon: String = "arrow.turn.up.left"
    ) {
        self.title = title
        self.mainInstruction = mainInstruction
        self.distanceValue = distanceValue
        self.distanceUnit = distanceUnit
        self.maneuverText = maneuverText
        self.maneuverIcon = maneuverIcon
    }
    
    public static let mock = NavigationInstruction()
    
    public var spokenAnnouncement: String {
        return "\(mainInstruction), in \(distanceValue) \(distanceUnit == "m" ? "meters" : distanceUnit). Next maneuver: \(maneuverText)."
    }
}
