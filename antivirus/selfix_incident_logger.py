#!/usr/bin/env python3
import json
import time
from pathlib import Path

INCIDENT_LOG = Path("logs/incidents.json")

def ensure_log_file():
    INCIDENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    if not INCIDENT_LOG.exists():
        with INCIDENT_LOG.open("w") as f:
            json.dump([], f)

def log_event(event_type, file_path, details=None):
    ensure_log_file()
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event_type,
        "file": str(file_path),
        "details": details or {}
    }

    with INCIDENT_LOG.open("r+") as f:
        data = json.load(f)
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=2)

    print(f"[📋] Logged {event_type} event for: {file_path}")

# === Example Usage ===
if __name__ == "__main__":
    log_event("healed", "/opt/SELFIX/quarantine/example.sh", {"module": "kill_backdoor.py"})
