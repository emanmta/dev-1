import httpx
from fastapi import APIRouter, HTTPException, Depends

from app.models.complaint import ComplaintTicket
from app.core.config import settings
from app.core.dependencies import get_session_id_from_token

router = APIRouter()

@router.post("/tickets/complaint", name="create_complaint_ticket")
async def forward_complaint_ticket(
    ticket: ComplaintTicket,
    session_id: str = "eeaa7038-02d0-4a01-b5a1-1b7a83f55815"
):
    """
    Receives a complaint ticket, validates it, and forwards it
    to the internal backend service's order webhook.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.BASE_URL}/webhook/order",
                json={"session_id": session_id, **ticket.dict()}
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
