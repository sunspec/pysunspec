
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

import sunspec.core.suns as suns

SMDX_ROOT = 'sunSpecModels'
SMDX_MODEL = 'model'
SMDX_BLOCK = 'block'
SMDX_POINT = 'point'
SMDX_ATTR_ID = 'id'
SMDX_ATTR_LEN = 'len'
SMDX_ATTR_NAME = 'name'
SMDX_ATTR_TYPE = 'type'
SMDX_ATTR_TYPE_FIXED = 'fixed'
SMDX_ATTR_TYPE_REPEATING = 'repeating'
SMDX_ATTR_OFFSET = 'offset'
SMDX_ATTR_MANDATORY = 'mandatory'
SMDX_ATTR_ACCESS = 'access'
SMDX_ATTR_SF = 'sf'
SMDX_ATTR_UNITS = 'units'

SMDX_SYMBOL = 'symbol'

SMDX_STRINGS = 'strings'
SMDX_LABEL = 'label'
SMDX_DESCRIPTION = 'description'
SMDX_NOTES = 'notes'

SMDX_TYPE_INT16 = 'int16'
SMDX_TYPE_UINT16 = 'uint16'
SMDX_TYPE_COUNT = 'count'
SMDX_TYPE_ACC16 = 'acc16'
SMDX_TYPE_ENUM16 = 'enum16'
SMDX_TYPE_BITFIELD16 = 'bitfield16'
SMDX_TYPE_PAD = 'pad'
SMDX_TYPE_INT32 = 'int32'
SMDX_TYPE_UINT32 = 'uint32'
SMDX_TYPE_ACC32 = 'acc32'
SMDX_TYPE_ENUM32 = 'enum32'
SMDX_TYPE_BITFIELD32 = 'bitfield32'
SMDX_TYPE_IPADDR = 'ipaddr'
SMDX_TYPE_INT64 = 'int64'
SMDX_TYPE_UINT64 = 'uint64'
SMDX_TYPE_ACC64 = 'acc64'
SMDX_TYPE_IPV6ADDR = 'ipv6addr'
SMDX_TYPE_FLOAT32 = 'float32'
SMDX_TYPE_STRING = 'string'
SMDX_TYPE_SUNSSF = 'sunssf'
SMDX_TYPE_EUI48 = 'eui48'

SMDX_ACCESS_R = 'r'
SMDX_ACCESS_RW = 'rw'

SMDX_MANDATORY_FALSE = 'false'
SMDX_MANDATORY_TRUE = 'true'

smdx_access_types = {
    SMDX_ACCESS_R: suns.SUNS_ACCESS_R,
    SMDX_ACCESS_RW: suns.SUNS_ACCESS_RW
}

smdx_mandatory_types = {
    SMDX_MANDATORY_FALSE: suns.SUNS_MANDATORY_FALSE,
    SMDX_MANDATORY_TRUE: suns.SUNS_MANDATORY_TRUE
}

# map SMDX block types to SunSpec block types
smdx_block_types = {
    SMDX_ATTR_TYPE_FIXED: suns.SUNS_BLOCK_FIXED,
    SMDX_ATTR_TYPE_REPEATING: suns.SUNS_BLOCK_REPEATING
}

# map SMDX point types to SunSpec point types
smdx_point_types = {
    SMDX_TYPE_INT16: suns.SUNS_TYPE_INT16,
    SMDX_TYPE_UINT16: suns.SUNS_TYPE_UINT16,
    SMDX_TYPE_COUNT: suns.SUNS_TYPE_COUNT,
    SMDX_TYPE_ACC16: suns.SUNS_TYPE_ACC16,
    SMDX_TYPE_ENUM16: suns.SUNS_TYPE_ENUM16,
    SMDX_TYPE_BITFIELD16: suns.SUNS_TYPE_BITFIELD16,
    SMDX_TYPE_PAD: suns.SUNS_TYPE_PAD,
    SMDX_TYPE_INT32: suns.SUNS_TYPE_INT32,
    SMDX_TYPE_UINT32: suns.SUNS_TYPE_UINT32,
    SMDX_TYPE_ACC32: suns.SUNS_TYPE_ACC32,
    SMDX_TYPE_ENUM32: suns.SUNS_TYPE_ENUM32,
    SMDX_TYPE_BITFIELD32: suns.SUNS_TYPE_BITFIELD32,
    SMDX_TYPE_IPADDR: suns.SUNS_TYPE_IPADDR,
    SMDX_TYPE_INT64: suns.SUNS_TYPE_INT64,
    SMDX_TYPE_UINT64: suns.SUNS_TYPE_UINT64,
    SMDX_TYPE_ACC64: suns.SUNS_TYPE_ACC64,
    SMDX_TYPE_IPV6ADDR: suns.SUNS_TYPE_IPV6ADDR,
    SMDX_TYPE_FLOAT32: suns.SUNS_TYPE_FLOAT32,
    SMDX_TYPE_STRING: suns.SUNS_TYPE_STRING,
    SMDX_TYPE_SUNSSF: suns.SUNS_TYPE_SUNSSF,
    SMDX_TYPE_EUI48: suns.SUNS_TYPE_EUI48
}

def model_id_to_filename(model_id):

    return 'smdx_%05d.xml' % (int(model_id))

def model_filename_to_id(filename):

    model_id = None

    if filename[0:5] == 'smdx_' and filename[-4:] == '.xml':
        try:
            model_id = int(filename[5:-4])
        except Exception as e:
            pass

    return model_id
