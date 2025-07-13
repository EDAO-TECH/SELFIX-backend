#!/usr/bin/env python3
import subprocess
import datetime

log_path = "/opt/SELFIX/logs/health_check.log"
services = ["glance", "selfix-av"]

def log_status(service, status):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as log:
        log.write(f"[{now}] {service}.service is {status}\n")

def check_service(service):
    try:
        output = subprocess.check_output(["systemctl", "is-active", f"{service}.service"], text=True).strip()
        log_status(service, output)
    except subprocess.CalledProcessError:
        log_status(service, "not found or error")

if __name__ == "__main__":
    for svc in services:
        check_service(svc)
