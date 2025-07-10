#!/usr/bin/env python3

import shutil
import os
import json
from pathlib import Path
from datetime import datetime

QUARANTINE_DIR = Path("/opt/SELFIX/quarantine")
LOG_FILE = Path("/opt/SELFIX/data/quarantine_log.json")

QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def quarantine_file(file_path):
    try:
        src = Path(file_path)
        if not src.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        dest = QUARANTINE_DIR / f"quarantine_{timestamp}_{src.name}"
        shutil.move(str(src), str(dest))

        log_entry = {
            "original_path": str(src),
            "quarantined_path": str(dest),
            "timestamp": datetime.utcnow().isoformat(),
            "status": "quarantined"
        }

        if LOG_FILE.exists():
            existing_log = json.loads(LOG_FILE.read_text())
        else:
            existing_log = []
        existing_log.append(log_entry)
        LOG_FILE.write_text(json.dumps(existing_log, indent=2))

        print(f"✅ Quarantined: {src} → {dest}")
        return log_entry

    except Exception as e:
        print(f"❌ Error quarantining {file_path}: {str(e)}")
        return {
            "file_path": file_path,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
            "status": "error"
        }


if __name__ == "__main__":
    test_path = input("Enter file path to quarantine: ").strip()
    quarantine_file(test_path)
