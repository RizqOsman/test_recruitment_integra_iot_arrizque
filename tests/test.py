from fastapi.testclient import TestClient
from app.api import app
from app.parser import parse_packet
import pytest

client = TestClient(app)

def test_parse_packet_crc_error():
    invalid_crc_hex = "02123409205030FFFF03" 
    with pytest.raises(ValueError, match="CRC Mismatch"):
        parse_packet(invalid_crc_hex)

def test_get_latest_404():
    response = client.get("/devices/XXXX/latest")
    assert response.status_code == 404