import datetime
import os.path
import pathlib

import xmlsec
from lxml import etree
from signxml import XMLSigner, XMLVerifier
from signxml import xades

class Xades:
    def __init__(self):
        print("Xades")

    def create_xades_signature(self, file_name: str, key_file: str = "private.pem", cert_file: str = "cert.pem"):
        # Załaduj klucz prywatny i certyfikat
        key = xmlsec.Key.from_file(key_file, xmlsec.constants.KeyDataFormatPem)
        key.load_cert_from_file(cert_file, xmlsec.constants.KeyDataFormatPem)

        
        # Utwórz obiekt podpisu XML
        sign_node = xmlsec.template.create(

        )


        print(key)

    def sign(self, file_name: str):
        data_to_sign = open(file_name, "rb").read()
        cert = open("cert.pem").read()
        key = open("private.pem").read()


        # General identification of the document (size, extension, date of modification)
        file_size = os.path.getsize(file_name)
        file_ext = pathlib.Path(file_name).suffix
        file_time_modification = os.path.getmtime(file_name)
        file_date = datetime.datetime.fromtimestamp(file_time_modification)
        print(file_size, file_ext, file_date)

        xades_signer = xades.XAdESSigner()
        # xades_signer.add_data_object_format()
