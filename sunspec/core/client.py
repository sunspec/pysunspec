
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

import os
import time
import struct
import sys
import sunspec.core.modbus.client as modbus
import sunspec.core.device as device
import sunspec.core.util as util
import sunspec.core.suns as suns
from sunspec.core.util import SunSpecError

RTU = 'RTU'
TCP = 'TCP'
MAPPED = 'Mapped'

PARITY_NONE = modbus.PARITY_NONE
PARITY_EVEN = modbus.PARITY_EVEN

class SunSpecClientError(SunSpecError):
    pass

class ClientDevice(device.Device):

    """ClientDevice

    A derived class based on :const:`sunspec.core.device.Device`. It adds Modbus
    device access capability to the device base class.

    Parameters:

        device_type :
             Device type. Possible values: :const:`RTU`, :const:`TCP`,
             :const:`MAPPED`.

        slave_id :
            Modbus slave id.

        name :
            For :const:`RTU` devices, the name of the serial port such as 'com4'
            or '/dev/tty2'. For :const:`MAPPED` devices, the name of the modbus
            map file.

        pathlist :
            Pathlist object containing alternate paths to support files.

        baudrate :
            For :const:`RTU` devices, baud rate such as 9600 or 19200. Defaulted
            by modbus module to 9600.

        parity :
            For :const:`RTU` devices, parity. Possible values:
            :const:`PARITY_NONE`, :const:`PARITY_EVEN`
            Defaulted by modbus module to :const:`PARITY_NONE`.

        ipaddr :
            For :const:`TCP` devices, device IP address.

        ipport :
            For :const:`TCP` devices, device IP port. Defaulted by modbus module
            to 502.

        timeout :
            Modbus request timeout in seconds. Fractional seconds are permitted
            such as .5.

        trace :
            Enable low level trace.

    Raises:

        SunSpecClientError: Raised for any sunspec module error.

    Attributes:

        type
            Device type. Possible values: :const:`RTU`, :const:`TCP`,
            :const:`MAPPED`.

        name
            For :const:`RTU` devices, the name of the serial port such as 'com4'
            or '/dev/tty2'. For :const:`MAPPED` devices, the name of the modbus
            map file.

        pathlist
            Pathlist object containing alternate paths to support files.

        slave_id
            Modbus slave id.

        modbus_device
            Modbus device object. Object type is based on the device type.

        retry_count
            Request retry count. Currently not used.

        base_addr_list
            List of Modbus base addresses to try when scanning a device for the
            first time.
    """

    def __init__(self, device_type, slave_id=None, name=None, pathlist = None, baudrate=None, parity=None, ipaddr=None, ipport=None,
                 timeout=None, trace=False):
        device.Device.__init__(self, addr=None)

        self.type = device_type
        self.name = name
        self.pathlist = pathlist
        self.slave_id = slave_id
        self.modbus_device = None
        self.retry_count = 2
        self.base_addr_list = [40000, 0, 50000]

        try:
            if device_type == RTU:
                self.modbus_device = modbus.ModbusClientDeviceRTU(slave_id, name, baudrate, parity, timeout, self, trace)
            elif device_type == TCP:
                self.modbus_device = modbus.ModbusClientDeviceTCP(slave_id, ipaddr, ipport, timeout, self, trace)
            elif device_type == MAPPED:
                if name is not None:
                    self.modbus_device = modbus.ModbusClientDeviceMapped(slave_id, name, pathlist, self)
                else:
                    if self.modbus_device is not None:
                        self.modbus_device.close()
                    raise SunSpecClientError('Map file required for mapped device')
        except modbus.ModbusClientError as e:
            if self.modbus_device is not None:
                self.modbus_device.close()
            raise SunSpecClientError('Modbus error: %s' % str(e))

    def close(self):

        if self.modbus_device is not None:
            self.modbus_device.close()

    def read(self, addr, count):
        """Read Modbus device registers.

        Parameters:

            addr :
                Starting Modbus address.

            count :
                Register count.

        Returns:
            Byte string containing register contents.
        """

        try:
            if self.modbus_device is not None:
                return self.modbus_device.read(addr, count)
            else:
                raise SunSpecClientError('No modbus device set for SunSpec device')
        except modbus.ModbusClientError as e:
            raise SunSpecClientError('Modbus read error: %s' % str(e))

    def write(self, addr, data):
        """Write Modbus device registers.

        Parameters:

            addr :
                Starting Modbus address.

            count :
                Byte string containing register contents.
        """

        try:
            if self.modbus_device is not None:
                return self.modbus_device.write(addr, data)
            else:
                raise SunSpecClientError('No modbus device set for SunSpec device')
        except modbus.ModbusClientError as e:
            raise SunSpecClientError('Modbus write error: %s' % str(e))

    def read_points(self):
        """Read the points for all models in the device from the physical
        device.
        """

        for model in self.models_list:
            model.read_points()

    def scan(self, progress=None, delay=None):
        """Scan all the models of the physical device and create the
        corresponding model objects within the device object based on the
        SunSpec model definitions.
        """

        error = ''

        connect = False
        if self.modbus_device and type(self.modbus_device) == modbus.ModbusClientDeviceTCP:
            self.modbus_device.connect()
            connect = True

            if delay is not None:
                time.sleep(delay)

        if self.base_addr is None:
            for addr in self.base_addr_list:
                # print('trying base address %s' % (addr))
                try:
                    data = self.read(addr, 3)
                    if data[:4] == b'SunS':
                        self.base_addr = addr
                        # print('device base address = %d' % self.base_addr)
                        break
                    else:
                        error = 'Device responded - not SunSpec register map'
                except SunSpecClientError as e:
                    if not error:
                        error = str(e)

                if delay is not None:
                    time.sleep(delay)

        if self.base_addr is not None:
            # print('base address = %s' % (self.base_addr))
            model_id = util.data_to_u16(data[4:6])
            addr = self.base_addr + 2

            while model_id != suns.SUNS_END_MODEL_ID:
                # read model and model len separately due to some devices not supplying
                # count for the end model id
                data = self.read(addr + 1, 1)
                if data and len(data) == 2:
                    if progress is not None:
                        cont = progress('Scanning model %s' % (model_id))
                        if not cont:
                            raise SunSpecClientError('Device scan terminated')
                    model_len = util.data_to_u16(data)
                    # print('model_id = %s  model_len = %s' % (model_id, model_len))

                    # move address past model id and length
                    model = ClientModel(self, model_id, addr + 2, model_len)
                    # print('loading model %s at %d' % (model_id, addr + 2))
                    try:
                        model.load()
                    except Exception as e:
                        model.load_error = str(e)
                    self.add_model(model)

                    addr += model_len + 2
                    data = self.read(addr, 1)
                    if data and len(data) == 2:
                        model_id = util.data_to_u16(data)
                    else:
                        break
                else:
                    break

                if delay is not None:
                    time.sleep(delay)

        else:
            if not error:
                error = 'Unknown error'
            raise SunSpecClientError(error)

        if connect:
            self.modbus_device.disconnect()

