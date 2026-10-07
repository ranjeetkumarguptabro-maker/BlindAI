# 🦯 Blind AI — Next-Gen Assistive Navigation System

[![Swift 6](https://img.shields.io/badge/Swift-6.0-FA7343?logo=swift&logoColor=white)](https://swift.org)
[![iOS 17+](https://img.shields.io/badge/iOS-17.0+-007AFF?logo=apple&logoColor=white)](https://developer.apple.com/ios/)
[![ARKit LiDAR](https://img.shields.io/badge/ARKit-LiDAR%20sceneDepth-FF9500?logo=apple&logoColor=white)](https://developer.apple.com/augmented-reality/)
[![Vision Framework](https://img.shields.io/badge/Vision-Object%20Detection-5856D6?logo=apple&logoColor=white)](https://developer.apple.com/documentation/vision)
[![Gemini AI](https://img.shields.io/badge/Gemini-1.5%20Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Node.js](https://img.shields.io/badge/Node.js-20+-339933?logo=node.js&logoColor=white)](https://nodejs.org)
[![WCAG 2.2](https://img.shields.io/badge/Accessibility-WCAG%202.2%20AAA-34C759)](https://www.w3.org/WAI/standards-guidelines/wcag/)

**Blind AI** is a retrofit, real-time smart assistive navigation platform engineered specifically for blind and visually impaired pedestrians. It fuses **Apple ARKit LiDAR (`sceneDepth`)**, **Camera Vision object detection**, **Google Gemini multimodal intelligence**, and a **Danger Decision Engine** with synchronized haptic and preemptive spatial audio feedback.

---

## 📑 Table of Contents

1. [Key Capabilities](#-key-capabilities)
2. [Security & Zero-Client-Key Architecture](#-security--zero-client-key-architecture)
3. [Sensor Fusion & Danger Decision Pipeline](#-sensor-fusion--danger-decision-pipeline)
4. [Obstacle Danger Rules & Audio Rate-Limiting](#-obstacle-danger-rules--audio-rate-limiting)
5. [Natural Language Voice Navigation (Gemini AI)](#-natural-language-voice-navigation-gemini-ai)
6. [Complete 9-Screen Workflow & State Machine](#-complete-9-screen-workflow--state-machine)
7. [Accessibility Engineering (WCAG 2.2 AAA)](#-accessibility-engineering-wcag-22-aaa)
8. [Backend API Reference](#-backend-api-reference)
9. [Project Directory Layout](#-project-directory-layout)
10. [Local Development & Quick Start](#-local-development--quick-start)
11. [Running the Native iOS Swift App](#-running-the-native-ios-swift-app)

---

## 🌟 Key Capabilities

- **ARKit LiDAR Spatial Scanning**: Direct reading of raw `CVPixelBuffer` depth maps (`kCVPixelFormatType_DepthFloat32`) filtered by confidence maps (`kCVPixelFormatType_OneComponent8`) to accurately measure distances from 0.3 m to 5.0+ m in daylight or total darkness.
- **Vision Object Classification**: Identifies 12 canonical street and indoor obstacle classes (`person`, `car`, `chair`, `table`, `wall`, `pole`, `tree`, `door`, `stairs`, `construction_barrier`, `trash_bin`, `bench`) at 15 FPS.
- **Corridor Lane & Vertical Height Mapping**: Categorizes obstacles into lateral zones (`left`, `center/walking path`, `right`) and vertical clearance (`ground`, `torso`, `head`).
- **Emergency Speech & Haptic Preemption**: Immediate override for critical hazards (<0.7 m) that halts navigation speech instantly and dispatches heavy continuous haptic vibration.
- **Ground Hazard Elevation Delta Tracking**: Analyzes point-cloud ground elevation deltas to detect drop-offs, curbs, stairs, potholes, and depressions.
- **Natural Language Destination Routing**: Voice commands powered by Google Gemini 1.5 Flash supporting both structured locations and arbitrary spoken addresses with clarification for ambiguous phrases.
- **Automatic Walking Safety Triggers**: Walk simulator auto-triggers obstacle alerts after 40–50 m walked and crosswalk safety after +20 m walked.
- **Dual-View Web Simulator**: Toggle seamlessly between clean **Pure Mobile View** and **Interactive Simulator Tools** (distance sliders, obstacle presets, depth map heatmaps).

---

## 🔒 Security & Zero-Client-Key Architecture

Per strict enterprise security guidelines:
1. **Zero Client-Side Keys**: API keys (`GEMINI_API_KEY`, `SUPABASE_KEY`) are **never** bundled in the iOS binary, HTML, or committed to GitHub.
2. **Backend Proxy Pattern**: The client app communicates exclusively with `/api/v1` over secure HTTPS.
3. **Environment Isolation**: Production secrets are managed through `backend/.env` (strictly excluded via `.gitignore`) or Vercel Environment Variables.
4. **Modular Fallbacks**: In offline or mock environments, local reasoning fallbacks ensure the app remains fully functional without crashing.

```
┌─────────────────────────────────┐
│       iOS App (SwiftUI)         │
│     (BlindAIBackendClient)      │
└────────────────┬────────────────┘
                 │ HTTP (localhost:3000/api/v1)
                 │ [No Secrets in App]
                 ▼
┌─────────────────────────────────┐
│        Blind AI Backend         │
│   (Node.js / Express Server)    │
│  Loads GEMINI_API_KEY from .env │
└────────────────┬────────────────┘
                 │
                 ├── AIProviderInterface (Modular Abstraction)
                 │         │
                 │         ▼
                 │   GeminiProvider (1.5 Flash)
                 │
                 ▼ HTTPS
┌─────────────────────────────────┐
│     Google Gemini API (Cloud)   │
└─────────────────────────────────┘
```

---

## 📡 Sensor Fusion & Danger Decision Pipeline

```
                        ┌────────────────────────────────────────────────┐
                        │      iPhone Camera + LiDAR Sensor Suite        │
                        └──────────────────────┬─────────────────────────┘
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       ▼                                               ▼
         ┌───────────────────────────┐                   ┌───────────────────────────┐
         │ Vision Framework Detector │                   │  ARKit sceneDepth Service │
         │   (VisionObjectDetector)  │                   │ (ARKitLiDARScannerService)│
         └─────────────┬─────────────┘                   └─────────────┬─────────────┘
                       │ Bounding Box + Category                       │ Depth Float32 Map +
                       │ Lane: Left | Center | Right                   │ Confidence Map Filtering
                       └───────────────────────┬───────────────────────┘
                                               ▼
                                 ┌───────────────────────────┐
                                 │   Sensor Fusion Router    │
                                 │  (LiDAR Region Sampling)  │
                                 └─────────────┬─────────────┘
                                               │ Target Distance + Lane + Height
                                               ▼
                                 ┌───────────────────────────┐
                                 │   Obstacle Danger System  │
                                 │   (ObstacleDangerSystem)  │
                                 └─────────────┬─────────────┘
                                               │ Danger Level & Rate Limiter
                       ┌───────────────────────┴───────────────────────┐
                       ▼                                               ▼
         ┌───────────────────────────┐                   ┌───────────────────────────┐
         │  Haptic Feedback Engine   │                   │  Speech Audio Dispatcher  │
         │ (UINotificationFeedback)  │                   │   (AVSpeechSynthesizer)   │
         │ - Urgent: Double heavy    │                   │ - Preempts ongoing speech │
         │ - Critical: Continuous    │                   │   for <0.7m "Stop"        │
         └───────────────────────────┘                   └───────────────────────────┘
```

---

## ⚠️ Obstacle Danger Rules & Audio Rate-Limiting

The decision engine classifies threats based on distance, lateral lane position, and obstacle category:

| Distance & Position | Danger Level | Spoken Audio Alert | Haptic Trigger | Visual / AR Overlay |
| :--- | :--- | :--- | :--- | :--- |
| **< 0.7 m, in path** | **Critical Stop** | *“Stop. Obstacle directly ahead.”* | Continuous heavy vibration (**Preempts all ongoing speech**) | Pulsing red bounding box & stop banner |
| **1.0 m, in path** | **Danger** | *“Obstacle ahead, 1 meter.”* | Double strong notification pulse | Orange bounding box with distance badge |
| **2.0 m, in path** | **Caution** | *“[Object] ahead, 2 meters. Keep left/right.”* | Directional cautionary vibration | Amber bounding box with directional guidance |
| **3.0 m, in path** | **Notice** | *“Object ahead.”* | Single subtle tap | Blue informational bounding box |
| **4.0 m, beside path** | **Safe / Ambient** | *Silent* (ambient log only) | None (Prevents sensory fatigue) | Green distance indicator |

### Auditory Overload Prevention
- Non-critical notifications enforce a **3.2-second rate-limiting window** to avoid audio fatigue.
- Critical hazards (**< 0.7 m**) bypass all cooldown timers, cancel active speech utterances, and sound immediately.

---

## 🎙️ Natural Language Voice Navigation (Gemini AI)

Tapping the microphone button activates the Voice Assistant, which supports natural conversational queries:

```
User: "Take me to the library"
Gemini: Understands destination -> Resolves to RTU Central Library -> Plans 8-waypoint walking route.

User: "Open the sports center"
Gemini: Matches RTU Sports Center -> Announces distance & duration -> Opens route preview.

User: "What is in front of me?"
Gemini + LiDAR: Reads live LiDAR depth buffer -> "There is a bicycle rack approximately 3 meters ahead on your right."

User: "Where am I?"
Gemini: Queries GPS & compass -> "You are near Riga Technical University, Ķīpsala Campus in Riga, Latvia. Facing east."

User: "Take me somewhere" (Ambiguous)
Gemini: Clarification flow -> "Where would you like to go? You can say the library, the main building, or any location in Riga."
```

---

## 📱 Complete 9-Screen Workflow & State Machine

```
                                  [ 1. HOME ]
                                       │
     ┌───────────────────┬─────────────┴─────────────┬───────────────────┐
     │                   │                           │                   │
Tap Microphone   Start navigation             Where am I?       Describe around me
     │                   │                           │                   │
     ▼                   ▼                           ▼                   ▼
[ 2. LISTENING ]  [ 3. DESTINATION SEARCH ]    [ 6. WHERE AM I? ]  [ 7. HERE'S WHAT I SEE ]
 (Voice speech:  ("Where would you like to go?")(RTU location card,  (RTU Campus photo,
 "Take me to RTU",       │                      Orientation East,     Sidewalk clear,
 "Where am I?")    Select RTU Campus            "Repeat location")    Bicycle rack,
     │                   │                           │                People, Sunny,
     │                   ▼                           │                "Repeat" audio)
     │          [ 4. ROUTE PREVIEW ] ◄───────────────┘
     │          (Daugava map canvas,
     │           Vanšu tilts, 2.4 km)
     │                   │
     │            Start navigation
     │                   │
     └───────────────────┼───────────────────────────────────────────────┐
                         │                                               │
                         ▼                                               ▼
              [ 5. ACTIVE NAVIGATION ]                        [ 8. OBSTACLE AHEAD ]
           (Live distance countdown 120m,                   (Red alert: Construction barrier,
            Turn right on Ķīpsalas iela,                     2m ahead on right, AR red path,
            Haptic directional feedback)                     "Repeat", "I Understand")
                         │                                               │
                         ├───────────────────────────────────────────────┘
                         │
                         ▼
             [ 9. APPROACHING CROSSWALK ]
           (Warm amber notice: Listen for traffic,
            Zebra crossing & green pedestrian signal,
            Animated audio waveform, Automatic silence,
            "I will be quiet while you cross")
```

### Screen Inventory:
1. **Screen 1 — Home**: 3D glowing status orb, *"How can I help you today?"*, and accessible action cards.
2. **Screen 2 — Voice Listening**: Audio-reactive ripple rings, real speech-to-text, prompt pills, and cancel button.
3. **Screen 3 — Destination Search**: Live search input, category filters (Campus, Library, Transit, Cafeteria), and recent places.
4. **Screen 4 — Route Preview**: Destination overview (2.4 km, 28 min, 8 waypoints), Daugava River/Vanšu tilts vector map, and *"Start navigation"*.
5. **Screen 5 — Active Navigation**: Step indicator, distance countdown (160 m $\to$ 0 m), maneuver icon, and safety event test buttons.
6. **Screen 6 — Where am I?**: Current street, compass heading (84° E), RTU landmark photo card, and *"Repeat location"*.
7. **Screen 7 — Describe What's Around Me**: Camera scene photo, structured 5-item perception list, and audio replay button.
8. **Screen 8 — Obstacle Ahead (Hazard Detection)**: Urgent warning banner, camera view with dynamic LiDAR depth overlay canvas, floating obstacle card, and *"I Understand"* button.
9. **Screen 9 — Approaching Crosswalk (Quiet Mode)**: Amber safety banner, zebra crossing visual, animated audio waveform, and *"Crosswalk Completed — Resume Route"*.

---

## ♿ Accessibility Engineering (WCAG 2.2 AAA)

Blind AI is engineered from the ground up to meet **WCAG 2.2 Level AAA** compliance:

- **Visible Focus Indicators**: High-contrast, 3px focus rings with 2px offset on all interactive controls.
- **WCAG Live Regions**: Persistent `aria-live="polite"` and `aria-live="assertive"` announcers for screen readers (VoiceOver, NVDA, TalkBack).
- **Logical Tab Order & Bypass Blocks**: Skip navigation link (`Skip to application screen`) and semantic landmarks (`<main>`, `<header>`, `<nav>`, `<aside>`).
- **Touch Targets**: Minimum target size of **48 $\times$ 48 px** with generous touch padding.
- **Color Independence**: Critical hazard states do not rely solely on color; they combine icons, clear text banners, haptic pulses, and speech announcements.
- **Contrast Ratios**: Body text achieves $> 7:1$ contrast against light backgrounds; badge highlights achieve $> 4.5:1$.

---

## 🛠️ Backend API Reference

Base URL: `http://localhost:3000/api/v1`

| Method | Endpoint | Description | Sample Request / Response |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Health check & active AI provider status | `{"status": "ok", "service": "Blind AI Backend", "aiProvider": "gemini"}` |
| `POST` | `/api/v1/voice/intent` | Natural language intent parsing | Body: `{"transcript": "Take me to the library"}`<br>Returns: `{"intent": "start_navigation", "destination": {...}}` |
| `POST` | `/api/v1/environment/describe` | Multimodal visual scene description | Body: `{"image_base64": "..."}`<br>Returns structured semantic objects list |
| `POST` | `/api/v1/environment/where-am-i` | Spatial GPS + landmark context | Body: `{"latitude": 56.95, "longitude": 24.08}`<br>Returns street name, campus name, and orientation |
| `GET` | `/api/v1/routes` | Predefined campus & city routes | Returns list of available accessible paths |
| `POST` | `/api/v1/navigation/sessions/:id/events` | Telemetry & obstacle encounter logging | Body: `{"obstacle_type": "chair", "distance_meters": 2.0, "action_taken": "avoid_left"}` |

---

## 📂 Project Directory Layout

```
BlindAI/
├── .gitignore                        # Excludes .env, node_modules, build, .cache
├── vercel.json                       # Vercel serverless SPA & API rewrite rules
├── package.json                      # Workspace configuration
├── index.html                        # Pure mobile application web interface
├── preview.html                      # Interactive 9-screen live logic simulator
├── scripts/
│   └── make_preview.py               # Generator script for preview and simulator files
├── backend/
│   ├── .env                          # Holds GEMINI_API_KEY (git-ignored)
│   ├── .env.example                  # Environment configuration template
│   ├── package.json                  # Node.js backend dependencies
│   ├── public/                       # Static public deployment assets
│   └── src/
│       ├── server.js                 # HTTP server with auto EADDRINUSE port fallback
│       ├── config/
│       │   └── env.js                # Environment validator & loader
│       ├── services/
│       │   ├── ai/
│       │   │   ├── aiProviderInterface.js # Modular AI abstraction
│       │   │   ├── geminiProvider.js     # Google Gemini API client
│       │   │   └── aiService.js          # Provider registry & manager
│       │   └── db/
│       │       └── supabaseClient.js     # Database persistence service
│       └── controllers/
│           ├── environmentController.js # Scene perception & location context
│           ├── voiceController.js       # Voice intent understanding
│           └── routesController.js      # Navigation routing & waypoints
└── ios/
    ├── BlindAI.xcodeproj/           # Xcode project with all 48 files registered
    ├── BlindAI/
    │   ├── App/
    │   │   ├── BlindAIApp.swift      # Main application lifecycle
    │   │   └── ContentView.swift     # 9-route SwiftUI router
    │   ├── Views/                    # 9 Native SwiftUI Screen Views
    │   │   ├── HomeView.swift
    │   │   ├── ListeningView.swift
    │   │   ├── DestinationSearchView.swift
    │   │   ├── RoutePreviewView.swift
    │   │   ├── ActiveNavigationView.swift
    │   │   ├── WhereAmIView.swift
    │   │   ├── DescribeAroundView.swift    # Screen 7 (Here's what I see)
    │   │   ├── ObstacleAlertView.swift     # Screen 8 (Obstacle ahead)
    │   │   └── CrosswalkSafetyView.swift   # Screen 9 (Approaching crosswalk)
    │   ├── ViewModels/               # 9 ObservableObject ViewModels
    │   ├── Components/               # Reusable Accessible UI Components
    │   ├── Services/
    │   │   ├── ARKitLiDARScannerService.swift # Apple ARKit sceneDepth LiDAR Scanner
    │   │   ├── VisionObjectDetector.swift     # Apple Vision Object Detection
    │   │   ├── ObstacleDangerSystem.swift     # Danger Evaluation & Speech Preemption
    │   │   ├── NavigationService.swift        # Turn-by-turn guidance
    │   │   ├── SpeechService.swift            # AVSpeechSynthesizer audio dispatch
    │   │   └── HapticsService.swift           # CoreHaptics engine
    │   ├── Models/                   # Data structures & AppRoute enum
    │   └── DesignSystem/             # Typography, colors, and layout spacing
    └── Logic/
        ├── GroundHazardDetector.swift # Elevation delta analysis
        └── Tests/
            └── LogicTests.swift      # Unit test suites
```

---

## 🚀 Local Development & Quick Start

### 1. Start the Backend Server
```bash
cd backend
npm start
```
- Listens on `http://localhost:3000`.
- Includes automatic port collision detection (switches to `3001` if `3000` is occupied).
- Loads `GEMINI_API_KEY` from `backend/.env`.

### 2. View the Web App in Your Browser
Navigate to:
```
http://localhost:3000
```
- **Pure Mobile View** (Default): Clean, edge-to-edge mobile screen with zero simulator clutter.
- **Interactive Simulator Tools**: Tap the **`📱 Mobile View / 🛠️ Tools: ON`** switcher in the bottom-right corner to open the LiDAR distance slider, scenario test buttons, and screen jump dropdown.
- **All Screens Gallery**: Access side-by-side mode via `http://localhost:3000/preview`.

---

## 📱 Running the Native iOS Swift App

The native iOS app is built in pure **Swift & SwiftUI** utilizing **ARKit** and **Vision**.

### Requirements
- **macOS** with **Xcode 15+** or **Xcode 16** (Download free from the Mac App Store).
- **Target OS**: iOS 17.0+.
- **Hardware (Optional for LiDAR)**: iPhone 12 Pro, 13 Pro, 14 Pro, 15 Pro, 16 Pro, or iPad Pro.
  *(Non-Pro iPhones and the Xcode Simulator automatically use the built-in sensor fallback simulator).*

### Steps to Run
1. Open the project in Xcode:
   ```bash
   open ios/BlindAI.xcodeproj
   ```
2. In the Xcode toolbar, select your device or an iOS Simulator (e.g., iPhone 15 Pro).
3. Press **⌘R** (or click **Product $\to$ Run**).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
