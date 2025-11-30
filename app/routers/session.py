from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from cryptography.fernet import Fernet, InvalidToken
from app.core.config import settings
from app.core.dependencies import validate_bearer_token
import base64

router = APIRouter()

class EncryptedSession(BaseModel):
    encrypted_session_id: str

class DecodedSession(BaseModel):
    session_id: str

@router.post("/sessions/decode", response_model=DecodedSession, name="decode_session")
async def decode_session_id(
    payload: EncryptedSession,
    is_authenticated: bool = Depends(validate_bearer_token)
):
    """
    Receives a Fernet-encrypted session ID, decrypts it,
    and returns the original session ID.
    """
    if not settings.FERNET_KEY:
        raise HTTPException(
            status_code=500,
            detail="Fernet key is not configured on the server."
        )

    try:
        # Ensure the key is a URL-safe base64 encoded string
        # Clean the key to remove potential quotes and whitespace from .env file
        cleaned_key = settings.FERNET_KEY.strip().strip('"').strip("'")
        key = cleaned_key.encode()
        f = Fernet(key)
        
        # Decrypt the token
        decrypted_bytes = f.decrypt(payload.encrypted_session_id.encode())
        decrypted_session_id = decrypted_bytes.decode()
        
        return DecodedSession(session_id=decrypted_session_id)

    except (InvalidToken, TypeError, base64.binascii.Error):
        raise HTTPException(
            status_code=400,
            detail="Invalid or malformed encrypted session ID."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred during decryption: {e}"
        )