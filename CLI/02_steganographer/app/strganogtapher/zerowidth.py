from cryptography.fernet import Fernet
from app.strganogtapher.characters import *


class ZeroWidthSteganographer:
    def __init__(self, key=None):
        # Generate a new key if one isn't provided
        self.key = key if key else Fernet.generate_key()
        self.cipher = Fernet(self.key)

    # --- 1. ENCRYPTION LAYER ---
    def encrypt_message(self, plain_text):
        return self.cipher.encrypt(plain_text.encode()).decode()

    def decrypt_message(self, encrypted_text):
        return self.cipher.decrypt(encrypted_text.encode()).decode()

    # --- 2. BINARY CONVERSION ---
    def text_to_binary(self, text):
        return "".join(format(ord(c), "08b") for c in text)

    def binary_to_text(self, binary_str):
        # Split binary string into chunks of 8 and convert back to characters
        chars = [
            chr(int(binary_str[i : i + 8], 2)) for i in range(0, len(binary_str), 8)
        ]
        return "".join(chars)

    # --- 3. STEGANOGRAPHY LAYER ---
    def hide(self, secret_message, cover_text):
        # 1. Encrypt the secret message
        encrypted_secret = self.encrypt_message(secret_message)

        # 2. Convert encrypted string to binary
        binary_secret = self.text_to_binary(encrypted_secret)

        # 3. Map binary to zero-width characters
        hidden_payload = ""
        for bit in binary_secret:
            hidden_payload += ZERO if bit == "0" else ONE

        # 4. Add delimiter so we know where to stop reading later
        hidden_payload += DELIM

        # 5. Inject the invisible payload into the cover text (right after the first character)
        if len(cover_text) > 0:
            stego_text = cover_text[0] + hidden_payload + cover_text[1:]
        else:
            stego_text = hidden_payload

        return stego_text

    def reveal(self, stego_text):
        hidden_binary = ""

        # 1. Extract zero-width characters until we hit the delimiter
        for char in stego_text:
            if char == ZERO:
                hidden_binary += "0"
            elif char == ONE:
                hidden_binary += "1"
            elif char == DELIM:
                break

        if not hidden_binary:
            return "No hidden message detected."

        try:
            # 2. Convert binary back to the encrypted string
            encrypted_secret = self.binary_to_text(hidden_binary)
            # 3. Decrypt the string
            return self.decrypt_message(encrypted_secret)
        except Exception as e:
            return f"Failed to decode or decrypt: Invalid key or corrupted data."
