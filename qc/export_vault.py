import tarfile
from datetime import datetime

VAULT_DIR = "/opt/SELFIX/vault"
EXPORT_PATH = f"/opt/SELFIX/archive/selfix_vault_{datetime.now().strftime('%Y%m%d')}.tar.gz"

def export():
    try:
        with tarfile.open(EXPORT_PATH, "w:gz") as tar:
            tar.add(VAULT_DIR, arcname="vault")
        return f"✅ Vault exported to: {EXPORT_PATH}"
    except Exception as e:
        return f"❌ Vault export failed: {e}"
