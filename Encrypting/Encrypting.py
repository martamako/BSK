"""
This module provides functionality:
- Encrypt/decrypt file
- Signing the file and writing information to XML file
- Verifying file with signature read from XML file
- Checking if provided PIN is correct to decrypt private key
- Converting signature to string or bytes
"""
import rsa
import base64
from Encrypting import Keys
from Encrypting.Xades import *


def encrypt_file(file_path: str, public_key_path: str) -> bool:
    """
    Function to encrypt file using public key. Encrypted file is saved in the same location.
    :param file_path: Path to file to encrypt.
    :param public_key_path: Path to public key.
    :return:
    """
    file = open(file_path, "rb").read()
    key_file = open(public_key_path, "rb").read()
    public_key = rsa.PublicKey.load_pkcs1(key_file)
    encrypted = rsa.encrypt(file, public_key)
    with open(file_path, "wb") as f:
        f.write(encrypted)
        print(f"Successful encryption of {file_path}")
        return True


def decrypt_file(file_path: str, private_key_path: str, pin: str = "12345") -> bool:
    """
    Function to decrypt encrypted file using private key. Private key is decrypted by using PIN.
    :param file_path: Path to file to decrypt.
    :param private_key_path: Path to private key.
    :param pin: PIN to decrypt private key. Set to default PIN '12345'
    :return:
    """
    file = open(file_path, "rb").read()
    aes_key = Keys.get_key_from_pin(pin)

    decrypted_key = Keys.decrypting_key(private_key_path, aes_key)
    private_key = rsa.PrivateKey.load_pkcs1(decrypted_key)

    decrypted = rsa.decrypt(file, private_key)
    with open(file_path, "wb") as f:
        f.write(decrypted)
        print(f"Successful decryption of {file_path}")
        return True


def get_str_from_signature(signature: bytes) -> str:
    """
    Function to convert Signature to string
    :param signature: Signature - encrypted by private key hash of file - in b'\xac\xce' format
    :return: Signature converted to string from utf-8 format
    """
    signature_base64 = base64.b64encode(signature)  # getting bytes of signature
    signature_base64 = signature_base64.decode('utf-8')  # getting string of signature
    return signature_base64


def get_signature_from_str(signature_base64: str) -> bytes:
    """
    Function to convert signature from string to bytes in format b'\\xaa\\xce'
    :param signature_base64: Signature in string format
    :return: Signature encoded to utf-8 in format b'\\xaa\\xce'
    """
    sig = signature_base64.encode('utf-8')  # getting bytes of signature from string
    signature_og = base64.b64decode(sig)  # getting bytes in b'\xa5\xcf
    return signature_og


def create_signature(file: bytes, private_key: rsa.PrivateKey) -> str:
    """
    Function of signing the file, creating signature and returning signature in string type
    :param file: Read file in "rb" mode.
    :param private_key: Private key used to sign file with.
    :return: SIgnature in string format.
    """
    signature = rsa.sign(file, private_key, "SHA-256")  # getting bytes in  b'\xa5\xcf
    signature_base64 = get_str_from_signature(signature)
    return signature_base64


def sing_file(file_path: str, key_path: str, pin: str) -> bool:
    """
    Function to sign file with private key and create XML file with information
    :param file_path: Path to file to sign
    :param key_path: Path to private key file
    :param pin: PIN to get AES key to decrypt private key
    :return:
    """
    file = open(file_path, "rb").read()
    aes_key = Keys.get_key_from_pin(pin)
    decrypted_key = Keys.decrypting_key(key_path, aes_key)
    private_key = rsa.PrivateKey.load_pkcs1(decrypted_key)
    signature_base64 = create_signature(file, private_key)  # signature of file

    result = sign(file_path, signature_base64)
    if result:
        return True
    return False


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
    signature = get_signature_from_str(encrypted_signature)
    verification = rsa.verify(file, signature, public_key)
    if verification == "SHA-256":
        print("Signature was verified")
        return True
    return False


def check_pin(pin: str) -> bool:
    """
    Function checks if key from input PIN is the same as PIN used to create AES key to encrypt private key
    :param pin: PIN to get key from
    :return: True if keys are the same, False if not
    """
    return Keys.get_key_from_pin(pin) == Keys.get_key_from_pin("12345")
