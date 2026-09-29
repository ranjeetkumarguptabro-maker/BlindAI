import SwiftUI

public struct BlindAIHeader: View {
    public var onSettingsTapped: (() -> Void)? = nil
    
    public init(onSettingsTapped: (() -> Void)? = nil) {
        self.onSettingsTapped = onSettingsTapped
    }
    
    public var body: some View {
        HStack(alignment: .center) {
            Text("Blind AI")
                .font(.blindAIHeaderTitle)
                .foregroundColor(.blindAITextPrimary)
                .accessibilityAddTraits(.isHeader)
            
            Spacer()
            
            Button {
                let generator = UIImpactFeedbackGenerator(style: .light)
                generator.impactOccurred()
                onSettingsTapped?()
            } label: {
                ZStack {
                    Circle()
                        .fill(Color(red: 236/255, green: 236/255, blue: 238/255))
                        .frame(width: 38, height: 38)
                    
                    Image(systemName: "gearshape.fill")
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundColor(.blindAITextPrimary)
                }
            }
            .buttonStyle(.plain)
            .accessibilityLabel("Settings")
            .accessibilityHint("Double tap to open settings")
        }
        .padding(.horizontal, BlindAISpacing.screenPadding)
        .padding(.top, 10)
        .padding(.bottom, 6)
    }
}

#Preview {
    BlindAIHeader()
}
