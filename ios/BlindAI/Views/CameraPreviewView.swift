import SwiftUI
import AVFoundation

/// SwiftUI UIViewRepresentable wrapper for AVCaptureVideoPreviewLayer.
/// Renders the live hardware camera feed with hardware acceleration.
public struct CameraPreviewView: UIViewRepresentable {
    public let captureSession: AVCaptureSession
    
    public init(captureSession: AVCaptureSession = CameraCaptureService.shared.captureSession) {
        self.captureSession = captureSession
    }
    
    public func makeUIView(context: Context) -> CameraPreviewUIView {
        let view = CameraPreviewUIView()
        view.videoPreviewLayer.session = captureSession
        view.videoPreviewLayer.videoGravity = .resizeAspectFill
        return view
    }
    
    public func updateUIView(_ uiView: CameraPreviewUIView, context: Context) {
        // Layout updates handled automatically by UIKit layer
    }
}

public class CameraPreviewUIView: UIView {
    public override class var layerClass: AnyClass {
        AVCaptureVideoPreviewLayer.self
    }
    
    public var videoPreviewLayer: AVCaptureVideoPreviewLayer {
        layer as! AVCaptureVideoPreviewLayer
    }
}
