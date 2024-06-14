import base64
import hashlib
import os
import rsa
from cryptography.fernet import Fernet


def creating_keys(key_length: int = 4096):
    public_key, private_key = rsa.newkeys(key_length)
    write_key_to_file(public_key, "public.pem")
    write_key_to_file(private_key, "private.pem")


def get_key_from_pin(pin: str):
    key = hashlib.sha256(pin.encode()).digest()
    key = base64.urlsafe_b64encode(key)
    #with open("mykey.key", "wb") as f:
    #    f.write(key)
    return key


def write_key_to_file(key, file_name: str):
    with open(file_name, "wb") as f:
        f.write(key.save_pkcs1("PEM"))


def encrypting_key(aes_key: bytes):
    with open("private.pem", "rb") as private_pem:
        private_key = private_pem.read()
    key = Fernet(aes_key)
    encrypted = key.encrypt(private_key)

    with open("private.pem", "wb") as encrypted_file:
        encrypted_file.write(encrypted)


def decrypting_key(key_path: str, aes_key: bytes):
    with open(key_path, "rb") as encrypted_file:
        encrypted = encrypted_file.read()
    key = Fernet(aes_key)
    return key.decrypt(encrypted)
    # with open("private.pem", "wb") as decrypted_file:
    #    decrypted_file.write(decrypted)


if __name__ == "__main__":
    if not (os.path.exists("public.pem") and os.path.exists("private.pem")):
        creating_keys()
