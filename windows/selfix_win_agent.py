#!/usr/bin/env python3
import os
import time
import hashlib
import json
import shutil
from pathlib import Path

WATCH_PATH = Path("C:/Program Files/SELFIX/scan")
QUARANTINE_PATH = Path("C:/Program Files/SELFIX/quarantine")
SIGNATURES_FILE = Path("selfix_signatures.json")
POLL_INTERVAL = 10  # seconds

def load_signatures():
    if SIGNATURES_FILE.exists():
        with open(SIGNATURES_FILE, "r") as f:
            return json.load(f)
    return {"hashes": [], "filenames": []}

def hash_file(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except:
        return None

def scan_and_quarantine():
    signatures = load_signatures()
    for root, _, files in os.walk(WATCH_PATH):
        for file in files:
            file_path = Path(root) / file
            file_hash = hash_file(file_path)
            if not file_hash:
                continue
            if file_hash in signatures["hashes"] or file in signatures["filenames"]:
                print(f"[⚠️] Infected file: {file_path}")
                quarantine(file_path)

def quarantine(file_path):
    QUARANTINE_PATH.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    new_name = f"{timestamp}_{file_path.name}"
    dest = QUARANTINE_PATH / new_name
    try:
        shutil.move(str(file_path), str(dest))
        print(f"[🔒] Quarantined to: {dest}")
    except Exception as e:
        print(f"[❌] Quarantine failed: {e}")

def main():
    print("[🛡️] SELFIX Windows Agent Monitoring Started")
    print(f"📂 Watching: {WATCH_PATH}")
    while True:
        scan_and_quarantine()
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
