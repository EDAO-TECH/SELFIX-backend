#!/usr/bin/env python3
import subprocess
import time
import json
from pathlib import Path

SCANNER = "antivirus/selfix_scanner.py"
QUARANTINE = "antivirus/selfix_quarantine.py"
MAINTENANCE_LOG = Path("logs/maintenance.log")

def extract_infected_files():
    if not MAINTENANCE_LOG.exists():
        return []

    infected = []
    with open(MAINTENANCE_LOG, "r") as f:
        for line in f:
            if "[INFECTED]" in line:
                file_path = line.strip().split("]")[-1].strip()
                if Path(file_path).exists():
                    infected.append(file_path)
    return list(set(infected))  # remove duplicates

def run_once():
    print("[🔍] Running scanner...")
    subprocess.run(["python3", SCANNER])

    print("[🔎] Extracting infected files from log...")
    infected_files = extract_infected_files()

    if not infected_files:
        print("[✅] No threats detected.")
        return

    for file in infected_files:
        print(f"[🛡️] Quarantining {file}...")
        subprocess.run(["python3", QUARANTINE, file])

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", type=int, help="Scan interval in minutes (e.g., --loop 10)")
    args = parser.parse_args()

    if args.loop:
        while True:
            run_once()
            print(f"[⏱️] Sleeping {args.loop} minutes...\n")
            time.sleep(args.loop * 60)
    else:
        run_once()

if __name__ == "__main__":
    main()
