
"""
  Copyright (c) 2014, SunSpec Alliance
  All Rights Reserved

"""

import sys
import os

import sunspec.core.device as device
import sunspec.core.modbus.client as modbus

def test_trace_func(s):
    print s

def test_modbus_client_device_rtu_read(pathlist=None):
    """
    -> 01 03 9C 40 00 02 EB 8F
    <- 01 03 04 53 75 6E 53 96 F0
    """

    try:
        d = modbus.ModbusClientDeviceRTU(1, modbus.TEST_NAME, trace_func=None)

        d.client.serial.in_buf = '\x01\x03\x04\x53\x75\x6E\x53\x96\xF0'
        d.client.serial.out_buf = ''

        data = d.read(40000, 2)

        if d.client.serial.out_buf != '\x01\x03\x9C\x40\x00\x02\xEB\x8F':
            raise Exception("Modbus request mismatch")

        if data != 'SunS':
            raise Exception("Read data mismatch - expected: 'SunS' received: %s") % (data)

        d.close()

    except Exception, e:
        print '*** Failure test_modbus_client_device_rtu_read: %s' % str(e)
        return False
    return True

def test_modbus_client_device_rtu_write(pathlist=None):
    """
    -> 01 10 9C 40 00 02 04 41 42 43 44 8B B2
    <- 01 10 9C 40 00 02 6E 4C
    """

    try:
        d = modbus.ModbusClientDeviceRTU(1, modbus.TEST_NAME, trace_func=None)

        d.client.serial.in_buf = '\x01\x10\x9C\x40\x00\x02\x6E\x4C'
        d.client.serial.out_buf = ''

        d.write(40000, 'ABCD')

        if d.client.serial.out_buf != '\x01\x10\x9C\x40\x00\x02\x04\x41\x42\x43\x44\x8B\xB2':
            raise Exception("Modbus request mismatch")

        d.close()

    except Exception, e:
        print '*** test_modbus_client_device_rtu_write: %s' % str(e)
        return False
    return True

def test_modbus_client_device_tcp_read(pathlist=None):
    """
    -> 00 00 00 00 00 06 01 03 9C 40 00 02
    <- 00 00 00 00 00 07 01 03 04 53 75 6E 53
    """

    try:
        d = modbus.ModbusClientDeviceTCP(1, ipaddr="127.0.0.1", trace_func=None, test=True)

        d.socket.in_buf = '\x00\x00\x00\x00\x00\x07\x01\x03\x04\x53\x75\x6E\x53'
        d.socket.out_buf = ''

        data = d.read(40000, 2)

        if d.socket.out_buf != '\x00\x00\x00\x00\x00\x06\x01\x03\x9C\x40\x00\x02':
            raise Exception("Modbus request mismatch")

        if data != 'SunS':
            raise Exception("Read data mismatch - expected: 'SunS' received: %s") % (data)

        d.close()

    except Exception, e:
        raise
        print '*** Failure test_modbus_client_device_tcp_read: %s' % str(e)
        return False
    return True

def test_modbus_client_device_tcp_write(pathlist=None):
    """
    -> 00 00 00 00 00 0B 01 10 9C 40 00 02 04 41 42 43 44
    <- 00 00 00 00 00 06 01 10 9C 40 00 02
    """

    try:
        d = modbus.ModbusClientDeviceTCP(1, ipaddr="127.0.0.1", trace_func=None, test=True)

        d.socket.in_buf = '\x00\x00\x00\x00\x00\x06\x01\x10\x9C\x40\x00\x02'
        d.socket.out_buf = ''

        d.write(40000, 'ABCD')

        if d.socket.out_buf != '\x00\x00\x00\x00\x00\x0B\x01\x10\x9C\x40\x00\x02\x04\x41\x42\x43\x44':
            raise Exception("Modbus request mismatch")

        d.close()
        
    except Exception, e:
        print '*** Failure test_modbus_client_device_tcp_write: %s' % str(e)
        return False
    return True

tests = [
    test_modbus_client_device_rtu_read,
    test_modbus_client_device_rtu_write,
    test_modbus_client_device_tcp_read,
    test_modbus_client_device_tcp_write
]

def test_all(pathlist=None, stop_on_failure=True):

    count_passed = 0
    count_failed = 0
    count_run = 0

    for test in tests:
        count_run += 1
        if test(pathlist) is True:
            count_passed += 1
        else:
            count_failed += 1
            if stop_on_failure is True:
                break

    print 'Test modbus client module: total tests: %d  tests run: %d  tests passed: %d  tests failed: %d' %  (len(tests), count_run, count_passed, count_failed)

    return (count_run, count_passed, count_failed)

if __name__ == "__main__":

    (count_run, count_passed, count_failed) = test_all()
    sys.exit(count_failed)

