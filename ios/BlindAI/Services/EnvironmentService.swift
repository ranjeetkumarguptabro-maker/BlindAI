import Foundation
import CoreLocation

public struct LocationContext {
    public let street: String
    public let landmark: String
    public let headingDescription: String
    public let coordinate: CLLocationCoordinate2D
    
    public var spokenDescription: String {
        "You are at \(landmark) in Riga, Latvia. Facing \(headingDescription) near the main entrance."
    }
}

public struct SceneDescription {
    public let summary: String
    public let hazardStatus: String
    public let walkingSurface: String
    
    public var spokenDescription: String {
        "\(summary) Walking surface: \(walkingSurface). \(hazardStatus)"
    }
}

public final class EnvironmentService: ObservableObject {
    public static let shared = EnvironmentService()
    
    @Published public private(set) var currentLocationContext: LocationContext = LocationContext(
        street: "Paula Valdena iela",
        landmark: "Riga Technical University (RTU), Ķīpsala Campus",
        headingDescription: "East",
        coordinate: CLLocationCoordinate2D(latitude: 56.9535, longitude: 24.0818)
    )
    
    @Published public private(set) var currentScene: SceneDescription = SceneDescription(
        summary: "Pedestrian pathway clear directly ahead. Sidewalk continues for 41 meters.",
        hazardStatus: "No immediate obstacles detected in your lane.",
        walkingSurface: "Paved concrete sidewalk"
    )
    
    private let backendClient = BlindAIBackendClient.shared
    
    private init() {}
    
    public func queryWhereAmI(completion: @escaping (String) -> Void) {
        Task {
            do {
                let result = try await backendClient.whereAmI(
                    latitude: currentLocationContext.coordinate.latitude,
                    longitude: currentLocationContext.coordinate.longitude,
                    heading: currentLocationContext.headingDescription
                )
                let text = "\(result.headline) \(result.orientation)"
                DispatchQueue.main.async {
                    completion(text)
                }
            } catch {
                // Fallback to local context if backend is offline
                DispatchQueue.main.async {
                    completion(self.currentLocationContext.spokenDescription)
                }
            }
        }
    }
    
    public func describeEnvironment(completion: @escaping (String) -> Void) {
        // If LiDAR currently detects an obstacle in front of user, announce immediate spatial details
        if let obstacle = ARKitLiDARScannerService.shared.nearestObstacle {
            let roundedMeters = Int(round(obstacle.distanceMeters))
            let distText = roundedMeters <= 1 ? "one meter" : "\(roundedMeters) meters"
            let sideText: String
            switch obstacle.lane {
            case .left: sideText = "on your left"
            case .right: sideText = "on your right"
            case .center: sideText = "directly ahead"
            }
            let liveDescription = "There is a \(obstacle.label.lowercased()) approximately \(distText) ahead \(sideText)."
            DispatchQueue.main.async {
                completion(liveDescription)
            }
            return
        }
        
        Task {
            do {
                let description = try await backendClient.describeEnvironment()
                DispatchQueue.main.async {
                    completion(description)
                }
            } catch {
                // Fallback to local scene description if backend is offline
                DispatchQueue.main.async {
                    completion(self.currentScene.spokenDescription)
                }
            }
        }
    }
}