class ClientModel(device.Model):
    """A derived class based on :const:`sunspec.core.device.Model`. It adds
    Modbus device access capability to the model base class.

    Parameters:

        dev :
            Device object associated with the model.

        mid :
            Model id.

        addr :
            Starting Modbus address of the model.

        mlen :
            Model length in Modbus registers.

        index :
            Model index.

    Raises:

        SunSpecClientError: Raised for any sunspec module error.
    """

    def __init__(self, dev=None, mid=None, addr=0, mlen=None, index=1):

        device.Model.__init__(self, device=dev, mid=mid, addr=addr, mlen=mlen, index=index)

    def load(self):
        """Create the block and point objects within the model object based on
        the corresponding SunSpec model definition.
        """

        device.Model.load(self, block_class=ClientBlock, point_class=ClientPoint)

    def read_points(self):
        """Read all points in the model from the physical device.
        """

        if self.model_type is not None:
            # read current model
            try:
                end_index = len(self.read_blocks)
                if end_index == 1:
                    data = self.device.read(self.addr, self.len)
                else:
                    data = b''
                    index = 0
                    while index < end_index:
                        addr = self.read_blocks[index]
                        index += 1
                        if index < end_index:
                            read_len = self.read_blocks[index] - addr
                        else:
                            read_len = self.addr + self.len - addr
                        data += self.device.read(addr, read_len)
                if data:
                    # print('data len = ', len(data))
                    data_len = len(data)/2
                    if data_len != self.len:
                        raise SunSpecClientError('Error reading model %s' % self.model_type)

                    #  for each repeating block
                    for block in self.blocks:
                        # scale factor points
                        for pname, point in block.points_sf.items():
                            offset = int(point.addr) - int(self.addr)
                            if point.point_type.data_to is not None:
                                byte_offset = offset * 2
                                # print(pname, point, offset, byte_offset, (byte_offset + (int(point.point_type.len) * 2)), point.point_type.len)
                                point.value_base = point.point_type.data_to(data[byte_offset:byte_offset + (int(point.point_type.len) * 2)])
                                if not point.point_type.is_impl(point.value_base):
                                    point.value_base = None
                            else:
                                raise SunSpecClientError('No data_to function set for %s : %s' % (pname, point.point_type))

                        # non-scale factor points
                        for pname, point in block.points.items():
                            offset = int(point.addr) - int(self.addr)
                            if point.point_type.data_to is not None:
                                byte_offset = offset * 2
                                # print(pname, point, offset, byte_offset, (byte_offset + (int(point.point_type.len) * 2)), point.point_type.len)
                                point.value_base = point.point_type.data_to(data[byte_offset:byte_offset + (int(point.point_type.len) * 2)])
                                if (type(point.value_base) == bytes and
                                        sys.version_info > (3,)):
                                    point.value_base = str(point.value_base, 'latin-1')
                                if point.point_type.is_impl(point.value_base):
                                    if point.sf_point is not None:
                                        point.value_sf = point.sf_point.value_base
                                else:
                                    point.value_base = None
                                    point.value_sf = None
                            else:
                                raise SunSpecClientError('No data_to function set for %s : %s' % (pname, point.point_type))

            except SunSpecError as e:
                raise SunSpecClientError(e)
            except modbus.ModbusClientError as e:
                raise SunSpecClientError('Modbus error: %s' % str(e))
            except:
                raise

    def write_points(self):
        """Write all points that have been modified since the last write
        operation to the physical device.
        """

        addr = None
        next_addr = None
        data = b''

        for block in self.blocks:
            for point in block.points_list:
                if point.dirty:
                    point_addr = int(point.addr)
                    point_len = int(point.point_type.len)
                    point_data = point.point_type.to_data(point.value_base, (point_len * 2))
                    if addr is None:
                        addr = point_addr
                        data = b''
                    else:
                        if point_addr != next_addr:
                            block.model.device.write(addr, data)
                            addr = point_addr
                            data = b''
                    next_addr = point_addr + point_len
                    data += point_data
                    point.dirty = False
            if addr is not None:
                block.model.device.write(addr, data)
                addr = None

