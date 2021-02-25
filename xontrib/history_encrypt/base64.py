from base64 import b64decode, b64encode

base64_key = None

def base64_encode(message: bytes) -> bytes:
    return b64encode(message)

def base64_decode(token: bytes) -> bytes:
    return b64decode(token)