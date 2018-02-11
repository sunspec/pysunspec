
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

import sunspec.core.device as device
import sunspec.core.modbus.client as modbus


class TestModbusClient(unittest.TestCase):
    def test_modbus_client_device_rtu_read(self):
        """
        -> 01 03 9C 40 00 02 EB 8F
        <- 01 03 04 53 75 6E 53 96 F0
        """

        d = modbus.ModbusClientDeviceRTU(1, modbus.TEST_NAME, trace_func=None)

        d.client.serial.in_buf = b'\x01\x03\x04\x53\x75\x6E\x53\x96\xF0'
        d.client.serial.out_buf = b''

        data = d.read(40000, 2)

        if d.client.serial.out_buf != b'\x01\x03\x9C\x40\x00\x02\xEB\x8F':
            raise Exception("Modbus request mismatch")

        if data != 'SunS':
            raise Exception("Read data mismatch - expected: 'SunS' received: %s") % (data)

        d.close()


    def test_modbus_client_device_rtu_write(self):
        """
        -> 01 10 9C 40 00 02 04 41 42 43 44 8B B2
        <- 01 10 9C 40 00 02 6E 4C
        """

        d = modbus.ModbusClientDeviceRTU(1, modbus.TEST_NAME, trace_func=None)

        d.client.serial.in_buf = b'\x01\x10\x9C\x40\x00\x02\x6E\x4C'
        d.client.serial.out_buf = b''

        d.write(40000, 'ABCD')

        if d.client.serial.out_buf != b'\x01\x10\x9C\x40\x00\x02\x04\x41\x42\x43\x44\x8B\xB2':
            raise Exception("Modbus request mismatch")

        d.close()


    def test_modbus_client_device_tcp_read(self):
        """
        -> 00 00 00 00 00 06 01 03 9C 40 00 02
        <- 00 00 00 00 00 07 01 03 04 53 75 6E 53
        """

        d = modbus.ModbusClientDeviceTCP(1, ipaddr="127.0.0.1", trace_func=None, test=True)

        d.socket.in_buf = b'\x00\x00\x00\x00\x00\x07\x01\x03\x04\x53\x75\x6E\x53'
        d.socket.out_buf = b''

        data = d.read(40000, 2)

        if d.socket.out_buf != b'\x00\x00\x00\x00\x00\x06\x01\x03\x9C\x40\x00\x02':
            raise Exception("Modbus request mismatch")

        if data != b'SunS':
            raise Exception("Read data mismatch - expected: 'SunS' received: %s") % (data)

        d.close()


    def test_modbus_client_device_tcp_write(self):
        """
        -> 00 00 00 00 00 0B 01 10 9C 40 00 02 04 41 42 43 44
        <- 00 00 00 00 00 06 01 10 9C 40 00 02
        """

        d = modbus.ModbusClientDeviceTCP(1, ipaddr="127.0.0.1", trace_func=None, test=True)

        d.socket.in_buf = b'\x00\x00\x00\x00\x00\x06\x01\x10\x9C\x40\x00\x02'
        d.socket.out_buf = b''

        d.write(40000, 'ABCD')

        if d.socket.out_buf != b'\x00\x00\x00\x00\x00\x0B\x01\x10\x9C\x40\x00\x02\x04\x41\x42\x43\x44':
            raise Exception("Modbus request mismatch")

        d.close()


if __name__ == "__main__":

    unittest.main()
