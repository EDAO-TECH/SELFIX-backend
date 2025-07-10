#!/usr/bin/env python3
import subprocess
import sys
import json
from pathlib import Path

HEALING_MAP = {
    "ransom_payload.bak": "healing_modules/ransom_restore.py",
    "backdoor.sh": "healing_modules/kill_backdoor.py",
    "malicious_script.py": "healing_modules/revert_script_patch.py"
}

LOGFILE = Path("logs/maintenance.log")

def select_healer(file_path: str):
    name = Path(file_path).name
    # Strip timestamp prefix like 20250622_101151_backdoor.sh
    parts = name.split("_", 2)
    if len(parts) > 2 and parts[0].isdigit():
        normalized = "_".join(parts[2:])  # handles timestamps with underscores
    elif len(parts) > 1 and parts[0].isdigit():
        normalized = "_".join(parts[1:])
    else:
        normalized = name
    return HEALING_MAP.get(normalized)

def run_healing_module(module_path, infected_file):
    if not Path(module_path).exists():
        print(f"[⚠️] Healing module not found: {module_path}")
        return

    print(f"[🧠] Healing with: {module_path}")
    try:
        subprocess.run(["python3", module_path, infected_file])
        with LOGFILE.open("a") as log:
            log.write(f"[HEALED] {infected_file} using {module_path}\n")
    except Exception as e:
        print(f"[❌] Healing failed: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 selfix_heal.py /path/to/infected.file")
        return

    infected_file = sys.argv[1]
    healer = select_healer(infected_file)

    if not healer:
        print(f"[ℹ️] No healing module mapped for: {infected_file}")
        return

    run_healing_module(healer, infected_file)

if __name__ == "__main__":
    main()
