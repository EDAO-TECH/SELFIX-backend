import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

# Print to check if the keys are loaded correctly
print("Stripe Secret Key:", STRIPE_SECRET_KEY)
print("Stripe Publishable Key:", STRIPE_PUBLISHABLE_KEY)
