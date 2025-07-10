#!/usr/bin/env python3
"""
SELFIX Auto-Service Documentation Generator

Generates /opt/SELFIX/SERVICES.md with live service status and descriptions.
"""

import os
from datetime import datetime

# List of SELFIX services with friendly descriptions
services = {
    "selfix-agent": "Core monitoring agent (heartbeat, health data)",
    "selfix-av": "Antivirus scanner engine (ClamAV or custom signatures)",
    "selfix-hq": "Telemetry uplink to SELFIX HQ (inactive by default)",
    "selfix-seeder": "Module sync and peer-to-peer update service",
    "selfix-backend": "Backend server (logs, API, web dashboard)",
}

# Start writing markdown
lines = [f"# SELFIX Service Overview\n",
         f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
         "| Service Name     | Status     | Description                                      |",
         "|------------------|------------|--------------------------------------------------|"]

# Check service status
for svc, desc in services.items():
    running = os.system(f"systemctl is-active --quiet {svc}") == 0
    status = "✅ Running" if running else "❌ Inactive"
    lines.append(f"| {svc:<16} | {status:<10} | {desc} |")

# Add module references
lines.append("\n## 🤖 Local Modules")
lines.append("- `local_ai.py`: AI logic for threat evaluation / automation")
lines.append("- `selfix_heal.py`: AV-specific healing script")
lines.append("- `engine/healing_manager.py`: System-wide healing dispatcher")
lines.append("- `scripts/selfix_precheck.py`: Full diagnostics check\n")

# Optional log and status tips
lines.append("## 📜 Logs & Reports")
lines.append("- Reports: `/opt/SELFIX/reports/precheck_*.log`")
lines.append("- Heal logs: `/opt/SELFIX/reports/heal_*.log`")
lines.append("- Status command: `selfix status`\n")

# Save to file
doc_path = "/opt/SELFIX/SERVICES.md"
with open(doc_path, "w") as f:
    f.write("\n".join(lines))

print(f"✅ SELFIX services documented to: {doc_path}")
