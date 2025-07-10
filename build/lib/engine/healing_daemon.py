#!/usr/bin/env python3

import os
import time
import json
import hashlib
import subprocess
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ────────── Config
WATCH_PATHS = ["/home", "/etc", "/opt/SELFIX"]
ENTROPY_LOG = "/opt/SELFIX/logs/entropy_events.log"
DAEMON_LOG = "/opt/SELFIX/logs/healing_daemon.log"
IGNORE_FILE = "/opt/SELFIX/config/daemon_ignore.json"
THROTTLE_SECONDS = 15

last_triggered = {}

def load_ignore_list():
    try:
        with open(IGNORE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

ignore_paths = load_ignore_list()

def should_ignore(path):
    return any(pattern in path for pattern in ignore_paths)

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
        now = time.time()

        if filepath in last_triggered and now - last_triggered[filepath] < THROTTLE_SECONDS:
            return

        last_triggered[filepath] = now

        if should_ignore(filepath):
            return

        hash_val = hash_file(filepath)
        event_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "file": filepath,
            "hash": hash_val,
            "action": "entropy_detected"
        }

        with open(ENTROPY_LOG, "a") as elog:
            elog.write(json.dumps(event_data) + "\n")
        with open(DAEMON_LOG, "a") as dlog:
            dlog.write(json.dumps(event_data) + "\n")

        subprocess.run(["python3", "/opt/SELFIX/rollback_manager.py", filepath])
        print(f"[+] Healing initiated for {filepath}")

def main():
    print("🛡️ Healing Daemon running... Monitoring for entropy changes.")
    observer = Observer()
    handler = HealingTriggerHandler()

    for path in WATCH_PATHS:
        if os.path.exists(path):
            observer.schedule(handler, path, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
