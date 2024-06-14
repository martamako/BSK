import rsa
import hashlib
import base64

from Szyfrowanie import Keys
from Szyfrowanie.Xades import Xades


def document_hash(file_name: str):
    file_content = open(file_name, "rb").read()
    file_hash = hashlib.sha256(file_content).digest()
    file_hash = base64.urlsafe_b64encode(file_hash)
    return file_hash


def encrypt_file(file_name: str, public_key: rsa.PublicKey):
    file = open(file_name, "rb").read()
    encrypted = rsa.encrypt(file, public_key)
    with open(file_name, "rb") as f:
        f.write(encrypted)


def decrypt_file(file_name: str, private_key: rsa.PrivateKey):
    file = open(file_name, "rb").read()
    decrypted = rsa.decrypt(file, private_key)
    with open(file_name, "rb") as f:
        f.write(decrypted)


class Szyfrowanie:
    def __init__(self):
        self.__pin = '12345'
        self.__aes_key = Keys.get_key_from_pin(self.__pin)

        with open("public.pem", "rb") as f:
            self.__public_key = rsa.PublicKey.load_pkcs1(f.read())

        self.__xades = Xades()

    def check_pin(self, pin: str):
        return Keys.get_key_from_pin(pin) == Keys.get_key_from_pin(self.__pin)

    def sing_file(self, file_name: str, key_name):
        private_key = Keys.decrypting_key(key_name, self.__aes_key)
        private_key = rsa.PrivateKey.load_pkcs1(private_key)
        hash_of_file = document_hash(file_name)

        signature = rsa.sign(hash_of_file, private_key, "SHA-256")
        signature_base64 = base64.b64encode(signature).decode('utf-8')

        self.__xades.sign(file_name, signature_base64, hash_of_file)
        # there was saving signature to file

    def verify_file(self, file_name: str):
        file_content = open(file_name, "rb").read()
        # there was reading signature from file
        signature = document_hash(file_name)
        verification = rsa.verify(file_content, signature, self.__public_key)
        print(verification)


