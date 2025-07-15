import json
import hmac
import hashlib
from datetime import datetime
from config import settings
import os

SECRET_KEY = settings.SECRET_KEY.encode()

def validate_license(filepath: str) -> dict:
    if not os.path.exists(filepath):
        return {"valid": False, "reason": "License file not found."}

    with open(filepath, "r") as f:
        license_data = json.load(f)

    try:
        payload = f"{license_data['email']}|{license_data['product']}|{license_data['issued']}|{license_data['expires']}"
        expected_signature = hmac.new(SECRET_KEY, payload.encode(), hashlib.sha256).hexdigest()

        if license_data["signature"] != expected_signature:
            return {"valid": False, "reason": "Invalid signature — file may have been tampered with."}

        # Check expiration
        expires = datetime.strptime(license_data["expires"], "%Y-%m-%d")
        if datetime.utcnow() > expires:
            return {"valid": False, "reason": "License has expired."}

        return {
            "valid": True,
            "email": license_data["email"],
            "product": license_data["product"],
            "expires": license_data["expires"]
        }

    except Exception as e:
        return {"valid": False, "reason": f"Error parsing license: {e}"}
