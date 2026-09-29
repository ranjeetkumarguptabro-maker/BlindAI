import SwiftUI
import Combine

public struct RouteStep: Identifiable, Hashable {
    public let id: String
    public let instruction: String
    public let distance: String
    public let iconName: String
    
    public init(id: String = UUID().uuidString, instruction: String, distance: String, iconName: String) {
        self.id = id
        self.instruction = instruction
        self.distance = distance
        self.iconName = iconName
    }
}

@MainActor
public final class RoutePreviewViewModel: ObservableObject {
    @Published public var destination: DestinationItem = .rtu
    @Published public var steps: [RouteStep] = [
        RouteStep(instruction: "Walk towards Vanšu tilts", distance: "320 m", iconName: "arrow.up"),
        RouteStep(instruction: "Cross Vanšu tilts (bridge)", distance: "730 m", iconName: "arrow.turn.up.left"),
        RouteStep(instruction: "Turn left towards Ķīpsala", distance: "610 m", iconName: "arrow.turn.up.left"),
        RouteStep(instruction: "Continue to RTU main entrance", distance: "450 m", iconName: "arrow.up")
    ]
    
    public var onNavigateToRoute: ((AppRoute) -> Void)?
    
    private let navService = NavigationService.shared
    private let speechService = SpeechService.shared
    private let hapticsService = HapticsService.shared
    
    public init(
        destination: DestinationItem = .rtu,
        onNavigateToRoute: ((AppRoute) -> Void)? = nil
    ) {
        self.destination = destination
        self.onNavigateToRoute = onNavigateToRoute
    }
    
    public func handleStartNavigation() {
        hapticsService.notification(type: .success)
        navService.startRoute()
        onNavigateToRoute?(.activeNavigation)
    }
    
    public func handleBack() {
        hapticsService.selection()
        onNavigateToRoute?(.destinationSearch)
    }
    
    public var spokenSummary: String {
        "Route to \(destination.title), \(destination.subtitle). Total distance \(destination.distanceKm) kilometers, approximately \(destination.estimatedMinutes) minutes, \(destination.waypointCount) waypoints. First instruction: Walk towards Vanšu tilts in 320 meters."
    }
}
