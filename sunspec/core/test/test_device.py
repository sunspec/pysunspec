
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

import sys
import os
import unittest

try:
    import xml.etree.ElementTree as ET
except:
    import elementtree.ElementTree as ET

import sunspec.core.device as device
import sunspec.core.util as util
import sunspec.core.pics as pics
import sunspec.core.smdx as smdx
import sunspec.core.suns as suns

test_device_pointtype_smdx_1 = """
<sunSpecModels v="1">
  <!-- 1: common -->
  <model id="63001" len="152">
    <block len="134">
      <point id="sunssf_1"      offset="0"    type="sunssf" />
      <point id="sunssf_2"      offset="1"    type="sunssf" />
      <point id="sunssf_3"      offset="2"    type="sunssf" />
      <point id="sunssf_4"      offset="3"    type="sunssf" />
      <point id="int16_1"       offset="4"    type="int16"   sf="sunssf_1"  units="units_1" />
        <symbol id="SYMBOL_1_1">1</symbol>
        <symbol id="SYMBOL_1_2">2</symbol>
        <symbol id="SYMBOL_1_3">3</symbol>
      <point id="int16_2"       offset="5"    type="int16"   sf="sunssf_2"  units="units_2" />
        <symbol id="SYMBOL_2_1">1</symbol>
        <symbol id="SYMBOL_2_2">2</symbol>
        <symbol id="SYMBOL_2_3">3</symbol>
      <point id="int16_3"       offset="6"    type="int16"   sf="sunssf_3"  units="units_3" />
      <point id="int16_4"       offset="7"    type="int16"   sf="sunssf_4"  units="units_4" />
      <point id="int16_5"       offset="8"    type="int16" />
      <point id="int16_u"       offset="9"    type="int16" />
      <point id="uint16_1"      offset="10"   type="uint16"  sf="sunssf_1" />
      <point id="uint16_2"      offset="11"   type="uint16"  sf="sunssf_2" />
      <point id="uint16_3"      offset="12"   type="uint16"  sf="sunssf_3" />
      <point id="uint16_4"      offset="13"   type="uint16"  sf="sunssf_4" />
      <point id="uint16_5"      offset="14"   type="uint16" />
      <point id="uint16_u"      offset="15"   type="uint16" />
      <point id="acc16"         offset="16"   type="acc16" />
      <point id="acc16_u"       offset="17"   type="acc16" />
      <point id="enum16"        offset="18"   type="enum16" />
      <point id="enum16_u"      offset="19"   type="enum16" />
      <point id="bitfield16"    offset="20"   type="bitfield16" />
      <point id="bitfield16_u"  offset="21"   type="bitfield16" />
      <point id="int32_1"       offset="22"   type="int32"   sf="sunssf_5" />
      <point id="int32_2"       offset="24"   type="int32"   sf="sunssf_6" />
      <point id="int32_3"       offset="26"   type="int32"   sf="sunssf_7" />
      <point id="int32_4"       offset="28"   type="int32" />
      <point id="int32_5"       offset="30"   type="int32" />
      <point id="int32_u"       offset="32"   type="int32" />
      <point id="uint32_1"      offset="34"   type="uint32"  sf="sunssf_5" />
      <point id="uint32_2"      offset="36"   type="uint32"  sf="sunssf_6" />
      <point id="uint32_3"      offset="38"   type="uint32"  sf="sunssf_7" />
      <point id="uint32_4"      offset="40"   type="uint32"  sf="1" />
      <point id="uint32_5"      offset="42"   type="uint32" />
      <point id="uint32_u"      offset="44"   type="uint32" />
      <point id="acc32"         offset="46"   type="acc32" />
      <point id="acc32_u"       offset="48"   type="acc32" />
      <point id="enum32"        offset="50"   type="enum32" />
      <point id="enum32_u"      offset="52"   type="enum32" />
      <point id="bitfield32"    offset="54"   type="bitfield32" />
      <point id="bitfield32_u"  offset="56"   type="bitfield32" />
      <point id="ipaddr"        offset="58"   type="ipaddr" />
      <point id="ipaddr_u"      offset="60"   type="ipaddr" />
      <point id="int64"         offset="62"   type="int64" />
      <point id="int64_u"       offset="66"   type="int64" />
      <point id="acc64"         offset="70"   type="acc64" />
      <point id="acc64_u"       offset="74"   type="int64" />
      <point id="ipv6addr"      offset="78"   type="ipv6addr" />
      <point id="ipv6addr_u"    offset="86"   type="ipv6addr" />
      <point id="float32"       offset="94"   type="float32" />
      <point id="float32_u"     offset="96"   type="float32" />
      <point id="string"        offset="98"   type="string"  len="16"/>
      <point id="string_u"      offset="114"  type="string"  len="16"/>
      <point id="sunssf_5"      offset="130"  type="sunssf" />
      <point id="sunssf_6"      offset="131"  type="sunssf" />
      <point id="sunssf_7"      offset="132"  type="sunssf" />
      <point id="pad_1"         offset="133"  type="pad" />
    </block>
    <block type="repeating" len="18">
      <point id="sunssf_8"      offset="0"    type="sunssf" />
      <point id="int16_11"      offset="1"    type="int16"   sf="sunssf_8" />
      <point id="int16_12"      offset="2"    type="int16"   sf="sunssf_9" />
      <point id="int16_u"       offset="3"    type="int16" />
      <point id="uint16_11"     offset="4"    type="uint16"  sf="sunssf_8" />
      <point id="uint16_12"     offset="5"    type="uint16"  sf="sunssf_9" />
      <point id="uint16_13"     offset="6"    type="uint16" />
      <point id="uint16_u"      offset="7"    type="uint16" />
      <point id="int32"         offset="8"    type="int32"   sf="sunssf_1" />
      <point id="int32_u"       offset="10"   type="int32" />
      <point id="uint32"        offset="12"   type="uint32"  sf="sunssf_9" />
      <point id="uint32_u"      offset="14"   type="uint32" />
      <point id="sunssf_9"      offset="16"   type="sunssf" />
      <point id="pad_2"         offset="17"   type="pad" />
    </block>
  </model>

  <strings id="63001" locale="en">
    <model>
      <label>Model 63001 label</label>
      <description>SunSpec test model 63001</description>
      <notes>Provides testing for all SunSpec smdx elements and attributes</notes>
    </model>
  </strings>

</sunSpecModels>
"""

