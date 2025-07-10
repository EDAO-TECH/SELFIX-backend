#!/usr/bin/env python3
# Launches only the services the user is allowed to use

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

USER_DB = "/opt/SELFIX/data/users.json"
LOG_FILE = "/opt/SELFIX/logs/activation.log"

SERVICE_MAP = {
    "AI_HEALING": "services/healing.py",
    "ROLLBACK_ENGINE": "services/rollback.py",
    "TRAP_LOGIC": "services/trap_logic.py",
    "SEEDER_AGENT": "services/seeder.py"
}

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.utcnow()}] {msg}\n")
    print(msg)

def load_user(email=None, license_key=None):
    if not os.path.exists(USER_DB):
        log("[❌] User database not found.")
        sys.exit(1)

    with open(USER_DB) as f:
        users = json.load(f)

    for user_email, info in users.items():
        if (email and user_email == email) or (license_key and info.get("license") == license_key):
            return info

    log("[❌] User not found or not licensed.")
    sys.exit(1)

def start_service(module_path):
    full_path = os.path.join("/opt/SELFIX", module_path)
    if not os.path.exists(full_path):
        log(f"[⚠️] Module not found: {full_path}")
        return
    subprocess.Popen(["python3", full_path])
    log(f"[✅] Started service: {module_path}")

def main():
    parser = argparse.ArgumentParser(description="SELFIX Service Activator")
    parser.add_argument("--email", help="Email address of the user")
    parser.add_argument("--license", help="License key of the user")
    args = parser.parse_args()

    log("====================================")
    log("🟢 SELFIX SERVICE ACTIVATION STARTED")
    log("====================================")

    user_info = load_user(email=args.email, license_key=args.license)
    allowed_services = user_info.get("services", [])

    log(f"[👤] Activating services for user: {args.email or args.license}")
    log(f"[🔓] Allowed features: {', '.join(allowed_services)}")

    for service in allowed_services:
        module_path = SERVICE_MAP.get(service)
        if module_path:
            start_service(module_path)
        else:
            log(f"[⚠️] Unknown service key: {service}")

    log("✅ Service activation complete.\n")

if __name__ == "__main__":
    main()
