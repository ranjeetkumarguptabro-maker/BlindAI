import Foundation

/// FallDetector handles accelerometer and gyroscope drop/impact thresholds.
/// Roadmap: Phase 13 (Emergency)
public final class FallDetector {
    public var onPossibleFall: (() -> Void)?
    public init() {}
}
