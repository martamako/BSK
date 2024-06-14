import os.path
import rsa
import hashlib
import base64
from cryptography.fernet import Fernet

from Szyfrowanie.Xades import Xades


class Szyfrowanie:
    def __init__(self):
        self.__pin = '12345'
        self.aes_key = self.get_key_from_pin(self.__pin)

        with open("public.pem", "rb") as f:
            self.__public_key = rsa.PublicKey.load_pkcs1(f.read())

        self.xades = Xades()

    def get_key_from_pin(self, pin: str):
        key = hashlib.sha256(pin.encode()).digest()
        key = base64.urlsafe_b64encode(key)
        with open("mykey.key", "wb") as f:
            f.write(key)
        return key

    def check_pin(self, pin: str):
        return self.get_key_from_pin(pin) == self.get_key_from_pin(self.__pin)


    def sign(self, message: str):
        signature = rsa.sign(message.encode(), self.__private_key, "SHA-256")

        with open("signature", "wb") as f:
            f.write(signature)

    def sing_file(self, file_name: str, key_name):

        private_key = self.decrypting_key(key_name)
        hash_of_file = self.document_hash(file_name)

        private_key = rsa.PrivateKey.load_pkcs1(private_key)
        signature = rsa.sign(hash_of_file, private_key, "SHA-256")
        signature_base64 = base64.b64encode(signature).decode('utf-8')

        self.xades.sign(file_name, signature_base64, hash_of_file)

        with open("file_signature", "wb") as file_signature:
            file_signature.write(signature)

    def document_hash(self, file_name: str):
        file_content = open(file_name, "rb").read()

        file_hash = hashlib.sha256(file_content).digest()
        file_hash = base64.urlsafe_b64encode(file_hash)
        return file_hash
    def verify_file(self, file_name: str):
        file_content = open(file_name, "rb").read()
        signature = open("file_signature", "rb").read()
        verification = rsa.verify(file_content, signature, self.__public_key)
        print(verification)

    def encrypt_file(self, file_name: str):
        file = open(file_name, "rb").read()
        encrypted = rsa.encrypt(file, self.__public_key)
        with open(file_name, "rb") as f:
            f.write(encrypted)


    def decrypt_file(self, file_name: str):
        file = open(file_name, "rb").read()
        decrypted = rsa.decrypt(file, self.__public_key)
        with open(file_name, "rb") as f:
            f.write(decrypted)


    def encrypting_key(self):
        with open("private.pem", "rb") as private_pem:
            private_key = private_pem.read()
        key = Fernet(self.aes_key)
        encrypted = key.encrypt(private_key)

        with open("private.pem", "wb") as encrypted_file:
            encrypted_file.write(encrypted)

    def decrypting_key(self, key_name: str):
        with open("private.pem", "rb") as encrypted_file:
            encrypted = encrypted_file.read()
        key = Fernet(self.aes_key)
        decrypted = key.decrypt(encrypted)
        # with open("private.pem", "wb") as decrypted_file:
        #    decrypted_file.write(decrypted)
        return decrypted