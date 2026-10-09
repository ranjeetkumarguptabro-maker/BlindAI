import Foundation
import AVFoundation
import UIKit
import Combine

/// Protocol defining live camera capture capabilities
public protocol CameraCaptureServiceProtocol: AnyObject {
    var isRunning: Bool { get }
    var framePublisher: AnyPublisher<UIImage, Never> { get }
    func startCapture() async throws
    func stopCapture()
    func captureCurrentFrameJPEG(compressionQuality: CGFloat) -> String?
}

/// Production-grade AVCaptureSession service for Blind AI.
/// Manages device rear-facing wide-angle camera with high-contrast exposure
/// and high-frequency video sample buffer streaming for real-time YOLO and Gemini Vision perception.
public final class CameraCaptureService: NSObject, ObservableObject, CameraCaptureServiceProtocol {
    public static let shared = CameraCaptureService()
    
    @Published public private(set) var isRunning: Bool = false
    @Published public private(set) var hasCameraPermission: Bool = false
    @Published public private(set) var currentFPS: Double = 0.0
    @Published public private(set) var latestCapturedImage: UIImage?
    
    private let frameSubject = PassthroughSubject<UIImage, Never>()
    public var framePublisher: AnyPublisher<UIImage, Never> {
        frameSubject.eraseToAnyPublisher()
    }
    
    public let captureSession = AVCaptureSession()
    private let videoOutput = AVCaptureVideoDataOutput()
    private let sessionQueue = DispatchQueue(label: "com.blindai.camera.sessionQueue", qos: .userInitiated)
    private let frameProcessingQueue = DispatchQueue(label: "com.blindai.camera.frameQueue", qos: .userInteractive)
    
    private var lastFrameTime: CFAbsoluteTime = 0
    private var frameCount: Int = 0
    private var lastFPSUpdateTime: CFAbsoluteTime = 0
    private var isConfigured: Bool = false
    
    public override init() {
        super.init()
        checkInitialPermission()
    }
    
    private func checkInitialPermission() {
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized:
            hasCameraPermission = true
        default:
            hasCameraPermission = false
        }
    }
    
    /// Requests camera authorization and prepares AVCaptureSession
    public func requestAuthorization() async -> Bool {
        let status = AVCaptureDevice.authorizationStatus(for: .video)
        switch status {
        case .authorized:
            DispatchQueue.main.async { self.hasCameraPermission = true }
            return true
        case .notDetermined:
            let granted = await AVCaptureDevice.requestAccess(for: .video)
            DispatchQueue.main.async { self.hasCameraPermission = granted }
            return granted
        default:
            DispatchQueue.main.async { self.hasCameraPermission = false }
            return false
        }
    }
    
    /// Configures the AVCaptureSession with rear wide-angle camera
    public func configureSession() throws {
        guard !isConfigured else { return }
        
        captureSession.beginConfiguration()
        captureSession.sessionPreset = .hd1280x720 // Optimized balance for YOLO inference & battery
        
        guard let device = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .back) else {
            captureSession.commitConfiguration()
            throw CameraError.deviceUnavailable
        }
        
        do {
            try device.lockForConfiguration()
            if device.isAutoFocusRangeRestrictionSupported {
                device.autoFocusRangeRestriction = .near
            }
            if device.isFocusModeSupported(.continuousAutoFocus) {
                device.focusMode = .continuousAutoFocus
            }
            if device.isExposureModeSupported(.continuousAutoExposure) {
                device.exposureMode = .continuousAutoExposure
            }
            device.unlockForConfiguration()
            
            let input = try AVCaptureDeviceInput(device: device)
            if captureSession.canAddInput(input) {
                captureSession.addInput(input)
            } else {
                captureSession.commitConfiguration()
                throw CameraError.inputAdditionFailed
            }
            
            videoOutput.alwaysDiscardsLateVideoFrames = true
            videoOutput.videoSettings = [
                kCVPixelBufferPixelFormatTypeKey as String: Int(kCVPixelFormatType_32BGRA)
            ]
            videoOutput.setSampleBufferDelegate(self, queue: frameProcessingQueue)
            
            if captureSession.canAddOutput(videoOutput) {
                captureSession.addOutput(videoOutput)
            } else {
                captureSession.commitConfiguration()
                throw CameraError.outputAdditionFailed
            }
            
            if let connection = videoOutput.connection(with: .video) {
                if connection.isVideoOrientationSupported {
                    connection.videoOrientation = .portrait
                }
                if connection.isVideoMirroringSupported {
                    connection.isVideoMirrored = false
                }
            }
            
            captureSession.commitConfiguration()
            isConfigured = true
        } catch {
            captureSession.commitConfiguration()
            throw error
        }
    }
    
    /// Starts real-time camera capture on dedicated background queue
    public func startCapture() async throws {
        guard await requestAuthorization() else {
            throw CameraError.permissionDenied
        }
        
        try configureSession()
        
        return try await withCheckedThrowingContinuation { continuation in
            sessionQueue.async { [weak self] in
                guard let self = self else { return }
                if !self.captureSession.isRunning {
                    self.captureSession.startRunning()
                    DispatchQueue.main.async {
                        self.isRunning = true
                    }
                }
                continuation.resume()
            }
        }
    }
    
    /// Stops camera capture session
    public func stopCapture() {
        sessionQueue.async { [weak self] in
            guard let self = self else { return }
            if self.captureSession.isRunning {
                self.captureSession.stopRunning()
                DispatchQueue.main.async {
                    self.isRunning = false
                }
            }
        }
    }
    
    /// Captures the most recent video frame converted to Base64 JPEG for Gemini Vision API
    public func captureCurrentFrameJPEG(compressionQuality: CGFloat = 0.65) -> String? {
        guard let image = latestCapturedImage else { return nil }
        guard let data = image.jpegData(compressionQuality: compressionQuality) else { return nil }
        return data.base64EncodedString()
    }
}

// MARK: - AVCaptureVideoDataOutputSampleBufferDelegate
extension CameraCaptureService: AVCaptureVideoDataOutputSampleBufferDelegate {
    public func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        let now = CFAbsoluteTimeGetCurrent()
        
        // Measure FPS
        frameCount += 1
        if now - lastFPSUpdateTime >= 1.0 {
            let fps = Double(frameCount) / (now - lastFPSUpdateTime)
            DispatchQueue.main.async {
                self.currentFPS = fps
            }
            frameCount = 0
            lastFPSUpdateTime = now
        }
        
        // Throttle frame emission to 10 FPS to preserve mobile battery
        guard now - lastFrameTime >= 0.10 else { return }
        lastFrameTime = now
        
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }
        let ciImage = CIImage(cvPixelBuffer: pixelBuffer)
        let context = CIContext(options: nil)
        guard let cgImage = context.createCGImage(ciImage, from: ciImage.extent) else { return }
        
        let uiImage = UIImage(cgImage: cgImage, scale: 1.0, orientation: .right)
        
        DispatchQueue.main.async {
            self.latestCapturedImage = uiImage
            self.frameSubject.send(uiImage)
        }
    }
}

public enum CameraError: LocalizedError {
    case permissionDenied
    case deviceUnavailable
    case inputAdditionFailed
    case outputAdditionFailed
    
    public var errorDescription: String? {
        switch self {
        case .permissionDenied: return "Camera access denied. Please enable in Settings."
        case .deviceUnavailable: return "Rear camera is unavailable on this device."
        case .inputAdditionFailed: return "Failed to add video input to capture session."
        case .outputAdditionFailed: return "Failed to add video output to capture session."
        }
    }
}
