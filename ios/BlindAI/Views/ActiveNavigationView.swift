import SwiftUI

public struct ActiveNavigationView: View {
    @ObservedObject public var viewModel: ActiveNavigationViewModel
    
    public init(viewModel: ActiveNavigationViewModel) {
        self.viewModel = viewModel
    }
    
    public var body: some View {
        ZStack(alignment: .bottomTrailing) {
            Color.blindAIBackground
                .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Header
                BlindAIHeader()
                
                ScrollView(.vertical, showsIndicators: false) {
                    VStack(spacing: 16) {
                        // Compact Glowing Orb centered above instruction card
                        GlowingOrb(mode: .compact)
                            .padding(.top, 4)
                            .padding(.bottom, 2)
                        
                        // Main Navigation Card (Live instruction & distance)
                        NavigationInstructionCard(instruction: viewModel.instruction)
                            .padding(.horizontal, BlindAISpacing.screenPadding)
                        
                        // Action Buttons Stack
                        VStack(spacing: 12) {
                            // Secondary light button: "Show more details"
                            SecondaryButton(
                                title: "Show more details",
                                iconName: "mappin"
                            ) {
                                viewModel.handleShowDetails()
                            }
                            
                            // Primary black button: "Stop route"
                            PrimaryButton(
                                title: "Stop route",
                                iconName: "square.fill"
                            ) {
                                viewModel.handleStopRoute()
                            }
                            
                            // Test triggers for safety workflow
                            HStack(spacing: 10) {
                                Button(action: {
                                    viewModel.triggerObstacleAlert()
                                }) {
                                    HStack(spacing: 6) {
                                        Image(systemName: "exclamationmark.triangle.fill")
                                            .foregroundColor(.red)
                                        Text("Obstacle Alert")
                                            .font(.system(size: 13, weight: .semibold))
                                            .foregroundColor(.black)
                                    }
                                    .padding(.vertical, 9)
                                    .padding(.horizontal, 12)
                                    .background(Color.white)
                                    .clipShape(RoundedRectangle(cornerRadius: 12))
                                    .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 1)
                                }
                                
                                Button(action: {
                                    viewModel.triggerCrosswalkSafety()
                                }) {
                                    HStack(spacing: 6) {
                                        Image(systemName: "figure.walk")
                                            .foregroundColor(.black)
                                        Text("Crosswalk")
                                            .font(.system(size: 13, weight: .semibold))
                                            .foregroundColor(.black)
                                    }
                                    .padding(.vertical, 9)
                                    .padding(.horizontal, 12)
                                    .background(Color.white)
                                    .clipShape(RoundedRectangle(cornerRadius: 12))
                                    .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 1)
                                }
                            }
                            .padding(.top, 4)
                        }
                        .padding(.horizontal, BlindAISpacing.screenPadding)
                        .padding(.top, 8)
                        .padding(.bottom, 28)
                    }
                }
            }
            
            // Subtle speaker repeat button
            SpeakerButton(textToRepeat: viewModel.instruction.spokenAnnouncement) {
                viewModel.repeatCurrentInstruction()
            }
            .padding(.trailing, 20)
            .padding(.bottom, 24)
        }
        .alert("Route Details", isPresented: $viewModel.isShowingDetails) {
            Button("OK", role: .cancel) {}
        } message: {
            Text("Waypoint \(viewModel.currentWaypoint) of \(viewModel.totalWaypoints)\nHeading: North towards CIF\nSurface: Paved Sidewalk, level\nObstacles: Path clear\nRemaining Distance: \(viewModel.instruction.distanceValue) meters")
        }
    }
}

#Preview {
    ActiveNavigationView(viewModel: ActiveNavigationViewModel())
}
