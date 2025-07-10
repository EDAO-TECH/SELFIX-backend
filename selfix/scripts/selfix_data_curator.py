#!/usr/bin/env python3

import os
import json
import re
from datetime import datetime, timedelta

# Log paths
LOG_DIR = "/opt/SELFIX/logs"
OUTPUT_FILE = "/opt/SELFIX/ai_modules/daily_learning_input.json"
RELEVANT_LOGS = {
    "trap": "trap.log",
    "healing": "healing.log",
    "entropy": "entropy_events.log",
    "antivirus": "selfix_service.log",
    "daemon": "daemon.log"
}

# Time window: last 24h
CUTOFF = datetime.now() - timedelta(days=1)

# Log parsing pattern (flexible fallback)
TIMESTAMP_REGEX = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")

def extract_entries(filepath, tag):
    entries = []
    try:
        with open(filepath, "r") as f:
            for line in f:
                match = TIMESTAMP_REGEX.search(line)
                if not match:
                    continue
                try:
                    ts = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                    if ts >= CUTOFF:
                        entries.append({
                            "timestamp": ts.isoformat(),
                            "source": tag,
                            "content": line.strip()
                        })
                except ValueError:
                    continue
    except Exception as e:
        print(f"⚠️ Error reading {filepath}: {e}")
    return entries

def main():
    curated = []

    print(f"🧪 Starting log curation from last 24h...")
    for tag, filename in RELEVANT_LOGS.items():
        path = os.path.join(LOG_DIR, filename)
        if os.path.exists(path):
            print(f"📖 Reading {tag} → {filename}")
            curated += extract_entries(path, tag)
        else:
            print(f"⚠️ Log file missing: {filename}")

    # Save output
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as out:
        json.dump(curated, out, indent=2)

    print(f"✅ Curated {len(curated)} log entries saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
