import os
import stripe
import logging
import traceback
from dotenv import load_dotenv  # ✅ Load .env automatically
from fastapi import APIRouter, Request, HTTPException
from starlette.responses import JSONResponse

load_dotenv()  # ✅ Load .env file before reading os.getenv

# ---[ Setup ]---
router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # Load Stripe API key
logger = logging.getLogger(__name__)

@router.post("/checkout")
async def create_checkout_session(request: Request):
    try:
        # ---[ Parse JSON payload ]---
        data = await request.json()
        price_id = data.get("price_id") or os.getenv("STRIPE_PRICE_ID")

        if not price_id:
            raise HTTPException(status_code=400, detail="Missing price_id")

        # ---[ Create Stripe Checkout Session ]---
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url='https://selfix.pro/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://selfix.pro/cancel',
        )

        # ---[ Return Success Response ]---
        return JSONResponse({"id": session.id})

    except Exception as e:
        # ---[ Log Error with Full Traceback ]---
        error_msg = f"Stripe checkout error: {str(e)}"
        traceback.print_exc()
        logger.error(error_msg)
        return JSONResponse({"error": error_msg}, status_code=500)
