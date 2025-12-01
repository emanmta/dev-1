from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.core.dependencies import decrypt_session_token

class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Bypass middleware for the root path and docs
        # Bypass middleware for the root path and docs
        if request.url.path in ["/", "/docs", "/openapi.json"]:
            return await call_next(request)

        encrypted_token = request.headers.get("x-session-token")

        if not encrypted_token:
            return JSONResponse(
                status_code=401,
                content={"detail": "X-Session-Token header is missing."}
            )

        try:
            session_id = decrypt_session_token(encrypted_token)
            request.state.session_id = session_id
        except Exception:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or malformed session token."}
            )
        
        response = await call_next(request)
        return response