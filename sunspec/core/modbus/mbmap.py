
"""
  Copyright (c) 2014, SunSpec Alliance
  All Rights Reserved

"""

import struct

try:
    import xml.etree.ElementTree as ET
except:
    import elementtree.ElementTree as ET

MBMAP_ROOT = 'mbmap'
MBMAP_ADDR = 'addr'
MBMAP_FUNC = 'func'
MBMAP_FUNC_INPUT = 'input'
MBMAP_FUNC_HOLDING = 'holding'
MBMAP_REGS = 'regs'
MBMAP_REGS_OFFSET = 'offset'
MBMAP_REGS_LEN = 'len'
MBMAP_REGS_TYPE = 'type'
MBMAP_REGS_ACCESS = 'access'
MBMAP_REGS_FILL = 'fill'
MBMAP_REGS_ACCESS_R = 'r'
MBMAP_REGS_ACCESS_RW = 'rw'
MBMAP_REGS_TYPE_S16 = 's16'
MBMAP_REGS_TYPE_U16 = 'u16'
MBMAP_REGS_TYPE_S32 = 's32'
MBMAP_REGS_TYPE_U32 = 'u32'
MBMAP_REGS_TYPE_S64 = 's64'
MBMAP_REGS_TYPE_U64 = 'u64'
MBMAP_REGS_TYPE_F32 = 'f32'
MBMAP_REGS_TYPE_F64 = 'f64'
MBMAP_REGS_TYPE_STRING = 'string'
MBMAP_REGS_TYPE_HEX_STRING = 'hexstr'

MBMAP_BASE_ADDR_DEFAULT = 40000

func_value = {MBMAP_FUNC_INPUT: 4, MBMAP_FUNC_HOLDING: 3}
func_name = {4: MBMAP_FUNC_INPUT, 3: MBMAP_FUNC_HOLDING}

class ModbusMapError(Exception):
    pass

