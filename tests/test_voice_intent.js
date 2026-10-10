/**
 * Automated Verification Test for Voice Navigation / Gemini AI Integration
 */
const http = require('http');

async function testVoiceIntent(transcript) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({ transcript });
    const req = http.request(
      {
        hostname: 'localhost',
        port: 3000,
        path: '/api/v1/voice/intent',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload)
        }
      },
      (res) => {
        let data = '';
        res.on('data', (chunk) => (data += chunk));
        res.on('end', () => {
          try {
            resolve({ statusCode: res.statusCode, body: JSON.parse(data) });
          } catch (e) {
            resolve({ statusCode: res.statusCode, raw: data });
          }
        });
      }
    );

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

async function runTests() {
  console.log("=== Testing Blind AI Natural-Language Voice Navigation ===\n");

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
    }
  ];

  let passed = 0;
  for (const tc of testCases) {
    try {
      const res = await testVoiceIntent(tc.input);
      const data = res.body?.data;
      if (!data) {
        console.error(`❌ [FAIL] ${tc.label}: No data in response`, res);
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

  console.log(`\n=== Summary: ${passed} / ${testCases.length} tests passed ===`);
  if (passed === testCases.length) {
    console.log("🎉 ALL TESTS PASSED! Voice navigation with Gemini AI is fully functioning.");
    process.exit(0);
  } else {
    process.exit(1);
  }
}

runTests();
