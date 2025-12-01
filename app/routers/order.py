import httpx
from fastapi import APIRouter, HTTPException, Request
from app.core.config import settings
from app.core.dependencies import decrypt_session_token
from app.models.order import MCPBase

router = APIRouter(tags=["Actions"])


async def _list_orders(session_id: str):
    """Helper to fetch a list of orders from the backend."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{settings.BASE_URL}/webhook/orders",
                params={"session_id": session_id}
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Error connecting to the backend service: {exc}")
    except httpx.HTTPStatusError as exc:
        try:
            detail = exc.response.json()
        except Exception:
            detail = exc.response.text
        raise HTTPException(status_code=exc.response.status_code, detail=detail)

async def _get_order(order_number: str):
    """Helper to fetch a single order from the backend."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.BASE_URL}/webhook/orders/{order_number}")
            response.raise_for_status()
            if not response.content:
                raise HTTPException(status_code=404, detail=f"Order '{order_number}' not found in the backend.")
            return response.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Error connecting to the backend service: {exc}")
    except httpx.HTTPStatusError as exc:
        try:
            detail = exc.response.json()
        except Exception:
            detail = exc.response.text
        raise HTTPException(status_code=exc.response.status_code, detail=detail)


@router.get("/webhook/orders", name="list_orders_by_session", include_in_schema=False)
async def list_orders(request: Request):
    """(Internal) Retrieves a list of orders from the backend."""
    session_id = request.state.session_id
    return await _list_orders(session_id)

@router.get("/webhook/orders/{order_number}", name="get_order_internal", include_in_schema=False)
async def get_order(request: Request, order_number: str):
    """(Internal) Retrieves a single order from the backend."""
    # Middleware validates the session, so we just call the helper.
    return await _get_order(order_number)


# --- MCP Proxy Endpoints ---

@router.post("/mcp/list_orders", name="list_orders")
async def mcp_list_orders(payload: MCPBase):
    """(MCP) Retrieves a list of orders, using a session token from the request body."""
    try:
        session_id = decrypt_session_token(payload.session_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return await _list_orders(session_id)

@router.post("/mcp/get_order/{order_number}", name="get_order")
async def mcp_get_order(order_number: str, payload: MCPBase):
    """(MCP) Retrieves a single order, using a session token from the request body."""
    try:
        # We decrypt the token to ensure it's valid, even if not used by the backend call itself.
        decrypt_session_token(payload.session_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return await _get_order(order_number)