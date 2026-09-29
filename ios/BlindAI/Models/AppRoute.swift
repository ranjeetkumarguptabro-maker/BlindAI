import Foundation

public enum AppRoute: String, CaseIterable, Hashable, Equatable {
    case home = "home"
    case listening = "listening"
    case destinationSearch = "destinationSearch"
    case routePreview = "routePreview"
    case activeNavigation = "activeNavigation"
    case whereAmI = "whereAmI"
    case describeAround = "describeAround"
    case obstacleAlert = "obstacleAlert"
    case crosswalkSafety = "crosswalkSafety"
}
