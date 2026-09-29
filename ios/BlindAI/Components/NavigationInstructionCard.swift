import SwiftUI

public struct NavigationInstructionCard: View {
    public let instruction: NavigationInstruction
    
    public init(instruction: NavigationInstruction = .mock) {
        self.instruction = instruction
    }
    
    public var body: some View {
        VStack(alignment: .leading, spacing: 18) {
            // Header tag: walking icon + "Navigation"
            HStack(spacing: 8) {
                Image(systemName: "figure.walk")
                    .font(.system(size: 15, weight: .bold))
                    .foregroundColor(.blindAIOrange)
                
                Text(instruction.title)
                    .font(.blindAINavTag)
                    .foregroundColor(.blindAITextSecondary)
            }
            
            // Primary direction instruction text
            Text(instruction.mainInstruction)
                .font(.blindAINavInstruction)
                .foregroundColor(.blindAITextPrimary)
                .fixedSize(horizontal: false, vertical: true)
                .lineSpacing(2)
            
            // Distance display (Huge number + unit)
            HStack(alignment: .firstTextBaseline, spacing: 3) {
                Text(instruction.distanceValue)
                    .font(.blindAIDistanceNumber)
                    .foregroundColor(.blindAITextPrimary)
                
                Text(instruction.distanceUnit)
                    .font(.blindAIDistanceUnit)
                    .foregroundColor(.blindAITextPrimary)
            }
            .padding(.top, -6)
            
            // Maneuver pill banner (Yellow card)
            HStack(spacing: 12) {
                Image(systemName: instruction.maneuverIcon)
                    .font(.system(size: 18, weight: .bold))
                    .foregroundColor(.black)
                
                Text(instruction.maneuverText)
                    .font(.blindAIManeuver)
                    .foregroundColor(.black)
                
                Spacer()
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 14)
            .background(Color.blindAIManeuverYellow)
            .clipShape(RoundedRectangle(cornerRadius: BlindAISpacing.pillCornerRadius, style: .continuous))
        }
        .padding(20)
        .background(Color.white)
        .clipShape(RoundedRectangle(cornerRadius: 24, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: 24, style: .continuous)
                .stroke(Color.black.opacity(0.04), lineWidth: 1)
        )
        .shadow(color: Color.black.opacity(0.04), radius: 12, x: 0, y: 4)
        .accessibilityElement(children: .combine)
        .accessibilityLabel(instruction.spokenAnnouncement)
    }
}

#Preview {
    NavigationInstructionCard()
        .padding()
        .background(Color.blindAIBackground)
}
