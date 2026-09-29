import SwiftUI

public struct ListeningView: View {
    @ObservedObject public var viewModel: ListeningViewModel
    
    public init(viewModel: ListeningViewModel) {
        self.viewModel = viewModel
    }
    
    public var body: some View {
        ZStack(alignment: .bottomTrailing) {
            Color.blindAIBackground
                .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Header
                BlindAIHeader()
                
                VStack(spacing: 16) {
                    Spacer(minLength: 10)
                    
                    // Concentric glowing orb with animated ripple rings reactive to microphone
                    GlowingOrb(mode: .listening, audioPower: viewModel.audioLevel)
                    
                    // "Listening..." text with live transcription feedback
                    VStack(spacing: 6) {
                        Text(viewModel.statusMessage)
                            .font(.system(size: 32, weight: .bold))
                            .foregroundColor(.blindAITextPrimary)
                            .accessibilityAddTraits(.isHeader)
                        
                        if !viewModel.transcript.isEmpty {
                            Text("“\(viewModel.transcript)”")
                                .font(.system(size: 17, weight: .medium))
                                .foregroundColor(.orange)
                                .multilineTextAlignment(.center)
                                .padding(.horizontal, 20)
                                .transition(.opacity)
                        }
                    }
                    
                    // Pill label: "You can say:"
                    Text("You can say:")
                        .font(.blindAIPromptLabel)
                        .foregroundColor(.blindAITextSecondary)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 7)
                        .background(Color.blindAIPillBackground)
                        .clipShape(Capsule())
                        .padding(.top, 4)
                    
                    // Suggested commands list (interactive)
                    VStack(spacing: 12) {
                        ForEach(viewModel.suggestedCommands, id: \.self) { command in
                            Button {
                                viewModel.handleCommandSelected(command)
                            } label: {
                                Text(command)
                                    .font(.blindAICommandSample)
                                    .foregroundColor(.blindAITextPrimary)
                            }
                            .buttonStyle(.plain)
                            .accessibilityLabel("Command suggestion: \(command)")
                            .accessibilityHint("Double tap to run this command")
                        }
                    }
                    .padding(.top, 2)
                    
                    Spacer(minLength: 20)
                    
                    // Large black circular stop button
                    VoiceButton(mode: .stop) {
                        viewModel.handleStopTapped()
                    }
                    .padding(.bottom, 36)
                }
                .padding(.horizontal, BlindAISpacing.screenPadding)
            }
            
            // Subtle speaker repeat button
            SpeakerButton(textToRepeat: "Listening. You can say: Take me to CIF, What's in front of me?, or Where am I? Tap the stop button to cancel.")
                .padding(.trailing, 20)
                .padding(.bottom, 24)
        }
        .onAppear {
            viewModel.onAppear()
        }
        .onDisappear {
            viewModel.onDisappear()
        }
    }
}

#Preview {
    ListeningView(viewModel: ListeningViewModel())
}
