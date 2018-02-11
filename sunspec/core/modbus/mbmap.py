
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

import struct
import sys

try:
    import xml.etree.ElementTree as ET
except:
    import elementtree.ElementTree as ET

# Python 3 compatibility for long()
if sys.version_info > (3,):
    long = int

MBMAP_ROOT = 'mbmap'
MBMAP_ADDR = 'addr'
MBMAP_FUNC = 'func'
MBMAP_FUNC_INPUT = 'input'
MBMAP_FUNC_HOLDING = 'holding'
MBMAP_NS = 'ns'
MBMAP_LID = 'lid'
MBMAP_MAPID = 'mapid'
MBMAP_TIME = 'time'
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
    """
    Parameters:

        slave_id :
            Modbus slave id.

        func :
            Modbus function string associated with the map. Valid values are:
                :const:`sunspec.core.modbus.mbmap.MBMAP_FUNC_HOLDING` or
                :const:`sunspec.core.modbus.mbmap.MBMAP_FUNC_INPUT`.

        base_addr :
            Base address of the Modbus map.

    Raises:

        ModbusMapError: Raised for any modbus map error.

    Attributes:

        slave_id
            Modbus slave id.

        func
            Actual Modbus function associated with the map.

        base_addr
            Base address of the Modbus map.

        regs
            List of :const:`sunspec.core.modbus.mbmap.ModbusMapRegs` blocks that
            comprise the Modbus register map.
    """

    def __init__(self, slave_id=None, func=MBMAP_FUNC_HOLDING, base_addr=MBMAP_BASE_ADDR_DEFAULT, ns=None, lid=None,
                 mapid=None, time=None):

        self.slave_id = slave_id
        self.base_addr = base_addr
        self.ns = ns
        self.lid = lid
        self.mapid = mapid
        self.time = time
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
                        # print(offset, data_list)
                        for b in data_list:
                            c = struct.pack('B', int(b, 16))
                            if data is None:
                                data = c
                            else:
                                data += c

            mmr = ModbusMapRegs(offset, len(data)/2, data, MBMAP_REGS_ACCESS_RW)
            self.regs.append(mmr)
            f.close()
        except Exception as e:
            try:
                f.close()
            except:
                pass
            raise ModbusMapError('Error loading map file: %s' % str(e))

    def from_xml(self, filename=None, pathlist=None, element=None):
        """Load Modbus map from a Modbus map (mbmap) formatted file.

        Parameters:

            filename :
                File name of the Modbus map file

            pathlist :
                Pathlist object containing alternate paths to the Modbus map
                file.
        """

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
            self.ns = root.attrib.get(MBMAP_NS)
            self.lid = root.attrib.get(MBMAP_LID)
            self.mapid = root.attrib.get(MBMAP_MAPID)
            self.time = root.attrib.get(MBMAP_TIME)

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

                    # Python 3 compatibility for byte strings
                    if sys.version_info > (3,):
                        text = bytes(text, 'latin-1')

                    data = struct.pack(str(rlen * 2) + 's', text)
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

        except Exception as e:
            raise ModbusMapError('Error loading %s (%s) at offset %d - %s' % (filename, pathlist, offset, str(e)))

    def to_xml(self, parent=None, no_data=False):

        attr = {}
        attr[MBMAP_ADDR] = str(self.base_addr)
        attr[MBMAP_FUNC] =  func_name.get(self.func, MBMAP_FUNC_HOLDING)
        if self.ns is not None:
            attr[MBMAP_NS] = str(self.ns)
        if self.lid is not None:
            attr[MBMAP_LID] = str(self.lid)
        if self.mapid is not None:
            attr[MBMAP_MAPID] = str(self.mapid)
        if self.time is not None:
            attr[MBMAP_TIME] = str(self.time)

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
        """Read Modbus map registers.

        Parameters:

            addr :
                Starting Modbus address.

            count :
                Read length in Modbus registers.

        Returns:

            Byte string containing register contents.
        """

        data = b''
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
            print(self)
            raise ModbusMapError('Data read error - addr = %d  data len = %d  count = %d' % (addr, len(data), count))

        return data

    def write(self, addr, data):
        """Write Modbus map registers.

        Parameters:

            addr :
                Starting Modbus address.

            count :
                Byte string containing register contents.
        """

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
                    start = data_offset
                    end = int(data_offset + (write_count * 2))
                    regs.write(offset, data[start:end])
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
        """ Determines if the specified modbus map instance is not equal based
        on the content of the map.  If not equal, returns a string indicating
        why the map is not equal. Returns False if the map is equal.
        """

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
    """
    Parameters:

        offset :
            Register offset into Modbus map.

        count :
            Register count.

        data :
            Byte string containing register data.

        access:
            Access for the register block. Valid values are:
                :const:`sunspec.core.modbus.mbmap.MBMAP_REGS_ACCESS_R` and
                :const:`sunspec.core.modbus.mbmap.MBMAP_REGS_ACCESS_RW`.

    Raises:

        :exception ModbusMapError: Raised for any modbus map error.

    Attributes:

        offset
            Start register offset of the register block.

        count
            Register count in the block.

        data
            Byte string containing data in the register block.

        access
            Access setting for the block. The access setting is currently not
            enforced.
    """

    def __init__(self, offset, count, data, access=MBMAP_REGS_ACCESS_R):
        self.offset = offset
        self.count = count
        self.data = data
        self.access = access

    def read(self, offset, count):
        """Read Modbus map registers in register block.

        Parameters:

            offset :
                Register offset into Modbus map.

            count :
                Register count.

        Returns:
            Byte string containing register contents.
        """

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
        """Write Modbus map registers tp register block.

        Parameters:

            addr :
                Register offset into Modbus map.

            count :
                Byte string containing register contents.
        """
        count = len(data)/2
        if (offset >= self.offset) and (offset + count <= self.offset + self.count):
            start = (offset - self.offset) * 2
            end = int(start + (count * 2))
            self.data = self.data[:start] + data + self.data[end:]
        else:
           raise ModbusMapError('Data write error')

    def append(self, offset, count, data, access=MBMAP_REGS_ACCESS_R):
        """Append registers to end of register block.

        Parameters:

            offset :
                Register offset into Modbus map.

            count :
                Register count.

            data :
                Byte string containing register data.

            access :
                Access for the register block. Valid values are:
                    :const:`sunspec.core.modbus.mbmap.MBMAP_REGS_ACCESS_R` and
                    :const:`sunspec.core.modbus.mbmap.MBMAP_REGS_ACCESS_RW`.
        """

        self.data += data
        self.count += count

    def not_equal(self, regs):
        """ Determines if the specified modbus map block instance is not equal
        based on the content of the map block.  If not equal, returns a string
        indicating why the map block is not equal. Returns False if the map
        block is equal.
        """

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


