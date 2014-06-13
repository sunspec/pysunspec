
"""
  Copyright (c) 2014, SunSpec Alliance
  All Rights Reserved

"""

import os
import socket
import struct
import serial

try:
    import xml.etree.ElementTree as ET
except:
    import elementtree.ElementTree as ET

import sunspec.core.modbus.mbmap as mbmap

PARITY_NONE = 'N'
PARITY_EVEN = 'E'

REQ_COUNT_MAX = 125

FUNC_READ_HOLDING = 3
FUNC_READ_INPUT = 4
FUNC_WRITE_MULTIPLE = 16

TEST_NAME = 'test_name'

modbus_rtu_clients = {}

class ModbusClientError(Exception):
    pass

class ModbusClientTimeout(ModbusClientError):
    pass

class ModbusClientException(ModbusClientError):
    pass

def modbus_rtu_client(name=None, baudrate=None, parity=None):

    global modbus_rtu_clients

    client = modbus_rtu_clients.get(name)
    if client is not None:
        if baudrate is not None and client.baudrate != baudrate:
            raise ModbusClientError('Modbus client baudrate mismatch')
        if parity is not None and client.parity != parity:
            raise ModbusClientError('Modbus client parity mismatch')
    else:
        if baudrate is None:
            baudrate = 9600
        if parity is None:
            parity = PARITY_NONE

        client = ModbusClientRTU(name, baudrate, parity)
        modbus_rtu_clients[name] = client

    return client

def modbus_rtu_client_remove(name=None):

    global modbus_rtu_clients

    if modbus_rtu_clients[name]:
        del modbus_rtu_clients[name]

