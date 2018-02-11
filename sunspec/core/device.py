
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
import math

try:
    import xml.etree.ElementTree as ET
except:
    import elementtree.ElementTree as ET

import sunspec.core.pics as pics
import sunspec.core.smdx as smdx
import sunspec.core.suns as suns
from sunspec.core.util import SunSpecError

# file path list
file_pathlist = None

MAX_READ_COUNT = 125

class Device(object):
    """
    Parameters:

        addr :
            Modbus base address of device.

    Raises:
        SunSpecError: Any error encountered in device processing.


    Attributes:

        base_addr
            Modbus base address of the device.

        models_list
            List of model objects present in the device in the order in which
            they appear in the device.

        models
            Dictionary of model object lists reperesenting model types present
            in the device indexed by model id. The elements are model lists to
            allow more than one model of the same model type to be present in
            the device.
    """

    def __init__(self, addr=suns.SUNS_BASE_ADDR_DEFAULT):

        self.base_addr = addr
        self.models_list = []
        self.models = {}               # dict of model arrays to support more than one instance of a model

    def add_model(self, model):
        """Add a model object to the device.

        Parameters:

            model :
                Model object to add to the device.
        """

        models = self.models.get(model.id)
        if models is None:
            self.models[model.id] = []
            models = self.models.get(model.id)
        models.append(model)
        self.models_list.append(model)

    def from_pics(self, element=None, filename=None, pathlist=None):
        """The PICS information for the device can be either an Element Tree
        element for a device from a document already being processed or the file
        name of document in the file system. Populates the device based on the
        elements within the device element.

        Parameters:

            element :
                Element Tree device element.

            filename :
                File name of the PICS document.

            pathlist :
                Pathlist object containing alternate paths to the PICS document.
        """

        global file_pathlist

        pics_data = ''

        try:
            if element is None:
                # try supplied path list
                if pathlist is not None:
                    try:
                        pics_data = pathlist.read(filename)
                    except NameError:
                        pass

                # try device file path list
                if not pics_data and file_pathlist is not None:
                    try:
                        pics_data = file_pathlist.read(filename)
                    except NameError:
                        pass

                # try local directory
                if not pics_data:
                    f = open(filename, 'r')
                    pics_data = f.read()
                    f.close()

                root = ET.fromstring(pics_data)
                if root.tag != pics.PICS_ROOT:
                    raise SunSpecError("Unexpected root element: %s" % (root.tag))

                d = root.find(pics.PICS_DEVICE)
                if d is None:
                    raise SunSpecError("No '%s' elements found in '%s' element" % (pics.PICS_DEVICE, root.tag))
            else:
                d = element
            if d.tag != pics.PICS_DEVICE:
                raise SunSpecError("Unexpected device tag: '%s'" % (d.tag))
            self.base_addr = d.attrib.get(pics.PICS_ATTR_BASE_ADDR, pics.PICS_BASE_ADDR_DEFAULT)
            addr = self.base_addr + 2

            for m in d.findall('*'):
                if m is None:
                    raise SunSpecError("No '%s' elements found in '%s' element" % (pics.PICS_MODEL, d.tag))
                if m.tag != pics.PICS_MODEL:
                    raise SunSpecError("Unexpected '%s' element in '%s' element" % (m.tag, d.tag))

                model_id = m.attrib.get(pics.PICS_ATTR_ID)
                if model_id is None:
                    raise SunSpecError('Module id error')
                model_len = m.attrib.get(pics.PICS_ATTR_LEN)
                if model_len is not None:
                    # raise SunSpecError('Module len error in model %d' % (model_id))
                    model_len = int(model_len)

                # move address past model id and length (even though address is not real in the case)
                model = Model(self, model_id, addr + 2, model_len)
                try:
                    model.load()
                except Exception as e:
                    model.load_error = str(e)
                model.from_pics(m)
                self.add_model(model)

                addr += model.len + 2

        except Exception as e:
            raise SunSpecError('Error loading PICS: %s' % str(e))

    """
    def to_pics(self, pretty_print=False, single_repeating=True):

        attr = {pics.PICS_ATTR_VERSION: str(pics.PICS_VERSION)}

        root = ET.Element(pics.PICS_ROOT)
        e = ET.SubElement(root, pics.PICS_DEVICE, attrib=attr)

        for model in self.models_list:
            model.to_pics(e, single_repeating=single_repeating)

        if pretty_print:
            util.indent(root)

        return ET.tostring(root)
    """

    def to_pics(self, parent, single_repeating=True):
        """Adds the device and all elements within the device to the parent
        element. If *single_repeating* is True, only the first repeating block
        for each model is added to the document.

        Parameters:

            parent :
                Element Tree element on which to place the device element.

            single_repeating :
                Flag to indicate whether to include a single or all repeating
                blocks within each model in the PICS document.
        """

        attr = {pics.PICS_ATTR_VERSION: str(pics.PICS_VERSION)}

        e = ET.SubElement(parent, pics.PICS_DEVICE, attrib=attr)

        for model in self.models_list:
            model.to_pics(e, single_repeating=single_repeating)

    def not_equal(self, device):
        """Determines if the specified device instance is not equal based on all
        the device attribute values including models, blocks and points.  If not
        equal, returns a string indicating why the device is not equal. Returns
        False if the device is equal.

        Parameters:

            device :
                Device to compare.
        """

        if len(self.models_list) != len(device.models_list):
            return 'Devices not equal - model counts: %d  %d' % (len(self.models_list), len(device.models_list))
        for i in range(len(self.models_list)):
            s = self.models_list[i].not_equal(device.models_list[i])
            if s:
                return 'Devices not equal - %s' % (s)
        return False

    def __str__(self):

        device_str = ''
        for model in self.models_list:
            device_str += str(model)
        return device_str

