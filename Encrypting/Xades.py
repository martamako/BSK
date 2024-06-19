"""
This module provides functionality:
- Writing the information to XML file
- Getting signature from XML file
"""
import os.path
import pathlib
import datetime
from lxml import etree


def add_child(root: etree.Element, name: str, text: str):
    """
    Adding subelement to root with given name and text
    :param root: Root of XML tree
    :param name: Name of element
    :param text: Content of element
    :return:
    """
    element = etree.SubElement(root, name)
    element.text = text


def sign(file_name: str, signature: str, xml_file_name: str = "output.xml") -> bool:
    """
    Creating XML with information about signing file.
    :param file_name: Name of signed file
    :param signature: Signature created during signing file
    :param xml_file_name: Name of XML file to which content will be written to. By default, it's 'output.xml'
    :return:
    """
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
    tree.write(xml_file_name, pretty_print=True, xml_declaration=True, encoding="utf-8")
    return True


class MissingSignatureError(Exception):
    """
    Exception when Signature couldn't be found in XML file
    """
    pass


def get_signature_from_xml(file_path: str) -> str:
    """
    Reading XML file and returning signature
    :param file_path: Path to XML file with signature
    :return: Signature in string format
    """
    try:
        tree = etree.parse(file_path)
        root = tree.getroot()
        signature_element = root.find('Signature')
        if signature_element is None:
            raise MissingSignatureError("Element 'Signature' nie został znaleziony w dokumencie XML.")
        else:
            signature = signature_element.text
            return signature
    except MissingSignatureError as e:
        print(f"Wystąpił błąd: {e}")
    except etree.ElementTree.ParseError as e:
        print(f"Błąd parsowania XML: {e}")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")


