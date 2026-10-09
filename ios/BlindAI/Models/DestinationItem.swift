import SwiftUI
import CoreLocation

public struct DestinationItem: Identifiable, Hashable {
    public let id: String
    public let title: String
    public let subtitle: String
    public let iconName: String
    public let iconColor: Color
    public let iconBackground: Color
    public let distanceKm: Double
    public let estimatedMinutes: Int
    public let waypointCount: Int
    public let latitude: Double
    public let longitude: Double
    
    public var coordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }
    
    public init(
        id: String = UUID().uuidString,
        title: String,
        subtitle: String,
        iconName: String,
        iconColor: Color,
        iconBackground: Color,
        distanceKm: Double = 2.4,
        estimatedMinutes: Int = 28,
        waypointCount: Int = 8,
        latitude: Double = 56.9535,
        longitude: Double = 24.0815
    ) {
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.iconName = iconName
        self.iconColor = iconColor
        self.iconBackground = iconBackground
        self.distanceKm = distanceKm
        self.estimatedMinutes = estimatedMinutes
        self.waypointCount = waypointCount
        self.latitude = latitude
        self.longitude = longitude
    }
    
    public static let rtu = DestinationItem(
        id: "rtu",
        title: "Riga Technical University (RTU)",
        subtitle: "Ķīpsala, Rīga",
        iconName: "graduationcap.fill",
        iconColor: Color(red: 120/255, green: 110/255, blue: 235/255),
        iconBackground: Color(red: 238/255, green: 237/255, blue: 255/255),
        distanceKm: 2.4,
        estimatedMinutes: 28,
        waypointCount: 8,
        latitude: 56.9535,
        longitude: 24.0815
    )
    
    public static let kipsalaCampus = DestinationItem(
        id: "kipsala",
        title: "Ķīpsala Campus",
        subtitle: "Ķīpsala, Rīga",
        iconName: "building.2.fill",
        iconColor: Color(red: 65/255, green: 130/255, blue: 240/255),
        iconBackground: Color(red: 235/255, green: 244/255, blue: 255/255),
        distanceKm: 2.2,
        estimatedMinutes: 26,
        waypointCount: 7
    )
    
    public static let rigaCentralStation = DestinationItem(
        id: "station",
        title: "Rīga Central Station",
        subtitle: "Rīga",
        iconName: "tram.fill",
        iconColor: Color(red: 70/255, green: 135/255, blue: 245/255),
        iconBackground: Color(red: 235/255, green: 244/255, blue: 255/255),
        distanceKm: 1.8,
        estimatedMinutes: 22,
        waypointCount: 6
    )
}

public struct NearbyCategory: Identifiable, Hashable {
    public let id: String
    public let title: String
    public let iconName: String
    public let iconColor: Color
    public let iconBackground: Color
    
    public init(id: String, title: String, iconName: String, iconColor: Color, iconBackground: Color) {
        self.id = id
        self.title = title
        self.iconName = iconName
        self.iconColor = iconColor
        self.iconBackground = iconBackground
    }
}
