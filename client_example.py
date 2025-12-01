import os
import requests
import json
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env (berguna untuk pengembangan lokal)
load_dotenv()

# 1. Ambil token dari environment secrets/variables.
# Pastikan nama variabel lingkungan di klien Anda (misalnya, 'X_SESSION_TOKEN')
# cocok dengan apa yang Anda atur di environment secrets Anda.
session_token = os.getenv("X_SESSION_TOKEN")

# 2. Lakukan validasi untuk memastikan token berhasil diambil.
if not session_token:
    print("Error: Environment variable X_SESSION_TOKEN tidak ditemukan.")
    # Hentikan eksekusi jika token tidak ada, karena request pasti akan gagal.
    exit()

# URL endpoint API Anda
api_url = "http://127.0.0.1:8000/tickets/restaurant"

# 3. Siapkan header untuk permintaan (request).
# Ini adalah bagian kunci: membuat dictionary untuk headers
# dan memasukkan token sesi ke dalamnya.
headers = {
    "Content-Type": "application/json",
    "X-Session-Token": session_token  # Token dari environment variable disisipkan di sini
}

# Data (payload) yang akan Anda kirim
payload = {
  "orders": [
    {
      "items": [
        {
          "title": "Nasi Goreng Spesial",
          "qty": 1
        }
      ],
      "additional_note": None,
      "category": "Halal",
      "note": None
    }
  ]
}

# 4. Kirim permintaan POST dengan header yang sudah disiapkan.
try:
    print(f"Mengirim request ke {api_url}...")
    # Mencetak header untuk verifikasi saat menjalankan skrip
    print(f"Headers yang dikirim: {headers}") 
    
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))

    # Periksa status code dari respons. Ini akan memunculkan error jika status 4xx atau 5xx.
    response.raise_for_status()

    # Jika berhasil, cetak respons dari server
    print("\n--- Request Berhasil ---")
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

except requests.exceptions.HTTPError as errh:
    print(f"\n--- Http Error ---: {errh}")
    print(f"Response Body: {errh.response.text}")
except requests.exceptions.RequestException as err:
    print(f"\n--- Terjadi Error ---: {err}")