test_device_pointtype_smdx_2 = """
    <block len="134">
      <point id="p_int16"       offset="0"    type="int16" />
      <point id="p_uint16"      offset="1"    type="uint16" />
      <point id="p_acc16"       offset="2"    type="acc16" />
      <point id="p_enum16"      offset="3"    type="enum16" />
      <point id="p_bitfield16"  offset="4"    type="bitfield16" />
      <point id="p_int32"       offset="5"    type="int32" />
      <point id="p_uint32"      offset="7"    type="uint32" />
      <point id="p_acc32"       offset="9"    type="acc32" />
      <point id="p_enum32"      offset="11"   type="enum32" />
      <point id="p_bitfield32"  offset="13"   type="bitfield32" />
      <point id="p_ipaddr"      offset="15"   type="ipaddr" />
      <point id="p_int64"       offset="17"   type="int64" />
      <point id="p_acc64"       offset="21"   type="acc64" />
      <point id="p_ipv6addr"    offset="25"   type="ipv6addr" />
      <point id="p_float32"     offset="33"   type="float32" />
      <point id="p_string"      offset="35"   type="string"     len="8" />
      <point id="p_sunssf"      offset="43"   type="sunssf" />
      <point id="p_pad"         offset="44"   type="pad" />
    </block>
"""

