import os
import base64

def get_b64(path):
    with open(path, 'rb') as f:
        return 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')

img_campus = get_b64('docs/scene_rtu_campus.jpg')
img_obstacle = get_b64('docs/scene_obstacle_barrier.jpg')
img_crosswalk = get_b64('docs/scene_crosswalk_signal.jpg')

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blind AI — Accessible Assistive Navigation System</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* Accessible Focus Ring System (WCAG 2.2 Level AA - SC 2.4.7 Focus Visible, SC 2.4.11 Focus Not Obscured) */
    :focus-visible {{
      outline: 2px solid #D97706 !important;
      outline-offset: 2px !important;
      box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.35) !important;
    }}
    button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible, [role="button"]:focus-visible {{
      outline: 2px solid #D97706 !important;
      outline-offset: 2px !important;
      box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.4) !important;
    }}

    /* Screen Reader Only Utility */
    .sr-only {{
      position: absolute !important;
      width: 1px !important;
      height: 1px !important;
      padding: 0 !important;
      margin: -1px !important;
      overflow: hidden !important;
      clip: rect(0, 0, 0, 0) !important;
      white-space: nowrap !important;
      border-width: 0 !important;
    }}
    .sr-only.focus\\:not-sr-only:focus,
    .sr-only.focus\\:not-sr-only:active {{
      position: fixed !important;
      width: auto !important;
      height: auto !important;
      padding: 0.75rem 1.25rem !important;
      margin: 0 !important;
      overflow: visible !important;
      clip: auto !important;
      white-space: normal !important;
      z-index: 9999 !important;
    }}

    /* Animations & Reduced Motion (WCAG 2.2 SC 2.3.3) */
    @keyframes ripple-pulse {{
      0% {{ transform: scale(0.96); opacity: 0.7; }}
      50% {{ transform: scale(1.06); opacity: 0.3; }}
      100% {{ transform: scale(0.96); opacity: 0.7; }}
    }}
    .ripple-ring-1 {{ animation: ripple-pulse 2.2s infinite ease-in-out; }}
    .ripple-ring-2 {{ animation: ripple-pulse 2.2s infinite ease-in-out 0.35s; }}
    .ripple-ring-3 {{ animation: ripple-pulse 2.2s infinite ease-in-out 0.7s; }}
    
    @keyframes wave-bounce {{
      0%, 100% {{ transform: scaleY(0.4); }}
      50% {{ transform: scaleY(1.0); }}
    }}
    .wave-bar {{
      transform-origin: center;
      animation: wave-bounce 1.2s ease-in-out infinite;
    }}
    .wave-1 {{ animation-delay: 0.1s; }}
    .wave-2 {{ animation-delay: 0.2s; }}
    .wave-3 {{ animation-delay: 0.35s; }}
    .wave-4 {{ animation-delay: 0.5s; }}
    .wave-5 {{ animation-delay: 0.65s; }}
    .wave-6 {{ animation-delay: 0.5s; }}
    .wave-7 {{ animation-delay: 0.35s; }}
    .wave-8 {{ animation-delay: 0.2s; }}
    .wave-9 {{ animation-delay: 0.1s; }}

    @media (prefers-reduced-motion: reduce) {{
      .ripple-ring-1, .ripple-ring-2, .ripple-ring-3, .wave-bar {{
        animation: none !important;
      }}
      .orb-glow {{
        filter: none !important;
        transition: none !important;
      }}
    }}
    
    .orb-3d {{
      background: radial-gradient(circle at 40% 34%, #FFE48F 0%, #FFB636 28%, #FF6000 65%, #D43900 100%);
      box-shadow: 0 12px 28px rgba(255, 100, 0, 0.38), inset 0 2px 4px rgba(255, 255, 255, 0.7);
      transition: transform 0.15s ease-out;
    }}
    .orb-glow {{
      background: radial-gradient(circle, rgba(255, 140, 0, 0.45) 0%, rgba(255, 170, 40, 0.22) 50%, rgba(255, 255, 255, 0) 75%);
      filter: blur(18px);
      transition: opacity 0.2s ease, transform 0.2s ease;
    }}
    
    .iphone-frame {{
      width: 380px;
      height: 780px;
      border-radius: 50px;
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.25), 0 0 0 10px #1E1E1E, 0 0 0 12px #2A2A2A;
      overflow: hidden;
      position: relative;
      background-color: #F8F8F9;
      user-select: none;
      flex-shrink: 0;
    }}
    
    .no-scrollbar::-webkit-scrollbar {{ display: none; }}
    .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
  </style>