class Block(object):
    """
    Parameters:

        model :
            Model associated with the block.

        addr :
            Modbus address of the first point in the block.

        blen :
            Length of the block in Modbus registers.

        block_type :
            The :const:`sunspec.core.device.BlockType` instance associated with
            the block.

        index :
            Block instance index for the block type within the model.

    Attributes:

        model
            Model associated with the block.

        block_type
            The :const:`sunspec.core.device.BlockType` instance associated with
            the block.

        addr
            Modbus address of the first point in the block.

        len
            Length of the block in Modbus registers.

        type
            Block type, either :const:`sunspec.core.suns.SUNS_BLOCK_FIXED` or
            :const:`sunspec.core.suns.SUNS_BLOCK_REPEATING`.

        index
            Block instance index for the block type within the model.

        points_list
            List of non-scale factor points in the block ordered by offset.

        points
            Dictionary of non-scale factor points in the block indexed by point
            id.

        points_sf
            Dictionary of scale factor points int the block indexed by point id.
    """

    def __init__(self, model, addr, blen, block_type, index=1):

        self.model = model
        self.block_type = block_type
        self.addr = addr
        self.len = blen
        self.type = block_type.type
        self.index = index
        self.points_list = []
        self.points = {}
        self.points_sf = {}

    def from_pics(self, element):
        """Sets the block contents based on an element tree model type element
        contained in a SunSpec PICS document.

        Parameters:

            element :
                Element Tree model element.
        """

        for p in element.findall('*'):
            if p.tag != pics.PICS_POINT:
                raise SunSpecError("Unexpected '%s' element in '%s' element" % (p.tag, element.tag))
            pid = p.attrib.get(pics.PICS_ATTR_ID)
            point = self.points.get(pid)
            if point is None:
                point = self.points_sf.get(pid)
            if point is not None:
                point.from_pics(p)

        # resolve scale factor values in points, must be done after all points in block are read
        for point in self.points_list:
            if point.sf_point is not None:
                point.value_sf = point.sf_point.value_base

    def to_pics(self, parent):
        """Adds the block and all elements within the block to the parent
        element.

        Parameters:

            parent :
                Element Tree element on which to place the block element.
        """

        attr = {}

        if self.index > 1:
            attr[pics.PICS_ATTR_INDEX] = str(self.index)

        if self.block_type.type == suns.SUNS_BLOCK_REPEATING:
            attr[pics.PICS_ATTR_TYPE] = pics.PICS_TYPE_REPEATING

        e = ET.SubElement(parent, pics.PICS_BLOCK, attrib=attr)

        # use block type points list to preserve original order of points in the block
        for pt in self.block_type.points_list:
            point = self.points.get(pt.id)
            if point is None:
                point = self.points_sf.get(pt.id)
            if point is not None:
                point.to_pics(e)

    def not_equal(self, block):
        """Determines if the specified block instance is not equal based on all
        the block attribute values including points.  If not equal, returns a
        string indicating why the block is not equal. Returns False if the block
        is equal.

        Parameters:

            device :
                Block to compare.
        """

        s = self.block_type.not_equal(block.block_type)
        if s:
            return 'block %s not equal - block type not equal: %s' % (self.block_type.type, s)

        for point in self.points_list:
            s = point.not_equal(block.points.get(point.point_type.id))
            if s:
                return 'block %d not equal - %s' % (self.index, s)
        return False

    def __str__(self):

        block_str = 'Block: type: %s index: %d:\n' % (self.type, self.index)
        for point in self.points_list:
            block_str += '  ' + str(point) + '\n'
        return block_str

