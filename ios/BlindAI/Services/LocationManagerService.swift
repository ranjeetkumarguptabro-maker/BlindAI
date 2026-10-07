import Foundation
import CoreLocation
import Combine

/// Service managing CoreLocation GPS tracking and automatic origin coordinate acquisition
public final class LocationManagerService: NSObject, ObservableObject, CLLocationManagerDelegate {
    public static let shared = LocationManagerService()
    
    @Published public private(set) var userLatitude: Double = 56.9535
    @Published public private(set) var userLongitude: Double = 24.0815
    @Published public private(set) var currentStreet: String = "Paula Valdena iela"
    @Published public private(set) var currentHeading: String = "East"
    @Published public private(set) var hasLocationPermission: Bool = false
    
    private let locationManager = CLLocationManager()
    private let geocoder = CLGeocoder()
    
    public override init() {
        super.init()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
        locationManager.distanceFilter = 2.0 // Update every 2 meters walked
    }
    
    public func requestLocationAccess() {
        locationManager.requestWhenInUseAuthorization()
        locationManager.startUpdatingLocation()
        locationManager.startUpdatingHeading()
    }
    
    // MARK: - CLLocationManagerDelegate
    
    public func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        switch manager.authorizationStatus {
        case .authorizedWhenInUse, .authorizedAlways:
            hasLocationPermission = true
            locationManager.startUpdatingLocation()
            locationManager.startUpdatingHeading()
        default:
            hasLocationPermission = false
        }
    }
    
    public func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }
        DispatchQueue.main.async {
            self.userLatitude = location.coordinate.latitude
            self.userLongitude = location.coordinate.longitude
        }
        
        // Reverse geocode to determine street name for accessibility announcement
        geocoder.reverseGeocodeLocation(location) { [weak self] placemarks, _ in
            guard let self = self, let place = placemarks?.first else { return }
            DispatchQueue.main.async {
                if let thoroughfare = place.thoroughfare {
                    self.currentStreet = thoroughfare
                }
            }
        }
    }
    
    public func locationManager(_ manager: CLLocationManager, didUpdateHeading newHeading: CLHeading) {
        let degrees = newHeading.trueHeading >= 0 ? newHeading.trueHeading : newHeading.magneticHeading
        let headingText: String
        switch degrees {
        case 337.5...360.0, 0.0..<22.5: headingText = "North"
        case 22.5..<67.5: headingText = "Northeast"
        case 67.5..<112.5: headingText = "East"
        case 112.5..<157.5: headingText = "Southeast"
        case 157.5..<202.5: headingText = "South"
        case 202.5..<247.5: headingText = "Southwest"
        case 247.5..<292.5: headingText = "West"
        default: headingText = "Northwest"
        }
        DispatchQueue.main.async {
            self.currentHeading = headingText
        }
    }
}