</head>
<body class="bg-slate-100 text-slate-900 font-sans antialiased min-h-screen p-3 md:p-6">

  <!-- Skip Navigation Link (WCAG 2.2 SC 2.4.1 Bypass Blocks) -->
  <a href="#screen-viewport" class="sr-only focus:not-sr-only bg-amber-600 text-white font-bold rounded-xl shadow-xl top-3 left-3 focus:outline-none focus:ring-4 focus:ring-amber-300">
    Skip to application screen
  </a>

  <!-- Persistent ARIA Live Region for Screen Readers -->
  <div id="a11y-announcer" class="sr-only" aria-live="polite" aria-atomic="true"></div>

  <!-- Top Toolbar / Header Landmark -->
  <header class="max-w-7xl mx-auto mb-5 bg-white p-4 rounded-2xl shadow-sm border border-slate-200 flex flex-wrap items-center justify-between gap-4" role="banner">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-full orb-3d flex items-center justify-center text-white font-bold text-xs shadow-md" aria-hidden="true">
        AI
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-lg font-bold text-slate-900 leading-tight">Blind AI — Complete 9-Screen Architecture</h1>
          <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-100 text-emerald-800">
            All 9 Screens Active
          </span>
        </div>
        <p class="text-xs text-slate-600 font-medium">Home • Voice • Destination • Route • Active Nav • Where Am I • Describe Around • Obstacle Alert • Crosswalk Quiet</p>
      </div>
    </div>
    
    <!-- Controls Landmark -->
    <nav class="flex flex-wrap items-center gap-2" aria-label="Simulator Controls">
      <!-- Direct Screen Quick Selector -->
      <div class="flex items-center gap-1.5 bg-slate-100 px-3 py-1 rounded-xl text-xs">
        <label for="screen-selector" class="font-semibold text-slate-700">Jump to:</label>
        <select id="screen-selector" onchange="jumpToScreen(this.value)" aria-label="Jump directly to screen" class="bg-white border border-slate-200 rounded-lg px-2 py-1 font-semibold text-slate-700 text-xs focus:ring-2 focus:ring-amber-500">
          <option value="home">1. Home</option>
          <option value="listening">2. Voice Listening</option>
          <option value="destinationSearch">3. Destination Search</option>
          <option value="routePreview">4. Route Preview (RTU)</option>
          <option value="activeNavigation">5. Active Navigation</option>
          <option value="whereAmI">6. Where am I?</option>
          <option value="describeAround">7. Describe what's around me</option>
          <option value="obstacleAlert">8. Obstacle ahead (Hazard)</option>
          <option value="crosswalkSafety">9. Approaching crosswalk (Quiet)</option>
        </select>
      </div>

      <!-- Mode Toggle (Accessible Tablist) -->
      <div role="tablist" aria-label="Display View Mode" class="inline-flex bg-slate-100 p-1 rounded-xl text-xs font-semibold text-slate-600">
        <button id="btn-tab-interactive" role="tab" aria-selected="true" aria-controls="view-interactive" onclick="switchSimulatorMode('interactive')" class="px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-sm transition">
          Interactive Device
        </button>
        <button id="btn-tab-sidebyside" role="tab" aria-selected="false" aria-controls="view-sidebyside" onclick="switchSimulatorMode('sidebyside')" class="px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition">
          All 9 Screens Side-by-Side
        </button>
      </div>
      
      <!-- Audio Toggle -->
      <button onclick="toggleAudioSpeech()" id="audio-toggle-btn" role="switch" aria-checked="true" aria-label="Voice guidance enabled. Tap to mute voice." class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200 text-xs font-medium text-slate-700 hover:bg-slate-50 transition">
        <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-amber-500" fill="currentColor" viewBox="0 0 24 24">
          <path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.5A2.25 2.25 0 0 0 2.25 9.75v4.5A2.25 2.25 0 0 0 4.5 16.5h1.94l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06ZM18.584 5.106a.75.75 0 0 1 1.06 0c3.808 3.807 3.808 9.98 0 13.788a.75.75 0 0 1-1.06-1.06 8.25 8.25 0 0 0 0-11.668.75.75 0 0 1 0-1.06Z" />
        </svg>
        <span id="speech-status-label">Voice: On</span>
      </button>

      <!-- Auto Walk Toggle -->
      <button onclick="toggleWalkSimulation()" id="walk-sim-btn" role="switch" aria-checked="true" aria-label="Auto-walk simulation active. Tap to pause." class="flex items-center gap-1 px-3 py-1.5 rounded-xl bg-amber-500 text-white text-xs font-semibold hover:bg-amber-600 transition shadow-sm">
        <span id="walk-sim-label">Auto-Walk: ON</span>
      </button>
    </nav>
  </header>

  <!-- Main Landmark -->
  <main id="main-content" class="max-w-7xl mx-auto flex items-center justify-center">

    <!-- VIEW 1: INTERACTIVE SINGLE PHONE SIMULATOR -->
    <div id="view-interactive" role="tabpanel" aria-labelledby="btn-tab-interactive" class="flex flex-col items-center">
      <div class="flex items-center gap-2 mb-2 text-xs text-slate-600" aria-live="polite">
        <span class="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse" aria-hidden="true"></span>
        <span id="instruction-tip">Tap <strong>Describe what's around me</strong> or <strong>Start navigation</strong></span>
      </div>

      <div class="iphone-frame flex flex-col justify-between" id="phone-container">
        <!-- Status Bar (Decorative Simulated Device Chrome) -->
        <div class="pt-3 px-7 flex justify-between items-center text-xs font-semibold text-black z-30" aria-hidden="true">
          <span>9:41</span>
          <!-- Dynamic Island -->
          <div class="w-24 h-6 bg-black rounded-full flex items-center justify-end pr-2">
            <div id="island-mic-dot" class="w-2.5 h-2.5 rounded-full bg-[#151515] border border-neutral-700 transition-colors"></div>
          </div>
          <div class="flex items-center space-x-1.5">
            <svg aria-hidden="true" class="w-3.5 h-3.5 fill-black" viewBox="0 0 24 24"><path d="M12 3c-4.97 0-9 4.03-9 9 0 2.12.74 4.07 1.97 5.61L12 22l7.03-4.39C20.26 16.07 21 14.12 21 12c0-4.97-4.03-9-9-9z"/></svg>
            <svg aria-hidden="true" class="w-3.5 h-3.5 fill-black" viewBox="0 0 24 24"><path d="M12 4C7.31 4 3.07 5.9 0 8.98L12 21 24 8.98A16.88 16.88 0 0012 4z"/></svg>
            <div class="w-5 h-2.5 border border-black rounded-sm p-0.5 flex items-center">
              <div class="w-full h-full bg-black rounded-2xs"></div>
            </div>
          </div>
        </div>

        <!-- Dynamic Screen Viewport -->
        <section id="screen-viewport" role="region" aria-label="Blind AI Mobile Screen" class="flex-1 flex flex-col overflow-y-auto no-scrollbar relative" tabindex="-1">
          
          <!-- ==================== SCREEN 1: HOME ==================== -->
          <div id="screen-home" role="region" aria-label="Screen 1: Home" class="flex-1 flex flex-col justify-between p-5 pb-6">
            <div class="flex justify-between items-center pt-2 px-1">
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition active:scale-95">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <div class="flex flex-col items-center justify-center my-auto py-2">
              <button type="button" onclick="navigateTo('listening')" aria-label="Activate voice listening assistant" class="relative flex items-center justify-center w-36 h-36 mb-4 cursor-pointer rounded-full focus:outline-none">
                <div class="absolute w-44 h-44 rounded-full orb-glow ripple-ring-1 pointer-events-none" aria-hidden="true"></div>
                <div class="absolute w-36 h-36 rounded-full orb-glow ripple-ring-2 pointer-events-none" aria-hidden="true"></div>
                <div class="w-28 h-28 rounded-full orb-3d relative z-10 flex items-center justify-center" aria-hidden="true">
                  <div class="w-10 h-10 rounded-full bg-white/20 blur-[2px]"></div>
                </div>
              </button>
              <h2 class="text-2xl font-bold text-center text-slate-900 tracking-tight leading-snug px-4">
                How can I help you today?
              </h2>
            </div>

            <div class="flex flex-col space-y-3">
              <!-- Card 1: Start navigation -->
              <button onclick="navigateTo('destinationSearch')" aria-label="Start navigation: Get directions to a place" class="w-full bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-slate-300 transition active:scale-[0.99]">
                <div class="flex items-center space-x-3.5">
                  <div class="w-11 h-11 rounded-xl bg-orange-50 border border-orange-100 flex items-center justify-center text-orange-600 flex-shrink-0" aria-hidden="true">
                    <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" /></svg>
                  </div>
                  <div>
                    <h3 class="font-bold text-slate-900 text-base leading-tight">Start navigation</h3>
                    <p class="text-xs text-slate-600 mt-0.5">Get directions to a place</p>
                  </div>
                </div>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>

              <!-- Card 2: Describe what's around me -->
              <button onclick="navigateTo('describeAround')" aria-label="Describe what's around me: Identify objects and obstacles" class="w-full bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-slate-300 transition active:scale-[0.99]">
                <div class="flex items-center space-x-3.5">
                  <div class="w-11 h-11 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 flex-shrink-0" aria-hidden="true">
                    <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                  </div>
                  <div>
                    <h3 class="font-bold text-slate-900 text-base leading-tight">Describe what's around me</h3>
                    <p class="text-xs text-slate-600 mt-0.5">Identify objects and obstacles</p>
                  </div>
                </div>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>

              <!-- Card 3: Where am I? -->
              <button onclick="navigateTo('whereAmI')" aria-label="Where am I?: Current location and surroundings" class="w-full bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-slate-300 transition active:scale-[0.99]">
                <div class="flex items-center space-x-3.5">
                  <div class="w-11 h-11 rounded-xl bg-purple-50 border border-purple-100 flex items-center justify-center text-purple-600 flex-shrink-0" aria-hidden="true">
                    <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  </div>
                  <div>
                    <h3 class="font-bold text-slate-900 text-base leading-tight">Where am I?</h3>
                    <p class="text-xs text-slate-600 mt-0.5">Current location and surroundings</p>
                  </div>
                </div>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>
            </div>

            <!-- Bottom Mic Button -->
            <div class="flex justify-center mt-3">
              <button onclick="navigateTo('listening')" aria-label="Start voice listening assistant" class="w-14 h-14 rounded-full bg-black text-white flex items-center justify-center shadow-lg hover:bg-neutral-800 transition active:scale-95">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 2: VOICE LISTENING ==================== -->
          <div id="screen-listening" role="region" aria-label="Screen 2: Voice Listening" class="flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <div class="flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('home')" aria-label="Back to home screen" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <div class="w-10 h-10" aria-hidden="true"></div>
            </div>

            <div class="flex flex-col items-center justify-center my-auto">
              <div class="relative flex items-center justify-center w-48 h-48 mb-6" aria-hidden="true">
                <div class="absolute w-56 h-56 rounded-full orb-glow ripple-ring-1"></div>
                <div class="absolute w-44 h-44 rounded-full orb-glow ripple-ring-2"></div>
                <div class="w-32 h-32 rounded-full orb-3d relative z-10 flex items-center justify-center">
                  <div class="w-12 h-12 rounded-full bg-white/20 blur-[2px]"></div>
                </div>
              </div>
              <h2 id="listening-title" class="text-2xl font-bold text-center text-slate-900 tracking-tight">
                I'm listening...
              </h2>
              <p id="live-transcript" aria-live="polite" class="text-sm text-slate-600 text-center mt-2 px-6 italic min-h-[3rem]">
                “Take me to Riga Technical University”
              </p>
            </div>

            <div class="flex flex-col gap-3">
              <div class="flex justify-center gap-2" role="group" aria-label="Suggested voice phrases">
                <button onclick="handleVoiceInput('Take me to RTU')" aria-label="Simulate voice input: Take me to RTU" class="px-3 py-1.5 rounded-full bg-white border border-slate-200 text-xs font-medium text-slate-700 shadow-sm hover:bg-slate-50">
                  Say: "Take me to RTU"
                </button>
                <button onclick="handleVoiceInput('Describe what is around me')" aria-label="Simulate voice input: Describe around me" class="px-3 py-1.5 rounded-full bg-white border border-slate-200 text-xs font-medium text-slate-700 shadow-sm hover:bg-slate-50">
                  Say: "Describe around me"
                </button>
              </div>

              <div class="flex justify-center">
                <button onclick="navigateTo('home')" aria-label="Cancel voice listening and return home" class="w-14 h-14 rounded-full bg-red-500 text-white flex items-center justify-center shadow-lg hover:bg-red-600 transition active:scale-95">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                </button>
              </div>
            </div>
          </div>

          <!-- ==================== SCREEN 3: DESTINATION SEARCH ==================== -->
          <div id="screen-destinationSearch" role="region" aria-label="Screen 3: Destination Search" class="flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <div class="flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('home')" aria-label="Back to home screen" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <div class="flex-1 flex flex-col pt-3 overflow-y-auto no-scrollbar">
              <div class="flex flex-col items-center mb-3">
                <div class="w-12 h-12 rounded-full orb-3d mb-2" aria-hidden="true"></div>
                <h2 class="text-xl font-bold text-slate-900">Where would you like to go?</h2>
              </div>

              <!-- Accessible Search Bar -->
              <div class="relative mb-3">
                <label for="destination-search-input" class="sr-only">Search destination or speak</label>
                <input type="text" id="destination-search-input" oninput="filterDestinations(this.value)" placeholder="Search destination or speak..." aria-label="Search destination or speak" class="w-full bg-white border border-slate-200 rounded-2xl py-3 pl-11 pr-11 text-sm font-medium text-slate-800 placeholder-slate-500 shadow-sm focus:border-amber-500 transition">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-500 absolute left-3.5 top-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                <button onclick="navigateTo('listening')" aria-label="Search destination using voice" class="absolute right-3 top-3 text-orange-500 hover:text-orange-600">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
                </button>
              </div>

              <!-- Category Pills -->
              <div role="group" aria-label="Destination categories" class="flex items-center gap-2 mb-4 overflow-x-auto no-scrollbar py-1">
                <button onclick="selectCategory('RTU')" class="px-3 py-1.5 bg-orange-100 text-orange-800 rounded-full text-xs font-semibold whitespace-nowrap">Campus (RTU)</button>
                <button onclick="selectCategory('Library')" class="px-3 py-1.5 bg-slate-100 text-slate-700 rounded-full text-xs font-semibold whitespace-nowrap">Library</button>
                <button onclick="selectCategory('Transit')" class="px-3 py-1.5 bg-slate-100 text-slate-700 rounded-full text-xs font-semibold whitespace-nowrap">Transit Stop</button>
                <button onclick="selectCategory('Cafeteria')" class="px-3 py-1.5 bg-slate-100 text-slate-700 rounded-full text-xs font-semibold whitespace-nowrap">Cafeteria</button>
              </div>

              <!-- Recent Destinations List -->
              <h3 class="text-xs font-bold text-slate-600 uppercase tracking-wider mb-2 px-1">Recent Places</h3>
              <div id="recent-places-list" role="list" aria-label="Recent destinations" class="flex flex-col space-y-2.5 pb-4">
                <button onclick="selectDestination('Riga Technical University (RTU)', 'Ķīpsala Campus, Paula Valdena iela 1')" aria-label="Select destination: Riga Technical University (RTU), Ķīpsala Campus, 2.4 kilometers, 28 minutes" class="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-amber-400 transition">
                  <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-orange-50 text-orange-600 flex items-center justify-center font-bold text-sm" aria-hidden="true">RTU</div>
                    <div>
                      <h4 class="font-bold text-slate-900 text-sm">Riga Technical University (RTU)</h4>
                      <p class="text-xs text-slate-600">Ķīpsala Campus • 2.4 km</p>
                    </div>
                  </div>
                  <span class="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-1 rounded-lg">28 min</span>
                </button>

                <button onclick="selectDestination('RTU Student Hostel', 'Āzenes iela 22, Ķīpsala')" aria-label="Select destination: RTU Student Hostel, Āzenes iela 22, 1.1 kilometers, 14 minutes" class="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-amber-400 transition">
                  <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-sm" aria-hidden="true">SH</div>
                    <div>
                      <h4 class="font-bold text-slate-900 text-sm">RTU Student Hostel</h4>
                      <p class="text-xs text-slate-600">Āzenes iela 22 • 1.1 km</p>
                    </div>
                  </div>
                  <span class="text-xs font-bold text-slate-700 bg-slate-100 px-2 py-1 rounded-lg">14 min</span>
                </button>

                <button onclick="selectDestination('Swedbank Central Building', 'Balasta dambis 15, Riga')" aria-label="Select destination: Swedbank Central Building, Balasta dambis 15, 1.8 kilometers, 21 minutes" class="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-amber-400 transition">
                  <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center font-bold text-sm" aria-hidden="true">SB</div>
                    <div>
                      <h4 class="font-bold text-slate-900 text-sm">Swedbank Central Building</h4>
                      <p class="text-xs text-slate-600">Balasta dambis 15 • 1.8 km</p>
                    </div>
                  </div>
                  <span class="text-xs font-bold text-slate-700 bg-slate-100 px-2 py-1 rounded-lg">21 min</span>
                </button>
              </div>
            </div>

            <!-- Bottom Mic Button -->
            <div class="flex justify-center mt-2">
              <button onclick="navigateTo('listening')" aria-label="Start voice listening assistant" class="w-14 h-14 rounded-full bg-black text-white flex items-center justify-center shadow-lg hover:bg-neutral-800 transition active:scale-95">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 4: ROUTE PREVIEW ==================== -->
          <div id="screen-routePreview" role="region" aria-label="Screen 4: Route Preview" class="flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <div class="flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('destinationSearch')" aria-label="Back to destination search" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <!-- Route Map Graphic (SVG) with ARIA description -->
            <div class="flex-1 flex flex-col justify-center my-2">
              <h2 class="sr-only">Route Map & Details</h2>
              <div class="w-full h-44 bg-slate-200 rounded-3xl relative overflow-hidden shadow-inner border border-slate-300">
                <svg role="img" aria-label="Walking route map: 2.4 kilometers across Vanšu tilts to Riga Technical University" class="w-full h-full" viewBox="0 0 320 180" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <title>Walking Route Map to RTU</title>
                  <rect width="320" height="180" fill="#E5E7EB"/>
                  <path d="M80 0 C 95 60, 110 120, 130 180 L 195 180 C 180 120, 160 60, 145 0 Z" fill="#93C5FD" opacity="0.75"/>
                  <text x="115" y="100" fill="#1D4ED8" font-size="10" font-weight="bold" transform="rotate(70, 115, 100)">Daugava River</text>
                  <path d="M30 70 L 290 85" stroke="#9CA3AF" stroke-width="6" stroke-linecap="round"/>
                  <text x="210" y="80" fill="#4B5563" font-size="9" font-weight="bold">Vanšu tilts</text>
                  <path d="M50 145 L 85 100 L 140 100 L 190 75 L 260 55" stroke="#F97316" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6 4"/>
                  <circle cx="50" cy="145" r="7" fill="#2563EB" stroke="white" stroke-width="2.5"/>
                  <circle cx="260" cy="55" r="8" fill="#EA580C" stroke="white" stroke-width="2.5"/>
                  <rect x="220" y="20" width="85" height="24" rx="6" fill="white" stroke="#EA580C" stroke-width="1.5"/>
                  <text x="226" y="36" fill="#EA580C" font-size="9" font-weight="bold">RTU Ķīpsala</text>
                </svg>
              </div>

              <!-- Destination Summary Card -->
              <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm mt-3">
                <div class="flex items-center space-x-3 mb-2">
                  <div class="w-9 h-9 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center font-bold text-sm" aria-hidden="true">
                    📍
                  </div>
                  <div>
                    <h3 id="preview-destination-title" class="font-bold text-slate-900 text-base leading-tight">Riga Technical University (RTU)</h3>
                    <p id="preview-destination-sub" class="text-xs text-slate-600 mt-0.5">Ķīpsala Campus • 2.4 km • 28 min • 8 waypoints</p>
                  </div>
                </div>
                <div class="flex items-center justify-between text-xs text-slate-700 border-t border-slate-100 pt-2.5">
                  <span>Sidewalk condition: <strong class="text-emerald-700">Clear</strong></span>
                  <span>Audio cues: <strong class="text-slate-900">High</strong></span>
                </div>
              </div>
            </div>

            <!-- Route Actions -->
            <div class="flex flex-col space-y-2.5 pt-1">
              <button onclick="startNavigationRoute('Riga Technical University')" aria-label="Start walking navigation to Riga Technical University" class="w-full py-4 rounded-2xl bg-black text-white font-bold text-base shadow-md hover:bg-neutral-800 transition active:scale-[0.99] flex items-center justify-center space-x-2">
                <span>Start navigation</span>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
              </button>
              <button onclick="speakRouteOverview()" aria-label="Describe route overview and audible cues" class="w-full py-3 rounded-2xl bg-white border border-slate-200 text-slate-800 font-semibold text-sm shadow-sm hover:bg-slate-50 transition active:scale-[0.99] flex items-center justify-center space-x-2">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
                <span>Describe route</span>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 5: ACTIVE NAVIGATION ==================== -->
          <div id="screen-activeNavigation" role="region" aria-label="Screen 5: Active Walking Navigation" class="flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <div class="flex justify-between items-center pt-2 px-1">
              <button onclick="stopNavigationRoute()" aria-label="Stop navigation and return to destination preview" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <!-- Navigation Instruction Card with ARIA live region -->
            <div class="flex-1 flex flex-col justify-center my-auto">
              <div class="flex justify-center mb-3">
                <div class="w-12 h-12 rounded-full orb-3d shadow-md" aria-hidden="true"></div>
              </div>

              <div class="bg-white rounded-3xl p-6 border border-slate-200 shadow-md flex flex-col items-center text-center relative overflow-hidden" role="region" aria-label="Current Navigation Step" aria-live="assertive">
                <span id="nav-step-label" class="text-xs font-bold text-orange-600 uppercase tracking-widest mb-1">
                  Navigation • Step 1 of 4
                </span>
                <h2 id="nav-instruction-text" class="text-2xl font-bold text-slate-900 tracking-tight leading-snug mb-2">
                  Turn right on Ķīpsalas iela
                </h2>
                
                <!-- Large Distance Number -->
                <div class="my-2 flex items-baseline justify-center space-x-1" aria-label="Distance remaining">
                  <span id="nav-distance-num" class="text-6xl font-black text-slate-900 tracking-tight">120</span>
                  <span class="text-lg font-bold text-slate-600">meters</span>
                </div>

                <!-- Maneuver Direction Banner -->
                <div class="w-full mt-3 bg-slate-50 border border-slate-200 rounded-2xl py-3 px-4 flex items-center justify-center space-x-3 text-slate-700">
                  <div id="nav-maneuver-icon" class="w-8 h-8 rounded-full bg-orange-500 text-white flex items-center justify-center font-bold text-base" aria-hidden="true">
                    ↱
                  </div>
                  <span id="nav-maneuver-text" class="font-bold text-sm text-slate-800">Turn right in 120m</span>
                </div>
              </div>

              <!-- Quick safety triggers -->
              <div class="flex justify-center gap-2 mt-3" role="group" aria-label="Simulation test triggers">
                <button onclick="navigateTo('obstacleAlert')" aria-label="Simulate obstacle hazard detection" class="px-3 py-1.5 bg-red-100 text-red-800 hover:bg-red-200 rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-sm">
                  <span aria-hidden="true">⚠️</span> Simulate Obstacle
                </button>
                <button onclick="navigateTo('crosswalkSafety')" aria-label="Simulate approaching crosswalk quiet mode" class="px-3 py-1.5 bg-amber-100 text-amber-900 hover:bg-amber-200 rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-sm">
                  <span aria-hidden="true">🚶</span> Simulate Crosswalk
                </button>
              </div>
            </div>

            <!-- Navigation Controls -->
            <div class="flex flex-col space-y-2 pt-2">
              <button onclick="repeatCurrentStep()" aria-label="Repeat current navigation instruction" class="w-full py-3 rounded-2xl bg-white border border-slate-200 text-slate-800 font-semibold text-sm shadow-sm hover:bg-slate-50 transition active:scale-[0.99] flex items-center justify-center space-x-2">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
                <span>Repeat instruction</span>
              </button>
              <button onclick="stopNavigationRoute()" aria-label="Stop navigation route and return to home screen" class="w-full py-4 rounded-2xl bg-black text-white font-bold text-base shadow-md hover:bg-neutral-800 transition active:scale-[0.99] flex items-center justify-center space-x-2">
                <span>Stop route</span>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 6: WHERE AM I? ==================== -->
          <div id="screen-whereAmI" role="region" aria-label="Screen 6: Where am I?" class="flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <div class="flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('home')" aria-label="Back to home screen" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <!-- Location Info Content -->
            <div class="flex-1 flex flex-col justify-center my-auto">
              <h2 class="sr-only">Current Location Context</h2>
              <div class="flex justify-center mb-3">
                <div class="w-12 h-12 rounded-full orb-3d shadow-md" aria-hidden="true"></div>
              </div>

              <!-- Main Location Card -->
              <div class="bg-white rounded-3xl p-5 border border-slate-200 shadow-md text-left">
                <div class="flex items-center space-x-2 text-xs font-bold text-purple-600 uppercase tracking-wider mb-1">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 010-5 2.5 2.5 0 010 5z"/></svg>
                  <span>Current Position</span>
                </div>
                <h3 class="text-xl font-bold text-slate-900 leading-snug mb-1">
                  You are near Riga Technical University, Ķīpsala Campus
                </h3>
                <p class="text-xs text-slate-600 mb-3">Paula Valdena iela • Ķīpsala, Riga, Latvia</p>

                <!-- Photo Thumbnail Card with descriptive alt -->
                <div class="w-full h-32 rounded-2xl overflow-hidden mb-3 border border-slate-200 shadow-sm relative">
                  <img src="{img_campus}" alt="Photograph of Riga Technical University main campus entrance building with paved pedestrian walkway and sunny plaza" class="w-full h-full object-cover">
                  <div class="absolute bottom-2 left-2 px-2 py-0.5 rounded-md bg-black/60 text-white text-[10px] font-semibold backdrop-blur-sm" aria-hidden="true">
                    RTU Main Building
                  </div>
                </div>

                <!-- Orientation & Compass Card -->
                <div class="bg-slate-50 rounded-2xl p-3 border border-slate-100 flex items-center justify-between text-xs">
                  <div>
                    <div class="font-bold text-slate-700">Orientation</div>
                    <div class="text-slate-600">Facing East (84°) towards entrance</div>
                  </div>
                  <div class="w-8 h-8 rounded-full bg-white border border-slate-200 flex items-center justify-center font-bold text-slate-800 text-xs shadow-xs" role="img" aria-label="Facing East">
                    E
                  </div>
                </div>
              </div>
            </div>

            <!-- Bottom Action -->
            <div class="flex flex-col space-y-2 pt-2">
              <button onclick="speakText('You are at Riga Technical University, Ķīpsala Campus in Riga, Latvia. Facing East towards the main entrance.')" aria-label="Repeat current location, address, and orientation" class="w-full py-3.5 rounded-2xl bg-white border border-slate-200 text-slate-800 font-semibold text-sm shadow-sm hover:bg-slate-50 transition active:scale-[0.99] flex items-center justify-center space-x-2">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-slate-600" fill="currentColor" viewBox="0 0 24 24"><path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.5A2.25 2.25 0 0 0 2.25 9.75v4.5A2.25 2.25 0 0 0 4.5 16.5h1.94l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06Z"/></svg>
                <span>Repeat location</span>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 7: DESCRIBE WHAT'S AROUND ME ==================== -->
          <div id="screen-describeAround" role="region" aria-label="Screen 7: Describe what's around me" class="flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <!-- Header -->
            <div class="flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('home')" aria-label="Back to home screen" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition active:scale-95">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <!-- Body -->
            <div class="flex-1 flex flex-col pt-1 overflow-y-auto no-scrollbar">
              <div class="flex justify-center mb-1.5">
                <div class="w-12 h-12 rounded-full orb-3d shadow-md" aria-hidden="true"></div>
              </div>

              <!-- Title -->
              <h2 class="text-2xl font-bold text-center text-slate-900 tracking-tight mb-3">
                Here’s what I see:
              </h2>

              <!-- Camera Scene Photo Card -->
              <div class="w-full h-36 rounded-2xl overflow-hidden mb-3 border border-slate-200 shadow-sm flex-shrink-0">
                <img src="{img_campus}" alt="Camera scene: Clear paved pathway in front, Riga Technical University main entrance on the left, bicycle rack on the right" class="w-full h-full object-cover">
              </div>

              <!-- Semantic List with 5 structured items -->
              <ul role="list" aria-label="Objects and environment observed" class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col divide-y divide-slate-100 list-none p-0 m-0">
                
                <!-- Row 1: Sidewalk ahead is clear -->
                <li class="flex items-center space-x-3 p-3">
                  <div class="w-6 h-6 rounded-full bg-emerald-500 text-white flex items-center justify-center font-bold text-xs flex-shrink-0" aria-hidden="true">
                    ✓
                  </div>
                  <span class="font-medium text-slate-900 text-sm">Sidewalk ahead is clear.</span>
                </li>

                <!-- Row 2: Riga Technical University (RTU) -->
                <li class="flex items-center space-x-3 p-3">
                  <div class="w-6 h-6 text-purple-600 flex items-center justify-center flex-shrink-0" aria-hidden="true">
                    <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M19 2H9c-1.1 0-2 .9-2 2v1H5c-1.1 0-2 .9-2 2v13c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM5 19V7h2v12H5zm6 0H9v-2h2v2zm0-4H9v-2h2v2zm0-4H9V9h2v2zm0-4H9V5h2v2zm4 12h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V9h2v2zm0-4h-2V5h2v2zm4 12h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V9h2v2zm0-4h-2V5h2v2z"/></svg>
                  </div>
                  <div class="flex flex-col">
                    <span class="font-bold text-slate-900 text-sm leading-tight">Riga Technical University (RTU)</span>
                    <span class="text-xs text-slate-600 mt-0.5">Main entrance on the left.</span>
                  </div>
                </li>

                <!-- Row 3: Bicycle rack 3 meters ahead on right -->
                <li class="flex items-center space-x-3 p-3">
                  <div class="w-6 h-6 text-blue-600 flex items-center justify-center flex-shrink-0" aria-hidden="true">
                    <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-3.6c.4-.6 1-1 1.8-1h4v2h-3.4l-1.4 2.1 2.2 2.5c.6.7 1.6 1.1 2.6 1.1V18c-1.6 0-3.1-.7-4.1-1.8l-1.5-1.7-.8 3.5H7.8l1.3-6-2.1 1.2v3.8H5v-4.9l4.5-2.6.9-.5 1.4 2zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z"/></svg>
                  </div>
                  <span class="font-medium text-slate-900 text-sm">Bicycle rack 3 meters ahead on right.</span>
                </li>

                <!-- Row 4: People walking nearby -->
                <li class="flex items-center space-x-3 p-3">
                  <div class="w-6 h-6 text-indigo-500 flex items-center justify-center flex-shrink-0" aria-hidden="true">
                    <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
                  </div>
                  <span class="font-medium text-slate-900 text-sm">People walking nearby.</span>
                </li>

                <!-- Row 5: It is sunny and bright -->
                <li class="flex items-center space-x-3 p-3">
                  <div class="w-6 h-6 text-amber-500 flex items-center justify-center flex-shrink-0" aria-hidden="true">
                    <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M6.76 4.84l-1.8-1.79-1.41 1.41 1.79 1.79 1.42-1.41zM4 10.5H1v2h3v-2zm9-9.95h-2V3.5h2V.55zm7.45 3.91l-1.41-1.41-1.79 1.79 1.41 1.41 1.79-1.79zm-3.21 13.7l1.79 1.8 1.41-1.41-1.8-1.79-1.4 1.4zM20 10.5v2h3v-2h-3zm-8-5c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm0 10c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4zm-1 4.45h2V23.4h-2v-3.45zm-7.45-1.41l1.41 1.41 1.79-1.8-1.41-1.41-1.79 1.8z"/></svg>
                  </div>
                  <span class="font-medium text-slate-900 text-sm">It is sunny and bright.</span>
                </li>

              </ul>
            </div>

            <!-- Bottom Repeat Pill Button -->
            <div class="flex justify-center pt-3">
              <button onclick="repeatSceneDescription()" aria-label="Repeat visual scene description" class="px-7 py-3 rounded-full bg-white border border-slate-200 text-slate-900 font-bold text-sm shadow-md hover:bg-slate-50 transition active:scale-95 flex items-center space-x-2">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-800" fill="currentColor" viewBox="0 0 24 24"><path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.5A2.25 2.25 0 0 0 2.25 9.75v4.5A2.25 2.25 0 0 0 4.5 16.5h1.94l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06ZM18.584 5.106a.75.75 0 0 1 1.06 0c3.808 3.807 3.808 9.98 0 13.788a.75.75 0 0 1-1.06-1.06 8.25 8.25 0 0 0 0-11.668.75.75 0 0 1 0-1.06Z"/></svg>
                <span>Repeat</span>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 8: OBSTACLE AHEAD (Hazard Detection) ==================== -->
          <div id="screen-obstacleAlert" role="region" aria-label="Screen 8: Obstacle Ahead Warning" class="flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <!-- Header -->
            <div class="flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('activeNavigation')" aria-label="Back to active navigation" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition active:scale-95">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <!-- Top Warning Alert Banner (role="alert" for immediate screen reader announcement) -->
            <div role="alert" aria-live="assertive" class="mt-2 bg-[#FEECEC] border border-red-200 rounded-3xl p-4 flex items-center space-x-3.5 shadow-sm">
              <div class="w-11 h-11 text-red-600 flex items-center justify-center flex-shrink-0" aria-hidden="true">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 fill-red-600" viewBox="0 0 24 24"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>
              </div>
              <div class="flex flex-col">
                <h2 class="text-xl font-bold text-red-600 leading-tight">Obstacle ahead</h2>
                <p class="text-xs text-slate-800 font-medium leading-relaxed mt-0.5">
                  Two meters ahead,<br>construction barrier on right.
                </p>
              </div>
            </div>

            <!-- Camera View with AR Path and Barrier Highlight -->
            <div class="flex-1 my-3 relative rounded-3xl overflow-hidden border border-slate-200 shadow-inner flex flex-col justify-end p-3.5">
              <img src="{img_obstacle}" alt="Camera scene showing sidewalk ahead with a high-visibility orange construction barrier on the right side two meters forward" class="absolute inset-0 w-full h-full object-cover">
              
              <!-- Floating Obstacle Detail Card -->
              <div class="relative z-10 bg-white/95 backdrop-blur-md rounded-2xl p-3.5 border border-slate-100 shadow-md flex items-center space-x-3">
                <div class="w-10 h-10 rounded-full bg-orange-100 text-orange-500 flex items-center justify-center text-xl flex-shrink-0" role="img" aria-label="Hazard barrier icon">
                  🚧
                </div>
                <div class="flex flex-col">
                  <h3 class="font-bold text-slate-900 text-sm leading-tight">Construction barrier</h3>
                  <p class="text-xs text-slate-600 mt-0.5">On the right, 2 meters ahead.</p>
                </div>
              </div>
            </div>

            <!-- Bottom Action Buttons -->
            <div class="flex flex-col space-y-2.5 pt-1">
              <!-- Repeat button -->
              <button onclick="repeatObstacleWarning()" aria-label="Repeat obstacle warning" class="w-full py-3.5 rounded-full bg-white border border-slate-200 text-slate-900 font-bold text-sm shadow-sm hover:bg-slate-50 transition active:scale-95 flex items-center justify-center space-x-2">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-800" fill="currentColor" viewBox="0 0 24 24"><path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.5A2.25 2.25 0 0 0 2.25 9.75v4.5A2.25 2.25 0 0 0 4.5 16.5h1.94l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06ZM18.584 5.106a.75.75 0 0 1 1.06 0c3.808 3.807 3.808 9.98 0 13.788a.75.75 0 0 1-1.06-1.06 8.25 8.25 0 0 0 0-11.668.75.75 0 0 1 0-1.06Z"/></svg>
                <span>Repeat</span>
              </button>

              <!-- I Understand button -->
              <button onclick="acknowledgeObstacle()" aria-label="I Understand obstacle warning, resume navigation path" class="w-full py-3.5 rounded-full bg-neutral-900 text-white font-bold text-sm shadow-md hover:bg-black transition active:scale-95 flex items-center justify-center space-x-2">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg>
                <span>I Understand</span>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 9: APPROACHING CROSSWALK (Quiet Mode) ==================== -->
          <div id="screen-crosswalkSafety" role="region" aria-label="Screen 9: Approaching Crosswalk Quiet Mode" class="flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <!-- Header -->
            <div class="flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('activeNavigation')" aria-label="Back to active navigation" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition active:scale-95">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <!-- Top Warning Notice Banner (role="alert" for immediate screen reader notice) -->
            <div role="alert" aria-live="assertive" class="mt-2 bg-[#FEE881] rounded-3xl p-4 flex items-center space-x-4 shadow-sm">
              <div class="w-10 h-10 text-black flex items-center justify-center flex-shrink-0" aria-hidden="true">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-9 h-9 fill-black" viewBox="0 0 24 24"><path d="M13.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.8 8.9L7 23h2.1l1.8-8 2.1 2v6h2v-7.5l-2.1-2 .6-3C14.8 12 16.8 13 19 13v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L6 8.3V13h2V9.6l1.8-.7z"/></svg>
              </div>
              <div class="flex flex-col">
                <h2 class="text-xl font-bold text-black leading-tight">Approaching crosswalk.</h2>
                <p class="text-sm text-slate-900 mt-0.5">Listen for traffic.</p>
              </div>
            </div>

            <!-- Camera View with Zebra Crossing & Green Signal -->
            <div class="flex-1 my-3 relative rounded-3xl overflow-hidden border border-slate-200 shadow-inner flex flex-col justify-end p-3.5">
              <img src="{img_crosswalk}" alt="Camera scene showing pedestrian zebra crossing on the asphalt street with a green pedestrian signal illuminated" class="absolute inset-0 w-full h-full object-cover">

              <!-- Accessible Floating Quiet Mode Waveform Card -->
              <button type="button" onclick="confirmCrossed()" aria-label="Quiet mode active: I will be quiet while you cross. Tap when across to resume route." class="w-full relative z-10 bg-white/95 backdrop-blur-md rounded-3xl p-5 border border-slate-100 shadow-lg flex flex-col items-center justify-center text-center cursor-pointer hover:bg-white transition">
                
                <!-- Amber Audio Waveform Bars (Decorative) -->
                <div class="flex items-center space-x-1.5 h-12 mb-3" aria-hidden="true">
                  <div class="w-1.5 h-4 bg-amber-500 rounded-full wave-bar wave-1"></div>
                  <div class="w-1.5 h-7 bg-amber-500 rounded-full wave-bar wave-2"></div>
                  <div class="w-1.5 h-10 bg-amber-500 rounded-full wave-bar wave-3"></div>
                  <div class="w-1.5 h-12 bg-amber-500 rounded-full wave-bar wave-4"></div>
                  <div class="w-1.5 h-14 bg-amber-500 rounded-full wave-bar wave-5"></div>
                  <div class="w-1.5 h-12 bg-amber-500 rounded-full wave-bar wave-6"></div>
                  <div class="w-1.5 h-10 bg-amber-500 rounded-full wave-bar wave-7"></div>
                  <div class="w-1.5 h-7 bg-amber-500 rounded-full wave-bar wave-8"></div>
                  <div class="w-1.5 h-4 bg-amber-500 rounded-full wave-bar wave-9"></div>
                </div>

                <p class="text-base font-medium text-slate-800">
                  I will be quiet while you cross.
                </p>
                <span class="text-xs text-slate-600 mt-1" aria-hidden="true">(Tap card when across to resume route)</span>
              </button>
            </div>

            <!-- Bottom Action -->
            <div class="pt-1">
              <button onclick="confirmCrossed()" aria-label="Confirm crosswalk completed and resume navigation route" class="w-full py-3.5 rounded-full bg-neutral-900 text-white font-bold text-sm shadow-md hover:bg-black transition active:scale-95 flex items-center justify-center space-x-2">
                <span>Crosswalk Completed — Resume Route</span>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>
            </div>
          </div>

        </section>

        <!-- Home Bar Indicator (Decorative) -->
        <div class="pb-2 flex justify-center z-30" aria-hidden="true">
          <div class="w-32 h-1 bg-neutral-400 rounded-full"></div>
        </div>
      </div>
    </div>

    <!-- VIEW 2: ALL 9 SCREENS SIDE-BY-SIDE GALLERY (Cloned Visual Previews - Hidden from Assistive Tech to avoid duplicate IDs) -->
    <div id="view-sidebyside" role="tabpanel" aria-labelledby="btn-tab-sidebyside" aria-hidden="true" class="hidden w-full overflow-x-auto py-4 px-2 no-scrollbar">
      <div class="flex gap-6 items-start pb-4 min-w-max">
        
        <div class="flex flex-col items-center">
          <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">1. Home</span>
          <div class="iphone-frame" id="gallery-screen-1"></div>
        </div>

        <div class="flex flex-col items-center">
          <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">2. Voice Listening</span>
          <div class="iphone-frame" id="gallery-screen-2"></div>
        </div>

        <div class="flex flex-col items-center">
          <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">3. Destination Search</span>
          <div class="iphone-frame" id="gallery-screen-3"></div>
        </div>

        <div class="flex flex-col items-center">
          <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">4. Route Preview</span>
          <div class="iphone-frame" id="gallery-screen-4"></div>
        </div>

        <div class="flex flex-col items-center">
          <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">5. Active Navigation</span>
          <div class="iphone-frame" id="gallery-screen-5"></div>
        </div>

        <div class="flex flex-col items-center">
          <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">6. Where am I?</span>
          <div class="iphone-frame" id="gallery-screen-6"></div>
        </div>

        <div class="flex flex-col items-center">
          <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">7. Here's what I see</span>
          <div class="iphone-frame" id="gallery-screen-7"></div>
        </div>

        <div class="flex flex-col items-center">
          <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">8. Obstacle Ahead</span>
          <div class="iphone-frame" id="gallery-screen-8"></div>
        </div>

        <div class="flex flex-col items-center">
          <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">9. Crosswalk Quiet</span>
          <div class="iphone-frame" id="gallery-screen-9"></div>
        </div>

      </div>
    </div>

  </main>

  <!-- Settings Modal (Accessible Dialog with Focus Trap & Escape key handling) -->
  <div id="settings-modal" role="dialog" aria-modal="true" aria-labelledby="settings-modal-title" class="fixed inset-0 bg-black/40 backdrop-blur-xs z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-white rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-100 flex flex-col space-y-4">
      <div class="flex justify-between items-center">
        <h2 id="settings-modal-title" class="text-lg font-bold text-slate-900">Blind AI Settings</h2>
        <button id="close-settings-btn" onclick="closeSettingsModal()" aria-label="Close settings modal" class="w-8 h-8 rounded-full bg-slate-100 text-slate-600 flex items-center justify-center font-bold text-xs hover:bg-slate-200">✕</button>
      </div>
      <div class="space-y-3 text-sm text-slate-700">
        <div class="flex justify-between items-center py-2 border-b border-slate-100">
          <span>Voice Guidance Mode</span>
          <span class="font-bold text-slate-900">Standard (Turn-by-turn)</span>
        </div>
        <div class="flex justify-between items-center py-2 border-b border-slate-100">
          <span>Obstacle Detection Sensitivity</span>
          <span class="font-bold text-orange-600">High (2.0m warning)</span>
        </div>
        <div class="flex justify-between items-center py-2 border-b border-slate-100">
          <span>Crosswalk Quiet Mode</span>
          <span class="font-bold text-emerald-700">Enabled (Auto-silence)</span>
        </div>
        <div class="flex justify-between items-center py-2 border-b border-slate-100">
          <span>Backend AI Engine</span>
          <span class="font-bold text-blue-600">Gemini Flash 1.5</span>
        </div>
        <div class="flex justify-between items-center py-2 border-b border-slate-100">
          <span>Current Location</span>
          <span class="font-bold text-slate-900">Riga, Latvia</span>
        </div>
      </div>
      <button onclick="closeSettingsModal()" aria-label="Save and close settings modal" class="w-full py-3 bg-black text-white font-bold rounded-2xl hover:bg-neutral-800 transition">Done</button>
    </div>
  </div>

  <!-- Client-side Logic Script -->
  <script>
    // State management
    let activeRoute = 'home';
    let voiceEnabled = true;
    let autoWalkEnabled = true;
    let webSpeechRec = null;
    let currentDistance = 120;
    let currentWaypointIdx = 0;
    let navigationInterval = null;
    let previousActiveElement = null;

    const allScreens = [
      'home',
      'listening',
      'destinationSearch',
      'routePreview',
      'activeNavigation',
      'whereAmI',
      'describeAround',
      'obstacleAlert',
      'crosswalkSafety'
    ];

    const screenTitles = {{
      home: "Blind AI — Home",
      listening: "Voice Listening — Blind AI",
      destinationSearch: "Destination Search — Blind AI",
      routePreview: "Route Preview — Blind AI",
      activeNavigation: "Active Navigation — Blind AI",
      whereAmI: "Where Am I? — Blind AI",
      describeAround: "Here's What I See — Blind AI",
      obstacleAlert: "Obstacle Ahead Warning — Blind AI",
      crosswalkSafety: "Approaching Crosswalk (Quiet Mode) — Blind AI"
    }};

    const rtuWaypoints = [
      {{
        instruction: "Turn right on Ķīpsalas iela",
        distance: 120,
        maneuver: "Turn right in 120m",
        icon: "↱"
      }},
      {{
        instruction: "Continue straight along Paula Valdena iela",
        distance: 80,
        maneuver: "Continue straight",
        icon: "↑"
      }},
      {{
        instruction: "Approaching pedestrian crossing at Zunda quay",
        distance: 30,
        maneuver: "Crosswalk ahead",
        icon: "🚶"
      }},
      {{
        instruction: "Arrival: Riga Technical University (RTU)",
        distance: 0,
        maneuver: "Destination reached",
        icon: "★"
      }}
    ];

    // Screen Reader Announcer Helper (WCAG Live Region)
    function announceToScreenReader(message) {{
      const announcer = document.getElementById('a11y-announcer');
      if (announcer) {{
        announcer.textContent = '';
        setTimeout(() => {{
          announcer.textContent = message;
        }}, 50);
      }}
    }}

    // Resolves a canonical route name from a path, hash, or query identifier
    function resolveRouteName(identifier) {{
      if (!identifier) return 'home';
      const clean = identifier.replace(/^[\\/#\\?]+/, '').replace(/^route=/, '').trim();
      if (!clean || clean === 'home' || clean === 'preview' || clean === 'index.html') {{
        return 'home';
      }}
      const normalized = clean.toLowerCase().replace(/-/g, '');
      for (const s of allScreens) {{
        if (s.toLowerCase() === normalized) {{
          return s;
        }}
      }}
      return null;
    }}

    // Determines the initial route on startup or reload based on window.location
    function getInitialRoute() {{
      if (window.location.hash) {{
        const hashRoute = resolveRouteName(window.location.hash);
        if (hashRoute && hashRoute !== 'home') return hashRoute;
      }}
      try {{
        const params = new URLSearchParams(window.location.search);
        const queryRoute = params.get('route');
        if (queryRoute) {{
          const resolved = resolveRouteName(queryRoute);
          if (resolved && resolved !== 'home') return resolved;
        }}
      }} catch (e) {{}}
      if (window.location.protocol && window.location.protocol.startsWith('http')) {{
        const pathRoute = resolveRouteName(window.location.pathname);
        if (pathRoute) return pathRoute;
      }}
      return 'home';
    }}

    // Navigation state router with browser history synchronization and accessible focus management
    function navigateTo(route, updateHistory = true) {{
      const resolved = resolveRouteName(route);
      const targetRoute = (resolved && allScreens.includes(resolved)) ? resolved : 'home';
      activeRoute = targetRoute;

      // Update page title (WCAG 2.2 SC 2.4.2 Page Titled)
      document.title = screenTitles[targetRoute] || "Blind AI Assistant";

      const selector = document.getElementById('screen-selector');
      if (selector) selector.value = targetRoute;

      allScreens.forEach(s => {{
        const el = document.getElementById('screen-' + s);
        if (el) el.classList.add('hidden');
      }});

      const target = document.getElementById('screen-' + targetRoute);
      if (target) {{
        target.classList.remove('hidden');
        // Set focus to the active screen or its primary heading for screen readers (WCAG 2.2 SC 2.4.3 Focus Order)
        target.setAttribute('tabindex', '-1');
        const primaryHeading = target.querySelector('h1, h2, [role="alert"]');
        if (primaryHeading) {{
          primaryHeading.setAttribute('tabindex', '-1');
          primaryHeading.focus({{ preventScroll: true }});
        }} else {{
          target.focus({{ preventScroll: true }});
        }}
      }}

      // Synchronize browser address bar and history
      if (updateHistory && typeof history !== 'undefined') {{
        const targetPath = targetRoute === 'home' ? '/' : '/' + targetRoute;
        if (window.location.protocol.startsWith('http')) {{
          if (window.location.pathname !== targetPath) {{
            history.pushState({{ route: targetRoute }}, '', targetPath);
          }}
        }} else {{
          const targetHash = targetRoute === 'home' ? '' : '#' + targetRoute;
          if (window.location.hash !== targetHash) {{
            history.pushState({{ route: targetRoute }}, '', targetHash || window.location.pathname);
          }}
        }}
      }}

      // Update instructions and voice announcements
      const tip = document.getElementById('instruction-tip');

      if (targetRoute === 'home') {{
        tip.innerHTML = "Tap <strong>Describe what's around me</strong> or <strong>Start navigation</strong>";
        speakText("Blind AI home. How can I help you today?");
      }} else if (targetRoute === 'listening') {{
        tip.innerHTML = "Listening actively... Say <strong>'Take me to RTU'</strong> or <strong>'Describe around me'</strong>";
        speakText("Listening. Say your command or destination.");
        startVoiceCapture();
      }} else if (targetRoute === 'destinationSearch') {{
        tip.innerHTML = "Select a destination like <strong>Riga Technical University</strong> or speak";
        speakText("Where would you like to go? You can select Riga Technical University, Ķīpsala Campus.");
      }} else if (targetRoute === 'routePreview') {{
        tip.innerHTML = "Route preview to <strong>RTU Ķīpsala</strong>. Tap <strong>Start navigation</strong> to begin";
        speakText("Route preview to Riga Technical University, Ķīpsala. 2.4 kilometers, 28 minutes, 8 waypoints.");
      }} else if (targetRoute === 'activeNavigation') {{
        tip.innerHTML = "Active walking navigation with live countdown. Test safety events below.";
        announceToScreenReader("Active walking navigation started. Turn right on Ķīpsalas iela in 120 meters.");
      }} else if (targetRoute === 'whereAmI') {{
        tip.innerHTML = "Current location and orientation near <strong>RTU Ķīpsala Campus</strong>";
        speakText("Where am I? You are at Riga Technical University, Ķīpsala Campus in Riga, Latvia. Facing east.");
      }} else if (targetRoute === 'describeAround') {{
        tip.innerHTML = "Perception scene: <strong>RTU Campus</strong>. Tap <strong>Repeat</strong> to hear again";
        speakText("Here's what I see: Sidewalk ahead is clear. Riga Technical University main entrance on the left. Bicycle rack 3 meters ahead on right. People walking nearby. It is sunny and bright.");
      }} else if (targetRoute === 'obstacleAlert') {{
        tip.innerHTML = "Warning: <strong>Obstacle ahead</strong>. Tap <strong>I Understand</strong> to resume";
        speakText("Warning: Obstacle ahead. Two meters ahead, construction barrier on right. Pathway is clear on left.");
      }} else if (targetRoute === 'crosswalkSafety') {{
        tip.innerHTML = "Crosswalk quiet mode active. Tap waveform card when across to resume.";
        speakText("Approaching pedestrian crosswalk. Quiet mode active. Listen for traffic.");
      }}
    }}

    function jumpToScreen(route) {{
      navigateTo(route);
    }}

    // Destination search logic
    function filterDestinations(query) {{
      const q = query.toLowerCase();
      const list = document.getElementById('recent-places-list');
      const items = list.children;
      let visibleCount = 0;
      for (let i = 0; i < items.length; i++) {{
        const text = items[i].innerText.toLowerCase();
        const matches = text.includes(q);
        items[i].style.display = matches ? 'flex' : 'none';
        if (matches) visibleCount++;
      }}
      if (query.trim().length > 1) {{
        announceToScreenReader(`${{visibleCount}} destinations found for "${{query}}"`);
      }}
    }}

    function selectDestination(title, sub) {{
      triggerHaptic([60]);
      document.getElementById('preview-destination-title').innerText = title;
      document.getElementById('preview-destination-sub').innerText = sub + " • 2.4 km • 28 min • 8 waypoints";
      navigateTo('routePreview');
    }}

    function selectCategory(cat) {{
      triggerHaptic([40]);
      document.getElementById('destination-search-input').value = cat;
      filterDestinations(cat);
      announceToScreenReader(`Filtered by category ${{cat}}`);
    }}

    // Voice recognition & Intent Handling
    function startVoiceCapture() {{
      document.getElementById('live-transcript').innerText = "Speak now...";
      document.getElementById('island-mic-dot').classList.remove('bg-[#151515]');
      document.getElementById('island-mic-dot').classList.add('bg-orange-500');

      const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRec) {{
        if (!webSpeechRec) {{
          webSpeechRec = new SpeechRec();
          webSpeechRec.continuous = false;
          webSpeechRec.interimResults = true;
          webSpeechRec.lang = 'en-US';
          webSpeechRec.onresult = (e) => {{
            let transcript = "";
            for (let i = e.resultIndex; i < e.results.length; i++) transcript += e.results[i][0].transcript;
            document.getElementById('live-transcript').innerText = '“' + transcript + '”';
            if (e.results[0].isFinal) handleVoiceInput(transcript);
          }};
          webSpeechRec.onend = () => {{
            document.getElementById('island-mic-dot').classList.remove('bg-orange-500');
            document.getElementById('island-mic-dot').classList.add('bg-[#151515]');
          }};
        }}
        try {{ webSpeechRec.start(); }} catch(e){{}}
      }}
    }}

    function handleVoiceInput(rawText) {{
      const t = rawText.toLowerCase();
      document.getElementById('live-transcript').innerText = '“' + rawText + '”';

      if (t.includes('rtu') || t.includes('cif') || t.includes('kipsala') || t.includes('take me to') || t.includes('navigate') || t.includes('start route')) {{
        document.getElementById('listening-title').innerText = "Routing to RTU...";
        triggerHaptic([80, 40, 80]);
        setTimeout(() => {{
          navigateTo('routePreview');
        }}, 900);
      }} else if (t.includes('where am i') || t.includes('location')) {{
        setTimeout(() => navigateTo('whereAmI'), 600);
      }} else if (t.includes('front') || t.includes('around') || t.includes('describe') || t.includes('see')) {{
        setTimeout(() => navigateTo('describeAround'), 600);
      }} else if (t.includes('stop') || t.includes('cancel')) {{
        navigateTo('home');
      }} else {{
        speakText("I heard: " + rawText);
        setTimeout(() => navigateTo('home'), 1500);
      }}
    }}

    // Active Navigation Lifecycle
    function startNavigationRoute(destName) {{
      navigateTo('activeNavigation');
      triggerHaptic([80, 40, 80]);
      currentWaypointIdx = 0;
      currentDistance = rtuWaypoints[0].distance;
      renderActiveWaypoint();

      speakText(`Starting walking route to ${{destName}}. ${{rtuWaypoints[0].instruction}} in ${{currentDistance}} meters.`);

      if (navigationInterval) clearInterval(navigationInterval);
      if (autoWalkEnabled) {{
        navigationInterval = setInterval(progressWalking, 2200);
      }}
    }}

    function renderActiveWaypoint() {{
      const wp = rtuWaypoints[currentWaypointIdx];
      document.getElementById('nav-step-label').innerText = `Navigation • Step ${{currentWaypointIdx + 1}} of ${{rtuWaypoints.length}}`;
      document.getElementById('nav-instruction-text').innerText = wp.instruction;
      document.getElementById('nav-distance-num').innerText = currentDistance;
      document.getElementById('nav-maneuver-text').innerText = wp.maneuver;
      document.getElementById('nav-maneuver-icon').innerText = wp.icon;
    }}

    function progressWalking() {{
      if (activeRoute !== 'activeNavigation') return;

      if (currentDistance > 10) {{
        currentDistance -= 10;
        document.getElementById('nav-distance-num').innerText = currentDistance;

        // Auto safety trigger 1: Construction barrier obstacle at 80m
        if (currentDistance === 80) {{
          triggerHaptic([100, 100, 150]);
          setTimeout(() => navigateTo('obstacleAlert'), 800);
          return;
        }}

        // Auto safety trigger 2: Crosswalk at 30m
        if (currentDistance === 30) {{
          triggerHaptic([80, 60, 80]);
          setTimeout(() => navigateTo('crosswalkSafety'), 800);
          return;
        }}

        if (currentDistance === 50) {{
          triggerHaptic([50]);
          speakText(`50 meters to next turn.`);
        }}
      }} else {{
        // Next waypoint
        currentWaypointIdx++;
        if (currentWaypointIdx < rtuWaypoints.length) {{
          currentDistance = rtuWaypoints[currentWaypointIdx].distance;
          renderActiveWaypoint();
          speakText(rtuWaypoints[currentWaypointIdx].instruction);
        }} else {{
          clearInterval(navigationInterval);
          speakText("You have arrived at Riga Technical University. Navigation complete.");
          triggerHaptic([120, 60, 120, 60, 200]);
          setTimeout(() => navigateTo('home'), 3500);
        }}
      }}
    }}

    function repeatCurrentStep() {{
      triggerHaptic([40]);
      const wp = rtuWaypoints[currentWaypointIdx];
      speakText(`${{wp.instruction}}. ${{currentDistance}} meters remaining.`);
    }}

    function stopNavigationRoute() {{
      triggerHaptic([100]);
      if (navigationInterval) clearInterval(navigationInterval);
      speakText("Navigation stopped.");
      navigateTo('home');
    }}

    function speakRouteOverview() {{
      triggerHaptic([40]);
      speakText("Route overview: Follow Paula Valdena iela across Ķīpsala. Distance 2.4 kilometers. Estimated time 28 minutes. Sidewalk condition is clear.");
    }}

    // Safety Screen Actions
    function repeatSceneDescription() {{
      triggerHaptic([40]);
      speakText("Here's what I see: Sidewalk ahead is clear. Riga Technical University main entrance on the left. Bicycle rack 3 meters ahead on right. People walking nearby. It is sunny and bright.");
    }}

    function repeatObstacleWarning() {{
      triggerHaptic([40]);
      speakText("Warning: Two meters ahead, construction barrier on right. Stay on the left pathway.");
    }}

    function acknowledgeObstacle() {{
      triggerHaptic([60, 40]);
      speakText("Obstacle acknowledged. Resuming path.");
      
      try {{
        fetch('http://localhost:3000/api/v1/navigation/sessions/default/events', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            obstacle_type: 'construction_barrier',
            lane: 'right',
            distance_meters: 2.0,
            action_taken: 'avoid_left'
          }})
        }}).catch(() => {{}});
      }} catch(e){{}}

      setTimeout(() => {{
        navigateTo('activeNavigation');
      }}, 400);
    }}

    function confirmCrossed() {{
      triggerHaptic([80, 50]);
      speakText("Crosswalk completed. Resuming route.");
      setTimeout(() => {{
        navigateTo('activeNavigation');
      }}, 400);
    }}

    // Speech Synthesizer & Accessibility Live Announcer helper
    function speakText(text) {{
      announceToScreenReader(text);
      if (!voiceEnabled) return;
      if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(text);
        utter.rate = 1.05;
        utter.pitch = 1.0;
        window.speechSynthesis.speak(utter);
      }}
    }}

    function toggleAudioSpeech() {{
      voiceEnabled = !voiceEnabled;
      const lbl = document.getElementById('speech-status-label');
      const btn = document.getElementById('audio-toggle-btn');
      lbl.innerText = voiceEnabled ? "Voice: On" : "Voice: Muted";
      btn.setAttribute('aria-checked', voiceEnabled ? 'true' : 'false');
      btn.setAttribute('aria-label', voiceEnabled ? 'Voice guidance enabled. Tap to mute voice.' : 'Voice guidance muted. Tap to enable voice.');
      if (!voiceEnabled && 'speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
      }}
      announceToScreenReader(voiceEnabled ? "Voice guidance enabled" : "Voice guidance muted");
    }}

    function toggleWalkSimulation() {{
      autoWalkEnabled = !autoWalkEnabled;
      const lbl = document.getElementById('walk-sim-label');
      const btn = document.getElementById('walk-sim-btn');
      btn.setAttribute('aria-checked', autoWalkEnabled ? 'true' : 'false');
      btn.setAttribute('aria-label', autoWalkEnabled ? 'Auto-walk simulation active. Tap to pause.' : 'Auto-walk simulation paused. Tap to resume.');
      if (autoWalkEnabled) {{
        lbl.innerText = "Auto-Walk: ON";
        btn.classList.remove('bg-slate-500');
        btn.classList.add('bg-amber-500');
        if (activeRoute === 'activeNavigation' && !navigationInterval) {{
          navigationInterval = setInterval(progressWalking, 2200);
        }}
        announceToScreenReader("Auto-walk simulation enabled");
      }} else {{
        lbl.innerText = "Auto-Walk: OFF";
        btn.classList.remove('bg-amber-500');
        btn.classList.add('bg-slate-500');
        if (navigationInterval) clearInterval(navigationInterval);
        announceToScreenReader("Auto-walk simulation paused");
      }}
    }}

    function triggerHaptic(pattern) {{
      if (navigator.vibrate) {{
        navigator.vibrate(pattern);
      }}
    }}

    // Accessible Modal controls with Focus Trap & Escape key handling (WCAG 2.2 SC 2.1.2)
    function openSettingsModal() {{
      previousActiveElement = document.activeElement;
      const modal = document.getElementById('settings-modal');
      modal.classList.remove('hidden');
      const closeBtn = document.getElementById('close-settings-btn');
      if (closeBtn) closeBtn.focus();
      document.addEventListener('keydown', handleModalKeyDown);
      announceToScreenReader("Opened Blind AI Settings modal");
    }}

    function closeSettingsModal() {{
      const modal = document.getElementById('settings-modal');
      modal.classList.add('hidden');
      document.removeEventListener('keydown', handleModalKeyDown);
      if (previousActiveElement && typeof previousActiveElement.focus === 'function') {{
        previousActiveElement.focus();
      }}
      announceToScreenReader("Closed Settings modal");
    }}

    function handleModalKeyDown(e) {{
      if (e.key === 'Escape') {{
        closeSettingsModal();
        return;
      }}
      if (e.key === 'Tab') {{
        const modal = document.getElementById('settings-modal');
        const focusable = modal.querySelectorAll('button:not([disabled]), [tabindex]:not([tabindex="-1"])');
        if (focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey) {{
          if (document.activeElement === first) {{
            e.preventDefault();
            last.focus();
          }}
        }} else {{
          if (document.activeElement === last) {{
            e.preventDefault();
            first.focus();
          }}
        }}
      }}
    }}

    // Switch between Interactive and Side-by-Side Gallery
    function switchSimulatorMode(mode) {{
      const btnInt = document.getElementById('btn-tab-interactive');
      const btnSide = document.getElementById('btn-tab-sidebyside');
      const viewInt = document.getElementById('view-interactive');
      const viewSide = document.getElementById('view-sidebyside');

      if (mode === 'interactive') {{
        btnInt.className = "px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-sm transition";
        btnInt.setAttribute('aria-selected', 'true');
        btnSide.className = "px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition";
        btnSide.setAttribute('aria-selected', 'false');
        viewInt.classList.remove('hidden');
        viewSide.classList.add('hidden');
        viewSide.setAttribute('aria-hidden', 'true');
        announceToScreenReader("Switched to Interactive Device view");
      }} else {{
        btnSide.className = "px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-sm transition";
        btnSide.setAttribute('aria-selected', 'true');
        btnInt.className = "px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition";
        btnInt.setAttribute('aria-selected', 'false');
        viewInt.classList.add('hidden');
        viewSide.classList.remove('hidden');
        viewSide.setAttribute('aria-hidden', 'false');
        populateSideBySideGallery();
        announceToScreenReader("Switched to All 9 Screens Side-by-Side view");
      }}
    }}

    function populateSideBySideGallery() {{
      const screens = [
        {{ id: 'home', target: 'gallery-screen-1' }},
        {{ id: 'listening', target: 'gallery-screen-2' }},
        {{ id: 'destinationSearch', target: 'gallery-screen-3' }},
        {{ id: 'routePreview', target: 'gallery-screen-4' }},
        {{ id: 'activeNavigation', target: 'gallery-screen-5' }},
        {{ id: 'whereAmI', target: 'gallery-screen-6' }},
        {{ id: 'describeAround', target: 'gallery-screen-7' }},
        {{ id: 'obstacleAlert', target: 'gallery-screen-8' }},
        {{ id: 'crosswalkSafety', target: 'gallery-screen-9' }}
      ];

      screens.forEach(item => {{
        const target = document.getElementById(item.target);
        const src = document.getElementById('screen-' + item.id);
        if (target && src) {{
          const clone = src.cloneNode(true);
          clone.classList.remove('hidden');
          clone.id = 'gallery-clone-' + item.id;
          clone.setAttribute('aria-hidden', 'true');
          // Disable interactive elements in gallery clones to prevent focus pollution
          clone.querySelectorAll('button, input, select').forEach(el => {{
            el.setAttribute('tabindex', '-1');
            el.setAttribute('aria-hidden', 'true');
          }});
          
          target.innerHTML = `
            <div class="pt-3 px-7 flex justify-between items-center text-xs font-semibold text-black z-30" aria-hidden="true">
              <span>9:41</span>
              <div class="w-24 h-6 bg-black rounded-full"></div>
              <div class="w-5 h-2.5 border border-black rounded-sm"></div>
            </div>
            <div class="flex-1 flex flex-col overflow-y-auto no-scrollbar relative" aria-hidden="true">
            </div>
            <div class="pb-2 flex justify-center z-30" aria-hidden="true">
              <div class="w-32 h-1 bg-neutral-400 rounded-full"></div>
            </div>
          `;
          target.querySelector('.relative').appendChild(clone);
        }}
      }});
    }}

    // Browser Back / Forward buttons handling
    window.addEventListener('popstate', (event) => {{
      const targetRoute = (event.state && event.state.route) ? event.state.route : getInitialRoute();
      navigateTo(targetRoute, false);
    }});

    // Initialize on load
    window.addEventListener('DOMContentLoaded', () => {{
      const initialRoute = getInitialRoute();
      navigateTo(initialRoute, false);

      // Ensure initial history state matches the current URL
      if (typeof history !== 'undefined' && history.replaceState) {{
        const targetPath = initialRoute === 'home' ? '/' : '/' + initialRoute;
        if (window.location.protocol.startsWith('http')) {{
          history.replaceState({{ route: initialRoute }}, '', targetPath);
        }} else {{
          const targetHash = initialRoute === 'home' ? '' : '#' + initialRoute;
          history.replaceState({{ route: initialRoute }}, '', targetHash || window.location.pathname);
        }}
      }}
    }});
  </script>
</body>
</html>"""

with open('preview.html', 'w') as f:
    f.write(html_content)

artifact_path = '/Users/ranjeet/.gemini/antigravity/brain/c5f01990-a932-4376-b981-a9dfcbedd688/blind_ai_simulator.html'
with open(artifact_path, 'w') as f:
    f.write(html_content)

print('Generated accessible preview.html and blind_ai_simulator.html successfully!')
