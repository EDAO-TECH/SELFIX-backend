import json
import os
from pathlib import Path
from datetime import datetime

LICENSE_PATH = Path("/opt/SELFIX/license/smartlicense.json")
TIERS = ["Lite", "Pro", "Enterprise", "NFT"]

class LicenseError(Exception):
    pass

def load_license():
    if not LICENSE_PATH.exists():
        raise LicenseError("❌ License file not found.")

    with open(LICENSE_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise LicenseError("❌ License file is corrupted.")

    if "tier" not in data or data["tier"] not in TIERS:
        raise LicenseError("❌ Invalid or missing license tier.")

    if "activated" not in data or not data["activated"]:
        raise LicenseError("❌ License not activated.")

    if data.get("expires"):
        expires = datetime.fromisoformat(data["expires"])
        if datetime.now() > expires:
            raise LicenseError("❌ License expired.")

    return data

def check_license_tier():
    try:
        data = load_license()
        return data["tier"]
    except LicenseError as e:
        print(str(e))
        return None

def print_license_status():
    try:
        data = load_license()
        print(f"✅ License: {data['tier']} Edition")
        print(f"🔑 Issued to: {data.get('issued_to', 'Unknown')}")
        if data.get("expires"):
            print(f"📅 Expires: {data['expires']}")
        else:
            print("♾️ Lifetime license")
    except LicenseError as e:
        print(str(e))
