==============
 API Reference
==============

:mod:`sunspec.core` --- SunSpec Core Functionality
==================================================

The core package contains modules that provide the ability to interact with
SunSpec devices and encode/decode documents in SunSpec standard formats.  The
modules in the core package used to interact with SunSpec devices are organized
into the following main functional areas: base SunSpec device/model support,
Modbus protocol support, and client device support.

The device module provides objects that map to the SunSpec model definitions
within the SunSpec standards.  A device is a collection of SunSpec model
definitions that are implemented by a SunSpec compliant device. The device
module provides objects for device, model, block, and point instances as well
as objects that support the model, block, and point type definitions.

The modbus package provides protocol support for Modbus TCP, Modbus RTU, and
locally defined Modbus maps that can be accessed directly.

The client module extends the basic objects in the device module to provide
objects that can be used to access devices using the Modbus protocol objects
supplied in the modbus package.

:mod:`sunspec.core.client` --- SunSpec Client classes
=====================================================

.. module:: sunspec.core.client

Classes
-------

.. autoclass:: sunspec.core.client.SunSpecClientDevice
    :members: close, read

.. autoclass:: sunspec.core.client.SunSpecClientModelBase
    :members: read, write

.. autoclass:: sunspec.core.client.SunSpecClientBlockBase
    :members:

.. autoclass:: sunspec.core.client.ClientDevice
    :members: read, write, read_points, scan

.. autoclass:: sunspec.core.client.ClientModel
    :members: load, read_points, write_points

.. autoclass:: sunspec.core.client.ClientBlock
    :members:

.. autoclass:: sunspec.core.client.ClientPoint
    :members: write

Exceptions
----------

.. exception:: SunSpecClientError

    Derived from :const:`sunspec.core.device.SunSpecError`. Raised for any
    sunspec module error in sunspec.core.client classes.

Constants
---------

*Device Types*

.. data:: RTU
.. data:: TCP
.. data:: MAPPED

*RTU Device Parity*

.. data:: PARITY_NONE
.. data:: PARITY_EVEN

:mod:`sunspec.core.device` --- SunSpec Device classes
=====================================================

.. module:: sunspec.core.device

The device module provides the base SunSpec device functionality. A SunSpec
device consists of a set of SunSpec models which contain blocks and points as
specified in the respective SunSpec model definitions.

Classes
-------

.. autoclass:: sunspec.core.device.Device
    :members: add_model, from_pics, to_pics, not_equal

.. autoclass:: sunspec.core.device.Model
    :members: load, from_pics, to_pics, not_equal

.. autoclass:: sunspec.core.device.Block
    :members: from_pics, to_pics, not_equal

.. autoclass:: sunspec.core.device.Point
    :members: from_pics, to_pics, not_equal

.. autoclass:: sunspec.core.device.ModelType
    :members: from_smdx, not_equal

.. autoclass:: sunspec.core.device.BlockType
    :members: from_smdx, not_equal

.. autoclass:: sunspec.core.device.PointType
    :members: from_smdx, not_equal

Exceptions
----------

.. exception:: SunSpecError

    Raised for sunspec.core.device errors.

:mod:`sunspec.core.modbus` --- SunSpec Modbus Package
========================================================

The Modbus package provides standard Modbus support for Modbus RTU, Modbus TCP, and Modbus file mapped client devices.

:mod:`sunspec.core.modbus.client` --- Modbus Client classes
===========================================================

.. module:: sunspec.core.modbus.client

Classes
-------

.. autoclass:: sunspec.core.modbus.client.ModbusClientDeviceRTU
    :members: close, read, write

.. autoclass:: sunspec.core.modbus.client.ModbusClientDeviceTCP
    :members: connect, disconnect, close, read, write

.. autoclass:: sunspec.core.modbus.client.ModbusClientDeviceMapped
    :members: close, read, write

.. autoclass:: sunspec.core.modbus.client.ModbusClientRTU
    :members: open, close, add_device, remove_device, read, write

