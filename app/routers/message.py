import httpx
from fastapi import APIRouter, HTTPException

from app.models.message import SendMessage
from app.core.config import settings

router = APIRouter()

@router.post("/send-message", name="send_whatsapp_message")
async def forward_send_message(payload: SendMessage):
    """
    Receives a message payload, validates it, and forwards it
    to the internal backend service.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.BASE_URL}/send-message",
                json=payload.dict()
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error connecting to the backend service: {exc}"
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json()
        )