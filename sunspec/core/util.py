
"""
  Copyright (c) 2014, SunSpec Alliance
  All Rights Reserved

"""

import os
import struct
import zipfile
import array

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
    addr = struct.unpack('16s', data)
    return addr[0]

def data_to_eui48(data):
    return '%02X:%02X:%02X:%02X:%02X:%02X' % (ord(data[2]), ord(data[3]), ord(data[4]), ord(data[5]), ord(data[6]), ord(data[7]))

try:
    float('nan')

    def data_to_float(data):
        f = struct.unpack('>f', data)
        return f[0]

    def data_to_double(data):
        d = struct.unpack('>d', data)
        return d[0]

except Exception:
    # earlier python version - nan not supported
    def data_to_float(data):
        e = struct.unpack('>L', data)
        # if all exponent bits are '1' it is nan or inf, set to None
        if (e[0] & 0x7f800000) == 0x7f800000:
            return None
        else:
            f = struct.unpack('>f', data)
        return f[0]

    def data_to_double(data):
        e = struct.unpack('>Q', data)
        # if all exponent bits are '1' it is nan or inf, set to None
        if (e[0] & 0x7ff0000000000000) == 0x7ff0000000000000:
            return None
        else:
            d = struct.unpack('>d', data)
        return d[0]

def data_to_str(data):
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

def ipv6addr_to_data(addr, len=None):
    return struct.pack('16s', addr)

def float_to_data32(f, len=None):
    # convert python float (float64) to float32 before packing
    fa = array('f', f)
    return struct.pack('>f', fa[0])

def float32_to_data(f, len=None):
    return struct.pack('>f', f)

def float_to_data(f, len=None):
    # python float is really a double
    return struct.pack('>d', f)

def str_to_data(s, slen=None):
    if slen is None:
        slen = len(s)
    return struct.pack(str(slen) + 's', s)

def eui48_to_data(eui48):
    return ('0000' + eui48.replace(':', '')).decode('hex')

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
                except Exception, e:
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




