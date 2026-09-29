import Foundation

// Test runner for Blind AI core logic
@main
struct LogicTestsRunner {
    static func main() {
        print("=== Running Blind AI Core Logic Test Suite ===")
        
        testSafetyStateMachine()
        testCueDecider()
        testLaneMath()
        testNavigationInstruction()
        testVoiceIntentParsing()
        
        print("\n✅ All Blind AI Logic Tests Passed Successfully!")
    }
    
    static func testSafetyStateMachine() {
        print("Testing SafetyStateMachine transitions...")
        let sm = SafetyStateMachine()
        assert(sm.currentState == .idle, "Initial state must be idle")
        
        // Idle -> Walking
        assert(sm.transition(to: .walking), "Should transition from idle to walking")
        assert(sm.currentState == .walking)
        
        // Walking -> Turn
        assert(sm.transition(to: .turn), "Should transition from walking to turn")
        assert(sm.currentState == .turn)
        
        // Turn -> Arrival
        assert(sm.transition(to: .arrival), "Should transition from turn to arrival")
        assert(sm.currentState == .arrival)
        
        // Arrival -> Idle
        assert(sm.transition(to: .idle), "Should transition from arrival to idle")
        assert(sm.currentState == .idle)
        
        // Emergency transition from any state
        assert(sm.transition(to: .emergency), "Should transition from any state to emergency")
        assert(sm.currentState == .emergency)
        
        // Emergency -> Idle
        assert(sm.transition(to: .idle))
        
        // Invalid transition: Idle cannot directly transition to Turn
        assert(!sm.transition(to: .turn), "Idle should not transition directly to turn")
        print("  ✓ SafetyStateMachine tests passed")
    }
    
    static func testCueDecider() {
        print("Testing CueDecider priorities...")
        let decider = CueDecider()
        
        let navCue = CueDecider.Cue(priority: .navigation, spokenMessage: "Take a right in 41m", hapticPattern: "light")
        let turnCue = CueDecider.Cue(priority: .turnImminent, spokenMessage: "Turn right now", hapticPattern: "turnRight")
        let emergencyCue = CueDecider.Cue(priority: .emergency, spokenMessage: "Stop. Hazard ahead", hapticPattern: "hazard")
        
        assert(decider.shouldPreempt(activeCue: navCue, newCue: turnCue), "Turn cue should preempt navigation cue")
        assert(decider.shouldPreempt(activeCue: turnCue, newCue: emergencyCue), "Emergency cue should preempt turn cue")
        assert(!decider.shouldPreempt(activeCue: emergencyCue, newCue: navCue), "Nav cue should NOT preempt emergency cue")
        print("  ✓ CueDecider tests passed")
    }
    
    static func testLaneMath() {
        print("Testing LaneMath 3x2 grid...")
        var laneMath = LaneMath()
        assert(laneMath.grid.count == 6, "Must have 3x2 = 6 grid cells")
        assert(laneMath.isCenterClear, "Initial grid should be clear")
        assert(laneMath.nearestObstacle() == nil, "No obstacles initially")
        
        // Place an obstacle in the center torso cell
        laneMath.grid[2] = LaneMath.GridCell(horizontal: .center, vertical: .torso, distanceMeters: 2.5, confidence: 0.95, isObstacle: true)
        assert(!laneMath.isCenterClear, "Center should no longer be clear")
        
        let nearest = laneMath.nearestObstacle()
        assert(nearest != nil)
        assert(nearest?.distanceMeters == 2.5)
        assert(nearest?.horizontal == .center)
        print("  ✓ LaneMath tests passed")
    }
    
    static func testNavigationInstruction() {
        print("Testing NavigationInstruction spoken announcement...")
        let inst = NavigationInstruction(
            title: "Navigation",
            mainInstruction: "Take a right onto the sidewalk.",
            distanceValue: "41",
            distanceUnit: "m",
            maneuverText: "Veer left 152°",
            maneuverIcon: "arrow.turn.up.left"
        )
        
        let spoken = inst.spokenAnnouncement
        assert(spoken.contains("Take a right onto the sidewalk"), "Should contain main instruction")
        assert(spoken.contains("41 meters"), "Should format 41 m into 41 meters")
        assert(spoken.contains("Veer left 152°"), "Should include next maneuver")
        print("  ✓ NavigationInstruction tests passed")
    }
    
    static func testVoiceIntentParsing() {
        print("Testing VoiceIntent parsing...")
        let speech = SpeechService()
        
        let intent1 = speech.parseIntent(from: "Take me to CIF")
        assert(intent1 == .startNavigation(destination: "Campus Instructional Facility"))
        
        let intent2 = speech.parseIntent(from: "Can you describe what's in front of me?")
        assert(intent2 == .describeEnvironment)
        
        let intent3 = speech.parseIntent(from: "Where am I right now?")
        assert(intent3 == .whereAmI)
        
        let intent4 = speech.parseIntent(from: "Stop navigation please")
        assert(intent4 == .stop)
        
        let intent5 = speech.parseIntent(from: "Repeat the instruction")
        assert(intent5 == .repeatInstruction)
        print("  ✓ VoiceIntent parsing tests passed")
    }
}
