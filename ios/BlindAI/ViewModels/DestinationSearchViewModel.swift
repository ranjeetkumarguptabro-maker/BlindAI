import SwiftUI
import Combine

@MainActor
public final class DestinationSearchViewModel: ObservableObject {
    @Published public var searchQuery: String = ""
    @Published public var recentPlaces: [DestinationItem] = [
        .rtu,
        .kipsalaCampus,
        .rigaCentralStation
    ]
    @Published public var nearbyCategories: [NearbyCategory] = [
        NearbyCategory(id: "uni", title: "Universities", iconName: "graduationcap.fill", iconColor: Color(red: 120/255, green: 110/255, blue: 235/255), iconBackground: Color(red: 238/255, green: 237/255, blue: 255/255)),
        NearbyCategory(id: "rest", title: "Restaurants", iconName: "fork.knife", iconColor: .orange, iconBackground: Color(red: 255/255, green: 243/255, blue: 230/255)),
        NearbyCategory(id: "cafe", title: "Coffee shops", iconName: "cup.and.saucer.fill", iconColor: Color(red: 50/255, green: 140/255, blue: 245/255), iconBackground: Color(red: 235/255, green: 245/255, blue: 255/255)),
        NearbyCategory(id: "park", title: "Parks", iconName: "tree.fill", iconColor: Color(red: 45/255, green: 180/255, blue: 80/255), iconBackground: Color(red: 235/255, green: 250/255, blue: 240/255)),
        NearbyCategory(id: "transit", title: "Public transport", iconName: "bus.fill", iconColor: Color(red: 240/255, green: 70/255, blue: 80/255), iconBackground: Color(red: 255/255, green: 235/255, blue: 238/255))
    ]
    
    public var onNavigateToRoute: ((AppRoute) -> Void)?
    public var onSelectDestination: ((DestinationItem) -> Void)?
    
    private let speechService = SpeechService.shared
    private let hapticsService = HapticsService.shared
    
    public init(
        onNavigateToRoute: ((AppRoute) -> Void)? = nil,
        onSelectDestination: ((DestinationItem) -> Void)? = nil
    ) {
        self.onNavigateToRoute = onNavigateToRoute
        self.onSelectDestination = onSelectDestination
    }
    
    public var displayedPlaces: [DestinationItem] {
        if searchQuery.trimmingCharacters(in: .whitespaces).isEmpty {
            return recentPlaces
        }
        return recentPlaces.filter {
            $0.title.localizedCaseInsensitiveContains(searchQuery) ||
            $0.subtitle.localizedCaseInsensitiveContains(searchQuery)
        }
    }
    
    public func selectDestination(_ item: DestinationItem) {
        hapticsService.impact(style: .medium)
        speechService.speak("Selected \(item.title). Loading route preview.")
        onSelectDestination?(item)
        onNavigateToRoute?(.routePreview)
    }
    
    public func handleSpeakDestination() {
        hapticsService.impact(style: .heavy)
        onNavigateToRoute?(.listening)
    }
    
    public func handleBack() {
        hapticsService.selection()
        onNavigateToRoute?(.home)
    }
}
