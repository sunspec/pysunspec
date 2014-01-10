
"""
  Copyright (c) 2014, SunSpec Alliance
  All Rights Reserved

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
        self.in_buf = ''
        self.out_buf = ''

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
