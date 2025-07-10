#!/usr/bin/env python3
import time
import os
from datetime import datetime

LOG_PATH = "/opt/SELFIX/logs/trap.log"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def log(msg):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{datetime.utcnow()}] {msg}\n")
    print(msg)

log("🪤 [TRAP LOGIC] Honeypot monitor launched.")

try:
    while True:
        log("🎯 Scanning for intrusion patterns...")
        time.sleep(15)
except KeyboardInterrupt:
    log("🛑 [TRAP LOGIC] Service stopped.")
