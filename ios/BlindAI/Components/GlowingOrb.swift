import SwiftUI

public enum GlowingOrbMode {
    case home
    case listening
    case compact
}

public struct GlowingOrb: View {
    public let mode: GlowingOrbMode
    public var audioPower: Float = 0.0
    
    @State private var pulseAnimation = false
    
    public init(mode: GlowingOrbMode = .home, audioPower: Float = 0.0) {
        self.mode = mode
        self.audioPower = audioPower
    }
    
    private var orbSize: CGFloat {
        switch mode {
        case .home:
            return 132
        case .listening:
            return 132
        case .compact:
            return 54
        }
    }
    
    private var dynamicScale: CGFloat {
        if mode == .listening && audioPower > 0.05 {
            return 1.0 + CGFloat(audioPower) * 0.18
        }
        return pulseAnimation ? 1.03 : 0.98
    }
    
    public var body: some View {
        ZStack {
            // Concentric ripple rings when in listening mode
            if mode == .listening {
                // Outer ring 3
                Circle()
                    .stroke(Color.orange.opacity(0.12 + Double(audioPower) * 0.15), lineWidth: 1.5)
                    .frame(width: orbSize * 2.1, height: orbSize * 2.1)
                    .scaleEffect(dynamicScale * 1.05)
                
                // Outer ring 2
                Circle()
                    .stroke(Color.orange.opacity(0.18 + Double(audioPower) * 0.2), lineWidth: 1.8)
                    .frame(width: orbSize * 1.7, height: orbSize * 1.7)
                    .scaleEffect(dynamicScale * 1.02)
                
                // Outer ring 1
                Circle()
                    .stroke(Color.orange.opacity(0.25 + Double(audioPower) * 0.25), lineWidth: 2)
                    .frame(width: orbSize * 1.35, height: orbSize * 1.35)
                    .scaleEffect(dynamicScale)
            }
            
            // Soft ambient glow background
            Circle()
                .fill(
                    RadialGradient(
                        colors: [
                            Color(red: 255/255, green: 130/255, blue: 0/255).opacity(mode == .compact ? 0.4 : (0.45 + Double(audioPower) * 0.3)),
                            Color(red: 255/255, green: 160/255, blue: 30/255).opacity(mode == .compact ? 0.2 : 0.25),
                            Color.clear
                        ],
                        center: .center,
                        startRadius: orbSize * 0.2,
                        endRadius: orbSize * 0.85
                    )
                )
                .frame(width: orbSize * 1.45, height: orbSize * 1.45)
                .blur(radius: mode == .compact ? 12 : 24)
            
            // 3D Spherical Orb Body
            ZStack {
                // Base deep radial gradient
                Circle()
                    .fill(
                        RadialGradient(
                            gradient: Gradient(stops: [
                                .init(color: Color(red: 255/255, green: 220/255, blue: 130/255), location: 0.0),
                                .init(color: Color(red: 255/255, green: 155/255, blue: 40/255), location: 0.35),
                                .init(color: Color(red: 250/255, green: 105/255, blue: 10/255), location: 0.70),
                                .init(color: Color(red: 220/255, green: 70/255, blue: 5/255), location: 1.0)
                            ]),
                            center: UnitPoint(x: 0.40, y: 0.36),
                            startRadius: orbSize * 0.05,
                            endRadius: orbSize * 0.65
                        )
                    )
                
                // Specular light highlight for 3D depth
                Circle()
                    .fill(
                        RadialGradient(
                            colors: [
                                Color.white.opacity(0.55),
                                Color.white.opacity(0.15),
                                Color.clear
                            ],
                            center: UnitPoint(x: 0.38, y: 0.34),
                            startRadius: 0,
                            endRadius: orbSize * 0.32
                        )
                    )
                
                // Edge darkening for spherical vignette
                Circle()
                    .stroke(
                        LinearGradient(
                            colors: [
                                Color(red: 255/255, green: 200/255, blue: 120/255).opacity(0.5),
                                Color(red: 180/255, green: 50/255, blue: 0/255).opacity(0.4)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        ),
                        lineWidth: 1
                    )
            }
            .frame(width: orbSize, height: orbSize)
            .shadow(color: Color(red: 255/255, green: 110/255, blue: 0/255).opacity(0.35), radius: mode == .compact ? 8 : 18, x: 0, y: mode == .compact ? 4 : 8)
        }
        .frame(height: mode == .compact ? orbSize + 12 : orbSize + (mode == .listening ? 60 : 36))
        .onAppear {
            if mode == .listening {
                withAnimation(
                    .easeInOut(duration: 1.6)
                    .repeatForever(autoreverses: true)
                ) {
                    pulseAnimation = true
                }
            }
        }
        .accessibilityElement(children: .ignore)
        .accessibilityLabel(mode == .listening ? "Listening indicator pulsing orb" : "Blind AI assistant status orb")
    }
}
