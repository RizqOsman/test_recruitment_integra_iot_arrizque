# IoT Gateway API

Project ini adalah gateway API untuk menerima dan menyimpan data dari perangkat IoT melalui protokol MQTT.

## Apa itu project ini?

Project ini menghubungkan perangkat IoT dengan database melalui:
- **MQTT**: Menerima data dari perangkat IoT (suhu, kelembaban, dll)
- **FastAPI**: Menyediakan REST API untuk mengakses data
- **Database**: Menyimpan data dari perangkat

## Setup Awal

### 1. Persiapan
Pastikan Anda sudah punya Python 3.8+ terinstall di komputer.

### 2. Clone project atau extract folder
```bash
cd /path/ke/project
```

### 3. Buat virtual environment (opsional tapi recommended)
```bash
python -m venv venv
source venv/bin/activate  # Untuk Mac/Linux
# atau
venv\Scripts\activate  # Untuk Windows
```

### 4. Install dependencies
```bash
pip install -r requirement.txt
```

## Cara Menjalankan

### 1. Setup MQTT Broker (opsional)
Jika Anda punya MQTT broker lokal, set environment variable:
```bash
export BROKER_URL=localhost
export BROKER_PORT=1883
```

Atau gunakan broker default (localhost:1883).

### 2. Jalankan project
```bash
python main.py
```

Program akan:
- Menghubungkan ke MQTT broker
- Menjalankan API server di http://localhost:8000

## API Endpoints

### Health Check
```
GET /healthz
```
Response:
```json
{
  "status": "ok"
}
```

### Get Latest Data dari Device
```
GET /devices/{device_id}/latest
```

Contoh:
```
GET /devices/device123/latest
```

Response:
```json
{
  "device_id": "device123",
  "ts": "2025-12-04T10:30:00",
  "temp": 25.5,
  "hum": 60
}
```

## Struktur Project

```
├── main.py              # File utama untuk menjalankan project
├── requirement.txt      # Daftar package yang diperlukan
├── app/
│   ├── api.py          # FastAPI endpoints
│   ├── config.py       # Konfigurasi
│   ├── database.py     # Fungsi database
│   └── mqtt_service.py # MQTT client dan subscriber
└── tests/
    └── test.py         # Unit tests
```

## Testing

Jalankan test:
```bash
pytest tests/
```

## Environment Variables

- `BROKER_URL` - URL MQTT broker (default: localhost)
- `BROKER_PORT` - Port MQTT broker (default: 1883)

## Troubleshooting

**Koneksi MQTT gagal?**
- Pastikan MQTT broker sudah running
- Cek URL dan port broker sudah benar
- Lihat log error di terminal

**API tidak bisa diakses?**
- Pastikan port 8000 belum digunakan program lain
- Cek apakah ada error saat startup

**Data tidak masuk database?**
- Pastikan MQTT broker terhubung
- Cek format message yang dikirim dari device sudah sesuai JSON
