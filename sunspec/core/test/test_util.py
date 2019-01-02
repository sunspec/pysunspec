
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

import sys
import os
import time
import unittest

import sunspec.core.util as util

class TestUtil(unittest.TestCase):

    def test_data_to_s16(self):
        self.assertEqual(util.data_to_s16(b'\x12\x34'), int(4660))
        self.assertEqual(util.data_to_s16(b'\x92\x34'), int(-28108))

    def test_data_to_u16(self):
        self.assertEqual(util.data_to_u16(b'\x12\x34'), int(4660))
        self.assertEqual(util.data_to_u16(b'\x92\x34'), int(37428))

    def test_data_to_s32(self):
        self.assertEqual(util.data_to_s32(b'\x12\x34\x56\x78'), int(305419896))
        self.assertEqual(util.data_to_s32(b'\x92\x34\x56\x78'), int(-1842063752))

    def test_data_to_u32(self):
        self.assertEqual(util.data_to_u32(b'\x12\x34\x56\x78'), int(305419896))
        self.assertEqual(util.data_to_u32(b'\x92\x34\x56\x78'), int(2452903544))

    def test_data_to_s64(self):
        self.assertEqual(util.data_to_s64(b'\x12\x34\x56\x78\x12\x34\x56\x78'), int(1311768465173141112))
        self.assertEqual(util.data_to_s64(b'\x92\x34\x56\x78\x12\x34\x56\x78'), int(-7911603571681634696))

    def test_data_to_u64(self):
        self.assertEqual(util.data_to_u64(b'\x12\x34\x56\x78\x12\x34\x56\x78'), int(1311768465173141112))
        self.assertEqual(util.data_to_u64(b'\x92\x34\x56\x78\x12\x34\x56\x78'), int(10535140502027916920))

    def test_data_to_ipv6addr(self):
        self.assertEqual(util.data_to_ipv6addr(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'), None)
        self.assertEqual(util.data_to_ipv6addr(b'\x12\x34\x56\x78\x9A\xBC\xDE\xF0\x12\x34\x56\x78\x9A\xBC\xDE\xF0'), '12345678:9ABCDEF0:12345678:9ABCDEF0')
        self.assertEqual(util.data_to_ipv6addr(b'\x01\x00\x00\x00\x00\x00\x00\x00'), None)

    def test_data_to_eui48(self):
        self.assertEqual(util.data_to_eui48(b'\x00\x00\x00\x00\x00\x00\x00\x00'), None)
        self.assertEqual(util.data_to_eui48(b'\x00\x00\x12\x34\x56\x78\x9A\xBC'), '12:34:56:78:9A:BC')

    def test_data_to_float(self):
        self.assertEqual(util.data_to_float(b'\x7f\xc0\x00\x00'), None)
        self.assertEqual(util.data_to_float(b'\x44\x7a\x00\x00'), float(1000))
        self.assertEqual(util.data_to_float(b'\xc4\x7a\x00\x00'), float(-1000))

    def test_data_to_double(self):
        self.assertEqual(util.data_to_double(b'\x7F\xF8\x00\x00\x00\x00\x00\x00'), None)
        self.assertEqual(util.data_to_double(b'\x40\x8f\x40\x00\x00\x00\x00\x00'), float(1000))
        self.assertEqual(util.data_to_double(b'\xc0\x8f\x40\x00\x00\x00\x00\x00'), float(-1000))

    def test_data_to_str(self):
        self.assertEqual(util.data_to_str(b'\x53\x75\x6e\x53\x70\x65\x63\x20\x54\x65\x73\x74\x00'), 'SunSpec Test')


    def test_s16_to_data(self):
        self.assertEqual(util.s16_to_data(int(4660)), b'\x12\x34')
        self.assertEqual(util.s16_to_data(int(-28108)), b'\x92\x34')

    def test_u16_to_data(self):
        self.assertEqual(util.u16_to_data(int(4660)), b'\x12\x34')
        self.assertEqual(util.u16_to_data(int(37428)), b'\x92\x34')

    def test_s32_to_data(self):
        self.assertEqual(util.s32_to_data(int(305419896)), b'\x12\x34\x56\x78')
        self.assertEqual(util.s32_to_data(int(-1842063752)), b'\x92\x34\x56\x78')

    def test_u32_to_data(self):
        self.assertEqual(util.u32_to_data(int(305419896)), b'\x12\x34\x56\x78')
        self.assertEqual(util.u32_to_data(int(2452903544)), b'\x92\x34\x56\x78')

    def test_s64_to_data(self):
        self.assertEqual(util.s64_to_data(int(1311768465173141112)), b'\x12\x34\x56\x78\x12\x34\x56\x78')
        self.assertEqual(util.s64_to_data(int(-7911603571681634696)), b'\x92\x34\x56\x78\x12\x34\x56\x78')

    def test_u64_to_data(self):
        self.assertEqual(util.u64_to_data(int(1311768465173141112)), b'\x12\x34\x56\x78\x12\x34\x56\x78')
        self.assertEqual(util.u64_to_data(int(10535140502027916920)), b'\x92\x34\x56\x78\x12\x34\x56\x78')

    def test_ipv6addr_to_data(self):
        self.assertEqual(util.ipv6addr_to_data('12345678:9ABCDEF0:12345678:9ABCDEF0'), b'\x12\x34\x56\x78\x9A\xBC\xDE\xF0\x12\x34\x56\x78\x9A\xBC\xDE\xF0')

    def test_float_to_data32(self):
        self.assertEqual(util.float_to_data32(float(1000)), b'\x44\x7a\x00\x00')
        self.assertEqual(util.float_to_data32(float(-1000)), b'\xc4\x7a\x00\x00')

    def test_float32_to_data(self):
        self.assertEqual(util.float32_to_data(float(1000)), b'\x44\x7a\x00\x00')
        self.assertEqual(util.float32_to_data(float(-1000)), b'\xc4\x7a\x00\x00')

    def test_float_to_data(self):
        self.assertEqual(util.float_to_data(float(1000)), b'\x40\x8f\x40\x00\x00\x00\x00\x00')
        self.assertEqual(util.float_to_data(float(-1000)), b'\xc0\x8f\x40\x00\x00\x00\x00\x00')

    def test_str_to_data(self):
        self.assertEqual(util.str_to_data('SunSpec Test'), b'\x53\x75\x6e\x53\x70\x65\x63\x20\x54\x65\x73\x74\x00')

    def test_eui48_to_data(self):
        self.assertEqual(util.eui48_to_data('12:34:56:78:9A:BC'), b'\x00\x00\x12\x34\x56\x78\x9A\xBC')


if __name__ == "__main__":

    unittest.main()
