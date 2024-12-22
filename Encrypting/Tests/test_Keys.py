from unittest import TestCase
from Encrypting import Keys
import rsa


class Test(TestCase):
    def test_creating_keys(self):
        Keys.creating_keys(4096)
        with open("private.pem", "rb") as f:
            private_key = f.read()
        with open("public.pem", "rb") as f:
            public_key = f.read()
        priv_key = rsa.PrivateKey.load_pkcs1(private_key)
        pub_key = rsa.PublicKey.load_pkcs1(public_key)
        self.assertTrue(True)

    def test_get_key_from_pin(self):
        self.fail()
