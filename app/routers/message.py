import httpx
import logging
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
    Receives a message, retrieves the session from the request state,
    gets the user's phone number, and sends the message via WAHA.
    """
    session_id = request.state.session_id

    # Logger
    logger.info(f"Received send message request for session_id: {session_id}, with message:'{payload.message}'")
    
    # Forward the request to the internal backend service
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.BASE_URL}/webhook/send-message",
                json={"session_id": str(session_id), "message": payload.message}
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        logger.error(f"Request error while connecting to backend: {exc}")
        raise HTTPException(
            status_code=502,
            detail=f"Error connecting to the backend service: {exc}"
        )
    except httpx.HTTPStatusError as exc:
        try:
            detail = exc.response.json()
        except Exception:
            detail = exc.response.text
        logger.error(f"Backend service returned an error: {detail}")
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=detail
        )