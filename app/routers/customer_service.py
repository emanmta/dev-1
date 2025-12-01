import httpx
from fastapi import APIRouter, HTTPException, Request

from app.models.complaint import ComplaintTicket, MCPComplaintTicket
from app.core.config import settings
from app.core.dependencies import decrypt_session_token

router = APIRouter()


async def _forward_and_process_complaint(session_id: str, ticket_data: dict):
    """
    Helper function to forward a complaint ticket to the backend and process the response.
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

@router.post("/tickets/complaint", name="create_complaint_ticket", include_in_schema=False)
async def forward_complaint_ticket(
    request: Request,
    ticket: ComplaintTicket
):
    """
    Receives a complaint ticket and forwards it to the internal backend.
    """
    session_id = request.state.session_id
    return await _forward_and_process_complaint(session_id, ticket.dict())


@router.post("/mcp/complain", name="make_complaint")
async def mcp_proxy_complaint_ticket(
    ticket: MCPComplaintTicket
):
    """
    A proxy endpoint for the MCP framework for creating complaint tickets.
    """
    try:
        session_id = decrypt_session_token(ticket.session_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    ticket_data = ticket.dict(exclude={"session_token"})
    return await _forward_and_process_complaint(session_id, ticket_data)
