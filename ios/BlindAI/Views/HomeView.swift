import SwiftUI

public struct HomeView: View {
    @ObservedObject public var viewModel: HomeViewModel
    
    public init(viewModel: HomeViewModel) {
        self.viewModel = viewModel
    }
    
    public var body: some View {
        ZStack(alignment: .bottomTrailing) {
            Color.blindAIBackground
                .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Header: "Blind AI" + settings cog
                BlindAIHeader(onSettingsTapped: {
                    viewModel.handleSettingsTapped()
                })
                
                ScrollView(.vertical, showsIndicators: false) {
                    VStack(spacing: 16) {
                        // Glowing Orb
                        GlowingOrb(mode: .home)
                            .padding(.top, 6)
                        
                        // Hero prompt heading
                        Text("How can I help you\ntoday?")
                            .font(.blindAIHeroHeading)
                            .foregroundColor(.blindAITextPrimary)
                            .multilineTextAlignment(.center)
                            .lineSpacing(4)
                            .padding(.horizontal, 24)
                            .accessibilityAddTraits(.isHeader)
                        
                        // Query Feedback Banner (when user triggers Where Am I or Describe)
                        if let toast = viewModel.statusToast {
                            HStack(alignment: .top, spacing: 10) {
                                Image(systemName: "speaker.wave.2.fill")
                                    .font(.system(size: 14, weight: .bold))
                                    .foregroundColor(.orange)
                                    .padding(.top, 2)
                                
                                Text(toast)
                                    .font(.system(size: 14, weight: .medium))
                                    .foregroundColor(.black)
                                
                                Spacer()
                                
                                Button {
                                    withAnimation {
                                        viewModel.dismissToast()
                                    }
                                } label: {
                                    Image(systemName: "xmark.circle.fill")
                                        .font(.system(size: 16))
                                        .foregroundColor(.gray)
                                }
                            }
                            .padding(14)
                            .background(Color.white)
                            .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
                            .shadow(color: Color.black.opacity(0.06), radius: 8, x: 0, y: 2)
                            .padding(.horizontal, BlindAISpacing.screenPadding)
                            .transition(.move(edge: .top).combined(with: .opacity))
                        }
                        
                        // Three Large Rounded Action Cards
                        VStack(spacing: 11) {
                            ForEach(viewModel.actionItems) { item in
                                ActionCard(item: item) {
                                    viewModel.handleCardSelection(item)
                                }
                            }
                        }
                        .padding(.horizontal, BlindAISpacing.screenPadding)
                        .padding(.top, 4)
                        
                        // Large circular microphone button
                        VoiceButton(mode: .speak) {
                            viewModel.handleMicrophoneTapped()
                        }
                        .padding(.top, 14)
                        .padding(.bottom, 24)
                    }
                }
            }
            
            // Subtle speaker repeat button (Bottom right corner as defined in system architecture)
            SpeakerButton(textToRepeat: "How can I help you today? You can start navigation, describe what's around you, check where you are, or tap the microphone to speak.")
                .padding(.trailing, 20)
                .padding(.bottom, 24)
        }
        .alert("Settings", isPresented: $viewModel.isShowingSettings) {
            Button("Done", role: .cancel) {}
        } message: {
            Text("Blind AI Settings:\n• Voice Mode: Standard\n• Speech Rate: 1.0x\n• Haptic Feedback: Enabled\n• Obstacle Sensitivity: Medium")
        }
    }
}

#Preview {
    HomeView(viewModel: HomeViewModel())
}
