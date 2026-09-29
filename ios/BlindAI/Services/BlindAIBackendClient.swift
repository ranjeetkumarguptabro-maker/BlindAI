import Foundation

/// BlindAIBackendClient manages communication between the iOS app and our Blind AI Backend.
/// CRITICAL: The iOS app NEVER contacts Gemini directly and NEVER contains the GEMINI_API_KEY.
/// All AI perception and reasoning is routed through our backend API server.
public final class BlindAIBackendClient {
    public static let shared = BlindAIBackendClient()
    
    // Configurable backend base URL (default local development port 3000)
    public var baseURL: URL = URL(string: "http://localhost:3000/api/v1")!
    
    private let urlSession: URLSession
    
    private init() {
        let configuration = URLSessionConfiguration.default
        configuration.timeoutIntervalForRequest = 8.0
        self.urlSession = URLSession(configuration: configuration)
    }
    
    // MARK: - API Calls
    
    /// Requests environment/camera scene description from backend AI service
    public func describeEnvironment(imageBase64: String? = nil) async throws -> String {
        let url = baseURL.appendingPathComponent("environment/describe")
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        var payload: [String: Any] = [:]
        if let imageBase64 {
            payload["imageBase64"] = imageBase64
        }
        request.httpBody = try JSONSerialization.data(withJSONObject: payload)
        
        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        
        if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
           let dataObj = json["data"] as? [String: Any],
           let desc = dataObj["description"] as? String {
            return desc
        }
        
        throw URLError(.cannotParseResponse)
    }
    
    /// Requests landmark & orientation context from backend AI service
    public func whereAmI(latitude: Double, longitude: Double, heading: String = "East") async throws -> (headline: String, orientation: String) {
        let url = baseURL.appendingPathComponent("environment/where-am-i")
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let payload: [String: Any] = [
            "latitude": latitude,
            "longitude": longitude,
            "heading": heading,
            "street": "Paula Valdena iela",
            "landmark": "Riga Technical University (RTU), Ķīpsala Campus"
        ]
        request.httpBody = try JSONSerialization.data(withJSONObject: payload)
        
        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        
        if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
           let dataObj = json["data"] as? [String: Any],
           let headline = dataObj["headline"] as? String,
           let orientation = dataObj["orientationDetails"] as? String {
            return (headline, orientation)
        }
        
        throw URLError(.cannotParseResponse)
    }
    
    /// Parses natural language spoken command via backend AI service
    public func parseVoiceIntent(transcript: String) async throws -> VoiceIntent {
        let url = baseURL.appendingPathComponent("voice/intent")
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let payload: [String: Any] = ["transcript": transcript]
        request.httpBody = try JSONSerialization.data(withJSONObject: payload)
        
        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        
        if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
           let dataObj = json["data"] as? [String: Any],
           let intentStr = dataObj["intent"] as? String {
            switch intentStr {
            case "start_navigation":
                let dest = dataObj["destination"] as? String ?? "Riga Technical University (RTU)"
                return .startNavigation(destination: dest)
            case "where_am_i":
                return .whereAmI
            case "describe_environment":
                return .describeEnvironment
            case "stop":
                return .stop
            case "repeat":
                return .repeatInstruction
            default:
                return .unknown(query: transcript)
            }
        }
        
        throw URLError(.cannotParseResponse)
    }
    
    /// Reports an obstacle detection event to the backend according to Backend Schema
    public func logObstacleEvent(
        type: String = "construction_barrier",
        lane: String = "right",
        distanceMeters: Double = 2.0,
        severity: String = "warning"
    ) async throws -> Bool {
        let url = baseURL.appendingPathComponent("navigation/sessions/default/events")
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let payload: [String: Any] = [
            "obstacle_type": type,
            "lane": lane,
            "height_zone": "torso",
            "distance_meters": distanceMeters,
            "confidence": 0.96,
            "severity": severity,
            "action_taken": "avoid_left",
            "detected_at": ISO8601DateFormatter().string(from: Date())
        ]
        request.httpBody = try JSONSerialization.data(withJSONObject: payload)
        
        let (_, response) = try await urlSession.data(for: request)
        if let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) {
            return true
        }
        return false
    }
}

