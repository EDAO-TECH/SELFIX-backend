import os
import json
import psutil
import shutil
import subprocess
from datetime import datetime

def run_hardware_check():
    status = {
        "timestamp": str(datetime.utcnow()),
        "hardware_ok": True,
        "issues": [],
        "mode_suggestion": "autonomous"
    }

    def check_cpu():
        try:
            output = subprocess.getoutput("sensors")
            if "Core 0" in output and "85.0°C" in output:
                status["hardware_ok"] = False
                status["issues"].append("CPU overheat risk")
            elif "No sensors found!" in output or "failed" in output.lower():
                status["issues"].append("CPU temperature sensors not available (virtual environment)")
            else:
                status["issues"].append("CPU check passed")
        except Exception as e:
            status["issues"].append("CPU check skipped: " + str(e))

    def check_disk():
        try:
            smart = subprocess.getoutput("smartctl -H /dev/sda")
            if "PASSED" not in smart:
                status["hardware_ok"] = False
                status["issues"].append("SMART disk test failed")
        except:
            status["issues"].append("SMART check unavailable")

    def check_ram():
        try:
            mem = psutil.virtual_memory()
            if mem.available < (mem.total * 0.1):
                status["issues"].append("Low available RAM")
        except:
            status["issues"].append("RAM check skipped")

    def check_disk_space():
        total, used, free = shutil.disk_usage("/")
        if used / total > 0.9:
            status["issues"].append("Disk usage over 90%")

    def detect_virtual_env():
        try:
            product = subprocess.getoutput("cat /sys/class/dmi/id/product_name")
            if "QEMU" in product or "Virtual" in product:
                status["issues"].append("Running in a virtual machine (QEMU detected)")
        except:
            pass

    check_cpu()
    check_disk()
    check_ram()
    check_disk_space()
    detect_virtual_env()

    if not status["hardware_ok"]:
        status["mode_suggestion"] = "quarantine"

    # Save log for UI/Audit
    with open("/opt/SELFIX/data/ai_phase_log.json", "w") as f:
        json.dump(status, f, indent=4)

    return status

# Optional CLI run
if __name__ == "__main__":
    result = run_hardware_check()
    print("🩺 Hardware Check Done")
    print("Suggested Mode:", result["mode_suggestion"])
    print("Issues:", result["issues"])