class Point(object):
    """
    Parameters:

        block :
            Block associated with the point.

        point_type :
            The :const:`sunspec.core.device.PointType` instance associated with
            the point.

        addr :
            The Modbus address of the point.

        sf_point :
            Scale factor point associated with the point if present.

        value :
            Initial value for the *value_base* attribute of the point.

    Attributes:

        block
            Block associated with the point.

        point_type
            The :const:`sunspec.core.device.PointType` instance associated with
            the point.

        addr
            Modbus address of the point.

        sf_point
            Scale factor point associated with the point if present.

        impl
            Indication if the point is implemented. A value of True indicates
            the point is implmented. Intended to be used for cases when no
            initial value is given for the point but the implementation status
            is known as in SunSpec PICS documents.

        value_base
            Value of the point without the point scale factor applied.

        value_sf
            Scale factor point value.

        dirty
            Indication if the point has been written to the physical device
            since the last update of the point. A value of True indicates that
            the point has not been written since the last update.

        value
            Value of the point with the scale factor applied.
    """

    def __init__(self, block=None, point_type=None, addr=None, sf_point=None, value=None):

        self.block = block
        self.point_type = point_type
        self.addr = addr
        self.sf_point = sf_point
        self.impl = True
        self.value_base = value
        self.value_sf = None
        self.dirty = False

    """
    @property
    def value(self):
        if self.value_sf:
            return self.value_base * math.pow(10, self.value_sf)
        else:
            return self.value_base

    @value.setter
    def value(self, v):
        if self.value_sf:
            self.value_base = int(round(float(v), abs(self.value_sf)) / math.pow(10, self.value_sf))
        else:
            self.value_base = v
        self.dirty = True

    @property
    def value_str(self):
        if self.value_sf:
            pass
        else:
            return str(self.value_base)

    @value.setter
    def value_str(self, v):
        if self.value_sf:
            pass
        else:
            self.value_base = int(v)
    """

    # use older property format to support earlier python 2.x versions
    def value_getter(self):

        if self.value_sf:
            return self.value_base * math.pow(10, self.value_sf)
        else:
            return self.value_base

    def value_setter(self, v):

        if self.value_sf:
            self.value_base = int(round(float(v), abs(self.value_sf)) / math.pow(10, self.value_sf))
        else:
            self.value_base = self.point_type.to_value(v)

        self.dirty = True

    value = property(value_getter, value_setter, None)

    def from_pics(self, element):
        """Sets the block contents based on an element tree model type element
        contained in a SunSpec PICS document.

        Parameters:

            element :
                Element Tree model element.
        """

        impl = True
        impl_attr = element.attrib.get(pics.PICS_ATTR_IMPLEMENTED)
        if impl_attr:
            if impl_attr == pics.PICS_IMPLEMENTED_FALSE:
                impl = False

        value = None
        if impl:
            if element.text:
                value = self.point_type.to_value(element.text)
                self.impl = self.point_type.is_impl(value)
        else:
            self.impl = False

        if self.impl and value is not None:
            self.value_base = value

    def to_pics(self, parent):
        """Adds the point to the parent element.

        Parameters:

            parent :
                Element Tree element on which to place the point element.
        """

        attr = {pics.PICS_ATTR_ID: str(self.point_type.id)}

        if self.value is None:
            attr[pics.PICS_ATTR_IMPLEMENTED] = str(pics.PICS_IMPLEMENTED_FALSE)
        else:
            if self.point_type.access != suns.SUNS_ACCESS_R:
                access =  [key for key, value in pics.pics_access_types.items() if value == suns.SUNS_ACCESS_RW][0]
                attr[pics.PICS_ATTR_ACCESS] = str(access)

        e = ET.SubElement(parent, pics.PICS_POINT, attrib=attr)
        if self.value_base is not None:
            e.text = str(self.value_base).rstrip('\0')

    def not_equal(self, point):
        """ Determines if the specified point instance is not equal based on all
        the point attribute values.  If not equal, returns a string indicating
        why the point is not equal. Returns False if the point is equal.

        Parameters:

            device :
                Point to compare.
        """

        s = self.point_type.not_equal(point.point_type)
        if s:
            return 'point %s not equal - point type not equal: %s' % (self.point_type.id, s)

        if (((self.value_base is not None or point.value_base is not None) and (self.value_base != point.value_base)) or
            ((self.value_sf is not None or point.value_sf is not None) and (self.value_sf != point.value_sf))):
            if self.value_base is not None:
                print('self.value_base')
            if point.value_base is not None:
                print('point.value_base', type(point.value_base), point.value_base)
            return 'point %s not equal: %s %s - %s %s' % (self.point_type.id, self.value_base, self.value_sf, point.value_base, point.value_sf)
        return False

    def __str__(self):
        point_str = 'Point: id = %s impl= %s addr = %s value_base = %s' % (self.point_type.id, str(self.impl), self.addr, str(self.value_base))
        if self.sf_point is not None:
            point_str += ' sf_value = %s' % (str(self.sf_point.value_base))
        return point_str

class ScaleFactor(object):

    def __init__(self, value=None):

        self.value_base = value

