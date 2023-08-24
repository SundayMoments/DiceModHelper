"""
The MIT License (MIT)

Copyright (c) 2015 Norbyte

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
CODE ADAPTED FROM LSLib: https://github.com/Norbyte/lslib/ -> https://github.com/Norbyte/lslib/blob/7e05210497c2cf640efdd725797fdae183cfc8b5/LSLib/LS/Localization.cs
"""

import struct

class LocaHeader:
    DEFAULT_SIGNATURE = 0x41434f4c  # 'LOCA'

    def __init__(self, signature=DEFAULT_SIGNATURE, num_entries=0, texts_offset=0):
        self.signature = signature
        self.num_entries = num_entries
        self.texts_offset = texts_offset

    def pack(self):
        return struct.pack("<III", self.signature, self.num_entries, self.texts_offset)

    @classmethod
    def unpack(cls, data):
        signature, num_entries, texts_offset = struct.unpack("<III", data)
        return cls(signature, num_entries, texts_offset)

class LocaEntry:
    def __init__(self, key=None, version=0, length=0):
        self.key = key or b'\0' * 64
        self.version = version
        self.length = length

    @property
    def key_string(self):
        return self.key.decode('utf-8').rstrip('\0')

    @key_string.setter
    def key_string(self, value):
        encoded = value.encode('utf-8')
        self.key = encoded + (b'\0' * (64 - len(encoded)))

    def pack(self):
        return struct.pack("<64sHI", self.key, self.version, self.length)

    @classmethod
    def unpack(cls, data):
        key, version, length = struct.unpack("<64sHI", data)
        return cls(key, version, length)

class LocalizedText:
    def __init__(self, key, version, text):
        self.key = key
        self.version = version
        self.text = text

class LocaResource:
    def __init__(self):
        self.entries = []

class LocaReader:
    def __init__(self, stream):
        self.stream = stream

    def read(self):
        header_data = self.stream.read(struct.calcsize("<III"))
        header = LocaHeader.unpack(header_data)

        if header.signature != LocaHeader.DEFAULT_SIGNATURE:
            raise ValueError("Incorrect signature in localization file")

        entries = [LocaEntry.unpack(self.stream.read(struct.calcsize("<64sHI"))) for _ in range(header.num_entries)]

        self.stream.seek(header.texts_offset)
        loca_resource = LocaResource()
        for entry in entries:
            text = self.stream.read(entry.length - 1).decode('utf-8')
            self.stream.read(1)  # Read the null byte
            localized_text = LocalizedText(entry.key_string, entry.version, text)
            loca_resource.entries.append(localized_text)

        return loca_resource

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.close()

class LocaWriter:
    def __init__(self, stream):
        self.stream = stream

    def write(self, res):
        header = LocaHeader(
            num_entries=len(res.entries),
            texts_offset=struct.calcsize("<III") + struct.calcsize("<64sHI") * len(res.entries)
        )
        self.stream.write(header.pack())

        entries = []
        for entry in res.entries:
            loca_entry = LocaEntry()
            loca_entry.key_string = entry.key
            loca_entry.version = entry.version
            loca_entry.length = len(entry.text.encode('utf-8')) + 1
            entries.append(loca_entry)
            self.stream.write(loca_entry.pack())

        for entry in res.entries:
            self.stream.write(entry.text.encode('utf-8'))
            self.stream.write(b'\0')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.close()

import xml.etree.ElementTree as ET

class LocaXmlReader:
    def __init__(self, stream):
        self.stream = stream

    def read(self):
        resource = LocaResource()
        tree = ET.parse(self.stream)
        root = tree.getroot()

        for content in root.findall('content'):
            key = content.get('contentuid')
            version = int(content.get('version', 1))
            text = content.text
            resource.entries.append(LocalizedText(key, version, text))

        return resource

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.close()

class LocaXmlWriter:
    def __init__(self, stream):
        self.stream = stream

    def write(self, res):
        root = ET.Element("contentList")

        for entry in res.entries:
            content = ET.SubElement(root, "content", contentuid=entry.key, version=str(entry.version))
            content.text = entry.text

        tree = ET.ElementTree(root)
        tree.write(self.stream, encoding='utf-8', xml_declaration=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.close()

import os

class LocaFormat:
    LOCA = 1
    XML = 2

def extension_to_file_format(path):
    extension = os.path.splitext(path)[1].lower()
    if extension == ".loca":
        return LocaFormat.LOCA
    elif extension == ".xml":
        return LocaFormat.XML
    else:
        raise ValueError("Unrecognized file extension: " + extension)

def load(input_path, format=None):
    if format is None:
        format = extension_to_file_format(input_path)

    with open(input_path, 'rb') as stream:
        if format == LocaFormat.LOCA:
            reader = LocaReader(stream)
            return reader.read()
        elif format == LocaFormat.XML:
            reader = LocaXmlReader(stream)
            return reader.read()
        else:
            raise ValueError("Invalid loca format")

def save(resource, output_path, format=None):
    if format is None:
        format = extension_to_file_format(output_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'wb') as stream:
        if format == LocaFormat.LOCA:
            writer = LocaWriter(stream)
            writer.write(resource)
        elif format == LocaFormat.XML:
            writer = LocaXmlWriter(stream)
            writer.write(resource)
        else:
            raise ValueError("Invalid loca format")