import SwiftUI

public struct CrosswalkStatusItem: Equatable {
    public let title: String
    public let subtitle: String
    public let quietMessage: String
    public let isWalkSignalGreen: Bool
    
    public init(
        title: String = "Approaching crosswalk.",
        subtitle: String = "Listen for traffic.",
        quietMessage: String = "I will be quiet while you cross.",
        isWalkSignalGreen: Bool = true
    ) {
        self.title = title
        self.subtitle = subtitle
        self.quietMessage = quietMessage
        self.isWalkSignalGreen = isWalkSignalGreen
    }
    
    public static let defaultCrossing = CrosswalkStatusItem()
}