Exceptions
----------

.. exception:: ModbusClientError

    Raised for general errors in sunspec.core.modbus.client modules.

.. exception:: ModbusClientTimeout

    Raised for Modbus timeout errors. Derived from :const:`ModbusClientError`.

.. exception:: ModbusClientException

    Raised for Modbus protocol exceptions. Derived from :const:`ModbusClientError`.

Constants
---------

*Parity*

.. data:: PARITY_NONE
.. data:: PARITY_EVEN

*Read Modbus Functions*

.. data:: FUNC_READ_HOLDING
.. data:: FUNC_READ_INPUT

:mod:`sunspec.core.modbus.mbmap` --- Modbus Map classes
========================================================

The mbmap module implements a local Modbus map image. The map supports read and write operations and can be used by Modbus clients
in place of an actual modbus device. The module supports an xml encoding for representing modbus maps as a document.

The xml representation has a root element of *mbmap* that contains a set of *regs* elements representing one or more registers in the map.
Currently only big endian is supported.

Attributes for *mbmap* element:

+-----------+--------------------------------------------+-------------------------------+----------------------+
| Attribute | Description                                | Valid values                  | Default value        |
+===========+============================================+===============================+======================+
| addr      | Base Modbus address                        | Valid modbus address          | 40000                |
+-----------+--------------------------------------------+-------------------------------+----------------------+
| func      | Modbus function associated with the map    | holding, input                | holding              |
+-----------+--------------------------------------------+-------------------------------+----------------------+

Attributes for *regs* element:

+-----------+--------------------------------------------+-------------------------------+----------------------+
| Attribute | Description                                | Valid values                  | Default value        |
+===========+============================================+===============================+======================+
| offset    | Register offset                            | Value with map length         | Next offset          |
+-----------+--------------------------------------------+-------------------------------+----------------------+
| type      | Register(s) type                           | s16, u16, s32, u32, s64, u64, | hexstr               |
|           |                                            | f32, f64, string, hexstr      |                      |
+-----------+--------------------------------------------+-------------------------------+----------------------+
| len       | String length for string type              | Value within map length       | Length of the *regs* |
|           |                                            |                               | element value        |
+-----------+--------------------------------------------+-------------------------------+----------------------+

If the registers are contiguous, offset is optional.

The *hexstr* type is a series of ascii hex characters. Spaces are removed from the string before processing and
can be used to increase readability.

Example::

    <mbmap>
      <!-- common model -->
      <regs type="string" len="2">SunS</regs>
      <regs type="u16">1</regs>
      <regs type="u16">66</regs>
      <regs type="string" len="16">SunSpecTest</regs>
      <regs type="string" len="16">TestInverter-1</regs>
      <regs type="string" len="8">opt_a_b_c</regs>
      <regs type="string" len="8">1.2.3</regs>
      <regs type="string" len="16">sn-123456789</regs>
      <regs type="u16">1</regs>
      <regs type="u16">0</regs>

      <!-- short test model -->
      <regs type="u16">63010</regs>
      <regs type="u16">4</regs>

      <!-- example of hexstr -->
      <regs>00 79 00 1E</regs>
      <regs>0079 001E</regs>

      <!-- end of models -->
      <regs type="u16">0xffff</regs>
      <regs type="u16">0</regs>
    </mbmap>

.. module:: sunspec.core.modbus.mbmap

Classes
-------

.. autoclass:: sunspec.core.modbus.mbmap.ModbusMap
    :members: from_xml, read, write, not_equal

.. autoclass:: sunspec.core.modbus.mbmap.ModbusMapRegs
    :members: read, write, append, not_equal

Exceptions
----------

.. exception:: ModbusMapError

    Raised for errors in sunspec.core.modbus.mbmap modules.

Constants
---------

*Modbus Map Functions*

.. attribute:: MBMAP_FUNC_INPUT
.. attribute:: MBMAP_FUNC_HOLDING
