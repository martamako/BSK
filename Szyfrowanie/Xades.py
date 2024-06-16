import os.path
import pathlib
import datetime
from lxml import etree


def add_child(root: etree.Element, name: str, text: str):
    element = etree.SubElement(root, name)
    element.text = text
    # root.append(element)


def sign(file_name: str, signature: str):
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
    add_child(root, "Timestamp", formatted_string)
    print(etree.tostring(root))

    tree = etree.ElementTree(root)
    tree.write('output.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")


def get_signature_from_xml(file_path: str) -> str:
    try:
        tree = etree.parse(file_path)
        root = tree.getroot()
        signature = root.find('Signature').text
        print(signature)
        return signature
    except:
        print("Couldn't get signature")
