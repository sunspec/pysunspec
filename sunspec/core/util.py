
"""
    Copyright (C) 2018 SunSpec Alliance

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.
"""

import os
import struct
import sys
import zipfile
import array
import base64

class SunSpecError(Exception):
    pass

""" Functions to pack and unpack data string values

"""
def data_to_s16(data):
    s16 = struct.unpack('>h', data)
    return s16[0]

def data_to_u16(data):
    u16 = struct.unpack('>H', data)
    return u16[0]

def data_to_s32(data):
    s32 = struct.unpack('>l', data)
    return s32[0]

def data_to_u32(data):
    u32 = struct.unpack('>L', data)
    return u32[0]

def data_to_s64(data):
    s64 = struct.unpack('>q', data)
    return s64[0]

def data_to_u64(data):
    u64 = struct.unpack('>Q', data)
    return u64[0]

def data_to_ipv6addr(data):
    if sys.version_info < (3,):
        data = [ord(x) for x in data]

    value = False
    for i in data:
        if i != 0:
            value = True
            break
    if value and len(data) == 16:
        return '%02X%02X%02X%02X:%02X%02X%02X%02X:%02X%02X%02X%02X:%02X%02X%02X%02X' % (
            data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
            data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15])

def data_to_eui48(data):
    if sys.version_info < (3,):
        data = [ord(x) for x in data]

    value = False
    for i in data:
        if i != 0:
            value = True
            break
    if value and len(data) == 8:
        return '%02X:%02X:%02X:%02X:%02X:%02X' % (
            data[2], data[3], data[4], data[5], data[6], data[7])

def data_to_float(data):
    f = struct.unpack('>f', data)
    if str(f[0]) != str(float('nan')):
        return f[0]

def data_to_double(data):
    d = struct.unpack('>d', data)
    if str(d[0]) != str(float('nan')):
        return d[0]

def data_to_str(data):

    # Change the data from bytes string to regular string for python 3
    # compatibility
    if sys.version_info > (3,):
        data = str(data, 'latin-1')

    if len(data) > 1:
        data = data[0] + data[1:].rstrip('\0')
    return data

def s16_to_data(s16, len=None):
    return struct.pack('>h', s16)

def u16_to_data(u16, len=None):
    return struct.pack('>H', u16)

def s32_to_data(s32, len=None):
    return struct.pack('>l', s32)

def u32_to_data(u32, len=None):
    return struct.pack('>L', u32)

def s64_to_data(s64, len=None):
    return struct.pack('>q', s64)

def u64_to_data(u64, len=None):
    return struct.pack('>Q', u64)

def ipv6addr_to_data(addr, slen=None):
    s = base64.b16decode(addr.replace(':', ''))
    if slen is None:
        slen = len(s)
    return struct.pack(str(slen) + 's', s)

def float_to_data32(f, len=None):
    return struct.pack('>f', f)

def float32_to_data(f, len=None):
    return struct.pack('>f', f)

def float_to_data(f, len=None):
    # python float is really a double
    return struct.pack('>d', f)

def str_to_data(s, slen=None):
    if slen is None:
        slen = len(s)
    if sys.version_info > (3,):
        s = bytes(s, 'latin-1')
    if slen < 16:
        s += b'\x00'
        slen += 1
    return struct.pack(str(slen) + 's', s)

def eui48_to_data(eui48):
    return (b'\x00\x00' + base64.b16decode(eui48.replace(':', '')))


""" Simple XML pretty print support function

"""
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

""" File path list

"""
class PathList(object):

    def __init__(self, path_list=None):
        self.path = []

        if path_list is not None:
            self.path = path_list

    """ Add path to path list

    Provides a list of file system paths to search for non-python files similar to sys.path for python 
    modules. Zipfiles can be included in a path name and the contents of the zipfile will be searched
    based on the remaining path content. Zip file support has the following restrictions: only one zip file
    in a path, zi pfiles must have a .zip extension in the name, directories can not end in .zip.
    Paths are searched in the order they were added to the path list.

    """
    def add(self, path):

        self.path.append(path)

    """ Read first instance of specified file found in path list

    Traverses the path list and returns the contents of the first instance of the specified file.
    Supports zip files in path.

    """
    def read(self, filename):

        file_path = ''
        zip_file_path = ''

        # traverse path list until first instance of file found
        for p in self.path:
            file_path = ''
            element_list = p.split(os.sep)
            sep = os.sep

            for e in element_list:
                if e == '':
                    file_path += sep
                elif file_path and file_path != sep:
                    file_path += sep
                file_path += e
                if e.endswith('.zip'):
                    zip_file_path = file_path
                    if os.path.exists(zip_file_path):
                        file_path = ''
                        # zip file separator is always '/'
                        sep = '/'
                    else:
                        # continue with next path list element if zip file does not exist
                        zip_file_path = ''
                        break

            if file_path and file_path != os.sep:
                file_path += sep
            file_path  += filename
            if zip_file_path:
                zip_file = zipfile.ZipFile(zip_file_path)
                try:
                    zip_file.getinfo(file_path)
                except Exception as e:
                    continue
                return zip_file.read(file_path)
            else:
                if os.path.exists(file_path):
                    f = open(file_path, 'rb')
                    return f.read()
                else:
                    continue

        # file not found
        raise NameError(filename)

    def __str__(self):

        paths = []

        for p in self.path:
            paths.append(p)

        return str(paths)




