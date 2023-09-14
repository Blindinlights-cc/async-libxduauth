from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode


def aec_cbc_encrypt(p: str, k: str) -> str:
    password: bytes = p.encode('utf-8')
    salt: bytes = k.encode('utf-8')

    crypt = AES.new(salt, AES.MODE_CBC, b'xidianscriptsxdu')
    padding = pad(b'xidianscriptsxdu' * 4 + password, 16)
    return b64encode(crypt.encrypt(padding)).decode('utf-8')


def aes_ecb_encrypt(p: str, k: str) -> str:
    password: bytes = p.encode('utf-8')
    key: bytes = k.encode('utf-8')

    ciper = AES.new(key, AES.MODE_ECB)
    return b64encode(ciper.encrypt(pad(password, 16))).decode('utf-8')
