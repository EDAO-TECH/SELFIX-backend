import os
import stripe
from fastapi import APIRouter, Request, HTTPException
from starlette.responses import Response

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # 🔁 Handle subscription-related events here
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("✅ Payment received:", session["id"])
        # TODO: Activate license or log user

    return Response(status_code=200)
