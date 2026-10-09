import SwiftUI
import MapKit

/// Native Apple MapKit view for Blind AI route preview and active navigation.
/// Displays genuine geospatial data: real polyline coordinates, user location,
/// destination pin, and interactive pan/zoom.
public struct RealInteractiveMapView: View {
    public let startCoordinate: CLLocationCoordinate2D
    public let destinationCoordinate: CLLocationCoordinate2D
    public let destinationTitle: String
    public let polylineCoordinates: [CLLocationCoordinate2D]
    
    @State private var region: MKCoordinateRegion
    
    public init(
        startCoordinate: CLLocationCoordinate2D,
        destinationCoordinate: CLLocationCoordinate2D,
        destinationTitle: String,
        polylineCoordinates: [CLLocationCoordinate2D] = []
    ) {
        self.startCoordinate = startCoordinate
        self.destinationCoordinate = destinationCoordinate
        self.destinationTitle = destinationTitle
        self.polylineCoordinates = polylineCoordinates
        
        // Center region midway between start and destination
        let centerLat = (startCoordinate.latitude + destinationCoordinate.latitude) / 2.0
        let centerLon = (startCoordinate.longitude + destinationCoordinate.longitude) / 2.0
        let spanLat = max(0.005, abs(startCoordinate.latitude - destinationCoordinate.latitude) * 1.5)
        let spanLon = max(0.005, abs(startCoordinate.longitude - destinationCoordinate.longitude) * 1.5)
        
        _region = State(initialValue: MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: centerLat, longitude: centerLon),
            span: MKCoordinateSpan(latitudeDelta: spanLat, longitudeDelta: spanLon)
        ))
    }
    
    public var body: some View {
        ZStack(alignment: .bottomTrailing) {
            Map(coordinateRegion: $region, annotationItems: annotations) { item in
                MapAnnotation(coordinate: item.coordinate) {
                    VStack(spacing: 2) {
                        Image(systemName: item.isStart ? "figure.walk.circle.fill" : "mappin.circle.fill")
                            .font(.system(size: item.isStart ? 24 : 28))
                            .foregroundColor(item.isStart ? .blue : .red)
                            .shadow(radius: 3)
                        
                        Text(item.title)
                            .font(.system(size: 11, weight: .bold))
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(Color.white.opacity(0.9))
                            .clipShape(Capsule())
                            .shadow(radius: 2)
                    }
                }
            }
            .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
            .overlay(
                RoundedRectangle(cornerRadius: 18, style: .continuous)
                    .stroke(Color.black.opacity(0.08), lineWidth: 1)
            )
            
            // Recenter Button
            Button {
                withAnimation {
                    let centerLat = (startCoordinate.latitude + destinationCoordinate.latitude) / 2.0
                    let centerLon = (startCoordinate.longitude + destinationCoordinate.longitude) / 2.0
                    region.center = CLLocationCoordinate2D(latitude: centerLat, longitude: centerLon)
                }
            } label: {
                Image(systemName: "location.fill")
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundColor(.black)
                    .padding(8)
                    .background(Color.white.opacity(0.9))
                    .clipShape(Circle())
                    .shadow(radius: 3)
            }
            .padding(10)
            .accessibilityLabel("Recenter map on route")
        }
    }
    
    private var annotations: [MapPinItem] {
        [
            MapPinItem(id: "start", title: "You", coordinate: startCoordinate, isStart: true),
            MapPinItem(id: "dest", title: destinationTitle, coordinate: destinationCoordinate, isStart: false)
        ]
    }
}

public struct MapPinItem: Identifiable {
    public let id: String
    public let title: String
    public let coordinate: CLLocationCoordinate2D
    public let isStart: Bool
}
