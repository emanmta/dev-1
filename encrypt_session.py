import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# The session ID you want to encrypt
SESSION_ID_TO_ENCRYPT = "74cbec76-9fad-487b-9041-120a1c121f6f"

def encrypt_session():
    """
    Encrypts the predefined session ID using the Fernet key
    from the .env file.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get the Fernet key from the environment
    fernet_key = os.getenv("FERNET_KEY")

    if not fernet_key:
    
        print("Error: FERNET_KEY not found in .env file.")
        return

    try:
        # Clean the key to remove potential quotes and whitespace
        cleaned_key = fernet_key.strip().strip('"').strip("'")
        f = Fernet(cleaned_key.encode())
        
        # Encrypt the session ID
        encrypted_token = f.encrypt(SESSION_ID_TO_ENCRYPT.encode())
        
        print("--- Encryption Successful ---")
        print(f"Original Session ID: {SESSION_ID_TO_ENCRYPT}")
        print(f"Encrypted Token: {encrypted_token.decode()}")
        print("\nYou can now use this token to test the /sessions/decode endpoint.")


    except Exception as e:
        print(f"An error occurred during encryption: {e}")

if __name__ == "__main__":
    encrypt_session()
