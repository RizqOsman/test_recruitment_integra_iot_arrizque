import uvicorn
import os
from app.api import app
from app.mqtt_service import MQTTService

BROKER = os.getenv("BROKER_URL", "localhost")
PORT = int(os.getenv("BROKER_PORT", 1883))

if __name__ == "__main__":
    mqtt_service = MQTTService(broker=BROKER, port=PORT)
    mqtt_service.start()
    
    print("Starting API Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)