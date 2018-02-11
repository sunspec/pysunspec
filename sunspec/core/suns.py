
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

import sunspec.core.util as util
import sys

# Python 3 compatibility for long()
if sys.version_info > (3,):
    long = int

SUNS_BASE_ADDR_DEFAULT = 40000
SUNS_SUNS_LEN = 2

SUNS_TYPE_INT16 = 'int16'
SUNS_TYPE_UINT16 = 'uint16'
SUNS_TYPE_COUNT = 'count'
SUNS_TYPE_ACC16 = 'acc16'
SUNS_TYPE_ENUM16 = 'enum16'
SUNS_TYPE_BITFIELD16 = 'bitfield16'
SUNS_TYPE_PAD = 'pad'
SUNS_TYPE_INT32 = 'int32'
SUNS_TYPE_UINT32 = 'uint32'
SUNS_TYPE_ACC32 = 'acc32'
SUNS_TYPE_ENUM32 = 'enum32'
SUNS_TYPE_BITFIELD32 = 'bitfield32'
SUNS_TYPE_IPADDR = 'ipaddr'
SUNS_TYPE_INT64 = 'int64'
SUNS_TYPE_UINT64 = 'uint64'
SUNS_TYPE_ACC64 = 'acc64'
SUNS_TYPE_IPV6ADDR = 'ipv6addr'
SUNS_TYPE_FLOAT32 = 'float32'
SUNS_TYPE_STRING = 'string'
SUNS_TYPE_SUNSSF = 'sunssf'
SUNS_TYPE_EUI48 = 'eui48'

SUNS_ACCESS_R = 'r'
SUNS_ACCESS_RW = 'rw'

SUNS_MANDATORY_FALSE = 'false'
SUNS_MANDATORY_TRUE = 'true'

SUNS_UNIMPL_INT16 = -32768
SUNS_UNIMPL_UINT16 = 0xffff
SUNS_UNIMPL_ACC16 = 0
SUNS_UNIMPL_ENUM16 = 0xffff
SUNS_UNIMPL_BITFIELD16 = 0xffff
SUNS_UNIMPL_INT32 = -2147483648
SUNS_UNIMPL_UINT32 = 0xffffffff
SUNS_UNIMPL_ACC32 = 0
SUNS_UNIMPL_ENUM32 = 0xffffffff
SUNS_UNIMPL_BITFIELD32 = 0xffffffff
SUNS_UNIMPL_IPADDR = 0
SUNS_UNIMPL_INT64 = -9223372036854775808
SUNS_UNIMPL_UINT64 = 0xffffffffffffffff
SUNS_UNIMPL_ACC64 = 0
SUNS_UNIMPL_IPV6ADDR = 0
SUNS_UNIMPL_FLOAT32 = 0x7fc00000
SUNS_UNIMPL_STRING = 0
SUNS_UNIMPL_SUNSSF = -32768
SUNS_UNIMPL_EUI48 = 'FF:FF:FF:FF:FF:FF'

SUNS_BLOCK_FIXED = 'fixed'
SUNS_BLOCK_REPEATING = 'repeating'

SUNS_END_MODEL_ID = 0xffff

def suns_to_int(x):
    try:
        return int(x, 0)
    except TypeError:
        return int(x)

def suns_to_long(x):
    try:
        return long(x, 0)
    except TypeError:
        return long(x)

def suns_to_str(s):
    return str(s)

def suns_to_float(f):
    try:
        return float(f)
    except ValueError:
        return None

def suns_is_impl_int16(value):
    return not value == SUNS_UNIMPL_INT16

def suns_is_impl_uint16(value):
    return not value == SUNS_UNIMPL_UINT16

def suns_is_impl_acc16(value):
    return not value == SUNS_UNIMPL_ACC16

def suns_is_impl_enum16(value):
    return not value == SUNS_UNIMPL_ENUM16

def suns_is_impl_bitfield16(value):
    return not value == SUNS_UNIMPL_BITFIELD16

def suns_is_impl_int32(value):
    return not value == SUNS_UNIMPL_INT32

def suns_is_impl_uint32(value):
    return not value == SUNS_UNIMPL_UINT32

def suns_is_impl_acc32(value):
    return not value == SUNS_UNIMPL_ACC32

def suns_is_impl_enum32(value):
    return not value == SUNS_UNIMPL_ENUM32

