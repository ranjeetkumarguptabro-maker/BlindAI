import SwiftUI
import Combine
import CoreLocation

@MainActor
public final class DestinationSearchViewModel: ObservableObject {
    @Published public var searchQuery: String = ""
    @Published public var liveSearchResults: [DestinationItem] = []
    @Published public var isSearchingLive: Bool = false
    
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
    private let searchService = DestinationSearchService.shared
    private var cancellables = Set<AnyCancellable>()
    
    public init(
        onNavigateToRoute: ((AppRoute) -> Void)? = nil,
        onSelectDestination: ((DestinationItem) -> Void)? = nil
    ) {
        self.onNavigateToRoute = onNavigateToRoute
        self.onSelectDestination = onSelectDestination
        
        setupSearchDebounce()
    }
    
    private func setupSearchDebounce() {
        $searchQuery
            .debounce(for: .milliseconds(350), scheduler: DispatchQueue.main)
            .removeDuplicates()
            .sink { [weak self] query in
                guard let self = self else { return }
                Task {
                    await self.performLiveSearch(query: query)
                }
            }
            .store(in: &cancellables)
    }
    
    public func performLiveSearch(query: String) async {
        let trimmed = query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else {
            liveSearchResults = []
            isSearchingLive = false
            return
        }
        
        isSearchingLive = true
        let results = await searchService.search(query: trimmed)
        
        liveSearchResults = results.map { item in
            DestinationItem(
                id: item.id,
                title: item.name,
                subtitle: item.subtitle,
                iconName: "mappin.and.ellipse",
                iconColor: Color(red: 70/255, green: 135/255, blue: 245/255),
                iconBackground: Color(red: 235/255, green: 244/255, blue: 255/255),
                distanceKm: item.distanceKm,
                estimatedMinutes: item.estimatedMinutes,
                waypointCount: max(3, Int(ceil(item.distanceKm * 2.5))),
                latitude: item.coordinate.latitude,
                longitude: item.coordinate.longitude
            )
        }
        isSearchingLive = false
    }
    
    public var displayedPlaces: [DestinationItem] {
        if searchQuery.trimmingCharacters(in: .whitespaces).isEmpty {
            return recentPlaces
        }
        if !liveSearchResults.isEmpty {
            return liveSearchResults
        }
        return recentPlaces.filter {
            $0.title.localizedCaseInsensitiveContains(searchQuery) ||
            $0.subtitle.localizedCaseInsensitiveContains(searchQuery)
        }
    }
    
    public func selectDestination(_ item: DestinationItem) {
        hapticsService.impact(style: .medium)
        speechService.speak("Selected \(item.title). Distance \(String(format: "%.1f", item.distanceKm)) kilometers, \(item.estimatedMinutes) minutes walking.")
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
