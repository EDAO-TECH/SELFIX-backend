#!/usr/bin/env python3
import hashlib
import os

def get_machine_hash():
    try:
        hostname = open("/etc/hostname").read().strip()
        boot_time = os.stat("/proc/stat").st_ctime
        machine_hash = hashlib.sha256((hostname + str(int(boot_time))).encode()).hexdigest()
        return machine_hash[:16]
    except Exception as e:
        return f"ERROR: {e}"

if __name__ == "__main__":
    print("📎 SELFIX Machine ID (Hash):")
    print(get_machine_hash())
    print("\n➡️ Please send this value to your SELFIX vendor to activate your license.")
