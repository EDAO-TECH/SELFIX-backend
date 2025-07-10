import shutil
import subprocess
import os
from pathlib import Path

QC_DIR = "/opt/SELFIX/qc/certified"
VAULT_DIR = "/opt/SELFIX/vault"
HEAL_DIR = "/opt/SELFIX/heal"

def verify_gpg_signature(cert_path):
    try:
        subprocess.run([
            "gpg", "--verify", f"{cert_path}.asc", cert_path
        ], check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def promote(module_name):
    cert_path = Path(QC_DIR) / f"{module_name}_cert.json"
    sig_path = Path(f"{cert_path}.asc")
    source_path = Path(HEAL_DIR) / f"{module_name}.py"
    dest_path = Path(VAULT_DIR) / f"{module_name}.py"

    if not cert_path.exists() or not sig_path.exists():
        return "❌ Missing QC cert or GPG signature. Run `selfix qc <module>` first."

    if not verify_gpg_signature(cert_path):
        return "❌ GPG signature verification failed. Promotion aborted."

    if not source_path.exists():
        return "❌ Healing module not found."

    os.makedirs(VAULT_DIR, exist_ok=True)
    shutil.copy2(source_path, dest_path)
    shutil.copy2(cert_path, Path(VAULT_DIR) / f"{module_name}_cert.json")
    shutil.copy2(sig_path, Path(VAULT_DIR) / f"{module_name}_cert.json.asc")

    return f"✅ Module '{module_name}' promoted to Golden Vault."
