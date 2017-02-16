import xml.etree.ElementTree as ET
import io
import os.path

"""
Script to parse the eON registry format.
"""

regfile = os.path.expanduser("~/.local/share/vpltd/SaintsRow3/EonRegistry.xml")

def hex_to_bin(s):
    """Converts a string of hex digits to bytes"""
    stream = io.StringIO(s)
    data = b""
    while True:
        char_hex = stream.read(2)
        if not char_hex:
            break
        char_int = int(char_hex, 16)
        data += char_int.to_bytes(1, byteorder="big")
    return data

def print_children(e, level=0):
    for attr, value in e.attrib.items():
        attrname = hex_to_bin(attr[1:]).decode("utf-16")
        attrtype = value[0:2]
        if attrtype == "01": # String?
            attrval = hex_to_bin(value[2:]).decode("utf-16")
        elif attrtype == "04": # dword?
            intval = int.from_bytes(hex_to_bin(value[2:]), byteorder="little")
            attrval = hex(intval)
        else:
            attrval = value[2:]

        if not attrname:
            continue
        print("  " * level + attrname + " = " + attrval)
    for child in e:
        tagname = hex_to_bin(child.tag[1:]).decode("utf-16")
        print("  " * level + tagname)
        print_children(child, level + 1)



tree = ET.parse(regfile)
root = tree.getroot()

assert root.tag == "eON"

print_children(root)
