import os.path

import rsa
from Crypto.Random import get_random_bytes

class Szyfrowanie:
    def __init__(self):
        if not (os.path.exists("public.pem") and os.path.exists("private.pem")):
            self.creating_keys()

        with open("public.pem", "rb") as f:
            self.__public_key = rsa.PublicKey.load_pkcs1(f.read())

        with open("private.pem", "rb") as f:
            self.__private_key = rsa.PrivateKey.load_pkcs1(f.read())

    def creating_keys(self, key_length: int = 4096):
        public_key, private_key = rsa.newkeys(key_length)
        self.write_key_to_file(public_key, "public.pem")
        self.write_key_to_file(private_key, "private.pem")

    def write_key_to_file(self, key, file_name: str):
        with open(file_name, "wb") as f:
            f.write(key.save_pkcs1("PEM"))

    def encode(self, message: str, key):
        encrypted_message = rsa.encrypt(message.encode(), key)

        with open("encrypted.message", "wb") as f:
            f.write(encrypted_message)

    def decode(self, key):
        encrypted_message = open("encrypted.message", "rb").read()
        clear_message = rsa.decrypt(encrypted_message, key)
        print(clear_message.decode())

    def sign(self, message: str):
        signature = rsa.sign(message.encode(), self.__private_key, "SHA-256")

        with open("signature", "wb") as f:
            f.write(signature)

    def verify(self, message: str):
        signature = open("signature", "rb").read()
        verification = rsa.verify(message.encode(), signature, self.__public_key)
        print(verification)