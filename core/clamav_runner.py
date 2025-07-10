#!/usr/bin/env python3

import subprocess
import json
from pathlib import Path
from datetime import datetime

# Define output log location
OUTPUT_LOG = Path("/opt/SELFIX/data/clamav_threats.json")
SCAN_PATHS = ["/home", "/etc", "/opt/SELFIX"]


def run_clamav_scan():
    threats = []
    for path in SCAN_PATHS:
        try:
            result = subprocess.run([
                "clamscan", "-r", "--infected", "--no-summary", path
            ], capture_output=True, text=True)

            for line in result.stdout.strip().split("\n"):
                if ": " in line:
                    filepath, status = line.split(": ", 1)
                    if status != "OK":
                        threats.append({
                            "file": filepath.strip(),
                            "status": status.strip(),
                            "timestamp": datetime.utcnow().isoformat()
                        })

        except Exception as e:
            threats.append({
                "file": path,
                "status": f"scan_error: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            })

    OUTPUT_LOG.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_LOG.write_text(json.dumps(threats, indent=2))
    return threats


if __name__ == "__main__":
    results = run_clamav_scan()
    print(json.dumps(results, indent=2))