def create_test_device_1():

    d = device.Device()

    # create model 1 with values
    m1 = device.Model(device=d, mid=1)
    m1.load()
    d.models_list.append(m1)
    b = m1.blocks[0]
    b.points['Mn'].value_base = 'SunSpecTest'
    b.points['Md'].value_base = 'TestDevice-1'
    b.points['Opt'].value_base = 'opt_a_b_c'
    b.points['Vr'].value_base = '1.2.3'
    b.points['SN'].value_base = 'sn-123456789'
    b.points['DA'].value_base = 1

    # create model 63001 with values
    m2 = device.Model(device=d, mid=63001, mlen=188)
    m2.load()
    d.models_list.append(m2)

    # fixed block
    b = m2.blocks[0]
    b.points_sf['sunssf_1'].value_base = -10
    b.points_sf['sunssf_2'].value_base = 10
    b.points_sf['sunssf_3'].value_base = 0
    b.points_sf['sunssf_4'].value_base = 1
    b.points_sf['sunssf_5'].value_base = 2
    b.points_sf['sunssf_6'].value_base = 3
    b.points_sf['sunssf_7'].value_base = 4

    b.points['int16_1'].value_base = 1
    b.points['int16_2'].value_base = -1
    b.points['int16_3'].value_base = 2
    b.points['int16_4'].value_base = -2
    b.points['int16_5'].value_base = 3
    b.points['int16_u'].value_base = None
    b.points['uint16_1'].value_base = 4
    b.points['uint16_2'].value_base = 5
    b.points['uint16_3'].value_base = 65524
    b.points['uint16_4'].value_base = 6
    b.points['uint16_5'].value_base = 7
    b.points['uint16_u'].value_base = None
    b.points['acc16'].value_base = 8
    b.points['acc16_u'].value_base = None
    b.points['enum16'].value_base = 9
    b.points['enum16_u'].value_base = None
    b.points['bitfield16'].value_base =  10
    b.points['bitfield16_u'].value_base = None
    b.points['int32_1'].value_base = 11
    b.points['int32_2'].value_base = 12
    b.points['int32_3'].value_base = 13
    b.points['int32_4'].value_base = 14
    b.points['int32_5'].value_base = 15
    b.points['int32_u'].value_base = None
    b.points['uint32_1'].value_base = 16
    b.points['uint32_2'].value_base = 17
    b.points['uint32_3'].value_base = 18
    b.points['uint32_4'].value_base = 19
    b.points['uint32_5'].value_base = 20
    b.points['uint32_u'].value_base = None
    b.points['acc32'].value_base = 21
    b.points['acc32_u'].value_base = None
    b.points['enum32'].value_base = 22
    b.points['enum32_u'].value_base = None
    b.points['bitfield32'].value_base = 23
    b.points['bitfield32_u'].value_base = None
    b.points['ipaddr'].value_base = 0x01020304
    b.points['ipaddr_u'].value_base = None
    b.points['int64'].value_base = 24
    b.points['int64_u'].value_base = None
    b.points['acc64'].value_base = 25
    b.points['acc64_u'].value_base = None
    b.points['ipv6addr'].value_base = None
    b.points['ipv6addr_u'].value_base = None
    b.points['float32'].value_base = 26
    b.points['float32_u'].value_base = None
    b.points['string'].value_base = '12345678'
    b.points['string_u'].value_base = None

    # repeating block 1
    b = m2.blocks[1]
    b.points_sf['sunssf_8'].value_base = -2
    b.points_sf['sunssf_9'].value_base = -3

    b.points['int16_11'].value_base = 30
    b.points['int16_12'].value_base = 31
    b.points['int16_u'].value_base = None
    b.points['uint16_11'].value_base = 32
    b.points['uint16_12'].value_base = 33
    b.points['uint16_13'].value_base = 34
    b.points['uint16_u'].value_base = None
    b.points['int32'].value_base = 35
    b.points['int32_u'].value_base = None
    b.points['uint32'].value_base = 36
    b.points['uint32_u'].value_base = None

    # repeating block 2
    b = m2.blocks[2]
    b.points_sf['sunssf_8'].value_base = -4
    b.points_sf['sunssf_9'].value_base = -5

    b.points['int16_11'].value_base = 40
    b.points['int16_12'].value_base = 41
    b.points['int16_u'].value_base = None
    b.points['uint16_11'].value_base = 42
    b.points['uint16_12'].value_base = 43
    b.points['uint16_13'].value_base = 44
    b.points['uint16_u'].value_base = None
    b.points['int32'].value_base = 45
    b.points['int32_u'].value_base = None
    b.points['uint32'].value_base = 46
    b.points['uint32_u'].value_base = None

    # repeating block 3
    b = m2.blocks[3]
    b.points_sf['sunssf_8'].value_base = 2
    b.points_sf['sunssf_9'].value_base = 3

    b.points['int16_11'].value_base = 50
    b.points['int16_12'].value_base = 51
    b.points['int16_u'].value_base = None
    b.points['uint16_11'].value_base = 52
    b.points['uint16_12'].value_base = 53
    b.points['uint16_13'].value_base = 54
    b.points['uint16_u'].value_base = None
    b.points['int32'].value_base = 55
    b.points['int32_u'].value_base = None
    b.points['uint32'].value_base = 56
    b.points['uint32_u'].value_base = None

    # update scale factor values in points
    for block in m2.blocks:
        for point in block.points_list:
            if point.sf_point is not None:
                point.value_sf = point.sf_point.value_base

    return d


