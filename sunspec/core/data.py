
"""
  Copyright (c) 2014, SunSpec Alliance
  All Rights Reserved

"""

import time

try:
    import xml.etree.ElementTree as ET
except:
    import elementtree.ElementTree as ET

import sunspec.core.util as util

SDX_VERSION = '1'
SDX_SUNSPEC_DATA = 'sunSpecData'
SDX_SUNSPEC_DATA_VERSION = 'v'
SDX_DEVICE = 'd'
SDX_DEVICE_LOGGER_ID = 'lid'
SDX_DEVICE_NAMESPACE = 'ns'
SDX_DEVICE_ID = 'id'
SDX_DEVICE_IFC = 'if'
SDX_DEVICE_MAN = 'man'
SDX_DEVICE_MOD = 'mod'
SDX_DEVICE_SN = 'sn'
SDX_DEVICE_TIME = 't'
SDX_DEVICE_CORRELATION_ID = 'cid'
SDX_MODEL = 'm'
SDX_MODEL_ID = 'id'
SDX_MODEL_NAMESPACE = 'ns'
SDX_MODEL_INDEX = 'x'
SDX_POINT = 'p'
SDX_POINT_ID = 'id'
SDX_POINT_INDEX = 'index'
SDX_POINT_SF = 'sf'
SDX_POINT_UNITS = 'u'
SDX_POINT_DESC = 'd'
SDX_POINT_TIME = 't'

class SunSpecDataError(Exception):
    pass

class SunSpecData(object):

    def device_add(self, logger_id=None, man=None, mod=None, sn=None, timestamp=None, cid=None, device_id=None, ifc=None, namespace=None):

    	d = DeviceData(logger_id,  man, mod, sn, timestamp, cid, device_id, ifc, namespace)
    	self.device_data.append(d)
    	return d

    def from_xml(self, element=None, data_record=None):

        if data_record is not None:
            self.root = ET.fromstring(data_record)
        elif element is not None:
            self.root = element

        if self.root:
            if self.root.tag != SDX_SUNSPEC_DATA:
                raise SunSpecDataError("Unexpected root element: %s" % (self.root.tag))

            self.version = self.root.attrib.get(SDX_SUNSPEC_DATA_VERSION)

            for d in self.root.findall('*'):
                if d.tag != SDX_DEVICE:
                    raise SunSpecDataError("Unexpected '%s' element in '%s' element" % (d.tag, self.root.tag))
                dd = DeviceData()
                dd.from_xml(d)
                self.device_data.append(dd)

    def to_xml(self, pretty_print=False):

        attr = {}

        if self.version:
            attr[SDX_SUNSPEC_DATA_VERSION] = self.version

        self.root = ET.Element(SDX_SUNSPEC_DATA, attrib=attr)
        for d in self.device_data:
            d.to_xml(self.root)

        if pretty_print:
            util.indent(self.root)

        return ET.tostring(self.root)

    def __init__(self, element=None, data_record=None):

        self.root = None
        self.version = None
        self.device_data = []

        self.from_xml(element, data_record)

