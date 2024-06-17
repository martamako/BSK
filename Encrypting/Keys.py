"""
This module provides functionality to:
- generate RSA keys and write them to file,
- generate AES key from PIN,
- encrypt and decrypt RSA keys with AES key.
"""

import base64
import hashlib
import os
import rsa
from cryptography.fernet import Fernet


def creating_keys(key_length: int = 4096):
    """
    Creating RSA keys with provided length with rsa module. It saves keys to files.
    :param key_length: Length of RSA key. By default, length is 4096 bytes
    :return:
    """
    public_key, private_key = rsa.newkeys(key_length)
    write_key_to_file(private_key, "private.pem")
    write_key_to_file(public_key, "public.pem")


def get_key_from_pin(pin: str) -> bytes:
    """
    Function to get AES key from provided PIN
    :param pin: PIN to create AES key
    :return: Key created with hashlib.sha256 converted to b64encode in bytes
    """
    key = hashlib.sha256(pin.encode()).digest()
    key = base64.urlsafe_b64encode(key)
    return key


def write_key_to_file(key, file_name: str):
    """
    Function to save key to file
    :param key: Private or public key
    :param file_name: File to which key will be written to
    :return:
    """
    with open(file_name, "wb") as f:
        f.write(key.save_pkcs1("PEM"))


def encrypting_key(_aes_key: bytes, key_path: str = "private.pem"):
    """
    Function reads private key from file and encrypt it with AES key
    :param _aes_key: Key to encrypting with AES
    :param key_path:
    :return:
    """
    with open(key_path, "rb") as private_pem:
        private_key = private_pem.read()
    key = Fernet(_aes_key)
    encrypted = key.encrypt(private_key)

    with open(key_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted)


def decrypting_key(key_path: str, _aes_key: bytes, save_to_file: bool = False) -> bytes:
    """
    Function of decrypting encrypted private key in file and returning decrypted key in bytes
    :param key_path: Path to file with private key with PEM extension
    :param _aes_key: AES key
    :param save_to_file: If decrypted key should be saved to file. By default it's False
    :return: Decrypted private key in byts
    """
    with open(key_path, "rb") as encrypted_file:
        encrypted = encrypted_file.read()
    key = Fernet(_aes_key)
    private_key = key.decrypt(encrypted)

    if save_to_file:
        with open(key_path, "wb") as decrypted_file:
            decrypted_file.write(private_key)

    return private_key


if __name__ == "__main__":
    if not (os.path.exists("public.pem") and os.path.exists("private.pem")):
        creating_keys()
    aes_key = get_key_from_pin("12345")
    encrypting_key(aes_key)
