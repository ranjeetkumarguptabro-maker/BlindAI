import SwiftUI

public struct ObstacleAlertView: View {
    @ObservedObject public var viewModel: ObstacleAlertViewModel
    
    public init(viewModel: ObstacleAlertViewModel) {
        self.viewModel = viewModel
    }
    
    public var body: some View {
        ZStack {
            Color.blindAIBackground
                .ignoresSafeArea()
            
            VStack(spacing: 12) {
                // Top Header
                BlindAIHeader(
                    showBackButton: true,
                    onBackTapped: {
                        viewModel.handleBackTapped()
                    },
                    onSettingsTapped: {
                        viewModel.handleSettingsTapped()
                    }
                )
                .padding(.horizontal, BlindAISpacing.screenHorizontal)
                .padding(.top, 4)
                
                // Top Warning Alert Banner
                HStack(alignment: .center, spacing: 16) {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .font(.system(size: 34, weight: .bold))
                        .foregroundColor(Color(red: 0.92, green: 0.15, blue: 0.15))
                        .frame(width: 44, alignment: .center)
                    
                    VStack(alignment: .leading, spacing: 4) {
                        Text(viewModel.hazard.title)
                            .font(.system(size: 22, weight: .bold))
                            .foregroundColor(Color(red: 0.92, green: 0.15, blue: 0.15))
                        
                        Text(viewModel.hazard.subtitle)
                            .font(.system(size: 14, weight: .regular))
                            .foregroundColor(Color(red: 0.20, green: 0.20, blue: 0.22))
                            .lineSpacing(2)
                    }
                    
                    Spacer()
                }
                .padding(.horizontal, 18)
                .padding(.vertical, 16)
                .background(Color(red: 1.0, green: 0.925, blue: 0.925))
                .clipShape(RoundedRectangle(cornerRadius: 22, style: .continuous))
                .overlay(
                    RoundedRectangle(cornerRadius: 22, style: .continuous)
                        .stroke(Color(red: 0.98, green: 0.80, blue: 0.80), lineWidth: 1)
                )
                .padding(.horizontal, BlindAISpacing.screenHorizontal)
                .accessibilityElement(children: .combine)
                .accessibilityLabel("Warning: Obstacle ahead. Two meters ahead, construction barrier on right.")
                
                // Camera View with AR Path and Barrier Highlight
                ZStack(alignment: .bottom) {
                    // Camera feed image
                    Group {
                        if let uiImage = UIImage(named: "scene_obstacle_barrier") {
                            Image(uiImage: uiImage)
                                .resizable()
                                .aspectRatio(contentMode: .fill)
                        } else {
                            Color.slate800
                        }
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                    .clipShape(RoundedRectangle(cornerRadius: 24, style: .continuous))
                    .shadow(color: Color.black.opacity(0.10), radius: 10, x: 0, y: 4)
                    
                    // Floating obstacle detail card inside camera view
                    HStack(spacing: 14) {
                        // Traffic Cone Icon
                        ZStack {
                            Circle()
                                .fill(Color(red: 1.0, green: 0.94, blue: 0.88))
                                .frame(width: 42, height: 42)
                            
                            Image(systemName: "cone.fill")
                                .font(.system(size: 22))
                                .foregroundColor(Color(red: 0.98, green: 0.45, blue: 0.05))
                        }
                        
                        VStack(alignment: .leading, spacing: 2) {
                            Text(viewModel.hazard.cardTitle)
                                .font(.system(size: 16, weight: .bold))
                                .foregroundColor(Color.blindAITextPrimary)
                            
                            Text(viewModel.hazard.cardSubtitle)
                                .font(.system(size: 13, weight: .regular))
                                .foregroundColor(Color.blindAITextSecondary)
                        }
                        
                        Spacer()
                    }
                    .padding(.horizontal, 16)
                    .padding(.vertical, 14)
                    .background(Color.white)
                    .clipShape(RoundedRectangle(cornerRadius: 20, style: .continuous))
                    .shadow(color: Color.black.opacity(0.12), radius: 10, x: 0, y: 4)
                    .padding(.horizontal, 14)
                    .padding(.bottom, 16)
                }
                .padding(.horizontal, BlindAISpacing.screenHorizontal)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                
                // Bottom Action Buttons
                VStack(spacing: 12) {
                    // 1. Repeat Button (White Pill)
                    Button(action: {
                        viewModel.repeatAlert()
                    }) {
                        HStack(spacing: 8) {
                            Image(systemName: "speaker.wave.2.fill")
                                .font(.system(size: 16, weight: .semibold))
                            Text("Repeat")
                                .font(.system(size: 16, weight: .semibold))
                        }
                        .foregroundColor(Color.blindAITextPrimary)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 14)
                        .background(Color.white)
                        .clipShape(Capsule())
                        .shadow(color: Color.black.opacity(0.06), radius: 6, x: 0, y: 2)
                        .overlay(
                            Capsule()
                                .stroke(Color.slate200, lineWidth: 1)
                        )
                    }
                    .accessibilityLabel("Repeat obstacle alert")
                    
                    // 2. I Understand Button (Black Pill)
                    Button(action: {
                        viewModel.acknowledgeObstacle()
                    }) {
                        HStack(spacing: 8) {
                            Image(systemName: "xmark")
                                .font(.system(size: 16, weight: .bold))
                            Text("I Understand")
                                .font(.system(size: 16, weight: .bold))
                        }
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 14)
                        .background(Color(red: 0.12, green: 0.12, blue: 0.14))
                        .clipShape(Capsule())
                        .shadow(color: Color.black.opacity(0.18), radius: 8, x: 0, y: 3)
                    }
                    .accessibilityLabel("I Understand obstacle, resume route")
                }
                .padding(.horizontal, BlindAISpacing.screenHorizontal)
                .padding(.bottom, 18)
            }
        }
        .onAppear {
            viewModel.handleOnAppear()
        }
    }
}

#Preview {
    ObstacleAlertView(viewModel: ObstacleAlertViewModel())
}
