import httpx
from fastapi import APIRouter, HTTPException, Request

from app.models.restaurant import RestaurantTicket
from app.core.config import settings

router = APIRouter(tags=["Actions"])

@router.post("/tickets/restaurant", name="create_restaurant_order")
async def forward_restaurant_ticket(
    request: Request,
    ticket: RestaurantTicket
):
    """
    Receives a restaurant ticket and forwards it to the internal backend,
    using the session_id from the authenticated request state.
    """
    session_id = request.state.session_id
    payload = {"session_id": session_id, **ticket.dict()}

    # # Map 'restaurant' category to 'room_service' for backend compatibility, as the backend rejects 'restaurant'.
    # if "orders" in payload:
    #     for order in payload["orders"]:
    #         if order.get("category") == "restaurant":
    #             order["category"] = "room_service"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.BASE_URL}/webhook/order",
                json=payload
            )
            response.raise_for_status()
            response_data = response.json()
            if "order_numbers" in response_data and isinstance(response_data.get("order_numbers"), list):
                response_data["order_numbers"] = [f"#{order}" for order in response_data["order_numbers"]]
            return response_data
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error connecting to the backend service: {exc}"
        )
    except httpx.HTTPStatusError as exc:
        try:
            detail = exc.response.json()
        except Exception:
            detail = exc.response.text
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=detail
        )