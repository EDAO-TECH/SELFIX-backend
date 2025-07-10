#!/usr/bin/env python3
import json
import socket
import requests
import psutil
import time
import os
import sys

CONFIG_FILE = "/opt/SELFIX/seeder/config.json"
SLEEP_SECONDS = 30  # interval between heartbeats

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Config file not found: {CONFIG_FILE}")
        sys.exit(1)
    with open(CONFIG_FILE) as f:
        return json.load(f)

def collect_status():
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "uptime": time.time() - psutil.boot_time()
    }

def send_to_hq(hq_url, payload):
    try:
        res = requests.post(hq_url, json=payload, timeout=5)
        res.raise_for_status()
        print(f"✅ Status sent to HQ ({res.status_code})")
    except Exception as e:
        print(f"❌ Failed to contact HQ: {e}")

def main():
    config = load_config()
    hq_url = config.get("hq_url")
    if not hq_url:
        print("❌ HQ URL is missing in config.")
        sys.exit(1)

    hostname = socket.gethostname()
    print(f"📡 Seeder Agent started on host: {hostname}")
    print(f"🔁 Sending status every {SLEEP_SECONDS} seconds...")

    while True:
        status = collect_status()
        payload = {"hostname": hostname, "status": status}
        send_to_hq(hq_url, payload)
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
