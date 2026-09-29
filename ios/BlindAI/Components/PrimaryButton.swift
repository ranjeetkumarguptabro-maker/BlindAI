import SwiftUI

public struct PrimaryButton: View {
    public let title: String
    public let iconName: String?
    public let action: () -> Void
    
    public init(
        title: String,
        iconName: String? = nil,
        action: @escaping () -> Void
    ) {
        self.title = title
        self.iconName = iconName
        self.action = action
    }
    
    public var body: some View {
        Button {
            let haptic = UIImpactFeedbackGenerator(style: .medium)
            haptic.impactOccurred()
            action()
        } label: {
            HStack(spacing: 10) {
                if let iconName {
                    Image(systemName: iconName)
                        .font(.system(size: 16, weight: .bold))
                }
                
                Text(title)
                    .font(.blindAIButton)
            }
            .foregroundColor(.white)
            .frame(maxWidth: .infinity)
            .frame(height: BlindAISpacing.primaryButtonHeight)
            .background(Color.blindAIPrimaryButton)
            .clipShape(RoundedRectangle(cornerRadius: BlindAISpacing.buttonCornerRadius, style: .continuous))
            .shadow(color: Color.black.opacity(0.12), radius: 8, x: 0, y: 3)
        }
        .buttonStyle(PrimaryButtonStyle())
        .accessibilityLabel(title)
        .accessibilityAddTraits(.isButton)
    }
}

private struct PrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .opacity(configuration.isPressed ? 0.9 : 1.0)
            .animation(.easeInOut(duration: 0.15), value: configuration.isPressed)
    }
}

#Preview {
    PrimaryButton(title: "Stop route", iconName: "square.fill", action: {})
        .padding()
}
