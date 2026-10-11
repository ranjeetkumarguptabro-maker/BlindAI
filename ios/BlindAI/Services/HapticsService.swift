import UIKit

public protocol HapticsServiceProtocol {
    func impact(style: UIImpactFeedbackGenerator.FeedbackStyle)
    func notification(type: UINotificationFeedbackGenerator.FeedbackType)
    func selection()
    func turnLeftHaptic()
    func turnRightHaptic()
    func warningHaptic()
    func emergencySOSHaptic()
    func beaconAlignmentHaptic(onCourse: Bool)
}

public final class HapticsService: HapticsServiceProtocol {
    public static let shared = HapticsService()
    
    private init() {}
    
    public func impact(style: UIImpactFeedbackGenerator.FeedbackStyle = .medium) {
        let generator = UIImpactFeedbackGenerator(style: style)
        generator.prepare()
        generator.impactOccurred()
    }
    
    public func notification(type: UINotificationFeedbackGenerator.FeedbackType) {
        let generator = UINotificationFeedbackGenerator()
        generator.prepare()
        generator.notificationOccurred(type)
    }
    
    public func selection() {
        let generator = UISelectionFeedbackGenerator()
        generator.prepare()
        generator.selectionChanged()
    }
    
    /// Technical requirement: Left -> two distinct taps
    public func turnLeftHaptic() {
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.prepare()
        generator.impactOccurred()
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.18) {
            generator.impactOccurred()
        }
    }
    
    /// Technical requirement: Right -> three distinct taps
    public func turnRightHaptic() {
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.prepare()
        generator.impactOccurred()
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.15) {
            generator.impactOccurred()
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.15) {
                generator.impactOccurred()
            }
        }
    }
    
    /// Technical requirement: Head-height / hazard -> high-priority strong double pulse
    public func warningHaptic() {
        let generator = UINotificationFeedbackGenerator()
        generator.prepare()
        generator.notificationOccurred(.warning)
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
            generator.notificationOccurred(.error)
        }
    }
    
    /// Emergency SOS pulse: High-priority repetitive triple-pulse
    public func emergencySOSHaptic() {
        let generator = UINotificationFeedbackGenerator()
        generator.prepare()
        generator.notificationOccurred(.error)
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.15) {
            generator.notificationOccurred(.error)
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.15) {
                generator.notificationOccurred(.error)
            }
        }
    }
    
    /// Audio beacon compass alignment tick haptic
    public func beaconAlignmentHaptic(onCourse: Bool) {
        let generator = UIImpactFeedbackGenerator(style: onCourse ? .light : .heavy)
        generator.prepare()
        generator.impactOccurred()
    }
}
