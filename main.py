import base64
import hashlib
import os

from Szyfrowanie.Szyfrowanie import Szyfrowanie
from cryptography.fernet import Fernet

from Szyfrowanie.Xades import Xades
from GUI import Application


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def encoding(pin: str):
    key = get_key_from_pin(pin)
    with open("mykey.key", "wb") as f:
        f.write(key)

def get_key_from_pin(pin: str):
    key = hashlib.sha256(pin.encode()).digest()
    key = base64.urlsafe_b64encode(key)
    return key

def getting_key():
    with open("mykey.key", "rb") as f:
        key = f.read()
        return key

def encrypting_file(key: Fernet):
    with open("private.pem", "rb") as private_pem:
        private_key = private_pem.read()
    encrypted = key.encrypt(private_key)

    with open("private.pem", "wb") as encrypted_file:
        encrypted_file.write(encrypted)

def decrypting_file(key: Fernet):
    with open("private.pem", "rb") as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = key.decrypt(encrypted)
    with open("private.pem", "wb") as decrypted_file:
        decrypted_file.write(decrypted)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    szyfrowanie = Szyfrowanie()
    print_hi('PyCharm')
    file_name = "main.cpp"
    # szyfrowanie.sing_file(file_name)
    #szyfrowanie.verify_file(file_name)
    #key = getting_key()
    # encrypting_file(Fernet(key))
    #decrypting_file(Fernet(key))
    encoding("1234")
    xades = Xades()
    # xades.sign(file_name)
    # xades.create_xades_signature(file_name=file_name)
    app = Application()




