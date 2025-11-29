import os
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# --- Konfigurasi ---
SESSION_ID_SAMPLE = "aeaa5d4d-3872-4b73-8a8c-b178bbc11824"
BEARER_PAYLOAD_SAMPLE = {"client_id": "letta_agent_service", "scope": "access_internal_api"}

def clean_key(key: str) -> bytes:
    """Removes quotes and whitespace, then encodes to bytes."""
    return key.strip().strip('"').strip("'").encode()

def generate_new_keys():
    """Generates and prints a new pair of Fernet keys."""
    print("--- Generate New Keys ---")
    fernet_key = Fernet.generate_key().decode()
    bearer_fernet_key = Fernet.generate_key().decode()
    print("Copy these new keys into your .env file:\n")
    print(f'FERNET_KEY="{fernet_key}"')
    print(f'BEARER_FERNET_KEY="{bearer_fernet_key}"')
    print("\n" + "="*40)

def generate_bearer_token():
    """Generates a static bearer token from the BEARER_FERNET_KEY in .env."""
    load_dotenv()
    bearer_key = os.getenv("BEARER_FERNET_KEY")
    if not bearer_key:
        print("Error: BEARER_FERNET_KEY not found in .env file. Please generate keys first.")
        return

    try:
        f = Fernet(clean_key(bearer_key))
        payload_bytes = json.dumps(BEARER_PAYLOAD_SAMPLE).encode()
        encrypted_token = f.encrypt(payload_bytes)
        
        print("--- Generate Static Bearer Token ---")
        print("Copy this token into your .env file and Letta secrets:\n")
        print(f'STATIC_BEARER_TOKEN="{encrypted_token.decode()}"')
        print("\n" + "="*40)
    except Exception as e:
        print(f"Error generating bearer token: {e}")

def encrypt_session_id():
    """Encrypts the sample session ID using the FERNET_KEY from .env."""
    load_dotenv()
    session_key = os.getenv("FERNET_KEY")
    if not session_key:
        print("Error: FERNET_KEY not found in .env file. Please generate keys first.")
        return

    try:
        f = Fernet(clean_key(session_key))
        encrypted_token = f.encrypt(SESSION_ID_SAMPLE.encode())
        
        print("--- Encrypt Session ID ---")
        print(f"Original Session ID: {SESSION_ID_SAMPLE}")
        print(f"Encrypted X-Session-Token: {encrypted_token.decode()}")
        print("\nUse this token in the X-Session-Token header for testing.")
        print("\n" + "="*40)
    except Exception as e:
        print(f"Error encrypting session ID: {e}")

def run_decryption_simulation():
    """Simulates how the FastAPI service decrypts both tokens."""
    load_dotenv()
    bearer_key_env = os.getenv("BEARER_FERNET_KEY")
    session_key_env = os.getenv("FERNET_KEY")
    static_token_env = os.getenv("STATIC_BEARER_TOKEN")

    if not all([bearer_key_env, session_key_env, static_token_env]):
        print("Error: Missing one or more keys/tokens in .env for full simulation.")
        return

    print("--- Decryption Simulation ---")
    
    # 1. Simulate Bearer Token validation
    print("\n1. Validating Bearer Token...")
    try:
        # In our app, we do a string compare, but here we'll decrypt to prove it works.
        f_bearer = Fernet(clean_key(bearer_key_env))
        decrypted_payload_bytes = f_bearer.decrypt(clean_key(static_token_env))
        decrypted_payload = json.loads(decrypted_payload_bytes)
        print(f"   - Success! Decrypted Bearer Token payload: {decrypted_payload}")
        assert decrypted_payload == BEARER_PAYLOAD_SAMPLE
    except Exception as e:
        print(f"   - FAILED to validate Bearer Token: {e}")

    # 2. Simulate Session Token decryption
    print("\n2. Decrypting X-Session-Token...")
    try:
        f_session = Fernet(clean_key(session_key_env))
        # First, create a sample encrypted token to decrypt
        encrypted_session_token = f_session.encrypt(SESSION_ID_SAMPLE.encode())
        print(f"   - Sample encrypted token: {encrypted_session_token.decode()}")
        
        decrypted_session_bytes = f_session.decrypt(encrypted_session_token)
        decrypted_id = decrypted_session_bytes.decode()
        print(f"   - Success! Decrypted Session ID: {decrypted_id}")
        assert decrypted_id == SESSION_ID_SAMPLE
    except Exception as e:
        print(f"   - FAILED to decrypt Session Token: {e}")
    
    print("\n" + "="*40)


def main():
    """Interactive menu for the crypto test script."""
    while True:
        print("\n--- Crypto Test Menu ---")
        print("1. Generate NEW Fernet Keys (do this first!)")
        print("2. Generate STATIC_BEARER_TOKEN (after setting keys in .env)")
        print("3. Encrypt a sample Session ID (for X-Session-Token)")
        print("4. Run full decryption simulation (verifies .env setup)")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            generate_new_keys()
        elif choice == '2':
            generate_bearer_token()
        elif choice == '3':
            encrypt_session_id()
        elif choice == '4':
            run_decryption_simulation()
        elif choice == '5':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()