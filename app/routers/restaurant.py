import httpx
from fastapi import APIRouter, HTTPException, Request

from app.models.restaurant import RestaurantTicket, MCPRestaurantTicket
from app.core.config import settings
from app.core.dependencies import decrypt_session_token

router = APIRouter()


async def _forward_and_process_ticket(session_id: str, ticket_data: dict):
    """
    Helper function to forward a ticket to the backend and process the response.
    This ensures consistent logic for all entry points.
    """
    payload = {"session_id": session_id, **ticket_data}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.BASE_URL}/webhook/order",
                json=payload
            )
            response.raise_for_status()
            response_data = response.json()
            # Consistent response processing
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

@router.post("/tickets/restaurant", name="create_restaurant_ticket", include_in_schema=False)
async def forward_restaurant_ticket(
    request: Request,
    ticket: RestaurantTicket
):
    """
    Receives a restaurant ticket and forwards it to the internal backend,
    using the session_id from the authenticated request state.
    """
    session_id = request.state.session_id
    return await _forward_and_process_ticket(session_id, ticket.dict())


@router.post("/mcp/resto", name="order_food")
async def mcp_proxy_restaurant_ticket(
    ticket: MCPRestaurantTicket
):
    """
    A proxy endpoint for the MCP framework that accepts the session token
    in the request body and forwards it using the shared processing logic.
    """
    try:
        session_id = decrypt_session_token(ticket.session_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    ticket_data = ticket.dict(exclude={"session_token"})
    return await _forward_and_process_ticket(session_id, ticket_data)