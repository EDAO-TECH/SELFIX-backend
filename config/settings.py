import os
from dotenv import load_dotenv

# Load environment variables from .env file (optional)
load_dotenv()

# Stripe config
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_dummy")

# Frontend site (Netlify, etc.)
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://www.selfix.pro")

# Directories
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "downloads/")
LICENSE_PATH = os.getenv("LICENSE_PATH", "licenses/")

# Secret key for license signing
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-selfix-key")

# Optional: future DB or logging settings can go here
