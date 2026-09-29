import SwiftUI

public struct ActionCard: View {
    public let item: ActionCardType
    public let action: () -> Void
    
    public init(item: ActionCardType, action: @escaping () -> Void) {
        self.item = item
        self.action = action
    }
    
    public var body: some View {
        Button {
            let generator = UIImpactFeedbackGenerator(style: .medium)
            generator.impactOccurred()
            action()
        } label: {
            HStack(spacing: 16) {
                // Leading Icon Container
                ZStack {
                    RoundedRectangle(cornerRadius: 14, style: .continuous)
                        .fill(item.iconBackground)
                        .frame(width: 48, height: 48)
                    
                    Image(systemName: item.iconName)
                        .font(.system(size: 22, weight: .semibold))
                        .foregroundColor(item.iconColor)
                }
                
                // Text Information Stack
                VStack(alignment: .leading, spacing: 3) {
                    Text(item.title)
                        .font(.blindAIActionTitle)
                        .foregroundColor(.blindAITextPrimary)
                        .lineLimit(1)
                    
                    Text(item.subtitle)
                        .font(.blindAIActionSubtitle)
                        .foregroundColor(.blindAITextSecondary)
                        .lineLimit(1)
                }
                
                Spacer()
                
                // Trailing Chevron
                Image(systemName: "chevron.right")
                    .font(.system(size: 15, weight: .semibold))
                    .foregroundColor(Color(red: 198/255, green: 198/255, blue: 200/255))
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 14)
            .background(Color.white)
            .clipShape(RoundedRectangle(cornerRadius: BlindAISpacing.cardCornerRadius, style: .continuous))
            .overlay(
                RoundedRectangle(cornerRadius: BlindAISpacing.cardCornerRadius, style: .continuous)
                    .stroke(Color.black.opacity(0.04), lineWidth: 1)
            )
            .shadow(color: Color.black.opacity(0.03), radius: 8, x: 0, y: 2)
        }
        .buttonStyle(ActionCardButtonStyle())
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(item.title). \(item.subtitle)")
        .accessibilityHint(item.accessibilityHint)
        .accessibilityAddTraits(.isButton)
    }
}

private struct ActionCardButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .opacity(configuration.isPressed ? 0.88 : 1.0)
            .animation(.easeInOut(duration: 0.15), value: configuration.isPressed)
    }
}

#Preview {
    VStack(spacing: 12) {
        ActionCard(item: .startNavigation, action: {})
        ActionCard(item: .describeAround, action: {})
        ActionCard(item: .whereAmI, action: {})
    }
    .padding()
    .background(Color.blindAIBackground)
}
