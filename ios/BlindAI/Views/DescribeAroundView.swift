import SwiftUI

public struct DescribeAroundView: View {
    @ObservedObject public var viewModel: DescribeAroundViewModel
    
    public init(viewModel: DescribeAroundViewModel) {
        self.viewModel = viewModel
    }
    
    public var body: some View {
        ZStack {
            Color.blindAIBackground
                .ignoresSafeArea()
            
            VStack(spacing: 0) {
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
                
                ScrollView(.vertical, showsIndicators: false) {
                    VStack(spacing: 16) {
                        // Glowing Orb (compact)
                        GlowingOrb(size: 78, isPulsing: true)
                            .padding(.top, 4)
                            .accessibilityLabel("Visual Perception Orb Active")
                        
                        // Main Heading
                        Text("Here’s what I see:")
                            .font(.system(size: 26, weight: .bold, design: .default))
                            .foregroundColor(Color.blindAITextPrimary)
                            .frame(maxWidth: .infinity, alignment: .center)
                            .accessibilityHeading(.h1)
                        
                        // Scene Live Camera Preview Card
                        ZStack {
                            if CameraCaptureService.shared.hasCameraPermission {
                                CameraPreviewView(captureSession: CameraCaptureService.shared.captureSession)
                            } else {
                                RoundedRectangle(cornerRadius: 20, style: .continuous)
                                    .fill(Color.slate200)
                                LinearGradient(
                                    colors: [Color.blue.opacity(0.3), Color.green.opacity(0.3)],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                                VStack {
                                    Image(systemName: "camera.viewfinder")
                                        .font(.system(size: 36))
                                        .foregroundColor(.white)
                                    Text("Live Camera Feed")
                                        .font(.caption)
                                        .foregroundColor(.white)
                                }
                            }
                        }
                        .frame(maxWidth: .infinity)
                        .frame(height: 175)
                        .clipShape(RoundedRectangle(cornerRadius: 20, style: .continuous))
                        .shadow(color: Color.black.opacity(0.06), radius: 8, x: 0, y: 3)
                        .accessibilityLabel("Forward live camera perception view")
                        
                        // Environmental Items List Card
                        VStack(spacing: 0) {
                            ForEach(Array(viewModel.items.enumerated()), id: \.element.id) { index, item in
                                HStack(alignment: .center, spacing: 14) {
                                    Image(systemName: item.iconSystemName)
                                        .font(.system(size: 22, weight: .semibold))
                                        .foregroundColor(item.iconColor)
                                        .frame(width: 30, alignment: .center)
                                    
                                    VStack(alignment: .leading, spacing: 2) {
                                        Text(item.title)
                                            .font(.system(size: 15, weight: .semibold))
                                            .foregroundColor(Color.blindAITextPrimary)
                                        
                                        if let subtitle = item.subtitle {
                                            Text(subtitle)
                                                .font(.system(size: 13, weight: .regular))
                                                .foregroundColor(Color.blindAITextSecondary)
                                        }
                                    }
                                    
                                    Spacer()
                                }
                                .padding(.vertical, 12)
                                .padding(.horizontal, 16)
                                .accessibilityElement(children: .combine)
                                
                                if index < viewModel.items.count - 1 {
                                    Divider()
                                        .background(Color.blindAIDivider.opacity(0.6))
                                        .padding(.leading, 60)
                                }
                            }
                        }
                        .background(Color.white)
                        .clipShape(RoundedRectangle(cornerRadius: 22, style: .continuous))
                        .shadow(color: Color.black.opacity(0.05), radius: 10, x: 0, y: 3)
                        
                        // Bottom Repeat Pill Button
                        Button(action: {
                            viewModel.repeatSpokenSummary()
                        }) {
                            HStack(spacing: 8) {
                                Image(systemName: "speaker.wave.2.fill")
                                    .font(.system(size: 16, weight: .medium))
                                Text("Repeat")
                                    .font(.system(size: 16, weight: .semibold))
                            }
                            .foregroundColor(Color.blindAITextPrimary)
                            .padding(.vertical, 13)
                            .padding(.horizontal, 28)
                            .background(Color.white)
                            .clipShape(Capsule())
                            .shadow(color: Color.black.opacity(0.08), radius: 6, x: 0, y: 2)
                            .overlay(
                                Capsule()
                                    .stroke(Color.slate200.opacity(0.7), lineWidth: 1)
                            )
                        }
                        .padding(.top, 4)
                        .padding(.bottom, 20)
                        .accessibilityLabel("Repeat spoken description")
                    }
                    .padding(.horizontal, BlindAISpacing.screenHorizontal)
                    .padding(.bottom, 16)
                }
            }
        }
        .onAppear {
            viewModel.handleOnAppear()
        }
    }
}

#Preview {
    DescribeAroundView(viewModel: DescribeAroundViewModel())
}