class Model(object):
    """
    Parameters:

        device :
            Device associated with the model.

        mid :
            Model id.

        addr :
            Modbus address of the first point in the model.

        mlen :
            Length of the model in Modbus registers.

        index :
            Model instance index for the model type within the device.

    Raises:

        SunSpecError: Any error encountered in device processing.


    Attributes:

        device
            Device instance that contains the model instance.

        id
            Model id. The model id maps to a SunSpec model type definition.

        index
            Model instance index for the model type within the device. Model
            instance indexes start at 1 for the first model type instance.

        model_type
            The :const:`sunspec.core.device.ModelType` instance associated with
            the model.

        addr
            Modbus address of the first point in the model.

        len
            Length of the model in Modbus registers.

        points_list
            List of fixed block non-scale factor points ordered by offset.

        points
            Dictionary of fixed block non-scale factor points indexed by point
            id.

        points_sf
            Dictionary of fixed block scale factor points indexed by point id.

        blocks
            List of blocks contained in the model instance. Block 0 is the fixed
            block if present and blocks 1 to n are the repeating block
            instances.
    """

    def __init__(self, device=None, mid=None, addr=0, mlen=0, index=1):

        self.device = device
        self.id = int(mid)
        self.index = index
        self.model_type = None
        self.addr = addr               # modbus address of first point in the model
        self.len = int(mlen)           # register count of the point elements in the model
        self.points_list = []          # fixed block non-scale factor points list ordered by offset
        self.points = {}               # fixed block non-scale factor points
        self.points_sf = {}            # fixed block scale factor points
        self.blocks = []
        self.load_error = None
        self.read_blocks = []

    def load(self, block_class=Block, point_class=Point):
        """Loads the model instance with blocks and points based on the SunSpec
        model type definition.

        Parameters:

            block_class :
                Block class to use to create block instances.

            point_class :
                Point class to use to create point instances.
        """

        last_read_addr = self.addr
        self.read_blocks.append(last_read_addr)

        self.model_type = model_type_get(self.id)

        if self.model_type is not None:
            if self.len == 0:
                self.len = self.model_type.len
            end_addr = self.addr + self.len

            index = 0
            # model type always has a fixed block defined
            block_type = self.model_type.fixed_block
            block_addr = self.addr
            block_len = int(block_type.len)
            # adjustment for legacy common model len = 65
            if self.id == 1 and self.len == 65:
                block_len = self.len

            # while another block
            while end_addr >= block_addr + block_len:
                block = block_class(self, block_addr, block_len, block_type, index)
                self.blocks.append(block)

                for point_type in block_type.points_list:
                    if point_type.type != suns.SUNS_TYPE_PAD:
                        point_addr = int(block_addr) + int(point_type.offset)
                        point = point_class(block, point_type, str(point_addr))
                        if point_addr + point.point_type.len - last_read_addr > MAX_READ_COUNT:
                            last_read_addr = point_addr
                            self.read_blocks.append(last_read_addr)
                        if point_type.type == suns.SUNS_TYPE_SUNSSF:
                            block.points_sf[point_type.id] = point
                        else:
                            block.points_list.append(point)
                            block.points[point_type.id] = point

                # resolve scale factor addresses for repeating block
                for point in block.points_list:
                    if point.point_type.sf is not None and point.sf_point is None:
                        # check for constant scale factor
                        try:
                            sf_value = int(point.point_type.sf)
                            point.sf_point = ScaleFactor(sf_value)
                        except Exception:
                            pass
                        # try local repeating block first
                        if point.sf_point is None:
                            point.sf_point = block.points_sf.get(point.point_type.sf)
                        if point.sf_point is None:
                            # if repeating block, try fixed block
                            if index > 0:
                                point.sf_point = self.blocks[0].points_sf.get(point.point_type.sf)
                        if point.sf_point is None:
                            # ### what state should model be left in on exception
                            raise SunSpecError('Unable to resolve scale factor point %s for point %s in model %s' %
                                point.point_type.sf, point.point_type.pid, self.id)

                block_addr += block_len
                block_type = self.model_type.repeating_block
                if block_type is None:
                    ### check for extra registers?
                    break
                index += 1
                block_len = int(block_type.len)
        else:
            raise SunSpecError('Unknown model type - id: %s' % str(self.id))

        # expose fixed block points at model level if present
        try:
            self.points_list = self.blocks[0].points_list
            self.points = self.blocks[0].points
            self.points_sf = self.blocks[0].points_sf
        except IndexError:
            pass

    def from_pics(self, element):
        """ Sets the model contents based on an element tree model type element
        contained in a SunSpec PICS document.

        Parameters:

            element :
                Element Tree model element.
        """

        # update index if present
        self.index = element.attrib.get(pics.PICS_ATTR_INDEX, self.index)

        for b in element.findall('*'):
            if b.tag != pics.PICS_BLOCK:
                raise SunSpecError("Unexpected '%s' element in '%s' element" % (b.tag, element.tag))
            block_type = pics.pics_block_types.get(b.attrib.get(pics.PICS_ATTR_TYPE, pics.PICS_TYPE_FIXED))
            if block_type is None:
                raise SunSpecError('Unknown block type')
            if block_type == suns.SUNS_BLOCK_FIXED:
                if len(self.blocks) > 0:
                    self.blocks[0].from_pics(b)
            elif block_type == suns.SUNS_BLOCK_REPEATING:
                block_index = b.attrib.get(pics.PICS_ATTR_INDEX)
                # if no index specified, apply to all repeating blocks
                if block_index is None:
                    if len(self.blocks) > 1:
                        for block in self.blocks[1:]:
                            block.from_pics(b)
                else:
                    block_index = int(block_index)
                    if len(self.blocks) < block_index:
                        raise SunSpecError('Block index out of range: %s' % (str(block_index)))
                    self.blocks[block_index].from_pics(b)
            else:
                raise SunSpecError('Internal block type error')

    def to_pics(self, parent, single_repeating=True):
        """ Adds the model and all elements within the model to the parent
        element. If *single_repeating* is True, only the first repeating block
        is added to the document.

        Parameters:

            parent :
                Element Tree element on which to place the model element.

            single_repeating :
                Flag to indicate whether to include a single or all repeating
                blocks within the model in the PICS document.
        """

        attr = {pics.PICS_ATTR_ID: str(self.id), pics.PICS_ATTR_LEN: str(self.len)}

        if self.index != 1:
            attr[pics.PICS_ATTR_INDEX] = str(self.index)

        e = ET.SubElement(parent, pics.PICS_MODEL, attrib=attr)

        for block in self.blocks:
            if single_repeating == False or block.index <= 1:
                block.to_pics(e)

    def not_equal(self, model):
        """ Determines if the specified model instance is not equal based on all
        the model attribute values including blocks and points.  If not equal,
        returns a string indicating why the model is not equal. Returns False if
        the model is equal.

        Parameters:

            device :
                Model to compare.
        """

        if len(self.blocks) != len(model.blocks):
            return 'model %s not equal - block counts: %d  %d' % (self.model_type.id, len(self.blocks), len(model.blocks))
        s = self.model_type.not_equal(model.model_type)
        if s:
            return 'model %s not equal - model id not equal: %s' % (self.model_type.id, s)

        for i in range(len(self.blocks)):
            s = self.blocks[i].not_equal(model.blocks[i])
            if s:
                return 'model %s not equal - %s' % (self.model_type.id, s)
        return False

    def __str__(self):

        model_str = 'Model %s:\n' % self.id
        for point in self.points_list:
            model_str += '  ' + str(point) + '\n'
        for block in self.blocks[1:]:
            model_str += str(block)
        return model_str


