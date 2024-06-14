import os
import rsa


class Keys:
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