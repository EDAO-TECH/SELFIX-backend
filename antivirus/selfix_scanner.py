#!/usr/bin/env python3
import os
import hashlib
import json
from pathlib import Path

SIGNATURES_FILE = "antivirus/selfix_signatures.json"
QUARANTINE_PATH = "quarantine"
LOGFILE = "logs/maintenance.log"

def load_signatures():
    if not os.path.exists(SIGNATURES_FILE):
        return {"hashes": [], "filenames": []}
    with open(SIGNATURES_FILE, 'r') as f:
        return json.load(f)

def hash_file(file_path):
    try:
        h = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def scan_folder(folder, signatures):
    infected = []
    for root, _, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root, file)
            file_hash = hash_file(full_path)
            if file_hash in signatures["hashes"] or file in signatures["filenames"]:
                infected.append(full_path)
    return infected

def log(message):
    with open(LOGFILE, "a") as f:
        f.write(f"[INFECTED] {message}\n")

def main():
    base_path = Path("/opt/SELFIX")
    targets = ["vault", "healing_modules", "backups"]

    signatures = load_signatures()
    total_infected = []

    for target in targets:
        path = base_path / target
        if path.exists():
            infected = scan_folder(path, signatures)
            for file in infected:
                print(f"[!] Infected file found: {file}")
                log(file)
            total_infected.extend(infected)

    if not total_infected:
        print("✅ No infected files found.")
    else:
        print(f"⚠️ Found {len(total_infected)} infected files. See log for details.")

if __name__ == "__main__":
    main()