model_type_path_default = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'smdx')
model_types = {}

def model_type_get(model_id):

    global file_pathlist
    global model_types

    model_type = model_types.get(str(model_id))
    if model_type is None:
        smdx_data = ''
        # create model file name
        filename = smdx.model_id_to_filename(model_id)

        # check in file path list if set
        if file_pathlist is not None:
            try:
                smdx_data = file_pathlist.read(filename)
            except NameError:
                pass

        if not smdx_data:
            if not os.path.exists(filename):
                filename = os.path.join(model_type_path_default, filename)

            if os.path.exists(filename):
                try:
                    f = open(filename, 'r')
                    smdx_data = f.read()
                    f.close()
                except Exception as e:
                    raise SunSpecError('Error loading model %s at %s: %s' % (model_id, filename, str(e)))

        if smdx_data:
            root = ET.fromstring(smdx_data)

            # load model type
            try:
                model_type = ModelType()
                model_type.from_smdx(root)
                model_types[model_type.id] = model_type
            except Exception as e:
                raise SunSpecError('Error loading model %s at %s: %s' % (model_id, filename, str(e)))
        else:
            raise SunSpecError('Model file for model %s not found' % (str(model_id)))

    return model_type

def check_for_models(pathlist):
    # The common model (1) should be accessible.
    try:
        model_type_get(1)
    except:
        raise Exception(
            'Unable to open common model (1).  '
            'Make certain model repository is available.  '
            'Please reference the README.md.'
        )

