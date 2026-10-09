import SwiftUI

public struct RoutePreviewView: View {
    @ObservedObject public var viewModel: RoutePreviewViewModel
    
    public init(viewModel: RoutePreviewViewModel) {
        self.viewModel = viewModel
    }
    
    public var body: some View {
        ZStack(alignment: .bottom) {
            Color.blindAIBackground
                .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Header with Back button and Settings
                HStack {
                    Button {
                        viewModel.handleBack()
                    } label: {
                        ZStack {
                            Circle()
                                .fill(Color(red: 236/255, green: 236/255, blue: 238/255))
                                .frame(width: 38, height: 38)
                            Image(systemName: "arrow.left")
                                .font(.system(size: 16, weight: .semibold))
                                .foregroundColor(.black)
                        }
                    }
                    .accessibilityLabel("Back to destination search")
                    
                    Spacer()
                    
                    Text("Blind AI")
                        .font(.blindAIHeaderTitle)
                        .foregroundColor(.blindAITextPrimary)
                    
                    Spacer()
                    
                    Button {} label: {
                        ZStack {
                            Circle()
                                .fill(Color(red: 236/255, green: 236/255, blue: 238/255))
                                .frame(width: 38, height: 38)
                            Image(systemName: "gearshape.fill")
                                .font(.system(size: 16, weight: .semibold))
                                .foregroundColor(.black)
                        }
                    }
                    .accessibilityLabel("Settings")
                }
                .padding(.horizontal, BlindAISpacing.screenPadding)
                .padding(.top, 10)
                .padding(.bottom, 6)
                
                ScrollView(.vertical, showsIndicators: false) {
                    VStack(spacing: 14) {
                        // Destination Overview Card
                        HStack(spacing: 12) {
                            ZStack {
                                RoundedRectangle(cornerRadius: 12, style: .continuous)
                                    .fill(Color.orange.opacity(0.12))
                                    .frame(width: 42, height: 42)
                                
                                Image(systemName: "mappin.circle.fill")
                                    .font(.system(size: 22))
                                    .foregroundColor(.orange)
                            }
                            
                            VStack(alignment: .leading, spacing: 2) {
                                Text(viewModel.destination.title)
                                    .font(.system(size: 16.5, weight: .bold))
                                    .foregroundColor(.black)
                                
                                Text("\(viewModel.destination.subtitle) • \(String(format: "%.1f", viewModel.destination.distanceKm)) km • \(viewModel.destination.estimatedMinutes) min • \(viewModel.destination.waypointCount) waypoints")
                                    .font(.system(size: 12))
                                    .foregroundColor(.neutral500)
                            }
                            
                            Spacer()
                        }
                        .padding(14)
                        .background(Color.white)
                        .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
                        .shadow(color: Color.black.opacity(0.03), radius: 6, x: 0, y: 2)
                        
                        // Real Interactive MapView (MapKit with dynamic coordinates)
                        RealInteractiveMapView(
                            startCoordinate: CLLocationCoordinate2D(
                                latitude: LocationManagerService.shared.userLatitude,
                                longitude: LocationManagerService.shared.userLongitude
                            ),
                            destinationCoordinate: viewModel.destination.coordinate,
                            destinationTitle: viewModel.destination.title
                        )
                        .frame(height: 200)
                            .overlay(
                                RoundedRectangle(cornerRadius: 18, style: .continuous)
                                    .stroke(Color.black.opacity(0.04), lineWidth: 1)
                            )
                            
                            // Compass button on map
                            Button {} label: {
                                Image(systemName: "location.north.fill")
                                    .font(.system(size: 14))
                                    .foregroundColor(.black)
                                    .padding(8)
                                    .background(Color.white)
                                    .clipShape(Circle())
                                    .shadow(color: Color.black.opacity(0.1), radius: 3)
                            }
                            .padding(10)
                        }
                        
                        // Turn-by-turn Step List Card
                        VStack(spacing: 0) {
                            ForEach(Array(viewModel.steps.enumerated()), id: \.offset) { index, step in
                                HStack(spacing: 12) {
                                    ZStack {
                                        Circle()
                                            .fill(Color(red: 235/255, green: 244/255, blue: 255/255))
                                            .frame(width: 32, height: 32)
                                        Image(systemName: step.iconName)
                                            .font(.system(size: 13, weight: .bold))
                                            .foregroundColor(Color(red: 30/255, green: 120/255, blue: 245/255))
                                    }
                                    
                                    VStack(alignment: .leading, spacing: 1) {
                                        Text(step.instruction)
                                            .font(.system(size: 14.5, weight: .medium))
                                            .foregroundColor(.black)
                                        Text(step.distance)
                                            .font(.system(size: 12))
                                            .foregroundColor(.neutral500)
                                    }
                                    
                                    Spacer()
                                }
                                .padding(.horizontal, 14)
                                .padding(.vertical, 10)
                                
                                if index < viewModel.steps.count - 1 {
                                    Divider().padding(.leading, 58)
                                }
                            }
                            
                            Divider().padding(.leading, 58)
                            
                            // 4 more steps footer
                            HStack {
                                Text("•••  4 more steps")
                                    .font(.system(size: 14, weight: .medium))
                                    .foregroundColor(.neutral700)
                                Spacer()
                                Image(systemName: "chevron.right")
                                    .font(.system(size: 13, weight: .semibold))
                                    .foregroundColor(Color(red: 200/255, green: 200/255, blue: 202/255))
                            }
                            .padding(.horizontal, 14)
                            .padding(.vertical, 12)
                        }
                        .background(Color.white)
                        .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
                        .shadow(color: Color.black.opacity(0.03), radius: 6, x: 0, y: 2)
                        
                        Spacer(minLength: 80)
                    }
                    .padding(.horizontal, BlindAISpacing.screenPadding)
                }
            }
            
            // Bottom Action Bar: Start Navigation Button + Speaker
            HStack(spacing: 12) {
                Button {
                    viewModel.handleStartNavigation()
                } label: {
                    HStack(spacing: 8) {
                        Image(systemName: "play.fill")
                            .font(.system(size: 15))
                        Text("Start navigation")
                            .font(.system(size: 16, weight: .bold))
                    }
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .frame(height: 54)
                    .background(Color.black)
                    .clipShape(Capsule())
                    .shadow(color: Color.black.opacity(0.12), radius: 8, x: 0, y: 3)
                }
                
                SpeakerButton(textToRepeat: viewModel.spokenSummary)
            }
            .padding(.horizontal, BlindAISpacing.screenPadding)
            .padding(.bottom, 20)
        }
    }
}
