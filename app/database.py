import sqlite3
import logging
from contextlib import contextmanager

DB_NAME = "data.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS readings (
                device_id TEXT,
                ts INTEGER,
                temp REAL,
                hum REAL
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_device_ts ON readings(device_id, ts)')
        conn.commit()

@contextmanager
def get_db_cursor():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    try:
        yield conn.cursor()
        conn.commit()
    finally:
        conn.close()

def insert_reading(device_id, ts, temp, hum):
    with get_db_cursor() as cursor:
        cursor.execute(
            "INSERT INTO readings (device_id, ts, temp, hum) VALUES (?, ?, ?, ?)",
            (str(device_id), ts, temp, hum)
        )

def get_latest_reading(device_id):
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT device_id, ts, temp, hum FROM readings WHERE device_id = ? ORDER BY ts DESC LIMIT 1",
            (device_id,)
        )
        row = cursor.fetchone()
        if row:
            return {"device_id": row[0], "ts": row[1], "temp": row[2], "hum": row[3]}
        return None

def get_aggregated_data(device_id, start_ts, end_ts):
    query = """
    SELECT 
        (ts / 300) * 300 as bucket_start_ts, 
        AVG(temp) as avg_temp
    FROM readings
    WHERE device_id = ? AND ts >= ? AND ts <= ?
    GROUP BY bucket_start_ts
    ORDER BY bucket_start_ts ASC
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, (device_id, start_ts, end_ts))
        return cursor.fetchall()