/**
 * Direct In-Process Verification Test for Voice Navigation / Gemini AI Integration
 */
const aiService = require('../backend/src/services/ai/aiService');

async function runDirectTests() {
  console.log("=== Testing Blind AI Natural-Language Voice Navigation (In-Process) ===\n");

  const testCases = [
    {
      label: '1. Library Request',
      input: 'Take me to the library',
      expectedIntent: 'start_navigation',
      expectedCanonical: 'RTU Scientific Library'
    },
    {
      label: '2. Main Building Request',
      input: 'Open the main building',
      expectedIntent: 'start_navigation',
      expectedCanonical: 'RTU Main Building & Administration'
    },
    {
      label: '3. Sports Center Request',
      input: 'I want to go to the sports center',
      expectedIntent: 'start_navigation',
      expectedCanonical: 'RTU Ķīpsala Sports Center & Pool'
    },
    {
      label: '4. RTU Campus Request',
      input: 'Take me to RTU',
      expectedIntent: 'start_navigation',
      expectedCanonical: 'Riga Technical University (RTU)'
    },
    {
      label: '5. Arbitrary Location (Old Town)',
      input: 'Take me to Old Town',
      expectedIntent: 'start_navigation',
      expectedCanonical: 'Old Town'
    },
    {
      label: '6. Vague Destination (Auto-GPS Routing Triggered)',
      input: 'Take me there',
      expectedIntent: 'start_navigation'
    },
    {
      label: '7. Where Am I Intent',
      input: 'Where am I?',
      expectedIntent: 'where_am_i'
    },
    {
      label: '8. Describe Surroundings Intent',
      input: 'Describe what is around me',
      expectedIntent: 'describe_environment'
    },
    {
      label: '9. Stop Navigation Intent',
      input: 'Stop navigation',
      expectedIntent: 'stop'
    },
    {
      label: '10. Affirmative Hands-Free Response ("Yes" / "Okay")',
      input: 'yes',
      expectedIntent: 'affirmative'
    },
    {
      label: '11. Negative Hands-Free Response ("No" / "Wait")',
      input: 'wait',
      expectedIntent: 'negative'
    },
    {
      label: '12. Active Guidance Query ("Where do I go?")',
      input: 'where do i go',
      expectedIntent: 'guidance_query'
    },
    {
      label: '13. Obstacle Query ("Is there anything in my way?")',
      input: 'is there anything in my way',
      expectedIntent: 'obstacle_query'
    },
    {
      label: '14. Directional Right Query ("Is someone coming from my right?")',
      input: 'is someone coming from my right',
      expectedIntent: 'directional_query'
    },
    {
      label: '15. Directional Left Query ("What is on my left?")',
      input: 'what is on my left',
      expectedIntent: 'directional_query'
    },
    {
      label: '16. Approaching Person Query ("Is someone approaching?")',
      input: 'is someone approaching',
      expectedIntent: 'directional_query'
    },
    {
      label: '17. Heading Alignment Query ("Am I facing the right way?")',
      input: 'am i facing the right way',
      expectedIntent: 'heading_query'
    },
    {
      label: '18. Distance Remaining Query ("How far am I?")',
      input: 'how far am i',
      expectedIntent: 'distance_query'
    },
    {
      label: '19. Current Street Query ("What street is this?")',
      input: 'what street is this',
      expectedIntent: 'street_query'
    },
    {
      label: '20. Crosswalk Safety Query ("Can I cross?")',
      input: 'can i cross',
      expectedIntent: 'click_button'
    },
    {
      label: '21. Stairs Ahead Query ("Are there stairs?")',
      input: 'are there stairs',
      expectedIntent: 'stairs_query'
    },
    {
      label: '22. Sunlight High Contrast Toggle ("High contrast")',
      input: 'high contrast',
      expectedIntent: 'click_button',
      expectedTargetButton: 'toggle_high_contrast'
    },
    {
      label: '23. Night Vision Filter Toggle ("Night vision")',
      input: 'night vision',
      expectedIntent: 'click_button',
      expectedTargetButton: 'toggle_night_vision'
    },
    {
      label: '24. Steps and Pedometer Query ("How many steps did I walk?")',
      input: 'how many steps did i walk',
      expectedIntent: 'steps_query'
    },
    {
      label: '25. Emergency SOS Beacon Trigger ("Emergency")',
      input: 'emergency',
      expectedIntent: 'emergency_sos'
    },
    {
      label: '26. Crosswalk Traffic Acoustic Query ("Is it quiet?")',
      input: 'is it quiet',
      expectedIntent: 'traffic_query'
    },
    {
      label: '27. Crossing Path YOLO Detection Query ("Is there a crossing path?")',
      input: 'is there a crossing path',
      expectedIntent: 'crossing_path_query'
    },
    {
      label: '28. Sidewalk Tree YOLO Detection Query ("Is there a tree?")',
      input: 'is there a tree',
      expectedIntent: 'tree_query'
    },
    {
      label: '29. Riga Road Sign YOLO Detection Query ("Detect road signs")',
      input: 'detect road signs',
      expectedIntent: 'detect_signs'
    },
    {
      label: '30. Standing People & People Around Query ("Is anyone standing ahead?")',
      input: 'is anyone standing ahead',
      expectedIntent: 'people_around_query'
    },
    {
      label: '31. Ground Depth Hole / Drop-off Query ("Is there a depth hole?")',
      input: 'is there a depth hole',
      expectedIntent: 'depth_hole_query'
    },
    {
      label: '32. Dual-Move Choice 1: Surface Walk ("Normal walk to bus stop")',
      input: 'normal walk to bus stop',
      expectedIntent: 'dual_move_select'
    },
    {
      label: '33. Dual-Move Choice 2: Underpass ("Use tunnel going down")',
      input: 'use tunnel going down',
      expectedIntent: 'dual_move_select'
    },
    {
      label: '34. Traffic Light Signal Color Query ("What color is the traffic light?")',
      input: 'what color is the traffic light',
      expectedIntent: 'traffic_light_query',
      liveContext: {
        trafficLightSignal: 'RED',
        groundState: 'Flat',
        objects: [{ label: 'Traffic Light (RED)', rawClass: 'traffic light', trafficLightColor: 'RED', distance: 4.2, lane: 'center', widthM: 0.35, heightM: 0.85 }]
      }
    },
    {
      label: '35. Ground Surface Flatness/Tilt Query ("Is the ground flat or uneven?")',
      input: 'is the ground flat or uneven',
      expectedIntent: 'ground_surface_query',
      liveContext: {
        groundState: 'Tilted',
        objects: []
      }
    },
    {
      label: '36. Object Distance & Width/Height Size Query ("How big and wide is the obstacle?")',
      input: 'how big and wide is the obstacle',
      expectedIntent: 'object_dimensions_query',
      liveContext: {
        groundState: 'Flat',
        objects: [{ label: 'Tree', rawClass: 'tree', distance: 2.4, lane: 'right', widthM: 0.9, heightM: 2.8 }]
      }
    },
    {
      label: '37. Pedestrian Motion Direction Query ("Are people walking toward me or crossing?")',
      input: 'are people walking toward me or crossing',
      expectedIntent: 'pedestrian_motion_query',
      liveContext: {
        groundState: 'Flat',
        objects: [{ label: '🚶⬆️ Person Approaching', rawClass: 'person', isPerson: true, personMotion: 'walking_toward', distance: 2.1, lane: 'center', widthM: 0.5, heightM: 1.7 }]
      }
    },
    {
      label: '38. Utility Pole / Bollard Detection Query ("Is there a pole ahead?")',
      input: 'is there a pole ahead',
      expectedIntent: 'pole_query',
      liveContext: {
        groundState: 'Flat',
        objects: [{ label: '💈 Pole', rawClass: 'pole', isPole: true, distance: 1.8, lane: 'left', widthM: 0.2, heightM: 2.2 }]
      }
    },
    {
      label: '39. Live-Context Surroundings Question ("What is in front of me right now?")',
      input: 'what is in front of me right now',
      expectedIntent: 'describe_environment',
      liveContext: {
        groundState: 'Flat',
        trafficLightSignal: 'GREEN',
        objects: [
          { label: '🚶↔️ Person Crossing Path', rawClass: 'person', isPerson: true, personMotion: 'crossing_path', distance: 2.6, lane: 'center', widthM: 0.5, heightM: 1.7 },
          { label: 'Traffic Light (GREEN)', rawClass: 'traffic light', isTrafficLight: true, trafficLightColor: 'GREEN', distance: 5.0, lane: 'center', widthM: 0.35, heightM: 0.85 }
        ]
      }
    }
  ];

  let passed = 0;
  for (const tc of testCases) {
    try {
      const data = await aiService.parseVoiceCommand({ transcript: tc.input, liveContext: tc.liveContext || null });
      if (!data) {
        console.error(`❌ [FAIL] ${tc.label}: No data returned`);
        continue;
      }

      const intentMatch = data.intent === tc.expectedIntent;
      let destMatch = true;
      if (tc.expectedCanonical) {
        const destName = data.destination?.canonicalName;
        destMatch = destName && destName.toLowerCase().includes(tc.expectedCanonical.toLowerCase());
      }
      let btnMatch = true;
      if (tc.expectedTargetButton) {
        btnMatch = data.target_button === tc.expectedTargetButton || data.action === tc.expectedTargetButton;
      }

      if (intentMatch && destMatch && btnMatch) {
        passed++;
        console.log(`✅ [PASS] ${tc.label} ("${tc.input}")`);
        console.log(`   -> Intent: ${data.intent}`);
        if (data.destination) {
          console.log(`   -> Destination: ${data.destination.canonicalName} (${data.destination.distanceKm} km, ${data.destination.estimatedMinutes} min, ${data.destination.waypoints?.length || 0} waypoints)`);
        }
        if (data.clarification_prompt) {
          console.log(`   -> Clarification Prompt: "${data.clarification_prompt}"`);
        }
        console.log(`   -> Spoken Response: "${data.spoken_response}"\n`);
      } else {
        console.error(`❌ [FAIL] ${tc.label} ("${tc.input}")`);
        console.error(`   Expected Intent: ${tc.expectedIntent}, got: ${data.intent}`);
        if (tc.expectedCanonical) {
          console.error(`   Expected Dest containing: ${tc.expectedCanonical}, got: ${data.destination?.canonicalName}`);
        }
        console.error(`   Response data:`, data, `\n`);
      }
    } catch (e) {
      console.error(`❌ [ERROR] ${tc.label}:`, e.message);
    }
  }

  console.log(`=== Summary: ${passed} / ${testCases.length} tests passed ===`);
  if (passed === testCases.length) {
    console.log("🎉 ALL TESTS PASSED! Voice navigation with Gemini AI is fully functioning.");
    process.exit(0);
  } else {
    process.exit(1);
  }
}

runDirectTests();
