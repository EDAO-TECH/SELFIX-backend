from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ---[ Import Routers ]---
from api import stripe_webhook
from api.stripe import create_checkout_session

# ---[ Initialize FastAPI App ]---
app = FastAPI(
    title="SELFIX API",
    description="Backend for SELFIX Cyber Healing System",
    version="1.0.0"
)

# ---[ Middleware: Allow Horizon Frontend ]---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://selfix.pro", "http://localhost:5173", "*"],  # Replace * with specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---[ Mount Stripe Routes ]---
app.include_router(create_checkout_session.router, prefix="/api/stripe")
app.include_router(stripe_webhook.router, prefix="/api/stripe")

# ---[ Health Check Route (Optional) ]---
@app.get("/")
def read_root():
    return {"message": "SELFIX backend is running."}
