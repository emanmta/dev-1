import httpx
import httpx
from fastapi import APIRouter, HTTPException, Request
from uuid import UUID

from app.core.config import settings

router = APIRouter()

@router.get("/webhook/orders", name="list_orders_by_session")
async def list_orders(
    request: Request
):
    """
    Retrieves a list of orders from the backend, filtered by the session_id
    from the authenticated request state.
    """
    session_id = request.state.session_id

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{settings.BASE_URL}/webhook/orders",
                params={"session_id": session_id}
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

@router.get("/webhook/orders/{order_number}", name="get_order")
async def get_order(
    request: Request,
    order_number: str
):
    """
    Retrieves a single order from the backend by its order_number.
    The request is authenticated by the session middleware.
    """
    # The middleware has already validated the session.
    # We can proceed directly with the business logic.
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{settings.BASE_URL}/webhook/orders/{order_number}"
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