#!/usr/bin/env python3

import time
import hashlib
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import subprocess

WATCH_PATHS = ["/home", "/etc", "/opt/SELFIX"]
ENTROPY_LOG = "/opt/SELFIX/logs/entropy_events.log"
DAEMON_LOG = "/opt/SELFIX/logs/daemon_log.json"

def hash_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

class HealingTriggerHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        print(f"[!] Change detected: {filepath}")
        hash_val = hash_file(filepath)

        event_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "file": filepath,
            "hash": hash_val,
            "action": "entropy_detected"
        }

        try:
            with open(ENTROPY_LOG, "a") as log:
                log.write(json.dumps(event_log) + "\n")
        except Exception as log_err:
            print(f"[ERROR] Failed to write to entropy log: {log_err}")

        try:
            subprocess.run(["python3", "/opt/SELFIX/rollback_manager.py", filepath])
            print(f"[+] Healing initiated for {filepath} (simulated)")
        except Exception as subprocess_err:
            print(f"[ERROR] Healing subprocess failed: {subprocess_err}")

def main():
    observer = Observer()
    handler = HealingTriggerHandler()

    for path in WATCH_PATHS:
        if os.path.exists(path):
            observer.schedule(handler, path, recursive=True)

    observer.start()
    print("🔁 Healing Daemon running... Monitoring for entropy.")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
