
"""
  Copyright (c) 2014, SunSpec Alliance
  All Rights Reserved

"""

import sys
import os

import sunspec.core.device as device
import sunspec.core.util as util
import sunspec.core.modbus.mbmap as mbmap

def test_modbus_mbmap_from_xml(pathlist=None):

    try:
        m1 = mbmap.ModbusMap()
        m1.from_xml('mbmap_test_device_1.xml', pathlist)

        m2 = mbmap.ModbusMap()
        m2.from_xml('mbmap_test_device_1_a.xml', pathlist)
        not_equal =  m1.not_equal(m2)
        if not_equal:
            raise Exception(not_equal)

        m3 = mbmap.ModbusMap()
        m3.from_xml('mbmap_test_device_1_b.xml', pathlist)
        not_equal =  m1.not_equal(m3)
        if not_equal:
            raise Exception(not_equal)

        m4 = mbmap.ModbusMap()
        m4.from_xml('mbmap_test_device_1_c.xml', pathlist)
        not_equal =  m1.not_equal(m4)
        if not_equal:
            raise Exception(not_equal)

    except Exception, e:
        print '*** Failure test_modbus_mbmap_from_xml: %s' % str(e)
        return False
    return True

tests = [
    test_modbus_mbmap_from_xml,
]

def test_all(pathlist=None, stop_on_failure=True):

    if pathlist is None:
        pathlist = util.PathList(['.', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'devices')])

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

    print 'Test modbus mbmap module: total tests: %d  tests run: %d  tests passed: %d  tests failed: %d' %  (len(tests), count_run, count_passed, count_failed)

    return (count_run, count_passed, count_failed)

if __name__ == "__main__":

    (count_run, count_passed, count_failed) = test_all()
    sys.exit(count_failed)

