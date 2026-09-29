# Blind AI — System Architecture & 9-Screen Workflow

A retrofit assistive smart-navigation application engineered specifically for blind and visually impaired pedestrians.

---

## 🔒 Security & AI Configuration Architecture

Per strict security and architectural requirements:
1. **Zero Client-Side Keys**: The Gemini API key and Supabase keys are **NEVER** hardcoded in the Swift iOS client, HTML, or committed to GitHub.
2. **Backend Environment Variables**: Secrets are stored exclusively as `GEMINI_API_KEY` and `SUPABASE_KEY` inside `backend/.env`.
3. **Git-Ignored Secrets**: `backend/.env` and all `.env*` files are strictly excluded via `.gitignore`.
4. **Backend Proxy Pattern**: The iOS app communicates strictly with our backend API server (`/api/v1`), which manages authentication, queries Supabase, and communicates securely with Google Gemini.
5. **Modular Services**: The backend implements an `AIProviderInterface` pattern for Gemini and a lightweight `SupabaseClient` for persisting navigation sessions, obstacle logs, and user settings.

```
┌─────────────────────────────────┐
│       iOS App (SwiftUI)         │
│     (BlindAIBackendClient)      │
└────────────────┬────────────────┘
                 │ HTTP (localhost:3000/api/v1)
                 │ [No API Keys in App]
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
                 │   GeminiProvider
                 │
                 ▼ HTTPS
┌─────────────────────────────────┐
│     Google Gemini API (Cloud)   │
└─────────────────────────────────┘
```

---

## 📱 The Complete 9-Screen Architecture & Workflow

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

### Screen Details:
1. **Screen 1 — Home**: Glowing 3D status orb, prompt *"How can I help you today?"*, and action cards.
2. **Screen 2 — Voice Listening**: Concentric animated audio-reactive ripple rings, real speech-to-text, prompt pills, and stop button.
3. **Screen 3 — Destination Search**: *"Where would you like to go?"*, live search bar for Riga, recent places (**RTU**, **Ķīpsala Campus**, **Central Station**), category filters, and *"Speak destination"*.
4. **Screen 4 — Route Preview**: Destination overview (2.4 km, 28 min, 8 waypoints), interactive **Daugava River & Vanšu tilts** vector map, turn steps list, and *"Start navigation"*.
5. **Screen 5 — Active Navigation**: Live dynamic meter countdown (120m ➔ 0m), turn instruction card (*"Turn right on Ķīpsalas iela"*), directional haptics, milestone audio cues, and *"Stop route"*.
6. **Screen 6 — Where am I?**: Glowing orb, precise location text (*"You are near Riga Technical University, Ķīpsala Campus"*), compass heading (84° E), **RTU landmark photo card**, and *"Repeat location"* action.
7. **Screen 7 — Describe What's Around Me ("Here’s what I see:")**: Compact glowing orb, heading *"Here’s what I see:"*, RTU campus camera preview photo, structured list card (Sidewalk clear, RTU main entrance on left, Bicycle rack 3m ahead, People walking nearby, Sunny and bright), and *"Repeat"* pill button.
8. **Screen 8 — Obstacle Ahead (Hazard Detection)**: Light pinkish-red warning banner (*"Obstacle ahead: Two meters ahead, construction barrier on right"*), camera view with red AR path & red glowing wireframe barrier cage, floating construction barrier info card, *"Repeat"* button, and dark *"✕ I Understand"* acknowledgment button.
9. **Screen 9 — Approaching Crosswalk (Quiet Mode)**: Warm amber banner (*"Approaching crosswalk. Listen for traffic."*), camera view showing zebra crossing and green pedestrian walking signal, floating card with animated amber audio waveform visualizer (*"I will be quiet while you cross."*), and resume route trigger.

---

## 📂 Project Directory Structure

```
BlindAI/
├── .gitignore                        # Blocks .env, *.env, node_modules, build/
├── backend/                          # Backend API & AI Provider
│   ├── .env                          # Holds GEMINI_API_KEY (git-ignored)
│   ├── .env.example                  # Template configuration
│   ├── .gitignore                    # Backend ignore rules
│   ├── package.json
│   └── src/
│       ├── server.js                 # HTTP API server on port 3000
│       ├── config/
│       │   └── env.js                # Environment validator
│       ├── services/ai/
│       │   ├── aiProviderInterface.js # Modular AI interface
│       │   ├── geminiProvider.js     # Google Gemini API integration
│       │   └── aiService.js          # AI Provider registry & manager
│       ├── controllers/
│       │   ├── environmentController.js # /describe and /where-am-i
│       │   ├── voiceController.js       # /voice/intent
│       │   └── routesController.js      # /routes and /routes/plan
├── ios/
│   ├── BlindAI.xcodeproj/           # Xcode project with 47 files registered
│   ├── BlindAI/
│   │   ├── App/                      # BlindAIApp & ContentView (9 routes)
│   │   ├── Views/                    # 9 SwiftUI Screen Views
│   │   │   ├── HomeView.swift
│   │   │   ├── ListeningView.swift
│   │   │   ├── DestinationSearchView.swift
│   │   │   ├── RoutePreviewView.swift
│   │   │   ├── ActiveNavigationView.swift
│   │   │   ├── WhereAmIView.swift
│   │   │   ├── DescribeAroundView.swift    # Screen 7 (Here's what I see)
│   │   │   ├── ObstacleAlertView.swift     # Screen 8 (Obstacle ahead)
│   │   │   └── CrosswalkSafetyView.swift   # Screen 9 (Approaching crosswalk)
│   │   ├── ViewModels/               # 9 ViewModels
│   │   ├── Components/               # Reusable accessible components
│   │   ├── Services/                 # BlindAIBackendClient, Speech, Nav, Haptics
│   │   ├── Models/                   # Data entities & AppRoute enum
│   │   ├── Resources/
│   │   │   └── Assets.xcassets/      # App assets + camera scene image sets
│   │   └── DesignSystem/             # Colors, Typography, Spacing
├── preview.html                      # Interactive 9-screen live logic simulator
└── README.md
```

---

## 🚀 Running the App & Simulator

### 1. Interactive Web Simulator
Open `preview.html` in your browser:
```bash
open /Users/ranjeet/.gemini/antigravity/scratch/BlindAI/preview.html
```
- Test all 9 screens interactively on a simulated iPhone 15 Pro display.
- Click **"All 9 Screens Side-by-Side"** to view the entire app gallery simultaneously.
- Jump directly to any screen with the **"Jump to"** selector.
- Use speech recognition, audio playback, auto-walk simulation, and obstacle/crosswalk triggers.

### 2. Backend Server
```bash
cd backend
npm start
```
Starts the API server on `http://localhost:3000/api/v1`.
Gemini API calls are executed through the backend using `GEMINI_API_KEY`.

### 3. iOS App in Xcode
Open `ios/BlindAI.xcodeproj` in Xcode to build and run on iOS Simulator or physical iPhone.
