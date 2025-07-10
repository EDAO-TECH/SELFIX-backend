# /opt/SELFIX/app/routes/stripe_checkout.py

from fastapi import APIRouter, Request
import stripe
import os

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # or hardcode for now

@router.post("/api/create-checkout-session")
async def create_checkout_session(data: dict):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                'price': data['priceId'],
                'quantity': 1,
            }],
            mode='subscription',
            success_url="https://yourdomain.com/success",
            cancel_url="https://yourdomain.com/cancel",
        )
        return {"id": session.id}
    except Exception as e:
        return {"error": str(e)}
