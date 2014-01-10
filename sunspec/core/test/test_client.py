
"""
  Copyright (c) 2014, SunSpec Alliance
  All Rights Reserved

"""

import sys
import os

import sunspec.core.client as client
import sunspec.core.device as device
import sunspec.core.util as util

def test_client_device(pathlist=None):

    try:
        d = client.ClientDevice(client.MAPPED, slave_id=1, name='mbmap_test_device_1.xml', pathlist = pathlist)
        d.scan()
        d.read_points()

        dp = device.Device()
        dp.from_pics(filename='pics_test_device_1.xml', pathlist=pathlist)
        not_equal = dp.not_equal(d)
        if not_equal:
            raise Exception(not_equal)

    except Exception, e:
        print '*** Failure test_client_device: %s' % str(e)
        return False
    return True

def test_sunspec_client_device_1(pathlist=None):

    try:
        d = client.SunSpecClientDevice(client.MAPPED, slave_id=1, name='mbmap_test_device_1.xml', pathlist = pathlist)

        dp = device.Device()
        dp.from_pics(filename='pics_test_device_1.xml', pathlist=pathlist)
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

        d.close()

    except Exception, e:
        print '*** Failure test_sunspec_client_device_1: %s' % str(e)
        return False
    return True

def test_sunspec_client_device_3(pathlist=None):

    try:
        d = client.SunSpecClientDevice(client.MAPPED, slave_id=1, name='mbmap_test_device_3.xml', pathlist = pathlist)

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

    except Exception, e:
        print '*** Failure test_sunspec_client_device_3: %s' % str(e)
        return False
    return True

tests = [
    test_client_device,
    test_sunspec_client_device_1,
    test_sunspec_client_device_3
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

    print 'Test client module: total tests: %d  tests run: %d  tests passed: %d  tests failed: %d' %  (len(tests), count_run, count_passed, count_failed)

    return (count_run, count_passed, count_failed)

if __name__ == "__main__":

    (count_run, count_passed, count_failed) = test_all()
    sys.exit(count_failed)
