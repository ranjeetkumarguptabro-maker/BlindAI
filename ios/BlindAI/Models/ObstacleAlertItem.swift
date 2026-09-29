import SwiftUI

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
        cardSubtitle: String = "On the right, 2 meters ahead."
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
    }
    
    public static let defaultHazard = ObstacleAlertItem()
}
