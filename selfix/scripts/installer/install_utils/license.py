# Validates SELFIX license or trial status
import json
import os
from datetime import datetime

USER_DB = "/opt/SELFIX/data/users.json"

def load_user(email=None, license_key=None):
    if not os.path.exists(USER_DB):
        return None, "User DB not found"

    with open(USER_DB) as f:
        users = json.load(f)

    for user_email, data in users.items():
        if (email and user_email == email) or (license_key and data.get("license") == license_key):
            return data, None

    return None, "User not found"

def is_license_valid(user):
    if not user.get("license"):
        return False, "No license provided"

    exp = user.get("paid_until")
    if not exp:
        return False, "License expiry not set"

    try:
        expiry_date = datetime.fromisoformat(exp).date()
        if datetime.utcnow().date() <= expiry_date:
            return True, "License is valid"
        else:
            return False, "License expired"
    except ValueError:
        return False, "Invalid expiry format"

def is_trial_valid(user):
    if not user.get("trial_start") or not user.get("expires"):
        return False, "Trial fields missing"

    try:
        expiry_date = datetime.fromisoformat(user["expires"]).date()
        if datetime.utcnow().date() <= expiry_date:
            return True, "Trial is valid"
        else:
            return False, "Trial expired"
    except ValueError:
        return False, "Invalid date format"

def get_allowed_features(user):
    return user.get("services", [])

# Optional CLI test
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--email")
    parser.add_argument("--license")
    args = parser.parse_args()

    user, err = load_user(email=args.email, license_key=args.license)
    if not user:
        print(f"[❌] {err}")
        exit(1)

    if user.get("license"):
        valid, reason = is_license_valid(user)
    else:
        valid, reason = is_trial_valid(user)

    print(f"[{'✅' if valid else '❌'}] {reason}")
    print(f"[🔓] Features: {get_allowed_features(user)}")