class ModelType(object):
    """
    Parameters:

        mid :
            Model id that identifies a specific SunSpec model type definition.

    Attributes:

        id
            Model id that identifies a specific SunSpec model type definition.

        len
            Length in Modbus registers of the model type as specified in the
            model definition.

        label
            Label string as specified in the model definition.

        description
            Description string as specified in the model definition.

        notes
            Notes string as specified in the model definition.

        fixed_block
            Fixed block type as specified in the model definition if present.

        repeating_block
            Repeating block type as specified in the model definition if
            present.
    """

    def __init__(self, mid=None):

        self.id = mid
        self.len = None
        self.name = None
        self.label = None
        self.description = None
        self.notes = None
        self.fixed_block = None
        self.repeating_block = None
        self.symbols = {}

    def from_smdx(self, element):
        """ Sets the model type attributes based on an element tree model type
        element contained in an SMDX model definition.

        Parameters:

            element :
                Element Tree model type element.
        """

        smdx_data = ''

        for m in element.findall(smdx.SMDX_MODEL):
            if True:
                self.id = int(m.attrib.get(smdx.SMDX_ATTR_ID))
                self.len = m.attrib.get(smdx.SMDX_ATTR_LEN)
                self.name = m.attrib.get(smdx.SMDX_ATTR_NAME)
                if self.name is None:
                    self.name = 'model_' + str(self.id)

                if self.len is None:
                    raise SunSpecError('Module len error')
                self.len = int(self.len)

                for b in m.findall(smdx.SMDX_BLOCK):
                    block = BlockType(model_type=self)
                    block.from_smdx(b)

                    if block.type == suns.SUNS_BLOCK_FIXED:
                        if self.fixed_block is None:
                            self.fixed_block = block
                        else:
                            raise SunSpecError('Duplicate fixed block type definition')
                    elif block.type == suns.SUNS_BLOCK_REPEATING:
                        if self.repeating_block is None:
                            self.repeating_block = block
                        else:
                            raise SunSpecError('Duplicate repeating block type definition')
                break
            else:
                raise SunSpecError('Unexpected smdx element: %s' % m.tag)

        for s in element.findall(smdx.SMDX_STRINGS):
            if s.attrib.get(smdx.SMDX_ATTR_ID) == str(self.id):
                m = s.find(smdx.SMDX_MODEL)
                if m is not None:
                    for e in m.findall('*'):
                        if e.tag == smdx.SMDX_LABEL:
                            self.label = e.text
                        elif e.tag == smdx.SMDX_DESCRIPTION:
                            self.description = e.text
                        elif e.tag == smdx.SMDX_NOTES:
                            self.notes = e.text
                for e in s.findall(smdx.SMDX_POINT):
                    pid = e.attrib.get(smdx.SMDX_ATTR_ID)
                    point_type = None
                    if self.fixed_block is not None:
                        point_type = self.fixed_block.points.get(pid)
                    if point_type is None and self.repeating_block is not None:
                        point_type = self.repeating_block.points.get(pid)
                    if point_type:
                        point_type.from_smdx(e, strings=True)

        if self.fixed_block is None:
            self.fixed_block = BlockType(suns.SUNS_BLOCK_FIXED, model_type=self)

    def symbol_add(self, symbol):
        self.symbols[symbol.id] = symbol

    def symbol_get(self, sid):
        return self.symbols.get(sid)

    def not_equal(self, model_type):
        """ Determines if the specified model type instance is not equal based
        on all the model type attribute values including blocks and points.  If
        not equal, returns a string indicating why the model type is not equal.
        Returns False if the model type is equal.

        Parameters:

            model_type :
                Model type to compare.
        """

        if self == model_type:
            return False

        if model_type is None:
            return "ModelType is None"
        if self.id != model_type.id:
            return "ModelType attribute 'id' not equal: %s  %s" % (str(self.id), str(model_type.id))
        if self.len != model_type.len:
            return "ModelType attribute 'len' not equal: %s  %s" % (str(self.len), str(model_type.len))
        if self.label != model_type.label:
            return "ModelType attribute 'label' not equal: %s  %s" % (str(self.label), str(model_type.label))
        if self.description != model_type.description:
            return "ModelType attribute 'description' not equal: %s  %s" % (str(self.description), str(model_type.description))
        if self.notes != model_type.notes:
            return "ModelType attribute 'notes' not equal: %s  %s" % (str(self.notes), str(model_type.notes))
        if self.fixed_block is not None:
            not_equal = self.fixed_block.not_equal(model_type.fixed_block)
            if not_equal:
                return not_equal
        elif model_type.fixed_block is not None:
            return "ModelType fixed block is None"
        if self.repeating_block is not None:
            not_equal = self.repeating_block.not_equal(model_type.repeating_block)
            if not_equal:
                return not_equal
        elif model_type.repeating_block is not None:
            return "ModelType repeating block is None"

        return False

    def __str__(self):

        s = 'ModelType: id = %s len = %s\n' % (self.id, self.len)
        if self.fixed_block:
            s += str(self.fixed_block)
        if self.repeating_block:
            s += str(self.repeating_block)
        return s

