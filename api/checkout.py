from fastapi import APIRouter, HTTPException, Request
router = APIRouter(prefix="/api", tags=["Checkout"])

# SELFIX product catalog with frontend pricing alignment
PRODUCTS = {
    "home_free": {
        "name": "Selfix Home (Free)",
        "price": 0
    },
    "home_premium": {
        "name": "Selfix Home Premium",
        "price": 500
    },
    "pro": {
        "name": "Selfix Pro",
        "price": 1200
    },
    "team": {
        "name": "Selfix Team",
        "price": 3900  # /user per month
    },
    "enterprise": {
        "name": "Selfix Enterprise",
        "price": 0  # Custom pricing handled offline
    },
    "healing_toolkit": {
        "name": "Selfix Healing Toolkit",
        "price": 1499
    }
}
