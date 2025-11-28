import httpx
from fastapi import APIRouter, HTTPException

from app.models.restaurant import RestaurantTicket
from app.core.config import settings

router = APIRouter()

@router.post("/tickets/restaurant", name="create_restaurant_ticket")
async def forward_restaurant_ticket(ticket: RestaurantTicket):
    """
    Receives a restaurant ticket, validates it, and forwards it
    to the internal backend service's order webhook.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.BASE_URL}/webhook/order",
                json=ticket.dict()
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