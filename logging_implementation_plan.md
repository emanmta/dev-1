# Rencana Implementasi Logging Terpusat

Dokumen ini merinci langkah-langkah teknis untuk mengimplementasikan sistem logging terpusat di seluruh aplikasi FastAPI. Tujuannya adalah untuk mempermudah proses debugging, terutama untuk melacak error `422 Unprocessable Entity`.

## Langkah 1: Buat File Konfigurasi Logging

Buat file baru di `app/core/logging_config.py` dengan konten berikut. File ini akan menjadi satu-satunya sumber kebenaran (single source of truth) untuk semua konfigurasi logging.

```python
# app/core/logging_config.py

import logging.config
import sys

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

def setup_logging():
    """Terapkan konfigurasi logging."""
    logging.config.dictConfig(LOGGING_CONFIG)

```

## Langkah 2: Terapkan Konfigurasi di `app/main.py`

Modifikasi file `app/main.py` untuk memanggil fungsi `setup_logging()` saat aplikasi dimulai.

```python
# Di bagian atas app/main.py
from app.core.logging_config import setup_logging

# Panggil fungsi ini sebelum mendefinisikan 'app = FastAPI()'
setup_logging()

app = FastAPI(...)
# ... sisa kode Anda
```

## Langkah 3: Gunakan Logger di Routers

Tambahkan logging ke endpoint yang relevan untuk melacak permintaan masuk.

### `app/routers/waha.py`

```python
# Di bagian atas app/routers/waha.py
import logging
from fastapi import APIRouter, Request
from app.models.waha import WahaWebhook

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Actions"])

@router.post("/webhook/waha", name="waha_webhook")
async def waha_webhook(
    request: Request,
    payload: WahaWebhook
):
    """
    Webhook endpoint to receive callbacks from WAHA service.
    """
    logger.info(f"Menerima webhook dari WAHA untuk sesi: {payload.session}, event: {payload.event}")
    # ... sisa logika Anda
    return {"status": "ok", "message": "Webhook received"}
```

### `app/routers/message.py`

```python
# Di bagian atas app/routers/message.py
import logging
import httpx
from fastapi import APIRouter, HTTPException, Request
from app.models.message import SendMessage
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Actions"])

@router.post("/webhook/send-message", name="send_whatsapp_message")
async def send_whatsapp_message(
    request: Request,
    payload: SendMessage
):
    """
    Receives a message and forwards it to the internal backend service.
    """
    session_id = request.state.session_id
    logger.info(f"Menerima permintaan pengiriman pesan untuk session_id: {session_id}")
    
    # ... sisa logika Anda
```

## Langkah 4: (Kritis) Terapkan Logger untuk Debugging Error 422

Langkah ini adalah yang paling penting untuk menyelesaikan masalah awal. Kita perlu memodifikasi `app/integrations/waha/waha_service.py` untuk mencatat payload yang dikirim dan respons error yang diterima.

**Karena konten file ini belum tersedia, ini adalah contoh implementasi yang harus diterapkan:**

```python
# Di dalam app/integrations/waha/waha_service.py
import logging
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

class WahaService:
    # ... (metode lain)

    async def send_text_message(self, chat_id: str, text: str, session: str):
        url = f"{settings.WAHA_API_URL}/api/sendText"
        headers = {"X-Api-Key": settings.WAHA_API_KEY}
        payload = {"chatId": chat_id, "text": text}

        # === LOG PAYLOAD SEBELUM DIKIRIM ===
        logger.info(f"Mengirim permintaan ke WAHA. Session: {session}, URL: {url}, Payload: {payload}")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                logger.info(f"Pesan berhasil dikirim ke WAHA untuk session: {session}, chatId: {chat_id}")
                return response.json()
        except httpx.HTTPStatusError as e:
            # === LOG DETAIL ERROR DARI WAHA ===
            error_details = e.response.text
            logger.error(
                f"Gagal mengirim pesan ke WAHA. Status: {e.response.status_code}, "
                f"Session: {session}, Payload: {payload}, Detail Error: {error_details}"
            )
            raise Exception(f"Failed to send message: {e.response.status_code}. Details: {error_details}") from e
        except httpx.RequestError as e:
            logger.error(f"Request error saat menghubungi WAHA: {e}")
            raise Exception(f"Failed to connect to WAHA service: {e}") from e

```

Setelah rencana ini diimplementasikan, log aplikasi akan memberikan informasi yang tepat untuk mendiagnosis mengapa WAHA mengembalikan error `422`.