import rsa
from Szyfrowanie.Szyfrowanie import Szyfrowanie


class SzyfrowaniePubliczne(Szyfrowanie):
    def __init__(self):
        super().__init__()

    def encode(self, message: str):
        super().encode(message, self.__public_key)

    def decode(self):
        super().decode(self.__private_key)