class ClientBlock(device.Block):
    """A derived class based on :const:`sunspec.core.device.Block`. It adds
    Modbus device access capability to the block base class.

    Parameters:

        model :
            Model object associated with the block.

        addr :
            Starting Modbus address of the block.

        blen :
            Block length in Modbus registers.

        block_type :
            The block type object associated with block in the model
            definition.

        index :
            Block index.
    """

    def __init__(self, model, addr, blen, block_type, index=1):

        device.Block.__init__(self, model, addr, blen, block_type, index)

class ClientPoint(device.Point):
    """A derived class based on :const:`sunspec.core.device.Point`. It adds
    Modbus device access capability to the point base class.

    Parameters:

        block :
            Block object associated with the point.

        point_type :
            The point type object associated with point in the model definition.

        addr :
            Starting Modbus address of the point.

        sf_point :
            Point object associated with the point scale factor if present.

        value :
            Point value.

    Raises:

        SunSpecClientError: Raised for any sunspec module error.
    """

    def __init__(self, block=None, point_type=None, addr=None, sf_point=None, value=None):

        device.Point.__init__(self, block, point_type, addr, sf_point, value)

    def write(self):
        """Write the point to the physical device.
        """

        data = self.point_type.to_data(self.value_base, (int(self.point_type.len) * 2))
        self.block.model.device.write(int(self.addr), data)
        self.dirty = False

