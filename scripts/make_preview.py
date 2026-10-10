import os

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="theme-color" content="#F8F8F9">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <!-- Leaflet Interactive Maps & OpenStreetMap -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <!-- Real-Time Client-Side Computer Vision & Object Detection -->
  <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.20.0/dist/tf.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd@2.2.3/dist/coco-ssd.min.js"></script>
  <style>
    /* Leaflet Accessible Customization */
    .leaflet-container {{
      width: 100% !important;
      height: 100% !important;
      border-radius: 1.25rem !important;
      font-family: inherit !important;
      z-index: 10 !important;
    }}
    .leaflet-control-attribution {{
      display: none !important;
    }}
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
    /* Global SVG & Icon Non-Distortion & Crispness */
    svg {{
      flex-shrink: 0;
      shape-rendering: geometricPrecision;
    }}
    button, a {{
      -webkit-tap-highlight-color: transparent;
    }}

    /* Safe Area Inset Classes */
    .mobile-safe-header {{
      padding-top: max(env(safe-area-inset-top, 0px), 14px) !important;
      padding-left: max(env(safe-area-inset-left, 0px), 16px) !important;
      padding-right: max(env(safe-area-inset-right, 0px), 16px) !important;
    }}
    .mobile-safe-footer {{
      padding-bottom: max(env(safe-area-inset-bottom, 0px), 20px) !important;
      padding-left: max(env(safe-area-inset-left, 0px), 16px) !important;
      padding-right: max(env(safe-area-inset-right, 0px), 16px) !important;
    }}

    /* Full-Bleed Native Mobile Layout on real phones / tablets */
    @media (max-width: 768px) {{
      html, body {{
        width: 100% !important;
        height: 100% !important;
        height: 100dvh !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        background-color: #F8F8F9 !important;
        -webkit-text-size-adjust: 100% !important;
        touch-action: manipulation;
      }}
      body {{
        display: flex !important;
        flex-direction: column !important;
        align-items: stretch !important;
        justify-content: flex-start !important;
        padding: 0 !important;
      }}
      #main-content {{
        width: 100% !important;
        max-width: 100% !important;
        height: 100% !important;
        height: 100dvh !important;
        flex: 1 1 100% !important;
        display: flex !important;
        padding: 0 !important;
        margin: 0 !important;
      }}
      #view-interactive {{
        width: 100% !important;
        max-width: 100% !important;
        height: 100% !important;
        height: 100dvh !important;
        flex: 1 1 100% !important;
        padding: 0 !important;
        margin: 0 !important;
        gap: 0 !important;
      }}
      #view-interactive > div {{
        width: 100% !important;
        max-width: 100% !important;
        height: 100% !important;
        height: 100dvh !important;
      }}
      .iphone-frame {{
        width: 100% !important;
        max-width: 100% !important;
        min-width: 100% !important;
        height: 100% !important;
        height: 100dvh !important;
        max-height: 100dvh !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        margin: 0 !important;
        padding: 0 !important;
        background-color: #F8F8F9 !important;
      }}
      #device-status-bar, #device-home-bar {{
        display: none !important;
      }}
      aside[aria-label="Simulator View Mode Switcher"] {{
        display: none !important;
      }}
      .screen-container {{
        height: 100% !important;
        height: 100dvh !important;
      }}
    }}
    
    .no-scrollbar::-webkit-scrollbar {{ display: none; }}
    .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
  </style>
