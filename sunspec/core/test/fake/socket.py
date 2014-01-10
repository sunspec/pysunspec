
"""
  Copyright (c) 2014, SunSpec Alliance
  All Rights Reserved

"""

class socket(object):

    def __init__(self, family=None, stype=None, proto=None):

        self.test_socket = True
        self.family = family
        self.stype = stype
        self.proto = proto
        self.connected = False
        self.timeout = 0
        self.in_buf = ''
        self.out_buf = ''

    def connect(self, addr_port):
    	self.connected = True

    def settimeout(self, timeout):
    	self.timeout = timeout

    def close(self):
    	self.connected = False

    def recv(self, size):
        data = ''
        read_len = size

        data_len = len(self.in_buf)
    	if data_len < read_len:
    		read_len = data_len

    	if read_len > 0:
    		data = self.in_buf[:read_len]
    		self.in_buf = self.in_buf[read_len:]
    	return data

    def send(self, data):
    	self.out_buf += data

    def sendall(self, data):
    	self.out_buf += data
