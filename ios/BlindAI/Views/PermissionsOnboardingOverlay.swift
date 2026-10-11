import SwiftUI
import AVFoundation

public struct PermissionsOnboardingOverlay: View {
    public var onAuthorizeAll: () -> Void
    public var onFallback: () -> Void
    
    @State private var cameraAuthorized: Bool = false
    @State private var micAuthorized: Bool = false
    @State private var locationAuthorized: Bool = false
    @State private var motionAuthorized: Bool = false
    
    public init(onAuthorizeAll: @escaping () -> Void, onFallback: @escaping () -> Void) {
        self.onAuthorizeAll = onAuthorizeAll
        self.onFallback = onFallback
    }
    
    public var body: some View {
        ZStack {
            Color.black.opacity(0.92)
                .ignoresSafeArea()
            
            VStack(spacing: 20) {
                // Header badge
                HStack(spacing: 12) {
                    ZStack {
                        RoundedRectangle(cornerRadius: 16)
                            .fill(Color.orange)
                            .frame(width: 48, height: 48)
                        Text("🛡️")
                            .font(.system(size: 24))
                    }
                    VStack(alignment: .leading, spacing: 2) {
                        Text("INITIAL SAFETY SETUP")
                            .font(.system(size: 10, weight: .bold))
                            .foregroundColor(.orange)
                        Text("Authorize Sensors")
                            .font(.system(size: 22, weight: .black))
                            .foregroundColor(.white)
                    }
                    Spacer()
                }
                .padding(.horizontal, 4)
                
                Text("Blind AI uses your iPhone's camera, microphone, GPS, and motion sensors to guide you hands-free and protect you from obstacles.")
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(.white.opacity(0.85))
                    .multilineTextAlignment(.leading)
                    .accessibilityLabel("Sensor authorization required. Blind AI uses camera, microphone, GPS, and motion sensors for obstacle protection.")
                
                // Checklist
                VStack(spacing: 12) {
                    sensorRow(icon: "camera.fill", title: "Camera (Obstacles & YOLO)", isGranted: cameraAuthorized)
                    sensorRow(icon: "mic.fill", title: "Microphone (Voice Control)", isGranted: micAuthorized)
                    sensorRow(icon: "location.fill", title: "Location (GPS Navigation)", isGranted: locationAuthorized)
                    sensorRow(icon: "figure.walk", title: "Motion & Pedestrian Pedometer", isGranted: motionAuthorized)
                }
                .padding(16)
                .background(Color.white.opacity(0.08))
                .cornerRadius(20)
                
                Spacer()
                
                // Actions
                VStack(spacing: 12) {
                    Button {
                        cameraAuthorized = true
                        micAuthorized = true
                        locationAuthorized = true
                        motionAuthorized = true
                        onAuthorizeAll()
                    } label: {
                        Text("Authorize All Assistive Sensors")
                            .font(.system(size: 16, weight: .heavy))
                            .foregroundColor(.black)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 16)
                            .background(Color.orange)
                            .cornerRadius(18)
                    }
                    .accessibilityHint("Double tap to grant access to camera, microphone, location, and motion sensors.")
                    
                    Button {
                        onFallback()
                    } label: {
                        Text("Continue with Safe Fallback Mode")
                            .font(.system(size: 13, weight: .semibold))
                            .foregroundColor(.white.opacity(0.6))
                            .padding(.vertical, 8)
                    }
                }
            }
            .padding(24)
        }
    }
    
    @ViewBuilder
    private func sensorRow(icon: String, title: String, isGranted: Bool) -> some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 16, weight: .bold))
                .foregroundColor(isGranted ? .green : .white)
                .frame(width: 24)
            Text(title)
                .font(.system(size: 14, weight: .semibold))
                .foregroundColor(.white)
            Spacer()
            Text(isGranted ? "Active" : "Required")
                .font(.system(size: 11, weight: .bold))
                .foregroundColor(isGranted ? .green : .orange)
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(isGranted ? Color.green.opacity(0.15) : Color.orange.opacity(0.15))
                .cornerRadius(8)
        }
    }
}
