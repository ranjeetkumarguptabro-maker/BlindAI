import SwiftUI
import AVFoundation

public struct ActiveNavigationView: View {
    @ObservedObject public var viewModel: ActiveNavigationViewModel
    @StateObject private var perceptionService = RealtimeVisionPerceptionService.shared
    @StateObject private var cameraService = CameraCaptureService.shared
    @State private var isCameraOverlayEnabled: Bool = true
    
    public init(viewModel: ActiveNavigationViewModel) {
        self.viewModel = viewModel
    }
    
    public var body: some View {
        ZStack(alignment: .bottomTrailing) {
            // Live Camera Background or High-Contrast Accessible Surface
            if isCameraOverlayEnabled && cameraService.hasCameraPermission {
                CameraPreviewView(captureSession: cameraService.captureSession)
                    .ignoresSafeArea()
                    .overlay(
                        Color.black.opacity(0.35)
                            .ignoresSafeArea()
                    )
            } else {
                Color.blindAIBackground
                    .ignoresSafeArea()
            }
            
            // Real-Time YOLO Bounding Boxes Overlay
            GeometryReader { geo in
                ForEach(perceptionService.detectedObjects) { obj in
                    ZStack(alignment: .topLeading) {
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(colorForDanger(obj.dangerLevel), lineWidth: 2.5)
                            .background(colorForDanger(obj.dangerLevel).opacity(0.12))
                        
                        Text("\(obj.label) \(String(format: "%.1f", obj.distanceMeters))m")
                            .font(.system(size: 11, weight: .bold))
                            .foregroundColor(.white)
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(colorForDanger(obj.dangerLevel))
                            .clipShape(RoundedRectangle(cornerRadius: 4))
                            .offset(y: -20)
                    }
                    .frame(
                        width: max(40, obj.boundingBox.width * geo.size.width),
                        height: max(40, obj.boundingBox.height * geo.size.height)
                    )
                    .position(
                        x: obj.boundingBox.midX * geo.size.width,
                        y: obj.boundingBox.midY * geo.size.height
                    )
                }
            }
            .allowsHitTesting(false)
            
            VStack(spacing: 0) {
                // Header with Camera & YOLO status pill
                HStack {
                    Button(action: {
                        viewModel.handleStopRoute()
                    }) {
                        Image(systemName: "chevron.left")
                            .font(.system(size: 16, weight: .bold))
                            .foregroundColor(.white)
                            .padding(10)
                            .background(Color.black.opacity(0.6))
                            .clipShape(Circle())
                    }
                    .accessibilityLabel("End navigation and return")
                    
                    Spacer()
                    
                    // Live YOLO Status Pill
                    HStack(spacing: 6) {
                        Circle()
                            .fill(perceptionService.isPerceptionActive ? Color.green : Color.orange)
                            .frame(width: 8, height: 8)
                        Text(cameraService.isRunning ? "Back Camera • YOLO Active" : "Perception Ready")
                            .font(.system(size: 12, weight: .bold))
                            .foregroundColor(.white)
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(Color.black.opacity(0.65))
                    .clipShape(Capsule())
                    
                    Spacer()
                    
                    // Toggle Camera View Button
                    Button(action: {
                        isCameraOverlayEnabled.toggle()
                    }) {
                        Image(systemName: isCameraOverlayEnabled ? "camera.fill" : "camera")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(.white)
                            .padding(10)
                            .background(Color.black.opacity(0.6))
                            .clipShape(Circle())
                    }
                    .accessibilityLabel("Toggle camera preview")
                }
                .padding(.horizontal, BlindAISpacing.screenPadding)
                .padding(.top, 10)
                .padding(.bottom, 6)
                
                ScrollView(.vertical, showsIndicators: false) {
                    VStack(spacing: 16) {
                        // Compact Glowing Orb centered above instruction card
                        GlowingOrb(mode: .compact)
                            .padding(.top, 4)
                            .padding(.bottom, 2)
                        
                        // Main Navigation Card (Live instruction & distance)
                        NavigationInstructionCard(instruction: viewModel.instruction)
                            .padding(.horizontal, BlindAISpacing.screenPadding)
                        
                        // Hazard Warning Pill if obstacle detected directly ahead
                        if let danger = perceptionService.highestDangerObject, danger.distanceMeters <= 2.5 {
                            HStack(spacing: 8) {
                                Image(systemName: "exclamationmark.triangle.fill")
                                    .foregroundColor(.red)
                                Text("Caution: \(danger.label) \(String(format: "%.1f", danger.distanceMeters))m ahead in walking path")
                                    .font(.system(size: 12, weight: .bold))
                                    .foregroundColor(.white)
                            }
                            .padding(.horizontal, 14)
                            .padding(.vertical, 8)
                            .background(Color.red.opacity(0.85))
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                            .padding(.horizontal, BlindAISpacing.screenPadding)
                        }
                        
                        // Action Buttons Stack
                        VStack(spacing: 12) {
                            // Instant scene scan ("What do you see?")
                            SecondaryButton(
                                title: "Describe what's around me",
                                iconName: "eye.fill"
                            ) {
                                Task {
                                    _ = await perceptionService.performInstantSceneScan()
                                }
                            }
                            
                            // Secondary light button: "Show more details"
                            SecondaryButton(
                                title: "Show more details",
                                iconName: "mappin"
                            ) {
                                viewModel.handleShowDetails()
                            }
                            
                            // Primary black button: "Stop route"
                            PrimaryButton(
                                title: "Stop route",
                                iconName: "square.fill"
                            ) {
                                viewModel.handleStopRoute()
                            }
                            
                            // Safety test triggers
                            HStack(spacing: 10) {
                                Button(action: {
                                    viewModel.triggerObstacleAlert()
                                }) {
                                    HStack(spacing: 6) {
                                        Image(systemName: "exclamationmark.triangle.fill")
                                            .foregroundColor(.red)
                                        Text("Obstacle Alert")
                                            .font(.system(size: 13, weight: .semibold))
                                            .foregroundColor(.black)
                                    }
                                    .padding(.vertical, 9)
                                    .padding(.horizontal, 12)
                                    .background(Color.white)
                                    .clipShape(RoundedRectangle(cornerRadius: 12))
                                    .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 1)
                                }
                                
                                Button(action: {
                                    viewModel.triggerCrosswalkSafety()
                                }) {
                                    HStack(spacing: 6) {
                                        Image(systemName: "figure.walk")
                                            .foregroundColor(.black)
                                        Text("Crosswalk")
                                            .font(.system(size: 13, weight: .semibold))
                                            .foregroundColor(.black)
                                    }
                                    .padding(.vertical, 9)
                                    .padding(.horizontal, 12)
                                    .background(Color.white)
                                    .clipShape(RoundedRectangle(cornerRadius: 12))
                                    .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 1)
                                }
                            }
                            .padding(.top, 4)
                        }
                        .padding(.horizontal, BlindAISpacing.screenPadding)
                        .padding(.top, 8)
                        .padding(.bottom, 28)
                    }
                }
            }
            
            // Speaker repeat button
            SpeakerButton(textToRepeat: viewModel.instruction.spokenAnnouncement) {
                viewModel.repeatCurrentInstruction()
            }
            .padding(.trailing, 20)
            .padding(.bottom, 24)
        }
        .task {
            do {
                try await perceptionService.startPerception()
            } catch {
                print("[ActiveNav] Camera perception initialization note: \(error)")
            }
        }
        .onDisappear {
            perceptionService.stopPerception()
        }
        .alert("Route Details", isPresented: $viewModel.isShowingDetails) {
            Button("OK", role: .cancel) {}
        } message: {
            Text("Waypoint \(viewModel.currentWaypoint) of \(viewModel.totalWaypoints)\nHeading: North\nSurface: Paved Sidewalk\nObstacles: Path monitored continuously\nRemaining Distance: \(viewModel.instruction.distanceValue) meters")
        }
    }
    
    private func colorForDanger(_ level: DangerLevel) -> Color {
        switch level {
        case .safe: return .green
        case .caution: return .yellow
        case .warning: return .orange
        case .critical: return .red
        }
    }
}

#Preview {
    ActiveNavigationView(viewModel: ActiveNavigationViewModel())
}