class BlockType(object):
    """
    Parameters:

        btype :
            Block type as specified in the model definition. Valid values are
            sunspec.core.suns.SUNS_BLOCK_FIXED or
            sunspec.core.suns.SUNS_BLOCK_REPEATING.

        blen : Block length in Modbus registers.

    Attributes:

        type
            Block type as specified in the model definition. Valid values are
            sunspec.core.suns.SUNS_BLOCK_FIXED or
            sunspec.core.suns.SUNS_BLOCK_REPEATING.

        len
            Block length in Modbus registers.

        points_list
            List containing the points in the block in offset order.

        points
            Dictionary containg the points in the block indexed by the point id.
    """

    def __init__(self, btype=None, blen=0, name=None, model_type=None):
        self.model_type = model_type
        self.type = btype
        self.len = blen
        self.name = name
        self.points_list = []
        self.points = {}

    def from_smdx(self, element):
        """ Sets the block type attributes based on an element tree block type
        element contained in an SMDX model definition.

        Parameters:

            element :
                Element Tree block type element.
        """

        btype = element.attrib.get(smdx.SMDX_ATTR_TYPE, smdx.SMDX_ATTR_TYPE_FIXED)

        if btype != smdx.SMDX_ATTR_TYPE_FIXED and btype != smdx.SMDX_ATTR_TYPE_REPEATING:
            raise SunSpecError('Invalid block type')

        self.type = smdx.smdx_block_types.get(btype)
        self.len = element.attrib.get(smdx.SMDX_ATTR_LEN)
        if self.len is None:
            raise SunSpecError('Block len error')
        self.name = element.attrib.get(smdx.SMDX_ATTR_NAME)
        if self.name is None:
            self.name = self.type

        # process points
        for e in element.findall(smdx.SMDX_POINT):
            pt = PointType(block_type=self)
            pt.from_smdx(e)

            if self.points.get(pt.id) is not None:
                ET.dump(e)
                raise SunSpecError('Duplicate point definition: %s' % (pt.id))

            self.points_list.append(pt)
            self.points[pt.id] = pt

    def not_equal(self, block_type):
        """ Determines if the specified block type instance is not equal based
        on all the block type attribute values including points.  If not equal,
        returns a string indicating why the block type is not equal. Returns
        False if the block type is equal.

        Parameters:

            block_type :
                Block type to compare.
        """

        if self == block_type:
            return False

        if block_type is None:
            return "BlockType '%s' is none" % (str(self.type))
        if self.type != block_type.type:
            return "BlockType attribute 'type' not equal: %s  %s" % (str(self.type), str(block_type.type))
        if self.len != block_type.len:
            return "BlockType attribute 'len' not equal: %s  %s" % (str(self.len), str(block_type.len))
        if len(self.points) != len(block_type.points):
            return "BlockType '%s' point count not equal" % (str(self.type))
        for k, v in self.points.items():
            value = block_type.points.get(k)
            not_equal =  v.not_equal(value)
            if not_equal:
                return not_equal

        return False

    def __str__(self):

        s = 'BlockType: type = %s len = %s\n' % (self.type, self.len)
        for p in self.points_list:
            s += '  %s\n' % (str(p))
        return s