class ModbusClientRTU(object):

    def __init__(self, name='/dev/ttyUSB0', baudrate=9600, parity=None):
        self.name = name
        self.baudrate = baudrate
        self.parity = parity
        self.serial = None
        self.timeout = .5
        self.write_timeout = .5
        self.devices = {}

        self.open()
        
    def open(self):

        try:
            if self.parity == PARITY_EVEN:
                parity = serial.PARITY_EVEN
            else:
                parity = serial.PARITY_NONE

            if self.name != TEST_NAME:
                self.serial = serial.Serial(port = self.name, baudrate=self.baudrate,
                                            bytesize=8, parity=parity,
                                            stopbits=1, xonxoff=0,
                                            timeout=self.timeout, writeTimeout=self.write_timeout)
            else:
                import sunspec.core.test.fake.serial as fake
                self.serial = fake.Serial(port = self.name, baudrate=self.baudrate,
                                          bytesize=8, parity=parity,
                                          stopbits=1, xonxoff=0,
                                          timeout=self.timeout, writeTimeout=self.write_timeout)

        except Exception, e:
            if self.serial is not None:
                self.serial.close()
                self.serial = None
            raise ModbusClientError('Serial init error: %s' % (e))

    def close(self):

        try:
            if self.serial is not None:
                self.serial.close()
        except Exception, e:
            raise ModbusClientError('Serial close error: %s' % (e))

    def add_device(self, slave_id, device):

        self.devices[slave_id] = device

    def remove_device(self, slave_id):

        if self.devices.get(slave_id):
            del self.devices[slave_id]

        # if no more devices using the client interface, close and remove the client
        if len(self.devices) == 0:
            self.close()
            modbus_rtu_client_remove(self.name)

    def _read(self, slave_id, addr, count, op=FUNC_READ_HOLDING, trace_func=None):
        resp = ''
        len_remaining = 5
        len_found = False
        except_code = None

        req = struct.pack('>BBHH', int(slave_id), op, int(addr), int(count))
        req += struct.pack('>H', computeCRC(req))
        
        if trace_func:
            s = '%s:%s ->' % (self.name, str(slave_id))
            for c in req:
                s += '%02X' % (ord(c))
            trace_func(s)

        self.serial.flushInput()
        try:
            self.serial.write(req)
        except Exception, e:
            raise ModbusClientError('Serial write error: %s' % (e))

        while len_remaining > 0:
            c = self.serial.read(len_remaining)
            len_read = len(c);
            if len_read > 0:
                resp += c
                len_remaining -= len_read
                if len_found is False and len(resp) >= 5:
                    if not (ord(resp[1]) & 0x80):
                        len_remaining = (ord(resp[2]) + 5) - len(resp)
                        len_found = True
                    else:
                        except_code = ord(resp[2])
            else:
                raise ModbusClientTimeout('Response timeout')

        if trace_func:
            s = '%s:%s <--' % (self.name, str(slave_id))
            for c in resp:
                s += '%02X' % (ord(c))
            trace_func(s)

        crc = (ord(resp[-2]) << 8) | ord(resp[-1])
        if not checkCRC(resp[:-2], crc):
            raise ModbusClientError('CRC error')

        if except_code:
            raise ModbusClientException('Modbus exception %d' % (except_code))

        return resp[3:-2]

    def read(self, slave_id, addr, count, op=FUNC_READ_HOLDING, trace_func=None, max_count=REQ_COUNT_MAX):
        resp = ''
        read_count = 0
        read_offset = 0

        if self.serial is not None:
            while (count > 0):
                if count > max_count:
                    read_count = max_count
                else:
                    read_count = count
                data = self._read(slave_id, addr + read_offset, read_count, op=op, trace_func=trace_func)
                if data:
                    resp += data
                    count -= read_count
                    read_offset += read_count
                else:
                    return
        else:
            raise ModbusClientError('Client serial port not open: %s' % self.name)

        return resp

    def _write(self, slave_id, addr, data, trace_func=None):
        resp = ''
        len_remaining = 5
        len_found = False
        except_code = None
        func = FUNC_WRITE_MULTIPLE
        len_data = len(data)
        count = len_data/2

        req = struct.pack('>BBHHB', int(slave_id), func, int(addr), count, len_data)
        req += data
        req += struct.pack('>H', computeCRC(req))

        if trace_func:
            s = '%s:%s ->' % (self.name, str(slave_id))
            for c in req:
                s += '%02X' % (ord(c))
            trace_func(s)

        self.serial.flushInput()
        try:
            self.serial.write(req)
        except Exception, e:
            raise ModbusClientError('Serial write error: %s' % (e))

        while len_remaining > 0:
            c = self.serial.read(len_remaining)
            len_read = len(c);
            if len_read > 0:
                resp += c
                len_remaining -= len_read
                if len_found is False and len(resp) >= 5:
                    if not (ord(resp[1]) & 0x80):
                        len_remaining = 8 - len(resp)
                        len_found = True
                    else:
                        except_code = ord(resp[2])
            else:
                raise ModbusClientTimeout('Response timeout')

        if trace_func:
            s = '%s:%s <--' % (self.name, str(slave_id))
            for c in resp:
                s += '%02X' % (ord(c))
            trace_func(s)


        crc = (ord(resp[-2]) << 8) | ord(resp[-1])
        if not checkCRC(resp[:-2], crc):
            raise ModbusClientError('CRC error')

        if except_code:
            raise ModbusClientException('Modbus exception: %d' % (except_code))
        else:
            resp_slave_id, resp_func, resp_addr, resp_count, resp_crc = struct.unpack('>BBHHH', resp)
            if resp_slave_id != slave_id or resp_func != func or resp_addr != addr or resp_count != count:
                raise ModbusClientError('Mobus response format error')

    def write(self, slave_id, addr, data, trace_func=None, max_count=REQ_COUNT_MAX):
        write_count = 0
        write_offset = 0
        count = len(data)/2

        if self.serial is not None:
            while (count > 0):
                if count > max_count:
                    write_count = max_count
                else:
                    write_count = count
                self._write(slave_id, addr + write_offset, data[(write_offset * 2):((write_offset + write_count) * 2)], trace_func=trace_func)
                count -= write_count
                write_offset += write_count
        else:
            raise ModbusClientError('Client serial port not open: %s' % self.name)

class ModbusClientDeviceRTU(object):

    def __init__(self, slave_id, name, baudrate=None, parity=None, timeout=None, ctx=None, trace_func=None, max_count=REQ_COUNT_MAX):
        self.slave_id = slave_id
        self.name = name
        self.client = None
        self.ctx = ctx
        self.trace_func = trace_func
        self.max_count = max_count

        self.client = modbus_rtu_client(name, baudrate, parity)
        if self.client is None:
            raise ModbusClientError('No modbus rtu client set for device')
        self.client.add_device(self.slave_id, self)

        if timeout is not None and self.client.serial is not None:
            self.client.serial.timeout = timeout
            self.client.serial.writeTimeout = timeout

    def close(self):

        if self.client:
            self.client.remove_device(self.slave_id)

    def read(self, addr, count, op=FUNC_READ_HOLDING):

        return self.client.read(self.slave_id, addr, count, op=op, trace_func=self.trace_func, max_count=self.max_count)

    def write(self, addr, data):

        return self.client.write(self.slave_id, addr, data, trace_func=self.trace_func, max_count=self.max_count)