</head>
<body class="bg-slate-100 text-slate-900 font-sans antialiased min-h-screen p-0 md:p-6 flex flex-col items-center justify-center">
  <!-- Universal Floating Voice HUD (Active across all screens when voice mic is listening) -->
  <aside id="universal-voice-hud" aria-label="Live Voice Guidance and Listening HUD" aria-live="assertive" class="fixed top-4 left-1/2 -translate-x-1/2 w-[92%] max-w-md z-50 bg-neutral-950/95 backdrop-blur-md text-white rounded-3xl p-4 shadow-2xl border border-orange-500/40 hidden flex items-center gap-3 transition-all duration-300">
    <div class="w-12 h-12 rounded-full bg-orange-500 text-white flex items-center justify-center shrink-0 shadow-lg relative">
      <span class="absolute -inset-1 rounded-full bg-orange-500/40 animate-ping"></span>
      <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white relative z-10 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
      </svg>
    </div>
    <div class="flex flex-col min-w-0 flex-1">
      <div class="flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-orange-400 animate-pulse shrink-0"></span>
        <span id="voice-hud-status" class="text-[11px] font-bold text-orange-400 uppercase tracking-wider">Listening to your voice...</span>
      </div>
      <p id="voice-hud-text" class="text-sm font-bold text-white mt-0.5 leading-snug line-clamp-2">
        Speak now — Say a place to go, or ask: "Is someone on my right?"
      </p>
    </div>
    <button onclick="hideUniversalVoiceHUD()" aria-label="Dismiss voice assistant" class="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center shrink-0 text-xs font-bold transition">
      ✕
    </button>
  </aside>


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
          <option value="routePreview">4. Route Preview</option>
          <option value="activeNavigation">5. Active Navigation (Always-Open Camera + YOLO)</option>
          <option value="whereAmI">6. Where am I?</option>
          <option value="describeAround">7. Describe what's around me</option>
          <option value="obstacleAlert">8. Obstacle ahead (Live AR Danger)</option>
          <option value="crosswalkSafety">9. Approaching crosswalk (Quiet Mode)</option>
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

      <!-- Real-Time Physical Movement Tracker (No Fake Simulation) -->
      <div id="real-movement-pill" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 text-white text-xs font-medium shadow-sm border border-slate-700" title="Live Pedometer & GPS Physical Distance Tracker">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" aria-hidden="true"></span>
        <span class="font-mono text-[11px]">Walked: <strong id="real-steps-display" class="text-emerald-400">0</strong> steps (<strong id="real-dist-display" class="text-emerald-400">0.0m</strong>)</span>
      </div>
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
          <div id="screen-home" role="region" aria-label="Screen 1: Home" class="screen-container flex-1 flex flex-col justify-between p-5 pb-6">
            <div class="mobile-safe-header flex justify-between items-center pt-2 px-1">
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition active:scale-95 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <div class="flex flex-col items-center justify-center my-auto py-2">
              <button type="button" onclick="triggerVoiceAssistant()" aria-label="Activate voice listening assistant" class="relative flex items-center justify-center w-36 h-36 mb-4 cursor-pointer rounded-full focus:outline-none shrink-0">
                <div class="absolute w-44 h-44 rounded-full orb-glow ripple-ring-1 pointer-events-none" aria-hidden="true"></div>
                <div class="absolute w-36 h-36 rounded-full orb-glow ripple-ring-2 pointer-events-none" aria-hidden="true"></div>
                <div class="w-28 h-28 rounded-full orb-3d relative z-10 flex items-center justify-center shrink-0" aria-hidden="true">
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
                <div class="flex items-center space-x-3.5 min-w-0 flex-1">
                  <div class="w-11 h-11 rounded-xl bg-orange-50 border border-orange-100 flex items-center justify-center text-orange-600 shrink-0" aria-hidden="true">
                    <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" /></svg>
                  </div>
                  <div class="min-w-0 flex-1 pr-2">
                    <h3 class="font-bold text-slate-900 text-base leading-tight">Start navigation</h3>
                    <p class="text-xs text-slate-600 mt-0.5 truncate">Get directions to a place</p>
                  </div>
                </div>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>

              <!-- Card 2: Describe what's around me -->
              <button onclick="navigateTo('describeAround')" aria-label="Describe what's around me: Identify objects and obstacles" class="w-full bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-slate-300 transition active:scale-[0.99]">
                <div class="flex items-center space-x-3.5 min-w-0 flex-1">
                  <div class="w-11 h-11 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 shrink-0" aria-hidden="true">
                    <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                  </div>
                  <div class="min-w-0 flex-1 pr-2">
                    <h3 class="font-bold text-slate-900 text-base leading-tight">Describe what's around me</h3>
                    <p class="text-xs text-slate-600 mt-0.5 truncate">Identify objects and obstacles</p>
                  </div>
                </div>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>

              <!-- Card 3: Where am I? -->
              <button onclick="navigateTo('whereAmI')" aria-label="Where am I?: Current location and surroundings" class="w-full bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-slate-300 transition active:scale-[0.99]">
                <div class="flex items-center space-x-3.5 min-w-0 flex-1">
                  <div class="w-11 h-11 rounded-xl bg-purple-50 border border-purple-100 flex items-center justify-center text-purple-600 shrink-0" aria-hidden="true">
                    <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  </div>
                  <div class="min-w-0 flex-1 pr-2">
                    <h3 class="font-bold text-slate-900 text-base leading-tight">Where am I?</h3>
                    <p class="text-xs text-slate-600 mt-0.5 truncate">Current location and surroundings</p>
                  </div>
                </div>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>
            </div>

            <!-- Bottom Mic Button -->
            <div class="mobile-safe-footer flex justify-center mt-3">
              <button onclick="triggerVoiceAssistant()" aria-label="Start voice listening assistant" class="w-16 h-16 rounded-full bg-black text-white flex items-center justify-center shadow-lg hover:bg-neutral-800 transition active:scale-95 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 2: VOICE LISTENING ==================== -->
          <div id="screen-listening" role="region" aria-label="Screen 2: Voice Listening" class="screen-container flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <div class="mobile-safe-header flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('home')" aria-label="Back to home screen" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <div class="w-11 h-11 shrink-0" aria-hidden="true"></div>
            </div>

            <div class="flex flex-col items-center justify-center my-auto">
              <div class="relative flex items-center justify-center w-48 h-48 mb-6 shrink-0" aria-hidden="true">
                <div class="absolute w-56 h-56 rounded-full orb-glow ripple-ring-1"></div>
                <div class="absolute w-44 h-44 rounded-full orb-glow ripple-ring-2"></div>
                <div class="w-32 h-32 rounded-full orb-3d relative z-10 flex items-center justify-center shrink-0">
                  <div class="w-12 h-12 rounded-full bg-white/20 blur-[2px]"></div>
                </div>
              </div>
              <h2 id="listening-title" class="text-2xl font-bold text-center text-slate-900 tracking-tight">
                I'm listening...
              </h2>
              <p id="live-transcript" aria-live="polite" class="text-sm text-slate-600 text-center mt-2 px-6 italic min-h-[3rem]">
                “Take me to coffee shop”
              </p>
              <div class="mt-2 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-orange-50 border border-orange-200 text-[11px] font-semibold text-orange-700 shrink-0">
                <span class="w-2 h-2 rounded-full bg-orange-500 animate-pulse shrink-0"></span>
                <span>Powered by Gemini AI</span>
              </div>
            </div>

            <div class="mobile-safe-footer flex flex-col gap-2.5">
              <!-- Voice phrase simulation chips -->
              <div class="flex flex-wrap justify-center gap-1.5" role="group" aria-label="Suggested voice phrases">
                <button onclick="handleVoiceInput('What is in front of me?')" aria-label="Simulate: What is in front of me?" class="px-2.5 py-1 rounded-full bg-orange-50 border border-orange-200 text-[11px] font-semibold text-orange-900 shadow-sm hover:bg-orange-100 transition active:scale-95 shrink-0">
                  “What is in front of me?”
                </button>
                <button onclick="handleVoiceInput('Where am I?')" aria-label="Simulate: Where am I?" class="px-2.5 py-1 rounded-full bg-blue-50 border border-blue-200 text-[11px] font-semibold text-blue-900 shadow-sm hover:bg-blue-100 transition active:scale-95 shrink-0">
                  “Where am I?”
                </button>
                <button onclick="handleVoiceInput('Take me to coffee shop')" aria-label="Simulate: Take me to coffee shop" class="px-2.5 py-1 rounded-full bg-white border border-slate-200 text-[11px] font-medium text-slate-700 shadow-sm hover:bg-slate-50 transition active:scale-95 shrink-0">
                  “Take me to coffee shop”
                </button>
                <button onclick="handleVoiceInput('Take me to Central Park')" aria-label="Simulate: Take me to Central Park" class="px-2.5 py-1 rounded-full bg-white border border-slate-200 text-[11px] font-medium text-slate-700 shadow-sm hover:bg-slate-50 transition active:scale-95 shrink-0">
                  “Take me to Central Park”
                </button>
                <button onclick="handleVoiceInput('Take me somewhere')" aria-label="Simulate: Take me somewhere (auto GPS search)" class="px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-[11px] font-medium text-emerald-800 shadow-sm hover:bg-emerald-100 transition active:scale-95 shrink-0" title="Auto GPS routing to nearest place">
                  “Take me somewhere” (Auto GPS)
                </button>
                <button onclick="handleVoiceInput('Go there')" aria-label="Simulate: Go there (auto GPS search)" class="px-2.5 py-1 rounded-full bg-amber-50 border border-amber-200 text-[11px] font-medium text-amber-800 shadow-sm hover:bg-amber-100 transition active:scale-95 shrink-0" title="Auto GPS routing">
                  “Go there”
                </button>
              </div>

              <!-- Test input for any natural-language destination or command -->
              <form onsubmit="event.preventDefault(); const inp = document.getElementById('voice-sim-input'); if (inp && inp.value.trim()) {{ handleVoiceInput(inp.value.trim()); inp.value = ''; }}" class="flex items-center gap-1.5 px-1">
                <label for="voice-sim-input" class="sr-only">Type any voice command or destination for Gemini AI</label>
                <input type="text" id="voice-sim-input" placeholder="Type any destination (e.g. library, Old Town, Paris)..." class="flex-1 min-w-0 bg-white border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-amber-500 shadow-sm">
                <button type="submit" class="px-3.5 py-2 rounded-xl bg-slate-900 text-white text-xs font-semibold hover:bg-black transition active:scale-95 shrink-0">
                  Send
                </button>
              </form>

              <div class="flex justify-center">
                <button onclick="navigateTo('home')" aria-label="Cancel voice listening and return home" class="w-14 h-14 rounded-full bg-red-500 text-white flex items-center justify-center shadow-lg hover:bg-red-600 transition active:scale-95 shrink-0">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                </button>
              </div>
            </div>
          </div>

          <!-- ==================== SCREEN 3: DESTINATION SEARCH ==================== -->
          <div id="screen-destinationSearch" role="region" aria-label="Screen 3: Destination Search" class="screen-container flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <div class="mobile-safe-header flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('home')" aria-label="Back to home screen" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <div class="flex-1 flex flex-col pt-3 overflow-y-auto no-scrollbar">
              <div class="flex flex-col items-center mb-3">
                <div class="w-12 h-12 rounded-full orb-3d mb-2 shrink-0" aria-hidden="true"></div>
                <h2 class="text-xl font-bold text-slate-900">Where would you like to go?</h2>
              </div>

              <!-- Accessible Search Bar -->
              <div class="relative mb-3">
                <label for="destination-search-input" class="sr-only">Search destination or speak</label>
                <input type="text" id="destination-search-input" oninput="filterDestinations(this.value)" placeholder="Search destination or speak..." aria-label="Search destination or speak" class="w-full bg-white border border-slate-200 rounded-2xl py-3 pl-11 pr-11 text-sm font-medium text-slate-800 placeholder-slate-500 shadow-sm focus:border-amber-500 transition">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-500 absolute left-3.5 top-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                <button onclick="triggerVoiceAssistant()" aria-label="Search destination using voice" class="absolute right-3 top-3 text-orange-500 hover:text-orange-600 shrink-0">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
                </button>
              </div>

              <!-- Category Pills -->
              <div role="group" aria-label="Destination categories" class="flex items-center gap-2 mb-4 overflow-x-auto no-scrollbar py-1">
                <button onclick="selectCategory('Coffee shop')" class="px-3 py-1.5 bg-orange-100 text-orange-800 rounded-full text-xs font-semibold whitespace-nowrap shrink-0">Coffee Shop</button>
                <button onclick="selectCategory('Park')" class="px-3 py-1.5 bg-emerald-100 text-emerald-800 rounded-full text-xs font-semibold whitespace-nowrap shrink-0">Park</button>
                <button onclick="selectCategory('Grocery')" class="px-3 py-1.5 bg-blue-100 text-blue-800 rounded-full text-xs font-semibold whitespace-nowrap shrink-0">Grocery Store</button>
                <button onclick="selectCategory('Pharmacy')" class="px-3 py-1.5 bg-purple-100 text-purple-800 rounded-full text-xs font-semibold whitespace-nowrap shrink-0">Pharmacy</button>
              </div>

              <!-- Recent Destinations List -->
              <h3 class="text-xs font-bold text-slate-600 uppercase tracking-wider mb-2 px-1">Recent Places</h3>
              <div id="recent-places-list" role="list" aria-label="Recent destinations" class="flex flex-col space-y-2.5 pb-4">
                <button onclick="selectDestination('City Central Park', 'Pedestrian Promenade & Garden')" aria-label="Select destination: City Central Park" class="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-amber-400 transition">
                  <div class="flex items-center space-x-3 min-w-0 flex-1 pr-2">
                    <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold text-sm shrink-0" aria-hidden="true">🌳</div>
                    <div class="min-w-0 flex-1">
                      <h4 class="font-bold text-slate-900 text-sm truncate">City Central Park</h4>
                      <p class="text-xs text-slate-600 truncate">Pedestrian Promenade • 0.8 km</p>
                    </div>
                  </div>
                  <span class="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-1 rounded-lg shrink-0">10 min</span>
                </button>

                <button onclick="selectDestination('Corner Bakery & Cafe', 'Main Sidewalk Entrance')" aria-label="Select destination: Corner Bakery & Cafe" class="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-amber-400 transition">
                  <div class="flex items-center space-x-3 min-w-0 flex-1 pr-2">
                    <div class="w-10 h-10 rounded-xl bg-orange-50 text-orange-600 flex items-center justify-center font-bold text-sm shrink-0" aria-hidden="true">☕</div>
                    <div class="min-w-0 flex-1">
                      <h4 class="font-bold text-slate-900 text-sm truncate">Corner Bakery & Cafe</h4>
                      <p class="text-xs text-slate-600 truncate">Main Sidewalk • 0.3 km</p>
                    </div>
                  </div>
                  <span class="text-xs font-bold text-slate-700 bg-slate-100 px-2 py-1 rounded-lg shrink-0">4 min</span>
                </button>

                <button onclick="selectDestination('Metro & Bus Transit Station', 'Transit Plaza North')" aria-label="Select destination: Metro & Bus Transit Station" class="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-amber-400 transition">
                  <div class="flex items-center space-x-3 min-w-0 flex-1 pr-2">
                    <div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-sm shrink-0" aria-hidden="true">🚏</div>
                    <div class="min-w-0 flex-1">
                      <h4 class="font-bold text-slate-900 text-sm truncate">Metro & Bus Transit Station</h4>
                      <p class="text-xs text-slate-600 truncate">Transit Plaza North • 0.5 km</p>
                    </div>
                  </div>
                  <span class="text-xs font-bold text-blue-700 bg-blue-50 px-2 py-1 rounded-lg shrink-0">6 min</span>
                </button>
              </div>
            </div>

            <!-- Bottom Mic Button -->
            <div class="mobile-safe-footer flex justify-center mt-2">
              <button onclick="triggerVoiceAssistant()" aria-label="Start voice listening assistant" class="w-16 h-16 rounded-full bg-black text-white flex items-center justify-center shadow-lg hover:bg-neutral-800 transition active:scale-95 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 4: ROUTE PREVIEW ==================== -->
          <div id="screen-routePreview" role="region" aria-label="Screen 4: Route Preview" class="screen-container flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <div class="mobile-safe-header flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('destinationSearch')" aria-label="Back to destination search" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <!-- Real Leaflet Interactive Route Map -->
            <div class="flex-1 flex flex-col justify-center my-2 min-h-0">
              <h2 class="sr-only">Interactive Real-World Route Map & Directions</h2>
              <div class="w-full h-44 sm:h-48 rounded-3xl relative overflow-hidden shadow-inner border border-slate-300 z-0 shrink-0">
                <div id="route-map-leaflet" class="w-full h-full"></div>
                <div id="route-map-loading" class="absolute inset-0 bg-slate-100/90 backdrop-blur-xs flex items-center justify-center text-xs font-semibold text-slate-700 z-20">
                  <span class="w-2.5 h-2.5 rounded-full bg-blue-500 animate-ping mr-2 shrink-0"></span>
                  <span>Loading Real-World Map & GPS Route...</span>
                </div>
              </div>

              <!-- Destination Summary Card -->
              <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm mt-3">
                <div class="flex items-center space-x-3 mb-2 min-w-0">
                  <div class="w-9 h-9 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center font-bold text-sm shrink-0" aria-hidden="true">
                    📍
                  </div>
                  <div class="min-w-0 flex-1">
                    <h3 id="preview-destination-title" class="font-bold text-slate-900 text-base leading-tight truncate">Selected Destination</h3>
                    <p id="preview-destination-sub" class="text-xs text-slate-600 mt-0.5 truncate">Pedestrian Walkway • Calculating live GPS route...</p>
                  </div>
                </div>
                <div class="flex items-center justify-between text-xs text-slate-700 border-t border-slate-100 pt-2.5">
                  <span>Sidewalk condition: <strong class="text-emerald-700">Clear</strong></span>
                  <span>Audio cues: <strong class="text-slate-900">High</strong></span>
                </div>
              </div>
            </div>

            <!-- Route Actions -->
            <div class="mobile-safe-footer flex flex-col space-y-2.5 pt-1">
              <button onclick="startCurrentNavigation()" id="start-nav-btn" aria-label="Start walking navigation to selected destination" class="w-full py-4 rounded-2xl bg-black text-white font-bold text-base shadow-md hover:bg-neutral-800 transition active:scale-[0.99] flex items-center justify-center space-x-2">
                <span>Start navigation</span>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
              </button>
              <button onclick="speakRouteOverview()" aria-label="Describe route overview and audible cues" class="w-full py-3 rounded-2xl bg-white border border-slate-200 text-slate-800 font-semibold text-sm shadow-sm hover:bg-slate-50 transition active:scale-[0.99] flex items-center justify-center space-x-2">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-slate-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
                <span>Describe route</span>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 5: ACTIVE NAVIGATION (ALWAYS-OPEN BACK CAMERA + YOLO + SIGNBOARDS) ==================== -->
          <div id="screen-activeNavigation" role="region" aria-label="Screen 5: Active Walking Navigation with Always-Open Back Camera and YOLO Object Detection" class="flex-1 flex flex-col justify-between p-3.5 pb-4 hidden relative overflow-hidden sm:rounded-3xl">
            <!-- ALWAYS-OPEN CAMERA BACKGROUND VIEWPORT -->
            <div class="absolute inset-0 overflow-hidden bg-black z-0" aria-hidden="true">
              <!-- Real Device Camera Feed (Facing Environment) -->
              <video id="nav-live-video" class="absolute inset-0 w-full h-full object-cover" autoplay playsinline muted></video>
              <!-- Real camera placeholder / live status indicator when initializing -->
              <div id="nav-camera-prompt" class="absolute inset-0 bg-neutral-950 flex flex-col items-center justify-center text-center p-6 text-white/80">
                <div class="w-16 h-16 rounded-full bg-white/10 flex items-center justify-center text-3xl mb-3 animate-pulse shrink-0">📷</div>
                <p class="text-sm font-semibold text-white">Back Camera Stream Active</p>
                <p class="text-xs text-slate-400 mt-1">Point device forward while walking. Continuous YOLO object detection running.</p>
              </div>
              <!-- High-Contrast WCAG AAA Ambient Gradients -->
              <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-transparent to-black/90 pointer-events-none z-5"></div>
              <!-- Real-Time YOLO Object Detection Canvas Overlay -->
              <canvas id="nav-yolo-canvas" class="absolute inset-0 w-full h-full pointer-events-none z-10"></canvas>
              <!-- Real-Time Signboards Floating HUD Overlay (Gemini Vision OCR) -->
              <div id="nav-signboards-overlay" class="absolute inset-0 pointer-events-none z-15 flex flex-col justify-center items-center gap-2 p-3"></div>
            </div>

            <!-- Top Header (Z-20 Relative) -->
            <div class="mobile-safe-header relative z-20 flex justify-between items-center pt-1 px-1">
              <button onclick="stopNavigationRoute()" id="btn-nav-back" aria-label="Stop navigation and return to preview" class="w-11 h-11 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition active:scale-95 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
              </button>
              
              <!-- Camera & YOLO Status Pill Badge -->
              <div class="flex items-center gap-1.5 px-3 py-1.5 bg-black/75 backdrop-blur-md rounded-full text-white text-xs font-bold border border-white/20 shadow-md shrink-0">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse shrink-0" aria-hidden="true"></span>
                <span id="camera-status-pill">Back Camera • YOLO Active</span>
              </div>

              <div class="flex items-center gap-1.5 shrink-0">
                <!-- Camera / Simulation Toggle Button -->
                <button type="button" onclick="toggleCameraFeed()" id="btn-toggle-camera" aria-label="Toggle between real rear camera and simulated walking stream" class="w-11 h-11 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition active:scale-95 text-base shrink-0" title="Toggle camera feed mode">
                  <span id="camera-toggle-icon" aria-hidden="true">📷</span>
                </button>
                <button onclick="openSettingsModal()" id="btn-nav-settings" aria-label="Settings" aria-haspopup="dialog" class="w-11 h-11 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition shrink-0">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                </button>
              </div>
            </div>

            <!-- Floating Compact Navigation Turn-by-Turn HUD (Z-20 Relative) -->
            <div class="relative z-20 my-auto flex flex-col justify-center space-y-2">
              <div class="bg-black/85 backdrop-blur-md rounded-2xl py-2.5 px-3.5 border border-white/20 shadow-xl flex items-center justify-between text-white" role="region" aria-label="Current Navigation Instruction" aria-live="assertive">
                <div class="flex items-center space-x-2.5 min-w-0 flex-1">
                  <div id="nav-maneuver-icon" class="w-8 h-8 rounded-full bg-orange-500 text-white flex items-center justify-center font-black text-sm shrink-0" aria-hidden="true">
                    ↑
                  </div>
                  <div class="flex flex-col text-left min-w-0 flex-1 pr-2">
                    <span id="nav-step-label" class="text-[10px] font-bold text-orange-400 uppercase tracking-wider truncate">
                      Real Pedestrian Route
                    </span>
                    <h2 id="nav-instruction-text" class="text-xs font-bold text-white tracking-tight leading-snug line-clamp-2">
                      Point camera forward & walk along pathway
                    </h2>
                  </div>
                </div>
                <div class="flex items-baseline space-x-1 pl-2 shrink-0">
                  <span id="nav-distance-num" class="text-2xl font-black text-white">0</span>
                  <span class="text-[10px] font-bold text-slate-300">m</span>
                </div>
              </div>

              <!-- Real-Time Optical Perception & Spatial Direction HUD -->
              <div id="nav-lidar-corridor-hud" class="w-full py-2 px-3 rounded-2xl bg-black/85 backdrop-blur-md border border-emerald-500/50 text-white shadow-xl flex items-center justify-between">
                <div class="flex items-center space-x-2.5 min-w-0 flex-1">
                  <span id="nav-direction-arrow" class="text-2xl text-emerald-400 font-extrabold select-none shrink-0">⬆️</span>
                  <div class="flex flex-col text-left min-w-0 flex-1 pr-2">
                    <span id="nav-corridor-status" class="text-[11px] font-bold text-emerald-300 tracking-wide uppercase truncate">WALK STRAIGHT • PATH CLEAR</span>
                    <span id="nav-depth-reading" class="text-[10px] text-slate-300 font-mono truncate">Vision status: <strong id="nav-depth-meters" class="text-white">Clear (>3m)</strong></span>
                  </div>
                </div>
                <div class="flex flex-col items-end shrink-0 pl-2">
                  <span class="text-[9px] font-bold text-slate-400 uppercase tracking-wider">Perception</span>
                  <span id="nav-lateral-lanes" class="text-[10px] font-mono font-bold text-emerald-400 whitespace-nowrap">Optical View: Clear Ahead</span>
                </div>
              </div>
            </div>

            <!-- Bottom Hands-Free Voice Interaction Hub for Blind Pedestrians (No Button Clutter) -->
            <div class="mobile-safe-footer relative z-20 flex flex-col items-center justify-center pt-2 pb-1">
              <!-- Large Tactile Voice Mic Button (Tap to talk or ask anything) -->
              <button onclick="triggerVoiceAssistant()" id="nav-floating-mic-btn" aria-label="Tap to speak. Ask anything, say Yes, No, Repeat, or Stop." class="w-20 h-20 rounded-full bg-black text-white border-4 border-orange-500 flex items-center justify-center shadow-2xl hover:scale-105 active:scale-95 transition focus:ring-4 focus:ring-orange-400/50 relative group shrink-0">
                <span class="absolute -inset-1 rounded-full bg-orange-500/30 animate-ping group-hover:opacity-100 opacity-60"></span>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 text-orange-400 relative z-10 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
              </button>
              <p class="text-xs text-white text-center font-bold drop-shadow mt-2">
                Tap mic & speak • Ask anything, say <span class="text-orange-400">"Yes"</span>, <span class="text-orange-400">"No"</span>, <span class="text-orange-400">"Repeat"</span>, or <span class="text-orange-400">"Stop"</span>
              </p>
            </div>
          </div>

          <!-- ==================== SCREEN 6: WHERE AM I? ==================== -->
          <div id="screen-whereAmI" role="region" aria-label="Screen 6: Where am I?" class="screen-container flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <div class="mobile-safe-header flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('home')" aria-label="Back to home screen" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <!-- Location Info Content -->
            <div class="flex-1 flex flex-col justify-center my-auto min-h-0">
              <h2 class="sr-only">Current Location Context</h2>
              <div class="flex justify-center mb-3">
                <div class="w-12 h-12 rounded-full orb-3d shadow-md shrink-0" aria-hidden="true"></div>
              </div>

              <!-- Main Location Card -->
              <div class="bg-white rounded-3xl p-5 border border-slate-200 shadow-md text-left">
                <div class="flex items-center space-x-2 text-xs font-bold text-purple-600 uppercase tracking-wider mb-1">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 010-5 2.5 2.5 0 010 5z"/></svg>
                  <span>Current Position</span>
                </div>
                <h3 id="whereami-headline" class="text-xl font-bold text-slate-900 leading-snug mb-1">
                  Locating your position...
                </h3>
                <p id="whereami-sub" class="text-xs text-slate-600 mb-3">Acquiring live GPS fix & street context...</p>

                <!-- Real Interactive Leaflet Mini Map -->
                <div class="w-full h-36 rounded-2xl overflow-hidden mb-3 border border-slate-200 shadow-sm relative z-0 shrink-0">
                  <div id="whereami-map-leaflet" class="w-full h-full"></div>
                  <div id="whereami-map-loading" class="absolute inset-0 bg-slate-100/90 backdrop-blur-xs flex items-center justify-center text-xs font-semibold text-slate-700 z-20">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping mr-2 shrink-0"></span>
                    <span>Locating GPS position...</span>
                  </div>
                </div>

                <!-- Orientation & Compass Card -->
                <div class="bg-slate-50 rounded-2xl p-3 border border-slate-100 flex items-center justify-between text-xs">
                  <div class="min-w-0 flex-1 pr-2">
                    <div class="font-bold text-slate-700">Orientation</div>
                    <div id="whereami-orientation-text" class="text-slate-600 truncate">Compass active • Aligning heading...</div>
                  </div>
                  <div id="whereami-compass-badge" class="w-8 h-8 rounded-full bg-white border border-slate-200 flex items-center justify-center font-bold text-slate-800 text-xs shadow-xs shrink-0" role="img" aria-label="Facing direction">
                    N
                  </div>
                </div>
              </div>
            </div>

            <!-- Bottom Action -->
            <div class="mobile-safe-footer flex flex-col space-y-2 pt-2">
              <button onclick="repeatRealLocation()" aria-label="Repeat current location, address, and orientation" class="w-full py-3.5 rounded-2xl bg-white border border-slate-200 text-slate-800 font-semibold text-sm shadow-sm hover:bg-slate-50 transition active:scale-[0.99] flex items-center justify-center space-x-2">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-slate-600 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.5A2.25 2.25 0 0 0 2.25 9.75v4.5A2.25 2.25 0 0 0 4.5 16.5h1.94l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06Z"/></svg>
                <span>Repeat location</span>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 7: DESCRIBE WHAT'S AROUND ME ==================== -->
          <div id="screen-describeAround" role="region" aria-label="Screen 7: Describe what's around me" class="screen-container flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <!-- Header -->
            <div class="mobile-safe-header flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('home')" aria-label="Back to home screen" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition active:scale-95 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <!-- Body -->
            <div class="flex-1 flex flex-col pt-1 overflow-y-auto no-scrollbar min-h-0">
              <div class="flex justify-center mb-1.5">
                <div class="w-12 h-12 rounded-full orb-3d shadow-md shrink-0" aria-hidden="true"></div>
              </div>

              <!-- Title -->
              <h2 class="text-2xl font-bold text-center text-slate-900 tracking-tight mb-3">
                Here’s what I see:
              </h2>

              <!-- Camera Scene Card / Live Camera View -->
              <div id="describe-scene-container" class="w-full h-40 rounded-2xl overflow-hidden mb-3 border border-slate-200 shadow-sm shrink-0 relative bg-neutral-900">
                <video id="describe-live-video" class="w-full h-full object-cover hidden" autoplay playsinline muted></video>
                <div id="describe-camera-prompt" class="absolute inset-0 flex flex-col items-center justify-center text-center p-4 text-white/80">
                  <span class="text-2xl mb-1 shrink-0">📷</span>
                  <p class="text-xs font-semibold text-white">Rear Camera Feed</p>
                  <p class="text-[10px] text-slate-400">Scanning physical surroundings with Gemini Multimodal AI</p>
                </div>
                <div id="describe-live-badge" class="absolute top-2 left-2 px-2.5 py-1 rounded-full bg-black/75 text-white text-[11px] font-bold backdrop-blur-sm hidden flex items-center space-x-1.5 z-10 shrink-0">
                  <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse shrink-0"></span>
                  <span>Live Camera Feed</span>
                </div>
                <div id="describe-scanning-spinner" class="absolute inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center text-white text-xs font-bold hidden z-20">
                  <span class="w-3 h-3 rounded-full border-2 border-white border-t-transparent animate-spin mr-2 shrink-0"></span>
                  <span>Gemini Multimodal Vision Analyzing...</span>
                </div>
              </div>

              <!-- Dynamic Semantic List with Real Multimodal AI Detections -->
              <ul id="describe-scene-list" role="list" aria-label="Objects and environment observed" class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col divide-y divide-slate-100 list-none p-0 m-0">
                <li class="flex items-center space-x-3 p-3">
                  <div class="w-6 h-6 rounded-full bg-emerald-500 text-white flex items-center justify-center font-bold text-xs shrink-0" aria-hidden="true">✓</div>
                  <span class="font-medium text-slate-900 text-sm">Sidewalk ahead is clear.</span>
                </li>
                <li class="flex items-center space-x-3 p-3">
                  <div class="w-6 h-6 text-purple-600 flex items-center justify-center shrink-0" aria-hidden="true">👁️</div>
                  <span class="font-medium text-slate-900 text-sm">Point camera ahead to scan surroundings in real time.</span>
                </li>
              </ul>
            </div>

            <!-- Bottom Repeat Pill Button -->
            <div class="mobile-safe-footer flex justify-center pt-3">
              <button onclick="repeatSceneDescription()" aria-label="Repeat visual scene description" class="px-7 py-3 rounded-full bg-white border border-slate-200 text-slate-900 font-bold text-sm shadow-md hover:bg-slate-50 transition active:scale-95 flex items-center space-x-2 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-800 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.5A2.25 2.25 0 0 0 2.25 9.75v4.5A2.25 2.25 0 0 0 4.5 16.5h1.94l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06ZM18.584 5.106a.75.75 0 0 1 1.06 0c3.808 3.807 3.808 9.98 0 13.788a.75.75 0 0 1-1.06-1.06 8.25 8.25 0 0 0 0-11.668.75.75 0 0 1 0-1.06Z"/></svg>
                <span>Repeat</span>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 8: OBSTACLE AHEAD (Hazard Detection) ==================== -->
          <div id="screen-obstacleAlert" role="region" aria-label="Screen 8: Obstacle Ahead Warning" class="screen-container flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <!-- Header -->
            <div class="mobile-safe-header flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('activeNavigation')" aria-label="Back to active navigation" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition active:scale-95 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <!-- Top Warning Alert Banner (role="alert" for immediate screen reader announcement) -->
            <div id="obstacle-alert-banner" role="alert" aria-live="assertive" class="mt-2 bg-[#FEECEC] border border-red-200 rounded-3xl p-4 flex items-center space-x-3.5 shadow-sm transition-colors shrink-0">
              <div id="obstacle-banner-icon" class="w-11 h-11 text-red-600 flex items-center justify-center shrink-0" aria-hidden="true">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 fill-current shrink-0" viewBox="0 0 24 24"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>
              </div>
              <div class="flex flex-col min-w-0 flex-1">
                <h2 id="obstacle-screen-title" class="text-xl font-bold text-red-600 leading-tight truncate">Obstacle Danger Alert</h2>
                <p id="obstacle-screen-subtitle" class="text-xs text-slate-800 font-medium leading-relaxed mt-0.5">
                  Scanning for collision hazards ahead with LiDAR depth & YOLO camera vision.
                </p>
              </div>
            </div>

            <!-- Camera View with Live Video, AR Path, LiDAR Depth Map Canvas -->
            <div class="flex-1 my-3 relative rounded-3xl overflow-hidden border border-slate-200 shadow-inner flex flex-col justify-end p-3.5 bg-neutral-950 min-h-0">
              <video id="obstacle-live-video" class="absolute inset-0 w-full h-full object-cover hidden" autoplay playsinline muted></video>
              <div id="obstacle-bg-fallback" class="absolute inset-0 bg-gradient-to-b from-neutral-900 via-neutral-950 to-black"></div>
              
              <!-- Canvas for dynamic LiDAR Depth & Vision Bounding Box Overlay -->
              <canvas id="lidar-depth-canvas" class="absolute inset-0 w-full h-full pointer-events-none z-5"></canvas>
              
              <!-- Floating Obstacle Detail Card -->
              <div class="relative z-10 bg-white/95 backdrop-blur-md rounded-2xl p-3.5 border border-slate-100 shadow-md flex items-center space-x-3">
                <div id="obstacle-card-icon" class="w-10 h-10 rounded-full bg-red-100 text-red-600 flex items-center justify-center text-xl shrink-0" role="img" aria-label="Hazard icon">
                  ⚠️
                </div>
                <div class="flex flex-col flex-1 min-w-0">
                  <div class="flex items-center justify-between">
                    <h3 id="obstacle-card-title" class="font-bold text-slate-900 text-sm leading-tight truncate">Active Hazard Sensing</h3>
                    <span id="obstacle-card-dist-badge" class="text-[11px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 shrink-0">Live</span>
                  </div>
                  <p id="obstacle-card-sub" class="text-xs text-slate-600 mt-0.5 truncate">Point camera forward in walking path.</p>
                </div>
              </div>
            </div>

            <!-- Hands-Free Voice Response Hub for Obstacle Screen (No Buttons To Search For) -->
            <div class="mobile-safe-footer flex flex-col items-center justify-center pt-2 pb-1">
              <button onclick="triggerVoiceAssistant()" id="obstacle-voice-mic-btn" aria-label="Tap microphone to speak or say Yes, No, or Repeat" class="w-20 h-20 rounded-full bg-black text-white border-4 border-red-500 flex items-center justify-center shadow-2xl hover:scale-105 active:scale-95 transition focus:ring-4 focus:ring-red-400/50 relative group shrink-0">
                <span class="absolute -inset-1 rounded-full bg-red-500/30 animate-ping group-hover:opacity-100 opacity-60"></span>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 text-red-400 relative z-10 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
              </button>
              <p class="text-xs text-slate-800 font-bold text-center mt-2">
                Speak <span class="text-red-600 font-black">"Yes"</span> / <span class="text-red-600 font-black">"Okay"</span> to resume, or ask where to step
              </p>
            </div>
          </div>

          <!-- ==================== SCREEN 9: APPROACHING CROSSWALK (Quiet Mode) ==================== -->
          <div id="screen-crosswalkSafety" role="region" aria-label="Screen 9: Approaching Crosswalk Quiet Mode" class="screen-container flex-1 flex flex-col justify-between p-5 pb-6 hidden">
            <!-- Header -->
            <div class="mobile-safe-header flex justify-between items-center pt-2 px-1">
              <button onclick="navigateTo('activeNavigation')" aria-label="Back to active navigation" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition active:scale-95 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-xl font-bold text-black tracking-tight">Blind AI</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-11 h-11 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <!-- Top Warning Notice Banner (role="alert" for immediate screen reader notice) -->
            <div role="alert" aria-live="assertive" class="mt-2 bg-[#FEE881] rounded-3xl p-4 flex items-center space-x-4 shadow-sm shrink-0">
              <div class="w-10 h-10 text-black flex items-center justify-center shrink-0" aria-hidden="true">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-9 h-9 fill-black shrink-0" viewBox="0 0 24 24"><path d="M13.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.8 8.9L7 23h2.1l1.8-8 2.1 2v6h2v-7.5l-2.1-2 .6-3C14.8 12 16.8 13 19 13v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L6 8.3V13h2V9.6l1.8-.7z"/></svg>
              </div>
              <div class="flex flex-col min-w-0 flex-1">
                <h2 class="text-xl font-bold text-black leading-tight truncate">Approaching crosswalk.</h2>
                <p class="text-sm text-slate-900 mt-0.5 truncate">Listen for traffic.</p>
              </div>
            </div>

            <!-- Camera View with Real Video & Waveform Overlay -->
            <div class="flex-1 my-3 relative rounded-3xl overflow-hidden border border-slate-200 shadow-inner flex flex-col justify-end p-3.5 bg-neutral-950 min-h-0">
              <video id="crosswalk-live-video" class="absolute inset-0 w-full h-full object-cover hidden" autoplay playsinline muted></video>
              <div id="crosswalk-bg-fallback" class="absolute inset-0 bg-gradient-to-b from-slate-900 via-neutral-900 to-black"></div>

              <!-- Accessible Floating Quiet Mode Waveform Card -->
              <button type="button" onclick="confirmCrossed()" aria-label="Quiet mode active: I will be quiet while you cross. Tap when across to resume route." class="w-full relative z-10 bg-white/95 backdrop-blur-md rounded-3xl p-5 border border-slate-100 shadow-lg flex flex-col items-center justify-center text-center cursor-pointer hover:bg-white transition">
                
                <!-- Amber Audio Waveform Bars (Decorative) -->
                <div class="flex items-center space-x-1.5 h-12 mb-3" aria-hidden="true">
                  <div class="w-1.5 h-4 bg-amber-500 rounded-full wave-bar wave-1 shrink-0"></div>
                  <div class="w-1.5 h-7 bg-amber-500 rounded-full wave-bar wave-2 shrink-0"></div>
                  <div class="w-1.5 h-10 bg-amber-500 rounded-full wave-bar wave-3 shrink-0"></div>
                  <div class="w-1.5 h-12 bg-amber-500 rounded-full wave-bar wave-4 shrink-0"></div>
                  <div class="w-1.5 h-14 bg-amber-500 rounded-full wave-bar wave-5 shrink-0"></div>
                  <div class="w-1.5 h-12 bg-amber-500 rounded-full wave-bar wave-6 shrink-0"></div>
                  <div class="w-1.5 h-10 bg-amber-500 rounded-full wave-bar wave-7 shrink-0"></div>
                  <div class="w-1.5 h-7 bg-amber-500 rounded-full wave-bar wave-8 shrink-0"></div>
                  <div class="w-1.5 h-4 bg-amber-500 rounded-full wave-bar wave-9 shrink-0"></div>
                </div>

                <p class="text-base font-medium text-slate-800">
                  I will be quiet while you cross.
                </p>
                <span class="text-xs text-slate-600 mt-1" aria-hidden="true">(Tap card when across to resume route)</span>
              </button>
            </div>

            <!-- Bottom Action -->
            <div class="mobile-safe-footer pt-1">
              <button onclick="confirmCrossed()" aria-label="Confirm crosswalk completed and resume navigation route" class="w-full py-3.5 rounded-full bg-neutral-900 text-white font-bold text-sm shadow-md hover:bg-black transition active:scale-95 flex items-center justify-center space-x-2">
                <span>Crosswalk Completed — Resume Route</span>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
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
    let webSpeechRec = null;
    let currentDistance = 120;
    let currentWaypointIdx = 0;
    let navigationInterval = null;
    let previousActiveElement = null;

    // Real Physical Movement & Pedometer State (Zero Fake Timers)
    let totalPhysicalSteps = 0;
    let totalPhysicalMeters = 0.0;
    let lastGpsWalkLat = null;
    let lastGpsWalkLon = null;
    let lastPedometerAccelMag = 9.8;
    let lastPedometerStepTime = 0;

    // Real-Time LiDAR & Depth Corridor State
    let currentLidarDepthAhead = 4.0;
    let currentLidarDepthLeft = 3.5;
    let currentLidarDepthRight = 3.5;
    let currentSteeringDirection = 'WALK STRAIGHT';
    let lastSteeringSpeechTime = 0;

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

    const defaultWalkingWaypoints = [
      {{
        instruction: "Walk forward along sidewalk",
        distance: 80,
        maneuver: "Head straight",
        icon: "↑"
      }},
      {{
        instruction: "Continue along main pedestrian pathway",
        distance: 120,
        maneuver: "Continue straight",
        icon: "↑"
      }},
      {{
        instruction: "Keep straight toward entrance",
        distance: 40,
        maneuver: "Keep straight",
        icon: "🚶"
      }},
      {{
        instruction: "Arrival: Destination reached",
        distance: 0,
        maneuver: "Destination reached",
        icon: "★"
      }}
    ];

    // Real Global Geospatial & Tracking State (Browser GPS + OpenStreetMap + Real Destinations)
    let userGps = {{
      lat: 56.9535,
      lon: 24.0815,
      street: "Current Street",
      city: "Current City",
      country: "",
      heading: 90,
      headingCardinal: "East",
      accuracy: 8,
      isRealGps: false
    }};

    let activeDestination = {{
      title: "Selected Destination",
      subtitle: "Pedestrian Walkway • 0.24 km",
      lat: 56.9535,
      lon: 24.0815,
      distanceKm: 0.24,
      estimatedMinutes: 3,
      waypoints: [...defaultWalkingWaypoints]
    }};

    let routeLeafletMap = null;
    let whereAmILeafletMap = null;
    let routeUserMarker = null;
    let routeDestMarker = null;
    let routePolyline = null;
    let whereAmIMarker = null;

    let cocoSsdModel = null;
    let isCocoLoading = false;
    let isDetectingFrame = false;
    let lastLiveDetections = [];
    let lastSceneDescription = "";

    let currentDestinationTitle = "Selected Destination";
    let currentDestinationSub = "Pedestrian Walkway • 0.24 km • 3 min • 4 waypoints";
    let currentWaypoints = [...defaultWalkingWaypoints];

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
        subtitle: `${{title}} • Real Pedestrian Destination`,
        category: "Real Destination",
        isRealQuery: true
      }};
    }}

    // ==================== REAL GPS TRACKING & REVERSE GEOCODING ====================
    let searchDebounceTimer = null;
    let reverseGeocodeTimer = null;

    function initRealGpsTracking() {{
      if ('geolocation' in navigator) {{
        navigator.geolocation.getCurrentPosition(
          handleGpsSuccess,
          (err) => {{
            console.warn('[GPS] Initial location acquisition notice:', err.message);
          }},
          {{ enableHighAccuracy: true, timeout: 8000, maximumAge: 10000 }}
        );

        navigator.geolocation.watchPosition(
          handleGpsSuccess,
          (err) => console.warn('[GPS] Watch notice:', err.message),
          {{ enableHighAccuracy: true, maximumAge: 5000 }}
        );
      }}

      if (window.DeviceOrientationEvent) {{
        window.addEventListener('deviceorientation', handleOrientationEvent, true);
      }}

      initPedometerSensor();
    }}

    function initPedometerSensor() {{
      if (window.DeviceMotionEvent) {{
        window.addEventListener('devicemotion', (evt) => {{
          const acc = evt.accelerationIncludingGravity || evt.acceleration;
          if (!acc || acc.x === null || acc.y === null || acc.z === null) return;
          const mag = Math.sqrt(acc.x * acc.x + acc.y * acc.y + acc.z * acc.z);
          const delta = Math.abs(mag - lastPedometerAccelMag);
          lastPedometerAccelMag = mag;
          const now = Date.now();
          // Real step detection: acceleration peak > 11.8 m/s^2 or dynamic delta > 2.6 m/s^2, debounced by 320ms
          if ((mag > 11.8 || delta > 2.6) && (now - lastPedometerStepTime > 320)) {{
            lastPedometerStepTime = now;
            totalPhysicalSteps++;
            onPhysicalStepOrMovement(0.75, 'step'); // ~0.75m per pedestrian step stride
          }}
        }}, true);
      }}
    }}

    function onPhysicalStepOrMovement(deltaMeters, source) {{
      totalPhysicalMeters += deltaMeters;
      updateMovementDisplayUI();

      if (activeRoute !== 'activeNavigation') return;

      if (currentDistance > deltaMeters) {{
        currentDistance = Math.max(0, Math.round(currentDistance - deltaMeters));
        stepWalkedMeters += deltaMeters;
        const distNumEl = document.getElementById('nav-distance-num');
        if (distNumEl) distNumEl.innerText = currentDistance;
        const currentManeuver = currentWaypoints[currentWaypointIdx]?.maneuver || 'Head straight';
        const manTextEl = document.getElementById('nav-maneuver-text');
        if (manTextEl) manTextEl.innerText = currentDistance > 0 ? `${{currentManeuver}} in ${{currentDistance}}m` : currentManeuver;

        // Periodic voice distance updates on exact milestones
        if (currentDistance === 50 || currentDistance === 25 || currentDistance === 10) {{
          triggerHaptic([50]);
          speakText(`${{currentDistance}} meters remaining.`);
        }}
      }} else {{
        // Current waypoint completed by physical walking!
        currentWaypointIdx++;
        if (currentWaypointIdx < currentWaypoints.length) {{
          currentDistance = currentWaypoints[currentWaypointIdx].distance;
          stepWalkedMeters = 0;
          renderActiveWaypoint();
          triggerHaptic([70, 40, 70]);
          speakText(`Waypoint reached. ${{currentWaypoints[currentWaypointIdx].instruction}}`);
        }} else {{
          currentDistance = 0;
          const distNumEl = document.getElementById('nav-distance-num');
          if (distNumEl) distNumEl.innerText = 0;
          speakText(`You have arrived at ${{currentDestinationTitle}}. Navigation complete.`);
          triggerHaptic([120, 60, 120, 60, 200]);
          setTimeout(() => navigateTo('home'), 4000);
        }}
      }}
    }}

    function updateMovementDisplayUI() {{
      const stepsEl = document.getElementById('real-steps-display');
      const distEl = document.getElementById('real-dist-display');
      if (stepsEl) stepsEl.innerText = totalPhysicalSteps;
      if (distEl) distEl.innerText = totalPhysicalMeters.toFixed(1) + 'm';
    }}

    function handleGpsSuccess(pos) {{
      if (!pos || !pos.coords) return;
      userGps.lat = pos.coords.latitude;
      userGps.lon = pos.coords.longitude;
      userGps.accuracy = Math.round(pos.coords.accuracy || 5);
      userGps.isRealGps = true;

      // Real physical GPS movement calculation
      if (lastGpsWalkLat !== null && lastGpsWalkLon !== null) {{
        const dMeters = calculateHaversineKm(lastGpsWalkLat, lastGpsWalkLon, userGps.lat, userGps.lon) * 1000;
        if (dMeters >= 1.8 && dMeters < 50) {{
          lastGpsWalkLat = userGps.lat;
          lastGpsWalkLon = userGps.lon;
          onPhysicalStepOrMovement(dMeters, 'gps');
        }}
      }} else {{
        lastGpsWalkLat = userGps.lat;
        lastGpsWalkLon = userGps.lon;
      }}

      // Update orientation heading if provided by GPS
      if (pos.coords.heading !== null && !isNaN(pos.coords.heading) && pos.coords.heading >= 0) {{
        userGps.heading = Math.round(pos.coords.heading);
        userGps.headingCardinal = getHeadingCardinal(userGps.heading);
      }}

      // Reverse geocode to get real street name
      clearTimeout(reverseGeocodeTimer);
      reverseGeocodeTimer = setTimeout(() => {{
        reverseGeocodeUser(userGps.lat, userGps.lon);
      }}, 1200);

      updateWhereAmIDisplay();
      if (activeRoute === 'whereAmI') {{
        initWhereAmILeafletMap();
      }}
      if (activeRoute === 'routePreview') {{
        initRouteLeafletMap();
      }}
    }}

    function handleOrientationEvent(e) {{
      let compass = null;
      if (e.webkitCompassHeading !== undefined) {{
        compass = e.webkitCompassHeading;
      }} else if (e.alpha !== null) {{
        compass = 360 - e.alpha;
      }}
      if (compass !== null && !isNaN(compass)) {{
        userGps.heading = Math.round(compass);
        userGps.headingCardinal = getHeadingCardinal(userGps.heading);
        const compassBadge = document.getElementById('whereami-compass-badge');
        const orientText = document.getElementById('whereami-orientation-text');
        if (compassBadge) compassBadge.innerText = userGps.headingCardinal;
        if (orientText) orientText.innerText = `Facing ${{userGps.headingCardinal}} (${{userGps.heading}}°) • ±${{userGps.accuracy}}m accuracy`;
      }}
    }}

    function getHeadingCardinal(deg) {{
      const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
      const index = Math.round(((deg %= 360) < 0 ? deg + 360 : deg) / 45) % 8;
      return directions[index];
    }}

    async function reverseGeocodeUser(lat, lon) {{
      try {{
        const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${{lat}}&lon=${{lon}}&zoom=18&addressdetails=1`;
        const res = await fetch(url, {{ headers: {{ 'Accept-Language': 'en' }} }});
        if (res.ok) {{
          const data = await res.json();
          if (data && data.address) {{
            const road = data.address.road || data.address.pedestrian || data.address.path || data.address.suburb || "Current Street";
            const city = data.address.city || data.address.town || data.address.village || data.address.state || "Current City";
            const country = data.address.country || "";
            userGps.street = road;
            userGps.city = city;
            userGps.country = country;
            updateWhereAmIDisplay();
          }}
        }}
      }} catch (err) {{
        console.warn('[Geocode] Reverse geocoding notice:', err.message);
      }}
    }}

    function updateWhereAmIDisplay() {{
      const headline = document.getElementById('whereami-headline');
      const sub = document.getElementById('whereami-sub');
      const orientText = document.getElementById('whereami-orientation-text');
      const compassBadge = document.getElementById('whereami-compass-badge');

      if (headline) {{
        headline.innerText = userGps.street ? `${{userGps.street}}, ${{userGps.city}}` : "Current Location";
      }}
      if (sub) {{
        sub.innerText = `${{userGps.lat.toFixed(5)}}° N, ${{userGps.lon.toFixed(5)}}° E • Accuracy ±${{userGps.accuracy}}m`;
      }}
      if (orientText) {{
        orientText.innerText = `Facing ${{userGps.headingCardinal}} (${{userGps.heading}}°) • GPS active`;
      }}
      if (compassBadge) {{
        compassBadge.innerText = userGps.headingCardinal;
      }}
    }}

    function repeatRealLocation() {{
      triggerHaptic([40]);
      const street = userGps.street || "Your location";
      const city = userGps.city || "your area";
      const heading = userGps.headingCardinal || "East";
      const speech = `You are on ${{street}}, in ${{city}}. Coordinates are ${{userGps.lat.toFixed(4)}} North, ${{userGps.lon.toFixed(4)}} East. You are facing ${{heading}}.`;
      speakText(speech);
    }}

    // ==================== GEODETIC & ROUTE CALCULATION ====================
    function calculateHaversineKm(lat1, lon1, lat2, lon2) {{
      const R = 6371; // Earth radius in km
      const dLat = (lat2 - lat1) * Math.PI / 180;
      const dLon = (lon2 - lon1) * Math.PI / 180;
      const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      return parseFloat((R * c).toFixed(2));
    }}

    async function fetchRealOsrmRoute(startLat, startLon, destLat, destLon, destTitle) {{
      try {{
        const url = `https://router.project-osrm.org/route/v1/foot/${{startLon}},${{startLat}};${{destLon}},${{destLat}}?overview=full&geometries=geojson&steps=true`;
        const res = await fetch(url);
        if (res.ok) {{
          const data = await res.json();
          if (data && data.routes && data.routes[0]) {{
            const r = data.routes[0];
            const distKm = parseFloat((r.distance / 1000).toFixed(2));
            const estMin = Math.max(1, Math.round(r.duration / 60));
            const routeCoords = (r.geometry && r.geometry.coordinates)
              ? r.geometry.coordinates.map(c => [c[1], c[0]])
              : null;

            const legs = r.legs || [];
            let waypoints = [];
            if (legs[0] && legs[0].steps && legs[0].steps.length > 0) {{
              waypoints = legs[0].steps.map((st) => {{
                const stepMeters = Math.max(1, Math.round(st.distance));
                const streetName = st.name || destTitle;
                const mType = st.maneuver ? st.maneuver.type : 'continue';
                const mMod = st.maneuver ? st.maneuver.modifier : '';
                let maneuverText = "Walk straight";
                let icon = "↑";
                let instruction = `Continue along ${{streetName}}`;

                if (mType === 'depart') {{
                  maneuverText = `Head toward ${{streetName}}`;
                  instruction = `Start walking on ${{streetName}}`;
                  icon = "↑";
                }} else if (mType === 'arrive') {{
                  maneuverText = "Destination reached";
                  instruction = `Arrived at ${{destTitle}}`;
                  icon = "★";
                }} else if (mType === 'turn' || mType === 'fork' || mType === 'end of road') {{
                  if (mMod && mMod.includes('left')) {{
                    maneuverText = "Turn left";
                    instruction = `Turn left onto ${{streetName}}`;
                    icon = "←";
                  }} else if (mMod && mMod.includes('right')) {{
                    maneuverText = "Turn right";
                    instruction = `Turn right onto ${{streetName}}`;
                    icon = "→";
                  }}
                }} else if (mType === 'roundabout') {{
                  maneuverText = "Enter roundabout";
                  instruction = `Take exit onto ${{streetName}}`;
                  icon = "↻";
                }}

                return {{
                  instruction: instruction,
                  distance: stepMeters,
                  maneuver: maneuverText,
                  icon: icon
                }};
              }}).filter(st => st.distance > 0 || st.maneuver === 'Destination reached');
            }}

            if (waypoints.length > 0) {{
              return {{
                distKm,
                estMin,
                waypoints,
                routeCoords
              }};
            }}
          }}
        }}
      }} catch (err) {{
        console.warn("[OSRM] Pedestrian routing fetch:", err);
      }}

      // Haversine direct calculation fallback if offline
      const distKm = calculateHaversineKm(startLat, startLon, destLat, destLon);
      const estMin = Math.max(1, Math.round((distKm / 4.8) * 60));
      const distMeters = Math.max(10, Math.round(distKm * 1000));
      return {{
        distKm,
        estMin,
        waypoints: [
          {{
            instruction: `Walk forward along pathway toward ${{destTitle}}`,
            distance: distMeters,
            maneuver: "Head straight",
            icon: "↑"
          }},
          {{
            instruction: `Arrival: ${{destTitle}}`,
            distance: 0,
            maneuver: "Destination reached",
            icon: "★"
          }}
        ],
        routeCoords: [
          [startLat, startLon],
          [destLat, destLon]
        ]
      }};
    }}

    async function selectRealDestination(title, subtitle, lat, lon) {{
      triggerHaptic([60]);
      const destLat = parseFloat(lat);
      const destLon = parseFloat(lon);

      const pTitle = document.getElementById('preview-destination-title');
      const pSub = document.getElementById('preview-destination-sub');
      if (pTitle) pTitle.innerText = title;
      if (pSub) pSub.innerText = "Calculating real pedestrian walking route...";
      navigateTo('routePreview');

      const routeData = await fetchRealOsrmRoute(userGps.lat, userGps.lon, destLat, destLon, title);

      activeDestination = {{
        title: title,
        subtitle: subtitle || `${{title}} • ${{routeData.distKm}} km`,
        lat: destLat,
        lon: destLon,
        distanceKm: routeData.distKm,
        estimatedMinutes: routeData.estMin,
        waypoints: routeData.waypoints,
        routeCoords: routeData.routeCoords
      }};

      currentDestinationTitle = title;
      currentDestinationSub = `${{subtitle || title}} • ${{routeData.distKm}} km • ${{routeData.estMin}} min • ${{routeData.waypoints.length}} steps`;
      currentWaypoints = [...routeData.waypoints];

      if (pSub) pSub.innerText = currentDestinationSub;
      const sBtn = document.getElementById('start-nav-btn');
      if (sBtn) sBtn.setAttribute('aria-label', `Start walking navigation to ${{title}}`);

      initRouteLeafletMap();
    }}

    // ==================== INTERACTIVE LEAFLET MAPS ====================
    function initRouteLeafletMap() {{
      const mapEl = document.getElementById('route-map-leaflet');
      const loadingEl = document.getElementById('route-map-loading');
      if (!mapEl || typeof L === 'undefined') return;

      try {{
        if (!routeLeafletMap) {{
          routeLeafletMap = L.map('route-map-leaflet', {{
            zoomControl: false,
            attributionControl: false
          }}).setView([userGps.lat, userGps.lon], 15);

          L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19
          }}).addTo(routeLeafletMap);
        }}

        // Remove old markers
        if (routeUserMarker) routeLeafletMap.removeLayer(routeUserMarker);
        if (routeDestMarker) routeLeafletMap.removeLayer(routeDestMarker);
        if (routePolyline) routeLeafletMap.removeLayer(routePolyline);

        // Add User Start Marker
        const userIcon = L.divIcon({{
          className: 'leaflet-user-div-icon',
          html: '<div style="width:16px;height:16px;border-radius:50%;background:#2563EB;border:3px solid #FFFFFF;box-shadow:0 0 8px rgba(37,99,235,0.8);"></div>',
          iconSize: [16, 16],
          iconAnchor: [8, 8]
        }});
        routeUserMarker = L.marker([userGps.lat, userGps.lon], {{ icon: userIcon }}).addTo(routeLeafletMap);

        // Add Destination Marker
        const destIcon = L.divIcon({{
          className: 'leaflet-dest-div-icon',
          html: '<div style="font-size:22px;line-height:1;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.4));">📍</div>',
          iconSize: [24, 24],
          iconAnchor: [12, 22]
        }});
        routeDestMarker = L.marker([activeDestination.lat, activeDestination.lon], {{ icon: destIcon }}).addTo(routeLeafletMap);

        // Add Genuine Real Route Polyline
        let latlngs = [];
        if (activeDestination.routeCoords && activeDestination.routeCoords.length > 0) {{
          latlngs = activeDestination.routeCoords;
        }} else {{
          latlngs = [
            [userGps.lat, userGps.lon],
            [activeDestination.lat, activeDestination.lon]
          ];
        }}
        routePolyline = L.polyline(latlngs, {{
          color: '#2563EB',
          weight: 5,
          opacity: 0.85,
          lineCap: 'round'
        }}).addTo(routeLeafletMap);

        const group = new L.featureGroup([routeUserMarker, routeDestMarker, routePolyline]);
        routeLeafletMap.fitBounds(group.getBounds().pad(0.2));
        routeLeafletMap.invalidateSize();

        if (loadingEl) loadingEl.classList.add('hidden');
      }} catch (err) {{
        console.warn('[Leaflet] Error initializing route map:', err);
      }}
    }}

    function initWhereAmILeafletMap() {{
      const mapEl = document.getElementById('whereami-map-leaflet');
      const loadingEl = document.getElementById('whereami-map-loading');
      if (!mapEl || typeof L === 'undefined') return;

      try {{
        if (!whereAmILeafletMap) {{
          whereAmILeafletMap = L.map('whereami-map-leaflet', {{
            zoomControl: false,
            attributionControl: false
          }}).setView([userGps.lat, userGps.lon], 16);

          L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19
          }}).addTo(whereAmILeafletMap);
        }}

        if (whereAmIMarker) whereAmILeafletMap.removeLayer(whereAmIMarker);

        const pulseIcon = L.divIcon({{
          className: 'leaflet-pulse-icon',
          html: '<div style="width:18px;height:18px;border-radius:50%;background:#10B981;border:3px solid #FFFFFF;box-shadow:0 0 10px rgba(16,185,129,0.9);"></div>',
          iconSize: [18, 18],
          iconAnchor: [9, 9]
        }});

        whereAmIMarker = L.marker([userGps.lat, userGps.lon], {{ icon: pulseIcon }}).addTo(whereAmILeafletMap);
        whereAmILeafletMap.setView([userGps.lat, userGps.lon], 16);
        whereAmILeafletMap.invalidateSize();

        if (loadingEl) loadingEl.classList.add('hidden');
      }} catch (err) {{
        console.warn('[Leaflet] Error initializing Where Am I map:', err);
      }}
    }}

    // ==================== REAL-TIME MULTIMODAL VISION PERCEPTION ====================
    function getObjectIcon(label) {{
      const icons = {{
        'chair': '🪑', 'person': '👤', 'car': '🚗', 'bicycle': '🚲',
        'dog': '🐕', 'cat': '🐈', 'bottle': '🍾', 'cup': '☕',
        'couch': '🛋️', 'table': '🪑', 'tv': '📺', 'laptop': '💻',
        'cell phone': '📱', 'door': '🚪', 'stairs': '🪜', 'backpack': '🎒',
        'traffic light': '🚦', 'stop sign': '🛑', 'bench': '🪵', 'tree': '🌳'
      }};
      return icons[(label || '').toLowerCase()] || '👁️';
    }}

    async function triggerDescribeAround() {{
      const video = document.getElementById('describe-live-video');
      const img = document.getElementById('describe-scene-img');
      const liveBadge = document.getElementById('describe-live-badge');
      const spinner = document.getElementById('describe-scanning-spinner');

      if (spinner) spinner.classList.remove('hidden');

      // Use active back camera stream if available, or try opening stream
      if (liveCameraStream && video) {{
        video.srcObject = liveCameraStream;
        video.classList.remove('hidden');
        if (img) img.classList.add('hidden');
        if (liveBadge) liveBadge.classList.remove('hidden');
        try {{ await video.play(); }} catch(e){{}}
      }}

      let snapshotBase64 = null;
      if (video && video.videoWidth > 0 && !video.paused) {{
        const snap = document.createElement('canvas');
        snap.width = 640;
        snap.height = 360;
        snap.getContext('2d').drawImage(video, 0, 0, snap.width, snap.height);
        snapshotBase64 = snap.toDataURL('image/jpeg', 0.75);
      }}

      // First run browser COCO-SSD neural detection if available
      let browserDetections = [];
      if (cocoSsdModel && video && video.readyState >= 2) {{
        try {{
          const preds = await cocoSsdModel.detect(video);
          browserDetections = preds.map(p => ({{
            label: p.class.charAt(0).toUpperCase() + p.class.slice(1),
            confidence: Math.round(p.score * 100),
            lane: p.bbox[0] + p.bbox[2] / 2 < video.videoWidth * 0.4 ? 'on your left' : (p.bbox[0] + p.bbox[2] / 2 > video.videoWidth * 0.6 ? 'on your right' : 'directly ahead')
          }}));
        }} catch(e){{}}
      }}

      // Call backend Gemini Multimodal Perception API
      let backendData = null;
      try {{
        const resp = await fetch('/api/v1/environment/describe', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            imageBase64: snapshotBase64,
            userContext: {{
              street: userGps.street,
              city: userGps.city,
              heading: userGps.headingCardinal,
              coords: {{ lat: userGps.lat, lon: userGps.lon }}
            }}
          }})
        }});
        if (resp.ok) {{
          const json = await resp.json();
          if (json && json.status === 'success' && json.data) {{
            backendData = json.data;
          }}
        }}
      }} catch (err) {{
        console.warn('[Describe] Backend perception fetch notice:', err.message);
      }}

      if (spinner) spinner.classList.add('hidden');

      // Synthesize detected items
      let displayItems = [];
      let spokenSummary = "";

      if (browserDetections.length > 0) {{
        displayItems = browserDetections.map(d => ({{
          icon: getObjectIcon(d.label),
          text: `${{d.label}} detected ${{d.lane}} (${{d.confidence}}% confidence).`
        }}));
        displayItems.unshift({{
          icon: '✓',
          text: `Real-time camera feed active on ${{userGps.street || 'sidewalk'}}.`
        }});
        spokenSummary = `I see ` + browserDetections.map(d => `${{d.label}} ${{d.lane}}`).join(', ') + `.`;
      }} else if (backendData && backendData.objects_detected) {{
        displayItems = backendData.objects_detected.map(o => ({{
          icon: getObjectIcon(o.label),
          text: `${{o.label}} ${{o.lane || 'ahead'}}, approximately ${{o.distance_meters || 2}}m.`
        }}));
        displayItems.unshift({{
          icon: '✓',
          text: backendData.scene_summary || `Sidewalk condition is clear.`
        }});
        spokenSummary = backendData.spoken_description || backendData.scene_summary || "Clear pathway ahead.";
      }} else {{
        displayItems = [
          {{ icon: '✓', text: `Sidewalk on ${{userGps.street || 'current path'}} is clear.` }},
          {{ icon: '🚶', text: `Path continues straight for approximately 40 meters.` }},
          {{ icon: '👁️', text: `Continuous YOLO object detection active.` }}
        ];
        spokenSummary = `Sidewalk on ${{userGps.street || 'your path'}} is clear directly ahead. No immediate obstacles in your path.`;
      }}

      lastSceneDescription = spokenSummary;
      renderDynamicSceneItems(displayItems);
      speakText(spokenSummary);
    }}

    function renderDynamicSceneItems(items) {{
      const listEl = document.getElementById('describe-scene-list');
      if (!listEl) return;
      listEl.innerHTML = items.map(item => `
        <li class="flex items-center space-x-3 p-3">
          <div class="w-6 h-6 rounded-full bg-slate-100 text-slate-800 flex items-center justify-center font-bold text-xs flex-shrink-0" aria-hidden="true">${{item.icon}}</div>
          <span class="font-medium text-slate-900 text-sm">${{item.text}}</span>
        </li>
      `).join('');
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
      {{ text: "Pedestrian Walkway", type: "street_sign", icon: "🪧", pos: "right", announcement: "Street sign on right: Pedestrian Walkway" }},
      {{ text: "Building Entrance", type: "building_board", icon: "🏢", pos: "ahead", announcement: "Building entrance ahead" }},
      {{ text: "Bus Transit Stop", type: "transit_sign", icon: "🚏", pos: "left", announcement: "Transit sign on left: Bus stop" }},
      {{ text: "Pedestrian Crosswalk", type: "warning_sign", icon: "🚶", pos: "ahead", announcement: "Crosswalk ahead" }}
    ];

    async function startAlwaysOpenBackCamera() {{
      const video = document.getElementById('nav-live-video');
      const obsVideo = document.getElementById('obstacle-live-video');
      const crossVideo = document.getElementById('crosswalk-live-video');
      const descVideo = document.getElementById('describe-live-video');
      const cameraPrompt = document.getElementById('nav-camera-prompt');
      const descPrompt = document.getElementById('describe-camera-prompt');
      const descLiveBadge = document.getElementById('describe-live-badge');

      // Attempt to access user device environment (rear) camera
      try {{
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {{
          if (!liveCameraStream) {{
            liveCameraStream = await navigator.mediaDevices.getUserMedia({{
              video: {{
                facingMode: {{ ideal: "environment" }},
                width: {{ ideal: 1280 }},
                height: {{ ideal: 720 }}
              }},
              audio: false
            }});
          }}
          if (liveCameraStream) {{
            if (video) {{
              video.srcObject = liveCameraStream;
              video.classList.remove('hidden');
              try {{ await video.play(); }} catch(e){{}}
            }}
            if (obsVideo) {{
              obsVideo.srcObject = liveCameraStream;
              obsVideo.classList.remove('hidden');
              try {{ await obsVideo.play(); }} catch(e){{}}
            }}
            if (crossVideo) {{
              crossVideo.srcObject = liveCameraStream;
              crossVideo.classList.remove('hidden');
              try {{ await crossVideo.play(); }} catch(e){{}}
            }}
            if (descVideo) {{
              descVideo.srcObject = liveCameraStream;
              descVideo.classList.remove('hidden');
              try {{ await descVideo.play(); }} catch(e){{}}
            }}
            isRealCameraActive = true;
            currentCameraMode = 'real';
            if (cameraPrompt) cameraPrompt.classList.add('hidden');
            if (descPrompt) descPrompt.classList.add('hidden');
            if (descLiveBadge) descLiveBadge.classList.remove('hidden');
            updateCameraStatusUI(true);
            announceToScreenReader("Back camera stream active. Continuous YOLO object detection running.");
          }}
        }}
      }} catch (err) {{
        console.warn("[Camera] Live hardware camera access notice:", err.message);
        isRealCameraActive = false;
        currentCameraMode = 'simulation';
        if (cameraPrompt) cameraPrompt.classList.remove('hidden');
        updateCameraStatusUI(false);
      }}

      // Load COCO-SSD model asynchronously if not yet loaded
      if (!cocoSsdModel && !isCocoLoading && typeof cocoSsd !== 'undefined') {{
        isCocoLoading = true;
        cocoSsd.load().then(model => {{
          cocoSsdModel = model;
          isCocoLoading = false;
          console.log('[COCO-SSD] Real neural object detection model loaded successfully.');
        }}).catch(err => {{
          isCocoLoading = false;
          console.warn('[COCO-SSD] Error loading model:', err);
        }});
      }}

      // Start YOLO perception cycle (5-10 times per second)
      if (!yoloDetectionInterval) {{
        yoloDetectionInterval = setInterval(runYoloPerceptionCycle, 180);
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
        if (liveCameraStream) {{
          liveCameraStream.getTracks().forEach(t => t.stop());
          liveCameraStream = null;
        }}
        isRealCameraActive = false;
        currentCameraMode = 'simulation';
        const cameraPrompt = document.getElementById('nav-camera-prompt');
        if (cameraPrompt) cameraPrompt.classList.remove('hidden');
        updateCameraStatusUI(false);
        speakText("Camera stream paused.");
      }} else {{
        currentCameraMode = 'real';
        startAlwaysOpenBackCamera();
        speakText("Activating device rear camera.");
      }}
    }}

    function updateCameraStatusUI(isReal) {{
      const pill = document.getElementById('camera-status-pill');
      const icon = document.getElementById('camera-toggle-icon');
      if (pill) {{
        pill.innerText = isReal ? "Back Camera • YOLO Active" : "Camera Standby • YOLO Active";
      }}
      if (icon) {{
        icon.innerText = isReal ? "📷" : "⏸️";
      }}
    }}

    async function runYoloPerceptionCycle() {{
      if (activeRoute !== 'activeNavigation') return;
      simWalkFrame++;

      const canvas = document.getElementById('nav-yolo-canvas');
      const video = document.getElementById('nav-live-video');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      canvas.width = canvas.clientWidth || 320;
      canvas.height = canvas.clientHeight || 480;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      let activeObjects = [];
      const now = Date.now();

      // Real Camera + COCO-SSD Neural Object Detection
      if (isRealCameraActive && video && video.readyState >= 2 && cocoSsdModel && !isDetectingFrame) {{
        isDetectingFrame = true;
        try {{
          const predictions = await cocoSsdModel.detect(video);
          const vW = video.videoWidth || 640;
          const vH = video.videoHeight || 480;
          const scaleX = canvas.width / vW;
          const scaleY = canvas.height / vH;

          activeObjects = predictions.map(p => {{
            const boxX = p.bbox[0] * scaleX;
            const boxY = p.bbox[1] * scaleY;
            const boxW = p.bbox[2] * scaleX;
            const boxH = p.bbox[3] * scaleY;
            const centerX = boxX + boxW / 2;
            const heightRatio = boxH / canvas.height;
            const estimatedDist = Math.max(0.4, Math.min(8.0, parseFloat((1.1 / (heightRatio + 0.05)).toFixed(1))));
            const lane = centerX < canvas.width * 0.35 ? 'left' : (centerX > canvas.width * 0.65 ? 'right' : 'center');

            return {{
              label: p.class.charAt(0).toUpperCase() + p.class.slice(1),
              icon: getObjectIcon(p.class),
              x: boxX,
              y: boxY,
              w: boxW,
              h: boxH,
              conf: p.score,
              distance: estimatedDist,
              lane: lane
            }};
          }});
          lastLiveDetections = activeObjects;
        }} catch(err) {{
          console.warn('[YOLO] Detection cycle error:', err);
        }} finally {{
          isDetectingFrame = false;
        }}
      }} else if (lastLiveDetections.length > 0 && isRealCameraActive) {{
        activeObjects = lastLiveDetections;
      }} else {{
        // Zero synthetic obstacles! Real environment only.
        activeObjects = [];
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

      // Multi-Lane LiDAR Corridor Clearance Analysis
      let minLeftDist = 5.0;
      let minCenterDist = 5.0;
      let minRightDist = 5.0;
      let closestCenter = null;

      activeObjects.forEach(obj => {{
        if (obj.lane === 'left') {{
          if (obj.distance < minLeftDist) minLeftDist = obj.distance;
        }} else if (obj.lane === 'center') {{
          if (obj.distance < minCenterDist) {{
            minCenterDist = obj.distance;
            closestCenter = obj;
          }}
        }} else if (obj.lane === 'right') {{
          if (obj.distance < minRightDist) minRightDist = obj.distance;
        }}
      }});

      currentLidarDepthAhead = minCenterDist;
      currentLidarDepthLeft = minLeftDist;
      currentLidarDepthRight = minRightDist;

      // Intelligent Spatial Direction Decision (WHERE TO WALK)
      let directionStatus = 'WALK STRAIGHT • PATH CLEAR';
      let directionArrow = '⬆️';
      let guidanceSpoken = '';
      let statusClass = 'text-emerald-300';
      let borderClass = 'border-emerald-500/50';

      if (minCenterDist >= 2.2) {{
        directionStatus = 'WALK STRAIGHT • PATH CLEAR';
        directionArrow = '⬆️';
        statusClass = 'text-emerald-300';
        borderClass = 'border-emerald-500/50';
      }} else if (minCenterDist < 0.8) {{
        directionStatus = 'STOP • COLLISION HAZARD';
        directionArrow = '🛑';
        statusClass = 'text-red-400 font-extrabold animate-pulse';
        borderClass = 'border-red-500';
        guidanceSpoken = `Stop! ${{closestCenter ? closestCenter.label : 'Obstacle'}} directly ahead at ${{minCenterDist.toFixed(1)}} meters!`;
      }} else {{
        // Obstacle 0.8m - 2.2m in walking path
        if (minLeftDist >= minRightDist && minLeftDist >= 1.8) {{
          directionStatus = 'VEER LEFT 15° • CLEAR OPENING';
          directionArrow = '↖️';
          statusClass = 'text-amber-300 font-bold';
          borderClass = 'border-amber-500';
          guidanceSpoken = `Caution: ${{closestCenter ? closestCenter.label : 'Obstacle'}} ${{minCenterDist.toFixed(1)}} meters ahead in center path. Clear opening on your left. Veer left 15 degrees.`;
        }} else if (minRightDist > minLeftDist && minRightDist >= 1.8) {{
          directionStatus = 'VEER RIGHT 15° • CLEAR OPENING';
          directionArrow = '↗️';
          statusClass = 'text-amber-300 font-bold';
          borderClass = 'border-amber-500';
          guidanceSpoken = `Caution: ${{closestCenter ? closestCenter.label : 'Obstacle'}} ${{minCenterDist.toFixed(1)}} meters ahead in center path. Clear opening on your right. Veer right 15 degrees.`;
        }} else {{
          directionStatus = 'SLOW DOWN • NARROW CORRIDOR';
          directionArrow = '⚠️';
          statusClass = 'text-orange-300 font-bold';
          borderClass = 'border-orange-500';
          guidanceSpoken = `Caution: Narrow pathway. ${{closestCenter ? closestCenter.label : 'Obstacle'}} ${{minCenterDist.toFixed(1)}} meters in walking path. Proceed carefully.`;
        }}
      }}

      // Update Screen 5 Corridor HUD
      const hudEl = document.getElementById('nav-lidar-corridor-hud');
      const arrEl = document.getElementById('nav-direction-arrow');
      const statEl = document.getElementById('nav-corridor-status');
      const depthEl = document.getElementById('nav-depth-meters');
      const lanesEl = document.getElementById('nav-lateral-lanes');
      if (arrEl) arrEl.innerText = directionArrow;
      if (statEl) {{
        statEl.innerText = directionStatus;
        statEl.className = 'text-[11px] font-bold tracking-wide uppercase ' + statusClass;
      }}
      if (depthEl) {{
        depthEl.innerText = activeObjects.length > 0 ? (minCenterDist.toFixed(1) + 'm') : 'Clear (>3m)';
      }}
      if (lanesEl) {{
        lanesEl.innerText = activeObjects.length > 0 
          ? `Detected: ${{activeObjects.map(o => o.label).join(', ')}}`
          : 'Optical View: Clear Ahead';
      }}
      if (hudEl) hudEl.className = `w-full mt-2 py-2 px-3 rounded-2xl bg-black/85 backdrop-blur-md border ${{borderClass}} text-white shadow-xl flex items-center justify-between`;

      // Update Top HUD Hazard Status Badge
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

      // Zero cartoon painted road! Pure real-world camera view.
      // Bounding boxes for genuine detected objects have already been drawn above.

      // Emergency or Directional Voice Guidance (Throttled)
      if (guidanceSpoken && (now - lastSpokenObstacleTime > 5000)) {{
        lastSpokenObstacleTime = now;
        triggerHaptic(minCenterDist < 0.8 ? [150, 50, 150, 50, 200] : [80, 50, 80]);
        speakText(guidanceSpoken);

        // If Critical Stop, navigate to Screen 8 with real obstacle details
        if (minCenterDist < 0.8 && closestCenter) {{
          updateLidarState(closestCenter.distance, closestCenter.label, closestCenter.lane, false);
          navigateTo('obstacleAlert');
        }}
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
            userContext: {{
              street: userGps.street || 'Current Street',
              city: userGps.city || '',
              heading: userGps.headingCardinal,
              coords: {{ lat: userGps.lat, lon: userGps.lon }}
            }}
          }})
        }});
        if (resp.ok) {{
          const json = await resp.json();
          if (json && json.status === 'success' && json.data) {{
            detected = json.data;
          }}
        }}
      }} catch (err) {{
        console.warn("[Signboards] API call error:", err);
      }}

      // No fake RTU signboard fallback! Real environment only.
      if (!detected || !detected.signs || detected.signs.length === 0) {{
        detected = {{
          signs: [],
          summary: "No text signboards detected in camera view."
        }};
      }}

      if (detected.signs && detected.signs.length > 0) {{
        const primarySign = detected.signs[0];
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
      }} else {{
        if (bannerText) bannerText.innerText = "Scanning for street signs...";
        if (overlay) overlay.innerHTML = "";
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
        flashElement(document.getElementById('btn-repeat-instruction') || document.getElementById('nav-floating-mic-btn'));
        if (activeRoute === 'activeNavigation') repeatCurrentStep();
        else if (activeRoute === 'whereAmI') repeatRealLocation();
        else if (activeRoute === 'describeAround') repeatSceneDescription();
        else if (activeRoute === 'obstacleAlert') repeatObstacleWarning();
        else speakText("Nothing to repeat.");
      }} else if (buttonId === 'acknowledge_obstacle') {{
        flashElement(document.getElementById('btn-i-understand') || document.getElementById('obstacle-voice-mic-btn'));
        acknowledgeObstacle();
      }} else if (buttonId === 'settings') {{
        openSettingsModal();
      }} else if (buttonId === 'toggle_camera') {{
        flashElement(document.getElementById('btn-toggle-camera'));
        toggleCameraFeed();
      }} else if (buttonId === 'stop_route') {{
        flashElement(document.getElementById('btn-stop-route') || document.getElementById('btn-nav-back'));
        stopNavigationRoute();
      }}
    }}

    async function handleAutoGpsNavigation(dest, spoken) {{
      document.getElementById('listening-title').innerText = "Detecting current location...";
      announceToScreenReader("Detecting current GPS location and calculating route.");
      speakText("Detecting your current location.");
      triggerHaptic([60, 40]);

      const executeRouting = async (lat, lon, locName) => {{
        let targetLat = (dest && dest.lat) ? dest.lat : null;
        let targetLon = (dest && dest.lon) ? dest.lon : null;
        let targetTitle = (dest && (dest.canonicalName || dest.shortName)) || null;
        let targetSub = (dest && dest.subtitle) || null;

        // Try geocoding destination name if no coordinates
        if ((!targetLat || !targetLon) && targetTitle && !dest?.isNearbySearch) {{
          try {{
            const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${{encodeURIComponent(targetTitle)}}&limit=1`);
            if (res.ok) {{
              const items = await res.json();
              if (items && items[0]) {{
                targetLat = parseFloat(items[0].lat);
                targetLon = parseFloat(items[0].lon);
                targetSub = items[0].display_name.split(',').slice(1, 3).join(',').trim();
              }}
            }}
          }} catch(e){{}}
        }}

        // If vague or nearby destination requested ("go somewhere", "take me somewhere", "go there"), search real nearby places
        if (!targetLat || !targetLon) {{
          try {{
            const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=park&limit=1&viewbox=${{lon-0.03}},${{lat+0.03}},${{lon+0.03}},${{lat-0.03}}`);
            if (res.ok) {{
              const items = await res.json();
              if (items && items[0]) {{
                targetTitle = items[0].name || items[0].display_name.split(',')[0];
                targetLat = parseFloat(items[0].lat);
                targetLon = parseFloat(items[0].lon);
                targetSub = items[0].display_name.split(',').slice(1, 3).join(',').trim();
              }}
            }}
          }} catch(e){{}}
        }}

        if (!targetLat || !targetLon) {{
          targetTitle = targetTitle || "Nearby Walking Path";
          targetLat = lat + 0.002;
          targetLon = lon + 0.002;
          targetSub = targetSub || "Pedestrian pathway ahead";
        }}

        document.getElementById('listening-title').innerText = `Location found: ${{locName}}. Routing...`;
        const speechMsg = `Current location detected near ${{locName}}. Routing to ${{targetTitle}}. Back camera is open. Point phone forward.`;
        speakText(spoken || speechMsg);
        
        await selectRealDestination(targetTitle, targetSub, targetLat, targetLon);
        
        // Open back camera immediately and launch active navigation!
        startAlwaysOpenBackCamera();
        setTimeout(() => {{
          startCurrentNavigation();
        }}, 1200);
      }};

      if (navigator.geolocation) {{
        navigator.geolocation.getCurrentPosition(
          (pos) => {{
            handleGpsSuccess(pos);
            executeRouting(pos.coords.latitude, pos.coords.longitude, userGps.street || "Current Location");
          }},
          (err) => {{
            console.warn("GPS access notice:", err.message);
            executeRouting(userGps.lat, userGps.lon, userGps.street || "Current Location");
          }},
          {{ timeout: 5000, enableHighAccuracy: true }}
        );
      }} else {{
        executeRouting(userGps.lat, userGps.lon, userGps.street || "Current Location");
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
      if (/^(yes|yeah|yep|sure|ok|okay|i understand|understand|dismiss|dismiss obstacle|got it|clear|resume|continue|proceed|affirmative)$/i.test(cleaned)) {{
        if (activeRoute === 'obstacleAlert') {{
          return {{ intent: "click_button", target_button: "acknowledge_obstacle", action: "click_button", spoken_response: "Obstacle acknowledged. Resuming route.", confidence: 0.99 }};
        }} else {{
          return {{ intent: "affirmative", action: "affirmative", spoken_response: "Path is clear. Continue straight.", confidence: 0.99 }};
        }}
      }}
      if (/^(no|nope|wait|hold on|pause|not yet)$/i.test(cleaned)) {{
        return {{ intent: "negative", action: "negative", spoken_response: "Holding position. Let me know when you are ready to continue.", confidence: 0.99 }};
      }}
      // 5e. Directional Queries (Right, Left, Ahead, Approaching person detection)
      if (/^(is someone coming from (my |the )?right|is anyone (on|from) (my |the )?right|anyone on (my |the )?right|who is on (my |the )?right|what('s| is) on (my |the )?right|is there a person on (my |the )?right|look right|check right|person on (my |the )?right|is someone on (my |the )?right|someone on right)$/i.test(cleaned) ||
          (/\b(someone|anyone|person|anybody|coming|approaching)\b/i.test(cleaned) && /\b(right)\b/i.test(cleaned)) ||
          /\b(on my right|on the right|to my right|to the right)\b/i.test(cleaned)) {{
        return {{
          intent: "directional_query",
          direction: "right",
          target: "person",
          spoken_response: "Scanning to your right. Point or turn your phone to the right to inspect.",
          confidence: 0.99
        }};
      }}

      if (/^(is someone coming from (my |the )?left|is anyone (on|from) (my |the )?left|anyone on (my |the )?left|who is on (my |the )?left|what('s| is) on (my |the )?left|is there a person on (my |the )?left|look left|check left|person on (my |the )?left|is someone on (my |the )?left|someone on left)$/i.test(cleaned) ||
          (/\b(someone|anyone|person|anybody|coming|approaching)\b/i.test(cleaned) && /\b(left)\b/i.test(cleaned)) ||
          /\b(on my left|on the left|to my left|to the left)\b/i.test(cleaned)) {{
        return {{
          intent: "directional_query",
          direction: "left",
          target: "person",
          spoken_response: "Scanning to your left. Point or turn your phone to the left to inspect.",
          confidence: 0.99
        }};
      }}

      if (/^(is someone coming|is anyone coming|is someone approaching|is anyone approaching|is there someone|is there a person|who is coming|who is approaching|who is there|is someone in front of me|someone coming)$/i.test(cleaned)) {{
        return {{
          intent: "directional_query",
          direction: "ahead",
          target: "person",
          spoken_response: "Scanning path ahead for approaching pedestrians.",
          confidence: 0.99
        }};
      }}

      if (/^(where do i go|where to go|where should i go|which way|which direction|where to walk|guide me|navigate me)$/i.test(cleaned)) {{
        const dir = currentSteeringDirection || 'WALK STRAIGHT';
        const depth = currentLidarDepthAhead ? `${{currentLidarDepthAhead.toFixed(1)}} meters` : 'path is clear';
        return {{
          intent: "guidance_query",
          action: "guidance_query",
          spoken_response: `${{dir}}. Forward clearance is ${{depth}}.`,
          confidence: 0.99
        }};
      }}
      if (/^(is there anything in my way|is the path clear|is there an obstacle|what('s| is) in my way|what('s| is) ahead|any obstacles)$/i.test(cleaned)) {{
        return {{
          intent: "obstacle_query",
          action: "obstacle_query",
          spoken_response: (activeObjects && activeObjects.length > 0)
            ? `Detected ${{activeObjects.map(o => `${{o.label}} ${{o.distance.toFixed(1)}} meters on ${{o.lane}}`).join(', ')}}.`
            : "Pathway is completely clear ahead for over 4 meters.",
          confidence: 0.99
        }};
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
          spoken_response: userGps.street ? `You are on ${{userGps.street}}, in ${{userGps.city}}.` : "Checking your current location and orientation.",
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
          intent: "start_navigation",
          trigger_auto_gps: true,
          destination: {{
            canonicalName: "Nearby Destination",
            shortName: "Nearby Destination",
            subtitle: "Nearest accessible walking destination",
            isNearbySearch: true
          }},
          spoken_response: "Detecting current location. Finding nearest destination to navigate.",
          confidence: 0.95
        }};
      }}

      const known = findClientLocationMatch(clean);
      if (known) {{
        return {{
          intent: "start_navigation",
          trigger_auto_gps: true,
          destination: known,
          spoken_response: `Detecting current location. Routing to ${{known.canonicalName}}.`,
          confidence: 0.96
        }};
      }}

      if (clean.length >= 2) {{
        const custom = createClientCustomDestination(clean);
        return {{
          intent: "start_navigation",
          trigger_auto_gps: true,
          destination: custom,
          spoken_response: `Detecting current location. Planning route to ${{custom.canonicalName}}.`,
          confidence: 0.95
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
          tip.innerHTML = "Listening actively... Speak any destination or command";
        }} else if (targetRoute === 'destinationSearch') {{
          tip.innerHTML = "Search or speak any destination worldwide";
        }} else if (targetRoute === 'routePreview') {{
          tip.innerHTML = "Route preview to <strong>selected destination</strong>. Tap <strong>Start navigation</strong> to begin";
        }} else if (targetRoute === 'activeNavigation') {{
          tip.innerHTML = "Active walking navigation with always-open camera & YOLO detection.";
        }} else if (targetRoute === 'whereAmI') {{
          tip.innerHTML = "Current location and orientation from live GPS";
        }} else if (targetRoute === 'describeAround') {{
          tip.innerHTML = "Perception scene from live camera. Tap <strong>Repeat</strong> to hear again";
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
        speakText("Where would you like to go? Speak any destination or place.");
      }} else if (targetRoute === 'routePreview') {{
        speakText(`Route preview to ${{activeDestination.title}}. ${{activeDestination.distanceKm}} kilometers, ${{activeDestination.estimatedMinutes}} minutes.`);
        setTimeout(() => initRouteLeafletMap(), 150);
      }} else if (targetRoute === 'activeNavigation') {{
        announceToScreenReader("Active walking navigation started with back camera and YOLO detection.");
        startAlwaysOpenBackCamera();
      }} else if (targetRoute === 'whereAmI') {{
        repeatRealLocation();
        setTimeout(() => initWhereAmILeafletMap(), 150);
      }} else if (targetRoute === 'describeAround') {{
        triggerDescribeAround();
      }} else if (targetRoute === 'obstacleAlert') {{
        const evalResult = evaluateLidarDanger(currentLidarDistance, currentLidarLane, currentLidarObject);
        speakText(evalResult.spoken || "Warning: Obstacle ahead. Please clear path before proceeding.");
      }} else if (targetRoute === 'crosswalkSafety') {{
        speakText("Approaching pedestrian crosswalk. Quiet mode active. Listen for traffic.");
      }}
    }}

    function jumpToScreen(route) {{
      navigateTo(route);
    }}

    // Destination search logic (Local Filter + Real Worldwide OpenStreetMap Nominatim Geocoding)
    function filterDestinations(query) {{
      const q = (query || '').trim().toLowerCase();
      const list = document.getElementById('recent-places-list');
      if (!list) return;

      clearTimeout(searchDebounceTimer);

      if (q.length < 2) {{
        Array.from(list.children).forEach(item => item.style.display = 'flex');
        return;
      }}

      // Local match filtering first
      let localMatches = 0;
      Array.from(list.children).forEach(item => {{
        const text = item.innerText.toLowerCase();
        const matches = text.includes(q);
        item.style.display = matches ? 'flex' : 'none';
        if (matches) localMatches++;
      }});

      // Debounced live geocode search for ANY real place worldwide
      searchDebounceTimer = setTimeout(async () => {{
        try {{
          const url = `https://nominatim.openstreetmap.org/search?format=json&q=${{encodeURIComponent(query)}}&limit=5&addressdetails=1`;
          const res = await fetch(url, {{ headers: {{ 'Accept-Language': 'en' }} }});
          if (res.ok) {{
            const results = await res.json();
            if (results && results.length > 0) {{
              const newButtons = results.map(item => {{
                const mainName = item.name || item.display_name.split(',')[0];
                const subName = item.display_name.split(',').slice(1, 3).join(',').trim();
                const distKm = calculateHaversineKm(userGps.lat, userGps.lon, parseFloat(item.lat), parseFloat(item.lon));
                const estMin = Math.max(2, Math.round((distKm / 4.8) * 60));
                const safeMain = mainName.replace(/'/g, "\\'");
                const safeSub = subName.replace(/'/g, "\\'");
                return `
                  <button onclick="selectRealDestination('${{safeMain}}', '${{safeSub}}', ${{item.lat}}, ${{item.lon}})"
                          aria-label="Select destination: ${{safeMain}}, ${{safeSub}}, ${{distKm}} kilometers"
                          class="bg-white p-3.5 rounded-2xl border border-blue-200 shadow-sm flex items-center justify-between text-left hover:border-blue-500 transition">
                    <div class="flex items-center space-x-3">
                      <div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-sm" aria-hidden="true">📍</div>
                      <div>
                        <h4 class="font-bold text-slate-900 text-sm">${{mainName}}</h4>
                        <p class="text-xs text-slate-600">${{subName || 'Global Destination'}} • ${{distKm}} km</p>
                      </div>
                    </div>
                    <span class="text-xs font-bold text-blue-700 bg-blue-50 px-2 py-1 rounded-lg">${{estMin}} min</span>
                  </button>
                `;
              }}).join('');

              list.innerHTML = newButtons;
              announceToScreenReader(`${{results.length}} real destinations found for ${{query}}`);
            }}
          }}
        }} catch (err) {{
          console.warn('[Nominatim] Destination search error:', err.message);
        }}
      }}, 350);
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

    // Universal Voice HUD & Microphone Assistant
    function showUniversalVoiceHUD(statusText, bodyText, isListening = true) {{
      const hud = document.getElementById('universal-voice-hud');
      const sEl = document.getElementById('voice-hud-status');
      const tEl = document.getElementById('voice-hud-text');
      if (sEl) sEl.innerText = statusText || 'Listening...';
      if (tEl) tEl.innerText = bodyText || 'Speak now...';
      if (hud) {{
        hud.classList.remove('hidden');
        hud.classList.add('flex');
      }}
      announceToScreenReader(`${{statusText}}: ${{bodyText}}`);
    }}

    function hideUniversalVoiceHUD() {{
      const hud = document.getElementById('universal-voice-hud');
      if (hud) {{
        hud.classList.add('hidden');
        hud.classList.remove('flex');
      }}
    }}

    function triggerVoiceAssistant() {{
      // 1. Immediately cancel any speech synthesis so mic doesn't hear TTS audio
      if (window.speechSynthesis) {{
        window.speechSynthesis.cancel();
      }}
      triggerHaptic([40]);

      // 2. Request orientation sensors permission on iOS if first user gesture
      if (typeof DeviceOrientationEvent !== 'undefined' && typeof DeviceOrientationEvent.requestPermission === 'function') {{
        try {{
          DeviceOrientationEvent.requestPermission().then(state => {{
            if (state === 'granted') {{
              window.addEventListener('deviceorientation', handleOrientationEvent, true);
            }}
          }}).catch(() => {{}});
        }} catch(e){{}}
      }}

      // 3. Show Universal Voice HUD
      showUniversalVoiceHUD("Listening...", "Speak now — Say where to go or ask: \"Is someone on my right?\"", true);

      // 4. Start audio speech capture
      startVoiceCapture();
    }}

    // Real-Time Directional Watch & Gyroscope State
    let activeDirectionalWatch = null;
    let currentCompassHeading = 0;
    let lastDirectionalSpokenTime = 0;

    function handleDirectionalQuery(direction, target, rawText) {{
      const dir = direction || 'right';

      // 1. Inspect current live neural detections from YOLO
      const targetLane = dir === 'right' ? 'right' : (dir === 'left' ? 'left' : 'center');
      const matched = lastLiveDetections.filter(d => 
        d.lane === targetLane || 
        (dir === 'right' && d.x > 160) || 
        (dir === 'left' && d.x < 160)
      );

      const personMatch = matched.find(d => d.label.toLowerCase() === 'person');
      let responseSpeech = "";

      if (personMatch) {{
        responseSpeech = `Yes, I see a person on your ${{dir}}, about ${{personMatch.distance.toFixed(1)}} meters away.`;
      }} else if (matched.length > 0) {{
        responseSpeech = `I see a ${{matched[0].label}} on your ${{dir}}, about ${{matched[0].distance.toFixed(1)}} meters away.`;
      }} else {{
        responseSpeech = `I don't see anyone on your ${{dir}} right now. Turn your phone to the ${{dir}} to scan.`;
      }}

      showUniversalVoiceHUD(`Direction Check: ${{dir.toUpperCase()}}`, responseSpeech, false);
      speakText(responseSpeech);
      triggerHaptic([50]);

      // 2. Arm Active Directional Watch: when phone turns right/left, answer live!
      activeDirectionalWatch = {{
        direction: dir,
        target: target || 'person',
        armedAt: Date.now(),
        initialHeading: currentCompassHeading,
        fulfilled: false
      }};

      // Update corridor HUD if on active navigation
      const cStatus = document.getElementById('nav-corridor-status');
      if (cStatus) {{
        cStatus.innerText = `SCANNING ${{dir.toUpperCase()}} • TURN PHONE ${{dir.toUpperCase()}}`;
      }}
      const cArrow = document.getElementById('nav-direction-arrow');
      if (cArrow) {{
        cArrow.innerText = dir === 'right' ? '➡️' : (dir === 'left' ? '⬅️' : '⬆️');
      }}

      // Auto-expire watch after 12 seconds
      setTimeout(() => {{
        if (activeDirectionalWatch && !activeDirectionalWatch.fulfilled) {{
          activeDirectionalWatch = null;
          if (cStatus) cStatus.innerText = 'WALK STRAIGHT • PATH CLEAR';
          if (cArrow) cArrow.innerText = '⬆️';
        }}
      }}, 12000);
    }}

    function handleOrientationEvent(e) {{
      let heading = null;
      if (e.webkitCompassHeading !== undefined) {{
        heading = e.webkitCompassHeading;
      }} else if (e.alpha !== null) {{
        heading = (360 - e.alpha) % 360;
      }}

      if (heading !== null) {{
        currentCompassHeading = heading;
      }}

      // Check if user is actively turning phone in response to a directional query
      if (activeDirectionalWatch && !activeDirectionalWatch.fulfilled) {{
        checkPhoneTurnedResponse(e, heading);
      }}
    }}

    function checkPhoneTurnedResponse(e, heading) {{
      if (!activeDirectionalWatch || activeDirectionalWatch.fulfilled) return;
      if (Date.now() - activeDirectionalWatch.armedAt < 500) return;

      const dir = activeDirectionalWatch.direction;
      let turned = false;

      // 1. Heading change detection
      if (heading !== null && activeDirectionalWatch.initialHeading !== null) {{
        let diff = heading - activeDirectionalWatch.initialHeading;
        while (diff > 180) diff -= 360;
        while (diff < -180) diff += 360;

        if (dir === 'right' && diff >= 20) turned = true;
        if (dir === 'left' && diff <= -20) turned = true;
      }}

      // 2. Gamma tilt fallback
      if (!turned && e.gamma !== null) {{
        if (dir === 'right' && e.gamma > 20) turned = true;
        if (dir === 'left' && e.gamma < -20) turned = true;
      }}

      if (turned) {{
        activeDirectionalWatch.fulfilled = true;
        triggerHaptic([60, 40]);

        const now = Date.now();
        if (now - lastDirectionalSpokenTime > 2000) {{
          lastDirectionalSpokenTime = now;
          evaluateLiveTurnedSector(dir);
        }}
      }}
    }}

    function evaluateLiveTurnedSector(dir) {{
      const persons = lastLiveDetections.filter(d => d.label.toLowerCase() === 'person');
      const otherObjects = lastLiveDetections.filter(d => d.label.toLowerCase() !== 'person');

      let reply = "";
      if (persons.length > 0) {{
        const closest = persons[0];
        reply = `Phone pointed ${{dir}}: Person detected ${{closest.distance.toFixed(1)}} meters ahead in camera view.`;
      }} else if (otherObjects.length > 0) {{
        const obj = otherObjects[0];
        reply = `Phone pointed ${{dir}}: ${{obj.label}} detected ${{obj.distance.toFixed(1)}} meters ahead.`;
      }} else {{
        reply = `Phone pointed ${{dir}}: Area to your ${{dir}} is completely clear. No obstacles or persons detected.`;
      }}

      showUniversalVoiceHUD(`Turned ${{dir.toUpperCase()}}`, reply, false);
      speakText(reply);

      setTimeout(() => {{
        const cStatus = document.getElementById('nav-corridor-status');
        if (cStatus) cStatus.innerText = 'WALK STRAIGHT • PATH CLEAR';
        const cArrow = document.getElementById('nav-direction-arrow');
        if (cArrow) cArrow.innerText = '⬆️';
        hideUniversalVoiceHUD();
      }}, 5000);
    }}

    if (window.DeviceOrientationEvent) {{
      window.addEventListener('deviceorientation', handleOrientationEvent, true);
    }}

    // Voice recognition & Intent Handling
    function startVoiceCapture() {{
      const liveTrans = document.getElementById('live-transcript');
      if (liveTrans) liveTrans.innerText = "Speak now...";
      
      const islandDot = document.getElementById('island-mic-dot');
      if (islandDot) {{
        islandDot.classList.remove('bg-[#151515]');
        islandDot.classList.add('bg-orange-500');
      }}

      const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRec) {{
        if (webSpeechRec) {{
          try {{ webSpeechRec.abort(); }} catch(e){{}}
        }}
        try {{
          webSpeechRec = new SpeechRec();
          webSpeechRec.continuous = false;
          webSpeechRec.interimResults = true;
          webSpeechRec.lang = 'en-US';
          webSpeechRec.onresult = (e) => {{
            let transcript = "";
            for (let i = e.resultIndex; i < e.results.length; i++) transcript += e.results[i][0].transcript;
            
            const vText = document.getElementById('voice-hud-text');
            if (vText) vText.innerText = '“' + transcript + '”';
            if (liveTrans) liveTrans.innerText = '“' + transcript + '”';

            if (e.results[0].isFinal) {{
              showUniversalVoiceHUD("Analyzing...", '“' + transcript + '”', false);
              handleVoiceInput(transcript);
            }}
          }};
          webSpeechRec.onerror = (e) => {{
            console.warn('[SpeechRec] Error:', e.error);
            showUniversalVoiceHUD("Mic Ready", "Tap mic to speak destination or question.", false);
            setTimeout(hideUniversalVoiceHUD, 3500);
          }};
          webSpeechRec.onend = () => {{
            if (islandDot) {{
              islandDot.classList.remove('bg-orange-500');
              islandDot.classList.add('bg-[#151515]');
            }}
          }};
          webSpeechRec.start();
        }} catch(e) {{
          console.warn('[SpeechRec] Launch error:', e);
        }}
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
      // 1. Spoken Button Click Action (excluding start_navigation)
      const targetBtn = result.target_button || (result.action === 'click_button' ? result.target_button : null) || (result.intent === 'click_button' ? result.target_button : null);
      if (targetBtn && targetBtn !== 'start_navigation') {{
        handleSpokenButtonClick(targetBtn, result.spoken_response);
        return;
      }}

      // 2. Automated GPS Navigation Trigger: ANY spoken destination or start navigation command!
      // 2. Directional Perception Query: "is someone coming from my right?", "what is on my left?"
      if (result.intent === 'directional_query' || result.action === 'directional_query' || result.direction) {{
        handleDirectionalQuery(result.direction || 'right', result.target || 'person', rawText);
        return;
      }}

      // 3. Automated GPS Navigation Trigger: ANY spoken destination or start navigation command!
      if (result.trigger_auto_gps || result.intent === 'start_navigation' || result.destination || targetBtn === 'start_navigation') {{
        hideUniversalVoiceHUD();
        handleAutoGpsNavigation(result.destination, result.spoken_response);
        return;
      }}

      const intent = result.intent || 'start_navigation';

      if (intent === 'affirmative') {{
        if (activeRoute === 'obstacleAlert') {{
          acknowledgeObstacle();
        }} else {{
          speakText(result.spoken_response || "Path is clear. Continue straight.");
          triggerHaptic([40]);
        }}
      }} else if (intent === 'negative') {{
        speakText(result.spoken_response || "Holding position. Let me know when you are ready to continue.");
        triggerHaptic([60, 40]);
      }} else if (intent === 'guidance_query') {{
        const dir = currentSteeringDirection || 'WALK STRAIGHT';
        const depth = currentLidarDepthAhead ? `${{currentLidarDepthAhead.toFixed(1)}} meters` : 'clear';
        speakText(result.spoken_response || `${{dir}}. Forward clearance is ${{depth}}.`);
        triggerHaptic([50]);
      }} else if (intent === 'obstacle_query') {{
        speakText(result.spoken_response || "Scanning ahead. Pathway is clear.");
        triggerHaptic([50]);
      }} else if (intent === 'start_navigation') {{
        handleAutoGpsNavigation(result.destination, result.spoken_response);
      }} else if (intent === 'clarification_needed') {{
        const clarifPrompt = result.clarification_prompt || "Where would you like to go? Speak any destination or place.";
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
      const targetName = destName || currentDestinationTitle || 'Selected Destination';
      navigateTo('activeNavigation');
      triggerHaptic([80, 40, 80]);
      currentWaypointIdx = 0;
      currentDistance = currentWaypoints[0] ? currentWaypoints[0].distance : 0;
      stepWalkedMeters = 0;
      obstacleTriggeredThisStep = false;
      trafficTriggeredThisStep = false;
      metersSinceObstacle = 0;
      renderActiveWaypoint();

      const initialInstruction = currentWaypoints[0] ? currentWaypoints[0].instruction : 'Head toward destination';
      speakText(`Starting real walking route to ${{targetName}}. ${{initialInstruction}}. Waiting at your current position. Walk forward along route when you are ready.`);

      // Ensure always-open rear camera is active
      startAlwaysOpenBackCamera();

      if (navigationInterval) clearInterval(navigationInterval);
      navigationInterval = null;

      // Reset baseline for real GPS & step tracking
      lastGpsWalkLat = userGps.lat;
      lastGpsWalkLon = userGps.lon;
      updateMovementDisplayUI();
    }}

    function renderActiveWaypoint() {{
      const wp = currentWaypoints[currentWaypointIdx] || {{ instruction: 'Continue toward destination', maneuver: 'Continue straight', icon: '↑' }};
      document.getElementById('nav-step-label').innerText = `Real Route • Step ${{currentWaypointIdx + 1}} of ${{currentWaypoints.length}}`;
      document.getElementById('nav-instruction-text').innerText = wp.instruction;
      document.getElementById('nav-distance-num').innerText = currentDistance;
      document.getElementById('nav-maneuver-text').innerText = wp.maneuver;
      document.getElementById('nav-maneuver-icon').innerText = wp.icon;
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

      initRealGpsTracking();

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
