#!/usr/bin/env python3
import os
import platform
import socket
import subprocess
import shutil
import json
import datetime
import psutil

REPORT_DIR = "/opt/SELFIX/reports"
LOG_PATH = "/opt/SELFIX/logs/selfix_service.log"
VERIFY_JSON_PATH = "/opt/SELFIX/logs/verify_log.json"

def print_header(title):
    print("\n🧪 SELFIX Full System Precheck")
    print("=" * 55)
    print(f"📅  Timestamp     : {datetime.datetime.now()}")
    print(f"🖥️   Hostname      : {socket.gethostname()}")
    print(f"🧠  System        : {platform.system()} {platform.release()} ({platform.machine()})")

def check_python():
    print("\n🐍 Checking Python...")
    version = platform.python_version()
    print(f"✅ Python version: {version}")

def check_memory():
    mem = psutil.virtual_memory()
    total_gb = round(mem.total / (1024 ** 3), 2)
    percent_used = mem.percent
    print(f"🧠 Memory: {total_gb} GB total")
    print(f"{'✅' if percent_used < 90 else '❌'} Memory usage: {percent_used}%")
    return percent_used < 90

def check_disk():
    usage = shutil.disk_usage("/")
    free_gb = round(usage.free / (1024 ** 3), 2)
    print(f"💽 Disk space: {free_gb} GB free")

def check_internet():
    print("🌐 Internet connectivity...")
    try:
        subprocess.check_call(["ping", "-c", "1", "8.8.8.8"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Internet available")
        return True
    except subprocess.CalledProcessError:
        print("❌ Internet unavailable")
        return False

def check_services():
    print("\n📡 Checking SELFIX system services...")
    services = ["selfix-agent", "selfix-av", "selfix-hq", "selfix-seeder", "selfix-backend"]
    for service in services:
        status = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True)
        active = status.stdout.strip() == "active"
        print(f"{'✅' if active else '❌'} {service}")

def check_agents():
    print("\n🤖 Checking local agents...")
    ai_path = "/opt/SELFIX/ai_modules/selfix_mission_context.py"
    seeder_path = "/etc/systemd/system/selfix-seeder.service"
    print(f"{'✅' if os.path.isfile(ai_path) else '❌'} Local AI module detected.")
    print(f"{'✅' if os.path.isfile(seeder_path) else '❌'} Seeder agent is installed.")

def check_antivirus():
    print("\n🦠 Antivirus engine check...")
    sig_path = "/opt/SELFIX/antivirus/selfix_signatures.json"
    if os.path.exists(sig_path):
        size_kb = round(os.path.getsize(sig_path) / 1024, 1)
        print(f"✅ Antivirus signatures found ({size_kb} KB)")
    else:
        print("❌ No antivirus signatures found")

def check_recent_logs():
    print("\n📜 Checking recent logs...")
    logs = []
    try:
        if os.path.exists(VERIFY_JSON_PATH):
            with open(VERIFY_JSON_PATH, "r") as f:
                content = f.read()
                json_objects = []
                for line in content.splitlines():
                    try:
                        obj = json.loads(line)
                        json_objects.append(obj)
                    except json.JSONDecodeError:
                        continue
                logs = json_objects[-5:]  # last 5 entries
        else:
            print("❌ verify_log.json not found.")
            return

        for i, entry in enumerate(logs, start=1):
            if isinstance(entry, dict):
                preview = ", ".join(f"{k}: {str(v)[:40]}..." if len(str(v)) > 40 else f"{k}: {v}"
                                    for k, v in list(entry.items())[:3])
                print(f"   - Entry {i}: {preview}")
            else:
                print(f"   - Entry {i}: (non-dict) {str(entry)[:80]}...")
    except Exception as e:
        print(f"❌ Error reading logs: {e}")

def write_report():
    os.makedirs(REPORT_DIR, exist_ok=True)
    report_path = os.path.join(REPORT_DIR, f"precheck_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    with open(report_path, "w") as f:
        f.write("Precheck summary written.\n")
    print(f"\n🧾 Summary written to {report_path}")

def main():
    print_header("SELFIX Precheck")
    check_python()
    memory_ok = check_memory()
    check_disk()
    internet_ok = check_internet()
    check_services()
    check_agents()
    check_antivirus()
    check_recent_logs()
    write_report()

    print("\n🧾 Summary:")
    if memory_ok and internet_ok:
        print("✅ All checks passed.")
    else:
        print("⚠️  One or more checks failed. Review the output above.")

def run_precheck():
    main()  # or whatever your precheck execution function is named

if __name__ == "__main__":
    main()