class ModbusMap(object):

    def __init__(self, slave_id=None, func=MBMAP_FUNC_HOLDING, base_addr=MBMAP_BASE_ADDR_DEFAULT):

        self.slave_id = slave_id
        self.base_addr = base_addr
        self.regs = []

        value = func_value.get(func)
        if value is None:
            raise ModbusMapError('Unsupported function: %s' % (func))
        self.func = value


    def from_hex(self, name, pathlist=None):

        data = None
        offset = 0
        try:
            f = open(name, 'r')
            for line in f:
                if line[0] != '#':
                    data_list = line.rstrip('\r\n').split()
                    data_len = len(data_list)/2
                    if data_len > 0:
                        # print offset, data_list
                        for b in data_list:
                            c = struct.pack('B', int(b, 16))
                            if data is None:
                                data = c
                            else:
                                data += c

            mmr = ModbusMapRegs(offset, len(data)/2, data, MBMAP_REGS_ACCESS_RW)
            self.regs.append(mmr)
            f.close()
        except Exception, e:
            try:
                f.close()
            except:
                pass
            raise ModbusMapError('Error loading map file: %s' % str(e))

    def from_xml(self, filename=None, pathlist=None, element=None):

        offset = 0
        next_offset = offset

        try:
            if filename is not None:
                if pathlist is not None:
                    map_data = pathlist.read(filename)
                else:
                    f = open(filename, 'r')
                    map_data = f.read()
                    f.close()

                root = ET.fromstring(map_data)
            elif element is not None:
                root = element
            else:
                raise ModbusMapError('Root element not provided')

            func = root.attrib.get(MBMAP_FUNC, MBMAP_FUNC_HOLDING)
            value = func_value.get(func)
            if value is None:
                raise ModbusMapError('Unsupported function: %s' % (func))
            self.func = value
            self.base_addr = root.attrib.get(MBMAP_ADDR, 40000)

            for r in root.findall(MBMAP_REGS):
                offset = r.attrib.get(MBMAP_REGS_OFFSET)
                if offset is None:
                    offset = next_offset
                else:
                    offset = int(offset)
                rlen = int(r.attrib.get(MBMAP_REGS_LEN, 0))
                rtype = r.attrib.get(MBMAP_REGS_TYPE, MBMAP_REGS_TYPE_HEX_STRING)
                access = r.attrib.get(MBMAP_REGS_ACCESS, MBMAP_REGS_ACCESS_R)
                fill = r.attrib.get(MBMAP_REGS_FILL, '\0')
                text = r.text

                if len(self.regs) > 0:
                    last_regs = self.regs[-1]
                    last_regs_next = last_regs.offset + last_regs.count
                else:
                    last_regs = None
                    last_regs_next = 0

                if offset < last_regs_next:
                    raise ModbusMapError('Register offsets must be in ascending order with no overlap %d  %d' % (offset, last_regs_next))

                data = None

                if not text:
                    if rtype ==  MBMAP_REGS_TYPE_STRING or rtype == MBMAP_REGS_TYPE_HEX_STRING:
                        text = ''
                    else:
                        text = '0'

                if rtype == MBMAP_REGS_TYPE_S16:
                    data = struct.pack('>h', int(text, 0))
                    rlen = 1
                elif rtype == MBMAP_REGS_TYPE_U16:
                    data = struct.pack('>H', int(text, 0))
                    rlen = 1
                elif rtype == MBMAP_REGS_TYPE_S32:
                    data = struct.pack('>l', int(text, 0))
                    rlen = 2
                elif rtype == MBMAP_REGS_TYPE_U32:
                    data = struct.pack('>L', long(text, 0))
                    rlen = 2
                elif rtype == MBMAP_REGS_TYPE_S64:
                    data = struct.pack('>q', long(text, 0))
                    rlen = 4
                elif rtype == MBMAP_REGS_TYPE_U64:
                    data = struct.pack('>Q', long(text, 0))
                    rlen = 4
                elif rtype == MBMAP_REGS_TYPE_F32:
                    data = struct.pack('>f', float(text))
                    rlen = 2
                elif rtype == MBMAP_REGS_TYPE_F64:
                    data = struct.pack('>d', float(text))
                    rlen = 4
                elif rtype == MBMAP_REGS_TYPE_STRING:
                    if rlen == 0:
                        rlen = (len(text) + 3)/4
                    data = struct.pack(str(rlen * 2) + 's', str(text))
                elif rtype == MBMAP_REGS_TYPE_HEX_STRING:
                    if text:
                        # remove any spaces
                        text = text.replace(' ','')
                    text_len = len(text)
                    if text_len % 4 != 0:
                        raise ModbusMapError('Hex string content length must be a multiple of 4 bytes')
                    if rlen == 0:
                        rlen = text_len/4
                    text_index = 0
                    while text_index < text_len:
                        c = struct.pack('B', int(text[text_index:text_index + 2], 16))
                        text_index += 2
                        if data is None:
                            data = c
                        else:
                            data += c
                    # fill remainder of string with nulls
                    regs_len = rlen * 2
                    if regs_len > text_len:
                        if data is None:
                            data = ''
                        data += struct.pack(str(regs_len - text_len) + 's', '')
                else:
                    raise ModbusMapError('Unknown type at offset %d' % (offset))

                next_offset = offset + rlen

                # if not contiguous, create a new register block
                if last_regs is None or offset > last_regs_next:
                    mmr = ModbusMapRegs(offset, rlen, data, access)
                    self.regs.append(mmr)
                # append to last register block
                else:
                    last_regs.append(offset, rlen, data, access)

        except Exception, e:
            raise ModbusMapError('Error loading %s (%s) at offset %d - %s' % (filename, pathlist, offset, str(e)))

    def to_xml(self, parent=None, no_data=False):

        attr = {}
        attr[MBMAP_ADDR] = str(self.base_addr)
        attr[MBMAP_FUNC] =  func_name.get(self.func, MBMAP_FUNC_HOLDING)
 
        if parent is None:
            element = ET.Element(MBMAP_ROOT, attrib=attr)
        else:
            element = ET.SubElement(parent, MBMAP_ROOT, attrib=attr)

        for regs in self.regs:
            e = ET.SubElement(element, MBMAP_REGS, attrib={MBMAP_REGS_OFFSET: str(regs.offset), MBMAP_REGS_LEN: str(regs.count)})

            if no_data is False:
                s = ''
                for d in regs.data:
                    s += '%02x' % ord(d)
                e.text = s

        return element

    def regs_add(self, addr=None, offset=None, count=1, access=MBMAP_REGS_ACCESS_RW):

        if addr is not None:
            if addr < self.base_addr:
                raise ModbusMapError('Address out of range')
            offset = addr - self.base_addr

        if len(self.regs) > 0:
            last_regs = self.regs[-1]
            last_regs_next = last_regs.offset + last_regs.count
        else:
            last_regs = None
            last_regs_next = 0

        if offset < last_regs_next:
            raise ModbusMapError('Register offsets must be in ascending order with no overlap %d  %d' % (offset, last_regs_next))

        data = struct.pack(str(count * 2) + 's', '')

        if last_regs is None or offset > last_regs_next:
            mmr = ModbusMapRegs(offset, count, data, access)
            self.regs.append(mmr)
        # append to last register block
        else:
            mmr = last_regs
            last_regs.append(offset, count, data, access)

        return mmr

    def read(self, addr, count, op=None):

        data = ''
        count_remaining = count

        if op and op != self.func:
            raise ModbusMapError('Data read error - function mismatch: request func = %s map func = %s' % (str(op), str(self.func)))

        offset = addr - int(self.base_addr)
        for regs in self.regs:
            if count_remaining > 0:
                regs_end_offset = regs.offset + regs.count
                if offset >= regs.offset and offset < regs_end_offset:
                    read_count = regs_end_offset - offset
                    if count_remaining < read_count:
                        read_count = count_remaining
                    data += regs.read(offset, read_count)
                    offset += read_count
                    count_remaining -= read_count
                else:
                    continue
            else:
                break

        # must have all requested data for success
        if len(data) != int(count) * 2:
            print self
            raise ModbusMapError('Data read error - addr = %d  data len = %d  count = %d' % (addr, len(data), count))

        return data
    
    def write(self, addr, data):

        data_len = len(data)
        count_remaining = data_len/2

        if data_len % 2 != 0:
            raise ModbusMapError('Data length not even number of bytes - addr: %d  data len: %d' % (addr, data_len))

        data_offset = 0
        offset = addr - int(self.base_addr)
        for regs in self.regs:
            if count_remaining > 0:
                regs_end_offset = regs.offset + regs.count
                if offset >= regs.offset and offset < regs_end_offset:
                    write_count = regs_end_offset - offset
                    if count_remaining < write_count:
                        write_count = count_remaining
                    # regs
                    # data += regs.read(offset, read_count)
                    regs.write(offset, data[data_offset:data_offset+(write_count * 2)])
                    offset += write_count
                    data_offset += write_count
                    count_remaining -= write_count
                else:
                    continue
            else:
                break

        # must have written all data for success
        if count_remaining > 0:
           raise ModbusMapError('Data write error')

    def not_equal(self, mbmap):

        if self.base_addr != mbmap.base_addr:
            return ('Base address mismatch: %s %s' % (str(self.base_addr), str(mbmap.base_addr)))
        if self.func != mbmap.func:
            return ('Function mismatch: %s %s' % (self.func, mbmap.func))

        if len(self.regs) != len(mbmap.regs):
            return ('Register group count mismatch')

        for i in range(len(self.regs)):
            not_equal = self.regs[i].not_equal(mbmap.regs[i])
            if not_equal:
                return not_equal
        return False

    def __str__(self):
        s = 'modbus_map: slave id = %s func = %s base_addr = %s' % (self.slave_id, self.func, self.base_addr)
        for regs in self.regs:
            s += '\n' + str(regs)
        return s

