from fastapi import Header, HTTPException, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from cryptography.fernet import Fernet, InvalidToken
from app.core.config import settings
import dotenv
import base64

def get_session_id_from_token(
    x_session_token_header: str | None = Header(None, alias="x-session-token")
):
    x_session_token = x_session_token_header
    if x_session_token is None:
        raise HTTPException(
            status_code=400,
            detail="X-Session-Token header or cookie is missing."
        )
    """
    A FastAPI dependency that extracts, decrypts, and returns the session ID
    from the X-Session-Token header.
    """
    if not settings.FERNET_KEY:
        raise HTTPException(
            status_code=500,
            detail="Fernet key is not configured on the server."
        )

    try:
        # Clean the key to remove potential quotes and whitespace
        cleaned_key = settings.FERNET_KEY.strip().strip('"').strip("'")
        key = cleaned_key.encode()
        f = Fernet(key)
        
        # Decrypt the token from the header
        decrypted_bytes = f.decrypt(x_session_token.encode())
        decrypted_session_id = decrypted_bytes.decode()
        
        return decrypted_session_id

    except (InvalidToken, TypeError, base64.binascii.Error):
        raise HTTPException(
            status_code=400,
            detail="Invalid or malformed X-Session-Token header."
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the session token."
        )

http_bearer = HTTPBearer()

# def validate_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
#     """
#     A dependency that validates the static Fernet-encrypted bearer token.
#     """
#     if not settings.STATIC_BEARER_TOKEN:
#         raise HTTPException(
#             status_code=500,
#             detail="Bearer token is not configured on the server."
#         )
    
#     # Clean the expected token from .env to remove potential quotes and whitespace
#     expected_token = settings.STATIC_BEARER_TOKEN.strip().strip('"').strip("'")
    
#     if credentials.scheme != "Bearer" or credentials.credentials != expected_token:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid or missing bearer token.",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return True # Token is valid
