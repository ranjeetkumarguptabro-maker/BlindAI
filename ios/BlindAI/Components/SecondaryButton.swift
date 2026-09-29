import SwiftUI

public struct SecondaryButton: View {
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
            let haptic = UIImpactFeedbackGenerator(style: .light)
            haptic.impactOccurred()
            action()
        } label: {
            HStack(spacing: 8) {
                if let iconName {
                    Image(systemName: iconName)
                        .font(.system(size: 16, weight: .bold))
                }
                
                Text(title)
                    .font(.blindAIButton)
            }
            .foregroundColor(.blindAITextPrimary)
            .frame(maxWidth: .infinity)
            .frame(height: BlindAISpacing.secondaryButtonHeight)
            .background(Color.blindAISecondaryButton)
            .clipShape(RoundedRectangle(cornerRadius: BlindAISpacing.buttonCornerRadius, style: .continuous))
        }
        .buttonStyle(SecondaryButtonStyle())
        .accessibilityLabel(title)
        .accessibilityAddTraits(.isButton)
    }
}

private struct SecondaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .opacity(configuration.isPressed ? 0.85 : 1.0)
            .animation(.easeInOut(duration: 0.15), value: configuration.isPressed)
    }
}

#Preview {
    SecondaryButton(title: "Show more details", iconName: "mappin", action: {})
        .padding()
}
