import Foundation
import MapKit
import CoreLocation
import Combine

/// Real-world destination search engine for Blind AI.
/// Uses Apple's MKLocalSearch to find genuine places, businesses, transit stops,
/// and addresses anywhere worldwide based on user queries or voice commands.
public final class DestinationSearchService: ObservableObject {
    public static let shared = DestinationSearchService()
    
    @Published public private(set) var searchResults: [RealSearchResultItem] = []
    @Published public private(set) var isSearching: Bool = false
    @Published public private(set) var lastSearchQuery: String = ""
    
    private let locationManager = LocationManagerService.shared
    
    public init() {}
    
    /// Searches for any real place worldwide centered around the user's current GPS location
    public func search(query: String) async -> [RealSearchResultItem] {
        let trimmed = query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else {
            await MainActor.run {
                self.searchResults = []
                self.isSearching = false
            }
            return []
        }
        
        await MainActor.run {
            self.isSearching = true
            self.lastSearchQuery = trimmed
        }
        
        let request = MKLocalSearch.Request()
        request.naturalLanguageQuery = trimmed
        
        // Center search around user's genuine GPS coordinates
        let userCoord = CLLocationCoordinate2D(
            latitude: locationManager.userLatitude,
            longitude: locationManager.userLongitude
        )
        request.region = MKCoordinateRegion(
            center: userCoord,
            latitudinalMeters: 25_000,
            longitudinalMeters: 25_000
        )
        request.resultTypes = [.pointOfInterest, .address]
        
        let localSearch = MKLocalSearch(request: request)
        
        do {
            let response = try await localSearch.start()
            let items: [RealSearchResultItem] = response.mapItems.compactMap { mapItem in
                guard let name = mapItem.name else { return nil }
                let coord = mapItem.placemark.coordinate
                
                // Calculate real distance from user
                let distMeters = MapKitNavigationService.haversineDistance(
                    lat1: userCoord.latitude, lon1: userCoord.longitude,
                    lat2: coord.latitude, lon2: coord.longitude
                )
                let distKm = distMeters / 1000.0
                let walkingMins = max(1, Int(ceil((distKm / 4.8) * 60.0)))
                
                let subtitle = mapItem.placemark.title ?? "\(String(format: "%.1f", distKm)) km away"
                let categoryName = mapItem.pointOfInterestCategory?.rawValue
                    .replacingOccurrences(of: "MKPointOfInterestCategory", with: "") ?? "Place"
                
                return RealSearchResultItem(
                    id: UUID().uuidString,
                    name: name,
                    subtitle: subtitle,
                    coordinate: coord,
                    distanceKm: distKm,
                    estimatedMinutes: walkingMins,
                    category: categoryName,
                    phoneNumber: mapItem.phoneNumber,
                    url: mapItem.url
                )
            }
            
            await MainActor.run {
                self.searchResults = items
                self.isSearching = false
            }
            return items
        } catch {
            await MainActor.run {
                self.searchResults = []
                self.isSearching = false
            }
            return []
        }
    }
}

public struct RealSearchResultItem: Identifiable, Equatable {
    public let id: String
    public let name: String
    public let subtitle: String
    public let coordinate: CLLocationCoordinate2D
    public let distanceKm: Double
    public let estimatedMinutes: Int
    public let category: String
    public let phoneNumber: String?
    public let url: URL?
    
    public static func == (lhs: RealSearchResultItem, rhs: RealSearchResultItem) -> Bool {
        lhs.id == rhs.id
    }
}