class SunSpecClientModelBase(object):

    """This class forms the base class of the dynamically generated model
    classes during SunSpecClientDevice initialization. In addition to the
    attributes listed below, the model (fixed block) points are placed as
    attributes on the model.

    Parameters:

        model :
            The :const:`sunspec.core.device.Model` associated with the model.

        name :
            Model name as specified in the model definition.

    Raises:

        SunSpecClientError : Raised for any sunspec module error.

    Attributes:

        model
            The :const:`sunspec.core.device.Model` object associated with the
            model.

        name
            Model name as specified in the model definition.

        repeating
            Repeating block if the model contains one.

        repeating_name
            Repeating block name.

        points
            Names of the point attributes added to the model object.
    """


    def __init__(self, model, name):
        self.model = model
        self.name = name
        self.repeating = [None]
        self.repeating_name = 'repeating'

        if len(model.blocks) > 1:
            block_class_name = self.__class__.__name__ + 'Repeating'
            for block in model.blocks[1:]:
                # set repeating block name and attribute if present
                if block.block_type.name != self.repeating_name:
                    self.repeating_name = block.block_type.name
                    setattr(self, self.repeating_name, self.repeating)
                # block_class_ = globals().get(block_class_name)
                block_class = globals().get(block_class_name)
                c = block_class(block, self.repeating_name)
                self.repeating.append(c)

    def _get_property(self, name):
        point = self.model.points.get(name)
        if point:
            return point.value

    def _set_property(self, name, value):
        point = self.model.points.get(name)
        if point:
            point.value = value

    def __getitem__(self, name):
        return self._get_property(name)
        # return self.__dict__.get(name, None)

    def __setitem__(self, name, item):
        return self._set_property(name, item)
        # self.__dict__.set(name, item)

    def read(self):
        """Read all points in the model from the physical device."""

        self.model.read_points()

    def write(self):
        """Write all points that have been modified since the last write
        operation to the physical device."""

        self.model.write_points()

    def __str__(self):
        s = '\n%s (%s):\n' % (self.name, self.model.id)
        for name in self.points:
            value = getattr(self, name)
            if value is not None:
                s += '%s:  %s\n' % (name, str(value))

        for block in self.repeating[1:]:
            s += str(block)

        return s

class SunSpecClientBlockBase(object):

    """SunSpecClientBlockBase

    This class forms the base class of the dynamically generated repeating
    block classes during SunSpecClientDevice initialization. In addition to
    the attributes listed below, the repeating block points are placed as
    attributes on the repeating block.

    Parameters:

        block :
             The :const:`sunspec.core.device.Block` object associated with the
             block.

        name :
             Repeating block name as specified in the model definition.

    Attributes:

        block
            The :const:`sunspec.core.device.Block` object associated with the
            block.

        name
            Block name as specified in the model definition.

        points
            Names of the point attributes added to the block object.
    """

    def __init__(self, block, name):
        self.block = block
        self.name = name

    def _get_property(self, name):
        point = self.block.points.get(name)
        if point:
            return point.value

    def _set_property(self, name, value):
        point = self.block.points.get(name)
        if point:
            point.value = value

    def __getitem__(self, name):
        return self._get_property(name)
        # return self.__dict__.get(name, None)

    def __setitem__(self, name, item):
        return self._set_property(name, item)
        # self.__dict__.set(name, item)

    def __str__(self):
        s = '\n%s[%d]:\n' % (self.name, self.block.index)
        for name in self.points:
            value = getattr(self, name)
            if value is not None:
                s += '%s:  %s\n' % (name, str(value))

        return s

def model_class_get(model_id):

    def add_property(self, name, value):
        fget = lambda self: self._get_property(name)
        fset = lambda self, value: self._set_property(name, value)
        setattr(self, name, property(fget, fset))

    def class_init(self, model, name):
        SunSpecClientModelBase.__init__(self, model, name)

    def block_class_init(self, block, name):
        SunSpecClientBlockBase.__init__(self, block, name)

    class_name = 'Model' + str(model_id)
    class_ = globals().get(class_name)
    if class_ is None:
        class_ = type(class_name, (SunSpecClientModelBase,), {'__init__' : class_init})
        globals()[class_name] = class_

    setattr(class_, 'points', [])
    model_type = None
    try:
        model_type = device.model_type_get(model_id)
    except Exception as e:
        setattr(class_, 'load_error', str(e))
    if model_type is not None:
        for point_type in model_type.fixed_block.points_list:
            if point_type.type != suns.SUNS_TYPE_SUNSSF and point_type.type != suns.SUNS_TYPE_PAD:
                add_property(class_, point_type.id, None)
                class_.points.append(point_type.id)
            ### check for writable point?

        block_type = model_type.repeating_block
        if block_type is not None:
            block_class_name = class_name + 'Repeating'
            block_class = type(block_class_name, (SunSpecClientBlockBase,), {'__init__' : block_class_init})
            globals()[block_class_name] = block_class

            setattr(block_class, 'points', [])
            for point_type in block_type.points_list:
                if point_type.type != suns.SUNS_TYPE_SUNSSF and point_type.type != suns.SUNS_TYPE_PAD:
                    add_property(block_class, point_type.id, None)
                    block_class.points.append(point_type.id)

    return class_