TCP_HDR_LEN = 6
TCP_RESP_MIN_LEN = 3
TCP_HDR_O_LEN = 4
TCP_READ_REQ_LEN = 6
TCP_WRITE_MULT_REQ_LEN = 7

TCP_DEFAULT_PORT = 502
TCP_DEFAULT_TIMEOUT = 2

class ModbusClientDeviceTCP(object):

    def __init__(self, slave_id, ipaddr, ipport=502, timeout=None, ctx=None, trace_func=None, max_count=REQ_COUNT_MAX, test=False):
        self.slave_id = slave_id
        self.ipaddr = ipaddr
        self.ipport = ipport
        self.timeout = timeout
        self.ctx = ctx
        self.socket = None
        self.trace_func = trace_func
        self.max_count = max_count

        if ipport is None:
            self.ipport = TCP_DEFAULT_PORT
        if timeout is None:
            self.timeout = TCP_DEFAULT_TIMEOUT

        if test:
            import sunspec.core.test.fake.socket as fake
            self.socket = fake.socket()

    def close(self):

        self.disconnect()

    def connect(self, timeout=TCP_DEFAULT_TIMEOUT):

        if self.socket:
            self.disconnect()

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(timeout)
            self.socket.connect((self.ipaddr, self.ipport))
        except Exception, e:
            raise ModbusClientError('Connection error: %s' % (e))

    def disconnect(self):

        try:
            if self.socket:
                self.socket.close()
            self.socket = None
        except Exception:
            pass

    def _read(self, addr, count, op=FUNC_READ_HOLDING):

        resp = ''
        len_remaining = TCP_HDR_LEN + TCP_RESP_MIN_LEN
        len_found = False
        except_code = None

        req = struct.pack('>HHHBBHH', 0, 0, TCP_READ_REQ_LEN, int(self.slave_id), op, int(addr), int(count))

        if self.trace_func:
            s = '%s:%s:%s ->' % (self.ipaddr, str(self.ipport), str(self.slave_id))
            for c in req:
                s += '%02X' % (ord(c))
            self.trace_func(s)

        try:
            self.socket.sendall(req)
        except Exception, e:
            raise ModbusClientError('Socket write error: %s' % (e))

        while len_remaining > 0:
            c = self.socket.recv(len_remaining)
            # print 'c = {0}'.format(c)
            len_read = len(c);
            if len_read > 0:
                resp += c
                len_remaining -= len_read
                if len_found is False and len(resp) >= TCP_HDR_LEN + TCP_RESP_MIN_LEN:
                    data_len = struct.unpack('>H', resp[TCP_HDR_O_LEN:TCP_HDR_O_LEN + 2])
                    len_remaining = data_len[0] - (len(resp) - TCP_HDR_LEN)
            else:
                raise ModbusClientError('Response timeout')

        if not (ord(resp[TCP_HDR_LEN + 1]) & 0x80):
            len_remaining = (ord(resp[TCP_HDR_LEN + 2]) + TCP_HDR_LEN) - len(resp)
            len_found = True
        else:
            except_code = ord(resp[TCP_HDR_LEN + 2])

        if self.trace_func:
            s = '%s:%s:%s <--' % (self.ipaddr, str(self.ipport), str(self.slave_id))
            for c in resp:
                s += '%02X' % (ord(c))
            self.trace_func(s)

        if except_code:
            raise ModbusClientException('Modbus exception %d' % (except_code))

        return resp[(TCP_HDR_LEN + 3):]

    def read(self, addr, count, op=FUNC_READ_HOLDING):

        resp = ''
        read_count = 0
        read_offset = 0
        local_connect = False

        if self.socket is None:
            local_connect = True
            self.connect(self.timeout)

        try:
            while (count > 0):
                if count > self.max_count:
                    read_count = self.max_count
                else:
                    read_count = count
                data = self._read(addr + read_offset, read_count, op=op)
                if data:
                    resp += data
                    count -= read_count
                    read_offset += read_count
                else:
                    break
        finally:
            if local_connect:
                self.disconnect()

        return resp

    def _write(self, addr, data):

        resp = ''
        len_remaining = TCP_HDR_LEN + TCP_RESP_MIN_LEN
        len_found = False
        except_code = None
        func = FUNC_WRITE_MULTIPLE

        write_len = len(data)
        write_count = write_len/2
        req = struct.pack('>HHHBBHHB', 0, 0, TCP_WRITE_MULT_REQ_LEN + write_len, int(self.slave_id), func, int(addr), write_count, write_len)
        req += data

        if self.trace_func:
            s = '%s:%s:%s ->' % (self.ipaddr, str(self.ipport), str(self.slave_id))
            for c in req:
                s += '%02X' % (ord(c))
            self.trace_func(s)

        try:
            self.socket.sendall(req)
        except Exception, e:
            raise ModbusClientError('Socket write error: %s' % (e))

        while len_remaining > 0:
            c = self.socket.recv(len_remaining)
            # print 'c = {0}'.format(c)
            len_read = len(c);
            if len_read > 0:
                resp += c
                len_remaining -= len_read
                if len_found is False and len(resp) >= TCP_HDR_LEN + TCP_RESP_MIN_LEN:
                    data_len = struct.unpack('>H', resp[TCP_HDR_O_LEN:TCP_HDR_O_LEN + 2])
                    len_remaining = data_len[0] - (len(resp) - TCP_HDR_LEN)
            else:
                raise ModbusClientTimeout('Response timeout')

        if not (ord(resp[TCP_HDR_LEN + 1]) & 0x80):
            len_remaining = (ord(resp[TCP_HDR_LEN + 2]) + TCP_HDR_LEN) - len(resp)
            len_found = True
        else:
            except_code = ord(resp[TCP_HDR_LEN + 2])

        if self.trace_func:
            s = '%s:%s:%s <--' % (self.ipaddr, str(self.ipport), str(self.slave_id))
            for c in resp:
                s += '%02X' % (ord(c))
            self.trace_func(s)

        if except_code:
            raise ModbusClientException('Modbus exception: %d' % (except_code))

    def write(self, addr, data):

        write_count = 0
        write_offset = 0
        local_connect = False
        count = len(data)/2

        if self.socket is None:
            local_connect = True
            self.connect(self.timeout)

        try:
            while (count > 0):
                if count > self.max_count:
                    write_count = self.max_count
                else:
                    write_count = count
                self._write(addr + write_offset, data[(write_offset * 2):((write_offset + write_count) * 2)])
                count -= write_count
                write_offset += write_count
        finally:
            if local_connect:
                self.disconnect()

