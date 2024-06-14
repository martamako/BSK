import base64
import datetime
import hashlib
import os.path
import pathlib
import datetime
from lxml import etree


def add_child(root: etree.Element, name: str, text: str):
    element = etree.SubElement(root, name)
    element.text = text
    # root.append(element)


class Xades:
    def __init__(self):
        print("Xades")

    def sign(self, file_name: str, signature, hash):
        data_to_sign = open(file_name, "rb").read()


        # General identification of the document (size, extension, date of modification)
        f_name = os.path.basename(file_name)
        file_size = os.path.getsize(file_name)
        file_ext = pathlib.Path(file_name).suffix
        file_time_modification = os.path.getmtime(file_name)
        file_date = datetime.datetime.fromtimestamp(file_time_modification)

        now = datetime.datetime.now()
        timestamp = now.timestamp()
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        formatted_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')

        print(file_size, file_ext, file_date)

        root = etree.Element("Signature")
        add_child(root, "DocumentName", f_name)
        add_child(root, "DocumentSize", str(file_size))
        add_child(root, "DocumentDate", str(file_date))
        add_child(root, "DocumentExtension", file_ext[1:])
        add_child(root, "SigningUser", "User A")
        add_child(root, "Signature", signature)
        add_child(root, "Hash", hash)
        add_child(root, "Timestamp", formatted_string)
        print(etree.tostring(root))

        tree = etree.ElementTree(root)
        tree.write('output.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")

    def read_xml(self):
        tree = etree.parse("../output.xml")
        root = tree.getroot()

        print(root.find('Signature').text)


        # printing the text contained within
        # first subtag of the 5th tag from
        # the parent
        # print(root[5][0].text)


if __name__ == "__main__":
    xades = Xades()
    # xades.sign("../main.cpp")
    xades.read_xml()
