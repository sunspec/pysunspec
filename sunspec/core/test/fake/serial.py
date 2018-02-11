
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

EIGHTBITS = 8
PARITY_NONE = 'N'
STOPBITS_ONE = 1

class Serial(object):

    def __init__(self, port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE,
    	         timeout=None, xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False, interCharTimeout=None):

        self.test_serial = True
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.xonoff = xonxoff
        self.rtscts = rtscts
        self.writeTimeout = writeTimeout
        self.dsrdtr = dsrdtr
        self.interCharTimeout = interCharTimeout
        self.is_open = False
        self.in_buf = b''
        self.out_buf = b''

        self.open()


    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def read(self, size=1):
        data = ''
        read_len = size

        data_len = len(self.in_buf)
        if data_len < read_len:
          read_len = data_len

        if read_len > 0:
                data = self.in_buf[:read_len]
                self.in_buf = self.in_buf[read_len:]
        return data

    def write(self, data):
        self.out_buf += data

    def flushInput(self):
        pass

    def flushOutput(self):
        pass
