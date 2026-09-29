import SwiftUI
import AVFoundation

public struct SpeakerButton: View {
    public let textToRepeat: String
    public var onRepeat: (() -> Void)?
    
    @State private var isSpeaking: Bool = false
    
    public init(textToRepeat: String, onRepeat: (() -> Void)? = nil) {
        self.textToRepeat = textToRepeat
        self.onRepeat = onRepeat
    }
    
    public var body: some View {
        Button {
            let haptic = UIImpactFeedbackGenerator(style: .medium)
            haptic.impactOccurred()
            
            speak(text: textToRepeat)
            onRepeat?()
        } label: {
            ZStack {
                Circle()
                    .fill(Color.white.opacity(0.92))
                    .frame(width: 44, height: 44)
                    .shadow(color: Color.black.opacity(0.08), radius: 6, x: 0, y: 2)
                    .overlay(
                        Circle()
                            .stroke(Color.black.opacity(0.06), lineWidth: 1)
                    )
                
                Image(systemName: isSpeaking ? "speaker.wave.3.fill" : "speaker.wave.2.fill")
                    .font(.system(size: 18, weight: .semibold))
                    .foregroundColor(.blindAITextPrimary)
            }
        }
        .buttonStyle(.plain)
        .accessibilityLabel("Repeat spoken instructions")
        .accessibilityHint("Double tap to speak the current instruction aloud")
    }
    
    private func speak(text: String) {
        guard !text.isEmpty else { return }
        isSpeaking = true
        let utterance = AVSpeechUtterance(string: text)
        utterance.rate = AVSpeechUtteranceDefaultVoiceRate
        utterance.voice = AVSpeechSynthesisVoice(language: "en-US")
        
        let synthesizer = AVSpeechSynthesizer()
        synthesizer.speak(utterance)
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.2) {
            isSpeaking = false
        }
    }
}

#Preview {
    SpeakerButton(textToRepeat: "Take a right onto the sidewalk.")
        .padding()
        .background(Color.blindAIBackground)
}
