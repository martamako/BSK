from lxml import etree
from signxml import XMLSigner, XMLVerifier

class Xades:
    def __init__(self, file_name: str):
        data_to_sign = open(file_name, "rb").read()
        print(data_to_sign)
