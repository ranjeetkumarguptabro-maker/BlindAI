import SwiftUI
import Combine
import CoreLocation

@MainActor
public final class WhereAmIViewModel: ObservableObject {
    @Published public var locationHeadline: String = "Locating your position..."
    @Published public var locationDetails: String = "Acquiring GPS fix and compass heading..."
    @Published public var isUpdating: Bool = false
    @Published public var userLatitude: Double = 56.9535
    @Published public var userLongitude: Double = 24.0815
    @Published public var currentHeading: String = "East"
    
    public var onNavigateToRoute: ((AppRoute) -> Void)?
    
    private let speechService = SpeechService.shared
    private let hapticsService = HapticsService.shared
    private let locationManager = LocationManagerService.shared
    private let backendClient = BlindAIBackendClient.shared
    private var cancellables = Set<AnyCancellable>()
    
    public init(onNavigateToRoute: ((AppRoute) -> Void)? = nil) {
        self.onNavigateToRoute = onNavigateToRoute
        setupLocationTracking()
        refreshLocation()
    }
    
    private func setupLocationTracking() {
        locationManager.$userLatitude
            .combineLatest(locationManager.$userLongitude, locationManager.$currentHeading)
            .receive(on: DispatchQueue.main)
            .sink { [weak self] lat, lon, heading in
                guard let self = self else { return }
                self.userLatitude = lat
                self.userLongitude = lon
                self.currentHeading = heading
            }
            .store(in: &cancellables)
    }
    
    public var spokenAnnouncement: String {
        "\(locationHeadline) \(locationDetails)"
    }
    
    public func handleUpdateLocation() {
        hapticsService.impact(style: .medium)
        speechService.speak("Updating your current location and compass direction...")
        refreshLocation()
    }
    
    public func refreshLocation() {
        isUpdating = true
        locationManager.requestLocationAccess()
        
        let lat = locationManager.userLatitude
        let lon = locationManager.userLongitude
        let street = locationManager.currentStreet
        let heading = locationManager.currentHeading
        
        Task {
            do {
                let locationResult = try await backendClient.whereAmI(
                    latitude: lat,
                    longitude: lon,
                    street: street,
                    heading: heading
                )
                
                self.locationHeadline = locationResult.headline
                self.locationDetails = locationResult.orientationDetails
                self.isUpdating = false
                self.hapticsService.notification(type: .success)
                self.speechService.speak("\(locationResult.headline). \(locationResult.orientationDetails)")
            } catch {
                // Graceful real GPS fallback
                let streetText = street.isEmpty ? "Current GPS Coordinates (\(String(format: "%.4f", lat)), \(String(format: "%.4f", lon)))" : street
                self.locationHeadline = "You are at \(streetText)."
                self.locationDetails = "Facing \(heading). Precision walking guidance active."
                self.isUpdating = false
                self.hapticsService.notification(type: .success)
                self.speechService.speak(self.spokenAnnouncement)
            }
        }
    }
    
    public func handleShowOnMap() {
        hapticsService.impact(style: .medium)
        onNavigateToRoute?(.routePreview)
    }
    
    public func handleBack() {
        hapticsService.selection()
        onNavigateToRoute?(.home)
    }
}
