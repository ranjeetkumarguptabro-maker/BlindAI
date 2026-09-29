import SwiftUI

public struct WhereAmIView: View {
    @ObservedObject public var viewModel: WhereAmIViewModel
    
    public init(viewModel: WhereAmIViewModel) {
        self.viewModel = viewModel
    }
    
    public var body: some View {
        ZStack(alignment: .bottomTrailing) {
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
                    .accessibilityLabel("Back to home")
                    
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
                .padding(.bottom, 4)
                
                ScrollView(.vertical, showsIndicators: false) {
                    VStack(spacing: 16) {
                        // Glowing 3D Orb
                        GlowingOrb(mode: .home)
                            .padding(.top, 2)
                        
                        // "Where am I?" Title
                        Text("Where am I?")
                            .font(.system(size: 32, weight: .bold))
                            .foregroundColor(.black)
                            .accessibilityAddTraits(.isHeader)
                        
                        // Location Card
                        VStack(alignment: .leading, spacing: 14) {
                            HStack(alignment: .top, spacing: 12) {
                                ZStack {
                                    Circle()
                                        .fill(Color.orange.opacity(0.12))
                                        .frame(width: 36, height: 36)
                                    Image(systemName: "mappin.circle.fill")
                                        .font(.system(size: 20))
                                        .foregroundColor(.orange)
                                }
                                
                                VStack(alignment: .leading, spacing: 8) {
                                    Text(viewModel.locationHeadline)
                                        .font(.system(size: 15.5, weight: .semibold))
                                        .foregroundColor(.black)
                                        .lineSpacing(2)
                                    
                                    Text(viewModel.locationDetails)
                                        .font(.system(size: 13.5))
                                        .foregroundColor(Color(red: 70/255, green: 70/255, blue: 75/255))
                                        .lineSpacing(3)
                                }
                            }
                            
                            // Visual Landmark Photo Representation (RTU Building)
                            ZStack {
                                // Background sky & building structure
                                LinearGradient(
                                    colors: [Color(red: 175/255, green: 215/255, blue: 245/255), Color(red: 220/255, green: 235/255, blue: 245/255)],
                                    startPoint: .top,
                                    endPoint: .bottom
                                )
                                
                                // Modern building facade
                                VStack(spacing: 0) {
                                    Spacer()
                                    HStack(spacing: 10) {
                                        // Left wing
                                        RoundedRectangle(cornerRadius: 4)
                                            .fill(Color(red: 230/255, green: 232/255, blue: 235/255))
                                            .frame(width: 100, height: 75)
                                        
                                        // Main modern glass building
                                        ZStack {
                                            RoundedRectangle(cornerRadius: 6)
                                                .fill(Color(red: 45/255, green: 80/255, blue: 110/255))
                                                .frame(width: 170, height: 95)
                                            
                                            // Glass reflections
                                            Rectangle()
                                                .fill(LinearGradient(colors: [Color.white.opacity(0.3), Color.clear], startPoint: .topLeading, endPoint: .bottomTrailing))
                                                .frame(width: 170, height: 95)
                                            
                                            // RTU Sign
                                            Text("RTU")
                                                .font(.system(size: 24, weight: .black))
                                                .foregroundColor(.white)
                                        }
                                        
                                        Spacer()
                                    }
                                    .padding(.horizontal, 10)
                                    
                                    // Paved forecourt & trees
                                    ZStack {
                                        Rectangle()
                                            .fill(Color(red: 215/255, green: 215/255, blue: 215/255))
                                            .frame(height: 35)
                                        
                                        HStack {
                                            Circle().fill(Color(red: 60/255, green: 140/255, blue: 50/255)).frame(width: 28, height: 28)
                                            Spacer()
                                            Circle().fill(Color(red: 70/255, green: 150/255, blue: 60/255)).frame(width: 32, height: 32)
                                        }
                                        .padding(.horizontal, 14)
                                    }
                                }
                            }
                            .frame(height: 145)
                            .clipShape(RoundedRectangle(cornerRadius: 14, style: .continuous))
                            .overlay(
                                RoundedRectangle(cornerRadius: 14, style: .continuous)
                                    .stroke(Color.black.opacity(0.04), lineWidth: 1)
                            )
                        }
                        .padding(16)
                        .background(Color.white)
                        .clipShape(RoundedRectangle(cornerRadius: 22, style: .continuous))
                        .shadow(color: Color.black.opacity(0.03), radius: 8, x: 0, y: 2)
                        
                        // Action Buttons Stack
                        VStack(spacing: 12) {
                            // Secondary button: Update location
                            SecondaryButton(
                                title: viewModel.isUpdating ? "Updating..." : "Update location",
                                iconName: "arrow.clockwise"
                            ) {
                                viewModel.handleUpdateLocation()
                            }
                            
                            // Primary button: Show on map
                            PrimaryButton(
                                title: "Show on map",
                                iconName: "map.fill"
                            ) {
                                viewModel.handleShowOnMap()
                            }
                        }
                        .padding(.top, 4)
                        .padding(.bottom, 40)
                    }
                    .padding(.horizontal, BlindAISpacing.screenPadding)
                }
            }
            
            // Subtle speaker repeat button
            SpeakerButton(textToRepeat: viewModel.spokenAnnouncement)
                .padding(.trailing, 20)
                .padding(.bottom, 24)
        }
    }
}
