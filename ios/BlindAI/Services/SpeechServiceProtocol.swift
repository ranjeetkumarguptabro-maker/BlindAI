import Foundation

public protocol SpeechServiceProtocol {
    var isListening: Bool { get }
    func startListening()
    func stopListening()
    func speak(_ text: String)
}

public final class MockSpeechService: SpeechServiceProtocol {
    public static let shared = MockSpeechService()
    
    public var isListening: Bool = false
    
    public init() {}
    
    public func startListening() {
        isListening = true
    }
    
    public func stopListening() {
        isListening = false
    }
    
    public func speak(_ text: String) {
        // Mock speech announcement for Phase 1
    }
}
