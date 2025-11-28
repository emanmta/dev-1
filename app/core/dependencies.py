from fastapi import Header, HTTPException
from cryptography.fernet import Fernet, InvalidToken
from app.core.config import settings
import dotenv
import base64

def get_session_id_from_token(x_session_token: str = Header(...)):
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