# SELFIX Service Overview

Generated on: 2025-07-08 19:49:56

| Service Name     | Status     | Description                                      |
|------------------|------------|--------------------------------------------------|
| selfix-agent     | ✅ Running  | Core monitoring agent (heartbeat, health data) |
| selfix-av        | ✅ Running  | Antivirus scanner engine (ClamAV or custom signatures) |
| selfix-hq        | ❌ Inactive | Telemetry uplink to SELFIX HQ (inactive by default) |
| selfix-seeder    | ✅ Running  | Module sync and peer-to-peer update service |
| selfix-backend   | ❌ Inactive | Backend server (logs, API, web dashboard) |

## 🤖 Local Modules
- `local_ai.py`: AI logic for threat evaluation / automation
- `selfix_heal.py`: AV-specific healing script
- `engine/healing_manager.py`: System-wide healing dispatcher
- `scripts/selfix_precheck.py`: Full diagnostics check

## 📜 Logs & Reports
- Reports: `/opt/SELFIX/reports/precheck_*.log`
- Heal logs: `/opt/SELFIX/reports/heal_*.log`
- Status command: `selfix status`
