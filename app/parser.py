import struct
import logging

logger = logging.getLogger(__name__)

def calculate_crc16_ccitt_false(data: bytes) -> int:

    "(Poly 0x1021, Init 0xFFFF)"
    crc = 0xFFFF
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if (crc & 0x8000):
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc

def parse_packet(hex_str: str) -> dict:
    try:
        raw_data = bytes.fromhex(hex_str)
        
        if len(raw_data) != 10:
            raise ValueError("Invalid payload length")

        if raw_data[0] != 0x02 or raw_data[-1] != 0x03:
            raise ValueError("Invalid STX or ETX")

        payload_content = raw_data[1:7]
        crc_received_bytes = raw_data[7:9]
        
        crc_calculated = calculate_crc16_ccitt_false(payload_content)
        crc_received = int.from_bytes(crc_received_bytes, 'little')
        
        if crc_calculated != crc_received:
            logger.warning(f"CRC Mismatch: Calc {hex(crc_calculated)} vs Recv {hex(crc_received)}")
            raise ValueError("CRC Mismatch")

        device_id_val = int.from_bytes(raw_data[1:3], 'little')
        temp_raw = int.from_bytes(raw_data[3:5], 'little')
        hum_raw = int.from_bytes(raw_data[5:7], 'little')
        temp_c = temp_raw / 100.0
        hum_pct = hum_raw / 100.0

        return {
            "device_id": device_id_val,
            "temp_c": temp_c,
            "hum_pct": hum_pct
        }

    except Exception as e:
        logger.error(f"Error parsing packet: {e}")
        raise e