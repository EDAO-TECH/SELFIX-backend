import os
import stripe
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")  # Optional if using secret

@router.post("/api/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        if endpoint_secret:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        else:
            event = stripe.Event.construct_from(
                json.loads(payload.decode()), stripe.api_key
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 🎯 Handle successful checkout
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_email", "unknown")

        # 🚀 Generate or assign license key
        license_key = f"SELFIX-{os.urandom(8).hex().upper()}"
        license_path = f"/opt/SELFIX/licenses/{license_key}.key"

        os.makedirs("/opt/SELFIX/licenses", exist_ok=True)
        with open(license_path, "w") as f:
            f.write(license_key)

        # 🔐 Optionally: email it to customer_email or send webhook to Horizon
        print(f"✅ License key generated for {customer_email}: {license_key}")

    return JSONResponse(status_code=200, content={"status": "success"})
