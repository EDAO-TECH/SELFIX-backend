from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from tools.license_validator import validate_license

router = APIRouter(prefix="/api", tags=["Activation"])

@router.post("/activate")
async def activate_license(request: Request):
    data = await request.json()
    license_path = data.get("license_path")

    if not license_path:
        raise HTTPException(status_code=400, detail="Missing license path")

    try:
        validation = validate_license(license_path)
        if not validation["valid"]:
            raise HTTPException(status_code=403, detail="Invalid or expired license")

        return JSONResponse({
            "message": "License activated successfully.",
            "product": validation["product"],
            "email": validation["email"],
            "expires": validation["expires"]
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
