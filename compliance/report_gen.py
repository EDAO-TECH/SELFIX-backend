import json, os, platform, socket
from datetime import datetime

def generate():
    report = {
        "timestamp": datetime.now().isoformat(),
        "hostname": socket.gethostname(),
        "system": platform.platform(),
        "license": _get_license_info(),
        "trap_log_present": os.path.exists("/opt/SELFIX/reports/trap_log.json"),
        "last_heal_logs": _get_recent_logs(),
    }

    out_path = "/opt/SELFIX/reports/compliance.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    return f"✅ Compliance report saved to {out_path}"

def _get_license_info():
    try:
        from license import smartlicense
        return smartlicense.load_license()
    except:
        return {"status": "unknown", "tier": "unknown"}

def _get_recent_logs():
    path = "/opt/SELFIX/reports/"
    logs = [f for f in os.listdir(path) if f.startswith("heal_") or f.startswith("precheck_")]
    return logs[-3:] if logs else []
