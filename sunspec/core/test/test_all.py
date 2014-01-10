
"""
  Copyright (c) 2014, SunSpec Alliance
  All Rights Reserved

"""

import sys
import os
import sunspec

test_modules = [
    'test_device',
    'test_client',
    'test_modbus_client',
    'test_modbus_mbmap',
    'test_data'
]

def test_all(pathlist=None, stop_on_failure=False, local=False):

    total_count_run = 0
    total_count_passed = 0
    total_count_failed = 0

    current_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(current_path)

    # add current directory path if local is true
    if local:
    	local_path = os.path.join(current_path, '..', '..', '..')
    	if sys.path[1] != local_path:
    		print 'Adding local path: ', local_path
    		sys.path.insert(1, local_path)
    	else:
            print 'Using local path: ', local_path

    print 'pySunSpec version: %s\nTest device path: %s\n' % (sunspec.version, os.path.join(current_path, 'devices'))

    for m in test_modules:
        module = __import__(m)
        (count_run, count_passed, count_failed) = module.test_all(pathlist, stop_on_failure)
        total_count_run += count_run
        total_count_passed += count_passed
        total_count_failed += count_failed

    print '\nTotal tests run: %d  Total tests passed: %d  Total tests failed: %d' % (total_count_run, total_count_passed, total_count_failed)
    return (total_count_run, total_count_passed, total_count_failed)

if __name__ == "__main__":

    local = False

    if len(sys.argv) > 1 and sys.argv[1] == 'local':
    	local = True

    (count_run, count_passed, count_failed) = test_all(local=local)
    sys.exit(count_failed)