class DeviceData(object):

    def __init__(self, logger_id=None, man=None, mod=None, sn=None, timestamp=None, cid=None, device_id=None, ifc=None, namespace=None):

        self.logger_id = logger_id
        self.namespace = namespace
        self.device_id = device_id
        self.ifc = ifc
        self.man = man
        self.mod = mod
        self.sn = sn
        self.timestamp = timestamp
        self.cid = cid
        self.model_data = []

        if timestamp:
        	self.timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(timestamp))

    def model_add(self, model_id=None, index=None, namespace=None):

    	m = ModelData(model_id, namespace, index)
    	self.model_data.append(m)
    	return m

    def from_xml(self, element):

        self.logger_id = element.attrib.get(SDX_DEVICE_LOGGER_ID)
        self.namespace = element.attrib.get(SDX_DEVICE_NAMESPACE)
        self.device_id = element.attrib.get(SDX_DEVICE_ID)
        self.ifc = element.attrib.get(SDX_DEVICE_IFC)
        self.man = element.attrib.get(SDX_DEVICE_MAN)
        self.mod = element.attrib.get(SDX_DEVICE_MOD)
        self.sn = element.attrib.get(SDX_DEVICE_SN)
        self.time = element.attrib.get(SDX_DEVICE_TIME)
        self.cid = element.attrib.get(SDX_DEVICE_CORRELATION_ID)

        for m in element.findall('*'):
            if m.tag != SDX_MODEL:
                raise SunSpecDataError("Unexpected '%s' element in '%s' element" % (m.tag, element.tag))
            md = ModelData()
            md.from_xml(m)
            self.model_data.append(md)

    def to_xml(self, parent):

        attr = {}

        if self.logger_id:
            attr[SDX_DEVICE_LOGGER_ID] = self.logger_id
        if self.namespace:
            attr[SDX_DEVICE_NAMESPACE] = self.namespace
        if self.device_id:
            attr[SDX_DEVICE_ID] = self.device_id
        if self.ifc:
            attr[SDX_DEVICE_IFC] = self.ifc
        if self.man:
            attr[SDX_DEVICE_MAN] = self.man
        if self.mod:
            attr[SDX_DEVICE_MOD] = self.mod
        if self.sn:
            attr[SDX_DEVICE_SN] = self.sn
        if self.timestamp:
            attr[SDX_DEVICE_TIME] = self.timestamp
        if self.cid:
            attr[SDX_DEVICE_CORRELATION_ID] = self.cid

        e = ET.SubElement(parent, SDX_DEVICE, attrib=attr)
        for m in self.model_data:
            m.to_xml(e)

class ModelData(object):

    def __init__(self, model_id=None, index=None, namespace=None):

        self.model_id = str(model_id)
        self.namespace = namespace
        self.index = index
        self.point_data = []

    def point_add(self, point_id=None, value=None, index=None, sf=None, units=None, desc=None, time=None):

    	p = PointData(point_id, value, index, sf, units, desc, time)
    	self.point_data.append(p)
    	return p

    def from_xml(self, element):

        self.model_id = element.attrib.get(SDX_MODEL_ID)
        self.namespace = element.attrib.get(SDX_MODEL_NAMESPACE)
        self.index = element.attrib.get(SDX_MODEL_INDEX)
        for p in element.findall('*'):
            if p.tag != SDX_POINT:
                raise SunSpecDataError("Unexpected '%s' element in '%s' element" % (p.tag, element.tag))
            pd = PointData()
            pd.from_xml(p)
            self.point_data.append(pd)

    def to_xml(self, parent):

        attr = {SDX_MODEL_ID: str(self.model_id)}

        if self.index:
            attr[SDX_MODEL_INDEX] = self.index
        if self.namespace:
            attr[SDX_MODEL_NAMESPACE] = self.namespace

        e = ET.SubElement(parent, SDX_MODEL, attrib=attr)
        for p in self.point_data:
            p.to_xml(e)

class PointData(object):

    def __init__(self, point_id=None, value=None, index=None, sf=None, units=None, desc=None, time=None):

        self.point_id = point_id
        self.value = value
        self.index = index
        self.sf = sf
        self.units = units
        self.desc = desc
        self.time = time

    # skip units and description for now
    def from_xml(self, element):

        self.point_id = element.attrib.get(SDX_POINT_ID)
        self.index = element.attrib.get(SDX_POINT_INDEX)
        self.sf = element.attrib.get(SDX_POINT_SF)
        # self.units = element.attrib.get(SDX_POINT_UNITS)
        # self.desc = element.attrib.get(SDX_POINT_DESC)
        self.time = element.attrib.get(SDX_POINT_TIME)
        self.value = element.text

    def to_xml(self, parent):

        attr = {SDX_POINT_ID: str(self.point_id)}

        if self.index:
            attr[SDX_POINT_INDEX] = str(self.index)
        if self.sf:
            attr[SDX_POINT_SF] = str(self.sf)
        if self.time:
            attr[SDX_POINT_TIME] = self.time

        e = ET.SubElement(parent, SDX_POINT, attrib=attr)
        if self.value:
            e.text = str(self.value)


