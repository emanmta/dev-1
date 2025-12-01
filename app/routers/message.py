import httpx
import httpx
from fastapi import APIRouter, HTTPException, Request

from app.models.message import SendMessage
from app.core.config import settings

router = APIRouter(tags=["Actions"])

@router.post("/webhook/send-message", name="send_whatsapp_message")
async def forward_send_message(
    request: Request,
    payload: SendMessage
):
    """
    Receives a message payload and forwards it to the internal backend,
    using the session_id from the authenticated request state.
    """
    session_id = request.state.session_id

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.BASE_URL}/webhook/send-message",
                json={"session_id": session_id, **payload.dict()}
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