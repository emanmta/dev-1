import os
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv

# ==============================================================================
# == GANTI TOKEN DI BAWAH INI DENGAN TOKEN YANG INGIN ANDA DEKRIPSI ==
# ==============================================================================
TOKEN_TO_DECRYPT = "gAAAAABpL-5NxJqJ1RAUTaE1FOKvAgt7izZOD3hBLnbDBxiOeJUYBu-eGMYGkiHGUTuLUh3EqLJffLpFn4mZ23lcgDyw4cBcAWPBfng-nH6STdixZwaGab_ldzXv1kOpvz5glq3QeJKZ"
# ==============================================================================

def decrypt_token():
    """
    Mendekripsi token yang diberikan menggunakan FERNET_KEY dari file .env.
    """
    # Muat variabel lingkungan dari file .env
    load_dotenv()
    fernet_key = os.getenv("FERNET_KEY")

    if not fernet_key:
        print("Error: FERNET_KEY tidak ditemukan di file .env.")
        return

    try:
        # Bersihkan kunci dari spasi atau kutip yang tidak perlu
        cleaned_key = fernet_key.strip().strip('"').strip("'")
        f = Fernet(cleaned_key.encode())
        
        # Dekripsi token
        decrypted_bytes = f.decrypt(TOKEN_TO_DECRYPT.encode())
        decrypted_session_id = decrypted_bytes.decode()
        
        print("--- Dekripsi Berhasil ---")
        print(f"Token Terenkripsi: {TOKEN_TO_DECRYPT}")
        print(f"Hasil Dekripsi (Session ID): {decrypted_session_id}")

    except InvalidToken:
        print("\nError: Token tidak valid atau kunci salah. Dekripsi gagal.")
        print("Pastikan TOKEN_TO_DECRYPT sudah benar dan FERNET_KEY di .env sesuai dengan yang digunakan untuk enkripsi.")
    except Exception as e:
        print(f"Terjadi error saat dekripsi: {e}")

if __name__ == "__main__":
    decrypt_token()