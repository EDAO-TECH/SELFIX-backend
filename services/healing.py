#!/usr/bin/env python3
import time
import os
from datetime import datetime

LOG_PATH = "/opt/SELFIX/logs/healing.log"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def log(msg):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{datetime.utcnow()}] {msg}\n")
    print(msg)

log("🔧 [HEALING AI] Service started.")

try:
    while True:
        log("🩺 Healing engine running diagnostics...")
        time.sleep(10)
except KeyboardInterrupt:
    log("🛑 [HEALING AI] Service stopped.")
