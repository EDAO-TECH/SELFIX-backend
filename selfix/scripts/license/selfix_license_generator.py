import json
import hashlib
from datetime import datetime
import argparse
from pathlib import Path

# Paths
TEMPLATE_PATH = str(Path(__file__).parent / "LICENSE_TEMPLATE.json")
OUTPUT_DIR = "/opt/SELFIX/config/"

# Signature using SHA256
def sha256_sig(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

# License generator function
def generate_license(email, license_type, features, device_limit, expiry_date):
    with open(TEMPLATE_PATH, 'r') as f:
        license_data = json.load(f)

    license_data.update({
        "user": email,
        "device_limit": device_limit,
        "features": features,
        "valid_until": expiry_date,
        "issued_on": str(datetime.today().date()),
        "license_type": license_type,
        "logo_url": "https://www.selfix.pro/static/media/selfix_logo.png"
    })

    # Generate signature (excluding signature field)
    license_data["signature"] = sha256_sig({k: v for k, v in license_data.items() if k != "signature"})

    # Save to file
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    output_path = Path(OUTPUT_DIR) / "selfix_license.key"
    with open(output_path, 'w') as f:
        json.dump(license_data, f, indent=4)

    print(f"✅ License for {email} saved to {output_path}")

# CLI entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SELFIX license.")
    parser.add_argument("--email", required=True)
    parser.add_argument("--type", default="Pro")
    parser.add_argument("--features", nargs="+", required=True)
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--expiry", default="2026-12-31")
    args = parser.parse_args()

    generate_license(args.email, args.type, args.features, args.limit, args.expiry)
