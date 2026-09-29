import SwiftUI

public struct CrosswalkSafetyView: View {
    @ObservedObject public var viewModel: CrosswalkSafetyViewModel
    @State private var wavePhase: CGFloat = 0
    
    // Waveform bar heights mimicking audio amplitude
    private let baseBarHeights: [CGFloat] = [10, 16, 26, 42, 54, 42, 26, 16, 10]
    
    public init(viewModel: CrosswalkSafetyViewModel) {
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
                
                // Top Crosswalk Notice Banner
                HStack(alignment: .center, spacing: 16) {
                    Image(systemName: "figure.walk")
                        .font(.system(size: 38, weight: .bold))
                        .foregroundColor(.black)
                        .frame(width: 44, alignment: .center)
                    
                    VStack(alignment: .leading, spacing: 3) {
                        Text(viewModel.crossing.title)
                            .font(.system(size: 22, weight: .bold))
                            .foregroundColor(.black)
                        
                        Text(viewModel.crossing.subtitle)
                            .font(.system(size: 15, weight: .regular))
                            .foregroundColor(Color(red: 0.15, green: 0.15, blue: 0.15))
                    }
                    
                    Spacer()
                }
                .padding(.horizontal, 20)
                .padding(.vertical, 18)
                .background(Color(red: 0.99, green: 0.88, blue: 0.44)) // Warm amber/yellow
                .clipShape(RoundedRectangle(cornerRadius: 22, style: .continuous))
                .padding(.horizontal, BlindAISpacing.screenHorizontal)
                .accessibilityElement(children: .combine)
                .accessibilityLabel("Approaching crosswalk. Listen for traffic.")
                
                // Camera View with Zebra Crossing & Green Signal
                ZStack(alignment: .bottom) {
                    // Camera feed image
                    Group {
                        if let uiImage = UIImage(named: "scene_crosswalk_signal") {
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
                    
                    // Floating Quiet Mode Audio Card inside camera view
                    VStack(spacing: 16) {
                        // Amber Audio Waveform Visualizer
                        HStack(spacing: 5) {
                            ForEach(0..<baseBarHeights.count, id: \.self) { i in
                                RoundedRectangle(cornerRadius: 3)
                                    .fill(
                                        LinearGradient(
                                            colors: [
                                                Color(red: 1.0, green: 0.76, blue: 0.05),
                                                Color(red: 0.98, green: 0.58, blue: 0.0)
                                            ],
                                            startPoint: .top,
                                            endPoint: .bottom
                                        )
                                    )
                                    .frame(
                                        width: 5,
                                        height: baseBarHeights[i] * (0.8 + 0.35 * sin(wavePhase + Double(i) * 0.7))
                                    )
                            }
                        }
                        .frame(height: 58)
                        .accessibilityLabel("Quiet Mode Active. Ambient listening waveform.")
                        
                        Text(viewModel.crossing.quietMessage)
                            .font(.system(size: 16, weight: .regular))
                            .foregroundColor(Color.blindAITextPrimary)
                            .multilineTextAlignment(.center)
                    }
                    .padding(.horizontal, 20)
                    .padding(.vertical, 24)
                    .frame(maxWidth: .infinity)
                    .background(Color.white)
                    .clipShape(RoundedRectangle(cornerRadius: 24, style: .continuous))
                    .shadow(color: Color.black.opacity(0.12), radius: 12, x: 0, y: 4)
                    .padding(.horizontal, 14)
                    .padding(.bottom, 20)
                    .onTapGesture {
                        viewModel.confirmCrossed()
                    }
                }
                .padding(.horizontal, BlindAISpacing.screenHorizontal)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .padding(.bottom, 12)
            }
        }
        .onAppear {
            viewModel.handleOnAppear()
            withAnimation(.easeInOut(duration: 1.2).repeatForever(autoreverses: true)) {
                wavePhase = .pi * 2
            }
        }
    }
}

#Preview {
    CrosswalkSafetyView(viewModel: CrosswalkSafetyViewModel())
}
