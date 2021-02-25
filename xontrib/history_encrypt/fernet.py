from cryptography.fernet import Fernet

def fernet_key():
    print('[xontrib-history-encrypt] Enter the key or press enter to create new: ', end='')
    key = input()
    if not key.strip():
      key = Fernet.generate_key()
      print('[xontrib-history-encrypt] Save the key and use it next time: ', key.decode())
    return key

def fernet_encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def fernet_decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)
