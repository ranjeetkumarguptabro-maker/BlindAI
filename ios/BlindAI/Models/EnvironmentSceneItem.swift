import SwiftUI

public struct EnvironmentSceneItem: Identifiable, Equatable {
    public let id: UUID
    public let iconSystemName: String
    public let iconColor: Color
    public let title: String
    public let subtitle: String?
    
    public init(
        id: UUID = UUID(),
        iconSystemName: String,
        iconColor: Color,
        title: String,
        subtitle: String? = nil
    ) {
        self.id = id
        self.iconSystemName = iconSystemName
        self.iconColor = iconColor
        self.title = title
        self.subtitle = subtitle
    }
}

public extension EnvironmentSceneItem {
    static let defaultRigaScene: [EnvironmentSceneItem] = [
        EnvironmentSceneItem(
            iconSystemName: "checkmark.circle.fill",
            iconColor: Color(red: 0.20, green: 0.78, blue: 0.35),
            title: "Sidewalk ahead is clear."
        ),
        EnvironmentSceneItem(
            iconSystemName: "building.2.fill",
            iconColor: Color(red: 0.55, green: 0.35, blue: 0.95),
            title: "Riga Technical University (RTU)",
            subtitle: "Main entrance on the left."
        ),
        EnvironmentSceneItem(
            iconSystemName: "bicycle",
            iconColor: Color(red: 0.15, green: 0.45, blue: 0.95),
            title: "Bicycle rack 3 meters ahead on right."
        ),
        EnvironmentSceneItem(
            iconSystemName: "person.2.fill",
            iconColor: Color(red: 0.38, green: 0.42, blue: 0.95),
            title: "People walking nearby."
        ),
        EnvironmentSceneItem(
            iconSystemName: "sun.max.fill",
            iconColor: Color(red: 0.98, green: 0.65, blue: 0.05),
            title: "It is sunny and bright."
        )
    ]
}
