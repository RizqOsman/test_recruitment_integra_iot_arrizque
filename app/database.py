import sqlite3
import logging

from contextlib import contextmanager

DB_NAME = 'data.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT,
                temp_c REAL,
                hum_pct REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_device_ts ON sensor_data (device_id, timestamp)')

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn.cursor()
        conn.commit()
    finally:
        conn.close()  

def insert_reading(device_id, ts, temp_c, hum_pct):
    with get_db_connection() as cursor:
        cursor.execute("INSERT INTO sensor_data (device_id, temp_c, hum_pct, timestamp) VALUES (?, ?, ?, ?)",)
