#!/usr/bin/env python3

import os
import platform
import datetime
import psutil

SELFIX_PATH = "/opt/SELFIX"
EDAO_PATH = "/opt/edao"
LOG_DIR = "/opt/SELFIX/reports"
os.makedirs(LOG_DIR, exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = f"{LOG_DIR}/full_precheck_{timestamp}.log"

def log(msg):
    print(msg)
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")

def check_header():
    log("🧪 SELFIX Full System Precheck")
    log("=" * 55)
    log(f"📅 Timestamp     : {datetime.datetime.now()}")
    log(f"🖥️  Hostname      : {platform.node()}")
    log(f"🧠 System        : {platform.system()} {platform.release()} ({platform.machine()})\n")

def check_system():
    log("🐍 Checking Python...")
    log(f"✅ Python version: {platform.python_version()}")

    mem = psutil.virtual_memory()
    log(f"🧠 Memory: {round(mem.total / (1024**3), 2)} GB total")
    log(f"✅ Memory usage: {mem.percent}%")

    disk = psutil.disk_usage("/")
    log(f"💽 Disk space: {round(disk.free / (1024**3), 2)} GB free")

    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        log("✅ Internet available\n")
    except:
        log("❌ No internet connection\n")

def check_services(name_prefix):
    log(f"📡 Checking {name_prefix.upper()} system services...")
    try:
        import subprocess
        result = subprocess.run(["systemctl", "list-units", "--type=service", "--no-pager"], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        found = False
        for line in lines:
            if name_prefix in line:
                log("✅ " + line.strip())
                found = True
        if not found:
            log(f"⚠️  No {name_prefix} services found.")
    except Exception as e:
        log(f"❌ Error checking {name_prefix} services: {str(e)}")
    log("")

def check_processes(label, path):
    log(f"🔍 Checking running processes for {label}...")
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = " ".join(proc.info['cmdline'])
            if path in cmdline:
                log(f"✅ PID {proc.info['pid']} | {cmdline}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    log("")

def list_python_files(label, base_path):
    log(f"📂 Listing Python files in {label} ({base_path})...")
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                log(f"📂 {full_path}")
    log("")

def main():
    check_header()
    check_system()
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