class SunSpecClientDevice(object):

    """This class wraps the sunspec.core.ClientDevice class to provide an
    alternate syntax for scripting. By placing the model (fixed block) points,
    and repeating block points directly on the model and repeating block objects
    as attributes, the syntax for accessing them is simplified.

    The model and block classes within the device are dynamically generated
    based on the model type with the appropriate attributes being added during
    creation.

    Parameters:

        device_type :
            Device type. Possible values: :const:`RTU`, :const:`TCP`,
            :const:`MAPPED`.

        slave_id :
            Modbus slave id

        name :
            For :const:`RTU` devices, the name of the serial port such as 'com4'
            or '/dev/ttyUSB0'. For :const:`MAPPED` devices, the name of the
            modbus map file.

        pathlist :
            Pathlist object containing alternate paths to support files.

        baudrate :
            For :const:`RTU` devices, baud rate such as 9600 or 19200. Defaulted
            by modbus module to 9600.

        parity :
            For :const:`RTU` devices, parity. Possible values:
            :const:`sunspec.core.client.PARITY_NONE`,
            :const:`sunspec.core.client.PARITY_EVEN` Defaulted by modbus module
            to :const:`PARITY_NONE`.

        ipaddr :
            For :const:`TCP` devices, device IP address.

        ipport :
            For :const:`TCP` devices, device IP port. Defaulted by modbus module
            to 502.

        timeout :
            Modbus request timeout in seconds. Fractional seconds are permitted
            such as .5.

        trace :
            Enable low level trace.

    Raises:

        SunSpecClientError: Raised for any sunspec module error.

    Attributes:

        device
            The :const:`sunspec.core.client.ClientDevice` associated with this
            object.

        models
            List of models present in the device in the order in which they
            appear in the device. If there is a single instance of the model in
            the device, the list element is a model object.

            If there are multiple instances of the same model in the list, the
            list element for that model is a list of the models of that type in
            the order in which they appear in the device with the first element
            having an index of 1.
    """

    def __init__(self, device_type, slave_id=None, name=None, pathlist = None, baudrate=None, parity=None, ipaddr=None, ipport=None,
                 timeout=None, trace=False, scan_progress=None, scan_delay=None):

        # super(self.__class__, self).__init__(device_type, slave_id, name, pathlist, baudrate, parity, ipaddr, ipport)
        self.device = ClientDevice(device_type, slave_id, name, pathlist, baudrate, parity, ipaddr, ipport, timeout, trace)
        self.models = []

        try:
            # scan device models
            self.device.scan(progress=scan_progress, delay=scan_delay)

            # create named attributes for each model
            for model in self.device.models_list:
                model_id = str(model.id)
                c = model_class_get(model_id)
                if model.model_type is not None:
                    name = model.model_type.name
                else:
                    name = 'model_' + model_id
                model_class = c(model, name)
                existing = getattr(self, name, None)
                # if model id already defined
                if existing:
                    # if model id definition is not a list, turn it into a list and add existing model
                    if type(self[name]) is not list:
                        # model instance index starts at 1 so first first list element is None
                        setattr(self, name, [None])
                        self[name].append(existing)
                    # add new model to the list
                    self[name].append(model_class)
                # if first model id instance, set attribute as model
                else:
                    setattr(self, name, model_class)
                    self.models.append(name)
        except Exception as e:
            if self.device is not None:
                self.device.close()
            raise

    def close(self):
        """Release resources associated with the device. Should be called when
        the device object is no longer in use.
        """

        self.device.close()

    def read(self):
        """Read the points for all models in the device from the physical
        device.
        """

        self.device.read_points()

    def __getitem__(self, key):
        return self.__dict__.get(key, None)

    def __setitem__(self, key, item):
        self.__dict__.set(key, item)

    def __str__(self):

        s = ''
        for model in self.models:
            s += str(self[model])

        return s

if __name__ == "__main__":

    pass
