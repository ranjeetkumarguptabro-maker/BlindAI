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
    }
  ];

  let passed = 0;
  for (const tc of testCases) {
    try {
      const data = await aiService.parseVoiceCommand({ transcript: tc.input });
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

      if (intentMatch && destMatch) {
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
