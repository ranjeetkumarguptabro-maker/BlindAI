import Foundation
import Combine

public protocol NavigationServiceProtocol: ObservableObject {
    var currentInstruction: NavigationInstruction { get }
    var isNavigating: Bool { get }
    func startRoute()
    func stopRoute()
}

public final class MockNavigationService: NavigationServiceProtocol, ObservableObject {
    public static let shared = MockNavigationService()
    
    @Published public var currentInstruction: NavigationInstruction = .mock
    @Published public var isNavigating: Bool = false
    
    public init() {}
    
    public func startRoute() {
        isNavigating = true
    }
    
    public func stopRoute() {
        isNavigating = false
    }
}
