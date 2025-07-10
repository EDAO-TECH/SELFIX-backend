#!/usr/bin/env python3
import os
import json
import time
import socket
import psutil
import datetime
import requests

SIGNATURE_FILE = "/opt/SELFIX/antivirus/selfix_signatures.json"
QUARANTINE_DIR = "/opt/SELFIX/quarantine"
LOG_FILE = "/opt/SELFIX/logs/av.log"
CONFIG_FILE = "/opt/SELFIX/seeder/config.json"

SCAN_INTERVAL = 60  # seconds
DEFAULT_EXCLUDE = {'/proc', '/sys', '/dev', '/run', '/snap', '/var/lib', '/boot', '/lib/modules'}

def load_signatures():
    try:
        with open(SIGNATURE_FILE) as f:
            return json.load(f)
    except Exception:
        return []

def load_config():
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except Exception:
        return {}

def get_scan_paths():
    config = load_config()
    if "scan_paths" in config:
        return config["scan_paths"]
    # Default to safe discovery
    paths = [os.path.join('/', d) for d in os.listdir('/') if os.path.isdir(os.path.join('/', d))]
    return [p for p in paths if p not in DEFAULT_EXCLUDE]

def log_detection(event):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as log:
        log.write(json.dumps(event) + "\n")

def notify_hq(event, hq_url):
    try:
        requests.post(hq_url, json=event, timeout=5)
    except Exception:
        pass

def quarantine_file(filepath):
    os.makedirs(QUARANTINE_DIR, exist_ok=True)
    filename = os.path.basename(filepath)
    quarantined_path = os.path.join(QUARANTINE_DIR, filename + ".quarantined")
    if not os.path.exists(quarantined_path):
        os.rename(filepath, quarantined_path)
    return quarantined_path

def scan_files(scan_paths):
    threats = []
    signatures = load_signatures()
    for path in scan_paths:
        for root, _, files in os.walk(path):
            for file in files:
                if file in signatures:
                    full_path = os.path.join(root, file)
                    threats.append(full_path)
    return threats

def main():
    config = load_config()
    hq_url = config.get("hq_url")
    hostname = socket.gethostname()
    scan_paths = get_scan_paths()

    while True:
        threats = scan_files(scan_paths)
        for file in threats:
            quarantined_path = quarantine_file(file)
            event = {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "hostname": hostname,
                "file": quarantined_path,
                "signature": os.path.basename(file),
                "status": "quarantined"
            }
            log_detection(event)
            if hq_url:
                notify_hq(event, hq_url)

        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()
