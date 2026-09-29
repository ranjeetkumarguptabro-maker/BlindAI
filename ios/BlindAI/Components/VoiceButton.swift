import SwiftUI

public enum VoiceButtonMode {
    case speak
    case stop
    
    var iconName: String {
        switch self {
        case .speak: return "mic.fill"
        case .stop: return "square.fill"
        }
    }
    
    var labelText: String {
        switch self {
        case .speak: return "Tap to speak"
        case .stop: return "Tap to stop"
        }
    }
    
    var accessibilityLabel: String {
        switch self {
        case .speak: return "Microphone. Tap to start voice listening"
        case .stop: return "Stop button. Tap to stop voice listening and return to home"
        }
    }
}

public struct VoiceButton: View {
    public let mode: VoiceButtonMode
    public let action: () -> Void
    
    public init(mode: VoiceButtonMode = .speak, action: @escaping () -> Void) {
        self.mode = mode
        self.action = action
    }
    
    public var body: some View {
        Button {
            let haptic = UIImpactFeedbackGenerator(style: mode == .speak ? .heavy : .medium)
            haptic.impactOccurred()
            action()
        } label: {
            VStack(spacing: 10) {
                ZStack {
                    Circle()
                        .fill(Color.black)
                        .frame(width: BlindAISpacing.voiceButtonSize, height: BlindAISpacing.voiceButtonSize)
                        .shadow(color: Color.black.opacity(0.12), radius: 10, x: 0, y: 4)
                    
                    Image(systemName: mode.iconName)
                        .font(.system(size: mode == .speak ? 28 : 22, weight: .semibold))
                        .foregroundColor(.white)
                }
                
                Text(mode.labelText)
                    .font(.blindAIFootnote)
                    .foregroundColor(.blindAITextPrimary)
            }
        }
        .buttonStyle(VoiceButtonStyle())
        .accessibilityElement(children: .combine)
        .accessibilityLabel(mode.accessibilityLabel)
        .accessibilityAddTraits(.isButton)
    }
}

private struct VoiceButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.94 : 1.0)
            .opacity(configuration.isPressed ? 0.85 : 1.0)
            .animation(.spring(response: 0.25, dampingFraction: 0.7), value: configuration.isPressed)
    }
}

#Preview {
    HStack(spacing: 40) {
        VoiceButton(mode: .speak, action: {})
        VoiceButton(mode: .stop, action: {})
    }
    .padding()
    .background(Color.blindAIBackground)
}
