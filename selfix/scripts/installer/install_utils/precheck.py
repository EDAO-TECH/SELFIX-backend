# installer/install_utils/precheck.py
import platform
import shutil
import socket
import subprocess
import logging
import os
import sys

try:
    import psutil
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

LOG_FILE = "/opt/SELFIX/logs/precheck.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='[%(asctime)s] %(message)s')

def check_os():
    dist = platform.system()
    version = platform.version()
    pretty = platform.platform()
    logging.info(f"OS: {pretty}")
    print(f"[✅] OS Detected: {pretty}")
    return {"os": dist, "version": version, "pretty": pretty}

def check_python():
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"[✅] Python version: {version.major}.{version.minor}")
    else:
        print(f"[❌] Python 3.8+ required, found {version.major}.{version.minor}")
        sys.exit(1)
    return {"python_version": f"{version.major}.{version.minor}"}

def check_pip():
    pip_path = shutil.which("pip3")
    if pip_path:
        print(f"[✅] pip3 found: {pip_path}")
    else:
        print("[❌] pip3 is not installed.")
        sys.exit(1)

def check_resources():
    ram = round(psutil.virtual_memory().total / (1024 * 1024))
    disk = shutil.disk_usage("/").free // (1024 * 1024 * 1024)
    print(f"[✅] RAM: {ram} MB")
    print(f"[✅] Free Disk: {disk} GB")
    return {"ram_mb": ram, "disk_gb": disk}

def check_package(pkg):
    result = shutil.which(pkg)
    if result:
        print(f"[✅] Package `{pkg}` found.")
        return True
    else:
        print(f"[⚠️] Package `{pkg}` not found.")
        return False

def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        print("[✅] Internet connection OK")
        return True
    except socket.error as ex:
        print(f"[⚠️] No internet access: {ex}")
        return False

def check_systemd():
    result = shutil.which("systemctl")
    if result:
        print("[✅] systemd found")
    else:
        print("[⚠️] systemd not available")

def run_full_check():
    print("\n🔍 Starting SELFIX System Precheck...\n")
    os.makedirs("/opt/SELFIX/logs", exist_ok=True)

    summary = {
        "os": check_os(),
        "python": check_python(),
        "pip": check_pip(),
        "resources": check_resources(),
        "packages": {
            "nginx": check_package("nginx"),
            "gunicorn": check_package("gunicorn"),
            "curl": check_package("curl"),
        },
        "internet": check_internet(),
        "systemd": check_systemd()
    }

    logging.info("Precheck summary:")
    for k, v in summary.items():
        logging.info(f"{k}: {v}")

    print("\n✅ Precheck complete. Log saved to:")
    print(f"   {LOG_FILE}")

    return summary

if __name__ == "__main__":
    run_full_check()
