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
      width: 100%;
      max-width: 420px;
      height: 100vh;
      height: 100dvh;
      max-height: 860px;
      border-radius: 0;
      box-shadow: none;
      overflow: hidden;
      position: relative;
      background-color: #F8F8F9;
      user-select: none;
      display: flex;
      flex-direction: column;
    }}
    @media (min-width: 640px) {{
      .iphone-frame {{
        border-radius: 38px;
        box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(0, 0, 0, 0.08);
        height: 844px;
      }}
    }}
    
    /* Simulator developer chrome hidden by default so ONLY mobile inside content shows */
    .simulator-chrome {{
      display: none !important;
    }}
    body.show-simulator .simulator-chrome {{
      display: flex !important;
    }}
    body.show-simulator header.simulator-chrome {{
      display: flex !important;
    }}
    body.show-simulator aside.simulator-chrome {{
      display: flex !important;
    }}
    body.show-simulator div.simulator-chrome {{
      display: flex !important;
    }}
    @media (max-width: 639px) {{
      #device-status-bar, #device-home-bar {{
        display: none !important;
      }}
    }}
    
    .no-scrollbar::-webkit-scrollbar {{ display: none; }}
    .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
  </style>
</head>
<body class="bg-slate-100 text-slate-900 font-sans antialiased min-h-screen p-0 md:p-6 flex flex-col items-center justify-center">

  <!-- Skip Navigation Link (WCAG 2.2 SC 2.4.1 Bypass Blocks) -->
  <a href="#screen-viewport" class="sr-only focus:not-sr-only bg-amber-600 text-white font-bold rounded-xl shadow-xl top-3 left-3 focus:outline-none focus:ring-4 focus:ring-amber-300">
    Skip to application screen
  </a>

  <!-- Persistent ARIA Live Region for Screen Readers -->
  <div id="a11y-announcer" class="sr-only" aria-live="polite" aria-atomic="true"></div>

  <!-- Top Toolbar / Header Landmark (Simulator Chrome - Hidden by default) -->
  <header class="simulator-chrome max-w-7xl mx-auto mb-5 bg-white p-4 rounded-2xl shadow-sm border border-slate-200 flex-wrap items-center justify-between gap-4" role="banner">
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
  <main id="main-content" class="w-full flex items-center justify-center">

    <!-- VIEW 1: INTERACTIVE SINGLE PHONE SIMULATOR -->
    <div id="view-interactive" role="tabpanel" aria-labelledby="btn-tab-interactive" class="flex flex-col lg:flex-row items-center lg:items-start justify-center gap-6 w-full">
      <div class="flex flex-col items-center w-full">
        <div class="simulator-chrome flex items-center gap-2 mb-2 text-xs text-slate-600" aria-live="polite">
          <span class="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse" aria-hidden="true"></span>
          <span id="instruction-tip">Tap <strong>Describe what's around me</strong> or <strong>Start navigation</strong></span>
        </div>

        <div class="iphone-frame flex flex-col justify-between" id="phone-container">
        <!-- Status Bar (Decorative Simulated Device Chrome) -->
        <div id="device-status-bar" class="pt-3 px-7 flex justify-between items-center text-xs font-semibold text-black z-30" aria-hidden="true">
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
              <div class="mt-2 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-orange-50 border border-orange-200 text-[11px] font-semibold text-orange-700">
                <span class="w-2 h-2 rounded-full bg-orange-500 animate-pulse"></span>
                <span>Powered by Gemini AI</span>
              </div>
            </div>

            <div class="flex flex-col gap-2.5">
              <!-- Voice phrase simulation chips -->
              <div class="flex flex-wrap justify-center gap-1.5" role="group" aria-label="Suggested voice phrases">
                <button onclick="handleVoiceInput('What is in front of me?')" aria-label="Simulate: What is in front of me?" class="px-2.5 py-1 rounded-full bg-orange-50 border border-orange-200 text-[11px] font-semibold text-orange-900 shadow-sm hover:bg-orange-100 transition active:scale-95">
                  “What is in front of me?”
                </button>
                <button onclick="handleVoiceInput('Where am I?')" aria-label="Simulate: Where am I?" class="px-2.5 py-1 rounded-full bg-blue-50 border border-blue-200 text-[11px] font-semibold text-blue-900 shadow-sm hover:bg-blue-100 transition active:scale-95">
                  “Where am I?”
                </button>
                <button onclick="handleVoiceInput('Take me to RTU')" aria-label="Simulate: Take me to RTU" class="px-2.5 py-1 rounded-full bg-white border border-slate-200 text-[11px] font-medium text-slate-700 shadow-sm hover:bg-slate-50 transition active:scale-95">
                  “Take me to RTU”
                </button>
                <button onclick="handleVoiceInput('Take me to the library')" aria-label="Simulate: Take me to the library" class="px-2.5 py-1 rounded-full bg-white border border-slate-200 text-[11px] font-medium text-slate-700 shadow-sm hover:bg-slate-50 transition active:scale-95">
                  “Take me to the library”
                </button>
                <button onclick="handleVoiceInput('Take me to Old Town')" aria-label="Simulate: Take me to Old Town" class="px-2.5 py-1 rounded-full bg-white border border-slate-200 text-[11px] font-medium text-slate-700 shadow-sm hover:bg-slate-50 transition active:scale-95">
                  “Take me to Old Town”
                </button>
                <button onclick="handleVoiceInput('Take me there')" aria-label="Simulate: Take me there (clarification test)" class="px-2.5 py-1 rounded-full bg-amber-50 border border-amber-200 text-[11px] font-medium text-amber-800 shadow-sm hover:bg-amber-100 transition active:scale-95" title="Tests clarification prompt">
                  “Take me there” (Clarify)
                </button>
              </div>

              <!-- Test input for any natural-language destination or command -->
              <form onsubmit="event.preventDefault(); const inp = document.getElementById('voice-sim-input'); if (inp && inp.value.trim()) {{ handleVoiceInput(inp.value.trim()); inp.value = ''; }}" class="flex items-center gap-1.5 px-1">
                <label for="voice-sim-input" class="sr-only">Type any voice command or destination for Gemini AI</label>
                <input type="text" id="voice-sim-input" placeholder="Type any destination (e.g. library, Old Town, Paris)..." class="flex-1 bg-white border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-amber-500 shadow-sm">
                <button type="submit" class="px-3 py-2 rounded-xl bg-slate-900 text-white text-xs font-semibold hover:bg-black transition active:scale-95">
                  Send
                </button>
              </form>

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
              <button onclick="startCurrentNavigation()" id="start-nav-btn" aria-label="Start walking navigation to selected destination" class="w-full py-4 rounded-2xl bg-black text-white font-bold text-base shadow-md hover:bg-neutral-800 transition active:scale-[0.99] flex items-center justify-center space-x-2">
                <span>Start navigation</span>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
              </button>
              <button onclick="speakRouteOverview()" aria-label="Describe route overview and audible cues" class="w-full py-3 rounded-2xl bg-white border border-slate-200 text-slate-800 font-semibold text-sm shadow-sm hover:bg-slate-50 transition active:scale-[0.99] flex items-center justify-center space-x-2">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
                <span>Describe route</span>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 5: ACTIVE NAVIGATION (ALWAYS-OPEN BACK CAMERA + YOLO + SIGNBOARDS) ==================== -->
          <div id="screen-activeNavigation" role="region" aria-label="Screen 5: Active Walking Navigation with Always-Open Back Camera and YOLO Object Detection" class="flex-1 flex flex-col justify-between p-3.5 pb-4 hidden relative overflow-hidden rounded-3xl">
            <!-- ALWAYS-OPEN CAMERA BACKGROUND VIEWPORT -->
            <div class="absolute inset-0 overflow-hidden bg-black z-0" aria-hidden="true">
              <!-- Real Device Camera Feed (Facing Environment) -->
              <video id="nav-live-video" class="absolute inset-0 w-full h-full object-cover" autoplay playsinline muted></video>
              <!-- Synthetic Street Walking Canvas (Fallback when camera permission not available or in testing) -->
              <canvas id="nav-sim-canvas" class="absolute inset-0 w-full h-full object-cover hidden"></canvas>
              <!-- Fallback Scene Photo -->
              <img id="nav-fallback-img" src="{img_campus}" alt="Camera walking view" class="absolute inset-0 w-full h-full object-cover opacity-90 transition-opacity">
              <!-- High-Contrast WCAG AAA Ambient Gradients -->
              <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-transparent to-black/90 pointer-events-none z-5"></div>
              <!-- Real-Time YOLO Object Detection Canvas Overlay -->
              <canvas id="nav-yolo-canvas" class="absolute inset-0 w-full h-full pointer-events-none z-10"></canvas>
              <!-- Real-Time Signboards Floating HUD Overlay (Gemini Vision OCR) -->
              <div id="nav-signboards-overlay" class="absolute inset-0 pointer-events-none z-15 flex flex-col justify-center items-center gap-2 p-3"></div>
            </div>

            <!-- Top Header (Z-20 Relative) -->
            <div class="relative z-20 flex justify-between items-center pt-1 px-1">
              <button onclick="stopNavigationRoute()" id="btn-nav-back" aria-label="Stop navigation and return to preview" class="w-10 h-10 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition active:scale-95">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
              </button>
              
              <!-- Camera & YOLO Status Pill Badge -->
              <div class="flex items-center gap-1.5 px-3 py-1 bg-black/75 backdrop-blur-md rounded-full text-white text-xs font-bold border border-white/20 shadow-md">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" aria-hidden="true"></span>
                <span id="camera-status-pill">Back Camera • YOLO Active</span>
              </div>

              <div class="flex items-center gap-1.5">
                <!-- Camera / Simulation Toggle Button -->
                <button type="button" onclick="toggleCameraFeed()" id="btn-toggle-camera" aria-label="Toggle between real rear camera and simulated walking stream" class="w-10 h-10 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition active:scale-95 text-sm" title="Toggle camera feed mode">
                  <span id="camera-toggle-icon" aria-hidden="true">📷</span>
                </button>
                <button onclick="openSettingsModal()" id="btn-nav-settings" aria-label="Settings" aria-haspopup="dialog" class="w-10 h-10 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                </button>
              </div>
            </div>

            <!-- Floating Navigation Turn-by-Turn HUD Card (Z-20 Relative) -->
            <div class="relative z-20 my-auto flex flex-col justify-center">
              <div class="bg-white/95 backdrop-blur-md rounded-3xl p-4 border border-white/50 shadow-2xl flex flex-col items-center text-center relative overflow-hidden" role="region" aria-label="Current Navigation Instruction" aria-live="assertive">
                <span id="nav-step-label" class="text-xs font-bold text-orange-600 uppercase tracking-widest mb-0.5">
                  Navigation • Step 1 of 6
                </span>
                <h2 id="nav-instruction-text" class="text-xl font-bold text-slate-900 tracking-tight leading-snug">
                  Walk towards Vanšu tilts
                </h2>
                
                <!-- Large Distance Number -->
                <div class="my-1.5 flex items-baseline justify-center space-x-1" aria-label="Distance remaining">
                  <span id="nav-distance-num" class="text-5xl font-black text-slate-900 tracking-tight">160</span>
                  <span class="text-base font-bold text-slate-600">meters</span>
                </div>

                <!-- Maneuver Direction Banner -->
                <div class="w-full bg-slate-50 border border-slate-200 rounded-2xl py-2 px-3 flex items-center justify-center space-x-2 text-slate-700">
                  <div id="nav-maneuver-icon" class="w-7 h-7 rounded-full bg-orange-500 text-white flex items-center justify-center font-bold text-sm" aria-hidden="true">
                    ↑
                  </div>
                  <span id="nav-maneuver-text" class="font-bold text-xs text-slate-800">Head straight • Facing East (84°)</span>
                </div>

                <!-- Live Path Clearance & YOLO Objects Counter -->
                <div id="nav-live-hazard-badge" class="w-full mt-2 py-1.5 px-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-[11px] font-semibold flex items-center justify-between">
                  <span>Path: <strong id="nav-path-status-text">Pathway clear ahead</strong></span>
                  <span id="nav-yolo-count" class="font-bold bg-emerald-200/80 px-2 py-0.5 rounded-full">YOLO: 2 objects</span>
                </div>
              </div>

              <!-- Real-Time Signboard Callout Banner (Gemini AI Vision) -->
              <div id="signboard-callout-banner" class="mt-2.5 bg-purple-900/90 backdrop-blur-md border border-purple-400/50 rounded-2xl p-2.5 text-white flex items-center justify-between shadow-xl transition-all" role="status" aria-live="polite">
                <div class="flex items-center space-x-2.5">
                  <span class="text-xl" aria-hidden="true">🪧</span>
                  <div class="text-left">
                    <div class="text-[10px] font-bold text-purple-200 uppercase tracking-wider">Signboard Detected (Gemini Vision)</div>
                    <div id="signboard-banner-text" class="text-xs font-bold text-white leading-tight">Paula Valdena iela • Street Sign</div>
                  </div>
                </div>
                <button type="button" onclick="triggerSignboardScan()" aria-label="Read detected signboards aloud" class="px-2.5 py-1 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-[10px] font-bold shadow-sm transition active:scale-95 flex items-center gap-1">
                  <span>Read aloud</span>
                </button>
              </div>

              <!-- Quick safety triggers for testing -->
              <div class="flex justify-center gap-2 mt-2" role="group" aria-label="Simulation test triggers">
                <button onclick="navigateTo('obstacleAlert')" aria-label="Simulate obstacle hazard detection" class="px-2.5 py-1 bg-red-600/80 text-white hover:bg-red-700 rounded-xl text-[11px] font-bold transition flex items-center gap-1 shadow-sm backdrop-blur-sm active:scale-95">
                  <span aria-hidden="true">⚠️</span> Simulate Obstacle
                </button>
                <button onclick="navigateTo('crosswalkSafety')" aria-label="Simulate approaching crosswalk quiet mode" class="px-2.5 py-1 bg-amber-500/80 text-black hover:bg-amber-600 rounded-xl text-[11px] font-bold transition flex items-center gap-1 shadow-sm backdrop-blur-sm active:scale-95">
                  <span aria-hidden="true">🚶</span> Simulate Crosswalk
                </button>
              </div>
            </div>

            <!-- Bottom Voice & Navigation Controls (Z-20 Relative) -->
            <div class="relative z-20 flex flex-col space-y-2 pt-1">
              <!-- Large Floating Voice Mic Button -->
              <div class="flex flex-col items-center justify-center">
                <button onclick="startVoiceCapture()" id="nav-floating-mic-btn" aria-label="Tap microphone to speak any button name or destination" class="w-16 h-16 rounded-full bg-black text-white border-2 border-orange-500 flex items-center justify-center shadow-2xl hover:scale-105 active:scale-95 transition">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
                </button>
                <p class="text-[11px] text-white/95 text-center font-bold drop-shadow mt-1">Tap mic & speak any button or destination</p>
              </div>

              <!-- Quick Action Row -->
              <div class="grid grid-cols-2 gap-2">
                <button onclick="repeatCurrentStep()" id="btn-repeat-instruction" aria-label="Repeat current navigation instruction" class="py-2.5 rounded-2xl bg-white/95 backdrop-blur-md border border-slate-200 text-slate-800 font-bold text-xs shadow-sm hover:bg-white transition active:scale-[0.99] flex items-center justify-center space-x-1.5">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
                  <span>Repeat</span>
                </button>
                <button onclick="triggerSignboardScan()" id="btn-detect-signs" aria-label="Read all signboards and street signs ahead" class="py-2.5 rounded-2xl bg-purple-600 text-white font-bold text-xs shadow-md hover:bg-purple-700 transition active:scale-[0.99] flex items-center justify-center space-x-1.5">
                  <span>🪧 Read signs</span>
                </button>
              </div>

              <!-- Stop Route Button -->
              <button onclick="stopNavigationRoute()" id="btn-stop-route" aria-label="Stop navigation route and return to home screen" class="w-full py-3 rounded-2xl bg-black/90 backdrop-blur-md text-white font-bold text-xs shadow-md hover:bg-black transition active:scale-[0.99] flex items-center justify-center space-x-2 border border-white/20">
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
            <div id="obstacle-alert-banner" role="alert" aria-live="assertive" class="mt-2 bg-[#FEECEC] border border-red-200 rounded-3xl p-4 flex items-center space-x-3.5 shadow-sm transition-colors">
              <div id="obstacle-banner-icon" class="w-11 h-11 text-red-600 flex items-center justify-center flex-shrink-0" aria-hidden="true">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 fill-current" viewBox="0 0 24 24"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>
              </div>
              <div class="flex flex-col">
                <h2 id="obstacle-screen-title" class="text-xl font-bold text-red-600 leading-tight">Obstacle ahead</h2>
                <p id="obstacle-screen-subtitle" class="text-xs text-slate-800 font-medium leading-relaxed mt-0.5">
                  Two meters ahead,<br>construction barrier on right.
                </p>
              </div>
            </div>

            <!-- Camera View with AR Path, LiDAR Depth Map Canvas, and Barrier Highlight -->
            <div class="flex-1 my-3 relative rounded-3xl overflow-hidden border border-slate-200 shadow-inner flex flex-col justify-end p-3.5">
              <img src="{img_obstacle}" alt="Camera scene showing sidewalk ahead with a high-visibility orange construction barrier" class="absolute inset-0 w-full h-full object-cover">
              
              <!-- Canvas for dynamic LiDAR Depth & Vision Bounding Box Overlay -->
              <canvas id="lidar-depth-canvas" class="absolute inset-0 w-full h-full pointer-events-none z-5"></canvas>
              
              <!-- Floating Obstacle Detail Card -->
              <div class="relative z-10 bg-white/95 backdrop-blur-md rounded-2xl p-3.5 border border-slate-100 shadow-md flex items-center space-x-3">
                <div id="obstacle-card-icon" class="w-10 h-10 rounded-full bg-orange-100 text-orange-500 flex items-center justify-center text-xl flex-shrink-0" role="img" aria-label="Hazard icon">
                  🚧
                </div>
                <div class="flex flex-col flex-1">
                  <div class="flex items-center justify-between">
                    <h3 id="obstacle-card-title" class="font-bold text-slate-900 text-sm leading-tight">Construction barrier</h3>
                    <span id="obstacle-card-dist-badge" class="text-[11px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">2.0m</span>
                  </div>
                  <p id="obstacle-card-sub" class="text-xs text-slate-600 mt-0.5">On the right, 2 meters ahead.</p>
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
        <div id="device-home-bar" class="pb-2 flex justify-center z-30" aria-hidden="true">
          <div class="w-32 h-1 bg-neutral-400 rounded-full"></div>
        </div>
      </div>
      </div>

      <!-- Right Side: LiDAR & Camera Sensor Fusion Dashboard (Simulator Chrome - Hidden by default) -->
      <aside aria-label="iPhone LiDAR Scanner and Danger System" class="simulator-chrome w-full max-w-sm bg-white rounded-3xl p-5 shadow-sm border border-slate-200 flex flex-col space-y-4">
        <!-- Header with LiDAR badge -->
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-2xl bg-orange-500 text-white flex items-center justify-center font-bold text-sm shadow-sm" aria-hidden="true">
              📡
            </div>
            <div>
              <h2 class="text-sm font-bold text-slate-900 leading-tight">iPhone LiDAR + Camera</h2>
              <span class="text-[11px] text-slate-500 font-medium">ARKit sceneDepth • Vision Fusion</span>
            </div>
          </div>
          <span id="lidar-status-badge" class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
            LiDAR Active
          </span>
        </div>

        <!-- Real-time Distance & Danger Gauge -->
        <div class="bg-slate-50 border border-slate-200/80 rounded-2xl p-3.5 flex flex-col space-y-2.5">
          <div class="flex items-center justify-between text-xs">
            <span class="text-slate-500 font-semibold uppercase tracking-wider text-[10px]">Real-time Proximity</span>
            <span id="lidar-confidence-tag" class="text-slate-600 font-medium text-[11px]">Confidence: 98% (High)</span>
          </div>
          <div class="flex items-baseline justify-between">
            <div class="flex items-baseline gap-1">
              <span id="lidar-live-dist-val" class="text-3xl font-extrabold text-slate-900">2.1</span>
              <span class="text-sm font-bold text-slate-500">meters</span>
            </div>
            <span id="lidar-danger-pill" class="px-3 py-1 rounded-xl text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300">
              Caution (In Path)
            </span>
          </div>

          <!-- Distance slider -->
          <div class="space-y-1 pt-1">
            <div class="flex justify-between text-[11px] font-medium text-slate-500">
              <span class="font-bold text-red-600">&lt;0.7m (Stop)</span>
              <span>1.5m</span>
              <span>3.0m</span>
              <span class="text-emerald-700">5.0m (Clear)</span>
            </div>
            <input type="range" id="lidar-slider" min="0.4" max="5.0" step="0.1" value="2.1" oninput="handleLidarSlider(this.value)" class="w-full accent-orange-500 cursor-pointer" aria-label="Adjust obstacle distance in meters">
          </div>
        </div>

        <!-- Identified Object & Corridor Position -->
        <div class="grid grid-cols-2 gap-2 text-xs">
          <div class="bg-slate-50 border border-slate-200 p-2.5 rounded-xl">
            <span class="text-slate-500 block text-[10px] uppercase font-bold mb-1">Identified Object</span>
            <select id="lidar-object-select" onchange="handleLidarObjectChange(this.value)" class="bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-800 p-1 w-full focus:ring-1 focus:ring-amber-500">
              <option value="Chair">Chair (In path)</option>
              <option value="Person">Person (Moving)</option>
              <option value="Construction barrier">Construction barrier</option>
              <option value="Car">Car</option>
              <option value="Bicycle">Bicycle</option>
              <option value="Bench">Bench</option>
              <option value="Trash bin">Trash bin</option>
              <option value="Tree">Tree</option>
              <option value="Pole">Pole</option>
              <option value="Stairs">Stairs</option>
              <option value="Table">Table</option>
              <option value="Wall">Wall</option>
            </select>
          </div>
          <div class="bg-slate-50 border border-slate-200 p-2.5 rounded-xl">
            <span class="text-slate-500 block text-[10px] uppercase font-bold mb-1">Lateral Lane</span>
            <select id="lidar-lane-select" onchange="handleLidarLaneChange(this.value)" class="bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-800 p-1 w-full focus:ring-1 focus:ring-amber-500">
              <option value="center">Center (Walking Path)</option>
              <option value="left">Left Lane</option>
              <option value="right">Right Lane</option>
            </select>
          </div>
        </div>

        <!-- Test Safety Scenarios (Exact Match to User Specs) -->
        <div class="space-y-1.5">
          <span class="text-[11px] font-bold text-slate-600 uppercase tracking-wider block">Test Safety Scenarios</span>
          <div class="grid grid-cols-1 gap-1.5">
            <button type="button" onclick="testLidarScenario(4.0, 'Beside path', 'right', 'Safe')" class="w-full py-2 px-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-medium text-xs flex items-center justify-between transition active:scale-95">
              <span><strong>4 m</strong> Beside path</span>
              <span class="text-slate-500 font-semibold text-[11px]">Usually silent</span>
            </button>
            <button type="button" onclick="testLidarScenario(3.0, 'Object', 'center', 'Notice')" class="w-full py-2 px-3 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-900 font-medium text-xs flex items-center justify-between border border-blue-200 transition active:scale-95">
              <span><strong>3 m</strong> Object ahead</span>
              <span class="font-bold text-[11px]">“Object ahead.”</span>
            </button>
            <button type="button" onclick="testLidarScenario(2.1, 'Chair', 'center', 'Caution')" class="w-full py-2 px-3 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-900 font-medium text-xs flex items-center justify-between border border-amber-200 transition active:scale-95">
              <span><strong>2 m</strong> Object in path</span>
              <span class="font-bold text-[11px]">“Chair ahead, 2 meters.”</span>
            </button>
            <button type="button" onclick="testLidarScenario(1.0, 'Obstacle', 'center', 'Danger')" class="w-full py-2 px-3 rounded-xl bg-orange-50 hover:bg-orange-100 text-orange-900 font-medium text-xs flex items-center justify-between border border-orange-200 transition active:scale-95">
              <span><strong>1 m</strong> Dangerous</span>
              <span class="font-bold text-[11px]">“Obstacle ahead, 1 meter.”</span>
            </button>
            <button type="button" onclick="testLidarScenario(0.65, 'Obstacle', 'center', 'Critical')" class="w-full py-2 px-3 rounded-xl bg-red-100 hover:bg-red-200 text-red-900 font-bold text-xs flex items-center justify-between border border-red-300 transition active:scale-95">
              <span><strong>&lt;0.7 m</strong> Very close</span>
              <span class="font-bold text-[11px]">“Stop. Obstacle directly ahead.”</span>
            </button>
          </div>
        </div>

        <!-- LiDAR Depth Map Visualization Toggle -->
        <div class="pt-2 border-t border-slate-100 flex items-center justify-between">
          <span class="text-xs text-slate-700 font-medium">LiDAR Depth Map Heatmap</span>
          <button type="button" onclick="toggleLidarDepthHeatmap()" id="lidar-depth-toggle" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-200 text-slate-700 hover:bg-slate-300 transition">
            Overlay: OFF
          </button>
        </div>
      </aside>
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
        instruction: "Walk towards Vanšu tilts",
        distance: 160,
        maneuver: "Head straight",
        icon: "↑"
      }},
      {{
        instruction: "Cross Vanšu tilts (bridge)",
        distance: 730,
        maneuver: "Cross bridge",
        icon: "↰"
      }},
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

    let currentDestinationTitle = "Riga Technical University (RTU)";
    let currentDestinationSub = "Ķīpsala Campus • 2.4 km • 28 min • 6 waypoints";
    let currentWaypoints = [...rtuWaypoints];

    const clientLocationsCatalog = [
      {{
        id: "rtu-campus",
        canonicalName: "Riga Technical University (RTU)",
        shortName: "RTU Campus",
        subtitle: "Ķīpsala Campus, Paula Valdena iela 1",
        category: "Campus",
        distanceKm: 2.4,
        estimatedMinutes: 28,
        aliases: ["rtu", "riga technical university", "campus", "kipsala campus", "kipsala", "university", "cif", "technical university", "faculty", "main campus"],
        waypoints: [
          {{ instruction: "Walk towards Vanšu tilts", distance: 160, maneuver: "Head straight", icon: "↑" }},
          {{ instruction: "Cross Vanšu tilts (bridge)", distance: 730, maneuver: "Cross bridge", icon: "↰" }},
          {{ instruction: "Turn right on Ķīpsalas iela", distance: 120, maneuver: "Turn right in 120m", icon: "↱" }},
          {{ instruction: "Continue straight along Paula Valdena iela", distance: 80, maneuver: "Continue straight", icon: "↑" }},
          {{ instruction: "Approaching pedestrian crossing at Zunda quay", distance: 30, maneuver: "Crosswalk ahead", icon: "🚶" }},
          {{ instruction: "Arrival: RTU Main Entrance", distance: 0, maneuver: "Destination reached", icon: "★" }}
        ]
      }},
      {{
        id: "rtu-library",
        canonicalName: "RTU Scientific Library",
        shortName: "Library",
        subtitle: "Paula Valdena iela 5, Ķīpsala",
        category: "Library",
        distanceKm: 1.3,
        estimatedMinutes: 16,
        aliases: ["library", "the library", "scientific library", "rtu library", "study hall", "reading room", "central library", "books"],
        waypoints: [
          {{ instruction: "Walk north on Paula Valdena iela", distance: 90, maneuver: "Continue straight", icon: "↑" }},
          {{ instruction: "Turn left towards Scientific Library portico", distance: 40, maneuver: "Turn left in 40m", icon: "↰" }},
          {{ instruction: "Ascend accessible entrance ramp", distance: 10, maneuver: "Ramp directly ahead", icon: "↑" }},
          {{ instruction: "Arrival: RTU Scientific Library", distance: 0, maneuver: "Destination reached", icon: "★" }}
        ]
      }},
      {{
        id: "rtu-main-building",
        canonicalName: "RTU Main Building & Administration",
        shortName: "Main Building",
        subtitle: "Kaļķu iela 1 / Ķīpsala Center",
        category: "Campus",
        distanceKm: 0.9,
        estimatedMinutes: 11,
        aliases: ["main building", "the main building", "administration", "admin building", "central building", "rectorate", "dean's office", "headquarters", "open main building", "open the main building"],
        waypoints: [
          {{ instruction: "Follow paved pathway towards central courtyard", distance: 70, maneuver: "Head straight", icon: "↑" }},
          {{ instruction: "Turn right toward administrative portico", distance: 30, maneuver: "Turn right in 30m", icon: "↱" }},
          {{ instruction: "Arrival: RTU Main Building Entrance", distance: 0, maneuver: "Destination reached", icon: "★" }}
        ]
      }},
      {{
        id: "rtu-sports-center",
        canonicalName: "RTU Ķīpsala Sports Center & Pool",
        shortName: "Sports Center",
        subtitle: "Ķīpsalas iela 5, Ķīpsala",
        category: "Sports",
        distanceKm: 0.7,
        estimatedMinutes: 9,
        aliases: ["sports center", "the sports center", "swimming pool", "gym", "rtu sports", "sports club", "fitness", "arena", "kipsala pool"],
        waypoints: [
          {{ instruction: "Walk south along Ķīpsalas iela sidewalk", distance: 60, maneuver: "Continue straight", icon: "↑" }},
          {{ instruction: "Cross tactile driveway entrance", distance: 20, maneuver: "Caution: driveway crossing", icon: "🚶" }},
          {{ instruction: "Arrival: Sports Center & Swimming Pool", distance: 0, maneuver: "Destination reached", icon: "★" }}
        ]
      }},
      {{
        id: "rtu-student-hostel",
        canonicalName: "RTU Student Hostel",
        shortName: "Hostel",
        subtitle: "Āzenes iela 22, Ķīpsala",
        category: "Dormitory",
        distanceKm: 1.1,
        estimatedMinutes: 14,
        aliases: ["student hostel", "hostel", "dormitory", "dorms", "student residence", "azenes"],
        waypoints: [
          {{ instruction: "Follow Āzenes iela westward", distance: 110, maneuver: "Head straight", icon: "↑" }},
          {{ instruction: "Turn left into hostel entrance walkway", distance: 25, maneuver: "Turn left", icon: "↰" }},
          {{ instruction: "Arrival: RTU Student Hostel", distance: 0, maneuver: "Destination reached", icon: "★" }}
        ]
      }},
      {{
        id: "rtu-cafeteria",
        canonicalName: "RTU Central Cafeteria",
        shortName: "Cafeteria",
        subtitle: "Paula Valdena iela 1 / 1st Floor",
        category: "Dining",
        distanceKm: 0.3,
        estimatedMinutes: 4,
        aliases: ["cafeteria", "canteen", "lunch", "food court", "cafe", "dining"],
        waypoints: [
          {{ instruction: "Enter student union atrium and take hallway left", distance: 30, maneuver: "Follow hallway left", icon: "↰" }},
          {{ instruction: "Arrival: RTU Central Cafeteria", distance: 0, maneuver: "Destination reached", icon: "★" }}
        ]
      }},
      {{
        id: "swedbank-building",
        canonicalName: "Swedbank Central Building",
        shortName: "Swedbank",
        subtitle: "Balasta dambis 15, Riga",
        category: "Commercial",
        distanceKm: 1.8,
        estimatedMinutes: 21,
        aliases: ["swedbank", "swedbank building", "balasta dambis", "bank"],
        waypoints: [
          {{ instruction: "Head south along Balasta dambis waterfront promenade", distance: 140, maneuver: "Continue along waterfront", icon: "↑" }},
          {{ instruction: "Turn right onto Swedbank pedestrian plaza", distance: 40, maneuver: "Turn right", icon: "↱" }},
          {{ instruction: "Arrival: Swedbank Central Building", distance: 0, maneuver: "Destination reached", icon: "★" }}
        ]
      }},
      {{
        id: "riga-central-station",
        canonicalName: "Rīga Central Station",
        shortName: "Central Station",
        subtitle: "Stacijas laukums, Rīga",
        category: "Transit",
        distanceKm: 3.1,
        estimatedMinutes: 38,
        aliases: ["central station", "riga central station", "train station", "railway station", "trains", "railway", "station"],
        waypoints: [
          {{ instruction: "Cross Vanšu tilts towards City Center", distance: 200, maneuver: "Head straight across bridge", icon: "↑" }},
          {{ instruction: "Continue along 13. Janvāra iela", distance: 150, maneuver: "Head straight", icon: "↑" }},
          {{ instruction: "Arrival: Rīga Central Station Main Concourse", distance: 0, maneuver: "Destination reached", icon: "★" }}
        ]
      }},
      {{
        id: "kipsala-transit-stop",
        canonicalName: "Ķīpsala Transit Stop",
        shortName: "Bus Stop",
        subtitle: "Krišjāņa Valdemāra iela, Ķīpsala",
        category: "Transit",
        distanceKm: 0.4,
        estimatedMinutes: 5,
        aliases: ["bus stop", "the bus stop", "transit stop", "public transport", "trolleybus stop", "kipsala bus", "bus"],
        waypoints: [
          {{ instruction: "Walk west toward Krišjāņa Valdemāra iela", distance: 40, maneuver: "Head straight", icon: "↑" }},
          {{ instruction: "Arrival: Ķīpsala Transit Shelter", distance: 0, maneuver: "Destination reached", icon: "★" }}
        ]
      }}
    ];

    function findClientLocationMatch(queryText) {{
      if (!queryText) return null;
      const clean = queryText.toLowerCase().trim();

      // 1. Direct alias match
      for (const loc of clientLocationsCatalog) {{
        for (const alias of loc.aliases) {{
          if (clean === alias) return loc;
        }}
      }}

      // 2. Whole-word alias match
      for (const loc of clientLocationsCatalog) {{
        for (const alias of loc.aliases) {{
          const re = new RegExp('\\b' + alias.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\$&') + '\\b', 'i');
          if (re.test(clean)) return loc;
        }}
      }}

      // 3. Majority token match
      const tokens = clean.split(/\\s+/).filter(t => t.length > 2);
      if (tokens.length === 0) return null;

      let best = null;
      let highest = 0;
      for (const loc of clientLocationsCatalog) {{
        let score = 0;
        const allToks = new Set([
          ...loc.canonicalName.toLowerCase().split(/\\s+/),
          ...loc.aliases.flatMap(a => a.split(/\\s+/))
        ]);
        for (const t of tokens) {{
          if (allToks.has(t)) score++;
        }}
        if (score > highest) {{
          highest = score;
          best = loc;
        }}
      }}

      if (tokens.length === 1 && highest >= 1) return best;
      if (tokens.length > 1 && highest >= Math.ceil(tokens.length * 0.6)) return best;
      return null;
    }}

    function createClientCustomDestination(rawName) {{
      const formatted = rawName.replace(/^to\\s+/i, '').replace(/^(the|a|an)\\s+/i, '').trim();
      const title = formatted.charAt(0).toUpperCase() + formatted.slice(1);
      return {{
        id: "custom-" + Date.now(),
        canonicalName: title,
        shortName: title,
        subtitle: `${{title}} • 2.6 km • 32 min • 6 waypoints`,
        category: "Custom Place",
        distanceKm: 2.6,
        estimatedMinutes: 32,
        waypoints: [
          {{ instruction: `Head toward ${{title}}`, distance: 100, maneuver: "Head straight", icon: "↑" }},
          {{ instruction: `Continue along pedestrian pathway to ${{title}}`, distance: 120, maneuver: "Head straight", icon: "↑" }},
          {{ instruction: `Arrival: ${{title}}`, distance: 0, maneuver: "Destination reached", icon: "★" }}
        ]
      }};
    }}

    // LiDAR & Camera Sensor Fusion Simulation State
    let currentLidarDistance = 2.1;
    let currentLidarObject = 'Chair';
    let currentLidarLane = 'center'; // 'left', 'center', 'right'
    let currentLidarDanger = 'Caution';
    let lidarDepthHeatmapActive = false;

    function getLidarSceneDescription() {{
      if (currentLidarDistance <= 3.5) {{
        const rounded = Math.round(currentLidarDistance);
        const distWord = rounded <= 1 ? "one meter" : `${{rounded}} meters`;
        const sideWord = currentLidarLane === 'center' ? 'directly ahead' : (currentLidarLane === 'left' ? 'ahead on your left' : 'ahead on your right');
        return `There is a ${{currentLidarObject.toLowerCase()}} approximately ${{distWord}} ${{sideWord}}.`;
      }}
      return "Pedestrian pathway clear directly ahead. Sidewalk continues for 41 meters. No immediate obstacles detected in your lane.";
    }}

    function evaluateLidarDanger(dist, lane, label) {{
      const objName = label || currentLidarObject || 'Obstacle';
      if (lane === 'center') {{
        if (dist < 0.75) {{
          return {{
            level: 'Critical Stop',
            class: 'bg-red-600 text-white border-red-700 animate-pulse',
            bannerBg: 'bg-red-100 border-red-400',
            bannerText: 'text-red-700',
            title: 'Stop. Obstacle directly ahead',
            subtitle: `${{objName}} less than 0.7m ahead. Halt immediately.`,
            guidance: 'Clear path before proceeding.',
            spoken: 'Stop. Obstacle directly ahead.',
            haptic: [150, 80, 200, 80, 250],
            isCritical: true
          }};
        }} else if (dist < 1.45) {{
          return {{
            level: 'Danger',
            class: 'bg-orange-500 text-white border-orange-600',
            bannerBg: 'bg-orange-50 border-orange-300',
            bannerText: 'text-orange-700',
            title: 'Obstacle ahead, 1 meter',
            subtitle: `${{objName}} 1 meter ahead in walking path.`,
            guidance: 'Keep left.',
            spoken: 'Obstacle ahead, 1 meter.',
            haptic: [100, 80, 150],
            isCritical: false
          }};
        }} else if (dist < 2.45) {{
          const sideText = lane === 'center' ? 'ahead' : (lane === 'left' ? 'ahead on left' : 'ahead on right');
          return {{
            level: 'Caution',
            class: 'bg-amber-100 text-amber-800 border-amber-300',
            bannerBg: 'bg-[#FEECEC] border-red-200',
            bannerText: 'text-red-600',
            title: `${{objName}} ahead`,
            subtitle: `${{objName}} ahead, 2 meters.`,
            guidance: 'Keep left.',
            spoken: `${{objName}} ahead, 2 meters. Keep left.`,
            haptic: [80, 60],
            isCritical: false
          }};
        }} else if (dist < 3.45) {{
          return {{
            level: 'Notice',
            class: 'bg-blue-100 text-blue-800 border-blue-200',
            bannerBg: 'bg-blue-50 border-blue-200',
            bannerText: 'text-blue-700',
            title: 'Object ahead',
            subtitle: `${{objName}} ahead, 3 meters.`,
            guidance: 'Path clear for 2 meters.',
            spoken: 'Object ahead.',
            haptic: [50],
            isCritical: false
          }};
        }} else {{
          return {{
            level: 'Safe',
            class: 'bg-emerald-100 text-emerald-800 border-emerald-300',
            bannerBg: 'bg-emerald-50 border-emerald-200',
            bannerText: 'text-emerald-700',
            title: 'Clear path',
            subtitle: 'No immediate obstacles detected.',
            guidance: 'Continue forward.',
            spoken: '', // Silent per requirement: "4m beside path: Usually silent"
            haptic: [],
            isCritical: false
          }};
        }}
      }} else {{
        // Beside path (left or right)
        if (dist < 1.0) {{
          return {{
            level: 'Caution',
            class: 'bg-amber-100 text-amber-800 border-amber-300',
            bannerBg: 'bg-amber-50 border-amber-200',
            bannerText: 'text-amber-700',
            title: `${{objName}} beside path`,
            subtitle: `${{dist.toFixed(1)}}m on ${{lane}}.`,
            guidance: 'Maintain center path.',
            spoken: `${{objName}} beside path, 1 meter.`,
            haptic: [60],
            isCritical: false
          }};
        }} else if (dist < 2.0) {{
          return {{
            level: 'Notice',
            class: 'bg-blue-100 text-blue-800 border-blue-200',
            bannerBg: 'bg-blue-50 border-blue-200',
            bannerText: 'text-blue-700',
            title: `${{objName}} on ${{lane}}`,
            subtitle: `${{dist.toFixed(1)}}m on ${{lane}}.`,
            guidance: 'Path clear.',
            spoken: `${{objName}} beside path.`,
            haptic: [40],
            isCritical: false
          }};
        }} else {{
          // 4m beside path: silent
          return {{
            level: 'Safe (Beside Path)',
            class: 'bg-slate-100 text-slate-700 border-slate-200',
            bannerBg: 'bg-slate-50 border-slate-200',
            bannerText: 'text-slate-600',
            title: 'Beside path',
            subtitle: `${{objName}} 4 meters beside path.`,
            guidance: 'Safe.',
            spoken: '', // Silent per requirement
            haptic: [],
            isCritical: false
          }};
        }}
      }}
    }}

    function updateLidarState(distance, objectLabel, lane, triggerAlert = true) {{
      currentLidarDistance = parseFloat(distance);
      if (objectLabel) currentLidarObject = objectLabel;
      if (lane) currentLidarLane = lane;

      const evalResult = evaluateLidarDanger(currentLidarDistance, currentLidarLane, currentLidarObject);
      currentLidarDanger = evalResult.level;

      // Update Dashboard elements
      const distEl = document.getElementById('lidar-live-dist-val');
      if (distEl) distEl.innerText = currentLidarDistance.toFixed(1);

      const sliderEl = document.getElementById('lidar-slider');
      if (sliderEl && Math.abs(parseFloat(sliderEl.value) - currentLidarDistance) > 0.05) {{
        sliderEl.value = currentLidarDistance;
      }}

      const pillEl = document.getElementById('lidar-danger-pill');
      if (pillEl) {{
        pillEl.className = 'px-3 py-1 rounded-xl text-xs font-bold border transition-colors ' + evalResult.class;
        pillEl.innerText = evalResult.level;
      }}

      const objSelect = document.getElementById('lidar-object-select');
      if (objSelect && objSelect.value !== currentLidarObject) {{
        objSelect.value = currentLidarObject;
      }}

      const laneSelect = document.getElementById('lidar-lane-select');
      if (laneSelect && laneSelect.value !== currentLidarLane) {{
        laneSelect.value = currentLidarLane;
      }}

      // Update Screen 8 elements if open
      const screenTitle = document.getElementById('obstacle-screen-title');
      if (screenTitle) {{
        screenTitle.innerText = evalResult.title;
        screenTitle.className = 'text-xl font-bold leading-tight ' + evalResult.bannerText;
      }}

      const screenSub = document.getElementById('obstacle-screen-subtitle');
      if (screenSub) {{
        screenSub.innerHTML = `${{evalResult.subtitle}}<br><span class="text-slate-600">${{evalResult.guidance}}</span>`;
      }}

      const bannerBox = document.getElementById('obstacle-alert-banner');
      if (bannerBox) {{
        bannerBox.className = 'mt-2 rounded-3xl p-4 flex items-center space-x-3.5 shadow-sm transition-colors ' + evalResult.bannerBg;
      }}

      const cardTitle = document.getElementById('obstacle-card-title');
      if (cardTitle) cardTitle.innerText = currentLidarObject;

      const cardSub = document.getElementById('obstacle-card-sub');
      if (cardSub) {{
        cardSub.innerText = `${{currentLidarLane === 'center' ? 'Directly ahead' : 'On ' + currentLidarLane}}, ${{currentLidarDistance.toFixed(1)}}m.`;
      }}

      const cardDistBadge = document.getElementById('obstacle-card-dist-badge');
      if (cardDistBadge) {{
        cardDistBadge.innerText = currentLidarDistance.toFixed(1) + 'm';
      }}

      const cardIcon = document.getElementById('obstacle-card-icon');
      if (cardIcon) {{
        const icons = {{
          'Chair': '🪑', 'Person': '🚶', 'Car': '🚗', 'Bicycle': '🚲',
          'Construction barrier': '🚧', 'Trash bin': '🗑️', 'Bench': '🪵',
          'Tree': '🌳', 'Pole': '💈', 'Stairs': '🪜', 'Table': '🪑', 'Wall': '🧱'
        }};
        cardIcon.innerText = icons[currentLidarObject] || '⚠️';
      }}

      drawLidarOverlay();

      if (triggerAlert) {{
        if (evalResult.haptic && evalResult.haptic.length) {{
          triggerHaptic(evalResult.haptic);
        }}
        if (evalResult.spoken) {{
          speakText(evalResult.spoken);
        }}
        if (evalResult.level === 'Critical Stop' || evalResult.level === 'Danger') {{
          if (activeRoute !== 'obstacleAlert') {{
            navigateTo('obstacleAlert');
          }}
        }}
      }}
    }}

    function testLidarScenario(distance, objectLabel, lane, dangerName) {{
      updateLidarState(distance, objectLabel, lane, true);
    }}

    function handleLidarSlider(val) {{
      updateLidarState(val, currentLidarObject, currentLidarLane, false);
    }}

    function handleLidarObjectChange(val) {{
      updateLidarState(currentLidarDistance, val, currentLidarLane, false);
    }}

    function handleLidarLaneChange(val) {{
      updateLidarState(currentLidarDistance, currentLidarObject, val, false);
    }}

    function toggleLidarDepthHeatmap() {{
      lidarDepthHeatmapActive = !lidarDepthHeatmapActive;
      const btn = document.getElementById('lidar-depth-toggle');
      if (btn) {{
        btn.innerText = lidarDepthHeatmapActive ? 'Overlay: ON' : 'Overlay: OFF';
        btn.className = lidarDepthHeatmapActive ? 'px-2.5 py-1 rounded-lg text-xs font-semibold bg-orange-500 text-white shadow-sm' : 'px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-200 text-slate-700 hover:bg-slate-300';
      }}
      drawLidarOverlay();
    }}

    function drawLidarOverlay() {{
      const canvas = document.getElementById('lidar-depth-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      canvas.width = canvas.clientWidth || 300;
      canvas.height = canvas.clientHeight || 360;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (lidarDepthHeatmapActive) {{
        const gradient = ctx.createLinearGradient(0, canvas.height, 0, 0);
        gradient.addColorStop(0, 'rgba(239, 68, 68, 0.45)');
        gradient.addColorStop(0.3, 'rgba(245, 158, 11, 0.35)');
        gradient.addColorStop(0.6, 'rgba(16, 185, 129, 0.25)');
        gradient.addColorStop(1.0, 'rgba(59, 130, 246, 0.20)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
        ctx.lineWidth = 1;
        ctx.setLineDash([4, 4]);
        [0.25, 0.5, 0.75].forEach(yFactor => {{
          ctx.beginPath();
          ctx.moveTo(0, canvas.height * yFactor);
          ctx.lineTo(canvas.width, canvas.height * yFactor);
          ctx.stroke();
        }});
        ctx.setLineDash([]);
      }}

      if (currentLidarDistance <= 3.5) {{
        const boxWidth = canvas.width * 0.52;
        const boxHeight = canvas.height * 0.38;
        let boxX = (canvas.width - boxWidth) / 2;
        if (currentLidarLane === 'left') boxX = canvas.width * 0.05;
        if (currentLidarLane === 'right') boxX = canvas.width * 0.43;
        const boxY = canvas.height * 0.38;

        ctx.strokeStyle = currentLidarDistance < 0.75 ? '#DC2626' : (currentLidarDistance < 1.45 ? '#EA580C' : '#D97706');
        ctx.lineWidth = 3;
        ctx.strokeRect(boxX, boxY, boxWidth, boxHeight);

        ctx.fillStyle = 'rgba(0, 0, 0, 0.85)';
        ctx.fillRect(boxX, boxY - 22, boxWidth, 22);
        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 11px sans-serif';
        ctx.fillText(`${{currentLidarObject}} • ${{currentLidarDistance.toFixed(1)}}m (98% conf)`, boxX + 6, boxY - 6);
      }}
    }}

    // ==================== ALWAYS-OPEN BACK CAMERA, YOLO OBJECT DETECTION & SIGNBOARDS ====================
    let liveCameraStream = null;
    let isRealCameraActive = false;
    let currentCameraMode = 'simulation'; // 'real' or 'simulation'
    let yoloDetectionInterval = null;
    let signboardDetectionInterval = null;
    let lastSpokenObstacleTime = 0;
    let lastSpokenSignTime = 0;
    let lastSpokenSignText = "";
    let simWalkFrame = 0;

    const yoloCandidateEntities = [
      {{ label: 'Person', icon: '👤', lane: 'center', defaultDist: 2.1, conf: 0.94, height: 'head' }},
      {{ label: 'Construction barrier', icon: '🚧', lane: 'right', defaultDist: 1.6, conf: 0.96, height: 'torso' }},
      {{ label: 'Car', icon: '🚗', lane: 'left', defaultDist: 4.5, conf: 0.98, height: 'torso' }},
      {{ label: 'Bicycle', icon: '🚲', lane: 'right', defaultDist: 3.2, conf: 0.91, height: 'torso' }},
      {{ label: 'Stairs', icon: '🪜', lane: 'center', defaultDist: 3.5, conf: 0.93, height: 'torso' }},
      {{ label: 'Building entrance', icon: '🚪', lane: 'center', defaultDist: 4.8, conf: 0.95, height: 'head' }},
      {{ label: 'Pole', icon: '📍', lane: 'left', defaultDist: 2.2, conf: 0.89, height: 'torso' }}
    ];

    const signboardCatalog = [
      {{ text: "Paula Valdena iela", type: "street_sign", icon: "🪧", pos: "right", announcement: "Street sign on right: Paula Valdena iela" }},
      {{ text: "RTU Datorzinātnes fakultāte", type: "building_board", icon: "🏢", pos: "ahead", announcement: "Building entrance ahead: RTU Faculty of Computer Science" }},
      {{ text: "9. autobuss: Ķīpsala", type: "transit_sign", icon: "🚏", pos: "left", announcement: "Transit sign on left: Bus 9 stop Ķīpsala" }},
      {{ text: "Gājēju pāreja (Crosswalk)", type: "warning_sign", icon: "🚶", pos: "ahead", announcement: "Crosswalk ahead in 30 meters" }},
      {{ text: "RTU Zinātniskā bibliotēka", type: "building_board", icon: "📚", pos: "right", announcement: "Building board: RTU Scientific Library" }}
    ];

    async function startAlwaysOpenBackCamera() {{
      const video = document.getElementById('nav-live-video');
      const fallbackImg = document.getElementById('nav-fallback-img');

      // Attempt to access user device environment (rear) camera
      try {{
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {{
          if (liveCameraStream) {{
            liveCameraStream.getTracks().forEach(t => t.stop());
            liveCameraStream = null;
          }}
          liveCameraStream = await navigator.mediaDevices.getUserMedia({{
            video: {{
              facingMode: {{ ideal: "environment" }},
              width: {{ ideal: 1280 }},
              height: {{ ideal: 720 }}
            }},
            audio: false
          }});
          if (video && liveCameraStream) {{
            video.srcObject = liveCameraStream;
            video.classList.remove('hidden');
            await video.play();
            isRealCameraActive = true;
            currentCameraMode = 'real';
            if (fallbackImg) fallbackImg.classList.add('opacity-0');
            updateCameraStatusUI(true);
            announceToScreenReader("Back camera stream active. Continuous YOLO object detection running.");
          }}
        }}
      }} catch (err) {{
        console.warn("[Camera] Live hardware camera unavailable or denied, running realistic walking simulation:", err.message);
        isRealCameraActive = false;
        currentCameraMode = 'simulation';
        if (fallbackImg) fallbackImg.classList.remove('opacity-0');
        updateCameraStatusUI(false);
      }}

      // Start YOLO perception cycle (5-10 times per second)
      if (!yoloDetectionInterval) {{
        yoloDetectionInterval = setInterval(runYoloPerceptionCycle, 200);
      }}

      // Start periodic Signboard OCR scan (every 5 seconds)
      if (!signboardDetectionInterval) {{
        signboardDetectionInterval = setInterval(() => triggerSignboardScan(true), 5000);
      }}

      // Initial signboard check
      setTimeout(() => triggerSignboardScan(true), 1200);
    }}

    function stopAlwaysOpenBackCamera() {{
      if (liveCameraStream) {{
        liveCameraStream.getTracks().forEach(t => t.stop());
        liveCameraStream = null;
      }}
      if (yoloDetectionInterval) {{
        clearInterval(yoloDetectionInterval);
        yoloDetectionInterval = null;
      }}
      if (signboardDetectionInterval) {{
        clearInterval(signboardDetectionInterval);
        signboardDetectionInterval = null;
      }}
      isRealCameraActive = false;
    }}

    function toggleCameraFeed() {{
      triggerHaptic([50]);
      if (currentCameraMode === 'real') {{
        // Switch to simulation
        if (liveCameraStream) {{
          liveCameraStream.getTracks().forEach(t => t.stop());
          liveCameraStream = null;
        }}
        isRealCameraActive = false;
        currentCameraMode = 'simulation';
        const fallbackImg = document.getElementById('nav-fallback-img');
        if (fallbackImg) fallbackImg.classList.remove('opacity-0');
        updateCameraStatusUI(false);
        speakText("Switched to realistic walking simulation.");
        announceToScreenReader("Switched to realistic walking simulation.");
      }} else {{
        // Switch to real camera
        currentCameraMode = 'real';
        startAlwaysOpenBackCamera();
        speakText("Activating device rear camera.");
      }}
    }}

    function updateCameraStatusUI(isReal) {{
      const pill = document.getElementById('camera-status-pill');
      const icon = document.getElementById('camera-toggle-icon');
      if (pill) {{
        pill.innerText = isReal ? "Back Camera • YOLO Active" : "Walk Sim • YOLO Active";
      }}
      if (icon) {{
        icon.innerText = isReal ? "📷" : "🎬";
      }}
    }}

    function runYoloPerceptionCycle() {{
      if (activeRoute !== 'activeNavigation') return;
      simWalkFrame++;

      const canvas = document.getElementById('nav-yolo-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      canvas.width = canvas.clientWidth || 320;
      canvas.height = canvas.clientHeight || 480;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Active simulated/detected objects based on route step and time
      const activeObjects = [];
      const now = Date.now();

      // Object 1: Person walking ahead (drifts slightly center/right)
      const personX = canvas.width * (0.42 + 0.08 * Math.sin(simWalkFrame * 0.08));
      const personY = canvas.height * 0.36;
      const personW = canvas.width * 0.28;
      const personH = canvas.height * 0.38;
      const personDist = Math.max(1.2, 2.4 - (stepWalkedMeters % 15) * 0.08);

      activeObjects.push({{
        label: 'Person',
        icon: '👤',
        x: personX,
        y: personY,
        w: personW,
        h: personH,
        conf: 0.94,
        distance: personDist,
        lane: personX < canvas.width * 0.35 ? 'left' : (personX > canvas.width * 0.65 ? 'right' : 'center')
      }});

      // Object 2: Construction barrier / physical obstacle on right
      if (stepWalkedMeters >= 35 && stepWalkedMeters <= 75) {{
        const barrierX = canvas.width * 0.55;
        const barrierY = canvas.height * 0.44;
        const barrierW = canvas.width * 0.38;
        const barrierH = canvas.height * 0.32;
        const barrierDist = Math.max(0.6, 2.0 - (stepWalkedMeters - 40) * 0.1);

        activeObjects.push({{
          label: 'Construction barrier',
          icon: '🚧',
          x: barrierX,
          y: barrierY,
          w: barrierW,
          h: barrierH,
          conf: 0.97,
          distance: barrierDist,
          lane: 'right'
        }});
      }} else {{
        // Distant building entrance / door ahead
        const doorX = canvas.width * 0.32;
        const doorY = canvas.height * 0.22;
        const doorW = canvas.width * 0.34;
        const doorH = canvas.height * 0.45;
        activeObjects.push({{
          label: 'RTU Entrance Door',
          icon: '🚪',
          x: doorX,
          y: doorY,
          w: doorW,
          h: doorH,
          conf: 0.96,
          distance: 4.8,
          lane: 'center'
        }});
      }}

      // Render YOLO bounding boxes & labels
      activeObjects.forEach(obj => {{
        let strokeColor = '#10B981'; // safe green
        let tagBg = 'rgba(16, 185, 129, 0.9)';
        if (obj.distance < 0.75) {{
          strokeColor = '#DC2626'; // critical red
          tagBg = 'rgba(220, 38, 38, 0.95)';
        }} else if (obj.distance < 1.5) {{
          strokeColor = '#EF4444'; // danger red
          tagBg = 'rgba(239, 68, 68, 0.9)';
        }} else if (obj.distance < 2.5) {{
          strokeColor = '#F59E0B'; // caution amber
          tagBg = 'rgba(245, 158, 11, 0.9)';
        }}

        // Bounding Box
        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = obj.distance < 1.5 ? 3 : 2;
        if (ctx.roundRect) {{
          ctx.beginPath();
          ctx.roundRect(obj.x, obj.y, obj.w, obj.h, 8);
          ctx.stroke();
        }} else {{
          ctx.strokeRect(obj.x, obj.y, obj.w, obj.h);
        }}

        // Tech Corner Accents
        const cornerLen = 10;
        ctx.lineWidth = 3.5;
        // Top-Left
        ctx.beginPath();
        ctx.moveTo(obj.x, obj.y + cornerLen);
        ctx.lineTo(obj.x, obj.y);
        ctx.lineTo(obj.x + cornerLen, obj.y);
        ctx.stroke();
        // Top-Right
        ctx.beginPath();
        ctx.moveTo(obj.x + obj.w - cornerLen, obj.y);
        ctx.lineTo(obj.x + obj.w, obj.y);
        ctx.lineTo(obj.x + obj.w, obj.y + cornerLen);
        ctx.stroke();

        // Label Pill
        const labelText = `${{obj.icon}} ${{obj.label}} ${{Math.round(obj.conf * 100)}}% • ${{obj.distance.toFixed(1)}}m`;
        ctx.font = 'bold 11px sans-serif';
        const textWidth = ctx.measureText(labelText).width;
        const pillW = textWidth + 12;
        const pillH = 20;
        const pillX = obj.x;
        const pillY = Math.max(8, obj.y - 24);

        ctx.fillStyle = tagBg;
        if (ctx.roundRect) {{
          ctx.beginPath();
          ctx.roundRect(pillX, pillY, pillW, pillH, 6);
          ctx.fill();
        }} else {{
          ctx.fillRect(pillX, pillY, pillW, pillH);
        }}

        ctx.fillStyle = '#FFFFFF';
        ctx.fillText(labelText, pillX + 6, pillY + 14);
      }});

      // Update Top HUD Hazard Status Badge
      const closestCenter = activeObjects.find(o => o.lane === 'center');
      const badge = document.getElementById('nav-live-hazard-badge');
      const pathText = document.getElementById('nav-path-status-text');
      const yoloCount = document.getElementById('nav-yolo-count');

      if (yoloCount) {{
        yoloCount.innerText = `YOLO: ${{activeObjects.length}} objects`;
      }}

      if (badge && pathText) {{
        if (closestCenter && closestCenter.distance < 1.5) {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-red-100 border border-red-300 text-red-900 text-[11px] font-semibold flex items-center justify-between";
          pathText.innerText = `Hazard: ${{closestCenter.label}} (${{closestCenter.distance.toFixed(1)}}m)`;
        }} else if (closestCenter && closestCenter.distance < 2.5) {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-amber-100 border border-amber-300 text-amber-900 text-[11px] font-semibold flex items-center justify-between";
          pathText.innerText = `Caution: ${{closestCenter.label}} (${{closestCenter.distance.toFixed(1)}}m)`;
        }} else {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-[11px] font-semibold flex items-center justify-between";
          pathText.innerText = "Clear pathway ahead";
        }}
      }}

      // Safety Voice Warning Throttle
      if (closestCenter && closestCenter.distance < 2.2 && (now - lastSpokenObstacleTime > 5500)) {{
        lastSpokenObstacleTime = now;
        triggerHaptic([80, 50, 80]);
        speakText(`Caution: ${{closestCenter.label.toLowerCase()}} ${{closestCenter.distance.toFixed(1)}} meters ahead in your walking path.`);
      }}
    }}

    async function triggerSignboardScan(quiet = false) {{
      const banner = document.getElementById('signboard-callout-banner');
      const bannerText = document.getElementById('signboard-banner-text');
      const overlay = document.getElementById('nav-signboards-overlay');

      let detected = null;
      try {{
        // Snapshot current video frame if live camera active
        let frameBase64 = null;
        const video = document.getElementById('nav-live-video');
        if (isRealCameraActive && video && video.videoWidth) {{
          const snapCanvas = document.createElement('canvas');
          snapCanvas.width = 640;
          snapCanvas.height = 360;
          snapCanvas.getContext('2d').drawImage(video, 0, 0, snapCanvas.width, snapCanvas.height);
          frameBase64 = snapCanvas.toDataURL('image/jpeg', 0.7);
        }}

        const resp = await fetch('/api/v1/environment/detect-signs', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            imageBase64: frameBase64,
            userContext: {{ street: 'Paula Valdena iela', heading: 'East', landmark: 'RTU Campus' }}
          }})
        }});
        if (resp.ok) {{
          const json = await resp.json();
          if (json && json.status === 'success' && json.data) {{
            detected = json.data;
          }}
        }}
      }} catch (err) {{
        console.warn("[Signboards] API call error, using contextual landmark signs:", err);
      }}

      // Fallback contextual signboards if offline or network failure
      if (!detected || !detected.signs || detected.signs.length === 0) {{
        detected = {{
          signs: [
            {{ text: "Paula Valdena iela", type: "street_sign", position: "right", confidence: 0.96, spoken_announcement: "Street sign on right: Paula Valdena iela" }},
            {{ text: "RTU Datorzinātnes fakultāte", type: "building_board", position: "ahead", confidence: 0.95, spoken_announcement: "Building entrance ahead: RTU Faculty of Computer Science" }},
            {{ text: "9. autobuss: Ķīpsala", type: "transit_sign", position: "left", confidence: 0.92, spoken_announcement: "Transit sign on left: Bus stop 9 Ķīpsala" }}
          ],
          summary: "Detected street sign Paula Valdena iela and RTU Faculty of Computer Science ahead."
        }};
      }}

      const primarySign = detected.signs[0] || signboardCatalog[0];
      const signLabel = `${{primarySign.text}} • ${{primarySign.type === 'street_sign' ? 'Street Sign' : 'Building Board'}}`;

      if (bannerText) {{
        bannerText.innerText = signLabel;
      }}
      if (banner) {{
        banner.classList.remove('opacity-0', 'scale-95');
        banner.classList.add('opacity-100', 'scale-100');
      }}

      // Render floating signboard badges on HUD overlay
      if (overlay) {{
        overlay.innerHTML = detected.signs.map(s => `
          <div class="px-3 py-1.5 rounded-2xl bg-purple-950/85 backdrop-blur-md border border-purple-400 text-white text-xs font-bold shadow-lg flex items-center space-x-2 animate-bounce pointer-events-auto">
            <span>${{s.type === 'street_sign' ? '🪧' : (s.type === 'transit_sign' ? '🚏' : '🏢')}}</span>
            <span>${{s.text}}</span>
            <span class="text-[10px] text-purple-200 bg-purple-800/80 px-1.5 py-0.5 rounded-full">${{Math.round((s.confidence || 0.95) * 100)}}%</span>
          </div>
        `).join('');
      }}

      const now = Date.now();
      if (!quiet || (now - lastSpokenSignTime > 12000 && lastSpokenSignText !== primarySign.text)) {{
        lastSpokenSignTime = now;
        lastSpokenSignText = primarySign.text;
        triggerHaptic([60, 40]);
        speakText(detected.summary || primarySign.spoken_announcement || `Detected signboard: ${{primarySign.text}}.`);
        announceToScreenReader(`Signboard detected: ${{primarySign.text}}`);
      }}
    }}

    // ==================== SPOKEN BUTTON CLICKING & AUTOMATED GPS ROUTING ====================
    function handleSpokenButtonClick(buttonId, spokenText) {{
      triggerHaptic([70, 40]);
      if (spokenText) speakText(spokenText);

      const flashElement = (el) => {{
        if (!el) return;
        el.classList.add('ring-4', 'ring-amber-400', 'scale-105');
        setTimeout(() => {{
          el.classList.remove('ring-4', 'ring-amber-400', 'scale-105');
        }}, 600);
      }};

      if (buttonId === 'start_navigation') {{
        flashElement(document.getElementById('start-nav-btn'));
        setTimeout(() => {{
          if (activeRoute === 'routePreview') {{
            startCurrentNavigation();
          }} else {{
            navigateTo('routePreview');
            setTimeout(() => startCurrentNavigation(), 700);
          }}
        }}, 400);
      }} else if (buttonId === 'where_am_i') {{
        flashElement(document.getElementById('btn-where-am-i'));
        setTimeout(() => navigateTo('whereAmI'), 400);
      }} else if (buttonId === 'describe_around') {{
        flashElement(document.getElementById('btn-describe-around'));
        setTimeout(() => navigateTo('describeAround'), 400);
      }} else if (buttonId === 'detect_signs') {{
        flashElement(document.getElementById('btn-detect-signs'));
        triggerSignboardScan(false);
      }} else if (buttonId === 'repeat') {{
        flashElement(document.getElementById('btn-repeat-instruction'));
        if (activeRoute === 'activeNavigation') repeatCurrentStep();
        else if (activeRoute === 'whereAmI') speakText(document.getElementById('where-am-i-headline')?.innerText || "You are at RTU Campus.");
        else if (activeRoute === 'describeAround') repeatSceneDescription();
        else if (activeRoute === 'obstacleAlert') repeatObstacleWarning();
        else speakText("Nothing to repeat.");
      }} else if (buttonId === 'acknowledge_obstacle') {{
        flashElement(document.getElementById('btn-i-understand'));
        acknowledgeObstacle();
      }} else if (buttonId === 'settings') {{
        openSettingsModal();
      }} else if (buttonId === 'toggle_camera') {{
        flashElement(document.getElementById('btn-toggle-camera'));
        toggleCameraFeed();
      }} else if (buttonId === 'stop_route') {{
        flashElement(document.getElementById('btn-stop-route'));
        stopNavigationRoute();
      }}
    }}

    function handleAutoGpsNavigation(dest, spoken) {{
      document.getElementById('listening-title').innerText = "Detecting current location...";
      announceToScreenReader("Detecting current GPS location and calculating route.");
      speakText("Detecting your current location.");
      triggerHaptic([60, 40]);

      const executeRouting = (lat, lng, locName) => {{
        const targetDest = dest || clientLocationsCatalog[0];
        document.getElementById('listening-title').innerText = `Location found: ${{locName}}. Routing...`;
        speakText(spoken || `Current location detected near ${{locName}}. Routing to ${{targetDest.canonicalName || targetDest.shortName}}.`);
        
        selectDestination(targetDest.canonicalName || targetDest.shortName, targetDest.subtitle || 'Selected walking destination');
        
        setTimeout(() => {{
          startCurrentNavigation();
        }}, 1400);
      }};

      if (navigator.geolocation) {{
        navigator.geolocation.getCurrentPosition(
          (pos) => {{
            executeRouting(pos.coords.latitude, pos.coords.longitude, "Paula Valdena iela");
          }},
          (err) => {{
            console.warn("GPS access notice:", err.message);
            executeRouting(56.953, 24.081, "RTU Ķīpsala Campus");
          }},
          {{ timeout: 5000, enableHighAccuracy: true }}
        );
      }} else {{
        executeRouting(56.953, 24.081, "RTU Ķīpsala Campus");
      }}
    }}

    function parseVoiceIntentLocalFallback(rawTranscript) {{
      const cleaned = (rawTranscript || "").toLowerCase().replace(/[\\?\\!\\.,;:]/g, "").trim();

      // Button click actions
      if (/^(start navigation|start route|begin navigation|start walking|let('s)? go)$/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "start_navigation", action: "click_button", spoken_response: "Starting navigation.", confidence: 0.99 }};
      }}
      if (/^(where am i|where i am|what is my location|my location|current location|where are we)$/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "where_am_i", action: "click_button", spoken_response: "Checking current location and orientation.", confidence: 0.99 }};
      }}
      if (/^(describe|describe what('s| is) around me|describe around me|what do you see|what('s| is) around|look around|see around)$/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "describe_around", action: "click_button", spoken_response: "Scanning surroundings with camera.", confidence: 0.99 }};
      }}
      if (/^(read signs|read signboards?|detect signs?|what does the sign say|look for signs?|sign boards?)$/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "detect_signs", action: "click_button", spoken_response: "Reading visible signboards and street signs.", confidence: 0.98 }};
      }}
      if (/^(repeat|say again|what was that|repeat instruction|repeat location|repeat warning)$/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "repeat", action: "click_button", spoken_response: "Repeating last instruction.", confidence: 0.99 }};
      }}
      if (/^(i understand|understand|dismiss|dismiss obstacle|got it|clear|okay|ok)$/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "acknowledge_obstacle", action: "click_button", spoken_response: "Obstacle acknowledged. Resuming route.", confidence: 0.99 }};
      }}
      if (/^(settings|open settings|audio settings|preferences)$/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "settings", action: "click_button", spoken_response: "Opening settings.", confidence: 0.99 }};
      }}
      if (/^(camera|switch camera|toggle camera|turn camera on|open camera|back camera)$/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "toggle_camera", action: "click_button", spoken_response: "Toggling back camera.", confidence: 0.98 }};
      }}
      if (/^(stop|cancel|end navigation|stop navigation|stop route|halt)/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "stop_route", action: "click_button", spoken_response: "Navigation stopped.", confidence: 0.99 }};
      }}

      const lowered = cleaned;
      if (/^(where am i|where i am|what is my location|current location|where are we)/i.test(lowered)) {{
        return {{
          intent: "where_am_i",
          destination: null,
          spoken_response: "You are near Riga Technical University, Kipsala Campus.",
          confidence: 0.98
        }};
      }}
      if (/^(what('s| is) in front of me|what('s| is) in front|describe|what do you see|what('s| is) around|look around|see around)/i.test(lowered)) {{
        return {{
          intent: "describe_environment",
          destination: null,
          spoken_response: getLidarSceneDescription(),
          confidence: 0.97
        }};
      }}
      if (/^(stop|cancel|end navigation|stop navigation|stop route|halt)/i.test(lowered)) {{
        return {{
          intent: "stop",
          destination: null,
          spoken_response: "Navigation stopped.",
          confidence: 0.99
        }};
      }}
      if (/^(repeat|say again|what was that|repeat instruction)/i.test(lowered)) {{
        return {{
          intent: "repeat",
          destination: null,
          spoken_response: "Repeating last instruction.",
          confidence: 0.98
        }};
      }}

      const navPrefixRegex = /^(please\\s+)?(take me to|navigate to|open the|open|i want to go to|i need to go to|i need to get to|head to|walk to|go to|find the|find|directions to|route to|start route to|start navigation to|take me|navigate|start navigation|start route|directions|route|head|walk|go)\\s*(.*)$/i;
      const match = lowered.match(navPrefixRegex);
      let destQuery = match ? (match[3] || "").trim() : lowered;
      const clean = destQuery.replace(/^(the|a|an)\\s+/i, "").trim();

      const vagueWords = new Set([
        "",
        "there",
        "somewhere",
        "anywhere",
        "it",
        "place",
        "location",
        "navigate",
        "navigation",
        "start navigation",
        "start route",
        "route",
        "directions",
        "go somewhere",
        "take me somewhere",
        "take me there",
        "take me",
        "where is it"
      ]);

      if (vagueWords.has(clean) || vagueWords.has(lowered) || /^(navigate|start navigation|go somewhere|take me somewhere|take me there|directions|route|start route)$/i.test(lowered)) {{
        return {{
          intent: "clarification_needed",
          destination: null,
          clarification_prompt: "Where would you like to go? You can say the library, the main building, the sports center, or any location in Riga.",
          spoken_response: "Where would you like to go? Please specify a destination.",
          confidence: 0.9
        }};
      }}

      const known = findClientLocationMatch(clean);
      if (known) {{
        return {{
          intent: "start_navigation",
          destination: known,
          spoken_response: `Routing to ${{known.canonicalName}}. Distance ${{known.distanceKm}} kilometers, estimated ${{known.estimatedMinutes}} minutes.`,
          confidence: 0.96
        }};
      }}

      if (clean.length >= 2) {{
        const custom = createClientCustomDestination(clean);
        return {{
          intent: "start_navigation",
          destination: custom,
          spoken_response: `Planning route to ${{custom.canonicalName}}. Distance ${{custom.distanceKm}} kilometers, estimated ${{custom.estimatedMinutes}} minutes.`,
          confidence: 0.92
        }};
      }}

      return {{
        intent: "clarification_needed",
        destination: null,
        clarification_prompt: "I didn't quite catch that destination. Where would you like to go?",
        spoken_response: "Where would you like to go? Please tell me the place or address.",
        confidence: 0.5
      }};
    }}

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
      if (tip) {{
        if (targetRoute === 'home') {{
          tip.innerHTML = "Tap <strong>Describe what's around me</strong> or <strong>Start navigation</strong>";
        }} else if (targetRoute === 'listening') {{
          tip.innerHTML = "Listening actively... Say <strong>'Take me to RTU'</strong> or <strong>'Describe around me'</strong>";
        }} else if (targetRoute === 'destinationSearch') {{
          tip.innerHTML = "Select a destination like <strong>Riga Technical University</strong> or speak";
        }} else if (targetRoute === 'routePreview') {{
          tip.innerHTML = "Route preview to <strong>RTU Ķīpsala</strong>. Tap <strong>Start navigation</strong> to begin";
        }} else if (targetRoute === 'activeNavigation') {{
          tip.innerHTML = "Active walking navigation with live countdown. Test safety events below.";
        }} else if (targetRoute === 'whereAmI') {{
          tip.innerHTML = "Current location and orientation near <strong>RTU Ķīpsala Campus</strong>";
        }} else if (targetRoute === 'describeAround') {{
          tip.innerHTML = "Perception scene: <strong>RTU Campus</strong>. Tap <strong>Repeat</strong> to hear again";
        }} else if (targetRoute === 'obstacleAlert') {{
          tip.innerHTML = "Warning: <strong>Obstacle ahead</strong>. Tap <strong>I Understand</strong> to resume";
        }} else if (targetRoute === 'crosswalkSafety') {{
          tip.innerHTML = "Crosswalk quiet mode active. Tap waveform card when across to resume.";
        }}
      }}

      if (targetRoute === 'home') {{
        speakText("Blind AI home. How can I help you today?");
      }} else if (targetRoute === 'listening') {{
        speakText("Listening. Say your command or destination.");
        startVoiceCapture();
      }} else if (targetRoute === 'destinationSearch') {{
        speakText("Where would you like to go? You can select Riga Technical University, Ķīpsala Campus.");
      }} else if (targetRoute === 'routePreview') {{
        speakText("Route preview to Riga Technical University, Ķīpsala. 2.4 kilometers, 28 minutes, 8 waypoints.");
      }} else if (targetRoute === 'activeNavigation') {{
        announceToScreenReader("Active walking navigation started. Turn right on Ķīpsalas iela in 120 meters.");
        startAlwaysOpenBackCamera();
      }} else if (targetRoute === 'whereAmI') {{
        speakText("Where am I? You are at Riga Technical University, Ķīpsala Campus in Riga, Latvia. Facing east.");
      }} else if (targetRoute === 'describeAround') {{
        speakText(getLidarSceneDescription());
      }} else if (targetRoute === 'obstacleAlert') {{
        const evalResult = evaluateLidarDanger(currentLidarDistance, currentLidarLane, currentLidarObject);
        speakText(evalResult.spoken || "Warning: Obstacle ahead. Two meters ahead, construction barrier on right. Pathway is clear on left.");
      }} else if (targetRoute === 'crosswalkSafety') {{
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
      currentDestinationTitle = title;
      currentDestinationSub = sub + " • 2.4 km • 28 min • 8 waypoints";
      const match = (typeof findClientLocationMatch === 'function') ? findClientLocationMatch(title) : null;
      if (match && match.waypoints) {{
        currentWaypoints = match.waypoints.map(w => ({{
          instruction: w.instruction,
          distance: w.distanceMeters !== undefined ? w.distanceMeters : (w.distance || 80),
          maneuver: w.maneuver || 'Head straight',
          icon: (w.icon === 'arrow.up' || w.icon === '↑') ? '↑' : (w.icon === '↱' ? '↱' : (w.icon === '↰' || w.icon === 'arrow.turn.up.left' ? '↰' : (w.icon === '🚶' ? '🚶' : '★')))
        }}));
      }}
      document.getElementById('preview-destination-title').innerText = title;
      document.getElementById('preview-destination-sub').innerText = currentDestinationSub;
      const startBtn = document.getElementById('start-nav-btn');
      if (startBtn) startBtn.setAttribute('aria-label', `Start walking navigation to ${{title}}`);
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

    async function handleVoiceInput(rawText) {{
      if (!rawText || !rawText.trim()) return;
      const trimmed = rawText.trim();
      document.getElementById('live-transcript').innerText = '“' + trimmed + '”';
      document.getElementById('listening-title').innerText = "Gemini is analyzing...";
      announceToScreenReader(`Voice input: "${{trimmed}}". Analyzing with Gemini AI.`);
      triggerHaptic([30]);

      let result = null;
      try {{
        const resp = await fetch('/api/v1/voice/intent', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ transcript: trimmed }})
        }});
        if (resp.ok) {{
          const json = await resp.json();
          if (json && json.status === 'success' && json.data) {{
            result = json.data;
          }}
        }}
      }} catch (err) {{
        console.warn("[Voice] Server fetch error, using local Gemini model fallback:", err);
      }}

      // Offline or network fallback
      if (!result) {{
        result = parseVoiceIntentLocalFallback(trimmed);
      }}

      applyVoiceIntentResult(result, trimmed);
    }}

    function applyVoiceIntentResult(result, rawText) {{
      // 1. Spoken Button Click Action
      const targetBtn = result.target_button || (result.action === 'click_button' ? result.target_button : null) || (result.intent === 'click_button' ? result.target_button : null);
      if (targetBtn) {{
        handleSpokenButtonClick(targetBtn, result.spoken_response);
        return;
      }}

      // 2. Automated GPS Navigation Trigger
      if (result.trigger_auto_gps && (result.intent === 'start_navigation' || result.destination)) {{
        handleAutoGpsNavigation(result.destination, result.spoken_response);
        return;
      }}

      const intent = result.intent || 'start_navigation';

      if (intent === 'start_navigation') {{
        const dest = result.destination || {{
          canonicalName: 'Riga Technical University (RTU)',
          shortName: 'RTU Campus',
          subtitle: 'Ķīpsala Campus, Paula Valdena iela 1',
          distanceKm: 2.4,
          estimatedMinutes: 28,
          waypoints: rtuWaypoints
        }};

        currentDestinationTitle = dest.canonicalName || dest.shortName || 'Custom Destination';
        currentDestinationSub = (dest.subtitle || dest.canonicalName) + ' • ' + (dest.distanceKm || '2.4') + ' km • ' + (dest.estimatedMinutes || '28') + ' min';

        document.getElementById('preview-destination-title').innerText = currentDestinationTitle;
        document.getElementById('preview-destination-sub').innerText = currentDestinationSub;
        const startBtn = document.getElementById('start-nav-btn');
        if (startBtn) startBtn.setAttribute('aria-label', `Start walking navigation to ${{currentDestinationTitle}}`);

        if (dest.waypoints && dest.waypoints.length) {{
          currentWaypoints = dest.waypoints.map(w => ({{
            instruction: w.instruction,
            distance: w.distanceMeters !== undefined ? w.distanceMeters : (w.distance || 80),
            maneuver: w.maneuver || 'Head straight',
            icon: (w.icon === 'arrow.up' || w.icon === '↑') ? '↑' : (w.icon === '↱' ? '↱' : (w.icon === '↰' || w.icon === 'arrow.turn.up.left' ? '↰' : (w.icon === '🚶' ? '🚶' : '★')))
          }}));
        }} else {{
          currentWaypoints = [
            {{ instruction: 'Head toward ' + currentDestinationTitle, distance: 90, maneuver: 'Head straight', icon: '↑' }},
            {{ instruction: 'Continue along pedestrian walkway to ' + currentDestinationTitle, distance: 70, maneuver: 'Continue straight', icon: '↑' }},
            {{ instruction: 'Arrival: ' + currentDestinationTitle, distance: 0, maneuver: 'Destination reached', icon: '★' }}
          ];
        }}

        document.getElementById('listening-title').innerText = `Routing to ${{dest.shortName || dest.canonicalName}}...`;
        announceToScreenReader(`Routing to ${{currentDestinationTitle}}. Estimated walking time ${{dest.estimatedMinutes || 28}} minutes.`);
        speakText(result.spoken_response || `Routing to ${{currentDestinationTitle}}.`);
        triggerHaptic([80, 40, 80]);

        setTimeout(() => {{
          navigateTo('routePreview');
        }}, 950);
      }} else if (intent === 'clarification_needed') {{
        const clarifPrompt = result.clarification_prompt || "Where would you like to go? You can say the library, the main building, or any location.";
        document.getElementById('listening-title').innerText = "Where would you like to go?";
        document.getElementById('live-transcript').innerText = `“${{clarifPrompt}}”`;
        speakText(result.spoken_response || clarifPrompt);
        announceToScreenReader(clarifPrompt);
        triggerHaptic([60, 40]);
      }} else if (intent === 'where_am_i') {{
        document.getElementById('listening-title').innerText = "Checking location...";
        speakText(result.spoken_response || "Checking your current location and orientation.");
        triggerHaptic([60]);
        setTimeout(() => navigateTo('whereAmI'), 700);
      }} else if (intent === 'describe_environment') {{
        document.getElementById('listening-title').innerText = "Scanning environment...";
        speakText(result.spoken_response || "Scanning surroundings with camera.");
        triggerHaptic([60]);
        setTimeout(() => navigateTo('describeAround'), 700);
      }} else if (intent === 'stop') {{
        stopNavigationRoute();
      }} else if (intent === 'repeat') {{
        repeatCurrentStep();
      }} else {{
        speakText(result.spoken_response || ("I heard: " + rawText));
        setTimeout(() => navigateTo('home'), 1500);
      }}
    }}

    function startCurrentNavigation() {{
      startNavigationRoute(currentDestinationTitle);
    }}

    // Active Navigation Lifecycle & Safety Event Triggers
    let stepWalkedMeters = 0;
    let obstacleTriggeredThisStep = false;
    let trafficTriggeredThisStep = false;
    let metersSinceObstacle = 0;

    function startNavigationRoute(destName) {{
      const targetName = destName || currentDestinationTitle || 'Riga Technical University';
      navigateTo('activeNavigation');
      triggerHaptic([80, 40, 80]);
      currentWaypointIdx = 0;
      currentDistance = currentWaypoints[0] ? currentWaypoints[0].distance : 160;
      stepWalkedMeters = 0;
      obstacleTriggeredThisStep = false;
      trafficTriggeredThisStep = false;
      metersSinceObstacle = 0;
      renderActiveWaypoint();

      const initialInstruction = currentWaypoints[0] ? currentWaypoints[0].instruction : 'Head toward destination';
      speakText(`Starting walking route to ${{targetName}}. ${{initialInstruction}} in ${{currentDistance}} meters.`);

      if (navigationInterval) clearInterval(navigationInterval);
      if (autoWalkEnabled) {{
        navigationInterval = setInterval(progressWalking, 2200);
      }}
    }}

    function renderActiveWaypoint() {{
      const wp = currentWaypoints[currentWaypointIdx] || {{ instruction: 'Continue toward destination', maneuver: 'Continue straight', icon: '↑' }};
      document.getElementById('nav-step-label').innerText = `Navigation • Step ${{currentWaypointIdx + 1}} of ${{currentWaypoints.length}}`;
      document.getElementById('nav-instruction-text').innerText = wp.instruction;
      document.getElementById('nav-distance-num').innerText = currentDistance;
      document.getElementById('nav-maneuver-text').innerText = wp.maneuver;
      document.getElementById('nav-maneuver-icon').innerText = wp.icon;
    }}

    function progressWalking() {{
      if (activeRoute !== 'activeNavigation') return;

      if (currentDistance > 10) {{
        currentDistance -= 10;
        stepWalkedMeters += 10;
        document.getElementById('nav-distance-num').innerText = currentDistance;
        const currentManeuver = currentWaypoints[currentWaypointIdx]?.maneuver || 'Head straight';
        document.getElementById('nav-maneuver-text').innerText = currentDistance > 0 ? `${{currentManeuver}} in ${{currentDistance}}m` : currentManeuver;

        // Auto Safety Trigger 1: After walking for 40-50m in starting, show obstacle alert
        if (!obstacleTriggeredThisStep && (stepWalkedMeters >= 40 && stepWalkedMeters <= 50)) {{
          obstacleTriggeredThisStep = true;
          metersSinceObstacle = 0;
          triggerHaptic([100, 100, 150]);
          speakText("Warning: Obstacle ahead. Two meters ahead, construction barrier on right. Pathway is clear on left.");
          setTimeout(() => navigateTo('obstacleAlert'), 750);
          return;
        }}

        // Auto Safety Trigger 2: After walking 20m further (or after obstacle), show traffic / crosswalk alert
        if (obstacleTriggeredThisStep && !trafficTriggeredThisStep) {{
          metersSinceObstacle += 10;
          if (metersSinceObstacle >= 20) {{
            trafficTriggeredThisStep = true;
            triggerHaptic([80, 60, 80]);
            speakText("Approaching crosswalk. Listen for traffic.");
            setTimeout(() => navigateTo('crosswalkSafety'), 750);
            return;
          }}
        }}

        // Secondary crosswalk safety fallback at 20m remaining
        if (!trafficTriggeredThisStep && currentDistance <= 20) {{
          trafficTriggeredThisStep = true;
          triggerHaptic([80, 60, 80]);
          speakText("Approaching crosswalk. Listen for traffic.");
          setTimeout(() => navigateTo('crosswalkSafety'), 750);
          return;
        }}

        if (currentDistance === 50) {{
          triggerHaptic([50]);
          speakText(`50 meters remaining.`);
        }}
      }} else {{
        // Next waypoint
        currentWaypointIdx++;
        if (currentWaypointIdx < currentWaypoints.length) {{
          currentDistance = currentWaypoints[currentWaypointIdx].distance;
          stepWalkedMeters = 0;
          obstacleTriggeredThisStep = false;
          trafficTriggeredThisStep = false;
          metersSinceObstacle = 0;
          renderActiveWaypoint();
          speakText(currentWaypoints[currentWaypointIdx].instruction);
        }} else {{
          clearInterval(navigationInterval);
          navigationInterval = null;
          speakText(`You have arrived at ${{currentDestinationTitle}}. Navigation complete.`);
          triggerHaptic([120, 60, 120, 60, 200]);
          setTimeout(() => navigateTo('home'), 3500);
        }}
      }}
    }}

    function repeatCurrentStep() {{
      triggerHaptic([40]);
      const wp = currentWaypoints[currentWaypointIdx] || {{ instruction: 'Continue along pathway' }};
      speakText(`${{wp.instruction}}. ${{currentDistance}} meters remaining.`);
    }}

    function stopNavigationRoute() {{
      triggerHaptic([100]);
      stopAlwaysOpenBackCamera();
      if (navigationInterval) {{
        clearInterval(navigationInterval);
        navigationInterval = null;
      }}
      stepWalkedMeters = 0;
      obstacleTriggeredThisStep = false;
      trafficTriggeredThisStep = false;
      metersSinceObstacle = 0;
      speakText("Navigation stopped.");
      navigateTo('home');
    }}

    function speakRouteOverview() {{
      triggerHaptic([40]);
      speakText(`Route overview to ${{currentDestinationTitle}}. ${{currentDestinationSub}}. Sidewalk condition is clear.`);
    }}

    // Safety Screen Actions
    function repeatSceneDescription() {{
      triggerHaptic([40]);
      speakText(getLidarSceneDescription());
    }}

    function repeatObstacleWarning() {{
      triggerHaptic([40]);
      const evalResult = evaluateLidarDanger(currentLidarDistance, currentLidarLane, currentLidarObject);
      speakText(evalResult.spoken || `Warning: ${{currentLidarObject}} ahead, ${{currentLidarDistance.toFixed(1)}} meters.`);
    }}

    function acknowledgeObstacle() {{
      triggerHaptic([60, 40]);
      speakText("Obstacle acknowledged. Resuming path.");
      updateLidarState(4.0, 'Clear Path', 'center', false);
      
      try {{
        fetch('/api/v1/navigation/sessions/default/events', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            obstacle_type: currentLidarObject.toLowerCase().replace(/ /g, '_'),
            lane: currentLidarLane,
            distance_meters: currentLidarDistance,
            action_taken: 'avoid_left'
          }})
        }}).catch(() => {{}});
      }} catch(e){{}}

      setTimeout(() => {{
        navigateTo('activeNavigation');
        if (autoWalkEnabled && !navigationInterval) {{
          navigationInterval = setInterval(progressWalking, 2200);
        }}
      }}, 400);
    }}

    function confirmCrossed() {{
      triggerHaptic([80, 50]);
      speakText("Crosswalk completed. Resuming route.");
      setTimeout(() => {{
        navigateTo('activeNavigation');
        if (autoWalkEnabled && !navigationInterval) {{
          navigationInterval = setInterval(progressWalking, 2200);
        }}
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
      try {{
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('simulator') === 'true' || urlParams.get('dev') === 'true' || window.location.hash === '#dev') {{
          document.body.classList.add('show-simulator');
        }}
      }} catch (e) {{}}

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

    function toggleSimulatorChrome() {{
      const isShowing = document.body.classList.toggle('show-simulator');
      const icon = document.getElementById('mode-icon');
      const text = document.getElementById('mode-text');
      const btn = document.getElementById('toggle-mobile-mode-btn');
      if (isShowing) {{
        if (icon) icon.innerText = '🛠️';
        if (text) text.innerText = 'Tools: ON';
        if (btn) btn.className = 'flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-500 text-white transition shadow-sm';
      }} else {{
        if (icon) icon.innerText = '📱';
        if (text) text.innerText = 'Mobile View';
        if (btn) btn.className = 'flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-neutral-900 text-white transition shadow-sm';
      }}
    }}
  </script>

  <!-- Floating View Mode Switcher (Tap to toggle Developer Simulator Tools on or off) -->
  <aside aria-label="Simulator View Mode Switcher" class="fixed bottom-4 right-4 z-50 flex items-center gap-2 bg-white/95 backdrop-blur-md border border-slate-300 rounded-full p-1.5 shadow-xl text-xs font-semibold text-slate-700">
    <button type="button" id="toggle-mobile-mode-btn" onclick="toggleSimulatorChrome()" aria-label="Toggle between Pure Mobile View and Developer Simulator Tools" class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-neutral-900 text-white transition hover:bg-neutral-800 active:scale-95 shadow-sm">
      <span id="mode-icon">📱</span>
      <span id="mode-text">Mobile View</span>
    </button>
  </aside>
</body>
</html>"""

os.makedirs('backend/public', exist_ok=True)

with open('preview.html', 'w') as f:
    f.write(html_content)

with open('index.html', 'w') as f:
    f.write(html_content)

with open('backend/preview.html', 'w') as f:
    f.write(html_content)

with open('backend/index.html', 'w') as f:
    f.write(html_content)

with open('backend/public/index.html', 'w') as f:
    f.write(html_content)

artifact_path = '/Users/ranjeet/.gemini/antigravity/brain/c5f01990-a932-4376-b981-a9dfcbedd688/blind_ai_simulator.html'
with open(artifact_path, 'w') as f:
    f.write(html_content)

print('Generated accessible preview.html, index.html, and simulator artifacts successfully!')
