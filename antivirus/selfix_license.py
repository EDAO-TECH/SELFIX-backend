#!/usr/bin/env python3
import json
import hashlib
from pathlib import Path
import time
import sys

LICENSE_FILE = Path("config/selfix_license.key")

def hash_machine():
    # Just a basic hash from hostname + boot time for binding
    try:
        host = Path("/etc/hostname").read_text().strip()
        boot = int(Path("/proc/stat").stat().st_ctime)
        return hashlib.sha256(f"{host}{boot}".encode()).hexdigest()[:16]
    except Exception:
        return "UNKNOWN_MACHINE"

def load_license():
    if not LICENSE_FILE.exists():
        return None

    try:
        with LICENSE_FILE.open() as f:
            return json.load(f)
    except:
        return None

def validate_license():
    lic = load_license()
    if not lic:
        print("[🔐] License missing or invalid.")
        return False

    expected = hash_machine()
    if lic.get("machine_id") != expected:
        print("[❌] License machine mismatch.")
        return False

    exp_time = time.strptime(lic["expires"], "%Y-%m-%d")
    if time.time() > time.mktime(exp_time):
        print("[⏳] License expired.")
        return False

    print("[✅] License is valid.")
    return True

if __name__ == "__main__":
    if not validate_license():
        sys.exit(1)