class ModbusClientDeviceMapped(object):

    def __init__(self, slave_id, name, pathlist=None, max_count=None, ctx=None):

        self.slave_id = slave_id
        self.name = name
        self.ctx = ctx
        self.modbus_map = None

        if name is not None:
            self.modbus_map = mbmap.ModbusMap(slave_id)
            self.modbus_map.from_xml(name, pathlist)
        else:
            raise mbmap.ModbusMapError('No modbus map file provided during initialization')

    def close(self):

        pass

    def read(self, addr, count, op=None):

        if self.modbus_map is not None:
            return self.modbus_map.read(addr, count, op)
        else:
            raise ModbusClientError('No modbus map set for device')

    def write(self, addr, data):

        if self.modbus_map is not None:
            return self.modbus_map.write(addr, data)
        else:
            raise ModbusClientError('No modbus map set for device')

def __generate_crc16_table():
    ''' Generates a crc16 lookup table

    .. note:: This will only be generated once
    '''
    result = []
    for byte in range(256):
        crc = 0x0000
        for bit in range(8):
            if (byte ^ crc) & 0x0001:
                crc = (crc >> 1) ^ 0xa001
            else: crc >>= 1
            byte >>= 1
        result.append(crc)
    return result

__crc16_table = __generate_crc16_table()

def computeCRC(data):
    ''' Computes a crc16 on the passed in string. For modbus,
    this is only used on the binary serial protocols (in this
    case RTU).

    The difference between modbus's crc16 and a normal crc16
    is that modbus starts the crc value out at 0xffff.

    :param data: The data to create a crc16 of
    :returns: The calculated CRC
    '''
    crc = 0xffff
    for a in data:
        idx = __crc16_table[(crc ^ ord(a)) & 0xff];
        crc = ((crc >> 8) & 0xff) ^ idx
    swapped = ((crc << 8) & 0xff00) | ((crc >> 8) & 0x00ff)
    return swapped

def checkCRC(data, check):
    ''' Checks if the data matches the passed in CRC

    :param data: The data to create a crc16 of
    :param check: The CRC to validate
    :returns: True if matched, False otherwise
    '''
    return computeCRC(data) == check

