from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from app.database import get_latest_reading, init_db
import logging

init_db()

app = FastAPI(title="IoT Gateway API")

logging.basicConfig(level=logging.INFO)

class HealthResponse(BaseModel):
    status: str

@app.get("/healthz", response_model=HealthResponse) 
async def health_check():
    return {"status": "ok"}

@app.get("/devices/{device_id}/latest") 
async def get_device_latest(
    device_id: str = Path(..., min_length=4, max_length=16, pattern="^[a-zA-Z0-9]+$") 
):
    data = get_latest_reading(device_id)
    if not data:
        raise HTTPException(status_code=404, detail="Device data not found") 
    return data
