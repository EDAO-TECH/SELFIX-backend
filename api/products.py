from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api", tags=["Products"])

@router.get("/products")
async def get_products():
    return JSONResponse([
        {
            "id": "selfix_basic",
            "name": "Selfix Antivirus Basic",
            "price": 999,
            "features": [
                "Real-time protection",
                "Manual scans",
                "Basic self-healing"
            ],
            "download": "selfix-basic.exe"
        },
        {
            "id": "selfix_pro",
            "name": "Selfix Antivirus Pro",
            "price": 2999,
            "features": [
                "Advanced AI healing",
                "Realtime cloud sync",
                "Priority license support"
            ],
            "download": "selfix-pro.exe"
        },
        {
            "id": "healing_toolkit",
            "name": "Selfix Healing Toolkit",
            "price": 1499,
            "features": [
                "Standalone healing scripts",
                "One-click malware rollback",
                "Offline use"
            ],
            "download": "selfix-healing-kit.zip"
        }
    ])
