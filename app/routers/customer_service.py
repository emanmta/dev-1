import httpx
import httpx
from fastapi import APIRouter, HTTPException, Request

from app.models.complaint import ComplaintTicket
from app.core.config import settings

router = APIRouter()

@router.post("/tickets/complaint", name="create_complaint_ticket")
async def forward_complaint_ticket(
    request: Request,
    ticket: ComplaintTicket
):
    """
    Receives a complaint ticket and forwards it to the internal backend,
    using the session_id from the authenticated request state.
    """
    session_id = request.state.session_id

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.BASE_URL}/webhook/order",
                json={"session_id": session_id, **ticket.dict()}
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
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json()
        )