class TestDevice(unittest.TestCase):
    def setUp(self):
        path = os.path.abspath(__file__)
        self.pathlist = util.PathList(['.',
                                       os.path.join(os.path.dirname(path),
                                                    'devices')])

        device.check_for_models(pathlist=self.pathlist)

    def test_device_modeltype(self):
        mt = device.ModelType()

        root = ET.fromstring(test_device_pointtype_smdx_1)
        mt.from_smdx(root)

        if mt.id != 63001 or mt.len != 152:
            raise Exception('model type attribute error: id = %s  len = %d' % (mt.id, mt.len))


    def test_device_pointtype(self):
        points = {}

        block = ET.fromstring(test_device_pointtype_smdx_2)
        for p in block.findall('*'):
            pt = device.PointType()
            pt.from_smdx(p)
            points[p.attrib.get(smdx.SMDX_ATTR_ID)] = pt

        pt = points.get('p_int16')
        if (pt.id != 'p_int16' or pt.offset != 0 or pt.type != suns.SUNS_TYPE_INT16 or pt.len != 1):
            raise Exception('p_int16 error')


    def test_device_pointtype_not_equal(self):
        pt1 = device.PointType('point_1', 0, smdx.SMDX_TYPE_INT16)
        pt2 = device.PointType('point_1', 0, smdx.SMDX_TYPE_INT16)
        pt3 = device.PointType('point_1', 0, smdx.SMDX_TYPE_INT16)

        not_equal = pt1.not_equal(pt2)
        if not_equal:
            raise Exception(not_equal)

        not_equal = pt1.not_equal(pt3)
        if not_equal:
            raise Exception(not_equal)


    def test_device_blocktype_not_equal(self):
        pt1a = device.PointType('point_1', 0, suns.SUNS_TYPE_INT16)
        pt1b = device.PointType('point_1', 0, suns.SUNS_TYPE_INT16)
        pt2a = device.PointType('point_2', 0, suns.SUNS_TYPE_UINT16)
        pt2b = device.PointType('point_2', 0, suns.SUNS_TYPE_UINT16)
        bt1a = device.BlockType(suns.SUNS_BLOCK_FIXED, 20)
        bt1b = device.BlockType(suns.SUNS_BLOCK_FIXED, 20)
        bt1a.points[pt1a.id] = pt1a
        bt1a.points[pt2a.id] = pt2a
        bt1b.points[pt1b.id] = pt1b
        bt1b.points[pt2b.id] = pt2b
        bt2a = device.BlockType(suns.SUNS_BLOCK_REPEATING, 30)
        bt2b = device.BlockType(suns.SUNS_BLOCK_REPEATING, 30)

        not_equal = bt1a.not_equal(bt1b)
        if not_equal:
            raise Exception(not_equal)

        not_equal = bt2a.not_equal(bt2b)
        if not_equal:
            raise Exception(not_equal)


    def test_device_modeltype_not_equal(self):
        pt1a = device.PointType('point_1', 0, suns.SUNS_TYPE_INT16)
        pt1b = device.PointType('point_1', 0, suns.SUNS_TYPE_INT16)
        pt2a = device.PointType('point_2', 0, suns.SUNS_TYPE_UINT16)
        pt2b = device.PointType('point_2', 0, suns.SUNS_TYPE_UINT16)
        bt1a = device.BlockType(suns.SUNS_BLOCK_FIXED, 20)
        bt1b = device.BlockType(suns.SUNS_BLOCK_FIXED, 20)
        bt1a.points[pt1a.id] = pt1a
        bt1a.points[pt2a.id] = pt2a
        bt1b.points[pt1b.id] = pt1b
        bt1b.points[pt2b.id] = pt2b
        bt2a = device.BlockType(suns.SUNS_BLOCK_REPEATING, 30)
        bt2b = device.BlockType(suns.SUNS_BLOCK_REPEATING, 30)
        mt1 = device.ModelType(1)
        mt2 = device.ModelType(1)
        mt1.fixed_block = bt1a
        mt1.repeating_block = bt2a
        mt2.fixed_block = bt1b
        mt2.repeating_block = bt2b

        not_equal = mt1.not_equal(mt2)
        if not_equal:
            raise Exception(not_equal)


    def test_device_from_pics(self):
        d1 = device.Device()
        d1.from_pics(filename='pics_test_device_1.xml', pathlist=self.pathlist)
        d2 = create_test_device_1()
        not_equal = d1.not_equal(d2)
        if not_equal:
            raise Exception(not_equal)


    def test_device_to_pics(self):
        d1 = device.Device()
        d1.from_pics(filename='pics_test_device_1.xml', pathlist=self.pathlist)

        root = ET.Element(pics.PICS_ROOT)
        d1.to_pics(root, single_repeating=False)
        # util.indent(root)
        # print(ET.tostring(root))

        d = root.find(pics.PICS_DEVICE)
        if d is None:
            raise Exception("No '%s' elements found in '%s' element" % (pics.PICS_DEVICE, root.tag))

        d2 = device.Device()
        d2.from_pics(element=d)

        not_equal = d1.not_equal(d2)
        if not_equal:
            raise Exception(not_equal)

    def test_device_value_get(self):
        d = device.Device()
        d.from_pics(filename='pics_test_device_1.xml', pathlist=self.pathlist)

        m = d.models[63001][0]
        p = 'int16_4'
        value = m.points[p].value
        expected_value = -20
        if value != expected_value:
            raise Exception("Value '%s' mismatch: %s %s" % (p, str(value), str(expected_value)))


    def test_device_value_set(self):
        d = device.Device()
        d.from_pics(filename='pics_test_device_1.xml', pathlist=self.pathlist)

        m = d.models[63001][0]
        expected_value = -180
        p = 'int16_4'
        m.points[p].value = expected_value
        value = m.points[p].value
        if value != expected_value:
            raise Exception("Value '%s' mismatch: %s %s" % (p, str(value), str(expected_value)))


    def test_device_common_len_65(self):
        d = device.Device()
        d.from_pics(filename='pics_test_device_2.xml', pathlist=self.pathlist)

        m_1 = d.models[1][0]
        expected_value = 'TestDevice-2'
        p = 'Md'
        value = m_1.points[p].value
        if value != expected_value:
            raise Exception("Value '%s' mismatch: %s %s" % (p, str(value), str(expected_value)))

        m_63001 = d.models[63001][0]
        expected_value = -180
        p = 'int16_4'
        m_63001.points[p].value = expected_value
        value = m_63001.points[p].value
        if value != expected_value:
            raise Exception("Value '%s' mismatch: %s %s" % (p, str(value), str(expected_value)))


    # verify all models in the default models directory can be read
    def test_device_models_smdx(self):

        path = device.model_type_path_default
        files = os.listdir(path)
        model_id = None
        for f in files:
            try:
                model_id = smdx.model_filename_to_id(f)
                if model_id is not None:
                    device.model_type_get(model_id)
            except Exception as e:
                raise Exception('Error scanning model %s: %s' % (str(model_id), e))

    def test_device_constant_sf(self):
        d = device.Device()
        d.from_pics(filename='pics_test_device_1.xml', pathlist=self.pathlist)

        m = d.models[63001][0]
        p = 'uint32_4'
        value = m.points[p].value
        expected_value = 190
        if value != expected_value:
            raise Exception("Value '%s' mismatch: %s %s" % (p, str(value), str(expected_value)))


if __name__ == "__main__":

  unittest.main()
