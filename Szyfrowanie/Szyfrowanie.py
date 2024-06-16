import rsa
import base64
from Szyfrowanie import Keys
from Szyfrowanie.Xades import *


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
    Function of signing the file, creating signature and returning signature in string type
    Signing file - creating hash of file and encrypting it with private key
    :param file:
    :param private_key:
    :return: signature_base64: str
    """
    signature = rsa.sign(file, private_key, "SHA-256")  # getting bytes in  b'\xa5\xcf
    signature_base64 = get_str_from_signature(signature)
    return signature_base64


def get_str_from_signature(signature: bytes) -> str:
    """
    Function to convert Signature to string
    :param signature: Signature - encrypted by private key hash of file - in b'\xac\xce' format
    :return: Signature converted to string from utf-8 format
    """
    signature_base64 = base64.b64encode(signature)  # getting bytes of signature
    signature_base64 = signature_base64.decode('utf-8')  # getting string of signature
    return signature_base64


def get_signature_from_string(signature_base64: str) -> bytes:
    """
    Function to convert signature from string to bytes in format b'\\xaa\\xce'
    :param signature_base64: Signature in string format
    :return: Signature encoded to utf-8 in format b'\\xaa\\xce'
    """
    sig = signature_base64.encode('utf-8')  # getting bytes of signature from string
    signature_og = base64.b64decode(sig)  # getting bytes in b'\xa5\xcf
    return signature_og


def sing_file(file_path: str, key_path: str, pin: str):
    """
    Function to sign file with private key and create XML file with information
    :param file_path: Path to file to sign
    :param key_path: Path to
    :return:
    """
    file = open(file_path, "rb").read()
    aes_key = Keys.get_key_from_pin(pin)
    decrypted_key = Keys.decrypting_key(key_path, aes_key)
    private_key = rsa.PrivateKey.load_pkcs1(decrypted_key)
    signature_base64 = create_signature(file, private_key)  # signature of file

    sign(file_path, signature_base64)


def verify_file(file_path: str, xml_file: str, public_key_path: str) -> bool:
    """
    Function verifies if signature of signed file is correct by public key
    :param file_path: (str) Path of file user wants to verify
    :param xml_file: str Path to XML signature file containing encrypted by private key hash of file
    :param public_key_path: str Path to public key file with PEM ext
    :return: bool Returns if verification was successful
    """
    public_key = open(public_key_path, "rb").read()
    public_key = rsa.PublicKey.load_pkcs1(public_key)

    file = open(file_path, "rb").read()

    encrypted_signature = get_signature_from_xml(xml_file)
    signature = get_signature_from_string(encrypted_signature)
    verification = rsa.verify(file, signature, public_key)
    if verification == "SHA-256":
        print("Signature was verified")
        return True
    return False


def check_pin(pin: str) -> bool:
    """

    :param pin:
    :return:
    """
    return Keys.get_key_from_pin(pin) == Keys.get_key_from_pin("12345")