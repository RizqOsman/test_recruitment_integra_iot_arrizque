import paho.mqtt.client as mqtt
import time
import random
import logging
import json
import asyncio
from app.database import insert_reading

logger = logging.getLogger(__name__)

MIN_RETRY_TIME = 1
MAX_RETRY_TIME = 32

class MQTTService:
    def __init__(self, broker="localhost", port=1883, username=None, password=None):
        self.client = mqtt.Client()
        if username and password:
            self.client.username_pw_set(username, password)
        
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        
        self.broker = broker
        self.port = port
        self.retry_time = MIN_RETRY_TIME

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("MQTT: Connected") 
            self.retry_time = MIN_RETRY_TIME
            client.subscribe("site/+/device/+/telemetry", qos=1)
        else:
            logger.error(f"MQTT: Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            logger.info(f"Msg Received: {msg.topic} | Payload: {payload[:50]}...") 
            
            data = json.loads(payload)
            
            insert_reading(data['device_id'], data['ts'], data['temp'], data['hum'])
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def on_disconnect(self, client, userdata, rc):
        logger.warning("MQTT: Disconnected")
        self.reconnect_loop()

    def reconnect_loop(self):
        while not self.client.is_connected():
            try:
                logger.info(f"Attempting reconnect in {self.retry_time}s...")
                time.sleep(self.retry_time)
                self.client.reconnect()
            except Exception:
                sleep_time = min(self.retry_time * 2, MAX_RETRY_TIME)
                self.retry_time = sleep_time + random.uniform(0, 1) # Jitter

    def start(self):
        try:
            self.client.connect(self.broker, self.port)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"Initial connection failed: {e}")
            self.reconnect_loop()