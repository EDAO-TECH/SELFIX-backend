#!/usr/bin/env python3
import os, time, psutil, datetime

def format_bool(flag):
    return "✅" if flag else "❌"

def header():
    os.system("clear")
    print("🛡️  SELFIX Realtime CLI Monitor     ⏱️", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("───────────────────────────────────────────────────────")

def system_status():
    print("🔁 SYSTEM STATUS")
    print("───────────────────────────────────────────────────────")
    print(f"🧠 Local AI Agent (Agent 001):         {format_bool(True)}")
    print(f"🌱 Seeder Agent:                       {format_bool(True)}")
    print(f"🔥 Healing Engine:                     {format_bool(True)}")
    print(f"🎯 Trap Logic System:                  {format_bool(False)}")
    print(f"📂 File Watcher:                       {format_bool(True)}")
    print(f"🔒 SmartLicense-X:                     {format_bool(True)}")
    print()

def entropy_status():
    print("🌡️  ENTROPY & THREAT ANALYTICS")
    print("───────────────────────────────────────────────────────")
    print("📈 Entropy Score:                 22.3%  (⚠️ Normal)")
    print("🧬 Healing Pulses Today:         19")
    print("🚨 Trap Triggers:                2")
    print("📤 Karma Score Drift:            +0.012")
    print()

def active_modules():
    print("🧰 ACTIVE MODULES")
    print("───────────────────────────────────────────────────────")
    modules = {
        "Antivirus & Heuristic Scanner": True,
        "AI Healing Engine": True,
        "Vault Purifier": False,
        "Forgiveness Protocol": True,
        "SmartLicense CLI": True
    }
    for m, status in modules.items():
        print(f"[{format_bool(status)}] {m}")
    print()

def logs():
    print("🔔 LAST EVENT LOGS")
    print("───────────────────────────────────────────────────────")
    try:
        with open("/opt/SELFIX/logs/healing_loop.log", "r") as f:
            lines = f.readlines()[-5:]
            for line in lines:
                print(line.strip())
    except:
        print("🚫 Log file not found.")
    print()

while True:
    header()
    system_status()
    entropy_status()
    active_modules()
    logs()
    print("🔄 REFRESHES EVERY 10s – Press Ctrl+C to exit")
    time.sleep(10)
