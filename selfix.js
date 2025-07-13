<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>SELFIX Dashboard</title>
  <style>
    body {
      font-family: monospace;
      background: #0f0f0f;
      color: #00ffaa;
      padding: 2rem;
    }
    h1, h3 {
      color: #66ffcc;
    }
    .block {
      margin-bottom: 2em;
      padding: 1em;
      border: 1px solid #00ffaa;
      border-radius: 8px;
      background: #1a1a1a;
    }
    ul { padding-left: 1.5rem; }
    pre { background: #000; padding: 1rem; overflow-x: auto; }
  </style>
</head>
<body>
  <h1>🛡️ SELFIX CyberDefense Node</h1>

  <div class="block" id="statusPanel">Checking status...</div>
  <div class="block" id="entropyPanel">Loading healing events...</div>
  <div class="block" id="journalPanel">Fetching AI journal...</div>

  <script>
    const baseURL = "http://<YOUR-BACKEND-IP>:5050/api";

    // STATUS PANEL
    fetch(`${baseURL}/status`)
      .then(res => res.json())
      .then(data => {
        document.getElementById("statusPanel").innerHTML = `
          <h3>System Status</h3>
          <p><strong>Status:</strong> ${data.status}</p>
          <p><strong>Healing:</strong> ${data.healing_active ? "🛡️ Active" : "⛔ Inactive"}</p>
          <p><strong>Timestamp:</strong> ${data.timestamp}</p>`;
      })
      .catch(err => {
        document.getElementById("statusPanel").innerHTML =
          `<strong>Error:</strong> Could not reach SELFIX backend.`;
      });

    // ENTROPY PANEL
    fetch(`${baseURL}/entropy`)
      .then(res => res.json())
      .then(data => {
        const events = data.events || [];
        const list = events.length
          ? `<ul>${events.map(e => `<li>${JSON.stringify(e)}</li>`).join('')}</ul>`
          : "No entropy events logged.";
        document.getElementById("entropyPanel").innerHTML = `
          <h3>Recent Healing Events</h3>${list}`;
      });

    // JOURNAL PANEL
    fetch(`${baseURL}/ai-journal`)
      .then(res => res.json())
      .then(data => {
        const entries = data.journal || {};
        document.getElementById("journalPanel").innerHTML = `
          <h3>AI Journal Snapshot</h3><pre>${JSON.stringify(entries, null, 2)}</pre>`;
      });
  </script>
</body>
</html>
