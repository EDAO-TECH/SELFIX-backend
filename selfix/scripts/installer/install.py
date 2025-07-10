#!/usr/bin/env python3
# Unified SELFIX Installer – commercial-ready

import argparse
import os
import subprocess
import sys
from datetime import datetime

LOG_FILE = "/opt/SELFIX/logs/install.log"
PRECHECK = "/opt/SELFIX/scripts/installer/install_utils/precheck.py"
ACTIVATOR = "/opt/SELFIX/scripts/installer/activate_services.py"

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.utcnow()}] {message}\n")
    print(message)

def run_precheck():
    if not os.path.exists(PRECHECK):
        log("[❌] precheck.py not found.")
        sys.exit(1)
    log("[🔍] Running precheck...")
    subprocess.run(["python3", PRECHECK], check=True)

def activate_services(email=None, license_key=None):
    cmd = ["python3", ACTIVATOR]
    if email:
        cmd += ["--email", email]
    if license_key:
        cmd += ["--license", license_key]
    log(f"[🚀] Activating services for {email or license_key}...")
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(description="SELFIX Commercial Installer")
    parser.add_argument("--license", help="License key to activate paid features")
    parser.add_argument("--email", help="User email (for trial or license match)")
    parser.add_argument("--trial", action="store_true", help="Start 14-day trial")
    parser.add_argument("--enable", nargs="+", help="Select features to enable")
    parser.add_argument("--skip-precheck", action="store_true", help="Skip preflight system check")
    args = parser.parse_args()

    os.makedirs("/opt/SELFIX/logs", exist_ok=True)

    log("\n===============================")
    log("🚀 SELFIX INSTALLER STARTED")
    log("===============================\n")

    if not args.skip_precheck:
        run_precheck()

    # Placeholder for license/trial validation (to be built in license.py)
    if args.trial:
        log("[🆓] Trial mode selected")
        # Could call trial validation in future
    elif args.license:
        log(f"[🔐] License provided: {args.license}")
    else:
        log("[❌] No license or trial selected. Exiting.")
        sys.exit(1)

    if args.enable:
        log(f"[⚙️] Enabling modules: {', '.join(args.enable)}")
        # Pass modules to activation script or write to config (next step)

    activate_services(email=args.email, license_key=args.license)

    log("\n✅ SELFIX Installation Complete")
    log("===============================\n")

if __name__ == "__main__":
    main()
