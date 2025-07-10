from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api/health")
async def health_check():
    return {"status": "SELFIX API running"}
