
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

import sunspec.core.client as client
import sunspec.core.device as device
import sunspec.core.util as util


class TestClientDevice(unittest.TestCase):
    def setUp(self):
        path = os.path.abspath(__file__)
        self.pathlist = util.PathList(['.',
                                       os.path.join(os.path.dirname(path),
                                                    'devices')])

        device.check_for_models(pathlist=self.pathlist)

    def test_client_device(self):
        d = client.ClientDevice(client.MAPPED, slave_id=1,
                                name='mbmap_test_device_1.xml',
                                pathlist=self.pathlist)
        d.scan()
        d.read_points()

        dp = device.Device()
        dp.from_pics(filename='pics_test_device_1.xml',
                        pathlist=self.pathlist)
        not_equal = dp.not_equal(d)
        if not_equal:
            raise Exception(not_equal)


    def test_sunspec_client_device_1(self):
        d = client.SunSpecClientDevice(client.MAPPED, slave_id=1,
                                        name='mbmap_test_device_1.xml',
                                        pathlist=self.pathlist)
        d.read()

        dp = device.Device()
        dp.from_pics(filename='pics_test_device_1.xml',
                        pathlist=self.pathlist)
        not_equal = dp.not_equal(d.device)
        if not_equal:
            raise Exception(not_equal)

        expected = 'SunSpecTest'
        if d.common.Mn != expected:
            raise Exception("'common.Mn' point mismatch: %s %s" % (d.common.Mn, expected))

        expected = 'sn-123456789'
        if d.common.SN != expected:
            raise Exception("'common.SN' point mismatch: %s %s" % (d.common.SN, expected))


        # int16 read and write
        d.model_63001.read()
        expected = -20
        if d.model_63001.int16_4 != expected:
            raise Exception("'model_63001.int16_4' point mismatch: %s %s" % (d.model_63001.int16_4, expected))
        value = 330
        d.model_63001.int16_4 = value
        d.model_63001.write()
        d.model_63001.read()
        value = d.model_63001.int16_4
        if d.model_63001.int16_4 != value:
            raise Exception("'model_63001.int16_4' write failure: %s %s" % (d.model_63001.int16_4, value))

        # string read and write
        expected = '12345678'
        if d.model_63001.string != expected:
            raise Exception("'model_63001.string' point mismatch: %s %s" % (d.model_63001.string, expected))

        value = 'abcdefg'
        d.model_63001.string = value
        d.model_63001.write()
        d.model_63001.read()
        if d.model_63001.string != value:
            raise Exception("'model_63001.string' write failure: %s %s" % (d.model_63001.string, value))

        # write multiple
        d.model_63001.read()
        expected = 65524
        if d.model_63001.uint16_3 != expected:
            raise Exception("'model_63001.uint16_3' point mismatch: %s %s" % (d.model_63001.uint16_3, expected))
        expected = 60
        if d.model_63001.uint16_4 != expected:
            raise Exception("'model_63001.uint16_4' point mismatch: %s %s" % (d.model_63001.uint16_4, expected))
        expected = 7
        if d.model_63001.uint16_5 != expected:
            raise Exception("'model_63001.uint16_5' point mismatch: %s %s" % (d.model_63001.uint16_5, expected))
        value_3 = 65525
        value_4 = 70
        value_5 = 8
        d.model_63001.uint16_3 = value_3
        d.model_63001.uint16_4 = value_4
        d.model_63001.uint16_5 = value_5
        d.model_63001.write()
        d.model_63001.read()
        value = d.model_63001.uint16_3
        if d.model_63001.uint16_3 != value_3:
            raise Exception("'model_63001.int16_3' write failure: %s %s" % (d.model_63001.uint16_3, value_3))
        value = d.model_63001.uint16_4
        if d.model_63001.uint16_4 != value_4:
            raise Exception("'model_63001.int16_4' write failure: %s %s" % (d.model_63001.uint16_4, value_4))
        value = d.model_63001.uint16_5
        if d.model_63001.uint16_5 != value_5:
            raise Exception("'model_63001.int16_5' write failure: %s %s" % (d.model_63001.uint16_5, value_5))

        # write multiple
        d.model_63001.read()
        expected = value_3
        if d.model_63001.uint16_3 != expected:
            raise Exception("'model_63001.uint16_3' point mismatch: %s %s" % (d.model_63001.uint16_3, expected))
        expected = value_4
        if d.model_63001.uint16_4 != expected:
            raise Exception("'model_63001.uint16_4' point mismatch: %s %s" % (d.model_63001.uint16_4, expected))
        expected = value_5
        if d.model_63001.uint16_5 != expected:
            raise Exception("'model_63001.uint16_5' point mismatch: %s %s" % (d.model_63001.uint16_5, expected))
        value_3 = 65524
        value_5 = 7
        d.model_63001.uint16_3 = value_3
        d.model_63001.uint16_5 = value_5
        d.model_63001.write()
        d.model_63001.read()
        value = d.model_63001.uint16_3
        if d.model_63001.uint16_3 != value_3:
            raise Exception("'model_63001.int16_3' write failure: %s %s" % (d.model_63001.uint16_3, value_3))
        value = d.model_63001.uint16_4
        if d.model_63001.uint16_4 != value_4:
            raise Exception("'model_63001.int16_4' write failure: %s %s" % (d.model_63001.uint16_4, value_4))
        value = d.model_63001.uint16_5
        if d.model_63001.uint16_5 != value_5:
            raise Exception("'model_63001.int16_5' write failure: %s %s" % (d.model_63001.uint16_5, value_5))

        d.close()


    def test_sunspec_client_device_3(self):
        d = client.SunSpecClientDevice(client.MAPPED, slave_id=1, name='mbmap_test_device_3.xml', pathlist=self.pathlist)

        # int16 read and write
        d.model_63002.read()
        expected = 1111
        value = int(d.model_63002.repeating[1].int16_1 * 10)
        if  value != expected:
            raise Exception("'model_63002.int16_1' point mismatch: %s %s" % (value, expected))

        d.model_63002.repeating[1].int16_1 = 333.3
        d.model_63002.write()
        d.model_63002.read()
        expected = 3333
        value = int(d.model_63002.repeating[1].int16_1 * 10)
        if value != expected:
            raise Exception("'model_63002.int16_2' write failure: %s %s" % (value, expected))

        expected = 2222
        value = int(d.model_63002.repeating[1].int16_2 * 100)
        if  value != expected:
            raise Exception("'model_63002.int16_1' point mismatch: %s %s" % (value, expected))

        d.close()


if __name__ == "__main__":

    unittest.main()
