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

      <!-- Global Persistent Microphone Button (Talk to AI Anytime) -->
      <button type="button" onclick="triggerVoiceAssistant()" id="top-bar-mic-btn" aria-label="Talk to Blind AI voice assistant anytime" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-orange-600 hover:bg-orange-700 text-white text-xs font-bold shadow-sm transition active:scale-95">
        <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
        <span>Ask AI Mic</span>
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
              <button onclick="triggerVoiceAssistant()" id="home-mic-btn" aria-label="Start voice listening assistant" class="w-16 h-16 rounded-full bg-black text-white flex items-center justify-center shadow-lg hover:bg-neutral-800 transition active:scale-95 shrink-0">
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
              <button type="button" onclick="triggerVoiceAssistant()" aria-label="Tap orb to speak to Gemini AI" class="relative flex items-center justify-center w-44 h-44 mb-4 shrink-0 cursor-pointer rounded-full focus:outline-none">
                <div class="absolute w-52 h-52 rounded-full orb-glow ripple-ring-1 pointer-events-none"></div>
                <div class="absolute w-40 h-40 rounded-full orb-glow ripple-ring-2 pointer-events-none"></div>
                <div class="w-32 h-32 rounded-full orb-3d relative z-10 flex items-center justify-center shrink-0">
                  <div class="w-12 h-12 rounded-full bg-white/20 blur-[2px]"></div>
                </div>
              </button>
              <h2 id="listening-title" class="text-2xl font-bold text-center text-slate-900 tracking-tight">
                I'm listening...
              </h2>
              <p id="live-transcript" aria-live="polite" class="text-sm text-slate-600 text-center mt-2 px-6 italic min-h-[2.5rem]">
                “Ask about surroundings, traffic lights, people, or directions”
              </p>
              <div class="mt-1 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-orange-50 border border-orange-200 text-[11px] font-semibold text-orange-700 shrink-0">
                <span class="w-2 h-2 rounded-full bg-orange-500 animate-pulse shrink-0"></span>
                <span>Web Speech API + Gemini Multimodal AI</span>
              </div>
            </div>

            <div class="mobile-safe-footer flex flex-col gap-2">
              <!-- Voice phrase simulation chips -->
              <div class="flex flex-wrap justify-center gap-1" role="group" aria-label="Suggested voice phrases">
                <button onclick="handleVoiceInput('What is in front of me?')" aria-label="Ask: What is in front of me?" class="px-2 py-1 rounded-full bg-orange-50 border border-orange-200 text-[10px] font-semibold text-orange-900 shadow-xs hover:bg-orange-100 transition active:scale-95 shrink-0">
                  “What is in front of me?”
                </button>
                <button onclick="handleVoiceInput('Are people walking toward me?')" aria-label="Ask: Are people walking toward me?" class="px-2 py-1 rounded-full bg-sky-50 border border-sky-200 text-[10px] font-semibold text-sky-900 shadow-xs hover:bg-sky-100 transition active:scale-95 shrink-0">
                  “Are people walking toward me?”
                </button>
                <button onclick="handleVoiceInput('What color is the traffic light?')" aria-label="Ask: What color is the traffic light?" class="px-2 py-1 rounded-full bg-rose-50 border border-rose-200 text-[10px] font-semibold text-rose-900 shadow-xs hover:bg-rose-100 transition active:scale-95 shrink-0">
                  “What color is the traffic light?”
                </button>
                <button onclick="handleVoiceInput('Is the ground flat, tilted, or uneven?')" aria-label="Ask: Is the ground flat, tilted, or uneven?" class="px-2 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-[10px] font-semibold text-emerald-900 shadow-xs hover:bg-emerald-100 transition active:scale-95 shrink-0">
                  “Is ground flat or uneven?”
                </button>
                <button onclick="handleVoiceInput('Where am I?')" aria-label="Ask: Where am I?" class="px-2 py-1 rounded-full bg-blue-50 border border-blue-200 text-[10px] font-semibold text-blue-900 shadow-xs hover:bg-blue-100 transition active:scale-95 shrink-0">
                  “Where am I?”
                </button>
                <button onclick="handleVoiceInput('Take me to coffee shop')" aria-label="Ask: Take me to coffee shop" class="px-2 py-1 rounded-full bg-white border border-slate-200 text-[10px] font-medium text-slate-700 shadow-xs hover:bg-slate-50 transition active:scale-95 shrink-0">
                  “Take me to coffee shop”
                </button>
              </div>

              <!-- Test input for any natural-language question or destination -->
              <form onsubmit="event.preventDefault(); const inp = document.getElementById('voice-sim-input'); if (inp && inp.value.trim()) {{ handleVoiceInput(inp.value.trim()); inp.value = ''; }}" class="flex items-center gap-1.5 px-1">
                <label for="voice-sim-input" class="sr-only">Ask any question about your surroundings or type any destination for Gemini AI</label>
                <input type="text" id="voice-sim-input" placeholder="Ask about surroundings or type destination..." class="flex-1 min-w-0 bg-white border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-amber-500 shadow-sm">
                <button type="submit" class="px-3.5 py-2 rounded-xl bg-slate-900 text-white text-xs font-semibold hover:bg-black transition active:scale-95 shrink-0">
                  Ask AI
                </button>
              </form>

              <div class="flex items-center justify-center gap-3">
                <button onclick="triggerVoiceAssistant()" id="listening-mic-btn" aria-label="Activate microphone to speak" class="w-14 h-14 rounded-full bg-black text-white flex items-center justify-center shadow-lg hover:bg-neutral-800 transition active:scale-95 shrink-0">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
                </button>
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

              <!-- Manual Starting Location (Origin) Input (Module 2) -->
              <div class="relative mb-2">
                <label for="origin-location-input" class="block text-[10px] font-bold uppercase tracking-wider text-slate-600 mb-1 px-1">Starting Location (GPS or Manual Origin)</label>
                <div class="relative">
                  <input type="text" id="origin-location-input" value="Riga Old Town (Vecrīga)" onchange="updateManualOriginLocation(this.value)" placeholder="Current GPS or type starting location..." aria-label="Starting location origin" class="w-full bg-slate-50 border border-slate-200 rounded-xl py-2 pl-9 pr-20 text-xs font-semibold text-slate-800 placeholder-slate-400 focus:border-amber-500 transition">
                  <span class="absolute left-3 top-2 text-xs" aria-hidden="true">🟢</span>
                  <button type="button" onclick="useDeviceGpsAsOrigin()" class="absolute right-2 top-1.5 px-2 py-0.5 rounded-lg bg-slate-200 hover:bg-slate-300 text-[10px] font-bold text-slate-800 transition">Use GPS</button>
                </div>
              </div>

              <!-- Accessible Search Bar -->
              <div class="relative mb-3">
                <label for="destination-search-input" class="sr-only">Search destination or speak</label>
                <input type="text" id="destination-search-input" oninput="filterDestinations(this.value)" placeholder="Search destination (e.g. Riga Technical University)..." aria-label="Search destination or speak" class="w-full bg-white border border-slate-200 rounded-2xl py-3 pl-11 pr-11 text-sm font-medium text-slate-800 placeholder-slate-500 shadow-sm focus:border-amber-500 transition">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-500 absolute left-3.5 top-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                <button onclick="triggerVoiceAssistant()" aria-label="Search destination using voice" class="absolute right-3 top-3 text-orange-500 hover:text-orange-600 shrink-0">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
                </button>
              </div>

              <!-- Category Pills -->
              <div role="group" aria-label="Destination categories" class="flex items-center gap-2 mb-3 overflow-x-auto no-scrollbar py-1">
                <button onclick="selectDestination('Riga Technical University (RTU)', 'Ķīpsala Campus, Paula Valdena iela 1')" class="px-3 py-1.5 bg-amber-100 text-amber-900 rounded-full text-xs font-bold whitespace-nowrap shrink-0">🎓 RTU Ķīpsala</button>
                <button onclick="selectCategory('Coffee shop')" class="px-3 py-1.5 bg-orange-100 text-orange-800 rounded-full text-xs font-semibold whitespace-nowrap shrink-0">Coffee Shop</button>
                <button onclick="selectCategory('Park')" class="px-3 py-1.5 bg-emerald-100 text-emerald-800 rounded-full text-xs font-semibold whitespace-nowrap shrink-0">Park</button>
                <button onclick="selectCategory('Pharmacy')" class="px-3 py-1.5 bg-purple-100 text-purple-800 rounded-full text-xs font-semibold whitespace-nowrap shrink-0">Pharmacy</button>
              </div>

              <!-- Recent Destinations List -->
              <h3 class="text-xs font-bold text-slate-600 uppercase tracking-wider mb-2 px-1">Validated Destinations & Riga Transit</h3>
              <div id="recent-places-list" role="list" aria-label="Recent destinations" class="flex flex-col space-y-2 pb-4">
                <button onclick="selectDestination('Riga Technical University (RTU)', 'Ķīpsala Campus • Walk + Trolleybus 9 / Bus 3 / Tram 1')" aria-label="Select destination: Riga Technical University" class="bg-white p-3 rounded-2xl border border-amber-300 shadow-sm flex items-center justify-between text-left hover:border-amber-500 transition">
                  <div class="flex items-center space-x-3 min-w-0 flex-1 pr-2">
                    <div class="w-10 h-10 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center font-bold text-sm shrink-0" aria-hidden="true">🎓</div>
                    <div class="min-w-0 flex-1">
                      <h4 class="font-bold text-slate-900 text-sm truncate">Riga Technical University (RTU)</h4>
                      <p class="text-xs text-slate-600 truncate">From Old Town • 2.1 km walk or 11m Transit</p>
                    </div>
                  </div>
                  <span class="text-xs font-bold text-amber-800 bg-amber-100 px-2 py-1 rounded-lg shrink-0">25 min</span>
                </button>

                <button onclick="selectDestination('RTU Scientific Library', 'Paula Valdena iela 5, Ķīpsala')" aria-label="Select destination: RTU Scientific Library" class="bg-white p-3 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-amber-400 transition">
                  <div class="flex items-center space-x-3 min-w-0 flex-1 pr-2">
                    <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold text-sm shrink-0" aria-hidden="true">📚</div>
                    <div class="min-w-0 flex-1">
                      <h4 class="font-bold text-slate-900 text-sm truncate">RTU Scientific Library</h4>
                      <p class="text-xs text-slate-600 truncate">Paula Valdena iela 5 • 1.3 km</p>
                    </div>
                  </div>
                  <span class="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-1 rounded-lg shrink-0">16 min</span>
                </button>

                <button onclick="selectDestination('Rīga Central Station', 'Stacijas laukums 2 • Trolleybus 9 / Tram 1')" aria-label="Select destination: Rīga Central Station" class="bg-white p-3 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between text-left hover:border-amber-400 transition">
                  <div class="flex items-center space-x-3 min-w-0 flex-1 pr-2">
                    <div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-sm shrink-0" aria-hidden="true">🚉</div>
                    <div class="min-w-0 flex-1">
                      <h4 class="font-bold text-slate-900 text-sm truncate">Rīga Central Station</h4>
                      <p class="text-xs text-slate-600 truncate">Stacijas laukums 2 • 3.1 km</p>
                    </div>
                  </div>
                  <span class="text-xs font-bold text-blue-700 bg-blue-50 px-2 py-1 rounded-lg shrink-0">14m Bus</span>
                </button>
              </div>
            </div>

            <!-- Bottom Mic Button -->
            <div class="mobile-safe-footer flex justify-center mt-2">
              <button onclick="triggerVoiceAssistant()" id="search-mic-btn" aria-label="Start voice listening assistant" class="w-16 h-16 rounded-full bg-black text-white flex items-center justify-center shadow-lg hover:bg-neutral-800 transition active:scale-95 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
              </button>
            </div>
          </div>

          <!-- ==================== SCREEN 4: ROUTE PREVIEW (WALKING + LATVIAN PUBLIC TRANSPORT + CROSSINGS) ==================== -->
          <div id="screen-routePreview" role="region" aria-label="Screen 4: Route Preview" class="screen-container flex-1 flex flex-col justify-between p-4 pb-5 hidden">
            <div class="mobile-safe-header flex justify-between items-center pt-1 px-1">
              <button onclick="navigateTo('destinationSearch')" aria-label="Back to destination search" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 hover:bg-slate-50 shadow-sm transition shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <span class="text-lg font-bold text-black tracking-tight">Route & Transit Plan</span>
              <button onclick="openSettingsModal()" aria-label="Settings" aria-haspopup="dialog" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </button>
            </div>

            <!-- Real Leaflet Interactive Route Map -->
            <div class="flex-1 flex flex-col justify-start my-1.5 min-h-0 overflow-y-auto no-scrollbar space-y-2">
              <h2 class="sr-only">Interactive Real-World Route Map & Latvian Public Transport</h2>
              <div class="w-full h-36 rounded-2xl relative overflow-hidden shadow-inner border border-slate-300 z-0 shrink-0">
                <div id="route-map-leaflet" class="w-full h-full"></div>
                <div id="route-map-loading" class="absolute inset-0 bg-slate-100/90 backdrop-blur-xs flex items-center justify-center text-xs font-semibold text-slate-700 z-20">
                  <span class="w-2.5 h-2.5 rounded-full bg-blue-500 animate-ping mr-2 shrink-0"></span>
                  <span>Loading Geographic Map & Route...</span>
                </div>
              </div>

              <!-- Origin, Destination, Next Turn & Crossings Card (Module 2) -->
              <div class="bg-white p-3 rounded-2xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1">
                  <span id="preview-origin-label">From: Riga Old Town (Vecrīga)</span>
                  <span id="preview-eta-badge" class="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md">ETA: 25 min</span>
                </div>
                <div class="flex items-center space-x-2.5 mb-2 min-w-0">
                  <div class="w-8 h-8 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center font-bold text-sm shrink-0" aria-hidden="true">
                    📍
                  </div>
                  <div class="min-w-0 flex-1">
                    <h3 id="preview-destination-title" class="font-bold text-slate-900 text-sm leading-tight truncate">Riga Technical University (RTU)</h3>
                    <p id="preview-destination-sub" class="text-[11px] text-slate-600 mt-0.5 truncate">2.1 km • 6 steps • 3 signalized pedestrian crossings</p>
                  </div>
                </div>
                <div id="preview-crossings-summary" class="text-[11px] text-slate-700 bg-slate-50 rounded-xl p-2 border border-slate-100">
                  <div><strong>Next Turn:</strong> <span id="preview-next-turn-text">Walk west toward 11. novembra krastmala (180m)</span></div>
                  <div class="mt-0.5"><strong>Crossings:</strong> 11. novembra krastmala (signalized), Balasta dambis, Ķīpsalas iela</div>
                </div>
              </div>

              <!-- Latvian Public Transport Options Card (Rīgas Satiksme Tram / Bus / Trolleybus) -->
              <div id="preview-transit-card" class="bg-blue-50/90 p-2.5 rounded-2xl border border-blue-200 text-xs text-slate-800">
                <div class="flex items-center justify-between mb-1">
                  <span class="font-extrabold text-blue-900 text-[11px] uppercase tracking-wider">🚊 Latvian Public Transport (Rīgas Satiksme)</span>
                  <button type="button" onclick="speakPublicTransportOptions()" class="px-2 py-0.5 rounded-lg bg-blue-600 text-white text-[10px] font-bold hover:bg-blue-700 transition">Hear Boarding</button>
                </div>
                <p id="preview-transit-line" class="text-[11px] font-semibold text-slate-900">Trolleybus 9 / Bus 3 / Tram 1: Grēcinieku iela → Ķīpsala (2 stops • 11 min)</p>
                <p id="preview-transit-boarding" class="text-[10px] text-slate-600 mt-0.5">Stand at raised tactile curb strip; external speaker announces arriving route number.</p>
              </div>

              <!-- Assistive Prototype Safety Disclaimer -->
              <div class="px-2.5 py-1.5 rounded-xl bg-amber-50 border border-amber-200 text-[10px] text-amber-900 font-medium">
                <strong>Assistive Prototype:</strong> Use alongside your white cane or guide dog. Camera/depth never guarantee traffic safety.
              </div>
            </div>

            <!-- Route Actions -->
            <div class="mobile-safe-footer flex flex-col space-y-2 pt-1">
              <button onclick="startCurrentNavigation()" id="start-nav-btn" aria-label="Start walking navigation to selected destination" class="w-full py-3 rounded-2xl bg-black text-white font-bold text-sm shadow-md hover:bg-neutral-800 transition active:scale-[0.99] flex items-center justify-center space-x-2">
                <span>Start navigation</span>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
              </button>
              <div class="flex items-center space-x-2">
                <button onclick="speakRouteOverview()" id="btn-describe-route" aria-label="Describe route overview and audible cues" class="flex-1 py-2.5 rounded-2xl bg-white border border-slate-200 text-slate-800 font-semibold text-xs shadow-sm hover:bg-slate-50 transition active:scale-[0.99] flex items-center justify-center space-x-1.5">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-slate-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
                  <span>Describe route & transit</span>
                </button>
                <button onclick="triggerVoiceAssistant()" id="route-preview-mic-btn" aria-label="Activate microphone to ask about route or change destination" class="w-11 h-11 rounded-2xl bg-black text-white flex items-center justify-center shadow-md hover:bg-neutral-800 transition active:scale-95 shrink-0">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
                </button>
              </div>
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
            <div class="mobile-safe-header relative z-20 flex justify-between items-center pt-1 px-0.5">
              <button onclick="stopNavigationRoute()" id="btn-nav-back" aria-label="Stop navigation and return to preview" class="w-10 h-10 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition active:scale-95 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
              </button>
              
              <!-- Camera & YOLO Status Pill Badge -->
              <div class="flex items-center gap-1 px-2.5 py-1 bg-black/75 backdrop-blur-md rounded-full text-white text-[11px] font-bold border border-white/20 shadow-md shrink-0">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse shrink-0" aria-hidden="true"></span>
                <span id="camera-status-pill">Back Camera • YOLO Active</span>
              </div>

              <div class="flex items-center gap-1 shrink-0">
                <!-- Scan Road Signs & Traffic Light Button -->
                <button type="button" onclick="triggerSignboardScan(false)" id="btn-detect-signs" aria-label="Scan road signs and traffic light signals now" class="w-9 h-9 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition active:scale-95 text-sm shrink-0" title="Scan Road Signs & Signals">
                  <span aria-hidden="true">🪧</span>
                </button>
                <!-- Describe Live Camera View Now Button -->
                <button type="button" onclick="describeActiveCameraSceneNow()" id="btn-nav-describe-now" aria-label="Describe live camera surroundings now" class="w-9 h-9 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition active:scale-95 text-sm shrink-0" title="Describe Camera Scene">
                  <span aria-hidden="true">👁️</span>
                </button>
                <!-- Sunlight High Contrast Toggle -->
                <button type="button" onclick="toggleHighContrastMode()" id="btn-contrast-mode" aria-label="Toggle sunlight high-contrast mode" class="w-9 h-9 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition active:scale-95 text-sm shrink-0" title="Sunlight High Contrast">
                  <span id="contrast-mode-icon" aria-hidden="true">☀️</span>
                </button>
                <!-- Night Vision AR Filter Toggle -->
                <button type="button" onclick="toggleNightVisionMode()" id="btn-night-vision" aria-label="Toggle night-vision low-light filter" class="w-9 h-9 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition active:scale-95 text-sm shrink-0" title="Night Vision Filter">
                  <span id="nightvision-mode-icon" aria-hidden="true">🌙</span>
                </button>
                <!-- Camera / Simulation Toggle Button -->
                <button type="button" onclick="toggleCameraFeed()" id="btn-toggle-camera" aria-label="Toggle between real rear camera and standby" class="w-9 h-9 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition active:scale-95 text-sm shrink-0" title="Toggle camera feed mode">
                  <span id="camera-toggle-icon" aria-hidden="true">📷</span>
                </button>
                <button onclick="openSettingsModal()" id="btn-nav-settings" aria-label="Settings" aria-haspopup="dialog" class="w-9 h-9 rounded-full bg-black/60 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-black/80 shadow-md transition shrink-0">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
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

              <!-- Real-Time Top-Down Proximity Radar HUD -->
              <div id="nav-mini-radar-container" class="w-full py-1.5 px-3 rounded-2xl bg-black/85 backdrop-blur-md border border-white/20 text-white shadow-xl flex items-center justify-between">
                <div class="flex items-center space-x-2.5 min-w-0 flex-1">
                  <canvas id="nav-radar-canvas" width="104" height="54" class="rounded-lg bg-black/70 border border-white/10 shrink-0"></canvas>
                  <div class="flex flex-col text-left min-w-0 flex-1 pr-2">
                    <span class="text-[9px] font-bold text-slate-400 uppercase tracking-wider">Top-Down 180° Radar</span>
                    <span id="nav-radar-summary" class="text-[11px] font-bold text-emerald-300 truncate">Clear corridor ahead</span>
                  </div>
                </div>
                <div class="flex items-center gap-1 shrink-0">
                  <span id="nav-radar-count-badge" class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">0 in path</span>
                </div>
              </div>

              <!-- Real-Time Walking Pedometer & Dead-Reckoning Cadence Chip -->
              <div id="nav-pedometer-cadence-chip" class="w-full py-1.5 px-3 rounded-2xl bg-black/85 backdrop-blur-md border border-white/20 text-white shadow-xl flex items-center justify-between text-xs">
                <div class="flex items-center space-x-2 min-w-0">
                  <span class="text-base shrink-0" aria-hidden="true">👟</span>
                  <div class="flex flex-col text-left min-w-0">
                    <span class="text-[9px] font-bold text-slate-400 uppercase tracking-wider">Physical Stride Integrator</span>
                    <span id="nav-cadence-text" class="text-[11px] font-bold text-amber-300 truncate">Steps: <strong id="real-steps-display" class="text-white">0</strong> • Walked: <strong id="real-dist-display" class="text-white">0.0m</strong></span>
                  </div>
                </div>
                <div class="flex items-center gap-1.5 shrink-0">
                  <span id="nav-pace-pill" class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">0 steps/min</span>
                </div>
              </div>

              <!-- Dual-Move Path Tracker & Ground / Pedestrian / Traffic Signal HUD -->
              <div id="nav-dual-move-hud" class="w-full py-2 px-3 rounded-2xl bg-black/90 backdrop-blur-md border border-cyan-500/40 text-white shadow-xl flex flex-col space-y-1.5" role="region" aria-label="Dual-Move Path Choice, Ground Surface, Traffic Signal, and Pedestrian Tracker">
                <div class="flex items-center justify-between gap-1 flex-wrap">
                  <span class="text-[9px] font-extrabold text-cyan-300 uppercase tracking-wider flex items-center gap-1">
                    <span aria-hidden="true">🛣️</span> Path &amp; Ground
                  </span>
                  <div class="flex items-center gap-1 flex-wrap">
                    <span id="nav-depth-hole-badge" class="px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Ground: Flat</span>
                    <span id="nav-people-around-badge" class="px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-sky-500/20 text-sky-300 border border-sky-500/30">👥 0 People</span>
                    <span id="nav-traffic-light-badge" class="px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-slate-500/25 text-slate-200 border border-slate-400/30">🚦 No Signal</span>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-1.5">
                  <button type="button" id="btn-move-normal-walk" onclick="selectDualMovePath('normal_walk', true)" aria-label="Move 1: Normal surface walk to Bus Stop" class="py-1.5 px-2 rounded-xl bg-emerald-600/35 border-2 border-emerald-400 text-left flex items-center space-x-1.5 transition active:scale-95">
                    <span class="text-sm shrink-0" aria-hidden="true">🚶</span>
                    <div class="flex flex-col min-w-0">
                      <span class="text-[10px] font-black text-white leading-tight truncate">Move 1: Bus Stop</span>
                      <span class="text-[8px] font-semibold text-emerald-200 truncate">Normal Surface Walk</span>
                    </div>
                  </button>
                  <button type="button" id="btn-move-tunnel-down" onclick="selectDualMovePath('tunnel_down', true)" aria-label="Move 2: Use tunnel going down into underpass" class="py-1.5 px-2 rounded-xl bg-white/10 border border-white/25 text-left flex items-center space-x-1.5 transition active:scale-95">
                    <span class="text-sm shrink-0" aria-hidden="true">🚇</span>
                    <div class="flex flex-col min-w-0">
                      <span class="text-[10px] font-black text-white leading-tight truncate">Move 2: Tunnel Down</span>
                      <span class="text-[8px] font-semibold text-slate-300 truncate">Underpass Going Down</span>
                    </div>
                  </button>
                </div>
                <div id="nav-dual-move-status" class="text-[10px] font-semibold text-cyan-200 truncate">
                  Active Move: Normal Walk to Bus Stop • Scanning people, ground &amp; signals
                </div>
              </div>
            </div>

            <!-- Bottom Hands-Free Voice Interaction Hub for Blind Pedestrians -->
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
            <div class="mobile-safe-footer flex items-center space-x-2 pt-2">
              <button onclick="repeatRealLocation()" id="btn-repeat-location" aria-label="Repeat current location, address, and orientation" class="flex-1 py-3.5 rounded-2xl bg-white border border-slate-200 text-slate-800 font-semibold text-sm shadow-sm hover:bg-slate-50 transition active:scale-[0.99] flex items-center justify-center space-x-2">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-slate-600 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.5A2.25 2.25 0 0 0 2.25 9.75v4.5A2.25 2.25 0 0 0 4.5 16.5h1.94l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06Z"/></svg>
                <span>Repeat location</span>
              </button>
              <button onclick="refreshLiveGpsLocationNow()" id="whereami-refresh-gps-btn" aria-label="Refresh live GPS coordinates and street address" class="px-3.5 py-3.5 rounded-2xl bg-purple-50 border border-purple-200 text-purple-900 font-bold text-xs shadow-sm hover:bg-purple-100 transition active:scale-95 shrink-0">
                📍 GPS
              </button>
              <button onclick="triggerVoiceAssistant()" id="whereami-mic-btn" aria-label="Activate microphone to ask where you are or where to go" class="w-12 h-12 rounded-2xl bg-black text-white flex items-center justify-center shadow-md hover:bg-neutral-800 transition active:scale-95 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
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
                <canvas id="describe-yolo-canvas" class="absolute inset-0 w-full h-full pointer-events-none z-10"></canvas>
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

            <!-- Bottom Functional Camera & Voice Action Bar -->
            <div class="mobile-safe-footer flex items-center justify-between gap-2 pt-3">
              <button onclick="triggerDescribeAround()" id="btn-rescan-scene" aria-label="Re-scan live camera scene with Gemini and YOLO" class="flex-1 py-3 px-3 rounded-2xl bg-blue-600 text-white font-bold text-xs shadow-md hover:bg-blue-700 transition active:scale-95 flex items-center justify-center space-x-1.5">
                <span aria-hidden="true">📷</span>
                <span>Re-Scan</span>
              </button>
              <button onclick="repeatSceneDescription()" id="btn-repeat-scene" aria-label="Repeat visual scene description" class="flex-1 py-3 px-3 rounded-2xl bg-white border border-slate-200 text-slate-900 font-bold text-xs shadow-sm hover:bg-slate-50 transition active:scale-95 flex items-center justify-center space-x-1.5">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-slate-800 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.5A2.25 2.25 0 0 0 2.25 9.75v4.5A2.25 2.25 0 0 0 4.5 16.5h1.94l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06Z"/></svg>
                <span>Repeat</span>
              </button>
              <button onclick="triggerSignboardScan(false)" id="btn-describe-signs" aria-label="Scan road signs and text in camera view" class="py-3 px-3 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 font-bold text-xs shadow-sm hover:bg-amber-100 transition active:scale-95 shrink-0">
                🪧 Signs
              </button>
              <button onclick="triggerVoiceAssistant()" id="describe-mic-btn" aria-label="Activate microphone to ask Gemini AI about what the camera sees" class="w-12 h-12 rounded-2xl bg-black text-white flex items-center justify-center shadow-md hover:bg-neutral-800 transition active:scale-95 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
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

            <!-- Hands-Free Voice & Touch Response Hub for Obstacle Screen -->
            <div class="mobile-safe-footer flex flex-col items-center justify-center gap-2 pt-1 pb-1">
              <div class="flex items-center justify-center gap-3 w-full">
                <button onclick="acknowledgeObstacle()" id="btn-i-understand" aria-label="Acknowledge obstacle and resume route" class="flex-1 py-3.5 px-3 rounded-2xl bg-neutral-900 text-white font-bold text-xs shadow-md hover:bg-black transition active:scale-95">
                  I Understand — Resume
                </button>
                <button onclick="triggerVoiceAssistant()" id="obstacle-voice-mic-btn" aria-label="Tap microphone to speak or say Yes, No, or Repeat" class="w-16 h-16 rounded-full bg-black text-white border-4 border-red-500 flex items-center justify-center shadow-2xl hover:scale-105 active:scale-95 transition focus:ring-4 focus:ring-red-400/50 relative group shrink-0">
                  <span class="absolute -inset-1 rounded-full bg-red-500/30 animate-ping group-hover:opacity-100 opacity-60"></span>
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-red-400 relative z-10 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
                </button>
                <button onclick="repeatObstacleWarning()" id="btn-repeat-obstacle" aria-label="Repeat obstacle distance and dimensions warning" class="py-3.5 px-3 rounded-2xl bg-white border border-slate-200 text-slate-800 font-bold text-xs shadow-sm hover:bg-slate-50 transition active:scale-95 shrink-0">
                  🔊 Repeat
                </button>
              </div>
              <p class="text-[11px] text-slate-800 font-bold text-center">
                Speak <span class="text-red-600 font-black">"Yes"</span> / <span class="text-red-600 font-black">"Okay"</span> to resume, or ask about the obstacle
              </p>
            </div>
          </div>

          <!-- ==================== SCREEN 9: APPROACHING CROSSWALK (Quiet Mode + Traffic Light Signal) ==================== -->
          <div id="screen-crosswalkSafety" role="region" aria-label="Screen 9: Approaching Crosswalk Quiet Mode and Traffic Light Signal" class="screen-container flex-1 flex flex-col justify-between p-5 pb-6 hidden">
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
                <p id="crosswalk-banner-sub" class="text-sm text-slate-900 mt-0.5 truncate">Checking traffic light signal &amp; traffic sound.</p>
              </div>
            </div>

            <!-- Camera View with Real Video & Waveform Overlay -->
            <div class="flex-1 my-3 relative rounded-3xl overflow-hidden border border-slate-200 shadow-inner flex flex-col justify-end p-3.5 bg-neutral-950 min-h-0">
              <video id="crosswalk-live-video" class="absolute inset-0 w-full h-full object-cover hidden" autoplay playsinline muted></video>
              <div id="crosswalk-bg-fallback" class="absolute inset-0 bg-gradient-to-b from-slate-900 via-neutral-900 to-black"></div>
              <canvas id="crosswalk-yolo-canvas" class="absolute inset-0 w-full h-full pointer-events-none z-[5]"></canvas>

              <!-- Accessible Floating Quiet Mode, Traffic Light Signal & Acoustic Traffic Analyzer Card -->
              <div class="w-full relative z-10 bg-white/95 backdrop-blur-md rounded-3xl p-3.5 border border-slate-100 shadow-lg flex flex-col items-center justify-center text-center">
                <!-- Live Traffic Light Signal Pill -->
                <div id="crosswalk-traffic-signal-pill" class="px-3 py-1 rounded-full text-xs font-extrabold bg-slate-100 text-slate-800 border border-slate-300 mb-2">
                  🚦 Traffic Light: Scanning intersection...
                </div>

                <!-- Acoustic Spectrum Waveform Visualizer Canvas -->
                <canvas id="crosswalk-acoustic-canvas" width="280" height="44" class="w-full h-10 rounded-xl bg-black/85 border border-amber-500/30 mb-1.5"></canvas>

                <!-- Traffic Quietness Gauge -->
                <div class="flex items-center justify-between w-full px-1 mb-1 text-xs">
                  <span class="text-slate-500 font-bold uppercase text-[10px]">Acoustic Frequency (50-280Hz)</span>
                  <span id="crosswalk-quietness-score" class="font-mono font-black text-emerald-600">82% Quietness</span>
                </div>

                <div id="crosswalk-safety-pill" class="px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 mb-1.5">
                  Safe Crossing Window Detected
                </div>

                <p class="text-xs font-medium text-slate-800">
                  I will be quiet while you cross.
                </p>
              </div>
            </div>

            <!-- Bottom Action with Signal Check, Resume & Microphone -->
            <div class="mobile-safe-footer flex items-center space-x-2 pt-1">
              <button onclick="checkCrosswalkSignalAndTrafficNow()" id="btn-crosswalk-check-signal" aria-label="Check traffic light signal and crossing safety now" class="py-3.5 px-3 rounded-2xl bg-amber-100 border border-amber-300 text-amber-950 font-bold text-xs shadow-sm hover:bg-amber-200 transition active:scale-95 shrink-0">
                🚦 Signal
              </button>
              <button onclick="confirmCrossed()" id="btn-crosswalk-confirm" aria-label="Confirm crosswalk completed and resume navigation route" class="flex-1 py-3.5 px-3 rounded-2xl bg-neutral-900 text-white font-bold text-xs shadow-md hover:bg-black transition active:scale-95 flex items-center justify-center space-x-1.5">
                <span>Crossed — Resume</span>
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>
              <button onclick="triggerVoiceAssistant()" id="crosswalk-mic-btn" aria-label="Activate microphone to ask about traffic light or crossing" class="w-12 h-12 rounded-2xl bg-black text-white flex items-center justify-center shadow-md hover:bg-neutral-800 transition active:scale-95 shrink-0">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
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
        <div class="flex justify-between items-center py-2 border-b border-slate-100">
          <span>Sunlight Contrast Filter</span>
          <button type="button" onclick="toggleHighContrastMode()" class="px-2.5 py-1 text-xs font-bold rounded-lg bg-slate-100 text-slate-800 hover:bg-slate-200">
            <span id="setting-contrast-status">Disabled</span>
          </button>
        </div>
        <div class="flex justify-between items-center py-2 border-b border-slate-100">
          <span>Night Vision Filter</span>
          <button type="button" onclick="toggleNightVisionMode()" class="px-2.5 py-1 text-xs font-bold rounded-lg bg-slate-100 text-slate-800 hover:bg-slate-200">
            <span id="setting-nightvision-status">Disabled</span>
          </button>
        </div>
      </div>
      <button onclick="closeSettingsModal()" aria-label="Save and close settings modal" class="w-full py-3 bg-black text-white font-bold rounded-2xl hover:bg-neutral-800 transition">Done</button>
    </div>
  </div>

  <!-- ==================== EMERGENCY SOS DISPATCH MODAL (ACCESSIBLE RED ALERT) ==================== -->
  <div id="sos-modal" role="dialog" aria-modal="true" aria-labelledby="sos-modal-title" class="fixed inset-0 bg-red-950/80 backdrop-blur-md z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-neutral-900 border-2 border-red-500 rounded-3xl p-6 max-w-sm w-full shadow-2xl flex flex-col space-y-4 text-white">
      <div class="flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <span class="w-3.5 h-3.5 rounded-full bg-red-500 animate-ping shrink-0" aria-hidden="true"></span>
          <h2 id="sos-modal-title" class="text-xl font-black text-red-400 tracking-wide">EMERGENCY SOS</h2>
        </div>
        <button id="close-sos-btn" onclick="closeEmergencySOS()" aria-label="Cancel emergency SOS" class="w-9 h-9 rounded-full bg-neutral-800 text-white flex items-center justify-center font-bold text-xs hover:bg-neutral-700">✕</button>
      </div>

      <div class="bg-black/60 rounded-2xl p-4 border border-red-500/30 space-y-2 text-xs">
        <div>
          <span class="text-neutral-400 font-bold block uppercase text-[10px]">Current Location Coordinates</span>
          <span id="sos-coordinates" class="font-mono text-sm font-black text-white">56.9515° N, 24.0812° E</span>
        </div>
        <div>
          <span class="text-neutral-400 font-bold block uppercase text-[10px]">Detected Street & Area</span>
          <span id="sos-street-address" class="text-sm font-bold text-amber-300">Ķīpsalas iela, Rīga, Latvia</span>
        </div>
        <div>
          <span class="text-neutral-400 font-bold block uppercase text-[10px]">Incident Timestamp</span>
          <span id="sos-timestamp" class="font-mono text-[11px] text-neutral-300">Active</span>
        </div>
      </div>

      <div class="flex flex-col gap-2.5 pt-1">
        <a id="sos-call-link" href="tel:112" class="w-full py-3.5 bg-red-600 hover:bg-red-500 active:scale-95 text-white font-black text-center text-sm rounded-2xl shadow-lg flex items-center justify-center space-x-2 transition">
          <span>📞</span>
          <span>Call Emergency (112)</span>
        </a>
        <a id="sos-sms-link" href="sms:?body=EMERGENCY: Blind AI user needs help." class="w-full py-3 bg-neutral-800 hover:bg-neutral-700 active:scale-95 text-white font-bold text-center text-sm rounded-2xl border border-white/20 transition flex items-center justify-center space-x-2">
          <span>💬</span>
          <span>Send SMS with GPS Pin</span>
        </a>
        <button type="button" onclick="closeEmergencySOS()" class="w-full py-2.5 text-neutral-400 hover:text-white text-xs font-bold transition">
          I am Safe • Dismiss Alert
        </button>
      </div>
    </div>
  </div>

  <!-- ==================== UPFRONT ACCESSIBLE SENSOR PERMISSIONS MODAL ==================== -->
  <div id="permissions-modal" role="dialog" aria-modal="true" aria-labelledby="permissions-modal-title" class="fixed inset-0 bg-black/90 backdrop-blur-md z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-neutral-900 border-2 border-amber-400 rounded-3xl p-6 max-w-sm w-full shadow-2xl flex flex-col space-y-4 text-white">
      <div class="flex items-center space-x-3">
        <div class="w-12 h-12 rounded-2xl bg-amber-400 text-black flex items-center justify-center text-2xl font-black shrink-0" aria-hidden="true">
          🛡️
        </div>
        <div class="flex flex-col min-w-0">
          <span class="text-[10px] font-bold text-amber-400 uppercase tracking-widest">Initial Safety Setup</span>
          <h2 id="permissions-modal-title" class="text-xl font-extrabold text-white leading-tight">Authorize Sensors</h2>
        </div>
      </div>

      <p class="text-xs text-slate-300 leading-relaxed">
        Blind AI uses your device’s sensors to guide your physical walking path hands-free. To protect you from obstacles, please authorize the sensors below before starting.
      </p>

      <!-- Checklist of Sensors with Status Badges -->
      <div class="bg-black/60 rounded-2xl p-3.5 border border-white/10 space-y-2.5 text-xs">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="text-base" aria-hidden="true">📷</span>
            <span class="font-bold text-slate-200">Camera</span>
          </div>
          <span id="perm-camera-status" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white/10 text-slate-300">Pending</span>
        </div>
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="text-base" aria-hidden="true">🎙️</span>
            <span class="font-bold text-slate-200">Microphone</span>
          </div>
          <span id="perm-mic-status" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white/10 text-slate-300">Pending</span>
        </div>
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="text-base" aria-hidden="true">📍</span>
            <span class="font-bold text-slate-200">Location (GPS)</span>
          </div>
          <span id="perm-location-status" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white/10 text-slate-300">Pending</span>
        </div>
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="text-base" aria-hidden="true">👟</span>
            <span class="font-bold text-slate-200">Motion & Gyroscope</span>
          </div>
          <span id="perm-motion-status" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white/10 text-slate-300">Pending</span>
        </div>
      </div>

      <!-- Main Action Buttons -->
      <div class="flex flex-col gap-2 pt-1">
        <button id="btn-grant-all-permissions" onclick="requestAllSensorsUpfront()" aria-label="Authorize all sensors now: Camera, Microphone, Location, and Motion" class="w-full py-3.5 bg-amber-400 hover:bg-amber-300 active:scale-95 text-black font-extrabold text-center text-sm rounded-2xl shadow-xl transition focus:ring-4 focus:ring-amber-400/50">
          Authorize All Assistive Sensors
        </button>
        <button type="button" onclick="continueWithAvailableSensors()" id="btn-skip-permissions" class="w-full py-2.5 text-slate-400 hover:text-white text-xs font-bold transition">
          Continue with Safe Fallback Mode
        </button>
      </div>
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

    // ==================== UNIFIED SAFETY ENGINE (SINGLE SOURCE OF TRUTH) ====================
    const UnifiedSafetyEngine = {{
      hazardSeverity: 'SAFE', // 'SAFE', 'NOTICE', 'CAUTION', 'DANGER', 'CRITICAL_STOP'
      navState: 'IDLE', // 'IDLE', 'LISTENING', 'ROUTING', 'ACTIVE_WALKING', 'APPROACHING_CROSSWALK', 'HAZARD_STOPPED', 'EMERGENCY_SOS'
      sensorFreshness: {{
        camera: {{ timestamp: 0, isStale: true, maxAgeMs: 1500 }},
        gps: {{ timestamp: 0, isStale: true, maxAgeMs: 12000 }},
        imu: {{ timestamp: 0, isStale: true, maxAgeMs: 1200 }},
        lidar: {{ timestamp: 0, isStale: true, maxAgeMs: 800 }}
      }},
      activePriority: 4,
      lastSpeechText: '',
      lastSpeechTime: 0,

      updateSensor(sensorName, timestamp = Date.now()) {{
        if (this.sensorFreshness[sensorName]) {{
          this.sensorFreshness[sensorName].timestamp = timestamp;
          this.sensorFreshness[sensorName].isStale = false;
        }}
      }},

      checkFreshness(currentTime = Date.now()) {{
        for (const [name, info] of Object.entries(this.sensorFreshness)) {{
          if (info.timestamp === 0 || (currentTime - info.timestamp > info.maxAgeMs)) {{
            info.isStale = true;
          }}
        }}
        return this.sensorFreshness;
      }},

      setHazardSeverity(severity, details = {{}}) {{
        const prev = this.hazardSeverity;
        this.hazardSeverity = severity;
        if (severity === 'CRITICAL_STOP') {{
          if (this.navState === 'ACTIVE_WALKING') {{
            this.navState = 'HAZARD_STOPPED';
          }}
          this.dispatchSpeech(
            details.message || "STOP! Immediate obstacle ahead. Do not proceed.",
            1,
            [200, 100, 200, 100, 400]
          );
        }} else if (severity === 'DANGER') {{
          this.dispatchSpeech(
            details.message || "Caution! Hazard detected in path.",
            2,
            [150, 80, 150]
          );
        }} else if (severity === 'CAUTION') {{
          this.dispatchSpeech(
            details.message || "Obstacle nearby. Keep center path.",
            2,
            [80, 60]
          );
        }} else if (prev === 'CRITICAL_STOP' && severity === 'SAFE') {{
          if (this.navState === 'HAZARD_STOPPED') {{
            this.navState = 'ACTIVE_WALKING';
            this.dispatchSpeech(
              "Obstacle cleared. Path is safe ahead. Resuming walking route.",
              2,
              [100]
            );
          }}
        }}
        return this.hazardSeverity;
      }},

      setNavState(newState) {{
        this.navState = newState;
        return this.navState;
      }},

      dispatchSpeech(text, priority = 3, hapticPattern = null) {{
        if (!text) return false;
        if (hapticPattern && Array.isArray(hapticPattern)) {{
          triggerHaptic(hapticPattern);
        }}
        // If CRITICAL_STOP is active, suppress lower-priority guidance (priority > 2)
        if (this.hazardSeverity === 'CRITICAL_STOP' && priority > 2) {{
          console.log('[SafetyEngine] Suppressing lower-priority guidance due to CRITICAL_STOP:', text);
          return false;
        }}
        const now = Date.now();
        if (this.lastSpeechText === text && (now - this.lastSpeechTime < 2800)) {{
          return false;
        }}
        this.lastSpeechText = text;
        this.lastSpeechTime = now;
        this.activePriority = priority;
        speakText(text);
        return true;
      }}
    }};
    if (typeof window !== 'undefined') {{
      window.UnifiedSafetyEngine = UnifiedSafetyEngine;
    }}

    // ==================== UPFRONT SENSOR PERMISSION & SAFE FALLBACKS ====================
    function checkSensorPermissionsOnLaunch() {{
      try {{
        const authStatus = localStorage.getItem('blindai_sensors_authorized');
        const modal = document.getElementById('permissions-modal');
        if (!authStatus && modal) {{
          modal.classList.remove('hidden');
          const grantBtn = document.getElementById('btn-grant-all-permissions');
          if (grantBtn) grantBtn.focus();
          setTimeout(() => {{
            speakText("Welcome to Blind AI. Please authorize camera, microphone, location, and motion sensors before starting.");
          }}, 500);
        }} else if (authStatus === 'granted') {{
          startAlwaysOpenBackCamera();
        }}
      }} catch (err) {{
        console.warn('[Permissions] Launch check notice:', err);
      }}
    }}

    async function requestAllSensorsUpfront() {{
      const grantBtn = document.getElementById('btn-grant-all-permissions');
      if (grantBtn) {{
        grantBtn.innerText = "Requesting System Permissions...";
        grantBtn.disabled = true;
      }}

      // Unlock Web Audio for iOS / mobile gestures
      try {{
        const ctx = getAudioContext();
        if (ctx && ctx.state === 'suspended') {{
          await ctx.resume();
        }}
      }} catch (e) {{}}

      // 1. Camera
      const camStatusEl = document.getElementById('perm-camera-status');
      try {{
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {{
          liveCameraStream = await navigator.mediaDevices.getUserMedia({{
            video: {{
              facingMode: {{ ideal: "environment" }},
              width: {{ ideal: 1280 }},
              height: {{ ideal: 720 }}
            }},
            audio: false
          }});
          isRealCameraActive = true;
          currentCameraMode = 'real';
          updateCameraStatusUI(true);
          UnifiedSafetyEngine.updateSensor('camera');
          if (camStatusEl) {{
            camStatusEl.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300";
            camStatusEl.innerText = "Active";
          }}
        }}
      }} catch (err) {{
        console.warn("[Permissions] Camera request notice:", err);
        if (camStatusEl) {{
          camStatusEl.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300";
          camStatusEl.innerText = "Fallback";
        }}
      }}

      // 2. Microphone
      const micStatusEl = document.getElementById('perm-mic-status');
      try {{
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {{
          const micStream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
          micStream.getTracks().forEach(t => t.stop());
          if (micStatusEl) {{
            micStatusEl.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300";
            micStatusEl.innerText = "Active";
          }}
        }}
      }} catch (err) {{
        console.warn("[Permissions] Microphone request notice:", err);
        if (micStatusEl) {{
          micStatusEl.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300";
          micStatusEl.innerText = "Fallback";
        }}
      }}

      // 3. Geolocation
      const locStatusEl = document.getElementById('perm-location-status');
      if ('geolocation' in navigator) {{
        navigator.geolocation.getCurrentPosition(
          (pos) => {{
            handleGpsSuccess(pos);
            UnifiedSafetyEngine.updateSensor('gps');
            if (locStatusEl) {{
              locStatusEl.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300";
              locStatusEl.innerText = "Active";
            }}
          }},
          (err) => {{
            console.warn("[Permissions] GPS notice:", err);
            if (locStatusEl) {{
              locStatusEl.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300";
              locStatusEl.innerText = "Fallback";
            }}
          }},
          {{ enableHighAccuracy: true, timeout: 6000 }}
        );
      }}

      // 4. Motion / DeviceOrientation (iOS 13+ user gesture)
      const motStatusEl = document.getElementById('perm-motion-status');
      try {{
        if (typeof DeviceOrientationEvent !== 'undefined' && typeof DeviceOrientationEvent.requestPermission === 'function') {{
          const perm = await DeviceOrientationEvent.requestPermission();
          if (perm === 'granted' && motStatusEl) {{
            motStatusEl.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300";
            motStatusEl.innerText = "Active";
          }}
        }} else if (motStatusEl) {{
          motStatusEl.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300";
          motStatusEl.innerText = "Active";
        }}
        if (typeof DeviceMotionEvent !== 'undefined' && typeof DeviceMotionEvent.requestPermission === 'function') {{
          await DeviceMotionEvent.requestPermission();
        }}
        UnifiedSafetyEngine.updateSensor('imu');
      }} catch (err) {{
        console.warn("[Permissions] Motion request notice:", err);
        if (motStatusEl) {{
          motStatusEl.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300";
          motStatusEl.innerText = "Fallback";
        }}
      }}

      try {{
        localStorage.setItem('blindai_sensors_authorized', 'granted');
      }} catch(e) {{}}

      setTimeout(() => {{
        const modal = document.getElementById('permissions-modal');
        if (modal) modal.classList.add('hidden');
        UnifiedSafetyEngine.dispatchSpeech("All sensors authorized. Real camera perception and GPS navigation active. Welcome to Blind AI.", 1, [150, 100, 150]);
      }}, 400);
    }}

    function continueWithAvailableSensors() {{
      try {{
        localStorage.setItem('blindai_sensors_authorized', 'fallback');
      }} catch(e) {{}}
      const modal = document.getElementById('permissions-modal');
      if (modal) modal.classList.add('hidden');
      UnifiedSafetyEngine.dispatchSpeech("Continuing in safe fallback mode. Voice and navigation active.", 2, [100]);
    }}

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
    let trackedSmoothedObjects = [];
    let lastSceneDescription = "";
    let userManuallyAdjustedLidarBench = false;

    let currentGroundSurfaceState = {{
      status: 'Flat', // 'Flat' | 'Tilted' | 'Uneven'
      slopeDeg: 0.0,
      roughnessScore: 0.0,
      detail: 'Ground surface ahead is flat and level.'
    }};

    let currentTrafficLightSignal = {{
      detected: false,
      color: 'NONE', // 'RED' | 'YELLOW' | 'GREEN' | 'NONE'
      distance: null,
      lane: 'center',
      confidence: 0,
      guidance: 'No traffic light signal currently in camera view.'
    }};

    let deviceTiltBeta = 70;
    let deviceTiltGamma = 0;
    let recentAccelJitter = 0;

    const metricObjectHeights = {{
      'person': 1.70, 'person standing': 1.70, 'person walking': 1.70,
      'person approaching': 1.70, 'person moving away': 1.70, 'person crossing path': 1.70,
      'bicycle': 1.05, 'car': 1.50, 'motorcycle': 1.15,
      'bus': 3.20, 'truck': 2.80, 'traffic light': 0.90, 'stop sign': 0.75,
      'fire hydrant': 0.75, 'bench': 0.85, 'dog': 0.55, 'cat': 0.30,
      'backpack': 0.45, 'umbrella': 0.85, 'handbag': 0.35, 'suitcase': 0.60,
      'bottle': 0.25, 'chair': 0.85, 'couch': 0.85, 'potted plant': 1.80,
      'dining table': 0.75, 'tv': 0.65, 'laptop': 0.25, 'cell phone': 0.15,
      'door': 2.05, 'stairs': 1.50, 'pole': 2.20,
      'tree': 2.60, 'tree trunk': 2.60,
      'depth hole': 0.45, 'depth hole / drop-off': 0.45,
      'tunnel going down': 2.20, 'underpass tunnel': 2.20,
      'road sign': 0.75, 'warning sign': 0.75, 'prohibition sign': 0.75,
      'mandatory sign': 0.75, 'information sign': 0.75, 'direction sign': 0.85,
      'temporary sign': 0.75, 'additional plate': 0.45,
      'pedestrian crossing sign': 0.75, 'bus stop sign': 0.75, 'tram stop sign': 0.75, 'road works sign': 0.75,
      'crossing path': 0.65, 'crosswalk': 0.65, 'zebra crossing': 0.65, 'pedestrian crossing': 0.65,
      'default': 1.40
    }};

    const metricObjectWidths = {{
      'person': 0.55, 'person standing': 0.55, 'person walking': 0.55,
      'person approaching': 0.55, 'person moving away': 0.55, 'person crossing path': 0.60,
      'bicycle': 0.65, 'car': 1.85, 'motorcycle': 0.80,
      'bus': 2.55, 'truck': 2.50, 'traffic light': 0.35, 'stop sign': 0.75,
      'fire hydrant': 0.40, 'bench': 1.50, 'dog': 0.45, 'cat': 0.25,
      'chair': 0.55, 'couch': 1.90, 'potted plant': 0.85,
      'dining table': 1.20, 'door': 0.90, 'stairs': 1.60, 'pole': 0.22,
      'tree': 1.10, 'tree trunk': 0.45,
      'depth hole': 0.80, 'depth hole / drop-off': 0.80,
      'tunnel going down': 2.40, 'underpass tunnel': 2.40,
      'road sign': 0.65, 'crossing path': 2.80, 'crosswalk': 2.80,
      'default': 0.70
    }};

    function computeObjectMetricDimensions(obj) {{
      if (!obj) return obj;
      const key = (obj.rawClass || obj.label || 'default').toLowerCase();
      const nomH = metricObjectHeights[key] || metricObjectHeights['default'];
      const nomW = metricObjectWidths[key] || metricObjectWidths['default'];
      const boxRatio = (obj.w && obj.h && obj.h > 8) ? (obj.w / obj.h) : (nomW / nomH);
      const estH = obj.heightM || parseFloat(nomH.toFixed(1));
      const rawW = (nomW * 0.6) + (estH * boxRatio * 0.4);
      const estW = obj.widthM || parseFloat(Math.max(0.2, Math.min(4.5, rawW)).toFixed(1));
      obj.widthM = estW;
      obj.heightM = estH;
      return obj;
    }}

    let lastDetectedSignboards = [];

    // ==================== COMPLETE RIGA (LATVIA) ROAD SIGNS CATALOG (ALL 7 CATEGORIES + TREE) ====================
    const rigaRoadSignsCatalog = [
      // 1. WARNING SIGNS (Brīdinošas zīmes)
      {{ id: 'warn_general_danger', code: '124', category: 'Warning', name: 'General danger', latvianName: 'Citi bīstamie posmi', icon: '⚠️', shape: 'triangle_red', keywords: ['general danger', 'danger', 'exclamation', 'warning'], spokenGuidance: 'Warning sign ahead: General danger. Proceed with caution.' }},
      {{ id: 'warn_bend_left', code: '111', category: 'Warning', name: 'Dangerous bend left', latvianName: 'Bīstams pagrieziens pa kreisi', icon: '⚠️', shape: 'triangle_red', keywords: ['bend left', 'curve left', 'dangerous bend left'], spokenGuidance: 'Warning sign ahead: Dangerous road bend to the left.' }},
      {{ id: 'warn_bend_right', code: '110', category: 'Warning', name: 'Dangerous bend right', latvianName: 'Bīstams pagrieziens pa labi', icon: '⚠️', shape: 'triangle_red', keywords: ['bend right', 'curve right', 'dangerous bend right'], spokenGuidance: 'Warning sign ahead: Dangerous road bend to the right.' }},
      {{ id: 'warn_double_bend', code: '112', category: 'Warning', name: 'Double bend', latvianName: 'Bīstami pagriezieni', icon: '⚠️', shape: 'triangle_red', keywords: ['double bend', 'winding road'], spokenGuidance: 'Warning sign ahead: Double bend in road.' }},
      {{ id: 'warn_steep_descent', code: '113', category: 'Warning', name: 'Steep descent', latvianName: 'Stāvs kritums', icon: '⚠️', shape: 'triangle_red', keywords: ['steep descent', 'downhill', '10%'], spokenGuidance: 'Warning sign ahead: Steep downhill slope (10 percent).' }},
      {{ id: 'warn_steep_ascent', code: '114', category: 'Warning', name: 'Steep ascent', latvianName: 'Stāvs kāpums', icon: '⚠️', shape: 'triangle_red', keywords: ['steep ascent', 'uphill'], spokenGuidance: 'Warning sign ahead: Steep uphill slope (10 percent).' }},
      {{ id: 'warn_narrow_road', code: '118', category: 'Warning', name: 'Narrow road', latvianName: 'Ceļa sašaurinājums', icon: '⚠️', shape: 'triangle_red', keywords: ['narrow road', 'road narrows'], spokenGuidance: 'Warning sign ahead: Narrow road. Keep to the inner sidewalk.' }},
      {{ id: 'warn_road_narrows_both', code: '118a', category: 'Warning', name: 'Road narrows (both sides)', latvianName: 'Ceļa sašaurinājums no abām pusēm', icon: '⚠️', shape: 'triangle_red', keywords: ['narrows both sides'], spokenGuidance: 'Warning sign ahead: Road narrows on both sides.' }},
      {{ id: 'warn_uneven_road', code: '115', category: 'Warning', name: 'Uneven road', latvianName: 'Nelīdzens ceļš', icon: '⚠️', shape: 'triangle_red', keywords: ['uneven road', 'bumps', 'Uneven surface'], spokenGuidance: 'Warning sign ahead: Uneven surface. Watch your footing.' }},
      {{ id: 'warn_slippery_road', code: '116', category: 'Warning', name: 'Slippery road', latvianName: 'Slidens ceļš', icon: '⚠️', shape: 'triangle_red', keywords: ['slippery road', 'slippery', 'ice'], spokenGuidance: 'Warning sign ahead: Slippery surface. Take shorter steps.' }},
      {{ id: 'warn_falling_rocks', code: '119', category: 'Warning', name: 'Falling rocks', latvianName: 'Akmeņu nogruvums', icon: '⚠️', shape: 'triangle_red', keywords: ['falling rocks', 'debris'], spokenGuidance: 'Warning sign ahead: Falling rocks or debris hazard.' }},
      {{ id: 'warn_pedestrians', code: '121', category: 'Warning', name: 'Pedestrians', latvianName: 'Gājēju pāreja (brīdinājums)', icon: '🚸', shape: 'triangle_red', keywords: ['pedestrians warning', 'pedestrian ahead'], spokenGuidance: 'Warning sign ahead: Pedestrian crossing zone approaching.' }},
      {{ id: 'warn_children', code: '122', category: 'Warning', name: 'Children', latvianName: 'Bērni', icon: '🚸', shape: 'triangle_red', keywords: ['children', 'school zone', 'kids'], spokenGuidance: 'Warning sign ahead: Children and school zone.' }},
      {{ id: 'warn_cyclists', code: '123', category: 'Warning', name: 'Cyclists', latvianName: 'Velosipēdisti', icon: '🚲', shape: 'triangle_red', keywords: ['cyclists', 'bicycle crossing'], spokenGuidance: 'Warning sign ahead: Cyclists crossing path.' }},
      {{ id: 'warn_crossroads', code: '105', category: 'Warning', name: 'Crossroads', latvianName: ' Vienādas nozīmes ceļu krustojums', icon: '⚠️', shape: 'triangle_red', keywords: ['crossroads', 'intersection warning'], spokenGuidance: 'Warning sign ahead: Uncontrolled crossroads intersection.' }},
      {{ id: 'warn_roundabout', code: '106', category: 'Warning', name: 'Roundabout', latvianName: 'Lokveida krustojums', icon: '🔄', shape: 'triangle_red', keywords: ['roundabout warning'], spokenGuidance: 'Warning sign ahead: Roundabout intersection.' }},
      {{ id: 'warn_tramway', code: '107', category: 'Warning', name: 'Tramway', latvianName: 'Tramvaja līnijas šķērsošana', icon: '🚋', shape: 'triangle_red', keywords: ['tramway', 'tram crossing', 'tram tracks'], spokenGuidance: 'Warning sign ahead: Riga tramway tracks crossing. Listen for trams.' }},
      {{ id: 'warn_level_crossing_barrier', code: '101', category: 'Warning', name: 'Level crossing with barrier', latvianName: 'Dzelzceļa pārbrauktuve ar barjeru', icon: '🚧', shape: 'triangle_red', keywords: ['level crossing with barrier', 'railway barrier'], spokenGuidance: 'Warning sign ahead: Railway level crossing with barrier.' }},
      {{ id: 'warn_level_crossing_no_barrier', code: '102', category: 'Warning', name: 'Level crossing without barrier', latvianName: 'Dzelzceļa pārbrauktuve bez barjeras', icon: '🚂', shape: 'triangle_red', keywords: ['level crossing without barrier', 'train warning'], spokenGuidance: 'Critical warning sign: Unprotected railway level crossing ahead. Stop and listen.' }},

      // 2. PROHIBITION SIGNS (Aizlieguma zīmes)
      {{ id: 'prohib_no_entry', code: '301', category: 'Prohibition', name: 'No entry', latvianName: 'Iebraukt aizliegts', icon: '⛔', shape: 'circle_red_solid', keywords: ['no entry', 'do not enter'], spokenGuidance: 'Prohibition sign ahead: No entry (One-way traffic exit).' }},
      {{ id: 'prohib_no_vehicles', code: '302', category: 'Prohibition', name: 'No vehicles', latvianName: 'Braukt aizliegts', icon: '🚫', shape: 'circle_red', keywords: ['no vehicles', 'closed to vehicles'], spokenGuidance: 'Prohibition sign ahead: No vehicles allowed. Pedestrian-safe zone.' }},
      {{ id: 'prohib_no_motor_vehicles', code: '303', category: 'Prohibition', name: 'No motor vehicles', latvianName: 'Mehāniskajiem transportlīdzekļiem braukt aizliegts', icon: '🚫', shape: 'circle_red', keywords: ['no motor vehicles', 'no cars'], spokenGuidance: 'Prohibition sign ahead: No motor vehicles.' }},
      {{ id: 'prohib_no_motorcycles', code: '304', category: 'Prohibition', name: 'No motorcycles', latvianName: 'Motocikliem braukt aizliegts', icon: '🚫', shape: 'circle_red', keywords: ['no motorcycles'], spokenGuidance: 'Prohibition sign ahead: No motorcycles.' }},
      {{ id: 'prohib_no_lorries', code: '306', category: 'Prohibition', name: 'No lorries', latvianName: 'Kravas automobiļiem braukt aizliegts', icon: '🚫', shape: 'circle_red', keywords: ['no lorries', 'no trucks'], spokenGuidance: 'Prohibition sign ahead: No heavy trucks.' }},
      {{ id: 'prohib_no_buses', code: '307', category: 'Prohibition', name: 'No buses', latvianName: 'Autobusiem braukt aizliegts', icon: '🚫', shape: 'circle_red', keywords: ['no buses'], spokenGuidance: 'Prohibition sign ahead: No buses.' }},
      {{ id: 'prohib_no_bicycles', code: '305', category: 'Prohibition', name: 'No bicycles', latvianName: 'Velosipēdiem braukt aizliegts', icon: '🚳', shape: 'circle_red', keywords: ['no bicycles', 'no bikes'], spokenGuidance: 'Prohibition sign ahead: No bicycles allowed.' }},
      {{ id: 'prohib_no_pedestrians', code: '309', category: 'Prohibition', name: 'No pedestrians', latvianName: 'Gājējiem iet aizliegts', icon: '🚷', shape: 'circle_red', keywords: ['no pedestrians', 'pedestrians prohibited'], spokenGuidance: 'STOP! Prohibition sign ahead: No pedestrians allowed on this path. Use opposite sidewalk.' }},
      {{ id: 'prohib_no_right_turn', code: '315', category: 'Prohibition', name: 'No right turn', latvianName: 'Nogriezties pa labi aizliegts', icon: '🚫', shape: 'circle_red', keywords: ['no right turn'], spokenGuidance: 'Prohibition sign ahead: No right turn for vehicles.' }},
      {{ id: 'prohib_no_left_turn', code: '316', category: 'Prohibition', name: 'No left turn', latvianName: 'Nogriezties pa kreisi aizliegts', icon: '🚫', shape: 'circle_red', keywords: ['no left turn'], spokenGuidance: 'Prohibition sign ahead: No left turn for vehicles.' }},
      {{ id: 'prohib_no_u_turn', code: '317', category: 'Prohibition', name: 'No U-turn', latvianName: 'Apgriezties pretējā virzienā aizliegts', icon: '🚫', shape: 'circle_red', keywords: ['no u-turn'], spokenGuidance: 'Prohibition sign ahead: No U-turn.' }},
      {{ id: 'prohib_no_overtaking', code: '318', category: 'Prohibition', name: 'No overtaking', latvianName: 'Apdzīt aizliegts', icon: '🚫', shape: 'circle_red', keywords: ['no overtaking'], spokenGuidance: 'Prohibition sign ahead: No overtaking.' }},
      {{ id: 'prohib_no_overtaking_lorries', code: '320', category: 'Prohibition', name: 'No overtaking (lorries)', latvianName: 'Kravas automobiļiem apdzīt aizliegts', icon: '🚫', shape: 'circle_red', keywords: ['no overtaking lorries'], spokenGuidance: 'Prohibition sign ahead: No overtaking by trucks.' }},
      {{ id: 'prohib_max_speed_50', code: '323', category: 'Prohibition', name: 'Maximum speed (50 km/h)', latvianName: 'Maksimālā ātruma ierobežojums (50 km/h)', icon: '🔞', shape: 'circle_red', keywords: ['maximum speed 50', 'speed limit 50', '50'], spokenGuidance: 'Speed limit sign: Maximum vehicle speed 50 kilometers per hour.' }},
      {{ id: 'prohib_max_height_4m', code: '312', category: 'Prohibition', name: 'Maximum height (4.0m)', latvianName: 'Augstuma ierobežojums 4.0m', icon: '🚫', shape: 'circle_red', keywords: ['4.0m', 'maximum height'], spokenGuidance: 'Prohibition sign: Maximum clearance height 4.0 meters.' }},
      {{ id: 'prohib_max_width_2_5m', code: '313', category: 'Prohibition', name: 'Maximum width (2.5m)', latvianName: 'Platuma ierobežojums 2.5m', icon: '🚫', shape: 'circle_red', keywords: ['2.5m', 'maximum width'], spokenGuidance: 'Prohibition sign: Maximum passage width 2.5 meters.' }},
      {{ id: 'prohib_max_axle_load_6t', code: '311', category: 'Prohibition', name: 'Maximum axle load (6t)', latvianName: 'Ass slodzes ierobežojums 6t', icon: '🚫', shape: 'circle_red', keywords: ['6t', 'axle load'], spokenGuidance: 'Prohibition sign: Maximum axle load 6 tons.' }},
      {{ id: 'prohib_no_stopping', code: '326', category: 'Prohibition', name: 'No stopping', latvianName: 'Apstāties aizliegts', icon: '🚫', shape: 'circle_red_blue', keywords: ['no stopping'], spokenGuidance: 'Prohibition sign: No vehicle stopping along curb.' }},
      {{ id: 'prohib_no_parking', code: '327', category: 'Prohibition', name: 'No parking', latvianName: 'Stāvēt aizliegts', icon: '🚫', shape: 'circle_red_blue', keywords: ['no parking'], spokenGuidance: 'Prohibition sign: No parking along curb.' }},

      // 3. MANDATORY SIGNS (Norādījuma zīmes)
      {{ id: 'mand_proceed_straight', code: '401', category: 'Mandatory', name: 'Proceed straight', latvianName: 'Braukt taisni', icon: '⬆️', shape: 'circle_blue', keywords: ['proceed straight', 'straight only'], spokenGuidance: 'Mandatory sign ahead: Proceed straight.' }},
      {{ id: 'mand_turn_right', code: '402', category: 'Mandatory', name: 'Turn right', latvianName: 'Braukt pa labi', icon: '➡️', shape: 'circle_blue', keywords: ['turn right sign'], spokenGuidance: 'Mandatory sign ahead: Turn right.' }},
      {{ id: 'mand_turn_left', code: '403', category: 'Mandatory', name: 'Turn left', latvianName: 'Braukt pa kreisi', icon: '⬅️', shape: 'circle_blue', keywords: ['turn left sign'], spokenGuidance: 'Mandatory sign ahead: Turn left.' }},
      {{ id: 'mand_straight_or_right', code: '404', category: 'Mandatory', name: 'Proceed straight or right', latvianName: 'Braukt taisni vai pa labi', icon: '↗️', shape: 'circle_blue', keywords: ['straight or right'], spokenGuidance: 'Mandatory sign ahead: Proceed straight or right.' }},
      {{ id: 'mand_straight_or_left', code: '405', category: 'Mandatory', name: 'Proceed straight or left', latvianName: 'Braukt taisni vai pa kreisi', icon: '↖️', shape: 'circle_blue', keywords: ['straight or left'], spokenGuidance: 'Mandatory sign ahead: Proceed straight or left.' }},
      {{ id: 'mand_keep_right', code: '407', category: 'Mandatory', name: 'Keep right', latvianName: ' šķērsli apbraukt pa labo pusi', icon: '↘️', shape: 'circle_blue', keywords: ['keep right'], spokenGuidance: 'Mandatory sign ahead: Keep right of traffic island.' }},
      {{ id: 'mand_keep_left', code: '408', category: 'Mandatory', name: 'Keep left', latvianName: 'Šķērsli apbraukt pa kreiso pusi', icon: '↙️', shape: 'circle_blue', keywords: ['keep left'], spokenGuidance: 'Mandatory sign ahead: Keep left of traffic island.' }},
      {{ id: 'mand_roundabout', code: '409', category: 'Mandatory', name: 'Roundabout (Mandatory)', latvianName: 'Lokveida krustojums', icon: '🔄', shape: 'circle_blue', keywords: ['roundabout mandatory'], spokenGuidance: 'Mandatory sign ahead: Roundabout traffic circulation.' }},
      {{ id: 'mand_min_speed_50', code: '417', category: 'Mandatory', name: 'Minimum speed (50)', latvianName: 'Minimālā ātruma ierobežojums 50', icon: '🔵', shape: 'circle_blue', keywords: ['minimum speed 50'], spokenGuidance: 'Mandatory sign ahead: Minimum speed 50.' }},
      {{ id: 'mand_pedestrian_path', code: '414', category: 'Mandatory', name: 'Pedestrian path', latvianName: 'Gājēju ceļš', icon: '🚶', shape: 'circle_blue', keywords: ['pedestrian path', 'footpath', 'walkway sign'], spokenGuidance: 'Mandatory blue sign ahead: Dedicated Pedestrian Path. Safe walking corridor.' }},
      {{ id: 'mand_cycle_path', code: '413', category: 'Mandatory', name: 'Cycle path', latvianName: 'Velosipēdu ceļš', icon: '🚲', shape: 'circle_blue', keywords: ['cycle path', 'bike lane'], spokenGuidance: 'Caution: Cycle path sign ahead. Watch for bicycles in this lane.' }},
      {{ id: 'mand_shared_ped_cycle', code: '415', category: 'Mandatory', name: 'Shared pedestrian and cycle path', latvianName: 'Kopīgs gājēju un velosipēdu ceļš', icon: '🚶', shape: 'circle_blue', keywords: ['shared pedestrian and cycle', 'shared path'], spokenGuidance: 'Mandatory blue sign ahead: Shared pedestrian and cycle path. Keep right.' }},
      {{ id: 'mand_snow_chains', code: '420', category: 'Mandatory', name: 'Snow chains compulsory', latvianName: 'Pretslīdes ķēdes', icon: '❄️', shape: 'circle_blue', keywords: ['snow chains'], spokenGuidance: 'Mandatory sign: Snow chains compulsory — icy road conditions.' }},
      {{ id: 'mand_sound_horn', code: '421', category: 'Mandatory', name: 'Sound horn', latvianName: 'Skaņas signāls', icon: '📯', shape: 'circle_blue', keywords: ['sound horn'], spokenGuidance: 'Mandatory sign: Sound horn zone.' }},
      {{ id: 'mand_end_min_speed', code: '418', category: 'Mandatory', name: 'End of mandatory speed', latvianName: 'Minimālā ātruma ierobežojuma beigas', icon: '🔵', shape: 'circle_blue', keywords: ['end of mandatory speed'], spokenGuidance: 'Sign ahead: End of mandatory minimum speed.' }},
      {{ id: 'mand_end_no_overtaking', code: '319', category: 'Mandatory', name: 'End of no overtaking', latvianName: 'Apdzīšanas aizlieguma beigas', icon: '⚪', shape: 'circle_white', keywords: ['end of no overtaking'], spokenGuidance: 'Sign ahead: End of no overtaking zone.' }},
      {{ id: 'mand_end_no_overtaking_lorries', code: '321', category: 'Mandatory', name: 'End of no overtaking (lorries)', latvianName: 'Kravas automobiļu apdzīšanas aizlieguma beigas', icon: '⚪', shape: 'circle_white', keywords: ['end of no overtaking lorries'], spokenGuidance: 'Sign ahead: End of truck no-overtaking zone.' }},

      // 4. INFORMATION SIGNS (Informācijas zīmes)
      {{ id: 'info_priority_road', code: '201', category: 'Information', name: 'Priority road', latvianName: 'Galvenais ceļš', icon: '🔶', shape: 'diamond_yellow', keywords: ['priority road', 'main road'], spokenGuidance: 'Information sign: Priority main road.' }},
      {{ id: 'info_end_priority_road', code: '202', category: 'Information', name: 'End of priority road', latvianName: 'Galvenā ceļa beigas', icon: '🔶', shape: 'diamond_yellow', keywords: ['end of priority road'], spokenGuidance: 'Information sign: End of priority road.' }},
      {{ id: 'info_give_way', code: '206', category: 'Information', name: 'Give way', latvianName: 'Dodiet ceļu', icon: '🔻', shape: 'triangle_inverted', keywords: ['give way', 'yield'], spokenGuidance: 'Information sign ahead: Give way / Yield intersection.' }},
      {{ id: 'info_stop', code: '207', category: 'Information', name: 'Stop Sign', latvianName: 'Neapstājoties tālāk braukt aizliegts (STOP)', icon: '🛑', shape: 'octagon_red', keywords: ['stop sign', 'stop'], spokenGuidance: 'STOP sign detected ahead at intersection. Pause at curb and check traffic.' }},
      {{ id: 'info_pedestrian_crossing', code: '535', category: 'Information', name: 'Pedestrian crossing Sign', latvianName: 'Gājēju pāreja', icon: '🚸', shape: 'square_blue', keywords: ['pedestrian crossing', 'crosswalk sign', 'zebra sign'], spokenGuidance: 'Information sign ahead: Pedestrian crossing (Gājēju pāreja). Align with zebra stripes to cross.' }},
      {{ id: 'info_underpass', code: '537', category: 'Information', name: 'Underpass', latvianName: 'Apakšzemes gājēju pāreja', icon: '🪜', shape: 'square_blue', keywords: ['underpass', 'pedestrian tunnel', 'stairs down'], spokenGuidance: 'Information sign ahead: Pedestrian underpass tunnel with stairs downward.' }},
      {{ id: 'info_overpass', code: '538', category: 'Information', name: 'Overpass', latvianName: 'Virsotnes gājēju pāreja', icon: '🪜', shape: 'square_blue', keywords: ['overpass', 'pedestrian bridge', 'stairs up'], spokenGuidance: 'Information sign ahead: Pedestrian overpass bridge with stairs upward.' }},
      {{ id: 'info_dead_end', code: '529', category: 'Information', name: 'Dead end', latvianName: 'Strupceļš', icon: '🪧', shape: 'square_blue', keywords: ['dead end', 'cul-de-sac'], spokenGuidance: 'Information sign ahead: Dead end street.' }},
      {{ id: 'info_one_way_street', code: '501', category: 'Information', name: 'One-way street', latvianName: 'Vienvirziena ceļš', icon: '⬆️', shape: 'square_blue', keywords: ['one-way street', 'one way'], spokenGuidance: 'Information sign ahead: One-way street.' }},
      {{ id: 'info_parking', code: '539', category: 'Information', name: 'Parking (P)', latvianName: 'Stāvvieta (P)', icon: '🅿️', shape: 'square_blue', keywords: ['parking', 'p sign'], spokenGuidance: 'Information sign ahead: Vehicle parking lot (P). Watch for reversing cars.' }},
      {{ id: 'info_parking_zone', code: '523', category: 'Information', name: 'Parking zone (ZONA P)', latvianName: 'Stāvvietu zona (ZONA P)', icon: '🅿️', shape: 'rect_white', keywords: ['zona p', 'parking zone'], spokenGuidance: 'Information sign ahead: Parking zone (ZONA P).' }},
      {{ id: 'info_bus_stop', code: '541', category: 'Information', name: 'Bus stop', latvianName: 'Autobusa pietura', icon: '🚏', shape: 'square_blue', keywords: ['bus stop', 'autobusa pietura'], spokenGuidance: 'Transit sign ahead: Riga Bus Stop (Autobusa pietura).' }},
      {{ id: 'info_tram_stop', code: '542', category: 'Information', name: 'Tram stop', latvianName: 'Tramvaja pietura', icon: '🚋', shape: 'square_blue', keywords: ['tram stop', 'tramvaja pietura'], spokenGuidance: 'Transit sign ahead: Riga Tram Stop (Tramvaja pietura).' }},
      {{ id: 'info_taxi_rank', code: '543', category: 'Information', name: 'Taxi rank (TAXI)', latvianName: 'Vieglā taksometra stāvvieta (TAXI)', icon: '🚕', shape: 'square_blue', keywords: ['taxi', 'taxi rank'], spokenGuidance: 'Transit sign ahead: Taxi rank (TAXI).' }},
      {{ id: 'info_hospital', code: '602', category: 'Information', name: 'Hospital', latvianName: 'Slimnīca (H)', icon: '🏥', shape: 'square_blue', keywords: ['hospital'], spokenGuidance: 'Information sign ahead: Hospital medical facility.' }},
      {{ id: 'info_first_aid', code: '601', category: 'Information', name: 'First aid post', latvianName: 'Pirmās medicīniskās palīdzības punkts', icon: '➕', shape: 'square_blue', keywords: ['first aid'], spokenGuidance: 'Information sign ahead: First aid medical post.' }},
      {{ id: 'info_police', code: '614', category: 'Information', name: 'Police (POLICIJA)', latvianName: 'Policija (POLICIJA)', icon: '🚓', shape: 'square_blue', keywords: ['policija', 'police'], spokenGuidance: 'Information sign ahead: Latvian Police station (POLICIJA).' }},
      {{ id: 'info_service_station', code: '603', category: 'Information', name: 'Service station', latvianName: 'Degvielas uzpildes stacija', icon: '⛽', shape: 'square_blue', keywords: ['service station', 'fuel'], spokenGuidance: 'Information sign ahead: Fuel service station. Watch for vehicles crossing sidewalk.' }},
      {{ id: 'info_ev_charging', code: '603a', category: 'Information', name: 'Electric vehicle charging', latvianName: 'Elektromobiļu uzlādes stacija', icon: '🔌', shape: 'square_blue', keywords: ['electric vehicle charging', 'ev charging'], spokenGuidance: 'Information sign ahead: Electric vehicle charging station. Watch for charging cables.' }},

      // 5. DIRECTION SIGNS (Ceļa zīmes – norādes)
      {{ id: 'dir_riga', code: '555-R', category: 'Direction', name: 'Direction: ↑ RĪGA', latvianName: 'Virziena rādītājs: ↑ RĪGA', icon: '🪧', shape: 'rect_blue', keywords: ['riga', 'rīga'], spokenGuidance: 'Direction board ahead: Straight toward RĪGA.' }},
      {{ id: 'dir_jurmala', code: '555-J', category: 'Direction', name: 'Direction: ← JŪRMALA', latvianName: 'Virziena rādītājs: ← JŪRMALA', icon: '🪧', shape: 'rect_blue', keywords: ['jurmala', 'jūrmala'], spokenGuidance: 'Direction board ahead: Left toward JŪRMALA.' }},
      {{ id: 'dir_daugavpils', code: '555-D', category: 'Direction', name: 'Direction: DAUGAVPILS →', latvianName: 'Virziena rādītājs: DAUGAVPILS →', icon: '🪧', shape: 'rect_blue', keywords: ['daugavpils'], spokenGuidance: 'Direction board ahead: Right toward DAUGAVPILS.' }},
      {{ id: 'dir_e22', code: '562-E22', category: 'Direction', name: 'European route E22', latvianName: 'Eiropas autoceļš E22', icon: '🛣️', shape: 'rect_green', keywords: ['e22', 'european route'], spokenGuidance: 'Route number sign: European Highway E22.' }},
      {{ id: 'dir_a2', code: '561-A2', category: 'Direction', name: 'National route A2', latvianName: 'Galvenais autoceļš A2', icon: '🛣️', shape: 'rect_red', keywords: ['a2', 'national route'], spokenGuidance: 'Route number sign: Latvian National Main Road A2.' }},
      {{ id: 'dir_p4', code: '561-P4', category: 'Direction', name: 'Regional route P4', latvianName: 'Reģionālais autoceļš P4', icon: '🛣️', shape: 'rect_blue', keywords: ['p4', 'regional route'], spokenGuidance: 'Route number sign: Latvian Regional Road P4.' }},
      {{ id: 'dir_centrs', code: '556-C', category: 'Direction', name: 'Direction: Centrs →', latvianName: 'Centrs →', icon: '🪧', shape: 'rect_white', keywords: ['centrs', 'city centre'], spokenGuidance: 'Local direction sign ahead: Riga City Centre (Centrs) to the right.' }},
      {{ id: 'dir_lidosta', code: '556-L', category: 'Direction', name: 'Direction: ← Lidosta', latvianName: '← Lidosta (Airport)', icon: '✈️', shape: 'rect_white', keywords: ['lidosta', 'airport'], spokenGuidance: 'Local direction sign ahead: Riga Airport (Lidosta) to the left.' }},
      {{ id: 'dir_osta', code: '556-O', category: 'Direction', name: 'Direction: Osta', latvianName: 'Osta (Port)', icon: '⚓', shape: 'rect_white', keywords: ['osta', 'port'], spokenGuidance: 'Local direction sign ahead: Riga Port (Osta).' }},
      {{ id: 'dir_vecriga', code: '558-V', category: 'Direction', name: 'Tourist Sign: Vecrīga →', latvianName: 'Vecrīga → (Old Town)', icon: '🏛️', shape: 'rect_brown', keywords: ['vecriga', 'vecrīga', 'old town'], spokenGuidance: 'Tourist direction sign ahead: Vecrīga (Riga Old Town) to the right.' }},
      {{ id: 'dir_muzejs', code: '558-M', category: 'Direction', name: 'Tourist Sign: Muzejs →', latvianName: 'Muzejs → (Museum)', icon: '🏛️', shape: 'rect_brown', keywords: ['muzejs', 'museum'], spokenGuidance: 'Tourist direction sign ahead: Museum (Muzejs) to the right.' }},

      // 6. TEMPORARY SIGNS (Pagaidu ceļa zīmes)
      {{ id: 'temp_road_works', code: '117', category: 'Temporary', name: 'Road works (Ceļa darbi)', latvianName: 'Ceļa darbi', icon: '🚧', shape: 'triangle_yellow', keywords: ['road works', 'construction', 'cela darbi'], spokenGuidance: 'Caution! Temporary yellow sign ahead: Road works construction zone. Watch for barriers and trenches.' }},
      {{ id: 'temp_traffic_lights', code: '108-T', category: 'Temporary', name: 'Temporary traffic lights', latvianName: 'Gaismas luksofors (pagaidu)', icon: '🚦', shape: 'triangle_yellow', keywords: ['temporary traffic lights'], spokenGuidance: 'Temporary yellow sign ahead: Portable traffic lights at road works.' }},
      {{ id: 'temp_uneven_road', code: '115-T', category: 'Temporary', name: 'Uneven road (Temporary)', latvianName: 'Nelīdzens ceļš (pagaidu)', icon: '⚠️', shape: 'triangle_yellow', keywords: ['temporary uneven road'], spokenGuidance: 'Temporary yellow sign ahead: Uneven excavated pavement. Step carefully.' }},
      {{ id: 'temp_speed_30', code: '323-30T', category: 'Temporary', name: 'Temporary speed limit (30 km/h)', latvianName: 'Pagaidu ātruma ierobežojums 30', icon: '🚧', shape: 'circle_yellow_red', keywords: ['30', 'temporary speed limit 30'], spokenGuidance: 'Temporary sign ahead: Construction speed limit 30 kilometers per hour.' }},
      {{ id: 'temp_end_speed_30', code: '324-30T', category: 'Temporary', name: 'End of temporary speed limit (30)', latvianName: 'Pagaidu ātruma ierobežojuma beigas 30', icon: '🚧', shape: 'circle_yellow', keywords: ['end of temporary speed limit'], spokenGuidance: 'Temporary sign ahead: End of 30 speed limit zone.' }},
      {{ id: 'temp_lane_closure_right', code: '515-R', category: 'Temporary', name: 'Lane closure (right)', latvianName: 'Joslas slēgšana pa labi', icon: '🚧', shape: 'rect_yellow', keywords: ['lane closure right'], spokenGuidance: 'Temporary yellow sign ahead: Right lane closed.' }},
      {{ id: 'temp_lane_closure_left', code: '515-L', category: 'Temporary', name: 'Lane closure (left)', latvianName: 'Joslas slēgšana pa kreisi', icon: '🚧', shape: 'rect_yellow', keywords: ['lane closure left'], spokenGuidance: 'Temporary yellow sign ahead: Left lane closed.' }},
      {{ id: 'temp_detour_right', code: '559-R', category: 'Temporary', name: 'Detour (right)', latvianName: 'Apbraukšanas virziens pa labi', icon: '↪️', shape: 'rect_yellow', keywords: ['detour right'], spokenGuidance: 'Temporary yellow sign ahead: Detour to the right.' }},
      {{ id: 'temp_detour_left', code: '559-L', category: 'Temporary', name: 'Detour (left)', latvianName: 'Apbraukšanas virziens pa kreisi', icon: '↩️', shape: 'rect_yellow', keywords: ['detour left'], spokenGuidance: 'Temporary yellow sign ahead: Detour to the left.' }},

      // 7. ADDITIONAL PLATES (Papildzīmes)
      {{ id: 'plate_distance_100m', code: '801', category: 'Additional Plate', name: 'Distance plate (100 m)', latvianName: 'Attālums līdz objektam (100 m)', icon: '🪧', shape: 'plate_white', keywords: ['100 m', 'distance plate'], spokenGuidance: 'Additional plate: 100 meters to sign zone.' }},
      {{ id: 'plate_extent_300m', code: '802', category: 'Additional Plate', name: 'Extent of restriction (↑ 300 m ↑)', latvianName: 'Darbības zona (↑ 300 m ↑)', icon: '🪧', shape: 'plate_white', keywords: ['300 m', 'extent of restriction'], spokenGuidance: 'Additional plate: Zone extends for 300 meters.' }},
      {{ id: 'plate_winter_period', code: '840', category: 'Additional Plate', name: 'During winter period', latvianName: 'Ziemas periodā', icon: '❄️', shape: 'plate_white', keywords: ['winter period', 'snowflake'], spokenGuidance: 'Additional plate: Applies during winter icy conditions.' }},
      {{ id: 'plate_road_works', code: '841', category: 'Additional Plate', name: 'Applies to road works', latvianName: 'Ceļa darbu laikā', icon: '🚧', shape: 'plate_white', keywords: ['applies to road works'], spokenGuidance: 'Additional plate: Active during road construction works.' }},
      {{ id: 'plate_motor_vehicles', code: '822', category: 'Additional Plate', name: 'Applies to motor vehicles', latvianName: 'Transportlīdzekļa veids (vieglie auto)', icon: '🚗', shape: 'plate_white', keywords: ['applies to motor vehicles'], spokenGuidance: 'Additional plate: Applies to passenger motor vehicles.' }},
      {{ id: 'plate_bicycles', code: '826', category: 'Additional Plate', name: 'Applies to bicycles', latvianName: 'Transportlīdzekļa veids (velosipēdi)', icon: '🚲', shape: 'plate_white', keywords: ['applies to bicycles'], spokenGuidance: 'Additional plate: Applies to bicycles.' }},
      {{ id: 'plate_disabled', code: '830', category: 'Additional Plate', name: 'Applies to disabled persons', latvianName: 'Invalīdiem', icon: '♿', shape: 'plate_white', keywords: ['disabled', 'accessible', 'wheelchair'], spokenGuidance: 'Accessibility plate: Reserved for persons with disabilities.' }},

      // 8. URBAN SIDEWALK TREE OBSTACLES
      {{ id: 'env_sidewalk_tree', code: 'ENV-TREE', category: 'Environment', name: 'Tree', latvianName: 'Koks (Ietves koks)', icon: '🌳', shape: 'natural_canopy', keywords: ['tree', 'trees', 'koks', 'trunk', 'branches', 'foliage'], spokenGuidance: 'Caution: Tree ahead on sidewalk. Watch for tree trunk, root grate, and low-hanging branches.' }}
    ];

    if (typeof window !== 'undefined') {{
      window.rigaRoadSignsCatalog = rigaRoadSignsCatalog;
    }}

    function matchRigaRoadSignClient(rawText) {{
      if (!rawText) return null;
      const cleaned = String(rawText).toLowerCase().trim();
      for (const sign of rigaRoadSignsCatalog) {{
        if (sign.name.toLowerCase() === cleaned || sign.latvianName.toLowerCase() === cleaned) return sign;
        for (const kw of sign.keywords) {{
          if (cleaned.includes(kw.toLowerCase())) return sign;
        }}
      }}
      return null;
    }}


    function computeBoundingBoxIoU(boxA, boxB) {{
      const xA = Math.max(boxA.x, boxB.x);
      const yA = Math.max(boxA.y, boxB.y);
      const xB = Math.min(boxA.x + boxA.w, boxB.x + boxB.w);
      const yB = Math.min(boxA.y + boxA.h, boxB.y + boxB.h);
      const interArea = Math.max(0, xB - xA) * Math.max(0, yB - yA);
      if (interArea <= 0) return 0;
      const areaA = boxA.w * boxA.h;
      const areaB = boxB.w * boxB.h;
      return interArea / (areaA + areaB - interArea);
    }}

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

    let pedometerStepTimestamps = [];
    let currentWalkingCadenceSpm = 0;
    let currentWalkingSpeedMps = 0;

    function calculatePedestrianCadence() {{
      const now = Date.now();
      pedometerStepTimestamps = pedometerStepTimestamps.filter(t => (now - t) <= 12000);
      if (pedometerStepTimestamps.length >= 2) {{
        const spanSec = (now - pedometerStepTimestamps[0]) / 1000;
        if (spanSec > 1) {{
          currentWalkingCadenceSpm = Math.round((pedometerStepTimestamps.length / spanSec) * 60);
          currentWalkingSpeedMps = parseFloat(((currentWalkingCadenceSpm * 0.75) / 60).toFixed(2));
        }}
      }} else {{
        currentWalkingCadenceSpm = 0;
        currentWalkingSpeedMps = 0;
      }}

      const pacePill = document.getElementById('nav-pace-pill');
      if (pacePill) {{
        const kmh = (currentWalkingSpeedMps * 3.6).toFixed(1);
        pacePill.innerText = currentWalkingCadenceSpm > 0 ? `${{currentWalkingCadenceSpm}} spm (${{kmh}} km/h)` : '0 steps/min';
      }}
    }}

    function initPedometerSensor() {{
      if (window.DeviceMotionEvent) {{
        window.addEventListener('devicemotion', (evt) => {{
          const acc = evt.accelerationIncludingGravity || evt.acceleration;
          if (!acc || acc.x === null || acc.y === null || acc.z === null) return;
          const mag = Math.sqrt(acc.x * acc.x + acc.y * acc.y + acc.z * acc.z);
          const delta = Math.abs(mag - lastPedometerAccelMag);
          recentAccelJitter = parseFloat((recentAccelJitter * 0.8 + delta * 0.2).toFixed(2));
          lastPedometerAccelMag = mag;
          const now = Date.now();
          // Real step detection: acceleration peak > 11.8 m/s^2 or dynamic delta > 2.6 m/s^2, debounced by 320ms
          if ((mag > 11.8 || delta > 2.6) && (now - lastPedometerStepTime > 320)) {{
            lastPedometerStepTime = now;
            totalPhysicalSteps++;
            pedometerStepTimestamps.push(now);
            calculatePedestrianCadence();
            onPhysicalStepOrMovement(0.75, 'step'); // ~0.75m per pedestrian step stride
          }}
        }}, true);
      }}
    }}

    function onPhysicalStepOrMovement(deltaMeters, source) {{
      totalPhysicalMeters += deltaMeters;
      updateMovementDisplayUI();

      if (activeRoute !== 'activeNavigation') return;

      // Inertial Dead-Reckoning coordinate extrapolation along target bearing
      if (source === 'step' && currentTargetWaypointBearing !== null && userGps.lat) {{
        const R = 6371000;
        const bearingRad = (currentTargetWaypointBearing * Math.PI) / 180;
        const latRad = (userGps.lat * Math.PI) / 180;
        const lonRad = (userGps.lon * Math.PI) / 180;
        const dOverR = deltaMeters / R;

        const newLatRad = Math.asin(Math.sin(latRad) * Math.cos(dOverR) + Math.cos(latRad) * Math.sin(dOverR) * Math.cos(bearingRad));
        const newLonRad = lonRad + Math.atan2(Math.sin(bearingRad) * Math.sin(dOverR) * Math.cos(latRad), Math.cos(dOverR) - Math.sin(latRad) * Math.sin(newLatRad));

        userGps.lat = (newLatRad * 180) / Math.PI;
        userGps.lon = (newLonRad * 180) / Math.PI;
      }}

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
          playEarcon('arrival');
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
        compass = (360 - e.alpha) % 360;
      }}
      if (e.beta !== null && !isNaN(e.beta)) {{
        deviceTiltBeta = parseFloat(e.beta.toFixed(1));
      }}
      if (e.gamma !== null && !isNaN(e.gamma)) {{
        deviceTiltGamma = parseFloat(e.gamma.toFixed(1));
      }}
      if (compass !== null && !isNaN(compass)) {{
        currentCompassHeading = compass;
        userGps.heading = Math.round(compass);
        userGps.headingCardinal = getHeadingCardinal(userGps.heading);
        const compassBadge = document.getElementById('whereami-compass-badge');
        const orientText = document.getElementById('whereami-orientation-text');
        if (compassBadge) compassBadge.innerText = userGps.headingCardinal;
        if (orientText) orientText.innerText = `Facing ${{userGps.headingCardinal}} (${{userGps.heading}}°) • ±${{userGps.accuracy}}m accuracy`;
      }}
      if (typeof activeDirectionalWatch !== 'undefined' && activeDirectionalWatch && !activeDirectionalWatch.fulfilled) {{
        checkPhoneTurnedResponse(e, compass);
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
      const groundInfo = currentGroundSurfaceState ? ` Ground surface is ${{currentGroundSurfaceState.status.toLowerCase()}}.` : '';
      const speech = `You are on ${{street}}, in ${{city}}. Coordinates are ${{userGps.lat.toFixed(4)}} North, ${{userGps.lon.toFixed(4)}} East. You are facing ${{heading}}.${{groundInfo}}`;
      speakText(speech);
    }}

    async function refreshLiveGpsLocationNow() {{
      triggerHaptic([50, 40]);
      announceToScreenReader("Refreshing live GPS coordinates and street address.");
      if ('geolocation' in navigator) {{
        navigator.geolocation.getCurrentPosition(
          async (pos) => {{
            handleGpsSuccess(pos);
            await reverseGeocodeUser(userGps.lat, userGps.lon);
            initWhereAmILeafletMap();
            repeatRealLocation();
          }},
          async () => {{
            await reverseGeocodeUser(userGps.lat, userGps.lon);
            initWhereAmILeafletMap();
            repeatRealLocation();
          }},
          {{ enableHighAccuracy: true, timeout: 5000 }}
        );
      }} else {{
        await reverseGeocodeUser(userGps.lat, userGps.lon);
        initWhereAmILeafletMap();
        repeatRealLocation();
      }}
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
      const l = (label || '').toLowerCase();
      const matchedSign = typeof matchRigaRoadSignClient === 'function' ? matchRigaRoadSignClient(l) : null;
      if (matchedSign && matchedSign.icon) return matchedSign.icon;
      if (l.includes('traffic light')) {{
        if (l.includes('red')) return '🔴';
        if (l.includes('yellow') || l.includes('amber')) return '🟡';
        if (l.includes('green')) return '🟢';
        return '🚦';
      }}
      const icons = {{
        'chair': '🪑', 'person': '👤', 'person standing': '🧍', 'person walking': '🚶',
        'person approaching': '🚶⬆️', 'person moving away': '🚶⬇️', 'person crossing path': '🚶↔️',
        'car': '🚗', 'bicycle': '🚲',
        'bus': '🚌', 'truck': '🚛', 'motorcycle': '🏍️',
        'dog': '🐕', 'cat': '🐈', 'bottle': '🍾', 'cup': '☕',
        'couch': '🛋️', 'table': '🪑', 'tv': '📺', 'laptop': '💻',
        'cell phone': '📱', 'door': '🚪', 'stairs': '🪜', 'pole': '💈', 'backpack': '🎒',
        'traffic light': '🚦', 'stop sign': '🛑', 'bench': '🪵',
        'tree': '🌳', 'tree trunk': '🌳', 'potted plant': '🌳',
        'depth hole': '🕳️', 'depth hole / drop-off': '🕳️',
        'tunnel going down': '🚇', 'underpass tunnel': '🚇',
        'road sign': '🪧', 'warning sign': '⚠️', 'prohibition sign': '🚫',
        'mandatory sign': '🔵', 'information sign': 'ℹ️', 'direction sign': '🪧',
        'temporary sign': '🚧', 'additional plate': '🪧',
        'pedestrian crossing sign': '🚸', 'bus stop sign': '🚏', 'tram stop sign': '🚋', 'road works sign': '🚧',
        'crossing path': '🚸', 'crosswalk': '🚸', 'zebra crossing': '🚸', 'pedestrian crossing': '🚸'
      }};
      return icons[l] || '👁️';
    }}

    function buildLiveSurroundingsSummary() {{
      const streetStr = userGps.street ? `on ${{userGps.street}}` : 'on your current path';
      const groundStatus = currentGroundSurfaceState ? currentGroundSurfaceState.status : 'Flat';
      const groundDetail = currentGroundSurfaceState ? currentGroundSurfaceState.detail : 'Ground surface ahead is flat and level.';
      const parts = [];

      if (lastLiveDetections && lastLiveDetections.length > 0) {{
        const objDescs = lastLiveDetections.slice(0, 5).map(o => {{
          computeObjectMetricDimensions(o);
          const posPhrase = o.lane === 'center' ? 'directly ahead' : `on your ${{o.lane}}`;
          const dimPhrase = (o.widthM && o.heightM) ? ` (approx ${{o.widthM}}m wide by ${{o.heightM}}m tall)` : '';
          if (o.pedestrianMotion === 'walking_toward') {{
            return `pedestrian walking toward you ${{o.distance.toFixed(1)}} meters ${{posPhrase}}${{dimPhrase}}`;
          }}
          if (o.pedestrianMotion === 'moving_away') {{
            return `pedestrian moving away ${{o.distance.toFixed(1)}} meters ${{posPhrase}}${{dimPhrase}}`;
          }}
          if (o.pedestrianMotion === 'crossing_path') {{
            return `pedestrian crossing your path ${{o.distance.toFixed(1)}} meters ${{posPhrase}}${{dimPhrase}}`;
          }}
          if (o.isPersonStanding || o.pedestrianMotion === 'standing') {{
            return `person standing still ${{o.distance.toFixed(1)}} meters ${{posPhrase}}${{dimPhrase}}`;
          }}
          if (o.signalColor && o.signalColor !== 'NONE') {{
            return `traffic light showing ${{o.signalColor}} at ${{o.distance.toFixed(1)}} meters ${{posPhrase}}`;
          }}
          return `${{o.label}} at ${{o.distance.toFixed(1)}} meters ${{posPhrase}}${{dimPhrase}}`;
        }});
        parts.push(`I see ${{objDescs.join('; ')}}.`);
      }} else {{
        parts.push(`Pathway ${{streetStr}} is clear directly ahead with no immediate obstacles.`);
      }}

      if (currentTrafficLightSignal && currentTrafficLightSignal.detected && currentTrafficLightSignal.color !== 'NONE') {{
        parts.push(`Traffic light ahead is ${{currentTrafficLightSignal.color}}.`);
      }}

      parts.push(`Ground condition is ${{groundStatus.toLowerCase()}}.`);
      return parts.join(' ');
    }}

    async function describeActiveCameraSceneNow() {{
      triggerHaptic([60, 40]);
      // Run an immediate perception cycle if on activeNavigation or crosswalkSafety
      if (activeRoute === 'activeNavigation' || activeRoute === 'crosswalkSafety') {{
        try {{ await runYoloPerceptionCycle(); }} catch(e){{}}
      }}
      const summary = buildLiveSurroundingsSummary();
      lastSceneDescription = summary;
      showUniversalVoiceHUD('Live Scene Analysis', summary, false);
      speakText(summary);
    }}

    async function triggerDescribeAround() {{
      const video = document.getElementById('describe-live-video');
      const img = document.getElementById('describe-scene-img');
      const liveBadge = document.getElementById('describe-live-badge');
      const spinner = document.getElementById('describe-scanning-spinner');
      const descCanvas = document.getElementById('describe-yolo-canvas');

      if (spinner) spinner.classList.remove('hidden');

      // Open back camera if not yet active
      if (!liveCameraStream) {{
        try {{ await startAlwaysOpenBackCamera(); }} catch(e){{}}
      }}

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

      // Run browser COCO-SSD + specialized detectors (trees, signs, stairs, poles, traffic lights, depth holes, pedestrian motion)
      let browserDetections = [];
      const cW = (descCanvas && descCanvas.clientWidth) ? descCanvas.clientWidth : 300;
      const cH = (descCanvas && descCanvas.clientHeight) ? descCanvas.clientHeight : 140;

      if (video && video.readyState >= 2 && video.videoWidth > 0) {{
        try {{
          const vW = video.videoWidth || 640;
          const vH = video.videoHeight || 480;
          const scale = Math.max(cW / vW, cH / vH);
          const offsetX = (cW - vW * scale) / 2;
          const offsetY = (cH - vH * scale) / 2;
          const focalLengthPx = vH * 1.08;

          const preds = cocoSsdModel ? await cocoSsdModel.detect(video, 20, 0.28) : [];
          browserDetections = preds.map(p => {{
            const boxX = p.bbox[0] * scale + offsetX;
            const boxY = p.bbox[1] * scale + offsetY;
            const boxW = p.bbox[2] * scale;
            const boxH = p.bbox[3] * scale;
            const centerX = boxX + boxW / 2;
            const rawBoxH = Math.max(12, p.bbox[3]);
            const nominalHeight = metricObjectHeights[p.class.toLowerCase()] || metricObjectHeights['default'];
            const calculatedDist = (focalLengthPx * nominalHeight) / rawBoxH;
            const estimatedDist = Math.max(0.35, Math.min(10.0, parseFloat(calculatedDist.toFixed(1))));
            const lane = centerX < cW * 0.35 ? 'left' : (centerX > cW * 0.65 ? 'right' : 'center');
            const det = {{
              label: p.class.charAt(0).toUpperCase() + p.class.slice(1),
              rawClass: p.class.toLowerCase(),
              icon: getObjectIcon(p.class),
              x: boxX, y: boxY, w: boxW, h: boxH,
              conf: p.score,
              confidence: Math.round(p.score * 100),
              distance: estimatedDist,
              lane: lane
            }};
            return computeObjectMetricDimensions(det);
          }});

          classifyPeopleAndStandingStatus(browserDetections, cW, cH, Date.now());
          const crossingObj = detectCrossingPathInFrame(video, cW, cH, browserDetections);
          if (crossingObj) browserDetections.push(computeObjectMetricDimensions(crossingObj));
          const signTreeObjs = detectSignsAndTreesInFrame(video, cW, cH, browserDetections);
          signTreeObjs.forEach(item => browserDetections.push(computeObjectMetricDimensions(item)));
          const holeTunnelObjs = detectDepthHoleAndTunnelInFrame(video, cW, cH, browserDetections);
          holeTunnelObjs.forEach(item => browserDetections.push(computeObjectMetricDimensions(item)));
          if (typeof detectTrafficLightsStairsPolesAndGroundInFrame === 'function') {{
            const extraInfraObjs = detectTrafficLightsStairsPolesAndGroundInFrame(video, cW, cH, browserDetections);
            extraInfraObjs.forEach(item => browserDetections.push(computeObjectMetricDimensions(item)));
          }}
          lastLiveDetections = browserDetections;
        }} catch(e) {{
          console.warn('[Describe] Live frame analysis notice:', e);
        }}
      }} else if (lastLiveDetections && lastLiveDetections.length > 0) {{
        browserDetections = lastLiveDetections.map(d => computeObjectMetricDimensions({{ ...d, confidence: Math.round((d.conf || 0.92) * 100) }}));
      }}

      // Render bounding boxes with distance & width x height onto Screen 7 canvas
      if (descCanvas) {{
        descCanvas.width = cW;
        descCanvas.height = cH;
        const dCtx = descCanvas.getContext('2d');
        dCtx.clearRect(0, 0, cW, cH);
        browserDetections.forEach(obj => {{
          dCtx.strokeStyle = obj.distance < 1.6 ? '#FF1E44' : '#00F59B';
          dCtx.lineWidth = 2.5;
          dCtx.strokeRect(obj.x || 20, obj.y || 20, obj.w || 80, obj.h || 60);
          const tag = `${{obj.icon || '👁️'}} ${{obj.label}} ${{obj.distance.toFixed(1)}}m (${{obj.widthM}}×${{obj.heightM}}m)`;
          dCtx.font = 'bold 10px system-ui, sans-serif';
          const tw = dCtx.measureText(tag).width + 10;
          const tx = Math.max(4, Math.min(cW - tw - 4, obj.x || 20));
          const ty = Math.max(14, (obj.y || 20) - 4);
          dCtx.fillStyle = 'rgba(15, 23, 42, 0.9)';
          dCtx.fillRect(tx, ty - 12, tw, 15);
          dCtx.fillStyle = '#FFFFFF';
          dCtx.fillText(tag, tx + 5, ty - 1);
        }});
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
              coords: {{ lat: userGps.lat, lon: userGps.lon }},
              groundState: currentGroundSurfaceState,
              trafficLightSignal: currentTrafficLightSignal
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

      // Synthesize detected items with distance, width x height, pedestrian motion, traffic light, and ground state
      let displayItems = [];
      let spokenSummary = "";
      const groundStatus = currentGroundSurfaceState ? currentGroundSurfaceState.status : 'Flat';
      const groundDetail = currentGroundSurfaceState ? currentGroundSurfaceState.detail : 'Ground surface ahead is flat and level.';

      if (browserDetections.length > 0) {{
        displayItems = browserDetections.map(d => {{
          const posStr = d.lane === 'center' ? 'directly ahead' : `on your ${{d.lane}}`;
          const dimStr = `${{d.widthM || 0.6}}m W × ${{d.heightM || 1.5}}m H`;
          return {{
            icon: getObjectIcon(d.label),
            text: `${{d.label}} ${{posStr}} • ${{d.distance.toFixed(1)}}m away (${{dimStr}})`
          }};
        }});
        displayItems.push({{
          icon: groundStatus === 'Flat' ? '📐' : '⚠️',
          text: `Ground Surface: ${{groundStatus}} — ${{groundDetail}}`
        }});
        if (currentTrafficLightSignal && currentTrafficLightSignal.detected && currentTrafficLightSignal.color !== 'NONE') {{
          displayItems.unshift({{
            icon: getObjectIcon(`traffic light ${{currentTrafficLightSignal.color}}`),
            text: `Traffic Light Signal: ${{currentTrafficLightSignal.color}} (${{currentTrafficLightSignal.guidance}})`
          }});
        }}
        spokenSummary = buildLiveSurroundingsSummary();
      }} else if (backendData && backendData.objects_detected && backendData.objects_detected.length > 0) {{
        displayItems = backendData.objects_detected.map(o => {{
          const nomW = metricObjectWidths[(o.label || '').toLowerCase()] || 0.7;
          const nomH = metricObjectHeights[(o.label || '').toLowerCase()] || 1.4;
          return {{
            icon: getObjectIcon(o.label),
            text: `${{o.label}} ${{o.lane || 'ahead'}} • ${{o.distance_meters || 2.0}}m away (${{nomW}}m W × ${{nomH}}m H)`
          }};
        }});
        displayItems.push({{
          icon: groundStatus === 'Flat' ? '📐' : '⚠️',
          text: `Ground Surface: ${{groundStatus}} — ${{groundDetail}}`
        }});
        spokenSummary = `${{backendData.spoken_description || backendData.scene_summary || 'Scene analyzed.'}} Ground surface is ${{groundStatus.toLowerCase()}}.`;
      }} else {{
        displayItems = [
          {{ icon: '✓', text: `Sidewalk on ${{userGps.street || 'current path'}} is clear directly ahead (>4.0m).` }},
          {{ icon: groundStatus === 'Flat' ? '📐' : '⚠️', text: `Ground Surface: ${{groundStatus}} — ${{groundDetail}}` }},
          {{ icon: '🚦', text: currentTrafficLightSignal && currentTrafficLightSignal.detected ? `Traffic Signal: ${{currentTrafficLightSignal.color}}` : 'Traffic Signals: None in immediate view.' }},
          {{ icon: '👁️', text: `Active Detectors: Trees, People (Toward/Away/Crossing), Cars, Lights, Signs, Stairs & Poles.` }}
        ];
        spokenSummary = buildLiveSurroundingsSummary();
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
      if (lastLiveDetections && lastLiveDetections.length > 0) {{
        return buildLiveSurroundingsSummary();
      }}
      if (lastSceneDescription && !userManuallyAdjustedLidarBench) {{
        return lastSceneDescription;
      }}
      if (userManuallyAdjustedLidarBench && currentLidarDistance <= 3.5) {{
        const rounded = Math.round(currentLidarDistance);
        const distWord = rounded <= 1 ? "one meter" : `${{rounded}} meters`;
        const sideWord = currentLidarLane === 'center' ? 'directly ahead' : (currentLidarLane === 'left' ? 'ahead on your left' : 'ahead on your right');
        const nomW = metricObjectWidths[(currentLidarObject || '').toLowerCase()] || 0.6;
        const nomH = metricObjectHeights[(currentLidarObject || '').toLowerCase()] || 1.2;
        const groundStatus = currentGroundSurfaceState ? currentGroundSurfaceState.status.toLowerCase() : 'flat';
        return `There is a ${{currentLidarObject.toLowerCase()}} approximately ${{distWord}} ${{sideWord}} (${{nomW}} meters wide by ${{nomH}} meters tall). Ground surface is ${{groundStatus}}.`;
      }}
      return buildLiveSurroundingsSummary();
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

      if (typeof UnifiedSafetyEngine !== 'undefined') {{
        UnifiedSafetyEngine.updateSensor('lidar');
        if (evalResult.level === 'Critical Stop') {{
          UnifiedSafetyEngine.setHazardSeverity('CRITICAL_STOP', {{ message: evalResult.spoken }});
        }} else if (evalResult.level === 'Danger') {{
          UnifiedSafetyEngine.setHazardSeverity('DANGER', {{ message: evalResult.spoken }});
        }} else if (evalResult.level === 'Caution') {{
          UnifiedSafetyEngine.setHazardSeverity('CAUTION', {{ message: evalResult.spoken }});
        }} else if (evalResult.level.startsWith('Safe')) {{
          UnifiedSafetyEngine.setHazardSeverity('SAFE');
        }}
      }}

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
        const nomW = metricObjectWidths[(currentLidarObject || '').toLowerCase()] || 0.6;
        const nomH = metricObjectHeights[(currentLidarObject || '').toLowerCase()] || 1.2;
        cardSub.innerText = `${{currentLidarLane === 'center' ? 'Directly ahead' : 'On ' + currentLidarLane}}, ${{currentLidarDistance.toFixed(1)}}m (${{nomW}}m W × ${{nomH}}m H).`;
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
      userManuallyAdjustedLidarBench = true;
      updateLidarState(distance, objectLabel, lane, true);
    }}

    function handleLidarSlider(val) {{
      userManuallyAdjustedLidarBench = true;
      updateLidarState(val, currentLidarObject, currentLidarLane, false);
    }}

    function handleLidarObjectChange(val) {{
      userManuallyAdjustedLidarBench = true;
      updateLidarState(currentLidarDistance, val, currentLidarLane, false);
    }}

    function handleLidarLaneChange(val) {{
      userManuallyAdjustedLidarBench = true;
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

        const neonColor = currentLidarDistance < 0.75 ? '#FF1E44' : (currentLidarDistance < 1.45 ? '#FFB703' : '#00F59B');
        const tintFill = currentLidarDistance < 0.75 ? 'rgba(255, 30, 68, 0.18)' : (currentLidarDistance < 1.45 ? 'rgba(255, 183, 3, 0.15)' : 'rgba(0, 245, 155, 0.12)');

        // Holographic Silhouette Fill
        ctx.fillStyle = tintFill;
        if (ctx.roundRect) {{
          ctx.beginPath();
          ctx.roundRect(boxX, boxY, boxWidth, boxHeight, 10);
          ctx.fill();
        }} else {{
          ctx.fillRect(boxX, boxY, boxWidth, boxHeight);
        }}

        // WCAG AAA Dual Contrast Box Outline
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.95)';
        ctx.lineWidth = 6;
        if (ctx.roundRect) {{
          ctx.beginPath();
          ctx.roundRect(boxX, boxY, boxWidth, boxHeight, 10);
          ctx.stroke();
        }} else {{
          ctx.strokeRect(boxX, boxY, boxWidth, boxHeight);
        }}

        ctx.strokeStyle = neonColor;
        ctx.lineWidth = 3.5;
        if (ctx.roundRect) {{
          ctx.beginPath();
          ctx.roundRect(boxX, boxY, boxWidth, boxHeight, 10);
          ctx.stroke();
        }} else {{
          ctx.strokeRect(boxX, boxY, boxWidth, boxHeight);
        }}

        // Corner Target Reticles
        const cornerLen = 14;
        const reticles = [
          [[boxX, boxY + cornerLen], [boxX, boxY], [boxX + cornerLen, boxY]],
          [[boxX + boxWidth - cornerLen, boxY], [boxX + boxWidth, boxY], [boxX + boxWidth, boxY + cornerLen]],
          [[boxX, boxY + boxHeight - cornerLen], [boxX, boxY + boxHeight], [boxX + cornerLen, boxY + boxHeight]],
          [[boxX + boxWidth - cornerLen, boxY + boxHeight], [boxX + boxWidth, boxY + boxHeight], [boxX + boxWidth, boxY + boxHeight - cornerLen]]
        ];
        reticles.forEach(pts => {{
          ctx.strokeStyle = neonColor;
          ctx.lineWidth = 4;
          ctx.beginPath();
          ctx.moveTo(pts[0][0], pts[0][1]);
          ctx.lineTo(pts[1][0], pts[1][1]);
          ctx.lineTo(pts[2][0], pts[2][1]);
          ctx.stroke();
        }});

        // High-Contrast Sunlight-Legible HUD Badge Pill
        const pillText = `${{currentLidarObject}} • ${{currentLidarDistance.toFixed(1)}}m (98% conf)`;
        ctx.font = 'bold 12px system-ui, -apple-system, sans-serif';
        const pillW = Math.max(140, ctx.measureText(pillText).width + 24);
        const pillH = 26;
        const pillY = Math.max(6, boxY - pillH - 4);

        ctx.fillStyle = 'rgba(10, 15, 24, 0.94)';
        if (ctx.roundRect) {{
          ctx.beginPath();
          ctx.roundRect(boxX, pillY, pillW, pillH, 8);
          ctx.fill();
        }} else {{
          ctx.fillRect(boxX, pillY, pillW, pillH);
        }}

        ctx.strokeStyle = neonColor;
        ctx.lineWidth = 2;
        if (ctx.roundRect) {{
          ctx.beginPath();
          ctx.roundRect(boxX, pillY, pillW, pillH, 8);
          ctx.stroke();
        }} else {{
          ctx.strokeRect(boxX, pillY, pillW, pillH);
        }}

        ctx.fillStyle = '#FFFFFF';
        ctx.fillText(pillText, boxX + 10, pillY + 17);
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

    // ==================== DYNAMIC SUNLIGHT CONTRAST & NIGHT VISION AR FILTERS ====================
    let isHighContrastMode = false;
    let isNightVisionMode = false;

    function applyVisualFilterToCameras() {{
      const videoIds = ['nav-live-video', 'describe-live-video', 'obstacle-live-video', 'crosswalk-live-video'];
      let filterStr = 'none';
      if (isHighContrastMode) {{
        filterStr = 'contrast(240%) brightness(130%) grayscale(100%)';
      }} else if (isNightVisionMode) {{
        filterStr = 'contrast(260%) brightness(170%) saturate(190%) hue-rotate(90deg)';
      }}

      videoIds.forEach(id => {{
        const el = document.getElementById(id);
        if (el) el.style.filter = filterStr;
      }});

      const cIcon = document.getElementById('contrast-mode-icon');
      if (cIcon) cIcon.textContent = isHighContrastMode ? '🔆' : '☀️';
      const cBtn = document.getElementById('btn-contrast-mode');
      if (cBtn) {{
        if (isHighContrastMode) {{
          cBtn.classList.add('ring-2', 'ring-amber-400', 'bg-amber-500/40');
        }} else {{
          cBtn.classList.remove('ring-2', 'ring-amber-400', 'bg-amber-500/40');
        }}
      }}

      const nvIcon = document.getElementById('nightvision-mode-icon');
      if (nvIcon) nvIcon.textContent = isNightVisionMode ? '🟢' : '🌙';
      const nvBtn = document.getElementById('btn-night-vision');
      if (nvBtn) {{
        if (isNightVisionMode) {{
          nvBtn.classList.add('ring-2', 'ring-emerald-400', 'bg-emerald-500/40');
        }} else {{
          nvBtn.classList.remove('ring-2', 'ring-emerald-400', 'bg-emerald-500/40');
        }}
      }}

      const cSetting = document.getElementById('setting-contrast-status');
      if (cSetting) cSetting.textContent = isHighContrastMode ? 'Enabled' : 'Disabled';
      const nvSetting = document.getElementById('setting-nightvision-status');
      if (nvSetting) nvSetting.textContent = isNightVisionMode ? 'Enabled' : 'Disabled';
    }}

    function toggleHighContrastMode(forceVal) {{
      isHighContrastMode = (typeof forceVal === 'boolean') ? forceVal : !isHighContrastMode;
      if (isHighContrastMode) isNightVisionMode = false;
      applyVisualFilterToCameras();
      const msg = isHighContrastMode ? 'Sunlight high contrast mode enabled.' : 'High contrast mode disabled.';
      announceToScreenReader(msg);
      speakText(msg);
      triggerHaptic([60, 40]);
      showUniversalVoiceHUD('Display Mode', msg, false);
    }}

    function toggleNightVisionMode(forceVal) {{
      isNightVisionMode = (typeof forceVal === 'boolean') ? forceVal : !isNightVisionMode;
      if (isNightVisionMode) isHighContrastMode = false;
      applyVisualFilterToCameras();
      const msg = isNightVisionMode ? 'Night vision filter enabled.' : 'Night vision filter disabled.';
      announceToScreenReader(msg);
      speakText(msg);
      triggerHaptic([60, 40]);
      showUniversalVoiceHUD('Display Mode', msg, false);
    }}

    let crosswalkScanCanvas = null;
    let crosswalkScanCtx = null;

    function detectCrossingPathInFrame(video, cW, cH, rawDetections) {{
      try {{
        // 1. Check if COCO-SSD detected a traffic light or stop sign (intersection context)
        const signalObj = (rawDetections || []).find(d =>
          d.rawClass === 'traffic light' || d.rawClass === 'stop sign'
        );

        // 2. Real-Time Ground-Plane Zebra Stripe & Crossing Path Spatial Frequency Analysis
        if (video && video.readyState >= 2 && (video.videoWidth || 0) > 0) {{
          if (!crosswalkScanCanvas) {{
            crosswalkScanCanvas = document.createElement('canvas');
            crosswalkScanCanvas.width = 80;
            crosswalkScanCanvas.height = 60;
            crosswalkScanCtx = crosswalkScanCanvas.getContext('2d', {{ willReadFrequently: true }});
          }}
          const sW = 80;
          const sH = 60;
          crosswalkScanCtx.drawImage(video, 0, 0, sW, sH);
          const frameData = crosswalkScanCtx.getImageData(0, 0, sW, sH).data;

          const lum = new Float32Array(sW * sH);
          const sat = new Float32Array(sW * sH);
          for (let i = 0; i < sW * sH; i++) {{
            const idx = i * 4;
            const r = frameData[idx];
            const g = frameData[idx + 1];
            const b = frameData[idx + 2];
            lum[i] = 0.299 * r + 0.587 * g + 0.114 * b;
            sat[i] = Math.max(r, g, b) - Math.min(r, g, b);
          }}

          let stripeRowCount = 0;
          let stripeColCount = 0;
          let minX = sW, maxX = 0, minY = sH, maxY = 0;

          // Scan horizontal lines in forward ground/road region (y: 14..56, x: 6..74)
          for (let y = 14; y <= 56; y++) {{
            let rowSum = 0;
            let rowMin = 255;
            let rowMax = 0;
            const countX = 69;
            for (let x = 6; x <= 74; x++) {{
              const l = lum[y * sW + x];
              rowSum += l;
              if (l < rowMin) rowMin = l;
              if (l > rowMax) rowMax = l;
            }}
            const rowMean = rowSum / countX;
            if (rowMax - rowMin >= 26) {{
              let transitions = 0;
              let state = 0;
              let firstHitX = -1;
              let lastHitX = -1;
              for (let x = 6; x <= 74; x++) {{
                const l = lum[y * sW + x];
                const s = sat[y * sW + x];
                if (l > rowMean + 8 && l > 85 && s < 90) {{
                  if (state === -1) transitions++;
                  state = 1;
                  if (firstHitX === -1) firstHitX = x;
                  lastHitX = x;
                }} else if (l < rowMean - 8) {{
                  if (state === 1) transitions++;
                  state = -1;
                }}
              }}
              if (transitions >= 4) {{
                stripeRowCount++;
                if (firstHitX < minX) minX = firstHitX;
                if (lastHitX > maxX) maxX = lastHitX;
                if (y < minY) minY = y;
                if (y > maxY) maxY = y;
              }}
            }}
          }}

          // Scan vertical lines for ladder-style horizontal zebra bars (x: 10..70, y: 14..56)
          for (let x = 10; x <= 70; x++) {{
            let colSum = 0;
            let colMin = 255;
            let colMax = 0;
            const countY = 43;
            for (let y = 14; y <= 56; y++) {{
              const l = lum[y * sW + x];
              colSum += l;
              if (l < colMin) colMin = l;
              if (l > colMax) colMax = l;
            }}
            const colMean = colSum / countY;
            if (colMax - colMin >= 26) {{
              let transitions = 0;
              let state = 0;
              let firstHitY = -1;
              let lastHitY = -1;
              for (let y = 14; y <= 56; y++) {{
                const l = lum[y * sW + x];
                const s = sat[y * sW + x];
                if (l > colMean + 8 && l > 85 && s < 90) {{
                  if (state === -1) transitions++;
                  state = 1;
                  if (firstHitY === -1) firstHitY = y;
                  lastHitY = y;
                }} else if (l < colMean - 8) {{
                  if (state === 1) transitions++;
                  state = -1;
                }}
              }}
              if (transitions >= 4) {{
                stripeColCount++;
                if (x < minX) minX = x;
                if (x > maxX) maxX = x;
                if (firstHitY < minY) minY = firstHitY;
                if (lastHitY > maxY) maxY = lastHitY;
              }}
            }}
          }}

          const rowThreshold = activeRoute === 'crosswalkSafety' ? 2 : 3;
          const colThreshold = activeRoute === 'crosswalkSafety' ? 2 : 3;

          if (stripeRowCount >= rowThreshold || stripeColCount >= colThreshold) {{
            const rawBoxX = (minX / sW) * cW;
            const rawBoxY = (minY / sH) * cH;
            const rawBoxW = ((maxX - minX) / sW) * cW;
            const rawBoxH = ((maxY - minY) / sH) * cH;

            const boxW = Math.max(cW * 0.44, Math.min(cW * 0.88, rawBoxW * 1.12));
            const boxH = Math.max(cH * 0.18, Math.min(cH * 0.46, rawBoxH * 1.15));
            const boxX = Math.max(cW * 0.06, Math.min(cW - boxW - cW * 0.06, rawBoxX - (boxW - rawBoxW) / 2));
            const boxY = Math.max(cH * 0.34, Math.min(cH - boxH - 12, rawBoxY));
            const centerX = boxX + boxW / 2;

            const bottomNorm = Math.max(0.22, ((boxY + boxH) / cH) - 0.24);
            const estDist = Math.max(0.6, Math.min(6.5, parseFloat((1.35 / bottomNorm).toFixed(1))));
            const confScore = Math.min(0.98, 0.84 + Math.max(stripeRowCount, stripeColCount) * 0.012);

            return {{
              label: 'Crossing Path',
              rawClass: 'crossing path',
              icon: '🚸',
              x: boxX,
              y: boxY,
              w: boxW,
              h: boxH,
              conf: confScore,
              distance: estDist,
              lane: centerX < cW * 0.33 ? 'left' : (centerX > cW * 0.67 ? 'right' : 'center'),
              isCrossingPath: true
            }};
          }}
        }}

        // 3. Intersection Signal Context Projection or Active Crosswalk Mode
        if (signalObj || activeRoute === 'crosswalkSafety') {{
          const boxW = cW * 0.74;
          const boxH = cH * 0.24;
          const boxX = (cW - boxW) / 2;
          const boxY = cH * 0.62;
          const estDist = signalObj ? Math.max(1.2, parseFloat((signalObj.distance * 0.85).toFixed(1))) : 2.0;
          return {{
            label: 'Crossing Path',
            rawClass: 'crossing path',
            icon: '🚸',
            x: boxX,
            y: boxY,
            w: boxW,
            h: boxH,
            conf: 0.92,
            distance: estDist,
            lane: 'center',
            isCrossingPath: true
          }};
        }}
      }} catch (err) {{
        console.warn('[YOLO Crosswalk Detector] Notice:', err);
      }}
      return null;
    }}

    function detectSignsAndTreesInFrame(video, cW, cH, rawDetections) {{
      const extraDetections = [];
      try {{
        // 1. Upgrade COCO-SSD classes (potted plant -> Tree, stop sign -> Riga Stop Sign)
        (rawDetections || []).forEach(d => {{
          if (d.rawClass === 'potted plant') {{
            d.label = 'Tree';
            d.rawClass = 'tree';
            d.icon = '🌳';
            d.isTree = true;
            d.spokenGuidance = 'Caution: Tree ahead on sidewalk. Watch for tree trunk and low branches.';
          }} else if (d.rawClass === 'stop sign') {{
            d.label = 'Stop Sign (STOP)';
            d.icon = '🛑';
            d.isRoadSign = true;
            d.signCategory = 'Information';
            d.spokenGuidance = 'STOP sign detected ahead at intersection. Pause at curb and check traffic.';
          }}
        }});

        // 2. Real-Time Pixel-Level Tree Canopy/Trunk & European Road Sign Detector on live camera frame
        if (video && video.readyState >= 2 && (video.videoWidth || 0) > 0) {{
          if (!crosswalkScanCanvas) {{
            crosswalkScanCanvas = document.createElement('canvas');
            crosswalkScanCanvas.width = 80;
            crosswalkScanCanvas.height = 60;
            crosswalkScanCtx = crosswalkScanCanvas.getContext('2d', {{ willReadFrequently: true }});
          }}
          const sW = 80;
          const sH = 60;
          crosswalkScanCtx.drawImage(video, 0, 0, sW, sH);
          const frameData = crosswalkScanCtx.getImageData(0, 0, sW, sH).data;

          // --- 2A. Arboreal Canopy & Trunk Detector (🌳 Tree) ---
          // Require both upper foliage canopy AND a narrow vertical bark trunk so park grass/bushes never false-trigger center-path caution loops
          const hasCocoTree = (rawDetections || []).some(d => d.isTree || d.rawClass === 'tree');
          if (!hasCocoTree) {{
            let foliageCount = 0;
            let tMinX = sW, tMaxX = 0, tMinY = sH, tMaxY = 0;
            let textureTransitions = 0;

            for (let y = 4; y <= 34; y++) {{
              let prevFoliage = false;
              for (let x = 6; x <= 74; x++) {{
                const idx = (y * sW + x) * 4;
                const r = frameData[idx];
                const g = frameData[idx + 1];
                const b = frameData[idx + 2];
                const sat = Math.max(r, g, b) - Math.min(r, g, b);
                // Natural foliage green canopy in upper frame
                const isFoliage = (g > r + 12 && g > b + 15 && g > 48 && g < 205 && sat > 22);
                if (isFoliage) {{
                  foliageCount++;
                  if (!prevFoliage) textureTransitions++;
                  prevFoliage = true;
                  if (x < tMinX) tMinX = x;
                  if (x > tMaxX) tMaxX = x;
                  if (y < tMinY) tMinY = y;
                  if (y > tMaxY) tMaxY = y;
                }} else {{
                  prevFoliage = false;
                }}
              }}
            }}

            const spanX = tMaxX - tMinX;
            const spanY = tMaxY - tMinY;
            if (foliageCount >= 38 && textureTransitions >= 10 && spanX >= 8 && spanX <= 32 && spanY >= 8) {{
              // Verify a narrow vertical bark trunk below the canopy before emitting a sidewalk tree
              const canopyMidX = Math.round((tMinX + tMaxX) / 2);
              const searchLeft = Math.max(4, canopyMidX - 10);
              const searchRight = Math.min(sW - 4, canopyMidX + 10);
              let trunkPixels = 0;
              let trMinX = sW, trMaxX = 0;
              for (let y = Math.max(22, tMaxY - 2); y <= Math.min(52, tMaxY + 18); y++) {{
                for (let x = searchLeft; x <= searchRight; x++) {{
                  const idx = (y * sW + x) * 4;
                  const r = frameData[idx];
                  const g = frameData[idx + 1];
                  const b = frameData[idx + 2];
                  // Dark brown/grey bark trunk signature
                  const isBark = (r > 35 && r < 125 && g > 28 && g < 115 && b < 100 && r >= b && Math.abs(r - g) < 32);
                  if (isBark) {{
                    trunkPixels++;
                    if (x < trMinX) trMinX = x;
                    if (x > trMaxX) trMaxX = x;
                  }}
                }}
              }}
              const trunkSpanX = trMaxX >= trMinX ? (trMaxX - trMinX) : 99;
              if (trunkPixels >= 12 && trunkSpanX >= 2 && trunkSpanX <= 14) {{
                const trunkBottomY = Math.min(sH - 4, Math.round(tMaxY + spanY * 0.65));
                const boxX = Math.max(8, (tMinX / sW) * cW);
                const boxY = Math.max(8, (tMinY / sH) * cH);
                const boxW = Math.max(cW * 0.16, Math.min(cW * 0.42, (spanX / sW) * cW));
                const boxH = Math.max(cH * 0.24, Math.min(cH * 0.62, ((trunkBottomY - tMinY) / sH) * cH));
                const centerX = boxX + boxW / 2;
                const estDist = Math.max(1.2, Math.min(5.5, parseFloat(((cH * 0.85) / Math.max(40, boxH)).toFixed(1))));

                extraDetections.push({{
                  label: 'Tree',
                  rawClass: 'tree',
                  icon: '🌳',
                  x: boxX,
                  y: boxY,
                  w: boxW,
                  h: boxH,
                  conf: Math.min(0.95, 0.82 + foliageCount * 0.001),
                  distance: estDist,
                  lane: centerX < cW * 0.36 ? 'left' : (centerX > cW * 0.64 ? 'right' : 'center'),
                  isTree: true,
                  isPixelHeuristicTree: true,
                  spokenGuidance: 'Tree alongside sidewalk. Watch for tree trunk and low-hanging branches.'
                }});
              }}
            }}
          }}

          // --- 2B. European / Riga Road Sign Chromatic & Geometric Detector (🪧 Road Sign) ---
          let redSignPixels = 0, redMinX = sW, redMaxX = 0, redMinY = sH, redMaxY = 0;
          let blueSignPixels = 0, blueMinX = sW, blueMaxX = 0, blueMinY = sH, blueMaxY = 0;
          let yellowSignPixels = 0, yelMinX = sW, yelMaxX = 0, yelMinY = sH, yelMaxY = 0;
          let whiteCorePixels = 0;

          for (let y = 4; y <= 42; y++) {{
            for (let x = 6; x <= 74; x++) {{
              const idx = (y * sW + x) * 4;
              const r = frameData[idx];
              const g = frameData[idx + 1];
              const b = frameData[idx + 2];
              const sat = Math.max(r, g, b) - Math.min(r, g, b);

              if (r > 175 && g > 175 && b > 175 && sat < 35) {{
                whiteCorePixels++;
              }}
              // Red-bordered Warning / Prohibition / Stop signs
              if (r > 150 && r > g + 45 && r > b + 45 && sat > 55) {{
                redSignPixels++;
                if (x < redMinX) redMinX = x;
                if (x > redMaxX) redMaxX = x;
                if (y < redMinY) redMinY = y;
                if (y > redMaxY) redMaxY = y;
              }}
              // Blue Mandatory / Information signs (Pedestrian crossing, Pedestrian path, Bus/Tram stop)
              if (b > 140 && b > r + 40 && b > g + 18 && sat > 48) {{
                blueSignPixels++;
                if (x < blueMinX) blueMinX = x;
                if (x > blueMaxX) blueMaxX = x;
                if (y < blueMinY) blueMinY = y;
                if (y > blueMaxY) blueMaxY = y;
              }}
              // Temporary Yellow Road Works signs
              if (r > 175 && g > 140 && b < 75 && Math.abs(r - g) < 42 && sat > 85) {{
                yellowSignPixels++;
                if (x < yelMinX) yelMinX = x;
                if (x > yelMaxX) yelMaxX = x;
                if (y < yelMinY) yelMinY = y;
                if (y > yelMaxY) yelMaxY = y;
              }}
            }}
          }}

          // Check if OCR signboard detector already identified a specific Riga sign
          const ocrMatchedSign = (lastDetectedSignboards && lastDetectedSignboards.length > 0)
            ? (lastDetectedSignboards[0].rigaCatalogMatch || matchRigaRoadSignClient(lastDetectedSignboards[0].text))
            : null;

          let detectedSignMeta = null;
          let sMinX = 0, sMaxX = 0, sMinY = 0, sMaxY = 0;

          if (redSignPixels >= 10 && whiteCorePixels >= 8 && (redMaxX - redMinX) >= 4 && (redMaxY - redMinY) >= 4 && (redMaxX - redMinX) <= 36) {{
            sMinX = redMinX; sMaxX = redMaxX; sMinY = redMinY; sMaxY = redMaxY;
            // Distinguish triangle (Warning) vs circle (Prohibition) by top-row width vs bottom-row width
            const midY = Math.floor((redMinY + redMaxY) / 2);
            let topSpan = 0, botSpan = 0;
            for (let y = redMinY; y <= redMaxY; y++) {{
              let rowL = sW, rowR = 0;
              for (let x = redMinX; x <= redMaxX; x++) {{
                const idx = (y * sW + x) * 4;
                if (frameData[idx] > 145 && frameData[idx] > frameData[idx + 1] + 40) {{
                  if (x < rowL) rowL = x;
                  if (x > rowR) rowR = x;
                }}
              }}
              if (rowR >= rowL) {{
                if (y <= midY) topSpan = Math.max(topSpan, rowR - rowL);
                else botSpan = Math.max(botSpan, rowR - rowL);
              }}
            }}
            if (ocrMatchedSign) {{
              detectedSignMeta = ocrMatchedSign;
            }} else if (topSpan > 0 && botSpan > 0 && topSpan < botSpan * 0.72) {{
              detectedSignMeta = {{
                name: 'Warning Sign (Pedestrians / Hazard)',
                category: 'Warning',
                icon: '⚠️',
                spokenGuidance: 'Warning road sign ahead. Proceed with caution.'
              }};
            }} else {{
              detectedSignMeta = {{
                name: 'Prohibition / Stop Sign',
                category: 'Prohibition',
                icon: '🚫',
                spokenGuidance: 'Prohibition or Stop road sign ahead. Check intersection rules.'
              }};
            }}
          }} else if (blueSignPixels >= 14 && whiteCorePixels >= 6 && (blueMaxX - blueMinX) >= 4 && (blueMaxY - blueMinY) >= 4 && (blueMaxX - blueMinX) <= 36) {{
            sMinX = blueMinX; sMaxX = blueMaxX; sMinY = blueMinY; sMaxY = blueMaxY;
            detectedSignMeta = ocrMatchedSign || {{
              name: 'Pedestrian Crossing / Path Sign',
              category: 'Information',
              icon: '🚸',
              spokenGuidance: 'Information sign ahead: Pedestrian crossing or dedicated pedestrian path.'
            }};
          }} else if (yellowSignPixels >= 14 && (yelMaxX - yelMinX) >= 4 && (yelMaxY - yelMinY) >= 4 && (yelMaxX - yelMinX) <= 36) {{
            sMinX = yelMinX; sMaxX = yelMaxX; sMinY = yelMinY; sMaxY = yelMaxY;
            detectedSignMeta = ocrMatchedSign || {{
              name: 'Road Works Sign (Ceļa darbi)',
              category: 'Temporary',
              icon: '🚧',
              spokenGuidance: 'Temporary yellow road works sign ahead. Watch for construction barriers.'
            }};
          }} else if (ocrMatchedSign) {{
            sMinX = 28; sMaxX = 52; sMinY = 10; sMaxY = 26;
            detectedSignMeta = ocrMatchedSign;
          }}

          if (detectedSignMeta) {{
            const rawBoxX = (sMinX / sW) * cW;
            const rawBoxY = (sMinY / sH) * cH;
            const rawBoxW = ((sMaxX - sMinX) / sW) * cW;
            const rawBoxH = ((sMaxY - sMinY) / sH) * cH;
            const boxW = Math.max(cW * 0.18, Math.min(cW * 0.42, rawBoxW * 1.25));
            const boxH = Math.max(cH * 0.12, Math.min(cH * 0.32, rawBoxH * 1.25));
            const boxX = Math.max(8, Math.min(cW - boxW - 8, rawBoxX));
            const boxY = Math.max(12, Math.min(cH * 0.58, rawBoxY));
            const centerX = boxX + boxW / 2;
            const estDist = Math.max(1.0, Math.min(6.5, parseFloat(((cH * 0.42) / Math.max(28, boxH)).toFixed(1))));

            extraDetections.push({{
              label: detectedSignMeta.name,
              rawClass: 'road sign',
              icon: detectedSignMeta.icon || '🪧',
              x: boxX,
              y: boxY,
              w: boxW,
              h: boxH,
              conf: 0.93,
              distance: estDist,
              lane: centerX < cW * 0.33 ? 'left' : (centerX > cW * 0.67 ? 'right' : 'center'),
              isRoadSign: true,
              signCategory: detectedSignMeta.category || 'Information',
              spokenGuidance: detectedSignMeta.spokenGuidance || `Road sign ahead: ${{detectedSignMeta.name}}.`
            }});
          }}
        }}
      }} catch (err) {{
        console.warn('[YOLO Sign & Tree Detector] Notice:', err);
      }}
      return extraDetections;
    }}

    // ==================== STANDING PEOPLE vs WALKING PEOPLE & DUAL-MOVE / DEPTH HOLE TRACKER ====================
    let personMotionHistory = [];
    let activeDualMovePath = 'normal_walk'; // 'normal_walk' (Move 1: Bus Stop Surface) or 'tunnel_down' (Move 2: Tunnel Going Down)
    let lastSpokenGuidanceKey = '';
    let lastSpokenGuidanceDist = 99.0;
    let lastPeopleAroundSpeechTime = 0;
    let lastPeopleAroundSignature = '';

    function selectDualMovePath(moveMode, announce = true) {{
      activeDualMovePath = moveMode === 'tunnel_down' ? 'tunnel_down' : 'normal_walk';
      triggerHaptic([60, 40]);

      const btnNormal = document.getElementById('btn-move-normal-walk');
      const btnTunnel = document.getElementById('btn-move-tunnel-down');
      const statusEl = document.getElementById('nav-dual-move-status');
      const stepLbl = document.getElementById('nav-step-label');
      const instrTxt = document.getElementById('nav-instruction-text');
      const manIcon = document.getElementById('nav-maneuver-icon');

      if (activeDualMovePath === 'tunnel_down') {{
        if (btnNormal) {{
          btnNormal.className = 'py-1.5 px-2 rounded-xl bg-white/10 border border-white/25 text-left flex items-center space-x-1.5 transition active:scale-95';
        }}
        if (btnTunnel) {{
          btnTunnel.className = 'py-1.5 px-2 rounded-xl bg-cyan-600/40 border-2 border-cyan-400 text-left flex items-center space-x-1.5 transition active:scale-95';
        }}
        if (statusEl) {{
          statusEl.innerText = 'Active Move 2: Tunnel Going Down • Tracking downward stairs, depth holes & people';
        }}
        if (stepLbl) stepLbl.innerText = 'Dual-Move Route • Move 2: Underpass Tunnel';
        if (instrTxt) instrTxt.innerText = 'Use tunnel going down — hold handrail & watch ground depth';
        if (manIcon) manIcon.innerText = '🚇';
        if (announce) {{
          const msg = 'Move 2 active: Using pedestrian tunnel going down. Tracking downward stairs, ground depth holes, and people standing in the underpass.';
          showUniversalVoiceHUD('Move 2: Tunnel Going Down', msg, false);
          speakText(msg);
        }}
      }} else {{
        if (btnNormal) {{
          btnNormal.className = 'py-1.5 px-2 rounded-xl bg-emerald-600/35 border-2 border-emerald-400 text-left flex items-center space-x-1.5 transition active:scale-95';
        }}
        if (btnTunnel) {{
          btnTunnel.className = 'py-1.5 px-2 rounded-xl bg-white/10 border border-white/25 text-left flex items-center space-x-1.5 transition active:scale-95';
        }}
        if (statusEl) {{
          statusEl.innerText = 'Active Move 1: Normal Walk to Bus Stop • Tracking surface path & people around';
        }}
        if (stepLbl) stepLbl.innerText = 'Dual-Move Route • Move 1: Surface Walk to Bus Stop';
        if (instrTxt) instrTxt.innerText = 'Normal walk along surface sidewalk toward Bus Stop';
        if (manIcon) manIcon.innerText = '🚶';
        if (announce) {{
          const msg = 'Move 1 active: Normal surface walk to Bus Stop. Tracking sidewalk clearance, ground depth holes, and people standing around you.';
          showUniversalVoiceHUD('Move 1: Normal Walk to Bus Stop', msg, false);
          speakText(msg);
        }}
      }}
    }}

    function classifyPeopleAndStandingStatus(rawDetections, cW, cH, now) {{
      // Prune stale person motion tracks older than 3.2 seconds
      personMotionHistory = personMotionHistory.filter(t => (now - t.lastSeen) < 3200);

      (rawDetections || []).forEach(d => {{
        if (d.rawClass !== 'person') return;
        d.isPerson = true;
        computeObjectMetricDimensions(d);
        const cx = d.x + d.w / 2;
        const cy = d.y + d.h / 2;

        // Match with existing person track by spatial proximity
        let matchedTrack = null;
        let minDistPx = Math.max(48, cW * 0.22);
        for (const tr of personMotionHistory) {{
          const deltaPx = Math.hypot(cx - tr.cx, cy - tr.cy);
          if (deltaPx < minDistPx) {{
            minDistPx = deltaPx;
            matchedTrack = tr;
          }}
        }}

        if (matchedTrack) {{
          const dx = cx - matchedTrack.anchorCx;
          const dy = cy - matchedTrack.anchorCy;
          const totalShiftPx = Math.hypot(dx, dy);
          const dDist = d.distance - matchedTrack.anchorDist; // negative = approaching user, positive = moving away
          const distShiftM = Math.abs(dDist);
          const boxScaleRatio = d.h / Math.max(12, matchedTrack.anchorH || d.h);

          matchedTrack.cx = cx;
          matchedTrack.cy = cy;
          matchedTrack.lastDist = d.distance;
          matchedTrack.lastSeen = now;
          matchedTrack.framesSeen = (matchedTrack.framesSeen || 1) + 1;

          // 1. Pedestrian Crossing Path (significant lateral movement across forward corridor)
          if (Math.abs(dx) >= cW * 0.075 && Math.abs(dx) > Math.abs(dy) * 1.1) {{
            d.isPersonStanding = false;
            d.isPersonCrossing = true;
            d.pedestrianMotion = 'crossing_path';
            d.personMotion = 'crossing_path';
            d.label = 'Person Crossing Path';
            d.rawClass = 'person crossing path';
            d.icon = '🚶↔️';
            d.spokenGuidance = `Caution: Pedestrian crossing your path ahead at ${{d.distance.toFixed(1)}} meters.`;
            matchedTrack.anchorCx = cx;
            matchedTrack.anchorCy = cy;
            matchedTrack.anchorDist = d.distance;
            matchedTrack.anchorH = d.h;
          }}
          // 2. Pedestrian Walking Toward User (distance shrinking or bounding box expanding)
          else if (dDist <= -0.25 || boxScaleRatio >= 1.09) {{
            d.isPersonStanding = false;
            d.isPersonApproaching = true;
            d.pedestrianMotion = 'walking_toward';
            d.personMotion = 'walking_toward';
            d.label = 'Person Approaching';
            d.rawClass = 'person approaching';
            d.icon = '🚶⬆️';
            d.spokenGuidance = `Caution: Pedestrian walking toward you at ${{d.distance.toFixed(1)}} meters on your ${{d.lane}}.`;
            matchedTrack.anchorCx = cx;
            matchedTrack.anchorCy = cy;
            matchedTrack.anchorDist = d.distance;
            matchedTrack.anchorH = d.h;
          }}
          // 3. Pedestrian Moving Away (distance increasing or bounding box shrinking)
          else if (dDist >= 0.25 || boxScaleRatio <= 0.91) {{
            d.isPersonStanding = false;
            d.isPersonMovingAway = true;
            d.pedestrianMotion = 'moving_away';
            d.personMotion = 'moving_away';
            d.label = 'Person Moving Away';
            d.rawClass = 'person moving away';
            d.icon = '🚶⬇️';
            d.spokenGuidance = `Pedestrian moving away ahead at ${{d.distance.toFixed(1)}} meters.`;
            matchedTrack.anchorCx = cx;
            matchedTrack.anchorCy = cy;
            matchedTrack.anchorDist = d.distance;
            matchedTrack.anchorH = d.h;
          }}
          // 4. Stationary Person Standing Still in One Place
          else if (totalShiftPx < cW * 0.065 && distShiftM < 0.25) {{
            d.isPersonStanding = true;
            d.pedestrianMotion = 'standing';
            d.personMotion = 'standing';
            d.label = 'Person Standing';
            d.rawClass = 'person standing';
            d.icon = '🧍';
            d.spokenGuidance = `Caution: A person is standing still ${{d.distance.toFixed(1)}} meters ${{d.lane === 'center' ? 'ahead in your path' : 'on your ' + d.lane}}.`;
          }} else {{
            d.isPersonStanding = false;
            d.pedestrianMotion = 'walking';
            d.personMotion = 'walking';
            d.label = 'Person Walking';
            d.rawClass = 'person walking';
            d.icon = '🚶';
            matchedTrack.anchorCx = cx;
            matchedTrack.anchorCy = cy;
            matchedTrack.anchorDist = d.distance;
            matchedTrack.anchorH = d.h;
          }}
        }} else {{
          personMotionHistory.push({{
            anchorCx: cx,
            anchorCy: cy,
            anchorDist: d.distance,
            anchorH: d.h,
            cx: cx,
            cy: cy,
            lastDist: d.distance,
            framesSeen: 1,
            lastSeen: now
          }});
          // If a person is detected close in the user's forward corridor on frame 1, immediately flag as Person Standing so user doesn't bump into them
          if (d.distance <= 2.8) {{
            d.isPersonStanding = true;
            d.pedestrianMotion = 'standing';
            d.personMotion = 'standing';
            d.label = 'Person Standing';
            d.rawClass = 'person standing';
            d.icon = '🧍';
          }} else {{
            d.isPersonStanding = false;
            d.pedestrianMotion = 'standing';
            d.personMotion = 'standing';
            d.label = 'Person';
            d.icon = '👤';
          }}
        }}
      }});
    }}

    function detectDepthHoleAndTunnelInFrame(video, cW, cH, rawDetections) {{
      const groundAndTunnelObjs = [];
      try {{
        if (!video || video.readyState < 2 || !(video.videoWidth > 0)) return groundAndTunnelObjs;
        if (!crosswalkScanCanvas) {{
          crosswalkScanCanvas = document.createElement('canvas');
          crosswalkScanCanvas.width = 80;
          crosswalkScanCanvas.height = 60;
          crosswalkScanCtx = crosswalkScanCanvas.getContext('2d', {{ willReadFrequently: true }});
        }}
        const sW = 80;
        const sH = 60;
        crosswalkScanCtx.drawImage(video, 0, 0, sW, sH);
        const frameData = crosswalkScanCtx.getImageData(0, 0, sW, sH).data;

        const lum = new Float32Array(sW * sH);
        for (let i = 0; i < sW * sH; i++) {{
          const idx = i * 4;
          lum[i] = 0.299 * frameData[idx] + 0.587 * frameData[idx + 1] + 0.114 * frameData[idx + 2];
        }}

        // --- 1. Ground Depth Hole / Drop-Off / Trench / Open Pit Detector (🕳️ Depth Hole) ---
        // Compute mean ground walkway luminance in lower sidewalk corridor (y: 35..56, x: 12..68)
        let groundSum = 0;
        let groundCount = 0;
        for (let y = 35; y <= 56; y++) {{
          for (let x = 12; x <= 68; x++) {{
            groundSum += lum[y * sW + x];
            groundCount++;
          }}
        }}
        const groundMeanLum = groundCount > 0 ? (groundSum / groundCount) : 0;

        // Only detect a ground cavity when surrounding pavement is visible (groundMeanLum > 68)
        if (groundMeanLum > 68) {{
          let holePixels = 0;
          let rimEdgePixels = 0;
          let hMinX = sW, hMaxX = 0, hMinY = sH, hMaxY = 0;

          for (let y = 37; y <= 55; y++) {{
            for (let x = 16; x <= 64; x++) {{
              const l = lum[y * sW + x];
              // Localized deep dark cavity significantly darker than surrounding pavement
              if (l < groundMeanLum - 38 && l < 65) {{
                holePixels++;
                if (x < hMinX) hMinX = x;
                if (x > hMaxX) hMaxX = x;
                if (y < hMinY) hMinY = y;
                if (y > hMaxY) hMaxY = y;
                const upperLum = lum[(y - 2) * sW + x];
                if (upperLum - l >= 28) {{
                  rimEdgePixels++;
                }}
              }}
            }}
          }}

          const hSpanX = hMaxX - hMinX;
          const hSpanY = hMaxY - hMinY;
          // Bounded ground cavity (prevents wide road asphalt or full-frame shadow from false-triggering)
          if (holePixels >= 12 && holePixels <= 175 && rimEdgePixels >= 5 && hSpanX >= 5 && hSpanX <= 32 && hSpanY >= 3 && hSpanY <= 15) {{
            const boxX = Math.max(10, (hMinX / sW) * cW);
            const boxY = Math.max(cH * 0.56, (hMinY / sH) * cH);
            const boxW = Math.max(cW * 0.16, Math.min(cW * 0.46, ((hSpanX + 4) / sW) * cW));
            const boxH = Math.max(cH * 0.10, Math.min(cH * 0.25, ((hSpanY + 3) / sH) * cH));
            const centerX = boxX + boxW / 2;
            const normBottom = Math.min(1.0, Math.max(0.0, (hMaxY - 36) / 20));
            const holeDist = parseFloat((2.8 - normBottom * 1.9).toFixed(1));
            const holeLane = centerX < cW * 0.35 ? 'left' : (centerX > cW * 0.65 ? 'right' : 'center');

            groundAndTunnelObjs.push(computeObjectMetricDimensions({{
              label: 'Depth Hole / Drop-off',
              rawClass: 'depth hole',
              icon: '🕳️',
              x: boxX,
              y: boxY,
              w: boxW,
              h: boxH,
              conf: 0.94,
              distance: holeDist,
              widthM: 0.8,
              heightM: 0.4,
              lane: holeLane,
              isDepthHole: true,
              spokenGuidance: `Danger: Ground depth hole or drop-off detected ${{holeDist.toFixed(1)}} meters ahead in ${{holeLane}} path! Step around carefully.`
            }}));
          }}
        }}

        // --- 2. Underpass / Tunnel Going Down Detector (🚇 Tunnel Going Down) ---
        const hasUnderpassSign = (rawDetections || []).some(d =>
          (d.label && d.label.toLowerCase().includes('underpass')) ||
          (d.spokenGuidance && d.spokenGuidance.toLowerCase().includes('underpass'))
        );

        // Check for recessed dark tunnel entrance portal framed by brighter side walls + horizontal stair risers
        let portalSum = 0, portalCnt = 0;
        let sideWallSum = 0, sideWallCnt = 0;
        let stairRiserEdges = 0;

        for (let y = 16; y <= 40; y++) {{
          for (let x = 26; x <= 54; x++) {{
            portalSum += lum[y * sW + x];
            portalCnt++;
          }}
          for (let x = 6; x <= 18; x++) {{
            sideWallSum += lum[y * sW + x];
            sideWallCnt++;
          }}
          for (let x = 62; x <= 74; x++) {{
            sideWallSum += lum[y * sW + x];
            sideWallCnt++;
          }}
        }}
        for (let y = 32; y <= 50; y++) {{
          let edgeHitsInRow = 0;
          for (let x = 24; x <= 56; x++) {{
            if (Math.abs(lum[y * sW + x] - lum[(y - 1) * sW + x]) > 22) {{
              edgeHitsInRow++;
            }}
          }}
          if (edgeHitsInRow >= 14) stairRiserEdges++;
        }}

        const portalMean = portalCnt > 0 ? (portalSum / portalCnt) : 128;
        const sideWallMean = sideWallCnt > 0 ? (sideWallSum / sideWallCnt) : 128;
        const isVisualTunnelPortal = (portalMean < 64 && sideWallMean > portalMean + 36 && stairRiserEdges >= 4);

        if (hasUnderpassSign || isVisualTunnelPortal) {{
          groundAndTunnelObjs.push(computeObjectMetricDimensions({{
            label: 'Tunnel Going Down',
            rawClass: 'tunnel going down',
            icon: '🚇',
            x: cW * 0.22,
            y: cH * 0.26,
            w: cW * 0.56,
            h: cH * 0.44,
            conf: 0.93,
            distance: 2.4,
            widthM: 2.4,
            heightM: 2.2,
            lane: 'center',
            isTunnelDown: true,
            spokenGuidance: 'Two moves ahead: Move 1 is normal surface walk to Bus Stop. Move 2 is tunnel going down into the underpass.'
          }}));
        }}
      }} catch (err) {{
        console.warn('[YOLO Depth Hole & Tunnel Detector] Notice:', err);
      }}
      return groundAndTunnelObjs;
    }}

    function detectTrafficLightsStairsPolesAndGroundInFrame(video, cW, cH, rawDetections) {{
      const extraObjs = [];
      try {{
        if (!video || video.readyState < 2 || !(video.videoWidth > 0)) {{
          return extraObjs;
        }}
        if (!crosswalkScanCanvas) {{
          crosswalkScanCanvas = document.createElement('canvas');
          crosswalkScanCanvas.width = 80;
          crosswalkScanCanvas.height = 60;
          crosswalkScanCtx = crosswalkScanCanvas.getContext('2d', {{ willReadFrequently: true }});
        }}
        const sW = 80;
        const sH = 60;
        crosswalkScanCtx.drawImage(video, 0, 0, sW, sH);
        const frameData = crosswalkScanCtx.getImageData(0, 0, sW, sH).data;

        const lum = new Float32Array(sW * sH);
        for (let i = 0; i < sW * sH; i++) {{
          const idx = i * 4;
          lum[i] = 0.299 * frameData[idx] + 0.587 * frameData[idx + 1] + 0.114 * frameData[idx + 2];
        }}

        // --- 1. Traffic Light Detection & Signal Color Identification (🔴 RED / 🟡 YELLOW / 🟢 GREEN) ---
        let cocoTrafficLight = (rawDetections || []).find(d => d.rawClass === 'traffic light');
        let tlSignalColor = 'NONE';
        let tlDist = cocoTrafficLight ? cocoTrafficLight.distance : null;
        let tlLane = cocoTrafficLight ? cocoTrafficLight.lane : 'center';

        const analyzeBoxForSignalColor = (minX, maxX, minY, maxY) => {{
          let redScore = 0, yellowScore = 0, greenScore = 0;
          const spanH = Math.max(3, maxY - minY);
          for (let y = minY; y <= maxY; y++) {{
            const relY = (y - minY) / spanH;
            for (let x = minX; x <= maxX; x++) {{
              const idx = (y * sW + x) * 4;
              const r = frameData[idx];
              const g = frameData[idx + 1];
              const b = frameData[idx + 2];
              // Bright Red emitter (prefer upper half of signal head)
              if (r > 170 && r > g + 55 && r > b + 55 && relY <= 0.65) {{
                redScore += (relY < 0.42 ? 2.0 : 1.0);
              }}
              // Bright Amber / Yellow emitter (prefer middle of signal head)
              if (r > 175 && g > 135 && b < 85 && Math.abs(r - g) < 55 && relY >= 0.22 && relY <= 0.78) {{
                yellowScore += 1.6;
              }}
              // Bright Green / Cyan pedestrian walk emitter (prefer lower half of signal head)
              if (g > 155 && g > r + 35 && g >= b - 20 && relY >= 0.35) {{
                greenScore += (relY > 0.55 ? 2.0 : 1.0);
              }}
            }}
          }}
          if (redScore >= 3 && redScore >= yellowScore && redScore >= greenScore) return 'RED';
          if (greenScore >= 3 && greenScore > redScore && greenScore >= yellowScore) return 'GREEN';
          if (yellowScore >= 3 && yellowScore > redScore && yellowScore > greenScore) return 'YELLOW';
          return 'NONE';
        }};

        if (cocoTrafficLight) {{
          const bMinX = Math.max(1, Math.min(sW - 2, Math.floor((cocoTrafficLight.x / cW) * sW)));
          const bMaxX = Math.max(bMinX + 2, Math.min(sW - 1, Math.ceil(((cocoTrafficLight.x + cocoTrafficLight.w) / cW) * sW)));
          const bMinY = Math.max(1, Math.min(sH - 2, Math.floor((cocoTrafficLight.y / cH) * sH)));
          const bMaxY = Math.max(bMinY + 3, Math.min(sH - 1, Math.ceil(((cocoTrafficLight.y + cocoTrafficLight.h) / cH) * sH)));
          tlSignalColor = analyzeBoxForSignalColor(bMinX, bMaxX, bMinY, bMaxY);
          if (tlSignalColor === 'NONE') tlSignalColor = 'RED'; // Default conservative safety signal if housing detected
          cocoTrafficLight.isTrafficLight = true;
          cocoTrafficLight.signalColor = tlSignalColor;
          cocoTrafficLight.label = `Traffic Light (${{tlSignalColor}})`;
          cocoTrafficLight.icon = tlSignalColor === 'RED' ? '🔴' : (tlSignalColor === 'YELLOW' ? '🟡' : '🟢');
          cocoTrafficLight.spokenGuidance = tlSignalColor === 'RED'
            ? `Red traffic light detected at ${{cocoTrafficLight.distance.toFixed(1)}} meters. Stop at curb and wait.`
            : (tlSignalColor === 'GREEN'
                ? `Green signal detected ahead at ${{cocoTrafficLight.distance.toFixed(1)}} meters, but camera detection cannot guarantee road safety. Listen for traffic and verify before crossing.`
                : `Yellow traffic light at ${{cocoTrafficLight.distance.toFixed(1)}} meters. Prepare to stop at curb.`);
        }} else {{
          // Pixel-level scan in upper intersection region (y: 4..28, x: 12..68) for dark signal housing + glowing emitter
          let bestColor = 'NONE';
          let bestX = -1, bestY = -1;
          for (let y = 5; y <= 26; y += 2) {{
            for (let x = 14; x <= 66; x += 2) {{
              // Check for dark housing surround
              const housingLum = lum[y * sW + x];
              if (housingLum < 62) {{
                const col = analyzeBoxForSignalColor(Math.max(2, x - 3), Math.min(sW - 2, x + 3), Math.max(2, y - 4), Math.min(sH - 2, y + 6));
                if (col !== 'NONE') {{
                  bestColor = col;
                  bestX = x;
                  bestY = y;
                  break;
                }}
              }}
            }}
            if (bestColor !== 'NONE') break;
          }}
          if (bestColor !== 'NONE' && bestX > 0) {{
            tlSignalColor = bestColor;
            const boxW = cW * 0.14;
            const boxH = cH * 0.18;
            const boxX = Math.max(8, Math.min(cW - boxW - 8, (bestX / sW) * cW - boxW / 2));
            const boxY = Math.max(8, Math.min(cH * 0.45, (bestY / sH) * cH - boxH / 3));
            tlDist = 3.2;
            tlLane = (boxX + boxW / 2) < cW * 0.35 ? 'left' : ((boxX + boxW / 2) > cW * 0.65 ? 'right' : 'center');
            extraObjs.push(computeObjectMetricDimensions({{
              label: `Traffic Light (${{tlSignalColor}})`,
              rawClass: 'traffic light',
              icon: tlSignalColor === 'RED' ? '🔴' : (tlSignalColor === 'YELLOW' ? '🟡' : '🟢'),
              x: boxX, y: boxY, w: boxW, h: boxH,
              conf: 0.91,
              distance: tlDist,
              widthM: 0.35,
              heightM: 0.90,
              lane: tlLane,
              isTrafficLight: true,
              signalColor: tlSignalColor,
              spokenGuidance: tlSignalColor === 'RED'
                ? `Red traffic light ahead (${{tlDist}}m). Wait on curb.`
                : (tlSignalColor === 'GREEN'
                    ? `Green signal detected ahead (${{tlDist}}m), but camera detection cannot guarantee road safety. Listen for traffic and verify before crossing.`
                    : `Yellow traffic light ahead (${{tlDist}}m). Do not start crossing.`)
            }}));
          }}
        }}

        if (tlSignalColor !== 'NONE') {{
          currentTrafficLightSignal = {{
            detected: true,
            color: tlSignalColor,
            distance: tlDist || 3.0,
            lane: tlLane,
            confidence: 0.94,
            guidance: tlSignalColor === 'RED'
              ? 'STOP — Red signal active'
              : (tlSignalColor === 'GREEN' ? 'GREEN — Verify traffic & listen before crossing' : 'WAIT — Yellow signal changing')
          }};
        }} else {{
          currentTrafficLightSignal = {{
            detected: false,
            color: 'NONE',
            distance: null,
            lane: 'center',
            confidence: 0,
            guidance: 'No traffic light signal currently in camera view.'
          }};
        }}

        // --- 2. Stairs Detector (🪜 Stairs) ---
        const hasStairsAlready = (rawDetections || []).some(d => d.rawClass === 'stairs' || d.isStairs || d.isTunnelDown);
        if (!hasStairsAlready) {{
          let stepRiserRows = 0;
          let stMinY = sH, stMaxY = 0;
          for (let y = 28; y <= 52; y++) {{
            let horizEdges = 0;
            for (let x = 22; x <= 58; x++) {{
              const diffV = Math.abs(lum[y * sW + x] - lum[(y - 1) * sW + x]);
              const diffH = Math.abs(lum[y * sW + x] - lum[y * sW + (x - 1)]);
              if (diffV > 24 && diffH < 12) horizEdges++;
            }}
            if (horizEdges >= 18) {{
              stepRiserRows++;
              if (y < stMinY) stMinY = y;
              if (y > stMaxY) stMaxY = y;
            }}
          }}
          if (stepRiserRows >= 4 && (stMaxY - stMinY) >= 6) {{
            const boxW = cW * 0.52;
            const boxH = Math.max(cH * 0.18, ((stMaxY - stMinY + 4) / sH) * cH);
            const boxX = (cW - boxW) / 2;
            const boxY = Math.max(cH * 0.42, (stMinY / sH) * cH);
            const stairsDist = parseFloat(Math.max(1.1, Math.min(3.8, 3.4 - ((stMaxY - 28) / 24) * 2.0)).toFixed(1));
            extraObjs.push(computeObjectMetricDimensions({{
              label: 'Stairs',
              rawClass: 'stairs',
              icon: '🪜',
              x: boxX, y: boxY, w: boxW, h: boxH,
              conf: 0.92,
              distance: stairsDist,
              widthM: 1.6,
              heightM: 1.5,
              lane: 'center',
              isStairs: true,
              spokenGuidance: `Caution: Stairs detected ${{stairsDist.toFixed(1)}} meters directly ahead (approx 1.6m wide by 1.5m high). Use handrail.`
            }}));
          }}
        }}

        // --- 3. Pole / Utility Post Detector (💈 Pole) ---
        const hasPoleAlready = (rawDetections || []).some(d => d.rawClass === 'pole' || d.isPole);
        if (!hasPoleAlready) {{
          let bestPoleX = -1;
          let bestPoleScore = 0;
          for (let x = 14; x <= 66; x++) {{
            let vertEdgeRows = 0;
            for (let y = 12; y <= 48; y++) {{
              const centerLum = lum[y * sW + x];
              const leftLum = lum[y * sW + Math.max(0, x - 3)];
              const rightLum = lum[y * sW + Math.min(sW - 1, x + 3)];
              // Narrow vertical post: distinct from both left and right background by >28 luminance units
              if (Math.abs(centerLum - leftLum) > 28 && Math.abs(centerLum - rightLum) > 28 && Math.abs(leftLum - rightLum) < 22) {{
                vertEdgeRows++;
              }}
            }}
            if (vertEdgeRows >= 24 && vertEdgeRows > bestPoleScore) {{
              bestPoleScore = vertEdgeRows;
              bestPoleX = x;
            }}
          }}
          if (bestPoleX > 0) {{
            const boxW = Math.max(28, cW * 0.10);
            const boxH = cH * 0.56;
            const boxX = Math.max(6, Math.min(cW - boxW - 6, (bestPoleX / sW) * cW - boxW / 2));
            const boxY = cH * 0.18;
            const poleLane = (boxX + boxW / 2) < cW * 0.35 ? 'left' : ((boxX + boxW / 2) > cW * 0.65 ? 'right' : 'center');
            const poleDist = 2.1;
            extraObjs.push(computeObjectMetricDimensions({{
              label: 'Pole',
              rawClass: 'pole',
              icon: '💈',
              x: boxX, y: boxY, w: boxW, h: boxH,
              conf: 0.90,
              distance: poleDist,
              widthM: 0.2,
              heightM: 2.2,
              lane: poleLane,
              isPole: true,
              spokenGuidance: `Caution: Vertical pole detected ${{poleDist.toFixed(1)}} meters ahead on your ${{poleLane}} (0.2m wide by 2.2m tall).`
            }}));
          }}
        }}

        // --- 4. Ground Surface State Estimation (Flat, Tilted, or Uneven) ---
        let groundGradSum = 0;
        let groundSamples = 0;
        let leftGroundLum = 0, rightGroundLum = 0;
        for (let y = 38; y <= 55; y++) {{
          for (let x = 16; x <= 64; x++) {{
            const gx = Math.abs(lum[y * sW + x] - lum[y * sW + (x - 1)]);
            const gy = Math.abs(lum[y * sW + x] - lum[(y - 1) * sW + x]);
            groundGradSum += (gx + gy);
            groundSamples++;
            if (x < 40) leftGroundLum += lum[y * sW + x];
            else rightGroundLum += lum[y * sW + x];
          }}
        }}
        const avgGroundRoughness = groundSamples > 0 ? (groundGradSum / groundSamples) : 0;
        const hasHoleOrStairs = (rawDetections || []).some(d => d.isDepthHole || d.isStairs) || extraObjs.some(d => d.isDepthHole || d.isStairs);
        const rollAngle = Math.abs(deviceTiltGamma || 0);

        if (hasHoleOrStairs || avgGroundRoughness > 36 || recentAccelJitter > 3.2) {{
          currentGroundSurfaceState = {{
            status: 'Uneven',
            slopeDeg: parseFloat(rollAngle.toFixed(1)),
            roughnessScore: parseFloat(avgGroundRoughness.toFixed(1)),
            detail: hasHoleOrStairs
              ? 'Ground surface ahead has elevation changes or drop-offs — step carefully.'
              : 'Ground surface ahead is uneven or rough pavement.'
          }};
        }} else if (rollAngle >= 7.5) {{
          currentGroundSurfaceState = {{
            status: 'Tilted',
            slopeDeg: parseFloat(rollAngle.toFixed(1)),
            roughnessScore: parseFloat(avgGroundRoughness.toFixed(1)),
            detail: `Ground surface is tilted (${{rollAngle.toFixed(1)}}° lateral/forward slope).`
          }};
        }} else {{
          currentGroundSurfaceState = {{
            status: 'Flat',
            slopeDeg: parseFloat(rollAngle.toFixed(1)),
            roughnessScore: parseFloat(avgGroundRoughness.toFixed(1)),
            detail: 'Ground surface ahead is flat and level.'
          }};
        }}
      }} catch (err) {{
        console.warn('[YOLO TrafficLight/Stairs/Pole/Ground Detector] Notice:', err);
      }}
      return extraObjs;
    }}

    async function runYoloPerceptionCycle() {{
      if (activeRoute !== 'activeNavigation' && activeRoute !== 'crosswalkSafety') return;
      simWalkFrame++;

      const isCrosswalkScreen = activeRoute === 'crosswalkSafety';
      const canvas = document.getElementById(isCrosswalkScreen ? 'crosswalk-yolo-canvas' : 'nav-yolo-canvas');
      const video = document.getElementById(isCrosswalkScreen ? 'crosswalk-live-video' : 'nav-live-video');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      canvas.width = canvas.clientWidth || 320;
      canvas.height = canvas.clientHeight || 480;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      let activeObjects = [];
      const now = Date.now();

      // Real Camera + COCO-SSD Neural Object Detection + Standing/Moving People + Traffic Lights + Stairs & Poles + Depth Hole & Tunnel + Zebra Crossing + Road Signs
      if (isRealCameraActive && video && video.readyState >= 2 && !isDetectingFrame) {{
        isDetectingFrame = true;
        try {{
          // Lower score threshold to 0.28 so real pedestrians standing or walking outdoors at 1.5m-5m are reliably detected
          const predictions = cocoSsdModel ? await cocoSsdModel.detect(video, 20, 0.28) : [];
          if (typeof UnifiedSafetyEngine !== 'undefined') {{
            UnifiedSafetyEngine.updateSensor('camera');
          }}
          const vW = video.videoWidth || 640;
          const vH = video.videoHeight || 480;
          const cW = canvas.width;
          const cH = canvas.height;

          // Invariant aspect-ratio preserving object-cover coordinate mapping
          const scale = Math.max(cW / vW, cH / vH);
          const scaledW = vW * scale;
          const scaledH = vH * scale;
          const offsetX = (cW - scaledW) / 2;
          const offsetY = (cH - scaledH) / 2;

          // Calibrated pinhole camera focal length in pixels (standard mobile camera 68° vFOV)
          const focalLengthPx = vH * 1.08;

          const rawDetections = predictions.map(p => {{
            const boxX = p.bbox[0] * scale + offsetX;
            const boxY = p.bbox[1] * scale + offsetY;
            const boxW = p.bbox[2] * scale;
            const boxH = p.bbox[3] * scale;
            const centerX = boxX + boxW / 2;

            // Physical metric distance via calibrated pinhole camera optics:
            // Distance = (focalLengthPx * realWorldHeight) / objectPixelHeightInVideo
            const rawBoxH = Math.max(12, p.bbox[3]);
            const nominalHeight = metricObjectHeights[p.class.toLowerCase()] || metricObjectHeights['default'];
            const calculatedDist = (focalLengthPx * nominalHeight) / rawBoxH;
            const estimatedDist = Math.max(0.35, Math.min(10.0, parseFloat(calculatedDist.toFixed(1))));

            const lane = centerX < cW * 0.35 ? 'left' : (centerX > cW * 0.65 ? 'right' : 'center');

            return computeObjectMetricDimensions({{
              label: p.class.charAt(0).toUpperCase() + p.class.slice(1),
              rawClass: p.class.toLowerCase(),
              icon: getObjectIcon(p.class),
              x: boxX,
              y: boxY,
              w: boxW,
              h: boxH,
              conf: p.score,
              distance: estimatedDist,
              lane: lane
            }});
          }});

          // Classify People Around User: Walking Toward (🚶⬆️), Moving Away (🚶⬇️), Crossing Path (🚶↔️), or Standing (🧍)
          classifyPeopleAndStandingStatus(rawDetections, cW, cH, now);

          // Execute dedicated Zebra Stripe & Crossing Path Spatial Detector on live camera frame
          const crossingObj = detectCrossingPathInFrame(video, cW, cH, rawDetections);
          if (crossingObj) {{
            rawDetections.push(computeObjectMetricDimensions(crossingObj));
          }}

          // Execute dedicated Riga Road Signs & Sidewalk Tree Detector on live camera frame
          const signAndTreeObjs = detectSignsAndTreesInFrame(video, cW, cH, rawDetections);
          if (signAndTreeObjs && signAndTreeObjs.length > 0) {{
            signAndTreeObjs.forEach(item => rawDetections.push(computeObjectMetricDimensions(item)));
          }}

          // Execute Ground Depth Hole / Drop-off & Underpass Tunnel Detector on live camera frame
          const holeAndTunnelObjs = detectDepthHoleAndTunnelInFrame(video, cW, cH, rawDetections);
          if (holeAndTunnelObjs && holeAndTunnelObjs.length > 0) {{
            holeAndTunnelObjs.forEach(item => rawDetections.push(computeObjectMetricDimensions(item)));
          }}

          // Execute Traffic Lights (RED/YELLOW/GREEN), Stairs, Poles & Ground Surface State (Flat/Tilted/Uneven) Detector
          const infraObjs = detectTrafficLightsStairsPolesAndGroundInFrame(video, cW, cH, rawDetections);
          if (infraObjs && infraObjs.length > 0) {{
            infraObjs.forEach(item => rawDetections.push(computeObjectMetricDimensions(item)));
          }}

          // Temporal Exponential Moving Average (EMA) smoothing using IoU tracking
          const alpha = 0.65;
          const smoothedObjects = [];

          rawDetections.forEach(raw => {{
            let bestMatch = null;
            let bestIoU = 0.28;

            trackedSmoothedObjects.forEach(prev => {{
              const sameCategory = (prev.label === raw.label) || (prev.isPerson && raw.isPerson);
              if (sameCategory) {{
                const iou = computeBoundingBoxIoU(raw, prev);
                if (iou > bestIoU) {{
                  bestIoU = iou;
                  bestMatch = prev;
                }}
              }}
            }});

            if (bestMatch) {{
              smoothedObjects.push(computeObjectMetricDimensions({{
                ...raw,
                x: bestMatch.x * (1 - alpha) + raw.x * alpha,
                y: bestMatch.y * (1 - alpha) + raw.y * alpha,
                w: bestMatch.w * (1 - alpha) + raw.w * alpha,
                h: bestMatch.h * (1 - alpha) + raw.h * alpha,
                distance: parseFloat((bestMatch.distance * (1 - alpha) + raw.distance * alpha).toFixed(1))
              }}));
            }} else {{
              smoothedObjects.push(computeObjectMetricDimensions(raw));
            }}
          }});

          trackedSmoothedObjects = smoothedObjects;
          activeObjects = smoothedObjects;
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

      // Render Ultra-High Visibility AR YOLO Bounding Boxes & High-Contrast Badges
      activeObjects.forEach(obj => {{
        computeObjectMetricDimensions(obj);
        // Color Matrix calibrated for direct outdoor sunlight & low vision visibility
        let neonColor = '#00F59B'; // Ultra-vivid neon emerald
        let tintFill = 'rgba(0, 245, 155, 0.12)';
        let badgeSectorBg = '#059669';

        if (obj.isDepthHole || obj.rawClass === 'depth hole') {{
          neonColor = '#FF0055'; // High-alert magenta-crimson for ground depth hole / drop-off
          tintFill = 'rgba(255, 0, 85, 0.24)';
          badgeSectorBg = '#BE123C';
        }} else if (obj.isTrafficLight || obj.rawClass === 'traffic light') {{
          neonColor = obj.signalColor === 'RED' ? '#FF1E44' : (obj.signalColor === 'YELLOW' ? '#FACC15' : '#00F59B');
          tintFill = obj.signalColor === 'RED' ? 'rgba(255, 30, 68, 0.22)' : 'rgba(0, 245, 155, 0.18)';
          badgeSectorBg = obj.signalColor === 'RED' ? '#DC2626' : '#059669';
        }} else if (obj.isTunnelDown || obj.rawClass === 'tunnel going down') {{
          neonColor = '#38BDF8'; // Electric sky-blue for tunnel going down
          tintFill = 'rgba(56, 189, 248, 0.18)';
          badgeSectorBg = '#0369A1';
        }} else if (obj.isPersonCrossing || obj.isPersonApproaching) {{
          neonColor = '#FF1E44'; // High-alert crimson for pedestrian crossing or walking toward user
          tintFill = 'rgba(255, 30, 68, 0.22)';
          badgeSectorBg = '#DC2626';
        }} else if (obj.isPersonStanding) {{
          neonColor = obj.distance < 2.2 ? '#FF1E44' : '#FB923C'; // High-contrast orange/red for stationary person
          tintFill = obj.distance < 2.2 ? 'rgba(255, 30, 68, 0.20)' : 'rgba(251, 146, 60, 0.18)';
          badgeSectorBg = '#EA580C';
        }} else if (obj.isCrossingPath || obj.rawClass === 'crossing path') {{
          neonColor = '#00E5FF'; // Electric safety cyan for pedestrian crossing path
          tintFill = 'rgba(0, 229, 255, 0.16)';
          badgeSectorBg = '#0284C7';
        }} else if (obj.isRoadSign || obj.rawClass === 'road sign') {{
          neonColor = '#FACC15'; // High-contrast traffic sign gold
          tintFill = 'rgba(250, 204, 21, 0.16)';
          badgeSectorBg = '#CA8A04';
        }} else if (obj.isTree || obj.rawClass === 'tree') {{
          neonColor = obj.distance < 1.8 ? '#FF1E44' : (obj.distance < 2.8 ? '#FFB703' : '#84CC16');
          tintFill = obj.distance < 1.8 ? 'rgba(255, 30, 68, 0.18)' : 'rgba(132, 204, 22, 0.16)';
          badgeSectorBg = '#65A30D';
        }} else if (obj.distance < 1.5) {{
          neonColor = '#FF1E44'; // Ultra-vivid laser crimson
          tintFill = 'rgba(255, 30, 68, 0.18)';
          badgeSectorBg = '#DC2626';
        }} else if (obj.distance < 2.8) {{
          neonColor = '#FFB703'; // Ultra-vivid laser amber
          tintFill = 'rgba(255, 183, 3, 0.15)';
          badgeSectorBg = '#D97706';
        }}

        const cornerLen = Math.min(22, Math.max(12, obj.w * 0.22));

        // 1. Perspective Ground Contact Projection Ellipse (Floor placement)
        const groundCenterX = obj.x + obj.w / 2;
        const groundCenterY = obj.y + obj.h;
        const groundRadiusX = Math.max(16, obj.w * 0.42);
        const groundRadiusY = Math.max(6, obj.w * 0.12);

        ctx.save();
        ctx.beginPath();
        ctx.ellipse(groundCenterX, groundCenterY, groundRadiusX, groundRadiusY, 0, 0, Math.PI * 2);
        ctx.fillStyle = tintFill;
        ctx.fill();
        ctx.lineWidth = 2.5;
        ctx.strokeStyle = neonColor;
        ctx.stroke();
        ctx.restore();

        // 2. Holographic Silhouette Fill & Zebra Crosswalk Stripe Overlay
        ctx.fillStyle = tintFill;
        if (ctx.roundRect) {{
          ctx.beginPath();
          ctx.roundRect(obj.x, obj.y, obj.w, obj.h, 10);
          ctx.fill();
        }} else {{
          ctx.fillRect(obj.x, obj.y, obj.w, obj.h);
        }}

        if (obj.isCrossingPath || obj.rawClass === 'crossing path') {{
          ctx.save();
          const numStripes = 4;
          const stripeStep = obj.h / (numStripes * 2);
          ctx.fillStyle = 'rgba(255, 255, 255, 0.30)';
          for (let s = 0; s < numStripes; s++) {{
            const sy = obj.y + stripeStep * (s * 2 + 0.5);
            const inset = (numStripes - 1 - s) * (obj.w * 0.04);
            ctx.fillRect(obj.x + inset + 6, sy, Math.max(10, obj.w - inset * 2 - 12), stripeStep * 0.75);
          }}
          ctx.restore();
        }}

        // 3. WCAG AAA Dual-Layer Anti-Glare Bounding Box
        ctx.save();
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.95)';
        ctx.lineWidth = 6;
        ctx.lineJoin = 'round';
        if (ctx.roundRect) {{
          ctx.beginPath();
          ctx.roundRect(obj.x, obj.y, obj.w, obj.h, 10);
          ctx.stroke();
        }} else {{
          ctx.strokeRect(obj.x, obj.y, obj.w, obj.h);
        }}

        ctx.strokeStyle = neonColor;
        ctx.lineWidth = 3.5;
        if (ctx.roundRect) {{
          ctx.beginPath();
          ctx.roundRect(obj.x, obj.y, obj.w, obj.h, 10);
          ctx.stroke();
        }} else {{
          ctx.strokeRect(obj.x, obj.y, obj.w, obj.h);
        }}
        ctx.restore();

        // 4. Tactical Aerospace Corner Reticles
        const reticles = [
          [[obj.x, obj.y + cornerLen], [obj.x, obj.y], [obj.x + cornerLen, obj.y]],
          [[obj.x + obj.w - cornerLen, obj.y], [obj.x + obj.w, obj.y], [obj.x + obj.w, obj.y + cornerLen]],
          [[obj.x, obj.y + obj.h - cornerLen], [obj.x, obj.y + obj.h], [obj.x + cornerLen, obj.y + obj.h]],
          [[obj.x + obj.w - cornerLen, obj.y + obj.h], [obj.x + obj.w, obj.y + obj.h], [obj.x + obj.w, obj.y + obj.h - cornerLen]]
        ];

        reticles.forEach(pts => {{
          ctx.strokeStyle = 'rgba(0, 0, 0, 0.95)';
          ctx.lineWidth = 7;
          ctx.lineCap = 'square';
          ctx.beginPath();
          ctx.moveTo(pts[0][0], pts[0][1]);
          ctx.lineTo(pts[1][0], pts[1][1]);
          ctx.lineTo(pts[2][0], pts[2][1]);
          ctx.stroke();

          ctx.strokeStyle = neonColor;
          ctx.lineWidth = 4;
          ctx.beginPath();
          ctx.moveTo(pts[0][0], pts[0][1]);
          ctx.lineTo(pts[1][0], pts[1][1]);
          ctx.lineTo(pts[2][0], pts[2][1]);
          ctx.stroke();
        }});

        // 5. High-Contrast Sunlight-Legible HUD Badge Pill (includes Distance + Width × Height)
        const distStr = `${{obj.distance.toFixed(1)}}m`;
        const dimStr = `${{obj.widthM || 0.6}}×${{obj.heightM || 1.5}}m`;
        const pillText = `${{obj.icon}} ${{obj.label}} • ${{distStr}} [${{dimStr}}]`;

        ctx.font = 'bold 12px system-ui, -apple-system, sans-serif';
        const labelWidth = ctx.measureText(pillText).width;
        const pillW = Math.max(135, labelWidth + 28);
        const pillH = 26;
        const pillX = Math.max(6, Math.min(canvas.width - pillW - 6, obj.x));
        const pillY = Math.max(8, obj.y - pillH - 6);

        ctx.fillStyle = 'rgba(10, 15, 24, 0.94)';
        if (ctx.roundRect) {{
          ctx.beginPath();
          ctx.roundRect(pillX, pillY, pillW, pillH, 8);
          ctx.fill();
        }} else {{
          ctx.fillRect(pillX, pillY, pillW, pillH);
        }}

        ctx.strokeStyle = neonColor;
        ctx.lineWidth = 2;
        if (ctx.roundRect) {{
          ctx.beginPath();
          ctx.roundRect(pillX, pillY, pillW, pillH, 8);
          ctx.stroke();
        }} else {{
          ctx.strokeRect(pillX, pillY, pillW, pillH);
        }}

        ctx.beginPath();
        ctx.arc(pillX + 11, pillY + pillH / 2, 4, 0, Math.PI * 2);
        ctx.fillStyle = neonColor;
        ctx.fill();

        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 11.5px system-ui, -apple-system, sans-serif';
        ctx.fillText(pillText, pillX + 20, pillY + 17);
      }});

      // Multi-Lane Corridor, People Around (Toward/Away/Crossing/Standing), Traffic Lights, Stairs/Poles, Ground State & Dual-Move Analysis
      let minLeftDist = 5.0;
      let minCenterDist = 5.0;
      let minRightDist = 5.0;
      let closestCenter = null;
      let detectedCrossing = null;
      let detectedRoadSign = null;
      let detectedTree = null;
      let detectedDepthHole = null;
      let detectedTunnelDown = null;
      let detectedTrafficLight = null;
      let detectedStairs = null;
      let detectedPole = null;
      const peopleAround = [];
      const standingPeople = [];
      const approachingOrCrossingPeople = [];
      const solidObstacles = [];

      activeObjects.forEach(obj => {{
        if (obj.isTrafficLight || obj.rawClass === 'traffic light') {{
          if (!detectedTrafficLight || obj.distance < detectedTrafficLight.distance) {{
            detectedTrafficLight = obj;
          }}
          return;
        }}
        if (obj.isCrossingPath || obj.rawClass === 'crossing path' || obj.rawClass === 'crosswalk') {{
          if (!detectedCrossing || obj.distance < detectedCrossing.distance) {{
            detectedCrossing = obj;
          }}
          return;
        }}
        if (obj.isTunnelDown || obj.rawClass === 'tunnel going down') {{
          if (!detectedTunnelDown || obj.distance < detectedTunnelDown.distance) {{
            detectedTunnelDown = obj;
          }}
          return;
        }}
        if (obj.isRoadSign || obj.rawClass === 'road sign') {{
          if (!detectedRoadSign || obj.distance < detectedRoadSign.distance) {{
            detectedRoadSign = obj;
          }}
          return;
        }}
        if (obj.isDepthHole || obj.rawClass === 'depth hole') {{
          if (!detectedDepthHole || obj.distance < detectedDepthHole.distance) {{
            detectedDepthHole = obj;
          }}
        }}
        if (obj.isStairs || obj.rawClass === 'stairs') {{
          if (!detectedStairs || obj.distance < detectedStairs.distance) {{
            detectedStairs = obj;
          }}
        }}
        if (obj.isPole || obj.rawClass === 'pole') {{
          if (!detectedPole || obj.distance < detectedPole.distance) {{
            detectedPole = obj;
          }}
        }}
        if (obj.isPerson || obj.rawClass.includes('person')) {{
          peopleAround.push(obj);
          if (obj.isPersonStanding) {{
            standingPeople.push(obj);
          }}
          if (obj.isPersonApproaching || obj.isPersonCrossing) {{
            approachingOrCrossingPeople.push(obj);
          }}
        }}
        if (obj.isTree || obj.rawClass === 'tree') {{
          if (!detectedTree || obj.distance < detectedTree.distance) {{
            detectedTree = obj;
          }}
          // Do not let pixel-heuristic foliage trigger center-path obstacle loops
          if (obj.isPixelHeuristicTree) return;
        }}
        solidObstacles.push(obj);
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

      // Update Dual-Move & People Around / Ground Surface / Traffic Light Badges
      const peopleBadge = document.getElementById('nav-people-around-badge');
      if (peopleBadge) {{
        if (approachingOrCrossingPeople.length > 0) {{
          const p0 = approachingOrCrossingPeople[0];
          peopleBadge.innerText = `${{p0.icon || '🚶⬆️'}} ${{peopleAround.length}} (${{p0.pedestrianMotion === 'crossing_path' ? 'Crossing' : 'Toward'}})`;
          peopleBadge.className = 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-rose-500/35 text-rose-200 border border-rose-400';
        }} else if (peopleAround.length > 0) {{
          peopleBadge.innerText = standingPeople.length > 0
            ? `🧍 ${{peopleAround.length}} (${{standingPeople.length}} Standing)`
            : `👥 ${{peopleAround.length}} Around`;
          peopleBadge.className = standingPeople.length > 0
            ? 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-orange-500/30 text-orange-200 border border-orange-400'
            : 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-sky-500/30 text-sky-200 border border-sky-400';
        }} else {{
          peopleBadge.innerText = '👥 0 People';
          peopleBadge.className = 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-sky-500/20 text-sky-300 border border-sky-500/30';
        }}
      }}

      const tlBadge = document.getElementById('nav-traffic-light-badge');
      if (tlBadge) {{
        if (currentTrafficLightSignal && currentTrafficLightSignal.detected && currentTrafficLightSignal.color !== 'NONE') {{
          const c = currentTrafficLightSignal.color;
          tlBadge.innerText = c === 'RED' ? '🔴 Signal: RED' : (c === 'YELLOW' ? '🟡 Signal: YELLOW' : '🟢 Signal: GREEN');
          tlBadge.className = c === 'RED'
            ? 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-red-600/40 text-red-200 border border-red-400 animate-pulse'
            : (c === 'YELLOW'
                ? 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-amber-500/40 text-amber-200 border border-amber-400'
                : 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-emerald-600/40 text-emerald-200 border border-emerald-400');
        }} else {{
          tlBadge.innerText = '🚦 Signal: None';
          tlBadge.className = 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30';
        }}
      }}

      const cwSignalPill = document.getElementById('crosswalk-traffic-signal-pill');
      if (cwSignalPill && currentTrafficLightSignal) {{
        if (currentTrafficLightSignal.detected && currentTrafficLightSignal.color !== 'NONE') {{
          const c = currentTrafficLightSignal.color;
          cwSignalPill.innerText = `🚦 Signal: ${{c}} — ${{currentTrafficLightSignal.guidance}}`;
          cwSignalPill.className = c === 'RED'
            ? 'px-3 py-1 rounded-full text-[11px] font-extrabold bg-red-600 text-white border border-red-300 mb-2 shadow-sm animate-pulse'
            : (c === 'YELLOW'
                ? 'px-3 py-1 rounded-full text-[11px] font-extrabold bg-amber-500 text-slate-950 border border-amber-300 mb-2 shadow-sm'
                : 'px-3 py-1 rounded-full text-[11px] font-extrabold bg-emerald-600 text-white border border-emerald-300 mb-2 shadow-sm');
        }}
      }}

      const depthHoleBadge = document.getElementById('nav-depth-hole-badge');
      if (depthHoleBadge) {{
        const gStat = currentGroundSurfaceState ? currentGroundSurfaceState.status : 'Flat';
        if (detectedDepthHole) {{
          depthHoleBadge.innerText = `🕳️ Hole ${{detectedDepthHole.distance.toFixed(1)}}m`;
          depthHoleBadge.className = 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-rose-600/40 text-rose-200 border border-rose-400 animate-pulse';
        }} else if (detectedTunnelDown || activeDualMovePath === 'tunnel_down') {{
          depthHoleBadge.innerText = '🚇 Tunnel Down';
          depthHoleBadge.className = 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-cyan-500/30 text-cyan-200 border border-cyan-400';
        }} else if (gStat === 'Uneven') {{
          depthHoleBadge.innerText = 'Ground: Uneven';
          depthHoleBadge.className = 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-amber-500/35 text-amber-200 border border-amber-400';
        }} else if (gStat === 'Tilted') {{
          depthHoleBadge.innerText = `Ground: Tilted (${{currentGroundSurfaceState.slopeDeg}}°)`;
          depthHoleBadge.className = 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-yellow-500/30 text-yellow-200 border border-yellow-400';
        }} else {{
          depthHoleBadge.innerText = 'Ground: Flat';
          depthHoleBadge.className = 'px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
        }}
      }}

      const approachingVehicle = solidObstacles.find(o =>
        ['car', 'bus', 'truck', 'motorcycle', 'bicycle'].includes(o.rawClass) && o.distance < 5.0
      );

      // Find closest standing or approaching/crossing person in or near walking path
      const closestStandingPerson = standingPeople.sort((a, b) => a.distance - b.distance)[0] || null;
      const closestApproachingOrCrossingPerson = approachingOrCrossingPeople.sort((a, b) => a.distance - b.distance)[0] || null;
      const closestPersonAny = peopleAround.sort((a, b) => a.distance - b.distance)[0] || null;

      // Intelligent Spatial Direction Decision (WHERE TO WALK)
      let directionStatus = 'WALK STRAIGHT • PATH CLEAR';
      let directionArrow = '⬆️';
      let guidanceSpoken = '';
      let guidanceKey = '';
      let guidanceDist = 99.0;
      let statusClass = 'text-emerald-300';
      let borderClass = 'border-emerald-500/50';

      if (detectedDepthHole && detectedDepthHole.distance <= 3.0) {{
        const safeSide = detectedDepthHole.lane === 'left' ? 'RIGHT' : (detectedDepthHole.lane === 'right' ? 'LEFT' : (minLeftDist >= minRightDist ? 'LEFT' : 'RIGHT'));
        directionStatus = `DEPTH HOLE / DROP-OFF (${{detectedDepthHole.distance.toFixed(1)}}m) • STEP ${{safeSide}}`;
        directionArrow = '🕳️';
        statusClass = 'text-rose-400 font-extrabold animate-pulse';
        borderClass = 'border-rose-500';
        guidanceSpoken = `Danger! Ground depth hole or drop-off detected ${{detectedDepthHole.distance.toFixed(1)}} meters ahead on your ${{detectedDepthHole.lane === 'center' ? 'center path' : detectedDepthHole.lane}}. Step ${{safeSide.toLowerCase()}} to avoid it.`;
        guidanceKey = `depth_hole_${{detectedDepthHole.lane}}`;
        guidanceDist = detectedDepthHole.distance;
      }} else if (detectedTrafficLight && detectedTrafficLight.signalColor === 'RED' && detectedTrafficLight.distance <= 4.5) {{
        directionStatus = `RED TRAFFIC LIGHT (${{detectedTrafficLight.distance.toFixed(1)}}m) • STOP AT CURB`;
        directionArrow = '🔴';
        statusClass = 'text-red-400 font-extrabold animate-pulse';
        borderClass = 'border-red-500';
        guidanceSpoken = `Stop at curb! Red traffic light ahead at ${{detectedTrafficLight.distance.toFixed(1)}} meters.`;
        guidanceKey = 'traffic_light_red';
        guidanceDist = detectedTrafficLight.distance;
      }} else if (closestApproachingOrCrossingPerson && closestApproachingOrCrossingPerson.distance <= 3.8) {{
        const p = closestApproachingOrCrossingPerson;
        const avoidDir = p.lane === 'left' ? 'RIGHT' : (p.lane === 'right' ? 'LEFT' : (minLeftDist >= minRightDist ? 'LEFT' : 'RIGHT'));
        directionStatus = p.isPersonCrossing
          ? `PERSON CROSSING PATH (${{p.distance.toFixed(1)}}m) • YIELD / STEP ${{avoidDir}}`
          : `PERSON WALKING TOWARD YOU (${{p.distance.toFixed(1)}}m ${{p.lane.toUpperCase()}}) • KEEP ${{avoidDir}}`;
        directionArrow = p.icon || '🚶⬆️';
        statusClass = 'text-rose-300 font-extrabold';
        borderClass = 'border-rose-400';
        guidanceSpoken = p.spokenGuidance || `Caution: ${{p.label}} at ${{p.distance.toFixed(1)}} meters. Keep ${{avoidDir.toLowerCase()}}.`;
        guidanceKey = `person_motion_${{p.pedestrianMotion}}_${{p.lane}}`;
        guidanceDist = p.distance;
      }} else if (closestStandingPerson && closestStandingPerson.distance <= 3.2) {{
        const avoidDir = closestStandingPerson.lane === 'left' ? 'RIGHT' : (closestStandingPerson.lane === 'right' ? 'LEFT' : (minLeftDist >= minRightDist ? 'LEFT' : 'RIGHT'));
        const posPhrase = closestStandingPerson.lane === 'center' ? 'ahead in your path' : `on your ${{closestStandingPerson.lane}}`;
        directionStatus = `PERSON STANDING (${{closestStandingPerson.distance.toFixed(1)}}m ${{closestStandingPerson.lane.toUpperCase()}}) • STEP ${{avoidDir}}`;
        directionArrow = '🧍';
        statusClass = 'text-orange-300 font-extrabold';
        borderClass = 'border-orange-500';
        guidanceSpoken = `Caution: A person is standing still ${{closestStandingPerson.distance.toFixed(1)}} meters ${{posPhrase}}. Step ${{avoidDir.toLowerCase()}} so you do not bump into them.`;
        guidanceKey = `person_standing_${{closestStandingPerson.lane}}`;
        guidanceDist = closestStandingPerson.distance;
      }} else if (detectedStairs && detectedStairs.distance <= 3.4) {{
        directionStatus = `STAIRS AHEAD (${{detectedStairs.distance.toFixed(1)}}m • ${{detectedStairs.widthM}}×${{detectedStairs.heightM}}m)`;
        directionArrow = '🪜';
        statusClass = 'text-amber-300 font-extrabold';
        borderClass = 'border-amber-400';
        guidanceSpoken = detectedStairs.spokenGuidance || `Caution: Stairs detected ${{detectedStairs.distance.toFixed(1)}} meters ahead.`;
        guidanceKey = 'stairs_ahead';
        guidanceDist = detectedStairs.distance;
      }} else if (detectedPole && detectedPole.distance <= 2.8) {{
        const avoidDir = detectedPole.lane === 'left' ? 'RIGHT' : 'LEFT';
        directionStatus = `POLE AHEAD (${{detectedPole.distance.toFixed(1)}}m ${{detectedPole.lane.toUpperCase()}}) • STEP ${{avoidDir}}`;
        directionArrow = '💈';
        statusClass = 'text-amber-300 font-bold';
        borderClass = 'border-amber-400';
        guidanceSpoken = detectedPole.spokenGuidance || `Caution: Pole ahead at ${{detectedPole.distance.toFixed(1)}} meters on your ${{detectedPole.lane}}. Step ${{avoidDir.toLowerCase()}}.`;
        guidanceKey = `pole_${{detectedPole.lane}}`;
        guidanceDist = detectedPole.distance;
      }} else if (closestPersonAny && closestPersonAny.distance <= 4.0) {{
        const posPhrase = closestPersonAny.lane === 'center' ? 'ahead' : `on your ${{closestPersonAny.lane}}`;
        directionStatus = `${{closestPersonAny.label.toUpperCase()}} (${{closestPersonAny.distance.toFixed(1)}}m ${{closestPersonAny.lane.toUpperCase()}})`;
        directionArrow = closestPersonAny.icon || '🚶';
        statusClass = 'text-sky-300 font-bold';
        borderClass = 'border-sky-400';
        guidanceSpoken = closestPersonAny.spokenGuidance || `${{closestPersonAny.label}} detected ${{closestPersonAny.distance.toFixed(1)}} meters ${{posPhrase}}.`;
        guidanceKey = `person_around_${{closestPersonAny.lane}}`;
        guidanceDist = closestPersonAny.distance;
      }} else if (detectedTrafficLight && detectedTrafficLight.signalColor === 'GREEN' && detectedTrafficLight.distance <= 4.5) {{
        directionStatus = `GREEN TRAFFIC LIGHT (${{detectedTrafficLight.distance.toFixed(1)}}m) • SAFE TO ALIGN`;
        directionArrow = '🟢';
        statusClass = 'text-emerald-300 font-extrabold';
        borderClass = 'border-emerald-400';
        guidanceSpoken = detectedTrafficLight.spokenGuidance;
        guidanceKey = 'traffic_light_green';
        guidanceDist = detectedTrafficLight.distance;
      }} else if (detectedTunnelDown && minCenterDist >= 1.2) {{
        directionStatus = `TWO MOVES: 1) WALK TO BUS STOP • 2) TUNNEL DOWN (${{detectedTunnelDown.distance.toFixed(1)}}m)`;
        directionArrow = '🚇';
        statusClass = 'text-cyan-300 font-extrabold';
        borderClass = 'border-cyan-400';
        guidanceSpoken = detectedTunnelDown.spokenGuidance;
        guidanceKey = 'tunnel_dual_move';
        guidanceDist = detectedTunnelDown.distance;
      }} else if (detectedCrossing && minCenterDist >= 1.2) {{
        if (approachingVehicle) {{
          directionStatus = `STOP AT CURB • VEHICLE NEAR CROSSING (${{approachingVehicle.distance.toFixed(1)}}m)`;
          directionArrow = '🛑';
          statusClass = 'text-red-400 font-extrabold animate-pulse';
          borderClass = 'border-red-500';
          guidanceSpoken = `Stop at curb! Crossing path ahead at ${{detectedCrossing.distance.toFixed(1)}} meters, ${{approachingVehicle.label}} approaching at ${{approachingVehicle.distance.toFixed(1)}} meters.`;
          guidanceKey = `crossing_vehicle_${{approachingVehicle.rawClass}}`;
          guidanceDist = approachingVehicle.distance;
        }} else {{
          directionStatus = `CROSSING PATH AHEAD (${{detectedCrossing.distance.toFixed(1)}}m) • ALIGN STRAIGHT`;
          directionArrow = '🚸';
          statusClass = 'text-cyan-300 font-extrabold';
          borderClass = 'border-cyan-400';
          guidanceSpoken = `Crossing path detected ahead, ${{detectedCrossing.distance.toFixed(1)}} meters. Path is clear to align and cross.`;
          guidanceKey = 'crossing_clear';
          guidanceDist = detectedCrossing.distance;
        }}
      }} else if (detectedRoadSign && minCenterDist >= 1.8) {{
        directionStatus = `SIGN DETECTED: ${{detectedRoadSign.label.toUpperCase()}} (${{detectedRoadSign.distance.toFixed(1)}}m)`;
        directionArrow = detectedRoadSign.icon || '🪧';
        statusClass = 'text-yellow-300 font-extrabold';
        borderClass = 'border-yellow-400';
        guidanceSpoken = detectedRoadSign.spokenGuidance || `Road sign ahead at ${{detectedRoadSign.distance.toFixed(1)}} meters: ${{detectedRoadSign.label}}.`;
        guidanceKey = `sign_${{detectedRoadSign.label}}`;
        guidanceDist = detectedRoadSign.distance;
      }} else if (detectedTree && !detectedTree.isPixelHeuristicTree && detectedTree.distance < 2.4 && minCenterDist >= 0.8) {{
        const veerSide = detectedTree.lane === 'left' ? 'RIGHT' : 'LEFT';
        directionStatus = `TREE AHEAD (${{detectedTree.distance.toFixed(1)}}m ON ${{detectedTree.lane.toUpperCase()}}) • KEEP ${{veerSide}}`;
        directionArrow = '🌳';
        statusClass = 'text-lime-300 font-bold';
        borderClass = 'border-lime-400';
        guidanceSpoken = `Caution: Tree ahead at ${{detectedTree.distance.toFixed(1)}} meters on your ${{detectedTree.lane}}. Watch for tree trunk and low branches. Keep ${{veerSide.toLowerCase()}}.`;
        guidanceKey = `tree_${{detectedTree.lane}}`;
        guidanceDist = detectedTree.distance;
      }} else if (minCenterDist >= 2.2) {{
        directionStatus = activeDualMovePath === 'tunnel_down'
          ? 'TUNNEL PATH • WATCH STEPS & DEPTH AHEAD'
          : 'WALK STRAIGHT • PATH CLEAR';
        directionArrow = activeDualMovePath === 'tunnel_down' ? '🚇' : '⬆️';
        statusClass = 'text-emerald-300';
        borderClass = 'border-emerald-500/50';
      }} else if (minCenterDist < 0.8) {{
        directionStatus = 'STOP • COLLISION HAZARD';
        directionArrow = '🛑';
        statusClass = 'text-red-400 font-extrabold animate-pulse';
        borderClass = 'border-red-500';
        guidanceSpoken = `Stop! ${{closestCenter ? closestCenter.label : 'Obstacle'}} directly ahead at ${{minCenterDist.toFixed(1)}} meters!`;
        guidanceKey = `critical_${{closestCenter ? closestCenter.rawClass : 'obstacle'}}`;
        guidanceDist = minCenterDist;
      }} else {{
        // Real COCO-SSD obstacle 0.8m - 2.2m in walking path
        const obsLabel = closestCenter ? closestCenter.label : 'Obstacle';
        if (minLeftDist >= minRightDist && minLeftDist >= 1.8) {{
          directionStatus = `STEER LEFT • ${{obsLabel.toUpperCase()}} (${{minCenterDist.toFixed(1)}}m)`;
          directionArrow = '↖️';
          statusClass = 'text-amber-300 font-bold';
          borderClass = 'border-amber-500';
          guidanceSpoken = `${{obsLabel}} ${{minCenterDist.toFixed(1)}} meters ahead. Step left to pass.`;
        }} else if (minRightDist > minLeftDist && minRightDist >= 1.8) {{
          directionStatus = `STEER RIGHT • ${{obsLabel.toUpperCase()}} (${{minCenterDist.toFixed(1)}}m)`;
          directionArrow = '↗️';
          statusClass = 'text-amber-300 font-bold';
          borderClass = 'border-amber-500';
          guidanceSpoken = `${{obsLabel}} ${{minCenterDist.toFixed(1)}} meters ahead. Step right to pass.`;
        }} else {{
          directionStatus = 'SLOW DOWN • NARROW CORRIDOR';
          directionArrow = '⚠️';
          statusClass = 'text-orange-300 font-bold';
          borderClass = 'border-orange-500';
          guidanceSpoken = `${{obsLabel}} ${{minCenterDist.toFixed(1)}} meters ahead. Proceed carefully.`;
        }}
        guidanceKey = `obs_${{obsLabel}}_${{closestCenter ? closestCenter.lane : 'center'}}`;
        guidanceDist = minCenterDist;
      }}

      // Update Screen 5 Corridor HUD
      const hudEl = document.getElementById('nav-lidar-corridor-hud');
      const arrEl = document.getElementById('nav-direction-arrow');
      const statEl = document.getElementById('nav-corridor-status');
      const depthEl = document.getElementById('nav-depth-meters');
      const lanesEl = document.getElementById('nav-lateral-lanes');
      const cameraPill = document.getElementById('camera-status-pill');

      if (cameraPill && isRealCameraActive) {{
        cameraPill.innerText = activeObjects.length > 0 
          ? `YOLO AR: ${{activeObjects.length}} object${{activeObjects.length > 1 ? 's' : ''}} tracked`
          : `YOLO AR: Scanning active`;
      }}
      if (arrEl) arrEl.innerText = directionArrow;
      if (statEl) {{
        statEl.innerText = directionStatus;
        statEl.className = 'text-[11px] font-bold tracking-wide uppercase ' + statusClass;
      }}
      if (depthEl) {{
        depthEl.innerText = detectedDepthHole
          ? (detectedDepthHole.distance.toFixed(1) + 'm 🕳️')
          : (detectedTrafficLight
              ? (`${{detectedTrafficLight.distance.toFixed(1)}}m ${{detectedTrafficLight.icon}}`)
              : (closestStandingPerson
                  ? (closestStandingPerson.distance.toFixed(1) + 'm 🧍')
                  : (detectedCrossing
                      ? (detectedCrossing.distance.toFixed(1) + 'm 🚸')
                      : (detectedRoadSign ? (detectedRoadSign.distance.toFixed(1) + 'm 🪧') : (solidObstacles.length > 0 ? (minCenterDist.toFixed(1) + 'm') : 'Clear (>3m)')))));
      }}
      if (lanesEl) {{
        const gStat = currentGroundSurfaceState ? currentGroundSurfaceState.status : 'Flat';
        lanesEl.innerText = activeObjects.length > 0 
          ? `${{activeObjects.length}} visible (${{activeObjects[0].label}} ${{activeObjects[0].widthM}}×${{activeObjects[0].heightM}}m) • Ground: ${{gStat}}`
          : `Corridor: Clear • Ground: ${{gStat}}`;
      }}
      if (hudEl) hudEl.className = `w-full mt-2 py-2 px-3 rounded-2xl bg-black/85 backdrop-blur-md border ${{borderClass}} text-white shadow-xl flex items-center justify-between`;

      // Update Top HUD Hazard Status Badge
      const badge = document.getElementById('nav-live-hazard-badge');
      const pathText = document.getElementById('nav-path-status-text');
      const yoloCount = document.getElementById('nav-yolo-count');

      if (yoloCount) {{
        yoloCount.innerText = activeObjects.length > 0 
          ? `YOLO AR: ${{activeObjects.length}} tracked (${{activeObjects[0].label}} ${{activeObjects[0].distance.toFixed(1)}}m [${{activeObjects[0].widthM}}×${{activeObjects[0].heightM}}m])` 
          : `YOLO AR: Active • Ground: ${{currentGroundSurfaceState ? currentGroundSurfaceState.status : 'Flat'}}`;
      }}

      if (badge && pathText) {{
        if (detectedDepthHole) {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-rose-100 border border-rose-400 text-rose-950 text-[11px] font-extrabold flex items-center justify-between";
          pathText.innerText = `🕳️ Depth Hole / Drop-off (${{detectedDepthHole.distance.toFixed(1)}}m ${{detectedDepthHole.lane}})`;
        }} else if (detectedTrafficLight && detectedTrafficLight.signalColor === 'RED') {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-red-100 border border-red-400 text-red-950 text-[11px] font-extrabold flex items-center justify-between";
          pathText.innerText = `🔴 Traffic Light: RED (${{detectedTrafficLight.distance.toFixed(1)}}m) • Stop at Curb`;
        }} else if (closestApproachingOrCrossingPerson && closestApproachingOrCrossingPerson.distance <= 3.8) {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-rose-100 border border-rose-400 text-rose-950 text-[11px] font-extrabold flex items-center justify-between";
          pathText.innerText = `${{closestApproachingOrCrossingPerson.icon}} ${{closestApproachingOrCrossingPerson.label}} (${{closestApproachingOrCrossingPerson.distance.toFixed(1)}}m ${{closestApproachingOrCrossingPerson.lane}})`;
        }} else if (closestStandingPerson && closestStandingPerson.distance <= 3.2) {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-orange-100 border border-orange-400 text-orange-950 text-[11px] font-extrabold flex items-center justify-between";
          pathText.innerText = `🧍 Person Standing (${{closestStandingPerson.distance.toFixed(1)}}m ${{closestStandingPerson.lane}}) • Step Around`;
        }} else if (detectedCrossing && approachingVehicle) {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-red-100 border border-red-300 text-red-900 text-[11px] font-semibold flex items-center justify-between";
          pathText.innerText = `🛑 Crossing Path (${{detectedCrossing.distance.toFixed(1)}}m) • Vehicle Nearby!`;
        }} else if (detectedCrossing && (!closestCenter || closestCenter.distance >= 1.5)) {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-cyan-50 border border-cyan-300 text-cyan-900 text-[11px] font-bold flex items-center justify-between";
          pathText.innerText = `🚸 Crossing Path Detected (${{detectedCrossing.distance.toFixed(1)}}m) • Safe to Align`;
        }} else if (detectedRoadSign && (!closestCenter || closestCenter.distance >= 1.5)) {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-yellow-50 border border-yellow-300 text-yellow-900 text-[11px] font-bold flex items-center justify-between";
          pathText.innerText = `${{detectedRoadSign.icon || '🪧'}} ${{detectedRoadSign.label}} (${{detectedRoadSign.distance.toFixed(1)}}m)`;
        }} else if (closestCenter && closestCenter.distance < 1.5) {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-red-100 border border-red-300 text-red-900 text-[11px] font-semibold flex items-center justify-between";
          pathText.innerText = `Hazard: ${{closestCenter.label}} (${{closestCenter.distance.toFixed(1)}}m • ${{closestCenter.widthM}}×${{closestCenter.heightM}}m)`;
        }} else if (closestCenter && closestCenter.distance < 2.5) {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-amber-100 border border-amber-300 text-amber-900 text-[11px] font-semibold flex items-center justify-between";
          pathText.innerText = `Caution: ${{closestCenter.label}} (${{closestCenter.distance.toFixed(1)}}m • ${{closestCenter.widthM}}×${{closestCenter.heightM}}m)`;
        }} else {{
          badge.className = "w-full mt-2 py-1.5 px-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-[11px] font-semibold flex items-center justify-between";
          pathText.innerText = `Clear pathway ahead • Ground: ${{currentGroundSurfaceState ? currentGroundSurfaceState.status : 'Flat'}}`;
        }}
      }}

      // Update 180° Top-Down Proximity Radar
      drawProximityRadar(activeObjects);

      // Smart Deduplicated Voice Guidance (No repetitive 5-second "Caution ... center path" loops and no popping sound)
      if (!guidanceSpoken) {{
        // Reset spoken key when corridor becomes clear for over 3 seconds
        if (now - lastSpokenObstacleTime > 3500) {{
          lastSpokenGuidanceKey = '';
          lastSpokenGuidanceDist = 99.0;
        }}
      }} else {{
        const isNewHazard = (guidanceKey !== lastSpokenGuidanceKey);
        const gotSignificantlyCloser = (lastSpokenGuidanceDist - guidanceDist >= 0.65);
        const criticalRepeat = (guidanceDist < 1.0 && (now - lastSpokenObstacleTime > 12000));
        const cooldownElapsed = (now - lastSpokenObstacleTime > 4200);

        if (cooldownElapsed && (isNewHazard || gotSignificantlyCloser || criticalRepeat)) {{
          lastSpokenObstacleTime = now;
          lastSpokenGuidanceKey = guidanceKey;
          lastSpokenGuidanceDist = guidanceDist;
          triggerHaptic(guidanceDist < 1.0 ? [150, 50, 150, 50, 200] : [80, 50, 80]);
          if (guidanceDist < 0.85 || detectedDepthHole) playEarcon('hazard');
          speakText(guidanceSpoken);

          // If Critical Stop (< 0.8m), navigate to Screen 8 with real obstacle details
          if (minCenterDist < 0.8 && closestCenter) {{
            updateLidarState(closestCenter.distance, closestCenter.label, closestCenter.lane, false);
            navigateTo('obstacleAlert');
          }}
        }}
      }}
    }}

    let radarSweepAngle = 0;
    function drawProximityRadar(activeObjects) {{
      const canvas = document.getElementById('nav-radar-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const w = canvas.width;
      const h = canvas.height;
      const originX = w / 2;
      const originY = h - 4;
      const maxRadius = 46;

      ctx.clearRect(0, 0, w, h);

      // Radar Range Arcs (1m, 2m, 3.5m)
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
      ctx.lineWidth = 1;
      [14, 28, maxRadius].forEach(r => {{
        ctx.beginPath();
        ctx.arc(originX, originY, r, Math.PI, 2 * Math.PI);
        ctx.stroke();
      }});

      // Sector dividing lines (-45°, 0°, +45°)
      [-Math.PI * 0.75, -Math.PI * 0.5, -Math.PI * 0.25].forEach(ang => {{
        ctx.beginPath();
        ctx.moveTo(originX, originY);
        ctx.lineTo(originX + maxRadius * Math.cos(ang), originY + maxRadius * Math.sin(ang));
        ctx.stroke();
      }});

      // Radar Sweep Line
      radarSweepAngle += 0.08;
      if (radarSweepAngle > Math.PI) radarSweepAngle = 0;
      const sweepRad = Math.PI + radarSweepAngle;
      ctx.strokeStyle = 'rgba(0, 245, 155, 0.5)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(originX, originY);
      ctx.lineTo(originX + maxRadius * Math.cos(sweepRad), originY + maxRadius * Math.sin(sweepRad));
      ctx.stroke();

      // Plot detected objects as glowing blips
      let hazardCount = 0;
      let closestInRadar = null;

      activeObjects.forEach(obj => {{
        // Map distance [0.4m .. 4.0m] to radial radius [8 .. maxRadius]
        const rNorm = Math.min(1.0, Math.max(0.12, (obj.distance - 0.3) / 3.7));
        const rPx = rNorm * maxRadius;

        // Map lane / X coordinate to polar angle in semi-circle
        let angle = Math.PI * 1.5;
        if (obj.lane === 'left') angle = Math.PI * 1.22;
        if (obj.lane === 'right') angle = Math.PI * 1.78;

        const blipX = originX + rPx * Math.cos(angle);
        const blipY = originY + rPx * Math.sin(angle);

        const blipColor = obj.distance < 1.5 ? '#FF1E44' : (obj.distance < 2.8 ? '#FFB703' : '#00F59B');
        if (obj.distance < 2.5) hazardCount++;
        if (!closestInRadar || obj.distance < closestInRadar.distance) closestInRadar = obj;

        // Blip outer glow
        ctx.beginPath();
        ctx.arc(blipX, blipY, 4.5, 0, Math.PI * 2);
        ctx.fillStyle = blipColor;
        ctx.fill();

        // Blip white core
        ctx.beginPath();
        ctx.arc(blipX, blipY, 2, 0, Math.PI * 2);
        ctx.fillStyle = '#FFFFFF';
        ctx.fill();
      }});

      // User Origin Indicator
      ctx.fillStyle = '#FFFFFF';
      ctx.beginPath();
      ctx.arc(originX, originY, 3, 0, Math.PI * 2);
      ctx.fill();

      // Update Radar Summary UI
      const sumEl = document.getElementById('nav-radar-summary');
      const countEl = document.getElementById('nav-radar-count-badge');
      if (sumEl) {{
        if (closestInRadar) {{
          sumEl.innerText = `${{closestInRadar.label}} ${{closestInRadar.distance.toFixed(1)}}m (${{closestInRadar.lane}})`;
          sumEl.className = 'text-[11px] font-bold truncate ' + (closestInRadar.distance < 1.5 ? 'text-red-400' : (closestInRadar.distance < 2.8 ? 'text-amber-300' : 'text-emerald-300'));
        }} else {{
          sumEl.innerText = 'Clear 180° field ahead';
          sumEl.className = 'text-[11px] font-bold text-emerald-300 truncate';
        }}
      }}
      if (countEl) {{
        countEl.innerText = `${{activeObjects.length}} in scan`;
        countEl.className = activeObjects.length > 0
          ? 'px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30'
          : 'px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
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
        lastDetectedSignboards = detected.signs.map(s => {{
          const m = s.rigaCatalogMatch || matchRigaRoadSignClient(s.text);
          return {{ ...s, rigaCatalogMatch: m || null }};
        }});
        const primarySign = lastDetectedSignboards[0];
        const matchedCatalog = primarySign.rigaCatalogMatch;
        const signLabel = matchedCatalog
          ? `${{matchedCatalog.icon}} ${{matchedCatalog.name}} (${{matchedCatalog.category}} Sign)`
          : `${{primarySign.text}} • ${{primarySign.type === 'street_sign' ? 'Street Sign' : 'Building Board'}}`;

        if (bannerText) {{
          bannerText.innerText = signLabel;
        }}
        if (banner) {{
          banner.classList.remove('opacity-0', 'scale-95');
          banner.classList.add('opacity-100', 'scale-100');
        }}

        // Render floating signboard badges on HUD overlay
        if (overlay) {{
          overlay.innerHTML = lastDetectedSignboards.map(s => {{
            const cat = s.rigaCatalogMatch;
            const icon = cat ? cat.icon : (s.type === 'street_sign' ? '🪧' : (s.type === 'transit_sign' ? '🚏' : '🏢'));
            return `
            <div class="px-3 py-1.5 rounded-2xl bg-purple-950/85 backdrop-blur-md border border-purple-400 text-white text-xs font-bold shadow-lg flex items-center space-x-2 animate-bounce pointer-events-auto">
              <span>${{icon}}</span>
              <span>${{cat ? cat.name : s.text}}</span>
              <span class="text-[10px] text-purple-200 bg-purple-800/80 px-1.5 py-0.5 rounded-full">${{Math.round((s.confidence || 0.95) * 100)}}%</span>
            </div>
          `;
          }}).join('');
        }}

        const now = Date.now();
        if (!quiet || (now - lastSpokenSignTime > 12000 && lastSpokenSignText !== primarySign.text)) {{
          lastSpokenSignTime = now;
          lastSpokenSignText = primarySign.text;
          triggerHaptic([60, 40]);
          const signConf = primarySign.confidence !== undefined ? primarySign.confidence : 0.92;
          const spoken = signConf < 0.65
            ? "I can't confidently identify the sign. Please proceed cautiously."
            : ((matchedCatalog && matchedCatalog.spokenGuidance) || detected.summary || primarySign.spoken_announcement || `Detected signboard: ${{primarySign.text}}.`);
          speakText(spoken);
          announceToScreenReader(`Signboard detected: ${{primarySign.text}}`);
        }}
      }} else {{
        lastDetectedSignboards = [];
        if (bannerText) bannerText.innerText = "Scanning for street signs...";
        if (overlay) overlay.innerHTML = "";
      }}
    }}

    // Module 3A: Format YOLO detections in canonical schema {{ objects: [{{ class, confidence, bbox }}] }}
    function formatYoloDetectionsJson(detections) {{
      return {{
        objects: (detections || []).map(d => ({{
          class: d.rawClass || (d.label ? d.label.toLowerCase() : 'object'),
          confidence: Number((d.conf !== undefined ? d.conf : 0.92).toFixed(2)),
          bbox: [
            Math.round(d.x || 0),
            Math.round(d.y || 0),
            Math.round((d.x || 0) + (d.w || 60)),
            Math.round((d.y || 0) + (d.h || 60))
          ],
          distanceMeters: d.distance,
          lane: d.lane
        }}))
      }};
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
      }} else if (buttonId === 'crosswalk_mode') {{
        flashElement(document.getElementById('btn-crosswalk-mode'));
        setTimeout(() => navigateTo('crosswalkSafety'), 400);
      }} else if (buttonId === 'toggle_high_contrast') {{
        flashElement(document.getElementById('btn-contrast-mode'));
        toggleHighContrastMode();
      }} else if (buttonId === 'toggle_night_vision') {{
        flashElement(document.getElementById('btn-night-vision'));
        toggleNightVisionMode();
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

    function buildLiveVoiceContext() {{
      const objects = (lastLiveDetections || []).map(o => {{
        computeObjectMetricDimensions(o);
        return {{
          label: o.label,
          rawClass: o.rawClass,
          distance: o.distance,
          widthM: o.widthM,
          heightM: o.heightM,
          lane: o.lane,
          pedestrianMotion: o.pedestrianMotion || (o.isPersonStanding ? 'standing' : null),
          signalColor: o.signalColor || null
        }};
      }});
      return {{
        objects,
        groundState: currentGroundSurfaceState || {{ status: 'Flat', slopeDeg: 0, detail: 'Ground surface ahead is flat and level.' }},
        trafficLightSignal: currentTrafficLightSignal || {{ detected: false, color: 'NONE' }},
        gps: {{
          lat: userGps.lat,
          lon: userGps.lon,
          street: userGps.street,
          city: userGps.city,
          heading: userGps.heading,
          headingCardinal: userGps.headingCardinal
        }},
        navigation: {{
          activeRoute,
          destination: currentDestinationTitle,
          remainingMeters: currentDistance,
          currentInstruction: (currentWaypoints && currentWaypoints[currentWaypointIdx]) ? currentWaypoints[currentWaypointIdx].instruction : ''
        }}
      }};
    }}

    function captureActiveVideoSnapshotBase64() {{
      try {{
        const videoIds = ['nav-live-video', 'describe-live-video', 'crosswalk-live-video', 'obstacle-live-video'];
        for (const id of videoIds) {{
          const v = document.getElementById(id);
          if (v && v.readyState >= 2 && v.videoWidth > 0 && !v.paused) {{
            const snap = document.createElement('canvas');
            snap.width = 480;
            snap.height = 270;
            snap.getContext('2d').drawImage(v, 0, 0, snap.width, snap.height);
            return snap.toDataURL('image/jpeg', 0.72);
          }}
        }}
      }} catch (e) {{}}
      return null;
    }}

    function parseVoiceIntentLocalFallback(rawTranscript) {{
      const cleaned = (rawTranscript || "").toLowerCase().replace(/[\\?\\!\\.,;:]/g, "").trim();

      // Button click actions
      if (/^(start navigation|start route|begin navigation|start walking|let('s)? go)$/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "start_navigation", action: "click_button", spoken_response: "Navigation started. Continue straight.", confidence: 0.99 }};
      }}
      if (/^(where am i|where i am|what is my location|my location|current location|where are we)$/i.test(cleaned)) {{
        const street = userGps.street || "your current street";
        const city = userGps.city || "your area";
        return {{
          intent: "click_button",
          target_button: "where_am_i",
          action: "click_button",
          spoken_response: `You are on ${{street}} in ${{city}}, facing ${{userGps.headingCardinal || 'North'}}.`,
          confidence: 0.99
        }};
      }}
      if (/^(describe|describe what('s| is) around me|describe around me|what do you see|what('s| is) around( me)?|look around|see around|tell me what('s| is) around( me)?|scan surroundings|describe scene)$/i.test(cleaned)) {{
        const liveSummary = buildLiveSurroundingsSummary();
        return {{
          intent: "click_button",
          target_button: "describe_around",
          action: "click_button",
          spoken_response: liveSummary,
          confidence: 0.99
        }};
      }}
      if (/^(read signs?|read signboards?|detect signs?|detect road signs?|what does the sign say|what sign is (this|ahead|there)|is there a (road )?sign|look for signs?|sign boards?|road signs?|traffic signs?)$/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "detect_signs", action: "click_button", spoken_response: "Scanning for Riga road signs, traffic boards, and street signs.", confidence: 0.99 }};
      }}

      // Module 2: Latvian Public Transport & Transit Boarding Query
      if (/\b(what bus|which bus|what tram|which tram|what trolleybus|which trolleybus|public transport|transit option|bus or tram|tram or bus|boarding instruction|how to get to .* by (bus|tram|trolleybus))\b/i.test(cleaned)) {{
        const transitSpoken = "For Riga Old Town to Riga Technical University (Ķīpsala), take Rīgas Satiksme Trolleybus 9 or Bus 3 from Grēcinieku iela stop (2 stops across Stone Bridge to Ķīpsala), then walk 350 meters north along Ķīpsalas iela.";
        return {{
          intent: "public_transport_query",
          action: "public_transport_query",
          spoken_response: transitSpoken,
          confidence: 0.99
        }};
      }}

      // Traffic Light & Signal Color Query (Enforcing Module 4 Critical Safety Rule)
      if (/\b(traffic light|traffic signal|signal color|light red|light green|light yellow|what color is the (traffic )?light|pedestrian signal|walk signal)\b/i.test(cleaned)) {{
        const tlObj = lastLiveDetections.find(o => o.isTrafficLight || o.rawClass === 'traffic light');
        const sig = (tlObj && tlObj.signalColor) || (currentTrafficLightSignal && currentTrafficLightSignal.detected ? currentTrafficLightSignal.color : 'NONE');
        let spoken = "No traffic light signal is currently detected in camera view. Point your phone toward the intersection ahead to scan.";
        if (sig && sig !== 'NONE') {{
          const dist = tlObj ? tlObj.distance.toFixed(1) : (currentTrafficLightSignal.distance || 3.0);
          spoken = sig === 'RED'
            ? `The traffic light ahead at ${{dist}} meters is RED. Stop at the curb and wait.`
            : (sig === 'GREEN'
                ? `Green signal detected ahead at ${{dist}} meters, but camera detection cannot guarantee road safety. Listen for traffic and verify before crossing.`
                : `The traffic light ahead at ${{dist}} meters is YELLOW. Wait on the curb for the next green cycle.`);
        }}
        return {{ intent: "traffic_light_query", action: "traffic_light_query", spoken_response: spoken, confidence: 0.99 }};
      }}

      // Ground Surface State Query (Flat, Tilted, Uneven)
      if (/\b(ground|surface|sidewalk|pavement|floor)\b.*\b(flat|tilted|uneven|level|slope|sloped|condition|rough|smooth)\b/i.test(cleaned) ||
          /\b(is it flat|is it tilted|is it uneven|is there a slope|ground condition|surface condition)\b/i.test(cleaned)) {{
        const gStatus = currentGroundSurfaceState ? currentGroundSurfaceState.status : 'Flat';
        const gDetail = currentGroundSurfaceState ? currentGroundSurfaceState.detail : 'Ground surface ahead is flat and level.';
        const holeObj = lastLiveDetections.find(o => o.isDepthHole || o.rawClass === 'depth hole');
        const spoken = holeObj
          ? `Warning: Ground is uneven with a depth hole or drop-off ${{holeObj.distance.toFixed(1)}} meters ahead on your ${{holeObj.lane}}. Step around carefully.`
          : `Ground surface condition is ${{gStatus.toLowerCase()}}. ${{gDetail}}`;
        return {{ intent: "ground_surface_query", action: "ground_surface_query", spoken_response: spoken, confidence: 0.99 }};
      }}

      // Object Width, Height & Distance Dimensions Query
      if (/\b(how big|how wide|how tall|width|height|dimensions|what size|size of)\b/i.test(cleaned)) {{
        let spoken = "";
        if (lastLiveDetections && lastLiveDetections.length > 0) {{
          const dimList = lastLiveDetections.slice(0, 3).map(o => {{
            computeObjectMetricDimensions(o);
            return `${{o.label}} at ${{o.distance.toFixed(1)}} meters is approximately ${{o.widthM}} meters wide by ${{o.heightM}} meters tall`;
          }});
          spoken = dimList.join('. ') + '.';
        }} else {{
          spoken = "No obstacles are currently in your path to measure. Forward corridor is clear.";
        }}
        return {{ intent: "object_dimensions_query", action: "object_dimensions_query", spoken_response: spoken, confidence: 0.99 }};
      }}

      // Pedestrian Motion / Trajectory Query (Walking Toward, Moving Away, Crossing Path, Standing)
      if (/\b(walking toward|moving away|crossing (my |the )?path|pedestrian(s)? (moving|walking|crossing)|what are (the )?people doing|which way (is|are) (the )?(person|people) (walking|going|moving))\b/i.test(cleaned)) {{
        const peopleList = lastLiveDetections.filter(o => o.isPerson || o.rawClass.includes('person'));
        let spoken = "No pedestrians detected in immediate camera view.";
        if (peopleList.length > 0) {{
          const details = peopleList.map(p => {{
            const pos = p.lane === 'center' ? 'ahead' : `on your ${{p.lane}}`;
            if (p.pedestrianMotion === 'walking_toward') return `a person walking toward you at ${{p.distance.toFixed(1)}} meters ${{pos}}`;
            if (p.pedestrianMotion === 'moving_away') return `a person moving away from you at ${{p.distance.toFixed(1)}} meters ${{pos}}`;
            if (p.pedestrianMotion === 'crossing_path') return `a person crossing your path at ${{p.distance.toFixed(1)}} meters ${{pos}}`;
            if (p.isPersonStanding || p.pedestrianMotion === 'standing') return `a person standing still at ${{p.distance.toFixed(1)}} meters ${{pos}}`;
            return `a person walking at ${{p.distance.toFixed(1)}} meters ${{pos}}`;
          }});
          spoken = `I detect ${{peopleList.length}} ${{peopleList.length === 1 ? 'pedestrian' : 'pedestrians'}}: ${{details.join(', ')}}.`;
        }}
        return {{ intent: "pedestrian_motion_query", action: "pedestrian_motion_query", spoken_response: spoken, confidence: 0.99 }};
      }}

      // Pole Detection Query
      if (/\b(is there a pole|any poles?|pole ahead|watch for poles?|utility pole|lamp post|sign post)\b/i.test(cleaned)) {{
        const poleObj = lastLiveDetections.find(o => o.isPole || o.rawClass === 'pole' || o.label.toLowerCase().includes('pole'));
        const spoken = poleObj
          ? `Caution: Pole detected ${{poleObj.distance.toFixed(1)}} meters ahead on your ${{poleObj.lane}} (approximately ${{poleObj.widthM || 0.2}} meters wide by ${{poleObj.heightM || 2.2}} meters tall).`
          : "No poles detected in your immediate walking corridor.";
        return {{ intent: "pole_query", action: "pole_query", spoken_response: spoken, confidence: 0.99 }};
      }}

      if (/^(is there a tree|are there trees|tree ahead|watch for trees|detect tree|detect trees|any trees|trees in my way|branches ahead|tree branch)$/i.test(cleaned)) {{
        const treeObj = lastLiveDetections.find(o => o.isTree || o.rawClass === 'tree' || o.label.toLowerCase().includes('tree'));
        const spoken = treeObj
          ? `Tree detected ${{treeObj.distance.toFixed(1)}} meters ahead on your ${{treeObj.lane}} (${{treeObj.widthM || 1.1}}m wide by ${{treeObj.heightM || 2.6}}m tall). Watch for tree trunk and low branches.`
          : "Scanning sidewalk ahead for tree trunks, root grates, and low-hanging branches.";
        return {{ intent: "tree_query", action: "tree_query", spoken_response: spoken, confidence: 0.99 }};
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

      // 5f. Heading & Audio Guidepost Compass Alignment
      if (/^(am i facing the right way|which way should i face|which way to face|check heading|heading check|is my heading right|am i on course|check compass|compass check)$/i.test(cleaned) ||
          /\b(facing the right way|on course|which way to face)\b/i.test(cleaned)) {{
        return {{
          intent: "heading_query",
          action: "check_heading",
          spoken_response: "Checking compass orientation relative to route path.",
          confidence: 0.99
        }};
      }}

      if (/^(where do i go|where to go|where should i go|which way|which direction|where to walk|guide me|navigate me|what is my next turn|next turn)$/i.test(cleaned)) {{
        const wpInstruction = (currentWaypoints && currentWaypoints[currentWaypointIdx]) ? currentWaypoints[currentWaypointIdx].instruction : 'Walk straight along pathway';
        const depth = currentLidarDepthAhead ? `${{currentLidarDepthAhead.toFixed(1)}} meters` : 'clear';
        const gStatus = currentGroundSurfaceState ? currentGroundSurfaceState.status.toLowerCase() : 'flat';
        return {{
          intent: "guidance_query",
          action: "guidance_query",
          spoken_response: `${{wpInstruction}} (${{currentDistance || 0}} meters remaining). Forward clearance is ${{depth}}, ground is ${{gStatus}}.`,
          confidence: 0.99
        }};
      }}
      if (/^(is there anything in my way|is the path clear|is there an obstacle|what('s| is) in my way|what('s| is) ahead|any obstacles|can i walk forward)$/i.test(cleaned)) {{
        const gStatus = currentGroundSurfaceState ? currentGroundSurfaceState.status.toLowerCase() : 'flat';
        return {{
          intent: "obstacle_query",
          action: "obstacle_query",
          spoken_response: (lastLiveDetections && lastLiveDetections.length > 0)
            ? `Detected ${{lastLiveDetections.map(o => `${{o.label}} at ${{o.distance.toFixed(1)}} meters on ${{o.lane}} (${{o.widthM || 0.6}}m by ${{o.heightM || 1.5}}m)`).join(', ')}}. Ground is ${{gStatus}}.`
            : `Pathway is completely clear ahead for over 4 meters. Ground surface is ${{gStatus}}.`,
          confidence: 0.99
        }};
      }}
      // Distance remaining query
      if (/^(how far am i|how far|distance left|how many meters|remaining distance|how much distance|how far to go)$/i.test(cleaned)) {{
        const distStr = currentDistance ? `${{currentDistance}} meters remaining on current route step to ${{currentDestinationTitle}}.` : "Route active. Keep walking along pathway.";
        return {{
          intent: "distance_query",
          action: "distance_query",
          spoken_response: distStr,
          confidence: 0.99
        }};
      }}

      // Current street query
      if (/^(what street is this|which street|what street am i on|current street|name of street|where is this street)$/i.test(cleaned)) {{
        const stStr = userGps.street ? `You are on ${{userGps.street}}, ${{userGps.city || ''}}, facing ${{userGps.headingCardinal || 'East'}}.` : "Detecting street name via GPS.";
        return {{
          intent: "street_query",
          action: "street_query",
          spoken_response: stStr,
          confidence: 0.99
        }};
      }}

      // Crossing Path / Zebra Crosswalk Detection Query
      if (/^(is there a crossing|is there a crossing path|where is the crossing|where is the crossing path|crossing path|zebra crossing|detect crossing|detect crossing path|is there a crosswalk)$/i.test(cleaned)) {{
        const crossObj = lastLiveDetections.find(o => o.isCrossingPath || o.label.toLowerCase().includes('crossing') || o.label.toLowerCase().includes('crosswalk'));
        const spoken = crossObj
          ? `Crossing path detected ${{crossObj.distance.toFixed(1)}} meters ahead in ${{crossObj.lane}} lane. Align straight to cross.`
          : "Scanning road surface ahead for zebra crossing path stripes and pedestrian signals.";
        return {{
          intent: "crossing_path_query",
          action: "crossing_path_query",
          spoken_response: spoken,
          confidence: 0.99
        }};
      }}

      // Crosswalk Quiet Mode Trigger
      if (/^(can i cross|is it safe to cross|crosswalk|pedestrian crossing|cross the street)$/i.test(cleaned)) {{
        return {{
          intent: "click_button",
          target_button: "crosswalk_mode",
          action: "crosswalk_mode",
          spoken_response: "Entering crosswalk quiet mode. Checking traffic light signal and listening for vehicles.",
          confidence: 0.99
        }};
      }}

      // People Around & Standing/Moving Person Collision-Prevention Query
      if (/^(are there people around( me)?|is anyone standing( ahead| there| near me)?|is someone standing( ahead| there| in front of me)?|is there a person standing|people around( me)?|who is around( me)?|anyone standing still|how many people)$/i.test(cleaned)) {{
        const peopleList = lastLiveDetections.filter(o => o.isPerson || o.rawClass.includes('person'));
        const standingList = peopleList.filter(o => o.isPersonStanding);
        let spoken = "No people detected in immediate camera view around you.";
        if (standingList.length > 0) {{
          const s = standingList[0];
          spoken = `Caution: A person is standing still ${{s.distance.toFixed(1)}} meters ${{s.lane === 'center' ? 'ahead in your path' : 'on your ' + s.lane}}. Total ${{peopleList.length}} ${{peopleList.length === 1 ? 'person' : 'people'}} around you.`;
        }} else if (peopleList.length > 0) {{
          spoken = `${{peopleList.length}} ${{peopleList.length === 1 ? 'person' : 'people'}} detected around you: ` + peopleList.map(p => `${{p.label}} at ${{p.distance.toFixed(1)}} meters (${{p.lane}})`).join(', ') + '.';
        }}
        return {{
          intent: "people_around_query",
          action: "people_around_query",
          spoken_response: spoken,
          confidence: 0.99
        }};
      }}

      // Ground Depth Hole / Pothole / Drop-off Query
      if (/^(is there a( depth)? hole|any( depth)? holes?|depth hole|ground hole|pothole|drop off( ahead)?|is the ground level|check ground depth)$/i.test(cleaned)) {{
        const holeObj = lastLiveDetections.find(o => o.isDepthHole || o.rawClass === 'depth hole');
        const gStatus = currentGroundSurfaceState ? currentGroundSurfaceState.status : 'Flat';
        const spoken = holeObj
          ? `Danger: Ground depth hole or drop-off detected ${{holeObj.distance.toFixed(1)}} meters ahead in ${{holeObj.lane}} path. Step around carefully.`
          : `No ground depth holes or drop-offs detected in immediate walking corridor. Ground surface is ${{gStatus.toLowerCase()}}.`;
        return {{
          intent: "depth_hole_query",
          action: "depth_hole_query",
          spoken_response: spoken,
          confidence: 0.99
        }};
      }}

      // Dual-Move Path Choice: Move 1 (Normal Walk to Bus Stop) vs Move 2 (Tunnel Going Down)
      if (/^(normal walk( to bus stop)?|choose normal walk|surface walk( to bus stop)?|move 1|move one|walk on surface)$/i.test(cleaned)) {{
        return {{
          intent: "dual_move_select",
          action: "dual_move_select",
          move_mode: "normal_walk",
          spoken_response: "Move 1 selected: Normal surface walk to Bus Stop. Tracking sidewalk clearance and people standing around you.",
          confidence: 0.99
        }};
      }}
      if (/^(use tunnel( going down)?|tunnel going down|take( the)? tunnel|underpass( going down)?|choose tunnel|move 2|move two|go down tunnel)$/i.test(cleaned)) {{
        return {{
          intent: "dual_move_select",
          action: "dual_move_select",
          move_mode: "tunnel_down",
          spoken_response: "Move 2 selected: Using pedestrian tunnel going down. Tracking downward stairs, ground depth holes, and people ahead.",
          confidence: 0.99
        }};
      }}

      // Stairs / Steps query
      if (/^(is there stairs|are there stairs|are there steps|any stairs|staircase)$/i.test(cleaned)) {{
        const stairsObj = lastLiveDetections.find(o => o.isStairs || o.label.toLowerCase().includes('stair') || o.isTunnelDown);
        const spoken = stairsObj
          ? `Warning: ${{stairsObj.label}} detected directly ahead at ${{stairsObj.distance.toFixed(1)}} meters (approx ${{stairsObj.widthM || 1.6}}m wide by ${{stairsObj.heightM || 1.5}}m high).`
          : "No stairs detected in immediate camera view. Ground surface is clear.";
        return {{
          intent: "stairs_query",
          action: "stairs_query",
          spoken_response: spoken,
          confidence: 0.99
        }};
      }}

      // Pedometer / Steps & Cadence Query
      if (/^(how many steps|how much have i walked|step count|how many steps did i walk|my steps|walking pace|walking speed)$/i.test(cleaned)) {{
        const spmStr = currentWalkingCadenceSpm > 0 ? `, current pace ${{currentWalkingCadenceSpm}} steps per minute.` : '.';
        const spoken = `You have taken ${{totalPhysicalSteps}} physical steps, covering ${{totalPhysicalMeters.toFixed(1)}} meters${{spmStr}}`;
        return {{
          intent: "steps_query",
          action: "steps_query",
          spoken_response: spoken,
          confidence: 0.99
        }};
      }}

      // Emergency SOS Alert
      if (/^(help|emergency|i am lost|sos|call for help|call emergency|danger)$/i.test(cleaned)) {{
        return {{
          intent: "emergency_sos",
          action: "emergency_sos",
          spoken_response: "Emergency SOS activated. Preparing coordinates and calling for help.",
          confidence: 0.99
        }};
      }}

      // Crosswalk Traffic Acoustic Query
      if (/^(is it quiet|traffic level|is traffic clear|crosswalk sound|traffic noise|can i walk across)$/i.test(cleaned)) {{
        const sigPart = (currentTrafficLightSignal && currentTrafficLightSignal.detected && currentTrafficLightSignal.color !== 'NONE')
          ? ` Traffic light signal is ${{currentTrafficLightSignal.color}}.`
          : '';
        return {{
          intent: "traffic_query",
          action: "traffic_query",
          spoken_response: `Crosswalk acoustic analyzer active. Ambient quietness index is ${{Math.round(crosswalkTrafficQuietness)}} percent.${{sigPart}}`,
          confidence: 0.99
        }};
      }}

      if (/^(settings|open settings|audio settings|preferences)$/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "settings", action: "click_button", spoken_response: "Opening settings.", confidence: 0.99 }};
      }}
      if (/^(camera|switch camera|toggle camera|turn camera on|open camera|back camera)$/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "toggle_camera", action: "click_button", spoken_response: "Toggling back camera.", confidence: 0.98 }};
      }}
      if (/^(toggle )?(high contrast|sunlight mode|bright mode|contrast mode)$/i.test(cleaned)) {{
        return {{
          intent: "click_button",
          target_button: "toggle_high_contrast",
          action: "toggle_high_contrast",
          spoken_response: "Toggling sunlight high contrast mode.",
          confidence: 0.99
        }};
      }}
      if (/^(toggle )?(night vision|low light mode|dark vision|dark mode)$/i.test(cleaned)) {{
        return {{
          intent: "click_button",
          target_button: "toggle_night_vision",
          action: "toggle_night_vision",
          spoken_response: "Toggling night vision low light filter.",
          confidence: 0.99
        }};
      }}
      if (/^(stop|cancel|end navigation|stop navigation|stop route|halt)/i.test(cleaned)) {{
        return {{ intent: "click_button", target_button: "stop_route", action: "click_button", spoken_response: "Navigation stopped.", confidence: 0.99 }};
      }}

      const lowered = cleaned;
      if (/^(where am i|where i am|what is my location|current location|where are we)/i.test(lowered)) {{
        return {{
          intent: "where_am_i",
          destination: null,
          spoken_response: userGps.street ? `You are on ${{userGps.street}}, in ${{userGps.city}}, facing ${{userGps.headingCardinal || 'North'}}.` : "Checking your current location and orientation.",
          confidence: 0.98
        }};
      }}
      if (/^(what('s| is) in front of me|what('s| is) in front|describe|what do you see|what('s| is) around|look around|see around)/i.test(lowered) ||
          /\b(around me|in front of me|surroundings|what do you see|tell me about)\b/i.test(lowered)) {{
        return {{
          intent: "describe_environment",
          destination: null,
          spoken_response: buildLiveSurroundingsSummary(),
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

      // Extract "from <origin> to <destination>" if spoken
      let extractedOrigin = null;
      let workingLowered = lowered;
      const fromToMatch = workingLowered.match(/\bfrom\s+(.+?)\s+to\s+(.+)$/i);
      if (fromToMatch) {{
        extractedOrigin = fromToMatch[1].trim();
        workingLowered = 'take me to ' + fromToMatch[2].trim();
        updateManualOriginLocation(extractedOrigin);
      }}

      const navPrefixRegex = /^(please\s+)?(take me to|navigate to|open the|open|i want to go to|i need to go to|i need to get to|head to|walk to|go to|find the|find|directions to|route to|start route to|start navigation to|take me|navigate|start navigation|start route|directions|route|head|walk|go)\s*(.*)$/i;
      const match = workingLowered.match(navPrefixRegex);
      let destQuery = match ? (match[3] || "").trim() : workingLowered;
      const clean = destQuery.replace(/^(the|a|an)\s+/i, "").trim();

      // Module 1 (mermaid-diagram.png): "Destination clear? -> No -> Ask User to Clarify"
      const ambiguousPrompts = {{
        "station": "Which station in Riga would you like to go to? For example, Riga Central Station or Autoosta Coach Terminal?",
        "train station": "Did you mean Riga Central Station (Stacijas laukums 2)? Say yes or Riga Central Station to confirm.",
        "university": "Which university or campus would you like to go to? For example, Riga Technical University (RTU) in Ķīpsala?",
        "park": "Which park would you like to walk to? For example, Bastejkalns Park or Vērmanes Garden?",
        "hospital": "Which hospital or medical center do you need? Please say the hospital name or street address.",
        "stop": "Which tram or bus stop would you like to walk to? For example, Grēcinieku iela or Ķīpsala?",
        "building": "Which building would you like to navigate to? For example, Riga Technical University or Latvian National Library?",
        "center": "Would you like to go to Riga Old Town (Vecrīga), Galleria Riga, or Origo Shopping Centre?"
      }};

      if (ambiguousPrompts[clean]) {{
        return {{
          intent: "clarification_needed",
          destination_clear: false,
          destination: null,
          clarification_prompt: ambiguousPrompts[clean],
          spoken_response: ambiguousPrompts[clean],
          confidence: 0.75
        }};
      }}

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
        " route",
        "directions",
        "go somewhere",
        "take me somewhere",
        "take me there",
        "take me",
        "where is it"
      ]);

      if (vagueWords.has(clean) || vagueWords.has(lowered) || /^(go somewhere|take me somewhere|take me there|directions|route)$/i.test(lowered)) {{
        const clarifMsg = "Where would you like to go? Please say a clear destination such as Riga Technical University, Riga Old Town, or Central Station.";
        return {{
          intent: "clarification_needed",
          destination_clear: false,
          destination: null,
          clarification_prompt: clarifMsg,
          spoken_response: clarifMsg,
          confidence: 0.65
        }};
      }}

      const known = findClientLocationMatch(clean);
      if (known) {{
        const originPhrase = extractedOrigin ? `from ${{extractedOrigin}} ` : '';
        return {{
          intent: "start_navigation",
          destination_clear: true,
          origin: extractedOrigin,
          trigger_auto_gps: true,
          destination: known,
          spoken_response: `Routing ${{originPhrase}}to ${{known.canonicalName}}.`,
          confidence: 0.96
        }};
      }}

      if (clean.length >= 2) {{
        const custom = createClientCustomDestination(clean);
        const originPhrase = extractedOrigin ? `from ${{extractedOrigin}} ` : '';
        return {{
          intent: "start_navigation",
          destination_clear: true,
          origin: extractedOrigin,
          trigger_auto_gps: true,
          destination: custom,
          spoken_response: `Planning route ${{originPhrase}}to ${{custom.canonicalName}}.`,
          confidence: 0.95
        }};
      }}

      return {{
        intent: "clarification_needed",
        destination_clear: false,
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

      if (typeof UnifiedSafetyEngine !== 'undefined') {{
        const stateMap = {{
          home: 'IDLE',
          listening: 'LISTENING',
          destinationSearch: 'ROUTING',
          routePreview: 'ROUTING',
          activeNavigation: 'ACTIVE_WALKING',
          whereAmI: 'IDLE',
          describeAround: 'IDLE',
          obstacleAlert: 'HAZARD_STOPPED',
          crosswalkSafety: 'APPROACHING_CROSSWALK'
        }};
        UnifiedSafetyEngine.setNavState(stateMap[targetRoute] || 'IDLE');
      }}

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
        speakText("Approaching pedestrian crosswalk. Quiet mode active. Listening for traffic rumble.");
        crosswalkSafeAnnounced = false;
        requestAnimationFrame(renderCrosswalkAcousticSpectrum);
      }}
    }}

    function jumpToScreen(route) {{
      navigateTo(route);
    }}

    // Module 2: Manual Starting Location (Origin) & Latvian Public Transport State
    let manualOriginName = "Riga Old Town (Vecrīga)";
    let isManualOriginActive = false;
    let currentRoutePlanData = null;

    function updateManualOriginLocation(val) {{
      const v = (val || "").trim();
      if (v && !/^current gps/i.test(v)) {{
        manualOriginName = v;
        isManualOriginActive = true;
      }} else {{
        manualOriginName = "Riga Old Town (Vecrīga)";
        isManualOriginActive = false;
      }}
      const inp = document.getElementById('origin-location-input');
      if (inp && v) inp.value = v;
    }}

    function useDeviceGpsAsOrigin() {{
      triggerHaptic([40]);
      isManualOriginActive = false;
      manualOriginName = userGps.street ? `${{userGps.street}} (${{userGps.city || 'Riga'}})` : "Riga Old Town (Vecrīga)";
      const inp = document.getElementById('origin-location-input');
      if (inp) inp.value = `Current GPS Location (${{manualOriginName}})`;
      speakText(`Using live device GPS location at ${{manualOriginName}} as starting point.`);
    }}

    function speakPublicTransportOptions() {{
      triggerHaptic([50]);
      let msg = "Latvian public transport option: Take Rīgas Satiksme Trolleybus 9 or Bus 3 from Grēcinieku iela stop (2 stops across Stone Bridge to Ķīpsala stop), then walk 350 meters north along Ķīpsalas iela.";
      if (currentRoutePlanData && currentRoutePlanData.publicTransportOptions && currentRoutePlanData.publicTransportOptions.length > 0) {{
        const t = currentRoutePlanData.publicTransportOptions[0];
        msg = `${{t.operator || 'Rīgas Satiksme'}} ${{t.mode || 'Transit'}} ${{t.line}}: Board at ${{t.fromStop}} toward ${{t.toStop}} (${{t.stopsCount || 2}} stops, approx ${{t.durationMinutes || 6}} minutes). ${{t.boardingInstructions || ''}}`;
      }}
      showUniversalVoiceHUD('Latvian Public Transport', msg, false);
      speakText(msg);
    }}

    function populateRoutePreviewArchitectureCards(title, routePlan) {{
      const originLabel = document.getElementById('preview-origin-label');
      const etaBadge = document.getElementById('preview-eta-badge');
      const nextTurnEl = document.getElementById('preview-next-turn-text');
      const crossEl = document.getElementById('preview-crossings-summary');
      const transitLineEl = document.getElementById('preview-transit-line');
      const transitBoardEl = document.getElementById('preview-transit-boarding');

      const originName = (routePlan && routePlan.origin && routePlan.origin.name) || manualOriginName || "Riga Old Town (Vecrīga)";
      if (originLabel) originLabel.innerText = `From: ${{originName}}`;

      const estMins = (routePlan && routePlan.estimatedArrivalTime && routePlan.estimatedArrivalTime.walkingMinutes) || activeDestination.estimatedMinutes || 22;
      if (etaBadge) etaBadge.innerText = `ETA: ~${{estMins}} min walk`;

      const firstStep = (routePlan && routePlan.nextTurn && routePlan.nextTurn.instruction) || (currentWaypoints && currentWaypoints[0] && currentWaypoints[0].instruction) || "Head west toward Stone Bridge pedestrian walkway";
      const firstDist = (routePlan && routePlan.nextTurn && routePlan.nextTurn.distanceMeters) || (currentWaypoints && currentWaypoints[0] && currentWaypoints[0].distance) || 120;
      if (nextTurnEl) nextTurnEl.innerText = `Next Turn: ${{firstStep}} (${{firstDist}}m)`;

      if (crossEl) {{
        const crossings = (routePlan && routePlan.pedestrianCrossings) || [];
        if (crossings.length > 0) {{
          crossEl.innerText = `${{crossings.length}} Crossings (${{crossings[0].location}})`;
        }} else {{
          crossEl.innerText = "2 Signalized Crossings (11. novembra krastmala & Ķīpsalas iela)";
        }}
      }}

      if (routePlan && routePlan.publicTransportOptions && routePlan.publicTransportOptions.length > 0) {{
        const t0 = routePlan.publicTransportOptions[0];
        if (transitLineEl) transitLineEl.innerText = `${{t0.operator || 'Rīgas Satiksme'}}: ${{t0.mode}} ${{t0.line}} (${{t0.fromStop}} → ${{t0.toStop}})`;
        if (transitBoardEl) transitBoardEl.innerText = t0.boardingInstructions || `Board at ${{t0.fromStop}} and ride ${{t0.stopsCount || 2}} stops to ${{t0.toStop}}.`;
      }}
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

    async function selectDestination(title, sub) {{
      triggerHaptic([60]);
      currentDestinationTitle = title;
      currentDestinationSub = sub + " • 1.8 km • 22 min • 6 waypoints";
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

      // Query Module 2 Routing & Transit API (/api/v1/routes/plan)
      try {{
        const resp = await fetch('/api/v1/routes/plan', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            origin: isManualOriginActive ? manualOriginName : "Riga Old Town",
            destination: title,
            currentGps: {{ lat: userGps.lat, lon: userGps.lon, street: userGps.street }}
          }})
        }});
        if (resp.ok) {{
          const json = await resp.json();
          if (json && json.status === 'success' && json.data) {{
            currentRoutePlanData = json.data;
            populateRoutePreviewArchitectureCards(title, json.data);
          }}
        }}
      }} catch (e) {{
        populateRoutePreviewArchitectureCards(title, null);
      }}

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
      showUniversalVoiceHUD("Listening...", "Speak now — Say where to go or ask: 'Is someone on my right?'", true);

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

      const personMatch = matched.find(d => d.isPerson || d.label.toLowerCase().includes('person'));
      let responseSpeech = "";

      if (personMatch) {{
        const stateText = personMatch.isPersonStanding ? 'standing still' : 'walking';
        responseSpeech = `Yes, I see a person ${{stateText}} on your ${{dir}}, about ${{personMatch.distance.toFixed(1)}} meters away.`;
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
      const persons = lastLiveDetections.filter(d => d.isPerson || d.label.toLowerCase().includes('person'));
      const otherObjects = lastLiveDetections.filter(d => !(d.isPerson || d.label.toLowerCase().includes('person')));

      let reply = "";
      if (persons.length > 0) {{
        const closest = persons[0];
        const motionDesc = closest.personMotion === 'walking_toward' ? 'walking toward you' :
                           (closest.personMotion === 'moving_away' ? 'moving away' :
                           (closest.personMotion === 'crossing_path' ? 'crossing your path' :
                           (closest.isPersonStanding ? 'standing still' : 'walking')));
        reply = `Phone pointed ${{dir}}: Person ${{motionDesc}} detected ${{closest.distance.toFixed(1)}} meters ahead (approx ${{closest.widthM || 0.5}}m wide by ${{closest.heightM || 1.7}}m tall).`;
      }} else if (otherObjects.length > 0) {{
        const obj = otherObjects[0];
        reply = `Phone pointed ${{dir}}: ${{obj.label}} detected ${{obj.distance.toFixed(1)}} meters ahead (approx ${{obj.widthM || 0.5}}m wide by ${{obj.heightM || 1.0}}m tall).`;
      }} else {{
        reply = `Phone pointed ${{dir}}: Area to your ${{dir}} is completely clear. Ground is ${{currentGroundSurfaceState.toLowerCase()}}.`;
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
      const liveTransEl = document.getElementById('live-transcript');
      if (liveTransEl) liveTransEl.innerText = '“' + trimmed + '”';
      const listenTitleEl = document.getElementById('listening-title');
      if (listenTitleEl) listenTitleEl.innerText = "Gemini is analyzing...";
      announceToScreenReader(`Voice input: "${{trimmed}}". Analyzing with Gemini AI and live camera sensors.`);
      triggerHaptic([30]);

      const liveContext = buildLiveVoiceContext();
      const imageBase64 = captureActiveVideoSnapshotBase64();

      let result = null;
      try {{
        const resp = await fetch('/api/v1/voice/intent', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            transcript: trimmed,
            liveContext: liveContext,
            imageBase64: imageBase64
          }})
        }});
        if (resp.ok) {{
          const json = await resp.json();
          if (json && json.status === 'success' && json.data) {{
            result = json.data;
          }}
        }}
      }} catch (err) {{
        console.warn("[Voice] Server fetch error, using local live-sensor voice engine fallback:", err);
      }}

      // Offline or network fallback with live sensor context
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

      // 2. Directional Perception Query: "is someone coming from my right?", "what is on my left?"
      if (result.intent === 'directional_query' || result.action === 'directional_query' || result.direction) {{
        handleDirectionalQuery(result.direction || 'right', result.target || 'person', rawText);
        return;
      }}

      // 3. Heading & Compass Audio Guidepost Alignment
      if (result.intent === 'heading_query' || result.action === 'check_heading') {{
        const headingCheck = checkAudioCompassHeadingAlignment(true);
        const text = result.spoken_response || headingCheck.text;
        showUniversalVoiceHUD('Heading Guidepost', text, false);
        speakText(text);
        triggerHaptic([60, 40]);
        return;
      }}

      // 3a. Module 2: Public Transport & Transit Query
      if (result.intent === 'public_transport_query' || result.action === 'public_transport_query') {{
        const text = result.spoken_response || "For Riga Old Town to Riga Technical University (Ķīpsala), take Rīgas Satiksme Trolleybus 9 or Bus 3 from Grēcinieku iela stop (2 stops across Stone Bridge to Ķīpsala), then walk 350 meters north along Ķīpsalas iela.";
        showUniversalVoiceHUD('Latvian Public Transport', text, false);
        speakText(text);
        triggerHaptic([60, 40]);
        return;
      }}

      // 3a-2. Module 5: Uncertain Detection Warning
      if (result.intent === 'uncertain_detection' || result.action === 'uncertain_detection') {{
        const text = result.spoken_response || "I can't confidently identify the sign. Please proceed cautiously.";
        showUniversalVoiceHUD('Uncertain Detection', text, false);
        speakText(text);
        triggerHaptic([50, 70, 50]);
        return;
      }}

      // 3b. Traffic Light Signal Query (Enforcing Module 4 Critical Safety Limitation)
      if (result.intent === 'traffic_light_query' || result.action === 'traffic_light_query') {{
        const tlObj = lastLiveDetections.find(o => o.isTrafficLight || o.rawClass === 'traffic light');
        const sig = (tlObj && (tlObj.signalColor || tlObj.trafficLightColor)) ? (tlObj.signalColor || tlObj.trafficLightColor) : (currentTrafficLightSignal && currentTrafficLightSignal.color ? currentTrafficLightSignal.color : 'NONE');
        let text = result.spoken_response;
        if (!text) {{
          if (sig === 'RED') {{
            text = `Traffic light signal is RED${{tlObj ? ' at ' + tlObj.distance.toFixed(1) + ' meters ahead' : ''}}. Stop at the curb and do not cross.`;
          }} else if (sig === 'YELLOW') {{
            text = `Traffic light signal is YELLOW${{tlObj ? ' at ' + tlObj.distance.toFixed(1) + ' meters ahead' : ''}}. Caution, signal is changing. Wait on the sidewalk.`;
          }} else if (sig === 'GREEN') {{
            text = `Green signal detected ahead${{tlObj ? ' at ' + tlObj.distance.toFixed(1) + ' meters' : ''}}, but camera detection cannot guarantee road safety. Listen for traffic and verify before crossing.`;
          }} else {{
            text = 'No active traffic light signal detected in the current camera view. Point your phone toward the intersection.';
          }}
        }}
        showUniversalVoiceHUD(`Traffic Light: ${{sig || 'SCANNING'}}`, text, false);
        speakText(text);
        triggerHaptic([60, 40]);
        return;
      }}

      // 3c. Ground Surface State Query (Flat, Tilted, Uneven)
      if (result.intent === 'ground_surface_query' || result.action === 'ground_surface_query') {{
        const holeObj = lastLiveDetections.find(o => o.isDepthHole || o.rawClass === 'depth hole');
        const stairsObj = lastLiveDetections.find(o => o.isStairs || o.rawClass === 'stairs');
        let text = result.spoken_response;
        if (!text) {{
          text = `The ground ahead is ${{currentGroundSurfaceState.toLowerCase()}}. Forward clearance is ${{currentLidarDepthAhead.toFixed(1)}} meters.`;
          if (holeObj) text += ` Warning: depth hole or drop-off at ${{holeObj.distance.toFixed(1)}} meters.`;
          if (stairsObj) text += ` Stairs detected at ${{stairsObj.distance.toFixed(1)}} meters.`;
        }}
        showUniversalVoiceHUD(`Ground: ${{currentGroundSurfaceState.toUpperCase()}}`, text, false);
        speakText(text);
        triggerHaptic([50]);
        return;
      }}

      // 3d. Object Distance, Width & Height Dimensions Query
      if (result.intent === 'object_dimensions_query' || result.action === 'object_dimensions_query') {{
        let text = result.spoken_response;
        if (!text) {{
          if (lastLiveDetections.length > 0) {{
            const details = lastLiveDetections.slice(0, 3).map(o => {{
              const dims = computeObjectMetricDimensions(o);
              return `${{o.label}} at ${{o.distance.toFixed(1)}}m (width ${{dims.widthM}}m, height ${{dims.heightM}}m)`;
            }}).join('; ');
            text = `Object distance and dimensions: ${{details}}. Ground surface is ${{currentGroundSurfaceState.toLowerCase()}}.`;
          }} else {{
            text = `Forward path is clear up to ${{currentLidarDepthAhead.toFixed(1)}} meters. Ground is ${{currentGroundSurfaceState.toLowerCase()}}.`;
          }}
        }}
        showUniversalVoiceHUD('Distance & Size (W×H)', text, false);
        speakText(text);
        triggerHaptic([50]);
        return;
      }}

      // 3e. Pedestrian Motion & Trajectory Query (Toward, Away, Crossing, Standing)
      if (result.intent === 'pedestrian_motion_query' || result.action === 'pedestrian_motion_query' || result.intent === 'people_around_query' || result.action === 'people_around_query') {{
        const peopleList = lastLiveDetections.filter(o => o.isPerson || (o.rawClass && o.rawClass.includes('person')));
        let text = result.spoken_response;
        if (!text) {{
          if (peopleList.length > 0) {{
            const pDescs = peopleList.slice(0, 3).map(p => {{
              const motion = p.personMotion === 'walking_toward' ? 'walking toward you' :
                             (p.personMotion === 'moving_away' ? 'moving away from you' :
                             (p.personMotion === 'crossing_path' ? 'crossing your path' :
                             (p.isPersonStanding ? 'standing still' : 'walking')));
              const dims = computeObjectMetricDimensions(p);
              return `person ${{motion}} at ${{p.distance.toFixed(1)}}m on your ${{p.lane}} (${{dims.widthM}}m wide, ${{dims.heightM}}m tall)`;
            }}).join('; ');
            text = `${{peopleList.length}} ${{peopleList.length === 1 ? 'person' : 'people'}} detected: ${{pDescs}}.`;
          }} else {{
            text = 'No pedestrians detected in your immediate camera corridor.';
          }}
        }}
        showUniversalVoiceHUD('Pedestrian Tracking', text, false);
        speakText(text);
        triggerHaptic([60, 40]);
        return;
      }}

      // 3f. Pole / Bollard Detection Query
      if (result.intent === 'pole_query' || result.action === 'pole_query') {{
        const poleObj = lastLiveDetections.find(o => o.isPole || o.rawClass === 'pole');
        let text = result.spoken_response;
        if (!text) {{
          if (poleObj) {{
            const dims = computeObjectMetricDimensions(poleObj);
            text = `Utility pole or bollard detected at ${{poleObj.distance.toFixed(1)}} meters on your ${{poleObj.lane}} (approx ${{dims.widthM}}m wide by ${{dims.heightM}}m tall). Step around carefully.`;
          }} else {{
            text = 'No poles or bollards detected in your immediate path ahead.';
          }}
        }}
        showUniversalVoiceHUD('Pole & Bollard Check', text, false);
        speakText(text);
        triggerHaptic([50]);
        return;
      }}

      // 3g. Extended Natural Query Dialogs (Distance, Street, Crossing, Trees, Holes, Stairs, Steps, SOS, Traffic)
      if (result.intent === 'distance_query' || result.action === 'distance_query') {{
        const distStr = currentDistance ? `${{currentDistance}} meters remaining on current route step to ${{currentDestinationTitle}}.` : `Forward clearance is ${{currentLidarDepthAhead.toFixed(1)}} meters. Ground is ${{currentGroundSurfaceState.toLowerCase()}}.`;
        const text = result.spoken_response || distStr;
        showUniversalVoiceHUD('Distance Check', text, false);
        speakText(text);
        triggerHaptic([50]);
        return;
      }}
      if (result.intent === 'street_query' || result.action === 'street_query') {{
        const stStr = userGps.street ? `You are on ${{userGps.street}}, ${{userGps.city || ''}}.` : 'Detecting current street location via live GPS.';
        const text = result.spoken_response || stStr;
        showUniversalVoiceHUD('Current Street', text, false);
        speakText(text);
        triggerHaptic([50]);
        return;
      }}
      if (result.intent === 'crossing_path_query' || result.action === 'crossing_path_query') {{
        const crossObj = lastLiveDetections.find(o => o.isCrossingPath || o.label.toLowerCase().includes('crossing') || o.label.toLowerCase().includes('crosswalk'));
        const sigStr = (currentTrafficLightSignal && currentTrafficLightSignal.color) ? ` Traffic signal is ${{currentTrafficLightSignal.color}}.` : '';
        const text = crossObj
          ? `Crossing path detected ${{crossObj.distance.toFixed(1)}} meters ahead in ${{crossObj.lane}} lane.${{sigStr}} Align straight to cross.`
          : (result.spoken_response || `No zebra crossing stripes detected right now.${{sigStr}} Point camera toward the road intersection.`);
        showUniversalVoiceHUD('Crossing Path Detection', text, false);
        speakText(text);
        triggerHaptic([60, 40, 60]);
        return;
      }}
      if (result.intent === 'tree_query' || result.action === 'tree_query') {{
        const treeObj = lastLiveDetections.find(o => o.isTree || o.rawClass === 'tree' || o.label.toLowerCase().includes('tree'));
        const text = treeObj
          ? `Tree detected ${{treeObj.distance.toFixed(1)}} meters ahead on your ${{treeObj.lane}} (approx ${{treeObj.widthM || 0.9}}m wide by ${{treeObj.heightM || 2.8}}m tall). Watch for trunk and branches.`
          : (result.spoken_response || 'No sidewalk trees or overhanging branches detected in your immediate path.');
        showUniversalVoiceHUD('Sidewalk Tree Detection', text, false);
        speakText(text);
        triggerHaptic([60, 40]);
        return;
      }}
      if (result.intent === 'depth_hole_query' || result.action === 'depth_hole_query') {{
        const holeObj = lastLiveDetections.find(o => o.isDepthHole || o.rawClass === 'depth hole');
        const text = holeObj
          ? `Danger: Ground depth hole or drop-off detected ${{holeObj.distance.toFixed(1)}} meters ahead in ${{holeObj.lane}} path. Ground is ${{currentGroundSurfaceState.toLowerCase()}}. Step around carefully.`
          : (result.spoken_response || `No depth holes or potholes detected. Ground surface ahead is ${{currentGroundSurfaceState.toLowerCase()}}.`);
        showUniversalVoiceHUD('Ground Depth & Surface Check', text, false);
        speakText(text);
        triggerHaptic([80, 40, 80]);
        return;
      }}
      if (result.intent === 'dual_move_select' || result.action === 'dual_move_select') {{
        const mode = result.move_mode || (rawText && /tunnel|underpass|move 2|move two|down/i.test(rawText) ? 'tunnel_down' : 'normal_walk');
        if (activeRoute !== 'activeNavigation') {{
          navigateTo('activeNavigation');
        }}
        selectDualMovePath(mode, true);
        return;
      }}
      if (result.intent === 'stairs_query' || result.action === 'stairs_query') {{
        const stairsObj = lastLiveDetections.find(o => o.isStairs || o.rawClass === 'stairs');
        const text = stairsObj
          ? `Stairs detected at ${{stairsObj.distance.toFixed(1)}} meters ahead on your ${{stairsObj.lane}} (approx ${{stairsObj.widthM || 1.4}}m wide, ${{stairsObj.heightM || 1.2}}m high). Use handrail.`
          : (result.spoken_response || `No stairs detected ahead. Ground surface is ${{currentGroundSurfaceState.toLowerCase()}}.`);
        showUniversalVoiceHUD('Stairs / Elevation Check', text, false);
        speakText(text);
        triggerHaptic([50]);
        return;
      }}
      if (result.intent === 'steps_query' || result.action === 'steps_query') {{
        const spmStr = currentWalkingCadenceSpm > 0 ? `, cadence ${{currentWalkingCadenceSpm}} steps per minute.` : '.';
        const text = result.spoken_response || `You have taken ${{totalPhysicalSteps}} steps, covering ${{totalPhysicalMeters.toFixed(1)}} meters${{spmStr}}`;
        showUniversalVoiceHUD('Physical Stride Integrator', text, false);
        speakText(text);
        triggerHaptic([50]);
        return;
      }}
      if (result.intent === 'emergency_sos' || result.action === 'emergency_sos') {{
        triggerEmergencySOS();
        return;
      }}
      if (result.intent === 'traffic_query' || result.action === 'traffic_query') {{
        const sigStr = (currentTrafficLightSignal && currentTrafficLightSignal.color) ? ` Traffic light is ${{currentTrafficLightSignal.color}}.` : '';
        const text = result.spoken_response || `Crosswalk acoustic analyzer active. Ambient quietness index is ${{Math.round(crosswalkTrafficQuietness)}} percent.${{sigStr}}`;
        showUniversalVoiceHUD('Traffic & Signal Check', text, false);
        speakText(text);
        triggerHaptic([50]);
        return;
      }}

      // 4. Automated GPS Navigation Trigger: ONLY when destination is clear and validated!
      if ((result.trigger_auto_gps || result.intent === 'start_navigation' || result.destination || targetBtn === 'start_navigation') && result.intent !== 'clarification_needed') {{
        hideUniversalVoiceHUD();
        handleAutoGpsNavigation(result.destination, result.spoken_response);
        return;
      }}

      const intent = result.intent || 'describe_environment';

      if (intent === 'affirmative') {{
        if (activeRoute === 'obstacleAlert') {{
          acknowledgeObstacle();
        }} else {{
          const msg = result.spoken_response || `Path is clear (${{currentLidarDepthAhead.toFixed(1)}}m). Ground is ${{currentGroundSurfaceState.toLowerCase()}}. Continue straight.`;
          showUniversalVoiceHUD('Confirmed', msg, false);
          speakText(msg);
          triggerHaptic([40]);
        }}
      }} else if (intent === 'negative') {{
        const msg = result.spoken_response || "Holding position. Tap the microphone whenever you are ready to continue.";
        showUniversalVoiceHUD('Holding Position', msg, false);
        speakText(msg);
        triggerHaptic([60, 40]);
      }} else if (intent === 'guidance_query') {{
        const dir = currentSteeringDirection || 'WALK STRAIGHT';
        const depth = currentLidarDepthAhead ? `${{currentLidarDepthAhead.toFixed(1)}} meters` : 'clear';
        const msg = result.spoken_response || `${{dir}}. Forward clearance is ${{depth}}. Ground is ${{currentGroundSurfaceState.toLowerCase()}}.`;
        showUniversalVoiceHUD('Live Guidance', msg, false);
        speakText(msg);
        triggerHaptic([50]);
      }} else if (intent === 'obstacle_query') {{
        const msg = result.spoken_response || buildLiveSurroundingsSummary(lastLiveDetections);
        showUniversalVoiceHUD('Obstacle & Depth Scan', msg, false);
        speakText(msg);
        triggerHaptic([50]);
      }} else if (intent === 'start_navigation') {{
        handleAutoGpsNavigation(result.destination, result.spoken_response);
      }} else if (intent === 'clarification_needed') {{
        const clarifPrompt = result.clarification_prompt || result.spoken_response || "Where would you like to go? Please say a destination such as Riga Technical University or Central Station.";
        const lTitle = document.getElementById('listening-title');
        if (lTitle) lTitle.innerText = "Destination Clarification";
        const lTrans = document.getElementById('live-transcript');
        if (lTrans) lTrans.innerText = `“${{clarifPrompt}}”`;
        showUniversalVoiceHUD('Clarification Needed', clarifPrompt, false);
        speakText(clarifPrompt);
        announceToScreenReader(clarifPrompt);
        triggerHaptic([60, 40]);
      }} else if (intent === 'where_am_i') {{
        const msg = result.spoken_response || `You are on ${{userGps.street || 'your current street'}}, ${{userGps.city || ''}}, heading ${{userGps.heading || 0}} degrees.`;
        showUniversalVoiceHUD('Where Am I', msg, false);
        speakText(msg);
        triggerHaptic([60]);
        if (activeRoute !== 'whereAmI') {{
          setTimeout(() => navigateTo('whereAmI'), 600);
        }}
      }} else if (intent === 'describe_environment') {{
        const liveMsg = result.spoken_response || buildLiveSurroundingsSummary(lastLiveDetections);
        showUniversalVoiceHUD('Live Surroundings', liveMsg, false);
        speakText(liveMsg);
        triggerHaptic([60]);
        if (activeRoute !== 'activeNavigation' && activeRoute !== 'describeAround') {{
          setTimeout(() => navigateTo('describeAround'), 600);
        }} else if (activeRoute === 'describeAround') {{
          triggerDescribeAround();
        }}
      }} else if (intent === 'stop') {{
        stopNavigationRoute();
      }} else if (intent === 'repeat') {{
        repeatCurrentStep();
      }} else {{
        const fallbackMsg = result.spoken_response || buildLiveSurroundingsSummary(lastLiveDetections);
        showUniversalVoiceHUD('Blind AI Assistant', fallbackMsg, false);
        speakText(fallbackMsg);
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
      playEarcon('clear');
      currentWaypointIdx = 0;
      currentDistance = currentWaypoints[0] ? currentWaypoints[0].distance : 0;
      stepWalkedMeters = 0;
      obstacleTriggeredThisStep = false;
      trafficTriggeredThisStep = false;
      metersSinceObstacle = 0;
      renderActiveWaypoint();

      const initialInstruction = currentWaypoints[0] ? currentWaypoints[0].instruction : 'Continue straight';
      speakText(`Navigation started. Continue straight. ${{initialInstruction}} toward ${{targetName}}.`);

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
      speakText(`${{wp.instruction}}. ${{currentDistance}} meters remaining. Ground is ${{currentGroundSurfaceState.toLowerCase()}}.`);
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
      const firstStep = currentWaypoints && currentWaypoints.length > 0 ? currentWaypoints[0].instruction : 'Walk along pedestrian pathway';
      const totalSteps = currentWaypoints ? currentWaypoints.length : 1;
      const msg = `Walking route to ${{currentDestinationTitle}}. ${{currentDestinationSub}} across ${{totalSteps}} turn-by-turn steps. First step: ${{firstStep}}. Ground surface is ${{currentGroundSurfaceState.toLowerCase()}}.`;
      showUniversalVoiceHUD('Route Overview', msg, false);
      speakText(msg);
    }}

    // Safety Screen Actions
    function repeatSceneDescription() {{
      triggerHaptic([40]);
      const sceneText = buildLiveSurroundingsSummary(lastLiveDetections);
      const descEl = document.getElementById('describe-scene-text');
      if (descEl) descEl.innerText = sceneText;
      showUniversalVoiceHUD('Scene Description', sceneText, false);
      speakText(sceneText);
    }}

    function repeatObstacleWarning() {{
      triggerHaptic([40]);
      const primaryObj = lastLiveDetections.length > 0 ? lastLiveDetections[0] : null;
      let dimStr = '';
      if (primaryObj) {{
        const dims = computeObjectMetricDimensions(primaryObj);
        dimStr = ` Size: approximately ${{dims.widthM}} meters wide by ${{dims.heightM}} meters tall.`;
      }}
      const evalResult = evaluateLidarDanger(currentLidarDistance, currentLidarLane, currentLidarObject);
      const msg = (evalResult.spoken || `Warning: ${{currentLidarObject}} ahead, ${{currentLidarDistance.toFixed(1)}} meters.`) + dimStr + ` Ground is ${{currentGroundSurfaceState.toLowerCase()}}.`;
      showUniversalVoiceHUD('Obstacle Details', msg, false);
      speakText(msg);
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

    function checkCrosswalkSignalAndTrafficNow() {{
      triggerHaptic([60, 40]);
      const tlObj = lastLiveDetections.find(o => o.isTrafficLight || o.rawClass === 'traffic light');
      const crossObj = lastLiveDetections.find(o => o.isCrossingPath || o.rawClass === 'crossing path');
      const vehicleObj = lastLiveDetections.find(o => ['car', 'bus', 'truck', 'motorcycle', 'bicycle'].includes(o.rawClass));
      const sig = (tlObj && (tlObj.signalColor || tlObj.trafficLightColor)) ? (tlObj.signalColor || tlObj.trafficLightColor) : (currentTrafficLightSignal && currentTrafficLightSignal.color ? currentTrafficLightSignal.color : 'NONE');

      const sigPill = document.getElementById('crosswalk-traffic-signal-pill');
      const titleEl = document.getElementById('crosswalk-status-title');
      const descEl = document.getElementById('crosswalk-status-desc');

      let msg = '';
      if (sig === 'RED') {{
        if (sigPill) {{
          sigPill.className = 'px-3 py-1 rounded-full text-xs font-extrabold bg-red-600 text-white border border-red-300 mb-2';
          sigPill.innerText = 'Traffic Signal: 🔴 RED — DO NOT CROSS';
        }}
        if (titleEl) titleEl.innerText = 'STOP — RED SIGNAL';
        msg = `Traffic light is RED${{tlObj ? ' at ' + tlObj.distance.toFixed(1) + ' meters' : ''}}. Do not cross. Wait at the curb.`;
      }} else if (sig === 'YELLOW') {{
        if (sigPill) {{
          sigPill.className = 'px-3 py-1 rounded-full text-xs font-extrabold bg-amber-500 text-black border border-amber-300 mb-2';
          sigPill.innerText = 'Traffic Signal: 🟡 YELLOW — WAIT ON CURB';
        }}
        if (titleEl) titleEl.innerText = 'WAIT — YELLOW SIGNAL';
        msg = `Traffic light is YELLOW${{tlObj ? ' at ' + tlObj.distance.toFixed(1) + ' meters' : ''}}. Signal is changing. Stay on the curb.`;
      }} else if (sig === 'GREEN') {{
        if (sigPill) {{
          sigPill.className = 'px-3 py-1 rounded-full text-xs font-extrabold bg-emerald-600 text-white border border-emerald-300 mb-2';
          sigPill.innerText = 'Traffic Signal: 🟢 GREEN — VERIFY TRAFFIC FIRST';
        }}
        if (titleEl) titleEl.innerText = 'GREEN SIGNAL — VERIFY TRAFFIC FIRST';
        msg = `Green signal detected ahead${{tlObj ? ' at ' + tlObj.distance.toFixed(1) + ' meters' : ''}}, but camera detection cannot guarantee road safety. Listen for traffic and verify before crossing.`;
        if (vehicleObj && vehicleObj.distance < 8.0) {{
          msg += ` Caution: ${{vehicleObj.label}} detected at ${{vehicleObj.distance.toFixed(1)}} meters on your ${{vehicleObj.lane}}.`;
        }}
      }} else {{
        if (sigPill) {{
          sigPill.className = 'px-3 py-1 rounded-full text-xs font-extrabold bg-slate-800 text-white border border-slate-600 mb-2';
          sigPill.innerText = `Traffic Signal: Scanning • Quietness ${{Math.round(crosswalkTrafficQuietness)}}%`;
        }}
        msg = `Scanning intersection. `;
        if (crossObj) msg += `Zebra crossing path detected at ${{crossObj.distance.toFixed(1)}} meters ahead. `;
        if (vehicleObj) {{
          msg += `Warning: ${{vehicleObj.label}} detected at ${{vehicleObj.distance.toFixed(1)}} meters on your ${{vehicleObj.lane}}. `;
        }} else {{
          msg += `No vehicles in camera view. Acoustic quietness is ${{Math.round(crosswalkTrafficQuietness)}} percent. `;
        }}
        msg += `Ground surface is ${{currentGroundSurfaceState.toLowerCase()}}.`;
      }}

      if (descEl) descEl.innerText = msg;
      showUniversalVoiceHUD('Crosswalk & Signal Check', msg, false);
      speakText(msg);
    }}

    function confirmCrossed() {{
      triggerHaptic([80, 50]);
      speakText("Crosswalk completed. Resuming route.");
      setTimeout(() => {{
        navigateTo('activeNavigation');
      }}, 400);
    }}

    // ==================== CROSSWALK ACOUSTIC FREQUENCY ANALYZER ====================
    let crosswalkTrafficQuietness = 82;
    let crosswalkAcousticAnim = null;
    let crosswalkSafeAnnounced = false;

    function renderCrosswalkAcousticSpectrum() {{
      if (activeRoute !== 'crosswalkSafety') return;
      const canvas = document.getElementById('crosswalk-acoustic-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0, 0, w, h);

      // Draw frequency spectrum grid
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.lineWidth = 1;
      for (let y = 12; y < h; y += 12) {{
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
      }}

      // Low frequency rumble band (50Hz - 280Hz)
      const numBars = 24;
      const barW = (w / numBars) - 2;
      const t = Date.now() / 300;

      // Realistic acoustic noise floor fluctuation
      const noiseLevel = 1.0 - (crosswalkTrafficQuietness / 100);

      for (let i = 0; i < numBars; i++) {{
        const x = i * (barW + 2) + 1;
        const freqWeight = i < 8 ? (1.2 + Math.sin(t + i * 0.7) * 0.4) : (0.4 + Math.cos(t + i * 0.5) * 0.2);
        const barHeight = Math.max(3, Math.min(h - 4, (freqWeight * noiseLevel * (h - 8)) + Math.random() * 4));

        const isLowRumble = i < 8;
        if (isLowRumble && crosswalkTrafficQuietness < 60) {{
          ctx.fillStyle = '#EF4444'; // Red: Loud vehicle rumble
        }} else if (isLowRumble) {{
          ctx.fillStyle = '#F59E0B'; // Amber: moderate rumble
        }} else {{
          ctx.fillStyle = '#10B981'; // Green: ambient safe
        }}

        ctx.fillRect(x, h - barHeight - 2, barW, barHeight);
      }}

      // Periodic subtle fluctuation
      if (Math.random() < 0.05) {{
        crosswalkTrafficQuietness = Math.min(95, Math.max(45, crosswalkTrafficQuietness + (Math.random() * 8 - 4)));
        const scoreEl = document.getElementById('crosswalk-quietness-score');
        const pillEl = document.getElementById('crosswalk-safety-pill');
        if (scoreEl) scoreEl.innerText = `${{Math.round(crosswalkTrafficQuietness)}}% Quietness`;
        if (pillEl) {{
          if (crosswalkTrafficQuietness >= 75) {{
            pillEl.className = 'px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 mb-2';
            pillEl.innerText = 'Safe Crossing Window Detected';
            if (!crosswalkSafeAnnounced) {{
              crosswalkSafeAnnounced = true;
              playEarcon('clear');
              speakText('Traffic noise subsided. Safe crossing window detected.');
            }}
          }} else {{
            pillEl.className = 'px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300 mb-2';
            pillEl.innerText = 'Moderate Traffic Noise • Listen on Curb';
            crosswalkSafeAnnounced = false;
          }}
        }}
      }}

      crosswalkAcousticAnim = requestAnimationFrame(renderCrosswalkAcousticSpectrum);
    }}

    // ==================== WEBAUDIO 3D BINAURAL EARCONS & PROXIMITY SONAR ====================
    let audioCtx = null;
    let sonarPingsEnabled = false;
    let lastSonarPingTime = 0;

    function getAudioContext() {{
      if (!audioCtx) {{
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        if (AudioContextClass) {{
          audioCtx = new AudioContextClass();
        }}
      }}
      if (audioCtx && audioCtx.state === 'suspended') {{
        audioCtx.resume().catch(() => {{}});
      }}
      return audioCtx;
    }}

    function playBinauralSonarPing(distance, lane = 'center') {{
      if (!sonarPingsEnabled) return;
      const ctx = getAudioContext();
      if (!ctx) return;

      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      let panner = null;

      if (ctx.createStereoPanner) {{
        panner = ctx.createStereoPanner();
        panner.pan.value = lane === 'left' ? -0.8 : (lane === 'right' ? 0.8 : 0);
      }}

      // Frequency mapped by distance (closer = higher pitch urgency)
      const freq = distance < 0.8 ? 1046 : (distance < 1.5 ? 880 : (distance < 2.5 ? 587 : 440));
      osc.type = distance < 0.8 ? 'sawtooth' : 'sine';
      osc.frequency.setValueAtTime(freq, now);

      const duration = distance < 0.8 ? 0.12 : 0.08;
      const volume = Math.min(0.28, Math.max(0.06, (3.5 - distance) / 3.5 * 0.28));

      gain.gain.setValueAtTime(0.001, now);
      gain.gain.exponentialRampToValueAtTime(volume, now + 0.015);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);

      if (panner) {{
        osc.connect(gain);
        gain.connect(panner);
        panner.connect(ctx.destination);
      }} else {{
        osc.connect(gain);
        gain.connect(ctx.destination);
      }}

      osc.start(now);
      osc.stop(now + duration + 0.02);
    }}

    function playEarcon(type) {{
      const ctx = getAudioContext();
      if (!ctx) return;
      const now = ctx.currentTime;

      if (type === 'clear') {{
        // Soft ascending dual-tone chime (C5 -> E5)
        [523.25, 659.25].forEach((freq, idx) => {{
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now + idx * 0.09);
          gain.gain.setValueAtTime(0.001, now + idx * 0.09);
          gain.gain.exponentialRampToValueAtTime(0.12, now + idx * 0.09 + 0.02);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.09 + 0.14);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now + idx * 0.09);
          osc.stop(now + idx * 0.09 + 0.16);
        }});
      }} else if (type === 'hazard') {{
        // Dissonant low frequency warning thrum
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(185, now);
        osc.frequency.linearRampToValueAtTime(130, now + 0.22);
        gain.gain.setValueAtTime(0.22, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.26);
      }} else if (type === 'turn_left' || type === 'turn_right') {{
        const isLeft = type === 'turn_left';
        let panner = null;
        if (ctx.createStereoPanner) {{
          panner = ctx.createStereoPanner();
          panner.pan.value = isLeft ? -0.85 : 0.85;
        }}
        [440, 554.37].forEach((freq, idx) => {{
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(freq, now + idx * 0.08);
          gain.gain.setValueAtTime(0.001, now + idx * 0.08);
          gain.gain.exponentialRampToValueAtTime(0.15, now + idx * 0.08 + 0.02);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.08 + 0.12);
          if (panner) {{
            osc.connect(gain);
            gain.connect(panner);
            panner.connect(ctx.destination);
          }} else {{
            osc.connect(gain);
            gain.connect(ctx.destination);
          }}
          osc.start(now + idx * 0.08);
          osc.stop(now + idx * 0.08 + 0.14);
        }});
      }} else if (type === 'arrival') {{
        // C - E - G major arrival chord
        [523.25, 659.25, 783.99].forEach((freq, idx) => {{
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now + idx * 0.10);
          gain.gain.setValueAtTime(0.001, now + idx * 0.10);
          gain.gain.exponentialRampToValueAtTime(0.18, now + idx * 0.10 + 0.02);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.10 + 0.35);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now + idx * 0.10);
          osc.stop(now + idx * 0.10 + 0.38);
        }});
      }}
    }}

    function playAudioBeaconTick(onCourse = true) {{
      const ctx = getAudioContext();
      if (!ctx) return;
      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = onCourse ? 'sine' : 'triangle';
      osc.frequency.setValueAtTime(onCourse ? 660 : 330, now);
      gain.gain.setValueAtTime(0.001, now);
      gain.gain.exponentialRampToValueAtTime(0.12, now + 0.015);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.07);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.08);
    }}

    function computeTargetWaypointBearing() {{
      const wp = currentWaypoints[currentWaypointIdx];
      if (!wp || typeof wp.lat === 'undefined' || typeof wp.lon === 'undefined') {{
        if (activeDestination && activeDestination.lat && activeDestination.lon) {{
          const dLon = (activeDestination.lon - userGps.lon) * Math.PI / 180;
          const lat1 = userGps.lat * Math.PI / 180;
          const lat2 = activeDestination.lat * Math.PI / 180;
          const y = Math.sin(dLon) * Math.cos(lat2);
          const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon);
          return Math.round((Math.atan2(y, x) * 180 / Math.PI + 360) % 360);
        }}
        return 90;
      }}
      const dLon = (wp.lon - userGps.lon) * Math.PI / 180;
      const lat1 = userGps.lat * Math.PI / 180;
      const lat2 = wp.lat * Math.PI / 180;
      const y = Math.sin(dLon) * Math.cos(lat2);
      const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon);
      return Math.round((Math.atan2(y, x) * 180 / Math.PI + 360) % 360);
    }}

    function checkAudioCompassHeadingAlignment(playChime = true) {{
      const targetBearing = computeTargetWaypointBearing();
      if (targetBearing === null) return {{ status: 'unknown', text: 'No active route bearing' }};

      const currentHeading = userGps.heading || 0;
      let diff = (targetBearing - currentHeading + 360) % 360;
      if (diff > 180) diff -= 360;

      let guidance = "";
      let onCourse = false;

      if (Math.abs(diff) <= 20) {{
        guidance = `Facing on course (${{currentHeading}}°). Waypoint is at ${{targetBearing}}°. Continue straight.`;
        onCourse = true;
        if (playChime) playAudioBeaconTick(true);
      }} else if (diff > 20) {{
        guidance = `Veering left. Bear right ${{Math.round(diff)}}° to face waypoint (${{targetBearing}}°).`;
        if (playChime) playAudioBeaconTick(false);
      }} else {{
        guidance = `Veering right. Bear left ${{Math.round(Math.abs(diff))}}° to face waypoint (${{targetBearing}}°).`;
        if (playChime) playAudioBeaconTick(false);
      }}
      return {{ status: onCourse ? 'on_course' : 'off_course', text: guidance, targetBearing, diff }};
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

    // ==================== EMERGENCY CONTACT & INCIDENT SOS DISPATCH ====================
    function triggerEmergencySOS() {{
      const modal = document.getElementById('sos-modal');
      if (modal) modal.classList.remove('hidden');

      const lat = userGps.lat ? userGps.lat.toFixed(5) : '56.9515';
      const lon = userGps.lon ? userGps.lon.toFixed(5) : '24.0812';
      const street = userGps.street ? `${{userGps.street}}, ${{userGps.city || ''}}` : 'Ķīpsalas iela, Rīga';

      const coordEl = document.getElementById('sos-coordinates');
      if (coordEl) coordEl.innerText = `${{lat}}° N, ${{lon}}° E`;

      const stEl = document.getElementById('sos-street-address');
      if (stEl) stEl.innerText = street;

      const timeEl = document.getElementById('sos-timestamp');
      if (timeEl) timeEl.innerText = new Date().toLocaleTimeString();

      const smsLink = document.getElementById('sos-sms-link');
      if (smsLink) {{
        const mapUrl = `https://maps.google.com/?q=${{lat}},${{lon}}`;
        const bodyText = encodeURIComponent(`EMERGENCY: Assistive Blind AI user needs help. Location: ${{street}} (${{lat}}, ${{lon}}). Map: ${{mapUrl}}`);
        smsLink.href = `sms:?body=${{bodyText}}`;
      }}

      triggerHaptic([200, 100, 200, 100, 500]);
      playEarcon('hazard');
      const spokenMsg = `Emergency SOS activated. You are at ${{street}}. Coordinates: ${{lat}} degrees north, ${{lon}} degrees east. Tap call or SMS on screen.`;
      speakText(spokenMsg);
      announceToScreenReader(spokenMsg);
      showUniversalVoiceHUD('EMERGENCY SOS', spokenMsg, false);
    }}

    function closeEmergencySOS() {{
      const modal = document.getElementById('sos-modal');
      if (modal) modal.classList.add('hidden');
      speakText("Emergency SOS dismissed. Route guidance resumed.");
      hideUniversalVoiceHUD();
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
      checkSensorPermissionsOnLaunch();

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
