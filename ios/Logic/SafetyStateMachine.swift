import Foundation

/// SafetyStateMachine coordinates user walking states, turns, obstacles, and emergency transitions.
public enum SafetyState: String, Sendable, Equatable {
    case idle
    case routePreview
    case walking
    case obstacle
    case turn
    case intersection
    case offRoute
    case arrival
    case emergency
}

public protocol SafetyStateMachineDelegate: AnyObject {
    func stateMachine(_ machine: SafetyStateMachine, didTransitionFrom oldState: SafetyState, to newState: SafetyState)
}

public final class SafetyStateMachine {
    public private(set) var currentState: SafetyState = .idle
    public weak var delegate: SafetyStateMachineDelegate?
    
    public init(initialState: SafetyState = .idle) {
        self.currentState = initialState
    }
    
    @discardableResult
    public func transition(to newState: SafetyState) -> Bool {
        guard isValidTransition(from: currentState, to: newState) else {
            print("Invalid state transition from \(currentState) to \(newState)")
            return false
        }
        
        let oldState = currentState
        currentState = newState
        delegate?.stateMachine(self, didTransitionFrom: oldState, to: newState)
        return true
    }
    
    private func isValidTransition(from: SafetyState, to: SafetyState) -> Bool {
        if to == .emergency { return true } // Emergency can trigger from any state
        
        switch from {
        case .idle:
            return to == .routePreview || to == .walking
        case .routePreview:
            return to == .walking || to == .idle
        case .walking:
            return to == .turn || to == .obstacle || to == .intersection || to == .offRoute || to == .arrival || to == .idle
        case .turn:
            return to == .walking || to == .obstacle || to == .intersection || to == .arrival || to == .idle
        case .obstacle:
            return to == .walking || to == .turn || to == .emergency || to == .idle
        case .intersection:
            return to == .walking || to == .turn || to == .arrival || to == .idle
        case .offRoute:
            return to == .walking || to == .idle
        case .arrival:
            return to == .idle
        case .emergency:
            return to == .idle || to == .walking
        }
    }
}
