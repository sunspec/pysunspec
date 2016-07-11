
"""
    Copyright (C) 2016 SunSpec Alliance

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

import sunspec.core.data as data
import sunspec.core.util as util

def test_data(pathlist=None):
    t = 1387560564.48
    expected_xml = '<sunSpecData><d lid="00:00:00:00:00:01" man="Man" mod="Mod" sn="SN" t="2013-12-20T17:29:24Z"><m id="1"><p id="P1">23</p><p id="P2">24</p></m></d></sunSpecData>'

    try:
        sd = data.SunSpecData()
        # def __init__(self, logger_id=None, namespace=None, device_id=None, ifc=None, man=None, mod=None, sn=None, time=None, cid=None):
        d = sd.device_add(logger_id='00:00:00:00:00:01', man='Man', mod='Mod', sn='SN', timestamp=t)
        m = d.model_add(1)
        m.point_add("P1", 23)
        m.point_add("P2", 24)

        # print sd.to_xml(pretty_print=True)
        xml = sd.to_xml_str()
        if xml != expected_xml:
            raise Exception('XML mismatch: %s %s' % (xml, expected_xml))

    except Exception, e:
        raise
        print '*** Failure test_data: %s' % str(e)
        return False
    return True

tests = [
    test_data,
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

    print 'Test data module: total tests: %d  tests run: %d  tests passed: %d  tests failed: %d' %  (len(tests), count_run, count_passed, count_failed)

    return (count_run, count_passed, count_failed)

if __name__ == "__main__":

    (count_run, count_passed, count_failed) = test_all()
    sys.exit(count_failed)
