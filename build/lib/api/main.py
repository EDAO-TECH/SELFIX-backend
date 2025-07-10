import os
from dotenv import load_dotenv
import stripe
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

# Load environment variables
load_dotenv()

# Stripe keys
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

# Set Stripe API key
stripe.api_key = STRIPE_SECRET_KEY

# FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="/opt/SELFIX/templates")

# Checkout page route (frontend)
@app.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    return templates.TemplateResponse("checkout.html", {
        "request": request,
        "stripe_key": STRIPE_PUBLISHABLE_KEY
    })

# Create Stripe session (backend API)
@app.post("/api/create-checkout-session")
async def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "SELFIX Subscription"},
                    "unit_amount": 1000,  # $10.00
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://www.selfix.pro/frontend/success.html",
            cancel_url="https://www.selfix.pro/frontend/cancel.html",
        )
        return JSONResponse({"url": session.url})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
