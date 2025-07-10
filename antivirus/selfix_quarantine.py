#!/usr/bin/env python3
import os
import shutil
import time
import json
from pathlib import Path

QUARANTINE_PATH = Path("/opt/SELFIX/quarantine")
METADATA_FILE = QUARANTINE_PATH / "quarantine_log.json"

def ensure_quarantine_folder():
    QUARANTINE_PATH.mkdir(parents=True, exist_ok=True)
    if not METADATA_FILE.exists():
        with open(METADATA_FILE, "w") as f:
            json.dump([], f)

def add_to_quarantine(file_path, reason="signature_match"):
    ensure_quarantine_folder()

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    original_name = Path(file_path).name
    quarantined_name = f"{timestamp}_{original_name}"
    destination = QUARANTINE_PATH / quarantined_name

    try:
        shutil.move(file_path, destination)
        print(f"[🔒] Quarantined: {file_path} → {destination}")

        record = {
            "original_path": str(file_path),
            "quarantined_as": quarantined_name,
            "reason": reason,
            "timestamp": timestamp
        }

        with open(METADATA_FILE, "r+") as f:
            data = json.load(f)
            data.append(record)
            f.seek(0)
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"[❌] Failed to quarantine {file_path}: {e}")

def main():
    # Example manual test (normally called from scanner)
    test_file = "healing_modules/backdoor.sh"
    if Path(test_file).exists():
        add_to_quarantine(test_file)
    else:
        print("[ℹ️] Test file not found — nothing to quarantine.")

if __name__ == "__main__":
    main()
