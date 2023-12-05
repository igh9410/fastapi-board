import os
import base64

secret_key = base64.urlsafe_b64encode(os.urandom(32)).decode()  # Generates a 32-byte (256-bit) key
print(secret_key)
