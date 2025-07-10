from fastapi import FastAPI, Request, HTTPException
import stripe
import json
import subprocess
import os

app = FastAPI()
stripe.api_key = "sk_test_..."  # ⬅️ Replace with your actual Stripe secret key
WEBHOOK_SECRET = "whsec_..."    # ⬅️ Replace with your actual webhook signing secret

@app.post("/api/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session["customer_details"]["email"]
        metadata = session.get("metadata", {})

        services = metadata.get("services", "AI_HEALING").split(",")
        license_key = metadata.get("license", f"AUTO-{customer_email[:6].upper()}")

        user_path = "/opt/SELFIX/data/users.json"
        users = {}

        if os.path.exists(user_path):
            with open(user_path) as f:
                users = json.load(f)

        users[customer_email] = {
            "license": license_key,
            "services": services,
            "paid_until": "2025-12-31"
        }

        with open(user_path, "w") as f:
            json.dump(users, f, indent=4)

        subprocess.Popen([
            "python3",
            "/opt/SELFIX/scripts/installer/activate_services.py",
            "--email", customer_email
        ])

        return {"status": "success", "activated": services}

    return {"status": "ignored"}

