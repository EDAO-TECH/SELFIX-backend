from fastapi import APIRouter, Request
from stripe import checkout, error, Customer, api_key
import os

router = APIRouter()

api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/api/create-checkout-session")
async def create_checkout_session(data: dict):
    try:
        session = checkout.Session.create(
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
    except error.StripeError as e:
        return {"error": str(e)}

