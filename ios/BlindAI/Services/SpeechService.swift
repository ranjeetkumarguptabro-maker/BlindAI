import Foundation
import Speech
import AVFoundation
import Combine

public enum VoiceIntent: Equatable {
    case startNavigation(destination: String)
    case describeEnvironment
    case whereAmI
    case stop
    case repeatInstruction
    case unknown(query: String)
}

public protocol SpeechServiceDelegate: AnyObject {
    func speechService(_ service: SpeechServiceProtocol, didUpdateTranscription text: String)
    func speechService(_ service: SpeechServiceProtocol, didDetectIntent intent: VoiceIntent)
    func speechService(_ service: SpeechServiceProtocol, didUpdateAudioLevel level: Float)
}

public final class SpeechService: NSObject, SpeechServiceProtocol, ObservableObject, AVSpeechSynthesizerDelegate {
    public static let shared = SpeechService()
    
    @Published public private(set) var isListening: Bool = false
    @Published public private(set) var liveTranscript: String = ""
    @Published public private(set) var audioLevel: Float = 0.0 // 0.0 to 1.0
    @Published public private(set) var isSpeaking: Bool = false
    
    public weak var delegate: SpeechServiceDelegate?
    
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()
    private let speechSynthesizer = AVSpeechSynthesizer()
    
    private var silenceTimer: Timer?
    
    public override init() {
        super.init()
        speechSynthesizer.delegate = self
    }
    
    public func startListening() {
        guard !isListening else { return }
        
        // Cancel any pending speech
        stopSpeaking()
        
        requestAuthorization { [weak self] authorized in
            guard let self = self, authorized else {
                // If not authorized or on simulator, start simulated speech listener
                self?.startSimulatedListening()
                return
            }
            self.beginAudioEngineRecognition()
        }
    }
    
    public func stopListening() {
        silenceTimer?.invalidate()
        silenceTimer = nil
        
        if audioEngine.isRunning {
            audioEngine.stop()
            audioEngine.inputNode.removeTap(onBus: 0)
        }
        
        recognitionRequest?.endAudio()
        recognitionTask?.cancel()
        
        recognitionRequest = nil
        recognitionTask = nil
        
        DispatchQueue.main.async {
            self.isListening = false
            self.audioLevel = 0.0
        }
    }
    
    public func speak(_ text: String, completion: (() -> Void)? = nil) {
        guard !text.isEmpty else {
            completion?()
            return
        }
        
        DispatchQueue.main.async {
            self.isSpeaking = true
        }
        
        // Interrupt previous speech
        if speechSynthesizer.isSpeaking {
            speechSynthesizer.stopSpeaking(at: .immediate)
        }
        
        let utterance = AVSpeechUtterance(string: text)
        utterance.rate = AVSpeechUtteranceDefaultVoiceRate
        utterance.pitchMultiplier = 1.0
        utterance.voice = AVSpeechSynthesisVoice(language: "en-US")
        
        speechSynthesizer.speak(utterance)
    }
    
    public func stopSpeaking() {
        if speechSynthesizer.isSpeaking {
            speechSynthesizer.stopSpeaking(at: .immediate)
            DispatchQueue.main.async {
                self.isSpeaking = false
            }
        }
    }
    
    // MARK: - AVSpeechSynthesizerDelegate
    public func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didFinish utterance: AVSpeechUtterance) {
        DispatchQueue.main.async {
            self.isSpeaking = false
        }
    }
    
    public func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didCancel utterance: AVSpeechUtterance) {
        DispatchQueue.main.async {
            self.isSpeaking = false
        }
    }
    
    // MARK: - Internal Recognition
    private func beginAudioEngineRecognition() {
        // Reset previous tasks
        recognitionTask?.cancel()
        recognitionTask = nil
        
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(.playAndRecord, mode: .measurement, options: [.duckOthers, .defaultToSpeaker])
            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        } catch {
            print("AudioSession setup error: \(error)")
        }
        
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let recognitionRequest = recognitionRequest else { return }
        recognitionRequest.shouldReportPartialResults = true
        
        let inputNode = audioEngine.inputNode
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { [weak self] buffer, _ in
            self?.recognitionRequest?.append(buffer)
            
            // Audio power metering
            guard let channelData = buffer.floatChannelData?[0] else { return }
            let frameLength = Int(buffer.frameLength)
            var sum: Float = 0
            for i in 0..<frameLength {
                sum += channelData[i] * channelData[i]
            }
            let rms = sqrt(sum / Float(frameLength))
            let normalized = min(max(rms * 5.0, 0.0), 1.0)
            
            DispatchQueue.main.async {
                self?.audioLevel = normalized
                self?.delegate?.speechService(self!, didUpdateAudioLevel: normalized)
            }
        }
        
        audioEngine.prepare()
        do {
            try audioEngine.start()
            DispatchQueue.main.async {
                self.isListening = true
                self.liveTranscript = ""
            }
        } catch {
            print("AudioEngine could not start: \(error)")
            startSimulatedListening()
            return
        }
        
        recognitionTask = speechRecognizer?.recognitionTask(with: recognitionRequest) { [weak self] result, error in
            guard let self = self else { return }
            
            if let result = result {
                let transcription = result.bestTranscription.formattedString
                DispatchQueue.main.async {
                    self.liveTranscript = transcription
                    self.delegate?.speechService(self, didUpdateTranscription: transcription)
                }
                
                // Reset silence timer on new transcription
                self.resetSilenceTimer(for: transcription)
            }
            
            if error != nil || result?.isFinal == true {
                self.stopListening()
            }
        }
    }
    
    private func resetSilenceTimer(for text: String) {
        silenceTimer?.invalidate()
        silenceTimer = Timer.scheduledTimer(withTimeInterval: 1.6, repeats: false) { [weak self] _ in
            guard let self = self else { return }
            let intent = self.parseIntent(from: text)
            DispatchQueue.main.async {
                self.delegate?.speechService(self, didDetectIntent: intent)
                self.stopListening()
            }
        }
    }
    
    public func parseIntentAsync(from text: String) async -> VoiceIntent {
        do {
            return try await BlindAIBackendClient.shared.parseVoiceIntent(transcript: text)
        } catch {
            return parseIntent(from: text)
        }
    }
    
    public func parseIntent(from text: String) -> VoiceIntent {
        let lowered = text.lowercased().trimmingCharacters(in: .whitespacesAndNewlines)
        
        if lowered.contains("cif") || lowered.contains("take me to") || lowered.contains("start navigation") || lowered.contains("directions") {
            let destination = lowered.contains("cif") ? "Campus Instructional Facility" : "Destination"
            return .startNavigation(destination: destination)
        } else if lowered.contains("where am i") || lowered.contains("location") {
            return .whereAmI
        } else if lowered.contains("what's in front") || lowered.contains("front of me") || lowered.contains("around me") || lowered.contains("describe") {
            return .describeEnvironment
        } else if lowered.contains("stop") || lowered.contains("cancel") || lowered.contains("end") {
            return .stop
        } else if lowered.contains("repeat") || lowered.contains("again") {
            return .repeatInstruction
        } else {
            return .unknown(query: text)
        }
    }
    
    private func startSimulatedListening() {
        DispatchQueue.main.async {
            self.isListening = true
            self.liveTranscript = "Listening for your voice..."
            self.audioLevel = 0.5
        }
    }
    
    private func requestAuthorization(completion: @escaping (Bool) -> Void) {
        SFSpeechRecognizer.requestAuthorization { authStatus in
            DispatchQueue.main.async {
                completion(authStatus == .authorized)
            }
        }
    }
}