class ModbusMapRegs(object):

    def __init__(self, offset, count, data, access=MBMAP_REGS_ACCESS_R):
        self.offset = offset
        self.count = count
        self.data = data
        self.access = access

    def read(self, offset, count):
        regs_end_offset = self.offset + self.count
        end_offset = offset + count
        read_count = count
        if offset >= self.offset and offset < regs_end_offset:
            if offset < regs_end_offset and end_offset > regs_end_offset:
                read_count = regs_end_offset - offset
            if read_count > 0:
                start = (offset - self.offset) * 2
                end = start + (read_count * 2)
                return self.data[start:end]
        else:
            raise ModbusMapError('Data read error')

    def write(self, offset, data):
        count = len(data)/2
        if (offset >= self.offset) and (offset + count <= self.offset + self.count):
            start = (offset - self.offset) * 2
            end = start + (count * 2)
            self.data = self.data[:start] + data + self.data[end:]
        else:
           raise ModbusMapError('Data write error')

    def append(self, offset, count, data, access=MBMAP_REGS_ACCESS_R):
        self.data += data
        self.count += count

    def not_equal(self, regs):

        if self.offset != regs.offset:
            return ('Offset mismatch: %d %d' % (self.offset, regs.offset))
        if self.count != regs.count:
            return ('Count mismatch for offset %d: %d %d' % (self.offset, self.count, regs.count))
        if self.data != regs.data:
            for i in range(len(self.data)):
                if self.data[i] != regs.data[i]:
                    return ('Data mismatch at offset %d' % (self.offset + (i/2)))
        if self.access != regs.access:
            return ('Access mismatch for offset %d' % (self.offset))
        return False

    def __str__(self):
        s = '  offset = %s count = %s access = %s' % (str(self.offset), str(self.count), str(self.access))
        return s


