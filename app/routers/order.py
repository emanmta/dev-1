import httpx
from fastapi import APIRouter, HTTPException
from uuid import UUID

from app.core.config import settings

router = APIRouter()

@router.get("/webhook/orders", name="list_orders_by_session")
async def list_orders(session_id: UUID):
    """
    Retrieves a list of orders from the backend, filtered by session_id.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{settings.BASE_URL}/webhook/orders",
                params={"session_id": str(session_id)}
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

@router.get("/webhook/orders/{order_number}", name="get_order_detail")
async def get_order_detail(order_number: str):
    """
    Retrieves a single order from the backend by its order_number.
    """
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