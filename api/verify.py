from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import stripe
import os
from tools.signed_license_generator import generate_signed_license
from tools.license_validator import validate_license
from config import settings

router = APIRouter(prefix="/api", tags=["License Verification"])

stripe.api_key = settings.STRIPE_SECRET_KEY

# Optional: Product features mapping
FEATURES = {
    "home_free": ["GUI", "Scanner", "VPN", "Legal Logging"],
    "home_premium": ["GUI", "Scanner", "VPN", "Legal Logging"],
    "pro": ["AI Healing", "CLI", "Rollback Engine"],
    "team": ["Dashboard", "Vault", "AI Chat"],
    "enterprise": ["Seeder Agents", "GPG Vault", "Compliance Logs"]
}

# Download mapping per product
DOWNLOADS = {
    "home_free": "https://yourcdn.com/downloads/selfix-home-installer.zip",
    "home_premium": "https://yourcdn.com/downloads/selfix-home-premium.zip",
    "pro": "https://yourcdn.com/downloads/selfix-pro-suite.zip",
    "team": "https://yourcdn.com/downloads/selfix-team-suite.zip",
    "enterprise": "https://yourcdn.com/downloads/selfix-enterprise-tools.zip"
}

@router.get("/verify-payment")
async def verify_payment(session_id: str):
    try:
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status != "paid":
            raise HTTPException(status_code=402, detail="Payment not completed")

        customer_email = session.customer_email
        product_id = session.metadata.get("product_id")
        product_name = session.metadata.get("product_name", "Selfix Pro")

        # Generate and save license
        license_path = generate_signed_license(customer_email, product_name)

        # Validate license
        license_info = validate_license(license_path)
        if not license_info["valid"]:
            raise HTTPException(status_code=403, detail="Generated license invalid")

        # Get download link and features
        download_url = DOWNLOADS.get(product_id, "https://yourcdn.com/downloads/default.zip")
        included_features = FEATURES.get(product_id, [])

        return JSONResponse({
            "license": license_info,
            "license_file": license_path,
            "product_id": product_id,
            "product_name": product_name,
            "features": included_features,
            "download_url": download_url
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
