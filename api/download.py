from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse
from tools.license_validator import validate_license
import os

router = APIRouter(prefix="/api", tags=["Download"])

DOWNLOAD_MAP = {
    "Selfix Antivirus Pro": "downloads/selfix_antivirus_pro_installer.zip",
    "Selfix Home Premium": "downloads/selfix_home_premium_installer.zip",
    "Selfix Team": "downloads/selfix_team_kit.zip",
    "Selfix Enterprise": "downloads/selfix_enterprise_suite.zip"
}

LICENSES_DIR = "licenses"

@router.post("/download")
async def download_product(request: Request):
    data = await request.json()
    license_key = data.get("license_key")

    if not license_key:
        raise HTTPException(status_code=400, detail="License key is required")

    # 🔍 Search for matching license file
    matching_file = None
    for filename in os.listdir(LICENSES_DIR):
        full_path = os.path.join(LICENSES_DIR, filename)
        with open(full_path, 'r') as f:
            content = f.read().strip()
            if content == license_key.strip():
                matching_file = full_path
                break

    if not matching_file:
        raise HTTPException(status_code=404, detail="License key not found")

    validation = validate_license(matching_file)
    if not validation["valid"]:
        raise HTTPException(status_code=403, detail="Invalid or expired license")

    product_name = validation["product"]
    download_file = DOWNLOAD_MAP.get(product_name)

    if not download_file or not os.path.exists(download_file):
        raise HTTPException(status_code=404, detail="Download not available for this product")

    return FileResponse(path=download_file, filename=os.path.basename(download_file), media_type='application/zip')
