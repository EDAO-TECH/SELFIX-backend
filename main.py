from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

# Routers (import AFTER defining app)
from api import products, checkout, verify, download, activate

app = FastAPI(title="Selfix AV API")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use: [settings.FRONTEND_URL]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(products.router)
app.include_router(checkout.router)
app.include_router(verify.router)
app.include_router(download.router)
app.include_router(activate.router)

# Default root test route
@app.get("/")
def root():
    return {"message": "SELFIX Backend API is running"}
