
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
import unittest

try:
    import xml.etree.ElementTree as ET
except:
    import elementtree.ElementTree as ET

import sunspec.core.device as device
import sunspec.core.util as util
import sunspec.core.modbus.mbmap as mbmap


class TestModbusMap(unittest.TestCase):
    def setUp(self):
        path = os.path.abspath(__file__)
        self.pathlist = util.PathList(['.',
                                       os.path.join(os.path.dirname(path),
                                                    'devices')])

    def test_modbus_mbmap_from_xml_file(self):
        m1 = mbmap.ModbusMap()
        m1.from_xml('mbmap_test_device_1.xml', self.pathlist)

        m2 = mbmap.ModbusMap()
        m2.from_xml('mbmap_test_device_1_a.xml', self.pathlist)
        not_equal =  m1.not_equal(m2)
        if not_equal:
            raise Exception(not_equal)

        m3 = mbmap.ModbusMap()
        m3.from_xml('mbmap_test_device_1_b.xml', self.pathlist)
        not_equal =  m1.not_equal(m3)
        if not_equal:
            raise Exception(not_equal)

        m4 = mbmap.ModbusMap()
        m4.from_xml('mbmap_test_device_1_c.xml', self.pathlist)
        not_equal =  m1.not_equal(m4)
        if not_equal:
            raise Exception(not_equal)


    def test_modbus_mbmap_from_xml_element(self):
        filename = os.path.join(self.pathlist.path[1],
                                'mbmap_test_device_1.xml')

        f = open(filename, 'r')
        map_data = f.read()
        f.close()
        root = ET.fromstring(map_data)

        m1 = mbmap.ModbusMap()
        m1.from_xml(element=root)

        m2 = mbmap.ModbusMap()
        m2.from_xml('mbmap_test_device_1_a.xml', self.pathlist)
        not_equal =  m1.not_equal(m2)
        if not_equal:
            raise Exception(not_equal)

        m3 = mbmap.ModbusMap()
        m3.from_xml('mbmap_test_device_1_b.xml', self.pathlist)
        not_equal =  m1.not_equal(m3)
        if not_equal:
            raise Exception(not_equal)

        m4 = mbmap.ModbusMap()
        m4.from_xml('mbmap_test_device_1_c.xml', self.pathlist)
        not_equal =  m1.not_equal(m4)
        if not_equal:
            raise Exception(not_equal)


if __name__ == "__main__":

    unittest.main()
