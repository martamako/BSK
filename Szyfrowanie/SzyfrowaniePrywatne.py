import os
import rsa

from Szyfrowanie.Szyfrowanie import Szyfrowanie


class SzyfrowaniePrywatne(Szyfrowanie):
    def __init__(self):
        if not (os.path.exists("public.pem") and os.path.exists("private.pem")):
            self.creating_keys()

        with open("public.pem", "rb") as f:
            self.__public_key = rsa.PublicKey.load_pkcs1(f.read())

        with open("private.pem", "rb") as f:
            self.__private_key = rsa.PrivateKey.load_pkcs1(f.read())

    def sign(self, message: str):
        signature = rsa.sign(message.encode(), self.__private_key, "SHA-256")

        with open("signature", "wb") as f:
            f.write(signature)

    def verify(self, message: str):
        signature = open("signature", "rb").read()
        verification = rsa.verify(message.encode(), signature, self.__public_key)
        print(verification)
        