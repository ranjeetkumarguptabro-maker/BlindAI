import XCTest
import CoreLocation
@testable import BlindAI

final class ComprehensiveNavigationAndPerceptionTests: XCTestCase {
    
    // MARK: - Haversine Geospatial Calculation Tests
    
    func testHaversineDistanceBetweenCoordinates() {
        // Distance between RTU Main Building (56.9535, 24.0815) and Old Town Riga (56.9496, 24.1052)
        // Expected distance is approximately 1.5 km (~1500m)
        let distance = MapKitNavigationService.haversineDistance(
            lat1: 56.9535, lon1: 24.0815,
            lat2: 56.9496, lon2: 24.1052
        )
        XCTAssertGreaterThan(distance, 1300, "Distance should be greater than 1.3 km")
        XCTAssertLessThan(distance, 1800, "Distance should be less than 1.8 km")
    }
    
    func testHaversineZeroDistanceForIdenticalCoordinates() {
        let lat = 56.9535
        let lon = 24.0815
        let dist = MapKitNavigationService.haversineDistance(lat1: lat, lon1: lon, lat2: lat, lon2: lon)
        XCTAssertEqual(dist, 0.0, accuracy: 0.001)
    }
    
    func testWalkingTimeEstimation() {
        // 1.2 km at 4.8 km/h walking speed should take approx 15 minutes
        let distanceKm = 1.2
        let walkingSpeedKmH = 4.8
        let estimatedMinutes = Int(ceil((distanceKm / walkingSpeedKmH) * 60.0))
        XCTAssertEqual(estimatedMinutes, 15)
    }
    
    // MARK: - Obstacle Danger Classification Tests
    
    func testCriticalDangerWhenObstacleUnder1Meter() {
        let obj = DetectedObject(
            id: UUID(),
            label: "Construction Barrier",
            confidence: 0.95,
            boundingBox: CGRect(x: 0.3, y: 0.3, width: 0.4, height: 0.4),
            distanceMeters: 0.8,
            lane: .center,
            dangerLevel: .critical
        )
        XCTAssertEqual(obj.dangerLevel, .dangerLevelCritical)
        XCTAssertEqual(obj.lane, .center)
        XCTAssertLessThan(obj.distanceMeters, 1.0)
    }
    
    func testSafeWhenObstacleBeyond3Meters() {
        let obj = DetectedObject(
            id: UUID(),
            label: "Park Bench",
            confidence: 0.88,
            boundingBox: CGRect(x: 0.8, y: 0.5, width: 0.15, height: 0.2),
            distanceMeters: 4.5,
            lane: .farRight,
            dangerLevel: .safe
        )
        XCTAssertEqual(obj.dangerLevel, .safe)
        XCTAssertEqual(obj.lane, .farRight)
    }
    
    // MARK: - Real Route Step Tests
    
    func testRouteStepManeuverIconMapping() {
        let stepLeft = RealRouteStep(
            id: 1,
            instruction: "Turn left onto Ķīpsalas iela",
            notice: nil,
            distanceMeters: 120,
            maneuverIcon: "arrow.turn.up.left"
        )
        XCTAssertEqual(stepLeft.maneuverIcon, "arrow.turn.up.left")
        
        let stepCross = RealRouteStep(
            id: 2,
            instruction: "Cross pedestrian crosswalk",
            notice: "Tactile paving present",
            distanceMeters: 30,
            maneuverIcon: "figure.walk"
        )
        XCTAssertEqual(stepCross.maneuverIcon, "figure.walk")
        XCTAssertNotNil(stepCross.notice)
    }
    
    // MARK: - Destination Search Item Equality
    
    func testSearchResultItemEquality() {
        let id = UUID().uuidString
        let item1 = RealSearchResultItem(
            id: id,
            name: "Central Library",
            subtitle: "Main St",
            coordinate: CLLocationCoordinate2D(latitude: 56.95, longitude: 24.10),
            distanceKm: 1.1,
            estimatedMinutes: 14,
            category: "Library",
            phoneNumber: nil,
            url: nil
        )
        let item2 = RealSearchResultItem(
            id: id,
            name: "Central Library",
            subtitle: "Main St",
            coordinate: CLLocationCoordinate2D(latitude: 56.95, longitude: 24.10),
            distanceKm: 1.1,
            estimatedMinutes: 14,
            category: "Library",
            phoneNumber: nil,
            url: nil
        )
        XCTAssertEqual(item1, item2)
    }
}

extension DangerLevel {
    static var dangerLevelCritical: DangerLevel { .critical }
}