def suns_is_impl_bitfield32(value):
    return not value == SUNS_UNIMPL_BITFIELD32

def suns_is_impl_ipaddr(value):
    return not value == SUNS_UNIMPL_IPADDR

def suns_is_impl_int64(value):
    return not value == SUNS_UNIMPL_INT64

def suns_is_impl_uint64(value):
    return not value == SUNS_UNIMPL_UINT64

def suns_is_impl_acc64(value):
    return not value == SUNS_UNIMPL_ACC64

def suns_is_impl_ipv6addr(value):
    if value:
        return not value[0] == '\0'
    return False

def suns_is_impl_float32(value):
    return (value == value) and (value != None)

def suns_is_impl_string(value):
    if value:
        return not value[0] == '\0'
    return False

def suns_is_impl_sunssf(value):
    return not value == SUNS_UNIMPL_SUNSSF

def suns_is_impl_eui48(value):
    return not value == SUNS_UNIMPL_EUI48

# each entry contains: (len in registers, uniplemented value, data to value function, value to data function, to value function, default value)
suns_point_type_info = {
    SUNS_TYPE_INT16: (1, suns_is_impl_int16, util.data_to_s16, util.s16_to_data, suns_to_int, 0),
    SUNS_TYPE_UINT16: (1, suns_is_impl_uint16, util.data_to_u16, util.u16_to_data, suns_to_int, 0),
    SUNS_TYPE_COUNT: (1, suns_is_impl_uint16, util.data_to_u16, util.u16_to_data, suns_to_int, 0),
    SUNS_TYPE_ACC16: (1, suns_is_impl_acc16, util.data_to_u16, util.u16_to_data, suns_to_int, 0),
    SUNS_TYPE_ENUM16: (1, suns_is_impl_enum16, util.data_to_u16, util.u16_to_data, suns_to_int, 0),
    SUNS_TYPE_BITFIELD16: (1, suns_is_impl_bitfield16, util.data_to_u16, util.u16_to_data, suns_to_int, 0),
    SUNS_TYPE_PAD: (1, suns_is_impl_int16, util.data_to_s16, util.s16_to_data, suns_to_int, 0),
    SUNS_TYPE_INT32: (2, suns_is_impl_int32, util.data_to_s32, util.s32_to_data, suns_to_int, 0),
    SUNS_TYPE_UINT32: (2, suns_is_impl_uint32, util.data_to_u32, util.u32_to_data, suns_to_long, 0),
    SUNS_TYPE_ACC32: (2, suns_is_impl_acc32, util.data_to_u32, util.u32_to_data, suns_to_long, 0),
    SUNS_TYPE_ENUM32: (2, suns_is_impl_enum32, util.data_to_u32, util.u32_to_data, suns_to_long, 0),
    SUNS_TYPE_BITFIELD32: (2, suns_is_impl_bitfield32, util.data_to_u32, util.u32_to_data, suns_to_long, 0),
    SUNS_TYPE_IPADDR: (2, suns_is_impl_ipaddr, util.data_to_u32, util.u32_to_data, suns_to_long, 0),
    SUNS_TYPE_INT64: (4, suns_is_impl_int64, util.data_to_s64, util.s64_to_data, suns_to_long, 0),
    SUNS_TYPE_UINT64: (4, suns_is_impl_uint64, util.data_to_s64, util.s64_to_data, suns_to_long, 0),
    SUNS_TYPE_ACC64: (4, suns_is_impl_acc64, util.data_to_s64, util.s64_to_data, suns_to_long, 0),
    SUNS_TYPE_IPV6ADDR: (8, suns_is_impl_ipv6addr, util.data_to_ipv6addr, util.ipv6addr_to_data, suns_to_str, 0),
    SUNS_TYPE_FLOAT32: (2, suns_is_impl_float32, util.data_to_float, util.float_to_data32, suns_to_float, 0),
    SUNS_TYPE_STRING: (None, suns_is_impl_string, util.data_to_str, util.str_to_data, suns_to_str, ''),
    SUNS_TYPE_SUNSSF: (1, suns_is_impl_sunssf, util.data_to_s16, util.s16_to_data, suns_to_int, 0),
    SUNS_TYPE_EUI48: (4, suns_is_impl_eui48, util.data_to_eui48, util.eui48_to_data, suns_to_str, 0)
}
