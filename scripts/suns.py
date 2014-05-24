#!/usr/bin/env python

"""
  Copyright (c) 2014, SunSpec Alliance
  All Rights Reserved

"""

import sys
import time
import sunspec.core.client as client
import sunspec.core.suns as suns
from optparse import OptionParser

"""
  Original suns options:

      -o: output mode for data (text, xml)
      -x: export model description (slang, xml)
      -t: transport type: tcp or rtu (default: tcp)
      -a: modbus slave address (default: 1)
      -i: ip address to use for modbus tcp (default: localhost)
      -P: port number for modbus tcp (default: 502)
      -p: serial port for modbus rtu (default: /dev/ttyUSB0)
      -b: baud rate for modbus rtu (default: 9600)
      -T: timeout, in seconds (can be fractional, such as 1.5; default: 2.0)
      -r: number of retries attempted for each modbus read
      -m: specify model file
      -M: specify directory containing model files
      -s: run as a test server
      -I: logger id (for sunspec logger xml output)
      -N: logger id namespace (for sunspec logger xml output, defaults to 'mac')
      -l: limit number of registers requested in a single read (max is 125)
      -c: check models for internal consistency then exit
      -v: verbose level (up to -vvvv for most verbose)
      -V: print current release number and exit
"""

if __name__ == "__main__":

    usage = 'usage: %prog [options]'
    parser = OptionParser(usage=usage)
    parser.add_option('-t', metavar=' ',
                      default='tcp',
                      help='transport type: rtu, tcp, mapped [default: tcp]')
    parser.add_option('-a', metavar=' ', type='int',
                      default=1,
                      help='modbus slave address [default: 1]')
    parser.add_option('-i', metavar=' ',
                      default='localhost',
                      help='ip address to use for modbus tcp [default: localhost]')
    parser.add_option('-P', metavar=' ', type='int',
                      default=502,
                      help='port number for modbus tcp [default: 502]')
    parser.add_option('-p', metavar=' ',
                      default='/dev/ttyUSB0',
                      help='serial port for modbus rtu [default: /dev/ttyUSB0]')
    parser.add_option('-b', metavar=' ',
                      default=9600,
                      help='baud rate for modbus rtu [default: 9600]')
    parser.add_option('-T', metavar=' ', type='float',
                      default=2.0,
                      help='timeout, in seconds (can be fractional, such as 1.5) [default: 2.0]')
    parser.add_option('-m', metavar=' ',
                      help='modbus map file')

    options, args = parser.parse_args()

    try:
        if options.t == 'tcp':
            sd = client.SunSpecClientDevice(client.TCP, 1, ipaddr=options.i, ipport=options.P, timeout=options.T)
        elif options.t == 'rtu':
            sd = client.SunSpecClientDevice(client.RTU, options.a, name=options.p, baudrate=options.b, timeout=options.T)
        elif options.t == 'mapped':
            sd = client.SunSpecClientDevice(client.MAPPED, options.a, name=options.m)
        else:
            print 'Unknown -t option: %s' % (options.t)
            sys.exit(1)

    except client.SunSpecClientError, e:
        print 'Error: %s' % (e)
        sys.exit(1)

    if sd is not None:
        print '\nTimestamp: %s' % (time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))

        # read all models in the device
        sd.read()

        for model in sd.device.models_list:
            if model.model_type.label:
                label = '%s (%s)' % (model.model_type.label, str(model.id))
            else:
                label = '(%s)' % (str(model.id))
            print '\nmodel: %s\n' % (label)
            for block in model.blocks:
                if block.index > 0:
                  index = '%02d:' % (block.index)
                else:
                  index = '   '
                for point in block.points_list:
                    if point.value is not None:
                        if point.point_type.label:
                            label = '   %s%s (%s):' % (index, point.point_type.label, point.point_type.id)
                        else:
                            label = '   %s(%s):' % (index, point.point_type.id)
                        units = point.point_type.units
                        if units is None:
                            units = ''
                        if point.point_type.type == suns.SUNS_TYPE_BITFIELD16:
                            value = '0x%04x' % (point.value)
                        elif point.point_type.type == suns.SUNS_TYPE_BITFIELD32:
                            value = '0x%08x' % (point.value)
                        else:
                            value = str(point.value).rstrip('\0')
                        print '%-40s %20s %-10s' % (label, value, str(units))

