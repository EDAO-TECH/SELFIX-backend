import json
from datetime import datetime
from pathlib import Path
import hashlib

LICENSE_PATH = "/opt/SELFIX/config/selfix_license.key"

def load_license():
    try:
        with open(LICENSE_PATH, 'r') as f:
            license_data = json.load(f)

        sig = license_data.get("signature", "")
        verify_data = {k: v for k, v in license_data.items() if k != "signature"}
        check_sig = hashlib.sha256(json.dumps(verify_data, sort_keys=True).encode()).hexdigest()

        if sig != check_sig:
            print("⚠️ Signature mismatch.")
            return None

        return license_data
    except Exception as e:
        print(f"[ERROR] Failed to load license: {e}")
        return None

def is_feature_enabled(feature):
    license_data = load_license()
    if not license_data:
        return False

    expiry = datetime.strptime(license_data["valid_until"], "%Y-%m-%d")
    if datetime.now() > expiry:
        print("🔒 License expired.")
        return False

    return feature in license_data["features"]

