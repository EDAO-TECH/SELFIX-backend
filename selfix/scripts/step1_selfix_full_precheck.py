#!/usr/bin/env python3
import os
import platform
import socket
import subprocess
import sys
import time
from datetime import datetime

LOG_DIR = "/opt/SELFIX/reports"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"full_precheck_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

SELFIX_PATH = "/opt/SELFIX"
EDAO_PATH = "/opt/edao"

def log(text):
    with open(LOG_FILE, "a") as f:
        f.write(text + "\n")
    print(text)

def check_header():
    log("🧪 SELFIX Full System Precheck")
    log("="*55)
    log(f"📅  Timestamp     : {datetime.now()}")
    log(f"🖥️   Hostname      : {socket.gethostname()}")
    log(f"🧠  System        : {platform.system()} {platform.release()} ({platform.machine()})\n")

def check_python():
    version = sys.version.split()[0]
    log("🐍 Checking Python...")
    log(f"✅ Python version: {version}")

def check_resources():
    try:
        mem = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024**3)
        disk = subprocess.check_output("df -h / | tail -1 | awk '{print $4}'", shell=True).decode().strip()
        mem_usage = subprocess.getoutput("free | awk '/Mem:/ { printf \"%.1f\", $3/$2 * 100.0 }'")
        log(f"🧠 Memory: {mem:.2f} GB total")
        log(f"✅ Memory usage: {mem_usage}%")
        log(f"💽 Disk space: {disk} free")
    except Exception as e:
        log(f"❌ Resource check failed: {e}")

def check_internet():
    log("🌐 Internet connectivity...")
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=3)
        log("✅ Internet available")
    except:
        log("❌ No internet access")

def check_services(prefix):
    log(f"\n📡 Checking {prefix.upper()} system services...")
    try:
        output = subprocess.check_output("systemctl list-units --type=service --no-pager", shell=True).decode()
        services = [line.split()[0] for line in output.splitlines() if line.startswith(f"{prefix}-")]
        if not services:
            log(f"⚠️  No {prefix} services found")
        for svc in services:
            active = subprocess.call(f"systemctl is-active --quiet {svc}", shell=True) == 0
            log(f"{'✅' if active else '❌'} {svc}")
    except Exception as e:
        log(f"❌ Error checking services: {e}")

def check_processes(label, path):
    log(f"\n🔍 Running processes under {label} ({path})...")
    try:
        output = subprocess.getoutput(f"ps aux | grep {path} | grep -v grep")
        if output:
            for line in output.splitlines():
                log(f"✅ {line}")
        else:
            log("⚠️  No running processes found.")
    except Exception as e:
        log(f"❌ Error checking processes: {e}")

def list_python_files(label, path):
    log(f"\n📂 Listing Python files under {label} ({path})...")
    try:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    log(f"📂 {os.path.join(root, file)}")
    except Exception as e:
        log(f"❌ Failed to list Python files in {path}: {e}")

def main():
    check_header()
    check_python()
    check_resources()
    check_internet()
    check_services("selfix")
    check_services("edao")
    check_processes("SELFIX", SELFIX_PATH)
    check_processes("EDAO", EDAO_PATH)
    list_python_files("SELFIX", SELFIX_PATH)
    list_python_files("EDAO", EDAO_PATH)
    log(f"\n🧾 Log saved to: {LOG_FILE}")
    print("\n✅ Precheck complete.\n")

if __name__ == "__main__":
    main()