class PointType(object):
    """
    Parameters:

        pid :
            Point id as specified in the model definition.

        offset :
            Point offset within the block as specified in the model definition.

        ptype :
            Point type as specified in the model definition. Valid values are
            defined in sunspec.core.suns.SUNS_TYPE_*.

        plen :
            Point length in Modbus registers for points that have a type of
            'string'.

        mandatory :
            Mandatory indication as specified in the model definition. Valid
            values are sunspec.core.suns.SUNS_MANDATORY_TRUE or
            sunspec.core.suns.SUNS_MANDATORY_FALSE.

        access :
            Point access setting as specfied in the model definition. Valid
            values are sunspec.core.suns.SUNS_ACCESS_R or
            sunspec.core.suns.SUNS_ACCESS_RW.

        sf :
            Id of the scale factor point associated with the point or None if
            the point does not have a scale factor.

    Attributes:

        id
            Point id as specified in the model definition.

        offset
            Point offset within the block as specified in the model definition.

        type
            Point type as specified in the model definition. Valid values are
            defined in sunspec.core.suns.SUNS_TYPE_*.

        len
            Point length in Modbus registers for points that have a type of
            'string'.

        mandatory
            Mandatory indication as specified in the model definition. Valid
            values are sunspec.core.suns.SUNS_MANDATORY_TRUE or
            sunspec.core.suns.SUNS_MANDATORY_FALSE.

        access
            Point access setting as specfied in the model definition. Valid
            values are sunspec.core.suns.SUNS_ACCESS_R or
            sunspec.core.suns.SUNS_ACCESS_RW.

        sf
            Id of the scale factor point associated with the point or None if
            the point does not have a scale factor.

        label
            Label string as specified in the model definition.

        description
            Description string as specified in the model definition.

        notes
            Notes string as specified in the model definition.

        value_default
            Default value for a point instance if no value specified.

        is_impl
            Contains the function to call with the point value as an argument to
            determine if the point is implemented.

        data_to
            Contains the function to call to transform a binary data string to
            the point value.

        to_data
            Contains the function to call to transform the point value to a
            binary data string.

        to_value
            Contains the function to call to transform a point value string into
            a point value of the type associated with the point.
    """

    def __init__(self, pid=None, offset=None, ptype=None, plen=None, mandatory=None, access=None, sf=None,
                 block_type=None):
        self.block_type = block_type
        self.id = pid
        self.offset = offset
        self.type = ptype
        self.len = plen
        self.mandatory = mandatory
        self.access = access
        self.units = None
        self.sf = sf
        self.label = None
        self.description = None
        self.notes = None
        self.value_default = None
        self.is_impl = None
        self.data_to = None
        self.to_data = None
        self.to_value = None
        self.symbols = []

    def from_smdx(self, element, strings=False):
        """ Sets the point attributes based on an element tree point element
        contained in an SMDX model definition.

        Parameters:

            element :
                Element Tree point type element.

            strings :
                Indicates if *element* is a subelement of the 'strings'
                definintion within the model definition.
        """

        for e in element.findall('*'):
            if e.tag == smdx.SMDX_LABEL:
                self.label = e.text
            elif e.tag == smdx.SMDX_DESCRIPTION:
                self.description = e.text
            elif e.tag == smdx.SMDX_NOTES:
                self.notes = e.text
            elif e.tag == smdx.SMDX_SYMBOL:
                sid = e.attrib.get(smdx.SMDX_ATTR_ID)
                symbol = self.block_type.model_type.symbol_get(sid)
                if symbol is None:
                    symbol = Symbol()
                    symbol.from_smdx(e, strings)
                    self.block_type.model_type.symbol_add(symbol)
                if self.symbol_get(sid) is None:
                    self.symbols.append(symbol)
                symbol.from_smdx(e, strings)

        if strings is False:
            self.id = element.attrib.get(smdx.SMDX_ATTR_ID)
            self.offset = int(element.attrib.get(smdx.SMDX_ATTR_OFFSET))
            ptype = element.attrib.get(smdx.SMDX_ATTR_TYPE)
            plen = element.attrib.get(smdx.SMDX_ATTR_LEN)
            mandatory = element.attrib.get(smdx.SMDX_ATTR_MANDATORY, smdx.SMDX_MANDATORY_FALSE)
            access = element.attrib.get(smdx.SMDX_ATTR_ACCESS, smdx.SMDX_ACCESS_R)
            self.units = element.attrib.get(smdx.SMDX_ATTR_UNITS)

            if self.id is None:
                raise SunSpecError('Missing point id attribute')
            if self.offset is None:
                raise SunSpecError('Missing offset attribute for point: %s' % self.id)
            if ptype is None:
                raise SunSpecError('Missing type attribute for point: %s' % self.id)
            if ptype == smdx.SMDX_TYPE_STRING and plen is None:
                raise SunSpecError('Missing len attribute for point: %s' % self.id)

            self.type = smdx.smdx_point_types.get(ptype)
            if self.type is None:
                raise SunSpecError('Unknown point type: %s' % ptype)
            self.mandatory = smdx.smdx_mandatory_types.get(mandatory)
            if self.mandatory is None:
                raise SunSpecError('Unknown mandatory type: %s' % mandatory)
            self.access = smdx.smdx_access_types.get(access)
            if self.access is None:
                raise SunSpecError('Unknown access type: %s' % access)
            self.sf = element.attrib.get(smdx.SMDX_ATTR_SF)

            info = suns.suns_point_type_info.get(self.type)

            if info is not None:
                self.len, self.is_impl, self.data_to, self.to_data, self.to_value, self.value_default = info
                if plen is not None:
                    self.len = int(plen)

    def symbol_get(self, sid):
        for symbol in self.symbols:
            if symbol.id == sid:
                return symbol

    def not_equal(self, point_type):
        """ Determines if the specified point type instance is not equal based
        on all the point type attribute values. If not equal, returns string
        indicating why the point type is not equal. Returns False if the point
        type is equal.

        Parameters:

            point_type :
                Point type to compare.
        """

        if self == point_type:
            return False

        if point_type is None:
            return "PointType '%s' is None" % (str(self.id))
        if len(self.__dict__) != len(point_type.__dict__):
            return "PointType '%s' attribute count not equal': %s  %s" % (str(self.id))
        for k, v in self.__dict__.items():
            if k != 'block_type':
                value = point_type.__dict__.get(k)
                if v is not None and value is not None:
                    if value is None or v != value:
                        return "PointType '%s' attribute '%s' not equal: %s  %s" % (str(self.id), str(k), str(v), str(value))

        return False

    def __str__(self):

        return 'PointType: id = %s offset = %d type = %s len = %d sf = %s access = %s mandatory = %s' % \
            (self.id, self.offset, self.type, self.len, self.sf, self.access, self.mandatory)

class Symbol(object):

    def __init__(self, sid=None):
        self.id = sid
        self.value = None
        self.label = None
        self.description = None
        self.notes = None

    def from_smdx(self, element, strings=False):

        for e in element.findall('*'):
            if e.tag == smdx.SMDX_LABEL:
                self.label = e.text
            elif e.tag == smdx.SMDX_DESCRIPTION:
                self.description = e.text
            elif e.tag == smdx.SMDX_NOTES:
                self.notes = e.text

        if strings is False:
            self.id = element.attrib.get(smdx.SMDX_ATTR_ID)
            self.value = element.text
            if self.id is None:
                raise SunSpecError('Missing point id attribute')

    def __str__(self):

        return 'Symbol: id = %s value = %s' % (self.id, self.value)
