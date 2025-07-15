import json
import os
import time
import hmac
import hashlib
from datetime import datetime, timedelta
from config import settings

SECRET_KEY = settings.SECRET_KEY.encode()
LICENSE_DIR = settings.LICENSE_PATH

def generate_signed_license(email: str, product: str, duration_days=365) -> str:
    issued_at = datetime.utcnow()
    expires_at = issued_at + timedelta(days=duration_days)

    license_data = {
        "email": email,
        "product": product,
        "issued": issued_at.strftime("%Y-%m-%d"),
        "expires": expires_at.strftime("%Y-%m-%d")
    }

    # Create signature
    payload = f"{email}|{product}|{license_data['issued']}|{license_data['expires']}"
    signature = hmac.new(SECRET_KEY, payload.encode(), hashlib.sha256).hexdigest()
    license_data["signature"] = signature

    # Save to file
    filename = f"{email}-{product}.license".replace(" ", "_")
    filepath = os.path.join(LICENSE_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(license_data, f, indent=4)

    return filepath
