import Foundation
import Combine
import CoreLocation

public final class NavigationService: NSObject, NavigationServiceProtocol, ObservableObject, CLLocationManagerDelegate {
    public static let shared = NavigationService()
    
    @Published public private(set) var isNavigating: Bool = false
    @Published public private(set) var currentInstruction: NavigationInstruction = .mock
    @Published public private(set) var currentWaypointIndex: Int = 0
    @Published public private(set) var remainingDistanceMeters: Int = 41
    @Published public private(set) var totalRouteDistanceMeters: Int = 136
    @Published public private(set) var estimatedTimeSeconds: Int = 105
    @Published public private(set) var routeName: String = "Campus Instructional Facility (CIF)"
    
    public let stateMachine = SafetyStateMachine()
    private let speechService = SpeechService.shared
    private let hapticsService = HapticsService.shared
    private let locationManager = CLLocationManager()
    
    private var simulationTimer: Timer?
    
    private let waypoints: [NavigationInstruction] = [
        NavigationInstruction(
            title: "Navigation",
            mainInstruction: "Take a right onto the sidewalk.",
            distanceValue: "41",
            distanceUnit: "m",
            maneuverText: "Veer left 152°",
            maneuverIcon: "arrow.turn.up.left"
        ),
        NavigationInstruction(
            title: "Navigation",
            mainInstruction: "Continue straight along the main quad.",
            distanceValue: "65",
            distanceUnit: "m",
            maneuverText: "Head straight",
            maneuverIcon: "arrow.up"
        ),
        NavigationInstruction(
            title: "Navigation",
            mainInstruction: "Approaching crosswalk. Listen for traffic.",
            distanceValue: "20",
            distanceUnit: "m",
            maneuverText: "Crosswalk ahead",
            maneuverIcon: "figure.walk"
        ),
        NavigationInstruction(
            title: "Navigation",
            mainInstruction: "Turn right. You have arrived at CIF entrance.",
            distanceValue: "10",
            distanceUnit: "m",
            maneuverText: "Destination on right",
            maneuverIcon: "checkmark.circle.fill"
        )
    ]
    
    public override init() {
        super.init()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
    }
    
    public func startRoute() {
        isNavigating = true
        currentWaypointIndex = 0
        currentInstruction = waypoints[0]
        remainingDistanceMeters = Int(currentInstruction.distanceValue) ?? 41
        
        stateMachine.transition(to: .walking)
        hapticsService.notification(type: .success)
        
        // Start continuous LiDAR scanning along the walking path
        ARKitLiDARScannerService.shared.startScanning()
        
        // Announce route start
        let initialPrompt = "Starting walking route to \(routeName). \(currentInstruction.mainInstruction) in \(remainingDistanceMeters) meters."
        speechService.speak(initialPrompt)
        
        // Trigger GPS or realistic walking countdown simulation
        startWalkingSimulation()
    }
    
    public func stopRoute() {
        simulationTimer?.invalidate()
        simulationTimer = nil
        
        // Stop LiDAR scanning when navigation ends
        ARKitLiDARScannerService.shared.stopScanning()
        
        isNavigating = false
        stateMachine.transition(to: .idle)
        
        hapticsService.impact(style: .heavy)
        speechService.speak("Navigation stopped. Returning to home.")
    }
    
    public func repeatInstruction() {
        let text = "\(currentInstruction.mainInstruction). Distance: \(remainingDistanceMeters) meters. Next maneuver: \(currentInstruction.maneuverText)."
        hapticsService.selection()
        speechService.speak(text)
    }
    
    private func startWalkingSimulation() {
        simulationTimer?.invalidate()
        // Simulate walking progress every 2.5 seconds (steps through distance and waypoints)
        simulationTimer = Timer.scheduledTimer(withTimeInterval: 2.2, repeats: true) { [weak self] _ in
            guard let self = self, self.isNavigating else { return }
            
            if self.remainingDistanceMeters > 5 {
                self.remainingDistanceMeters -= 4
                self.updateCurrentInstructionDistance()
                
                // Voice guidance milestones
                if self.remainingDistanceMeters == 30 || self.remainingDistanceMeters == 15 {
                    self.speechService.speak("\(self.currentInstruction.mainInstruction) in \(self.remainingDistanceMeters) meters.")
                    self.hapticsService.impact(style: .light)
                }
            } else {
                // Waypoint reached! Transition to next waypoint
                self.advanceToNextWaypoint()
            }
        }
    }
    
    private func updateCurrentInstructionDistance() {
        let updated = NavigationInstruction(
            title: currentInstruction.title,
            mainInstruction: currentInstruction.mainInstruction,
            distanceValue: "\(max(remainingDistanceMeters, 0))",
            distanceUnit: currentInstruction.distanceUnit,
            maneuverText: currentInstruction.maneuverText,
            maneuverIcon: currentInstruction.maneuverIcon
        )
        self.currentInstruction = updated
    }
    
    private func advanceToNextWaypoint() {
        if currentWaypointIndex + 1 < waypoints.count {
            currentWaypointIndex += 1
            currentInstruction = waypoints[currentWaypointIndex]
            remainingDistanceMeters = Int(currentInstruction.distanceValue) ?? 20
            
            stateMachine.transition(to: .turn)
            
            // Directional haptic feedback for the turn
            if currentInstruction.maneuverIcon.contains("left") {
                hapticsService.turnLeftHaptic()
            } else if currentInstruction.maneuverIcon.contains("right") {
                hapticsService.turnRightHaptic()
            } else {
                hapticsService.notification(type: .success)
            }
            
            // Speak next turn guidance
            speechService.speak("\(currentInstruction.mainInstruction) in \(remainingDistanceMeters) meters.")
        } else {
            // Arrival reached!
            simulationTimer?.invalidate()
            simulationTimer = nil
            stateMachine.transition(to: .arrival)
            hapticsService.notification(type: .success)
            speechService.speak("You have arrived at your destination: \(routeName).")
        }
    }
}
