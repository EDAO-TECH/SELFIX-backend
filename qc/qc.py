import importlib
import hashlib
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

VAULT_DIR = "/opt/SELFIX/vault"
QC_DIR = "/opt/SELFIX/qc/certified"
HEAL_DIR = "/opt/SELFIX/heal"

def get_healing_module(module_name):
    try:
        return importlib.import_module(f"heal.{module_name}"), None
    except Exception as e:
        return None, f"❌ Could not load heal.{module_name}: {e}"

def sign_cert(cert_path):
    try:
        subprocess.run([
            "gpg", "--yes", "--batch", "--output",
            f"{cert_path}.asc", "--armor", "--sign", cert_path
        ], check=True)
        return f"✅ GPG signature created: {cert_path}.asc"
    except subprocess.CalledProcessError as e:
        return f"❌ Failed to GPG-sign: {e}"

def run_qc(module_name, inspector="anonymous"):
    mod, err = get_healing_module(module_name)
    if not mod:
        return err

    try:
        if hasattr(mod, "main"):
            result = mod.main()
        elif hasattr(mod, "heal"):
            result = mod.heal()
        else:
            return f"❌ Module '{module_name}' has no 'main()' or 'heal()' method."
    except Exception as e:
        return f"❌ Error running module: {e}"

    path = Path(HEAL_DIR) / f"{module_name}.py"
    if not path.exists():
        return f"❌ Module file not found at {path}"
    with open(path, "rb") as f:
        code_hash = hashlib.sha256(f.read()).hexdigest()

    cert = {
        "module": module_name,
        "status": "PASSED",
        "inspector": inspector,
        "timestamp": datetime.utcnow().isoformat(),
        "hash": code_hash,
        "result": str(result)
    }

    os.makedirs(QC_DIR, exist_ok=True)
    cert_path = Path(QC_DIR) / f"{module_name}_cert.json"
    with open(cert_path, "w") as f:
        json.dump(cert, f, indent=2)

    sign_msg = sign_cert(cert_path)
    return f"✅ QC passed for {module_name}.\n{sign_msg}"
