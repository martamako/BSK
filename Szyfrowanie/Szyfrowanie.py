import rsa
import hashlib
import base64

from Szyfrowanie import Keys
from Szyfrowanie.Xades import Xades


def document_hash(file_name: str) -> bytes:
    file_content = open(file_name, "rb").read(65536)
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


def create_signature(file: bytes, private_key: rsa.PrivateKey) -> str:
    """
    Function of signing the hash of file, creating signature and returning signature in string type
    :param file: bytes
    :param private_key: rsa.PrivateKey
    :return: signature_base64: str
    """
    signature = rsa.sign(file, private_key, "SHA-256") # getting bytes in  b'\xa5\xcf
    signature_base64 = get_str_from_signature(signature)
    return signature_base64


def get_str_from_signature(signature: bytes):
    signature_base64 = base64.b64encode(signature)  # getting bytes of signature
    signature_base64 = signature_base64.decode('utf-8')  # getting string of signature
    return signature_base64


def get_signature_from_string(signature_base64: str) -> bytes:
    sig = signature_base64.encode('utf-8')  # getting bytes of signature from string
    signature_og = base64.b64decode(sig)  # getting bytes in b'\xa5\xcf
    return signature_og


class Szyfrowanie:
    def __init__(self):
        self.__pin = '12345'
        self.__aes_key = Keys.get_key_from_pin(self.__pin)

        with open("public.pem", "rb") as f:
            self.__public_key = rsa.PublicKey.load_pkcs1(f.read())

        self.__xades = Xades()

    def check_pin(self, pin: str):
        return Keys.get_key_from_pin(pin) == Keys.get_key_from_pin(self.__pin)

    def sing_file(self, file_name: str, key_path: str):
        file = open(file_name, "rb").read()

        private_key = Keys.decrypting_key(key_path, self.__aes_key)
        private_key = rsa.PrivateKey.load_pkcs1(private_key)
        hash_of_file = document_hash(file_name)  # hash of file

        signature_base64 = create_signature(file, private_key)  # signature of file
        encrypted_hash = self.encrypt_hash(hash_of_file, private_key)
        self.__xades.sign(file_name, signature_base64, encrypted_hash)
        # there was saving signature to file

    def encrypt_hash(self, hash_of_file: bytes, private_key) -> str:
        encrypted_hash = rsa.encrypt(hash_of_file, private_key)  # encrypted hash of file
        encrypted_hash = get_str_from_signature(encrypted_hash)  # str version of encrypted hash of file
        return encrypted_hash

    def decrypt_hash(self, encrypted_hash: str, public_key) -> bytes:
        pass

    def verify_file(self, file_name: str, xml_file: str, private_key: rsa.PrivateKey):
        file_content = open(file_name, "rb").read()
        # there was reading signature from file
        signature = document_hash(file_name)
        verification = rsa.verify(file_content, signature, private_key)
        print(verification)
