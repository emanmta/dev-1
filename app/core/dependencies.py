from cryptography.fernet import Fernet, InvalidToken
from app.core.config import settings
import base64

def decrypt_session_token(encrypted_token: str) -> str:
    """
    Decrypts the provided Fernet-encrypted session token and returns the session ID.

    Args:
        encrypted_token: The encrypted session token.

    Returns:
        The decrypted session ID.

    Raises:
        ValueError: If the Fernet key is not configured, or if the token is
                    invalid, malformed, or fails decryption.
    """
    if not settings.FERNET_KEY:
        raise ValueError("Fernet key is not configured on the server.")

    try:
        cleaned_key = settings.FERNET_KEY.strip().strip('"').strip("'")
        key = cleaned_key.encode()
        f = Fernet(key)
        
        decrypted_bytes = f.decrypt(encrypted_token.encode())
        decrypted_session_id = decrypted_bytes.decode()
        
        return decrypted_session_id

    except (InvalidToken, TypeError, base64.binascii.Error) as e:
        raise ValueError(f"Invalid or malformed session token: {e}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred during decryption: {e}")
