#!/usr/bin/env python3

import os
import shutil
import socket
import psutil
import platform
from datetime import datetime

def banner():
    print("\n🧪 SELFIX System Precheck")
    print("=" * 40)
    print(f"Timestamp: {datetime.now()}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"System: {platform.system()} {platform.release()} ({platform.machine()})\n")

def check_python():
    print("🐍 Python Version Check...")
    if not shutil.which("python3"):
        print("❌ Python3 not found!")
        return False
    version = platform.python_version()
    print(f"✅ Found Python {version}")
    return True

def check_memory():
    print("🧠 Memory Check...")
    mem = psutil.virtual_memory()
    total = round(mem.total / (1024**3), 2)
    print(f"✅ {total} GB RAM detected")
    return total >= 2  # Minimum 2 GB

def check_disk():
    print("💽 Disk Space Check...")
    usage = shutil.disk_usage("/")
    free_gb = round(usage.free / (1024**3), 2)
    print(f"✅ {free_gb} GB free space available")
    return free_gb >= 5

def check_services():
    print("📡 Checking core services...")
    services = ["selfix-agent", "selfix-av", "selfix-hq", "selfix-seeder"]
    results = {}
    for service in services:
        status = os.system(f"systemctl is-active --quiet {service}")
        results[service] = (status == 0)
    for s, ok in results.items():
        icon = "✅" if ok else "❌"
        print(f"{icon} {s}")
    return all(results.values())

def main():
    banner()
    checks = [
        check_python(),
        check_memory(),
        check_disk(),
        check_services()
    ]
    if all(checks):
        print("\n✅ Precheck passed. System is ready.")
    else:
        print("\n⚠️ Some checks failed. Please investigate the issues.")

if __name__ == "__main__":
    main()
